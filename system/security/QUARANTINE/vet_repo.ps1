<#
.SYNOPSIS
    AI OS Repository Vetting Script - Strix Security Protocol v2.0
.DESCRIPTION
    Scans a cloned repository in QUARANTINE for malware indicators,
    data exfiltration patterns, suspicious dependencies, and git hook injections.
    Must PASS before any content is moved into AI OS ecosystem.
    QUARANTINE path: <AI_OS_ROOT>\security\QUARANTINE\
.PARAMETER RepoPath
    Full path to the quarantined repo (e.g., <AI_OS_ROOT>\security\QUARANTINE\incoming\repos\repo-name)
.PARAMETER Verbose
    Show detailed scan output
.EXAMPLE
    .\vet_repo.ps1 -RepoPath "<AI_OS_ROOT>\security\QUARANTINE\incoming\repos\everything-claude-code"
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$RepoPath,
    [switch]$VerboseOutput
)

# CONFIGURATION
$script:Findings = @()
$script:CriticalCount = 0
$script:WarnCount = 0
$ReportPath = Join-Path $RepoPath "_VET_REPORT.md"

function Add-Finding {
    param([string]$Level, [string]$Category, [string]$Detail, [string]$File = "")
    $script:Findings += [PSCustomObject]@{
        Level    = $Level
        Category = $Category
        Detail   = $Detail
        File     = $File
    }
    if ($Level -eq "CRITICAL") { $script:CriticalCount++ }
    if ($Level -eq "WARN")     { $script:WarnCount++ }
    if ($VerboseOutput) {
        $color = if ($Level -eq "CRITICAL") { "Red" } elseif ($Level -eq "WARN") { "Yellow" } else { "Green" }
        Write-Host "  [$Level] $Category - $Detail" -ForegroundColor $color
    }
}

# VALIDATION
Write-Host ""
Write-Host "=== AI OS STRIX SECURITY VET - v2.0 (12-STAGE) ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Target: $RepoPath" -ForegroundColor White

if (-not (Test-Path $RepoPath)) {
    Write-Host "[ERROR] Path does not exist: $RepoPath" -ForegroundColor Red
    exit 1
}

$RepoName = Split-Path $RepoPath -Leaf
Write-Host "Scanning: $RepoName" -ForegroundColor White
Write-Host ""

# SCAN 1: GIT HOOKS (HIGH PRIORITY)
Write-Host "[1/7] Scanning .git/hooks..." -ForegroundColor Cyan
$hooksPath = Join-Path $RepoPath ".git\hooks"
if (Test-Path $hooksPath) {
    $hooks = @(Get-ChildItem $hooksPath | Where-Object { -not $_.Name.EndsWith(".sample") })
    if ($hooks.Count -gt 0) {
        foreach ($hook in $hooks) {
            Add-Finding "CRITICAL" "GIT_HOOK" "Executable hook found: $($hook.Name)" $hook.FullName
        }
        Write-Host "  >> DELETE all non-.sample hooks before any git operations!" -ForegroundColor Red
    } else {
        Add-Finding "PASS" "GIT_HOOK" "No active hooks found"
        Write-Host "  >> OK: No active hooks" -ForegroundColor Green
    }
}

# SCAN 2: PACKAGE.JSON - DANGEROUS SCRIPTS
Write-Host "[2/7] Scanning package.json lifecycle scripts..." -ForegroundColor Cyan
$packageFiles = @(Get-ChildItem $RepoPath -Name "package.json" -Recurse |
    Where-Object { $_ -notmatch "node_modules" })

foreach ($pkgFile in $packageFiles) {
    $pkgPath = Join-Path $RepoPath $pkgFile
    $content = Get-Content $pkgPath -Raw | ConvertFrom-Json -ErrorAction SilentlyContinue
    if ($content.scripts) {
        $dangerousScripts = @("preinstall", "postinstall", "prepare", "prepublish")
        foreach ($s in $dangerousScripts) {
            $scriptValue = $null
            try { $scriptValue = $content.scripts.PSObject.Properties[$s].Value } catch {}
            if ($scriptValue) {
                if ($scriptValue -match "curl|wget|http[s]?://|Invoke-WebRequest") {
                    Add-Finding "CRITICAL" "NPM_SCRIPT" "$s script makes network call: $scriptValue" $pkgPath
                } else {
                    Add-Finding "WARN" "NPM_SCRIPT" "$s script exists (review manually): $scriptValue" $pkgPath
                }
            }
        }
        Write-Host "  >> Found package.json: $pkgFile" -ForegroundColor Yellow
    }
}
if ($packageFiles.Count -eq 0) {
    Write-Host "  >> No package.json found (no npm risk)" -ForegroundColor Green
}

# SCAN 3: NETWORK CALL PATTERNS
Write-Host "[3/7] Scanning for network exfiltration patterns..." -ForegroundColor Cyan
$networkPatterns = @(
    @{ Pattern = 'curl\s+https?://'; Label = "curl to external URL" },
    @{ Pattern = 'wget\s+https?://'; Label = "wget to external URL" },
    @{ Pattern = 'Invoke-WebRequest.*https?://'; Label = "PowerShell web request" },
    @{ Pattern = "fetch\([`"']https?://(?!localhost|127\.0\.0\.1)"; Label = "JS fetch to external" },
    @{ Pattern = "requests\.(post|get)\([`"']https?://(?!localhost)"; Label = "Python requests to external" },
    @{ Pattern = "axios\.(post|get)\([`"']https?://(?!localhost)"; Label = "axios to external" }
)

$sourceExtensions = @("*.js", "*.ts", "*.py", "*.sh", "*.ps1", "*.bat", "*.rb")
$excludeDirs = @("node_modules", ".git", "__pycache__", "dist", "build")

$allSourceFiles = @()
foreach ($ext in $sourceExtensions) {
    $files = Get-ChildItem $RepoPath -Filter $ext -Recurse -ErrorAction SilentlyContinue |
        Where-Object {
            $path = $_.FullName
            -not ($excludeDirs | Where-Object { $path -match [regex]::Escape($_) })
        }
    $allSourceFiles += $files
}

$networkHits = 0
foreach ($file in $allSourceFiles) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }
    foreach ($check in $networkPatterns) {
        if ($content -match $check.Pattern) {
            Add-Finding "WARN" "NETWORK_CALL" $check.Label $file.FullName
            $networkHits++
        }
    }
}
if ($networkHits -eq 0) {
    Write-Host "  >> No suspicious network calls found" -ForegroundColor Green
} else {
    Write-Host "  >> $networkHits potential network call(s) flagged - review manually" -ForegroundColor Yellow
}

# SCAN 4: SENSITIVE DATA ACCESS PATTERNS
Write-Host "[4/7] Scanning for sensitive data access..." -ForegroundColor Cyan
$sensitivePatterns = @(
    @{ Pattern = '\.ssh[/\\]|id_rsa|authorized_keys'; Label = "SSH key access" },
    @{ Pattern = '\.aws[/\\]credentials|AWS_SECRET'; Label = "AWS credentials access" },
    @{ Pattern = 'APPDATA|%USERPROFILE%|Path\.home\(\)|os\.path\.expanduser'; Label = "User profile path access" },
    @{ Pattern = '\.env\b|dotenv'; Label = ".env file access" },
    @{ Pattern = 'os\.getenv|process\.env\.|environ\['; Label = "Environment variable access" }
)

$sensitiveHits = 0
foreach ($file in $allSourceFiles) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }
    foreach ($check in $sensitivePatterns) {
        if ($content -match $check.Pattern) {
            Add-Finding "WARN" "SENSITIVE_ACCESS" $check.Label $file.FullName
            $sensitiveHits++
            break
        }
    }
}
if ($sensitiveHits -eq 0) {
    Write-Host "  >> No suspicious data access patterns" -ForegroundColor Green
} else {
    Write-Host "  >> $sensitiveHits sensitive access pattern(s) found - review context" -ForegroundColor Yellow
}

# SCAN 5: CODE OBFUSCATION / EXECUTION PATTERNS
Write-Host "[5/7] Scanning for obfuscation and dynamic execution..." -ForegroundColor Cyan
$obfuscationPatterns = @(
    @{ Pattern = 'eval\s*\('; Label = "eval dynamic execution" },
    @{ Pattern = 'exec\s*\('; Label = "exec dynamic execution" },
    @{ Pattern = 'os\.system\s*\('; Label = "os.system shell execution" },
    @{ Pattern = 'subprocess\.(run|Popen|call)'; Label = "subprocess shell execution" },
    @{ Pattern = 'base64\.decode|atob\(|Buffer\.from.*base64'; Label = "Base64 decode potential obfuscation" },
    @{ Pattern = '\\x[0-9a-fA-F]{2}\\x[0-9a-fA-F]{2}\\x[0-9a-fA-F]{2}'; Label = "Hex-encoded string obfuscation" },
    @{ Pattern = 'String\.fromCharCode'; Label = "Char code obfuscation" }
)

$obfuscationHits = 0
foreach ($file in $allSourceFiles) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }
    foreach ($check in $obfuscationPatterns) {
        if ($content -match $check.Pattern) {
            if ($check.Label -match "Base64" -and $file.Name -match "\.(md|txt|json)$") { continue }
            Add-Finding "WARN" "OBFUSCATION" $check.Label $file.FullName
            $obfuscationHits++
            break
        }
    }
}
if ($obfuscationHits -eq 0) {
    Write-Host "  >> No obfuscation patterns found" -ForegroundColor Green
} else {
    Write-Host "  >> $obfuscationHits obfuscation pattern(s) - verify these are legitimate" -ForegroundColor Yellow
}

# SCAN 6: HARDCODED SECRETS
Write-Host "[6/7] Scanning for hardcoded secrets and tokens..." -ForegroundColor Cyan
$secretPatterns = @(
    @{ Pattern = 'sk-[a-zA-Z0-9]{32,}'; Label = "Possible API key (sk-....)" },
    @{ Pattern = 'ghp_[a-zA-Z0-9]{36}'; Label = "GitHub Personal Access Token" },
    @{ Pattern = 'AKIA[0-9A-Z]{16}'; Label = "AWS Access Key ID" },
    @{ Pattern = "password\s*=\s*[`"'][^`"']{8,}[`"']"; Label = "Hardcoded password" },
    @{ Pattern = "secret\s*=\s*[`"'][^`"']{8,}[`"']"; Label = "Hardcoded secret" },
    @{ Pattern = "token\s*=\s*[`"'][^`"']{20,}[`"']"; Label = "Hardcoded token" }
)

$secretHits = 0
$allFiles = Get-ChildItem $RepoPath -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Extension -in @(".js", ".ts", ".py", ".env", ".yml", ".yaml", ".json", ".ps1", ".sh") -and
                   $_.FullName -notmatch "node_modules|\.git" }

foreach ($file in $allFiles) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }
    foreach ($check in $secretPatterns) {
        if ($content -match $check.Pattern) {
            Add-Finding "CRITICAL" "HARDCODED_SECRET" $check.Label $file.FullName
            $secretHits++
            break
        }
    }
}
if ($secretHits -eq 0) {
    Write-Host "  >> No hardcoded secrets detected" -ForegroundColor Green
} else {
    Write-Host "  >> $secretHits hardcoded secret(s) found!" -ForegroundColor Red
}

# SCAN 7: FILE PERMISSIONS & SUSPICIOUS EXECUTABLES
Write-Host "[7/12] Scanning for suspicious executable files..." -ForegroundColor Cyan
$suspiciousExtensions = @(".exe", ".dll", ".com", ".msi", ".scr", ".vbs", ".hta", ".pif", ".cpl", ".jar", ".wsf", ".jse")
$suspiciousFiles = @(Get-ChildItem $RepoPath -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $suspiciousExtensions -contains $_.Extension -and $_.FullName -notmatch "\.git" })

if ($suspiciousFiles.Count -gt 0) {
    foreach ($f in $suspiciousFiles) {
        Add-Finding "CRITICAL" "SUSPICIOUS_BINARY" "Binary/executable file found: $($f.Name)" $f.FullName
    }
    Write-Host "  >> $($suspiciousFiles.Count) suspicious binary file(s) found!" -ForegroundColor Red
} else {
    Write-Host "  >> No suspicious executables" -ForegroundColor Green
}

# SCAN 8: BLOCKCHAIN / CRYPTO MINER PATTERNS (NEW v2.0)
Write-Host "[8/12] Scanning for blockchain/cryptominer/wallet exfiltration..." -ForegroundColor Cyan
$blockchainPatterns = @(
    @{ Level = "CRITICAL"; Pattern = 'CryptoNight|stratum\+tcp|xmrig|monero.*mine|coinhive|cryptoloot'; Label = "Cryptominer code detected" },
    @{ Level = "CRITICAL"; Pattern = 'private_key|privateKey.*wallet|seed_phrase|mnemonic.*wallet|keystore.*crypto'; Label = "Crypto wallet private key access" },
    @{ Level = "CRITICAL"; Pattern = 'web3\.eth\.accounts\.privateKeyToAccount|from_key\(|sign_transaction.*private'; Label = "Web3 private key signing" },
    @{ Level = "WARN";     Pattern = 'ethers\.Wallet\(|web3\.eth\.getBalance|solana.*keypair|phantom.*connect'; Label = "Blockchain wallet interaction" },
    @{ Level = "WARN";     Pattern = 'bitcoin|ethereum|solana|binance.*bnb|metamask.*inject'; Label = "Cryptocurrency reference (verify context)" },
    @{ Level = "WARN";     Pattern = 'mining.*pool|hashrate|nonce.*block|proof.of.work|gpu.*mine'; Label = "Mining/PoW pattern" }
)

$cryptoHits = 0
foreach ($file in $allSourceFiles) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }
    foreach ($check in $blockchainPatterns) {
        if ($content -match $check.Pattern) {
            Add-Finding $check.Level "CRYPTO_BLOCKCHAIN" $check.Label $file.FullName
            $cryptoHits++
            break
        }
    }
}
if ($cryptoHits -eq 0) {
    Write-Host "  >> No crypto/blockchain threats detected" -ForegroundColor Green
} else {
    Write-Host "  >> $cryptoHits crypto/blockchain pattern(s) found -- REVIEW IMMEDIATELY" -ForegroundColor Red
}

# SCAN 9: COOKIE / SESSION / BROWSER DATA THEFT (NEW v2.0)
Write-Host "[9/12] Scanning for cookie/session/browser data theft..." -ForegroundColor Cyan
$cookiePatterns = @(
    @{ Level = "CRITICAL"; Pattern = 'document\.cookie|localStorage\.getItem|sessionStorage\.getItem|indexedDB.*open'; Label = "Browser storage read (possible theft)" },
    @{ Level = "CRITICAL"; Pattern = 'Chrome.*Login Data|Firefox.*cookies\.sqlite|AppData.*Cookies|\\Cookies\\Cookies'; Label = "Browser cookie file access" },
    @{ Level = "CRITICAL"; Pattern = 'steal.*cookie|harvest.*token|exfil.*session|dump.*browser'; Label = "Explicit cookie/session theft keyword" },
    @{ Level = "CRITICAL"; Pattern = 'discord.*token|telegram.*session|whatsapp.*key|slack.*token.*steal'; Label = "Messenger token exfiltration" },
    @{ Level = "WARN";     Pattern = 'Set-Cookie|getCookie\(|parseCookies|cookie.*httpOnly'; Label = "Cookie manipulation (verify purpose)" },
    @{ Level = "WARN";     Pattern = '\$_COOKIE|request\.cookies|flask.*session|express.*cookie'; Label = "Server-side cookie access" }
)

$cookieHits = 0
$allFilesBroad = Get-ChildItem $RepoPath -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Extension -in @(".js", ".ts", ".py", ".php", ".rb", ".sh", ".ps1", ".cs", ".go") -and
                   $_.FullName -notmatch "node_modules|\.git|__pycache__" }

foreach ($file in $allFilesBroad) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }
    foreach ($check in $cookiePatterns) {
        if ($content -match $check.Pattern) {
            Add-Finding $check.Level "COOKIE_SESSION_THEFT" $check.Label $file.FullName
            $cookieHits++
            break
        }
    }
}
if ($cookieHits -eq 0) {
    Write-Host "  >> No cookie/session theft patterns" -ForegroundColor Green
} else {
    Write-Host "  >> $cookieHits cookie/session pattern(s) -- REVIEW" -ForegroundColor Red
}

# SCAN 10: HIDDEN / STEGANOGRAPHY / ENCODED PAYLOAD (NEW v2.0)
Write-Host "[10/12] Scanning for hidden payloads and steganography..." -ForegroundColor Cyan
$hiddenPatterns = @(
    @{ Level = "CRITICAL"; Pattern = '\\u[0-9a-fA-F]{4}\\u[0-9a-fA-F]{4}\\u[0-9a-fA-F]{4}'; Label = "Unicode escape sequence chain (obfuscation)" },
    @{ Level = "CRITICAL"; Pattern = 'fromCharCode.*fromCharCode.*fromCharCode'; Label = "Multiple fromCharCode chaining (obfuscation)" },
    @{ Level = "CRITICAL"; Pattern = '(?s)eval\(.*base64.*\)'; Label = "eval(base64(...)) payload" },
    @{ Level = "CRITICAL"; Pattern = 'powershell.*-enc |powershell.*-EncodedCommand |iex\s*\('; Label = "PowerShell encoded command execution" },
    @{ Level = "CRITICAL"; Pattern = '\$env:TEMP.*\.exe|%TEMP%.*\.exe|/tmp/.*chmod.*\+x'; Label = "Temp dir executable drop" },
    @{ Level = "WARN";     Pattern = 'zlib\.decompress|gzip\.decompress|lzma\.decompress'; Label = "Compressed payload decompression" },
    @{ Level = "WARN";     Pattern = 'PIL\.Image.*LSB|steganograph|stegano|hide.*pixel'; Label = "Image steganography pattern" },
    @{ Level = "WARN";     Pattern = 'reflect\.Type|runtime\.GOARCH|Unsafe\.Pointer|unsafe\.Slice'; Label = "Unsafe runtime reflection (Go/Rust)" }
)

$hiddenHits = 0
foreach ($file in $allFilesBroad) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }
    foreach ($check in $hiddenPatterns) {
        if ($content -match $check.Pattern) {
            Add-Finding $check.Level "HIDDEN_PAYLOAD" $check.Label $file.FullName
            $hiddenHits++
            break
        }
    }
}
if ($hiddenHits -eq 0) {
    Write-Host "  >> No hidden/steganography patterns" -ForegroundColor Green
} else {
    Write-Host "  >> $hiddenHits hidden payload pattern(s) -- CRITICAL REVIEW REQUIRED" -ForegroundColor Red
}

# SCAN 11: SUPPLY CHAIN / DEPENDENCY CONFUSION (NEW v2.0)
Write-Host "[11/12] Scanning for supply chain attack indicators..." -ForegroundColor Cyan
$supplyChainHits = 0

# Check for suspicious registry/mirror override in package config files
$configFiles = Get-ChildItem $RepoPath -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -in @(".npmrc", ".yarnrc", "pip.conf", "setup.cfg", "pyproject.toml") -and
                   $_.FullName -notmatch "\.git" }

foreach ($cfg in $configFiles) {
    $content = Get-Content $cfg.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }
    # Override npm/pip registry = potential dependency confusion
    if ($content -match 'registry\s*=\s*https?://(?!registry\.npmjs\.org|pypi\.org|files\.pythonhosted)') {
        Add-Finding "CRITICAL" "SUPPLY_CHAIN" "Non-standard package registry override in $($cfg.Name)" $cfg.FullName
        $supplyChainHits++
    }
    if ($content -match 'always-auth\s*=\s*true|_auth\s*=') {
        Add-Finding "WARN" "SUPPLY_CHAIN" "Auto-auth in $($cfg.Name) -- may expose tokens to custom registry" $cfg.FullName
        $supplyChainHits++
    }
}

# Check package.json for known dangerous dependency patterns
foreach ($pkgFile in $packageFiles) {
    $content = Get-Content (Join-Path $RepoPath $pkgFile) -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }
    # Suspicious: install scripts that call external URLs combined with unpublished-looking versions
    if ($content -match '"version"\s*:\s*"0\.0\.1"|"private"\s*:\s*false') {
        Add-Finding "WARN" "SUPPLY_CHAIN" "Very low version + public flag in package.json" (Join-Path $RepoPath $pkgFile)
        $supplyChainHits++
    }
}

if ($supplyChainHits -eq 0) {
    Write-Host "  >> No supply chain indicators found" -ForegroundColor Green
} else {
    Write-Host "  >> $supplyChainHits supply chain indicator(s) -- INVESTIGATE" -ForegroundColor Red
}

# SCAN 12: LARGE BINARY BLOBS (potential hidden data/stego) (NEW v2.0)
Write-Host "[12/12] Scanning for suspicious large binary blobs..." -ForegroundColor Cyan
$binaryBlobFiles = Get-ChildItem $RepoPath -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object {
        $_.Extension -in @(".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".zip", ".tar", ".gz", ".7z", ".bin", ".dat") -and
        $_.FullName -notmatch "\.git" -and
        $_.Length -gt 5MB
    }

if ($binaryBlobFiles.Count -gt 0) {
    foreach ($blob in $binaryBlobFiles) {
        $sizeMB = [Math]::Round($blob.Length / 1MB, 1)
        Add-Finding "WARN" "BINARY_BLOB" "Large binary ($($sizeMB)MB) -- verify not carrying hidden payload: $($blob.Name)" $blob.FullName
    }
    Write-Host "  >> $($binaryBlobFiles.Count) large binary file(s) found -- verify they are legitimate" -ForegroundColor Yellow
} else {
    Write-Host "  >> No suspicious large binary blobs" -ForegroundColor Green
}

# GENERATE REPORT
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$status = if ($script:CriticalCount -gt 0) { "FAIL" }
          elseif ($script:WarnCount -gt 5) { "WARN" }
          else { "PASS" }

$statusColor = if ($status -eq "FAIL") { "Red" } elseif ($status -eq "WARN") { "Yellow" } else { "Green" }

Write-Host ""
Write-Host "=== RESULT: $status | Critical: $($script:CriticalCount) | Warnings: $($script:WarnCount) ===" -ForegroundColor $statusColor

$verdictText = ""
if ($status -eq "PASS") {
    $verdictText = "PASS - Repo passed all security checks. Safe to extract specific files into AI OS."
} elseif ($status -eq "WARN") {
    $verdictText = "WARN - Warnings found. Manual review required before ingestion. See findings below."
} else {
    $verdictText = "FAIL - Critical issues found. DO NOT ingest into AI OS until resolved."
}

$nextStepText = ""
if ($status -eq "PASS") {
    $nextStepText = @"
Step 3.5 — content-analyst-agent (open-notebook) sẽ chạy tự động:
  gitingest $RepoPath | open-notebook (localhost:5055)
  6 CIV questions: purpose / conflict / dept / risk / gap_domain / proposed_agent
  Output: $RepoPath\_CIV_ANALYSIS.md

Sau khi _CIV_ANALYSIS.md hoàn tất:
  APPROVED + no gap  → copy cần thiết vào destination
  APPROVED + gap     → Step 3.6 GAP PROPOSAL → CEO qua Telegram
  REJECTED           → move to security/QUARANTINE/rejected/
"@
} elseif ($status -eq "WARN") {
    $nextStepText = "Review each WARN item manually. If comfortable, proceed with caution. Document your review decision."
} else {
    $nextStepText = "STOP. Review CRITICAL items. Delete quarantine folder if unsolvable: Remove-Item -Recurse -Force '$RepoPath'"
}

$findingsTable = $script:Findings | ForEach-Object {
    "| $($_.Level) | $($_.Category) | $($_.Detail) | ``$($_.File)`` |"
} | Out-String

$reportContent = @"
# Strix Vet Report: $RepoName
**Date:** $timestamp
**Status:** $status
**Critical Findings:** $($script:CriticalCount)
**Warnings:** $($script:WarnCount)

## Verdict

$verdictText

## Findings

| Level | Category | Detail | File |
|-------|----------|--------|------|
$findingsTable

## Next Step

$nextStepText
"@

Set-Content -Path $ReportPath -Value $reportContent -Encoding UTF8
Write-Host ""
Write-Host "Report saved: $ReportPath" -ForegroundColor White
Write-Host ""

# Exit codes: 0=PASS, 1=WARN, 2=FAIL
if ($status -eq "FAIL") { exit 2 }
elseif ($status -eq "WARN") { exit 1 }
else { exit 0 }
