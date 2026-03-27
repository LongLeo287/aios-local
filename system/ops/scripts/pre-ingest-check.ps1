# pre-ingest-check.ps1 -- AI OS Layer 1 Pre-Ingest Protection
# Version: 1.2 | 2026-03-14
# Run BEFORE cloning any external repo into AI OS plugins/ or skills/
#
# INSPIRED BY:
#   TruffleHog (secret scanning), ZeroLeaks (leak detection),
#   PentestOPS (attack surface), Katana (recon), hintshell (shell injection)
#
# USAGE:
#   .\scripts\pre-ingest-check.ps1 -RepoUrl "https://github.com/owner/repo"
#   .\scripts\pre-ingest-check.ps1 -RepoUrl "https://github.com/owner/repo" -AutoApprove

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$RepoUrl,
    [switch]$SkipApiCheck,
    [switch]$AutoApprove
)

$ErrorActionPreference = "Stop"

# --- LOAD .env (never hardcode tokens) ---
$envFile = Join-Path $PSScriptRoot "..\\.env"
if (Test-Path $envFile) {
    Get-Content $envFile | Where-Object { $_ -match "^[^#].*=.+" } | ForEach-Object {
        $parts = $_ -split "=", 2
        if ($parts.Count -eq 2 -and $parts[1].Trim() -ne "") {
            [System.Environment]::SetEnvironmentVariable($parts[0].Trim(), $parts[1].Trim(), "Process")
        }
    }
}

# Build auth header - use GITHUB_TOKEN from .env if available
$ghToken = [System.Environment]::GetEnvironmentVariable("GITHUB_TOKEN", "Process")
$h = @{ "User-Agent" = "AI-OS-Security/1.0"; "Accept" = "application/vnd.github+json" }
if ($ghToken -and $ghToken.Length -gt 10) {
    $h["Authorization"] = "Bearer $ghToken"
    Write-Host "  [AUTH] GitHub token loaded from .env" -ForegroundColor DarkGray
} else {
    Write-Host "  [AUTH] No GITHUB_TOKEN found -- unauthenticated (60 req/hr limit)" -ForegroundColor DarkYellow
}

# ---  TRUSTED ORG LIST ---
$TRUSTED_ORGS = @(
    "vercel", "prisma", "shadcn-ui", "ant-design", "tailwindlabs",
    "microsoft", "google", "facebook", "meta", "anthropic",
    "nextlevelbuilder", "duthaho", "projectdiscovery", "trufflesecurity"
)

$DANGER_EXT = @(".exe", ".dll", ".bat", ".cmd", ".vbs", ".msi", ".pkg", ".dmg", ".pif", ".scr")

$SECRET_PATTERNS = @(
    "sk-[a-zA-Z0-9]{32}",
    "ghp_[a-zA-Z0-9]{36}",
    "AKIA[A-Z0-9]{16}",
    "AIza[0-9A-Za-z_-]{35}",
    "xoxb-[0-9]+-[0-9]+-[a-zA-Z0-9]+"
)

$INJECT_PATTERNS = @(
    "eval\s*\(",
    "exec\s*\(",
    "os\.system\s*\(",
    "shell=True",
    "base64\.b64decode",
    "pickle\.loads",
    "__import__\("
)

$SUSPICIOUS_NAMES = @("\.env$", "id_rsa", "id_ed25519", "\.pem$", "\.key$", "secret", "credential", "token", "password")

# --- HELPERS ---
function Write-Pass { param([string]$m) Write-Host "  [OK] $m" -ForegroundColor Green }
function Write-Warn { param([string]$m) Write-Host "  [!!] $m" -ForegroundColor Yellow }
function Write-Fail { param([string]$m) Write-Host "  [XX] $m" -ForegroundColor Red }
function Write-Info { param([string]$m) Write-Host "       $m" -ForegroundColor Gray }

# --- PARSE URL ---
if ($RepoUrl -match "github\.com/([a-zA-Z0-9_.-]+)/([a-zA-Z0-9_.-]+)") {
    $owner = $Matches[1]
    $repo  = $Matches[2] -replace "\.git$", ""
} else {
    Write-Host "[ERROR] Invalid GitHub URL: $RepoUrl" -ForegroundColor Red
    exit 1
}

$apiBase = "https://api.github.com/repos/$owner/$repo"

Write-Host ""
Write-Host "=================================================" -ForegroundColor Magenta
Write-Host "  AI OS -- Layer 1 Pre-Ingest Security Check"      -ForegroundColor Magenta
Write-Host "=================================================" -ForegroundColor Magenta
Write-Host "  Repo  : $owner/$repo"
Write-Host "  Time  : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host ""

$score   = 0
$issues  = [System.Collections.ArrayList]@()
$warns   = [System.Collections.ArrayList]@()
$ok      = [System.Collections.ArrayList]@()

# ============================
# CHECK 1: Repo Reputation
# ============================
Write-Host "--- [1] Repo Reputation ---" -ForegroundColor White

if (-not $SkipApiCheck) {
    try {
        $ri = Invoke-RestMethod -Uri $apiBase -Headers $h -TimeoutSec 15

        # Stars
        $stars = $ri.stargazers_count
        if ($stars -ge 1000) {
            Write-Pass "Stars: $stars (high credibility)"
            $score += 25; $null = $ok.Add("High stars ($stars)")
        } elseif ($stars -ge 50) {
            Write-Warn "Stars: $stars (moderate)"
            $score += 10; $null = $warns.Add("Moderate stars ($stars)")
        } else {
            Write-Fail "Stars: $stars (very low)"
            $null = $issues.Add("Very low star count ($stars)")
        }

        # Age
        $created = [datetime]$ri.created_at
        $ageMonths = [math]::Round(((Get-Date) - $created).TotalDays / 30)
        if ($ageMonths -ge 12) {
            Write-Pass "Age: $ageMonths months old"
            $score += 15; $null = $ok.Add("Established ($ageMonths months)")
        } elseif ($ageMonths -ge 3) {
            Write-Warn "Age: $ageMonths months (relatively new)"
            $score += 5; $null = $warns.Add("New repo ($ageMonths months)")
        } else {
            Write-Fail "Age: $ageMonths months (very new)"
            $null = $issues.Add("Very new repo (< 3 months)")
        }

        # Fork
        if ($ri.fork) {
            Write-Warn "This is a FORK -- verify the original"
            $score -= 5; $null = $warns.Add("Forked repo")
        } else {
            Write-Pass "Original repo (not a fork)"
            $score += 5; $null = $ok.Add("Not a fork")
        }

        # Archived
        if ($ri.archived) {
            Write-Warn "Repo is ARCHIVED (no active maintenance)"
            $null = $warns.Add("Archived")
        } else {
            Write-Pass "Active (not archived)"
            $null = $ok.Add("Active repo")
        }

        # Last push
        $lastPush = [datetime]$ri.pushed_at
        $daysSince = [math]::Round(((Get-Date) - $lastPush).TotalDays)
        if ($daysSince -le 180) {
            Write-Pass "Last push: $daysSince days ago"
            $null = $ok.Add("Recently updated ($daysSince days)")
        } else {
            Write-Warn "Last push: $daysSince days ago (stale)"
            $null = $warns.Add("Stale ($daysSince days since update)")
        }

    } catch {
        Write-Warn "API check skipped: $($_.Exception.Message)"
        $score += 10; $null = $warns.Add("API check skipped")
    }
} else {
    Write-Warn "--SkipApiCheck flag set"
}

# ============================
# CHECK 2: Trusted Author
# ============================
Write-Host ""
Write-Host "--- [2] Source Trust ---" -ForegroundColor White

$ownerLower = $owner.ToLower()
$isTrusted = $false
foreach ($org in $TRUSTED_ORGS) {
    if ($ownerLower -eq $org.ToLower()) { $isTrusted = $true; break }
}

if ($isTrusted) {
    Write-Pass "Author '$owner' is in AI OS trusted list"
    $score += 20; $null = $ok.Add("Trusted org: $owner")
} else {
    Write-Warn "Author '$owner' NOT in trusted list -- manual review needed"
    $null = $warns.Add("Unknown author: $owner")
}

# ============================
# CHECK 3: Dangerous Files
# ============================
Write-Host ""
Write-Host "--- [3] Dangerous File Detection ---" -ForegroundColor White

if (-not $SkipApiCheck) {
    try {
        $treeUrl = "$apiBase/git/trees/HEAD?recursive=1"
        $tree = Invoke-RestMethod -Uri $treeUrl -Headers $h -TimeoutSec 20
        $files = $tree.tree | Where-Object { $_.type -eq "blob" } | Select-Object -ExpandProperty path

        $dangerFound = [System.Collections.ArrayList]@()
        $suspFound   = [System.Collections.ArrayList]@()

        foreach ($f in $files) {
            $ext   = [System.IO.Path]::GetExtension($f).ToLower()
            $fname = [System.IO.Path]::GetFileName($f).ToLower()

            if ($DANGER_EXT -contains $ext) { $null = $dangerFound.Add($f) }

            foreach ($pat in $SUSPICIOUS_NAMES) {
                if ($fname -match $pat) { $null = $suspFound.Add($f); break }
            }
        }

        if ($dangerFound.Count -eq 0) {
            Write-Pass "No dangerous executables (.exe .dll .bat .cmd .msi)"
            $score += 15; $null = $ok.Add("No dangerous executables")
        } else {
            Write-Fail "DANGEROUS files found ($($dangerFound.Count)):"
            $dangerFound | ForEach-Object { Write-Info "  >> $_" }
            $null = $issues.Add("Executables: $($dangerFound -join '; ')")
        }

        if ($suspFound.Count -eq 0) {
            Write-Pass "No suspicious filenames (.env .key id_rsa secret/token/password)"
            $score += 10; $null = $ok.Add("No suspicious filenames")
        } else {
            Write-Warn "Suspicious files ($($suspFound.Count)):"
            $suspFound | Select-Object -First 5 | ForEach-Object { Write-Info "  >> $_" }
            $null = $warns.Add("Suspicious filenames: $($suspFound -join '; ')")
        }

        Write-Info "Files scanned: $($files.Count)"

    } catch {
        Write-Warn "File tree scan failed: $($_.Exception.Message)"
        $null = $warns.Add("File scan skipped")
    }
}

# ============================
# CHECK 4: Secret Scan (TruffleHog-style)
# ============================
Write-Host ""
Write-Host "--- [4] Secret / Credential Scan ---" -ForegroundColor White

try {
    $rmResp = Invoke-RestMethod -Uri "$apiBase/readme" -Headers $h -TimeoutSec 15
    $rmContent = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($rmResp.content))

    $secretFound = $false
    foreach ($pat in $SECRET_PATTERNS) {
        if ($rmContent -match $pat) {
            Write-Fail "Secret pattern found in README: $pat"
            $null = $issues.Add("Suspected secret in README ($pat)")
            $secretFound = $true
        }
    }

    if (-not $secretFound) {
        Write-Pass "No hardcoded secrets in README"
        $score += 10; $null = $ok.Add("Clean README")
    }
} catch {
    Write-Warn "README secret scan skipped: $($_.Exception.Message)"
    $null = $warns.Add("README scan skipped")
}

# ============================
# CHECK 5: Shell Injection (hintshell-style)
# ============================
Write-Host ""
Write-Host "--- [5] Shell Injection Risk ---" -ForegroundColor White

try {
    $topLevel = Invoke-RestMethod -Uri "$apiBase/contents" -Headers $h -TimeoutSec 10
    $scriptFiles = $topLevel | Where-Object { $_.type -eq "file" -and $_.name -match "\.(py|sh|bash|rb)$" }

    if ($scriptFiles.Count -eq 0) {
        Write-Pass "No script files at root level"
        $score += 10; $null = $ok.Add("No root-level scripts")
    } else {
        Write-Warn "$($scriptFiles.Count) root-level script(s) -- scanning..."
        $injFound = $false
        foreach ($sf in $scriptFiles | Select-Object -First 5) {
            try {
                $sc = Invoke-RestMethod -Uri $sf.url -Headers $h -TimeoutSec 10
                $content = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($sc.content))
                foreach ($pat in $INJECT_PATTERNS) {
                    if ($content -match $pat) {
                        Write-Warn "  Injection pattern '$pat' in $($sf.name)"
                        $null = $warns.Add("Shell injection pattern in $($sf.name)")
                        $injFound = $true
                    }
                }
            } catch {}
        }
        if (-not $injFound) {
            Write-Pass "No injection patterns found in scanned scripts"
            $score += 5; $null = $ok.Add("Scripts clean (no injection patterns)")
        }
    }
} catch {
    Write-Warn "Shell injection scan skipped: $($_.Exception.Message)"
}

# ============================
# CHECK 6: License
# ============================
Write-Host ""
Write-Host "--- [6] License Check ---" -ForegroundColor White

try {
    $lic = Invoke-RestMethod -Uri "$apiBase/license" -Headers $h -TimeoutSec 10
    $spdx = $lic.license.spdx_id
    $permissive = @("MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "CC0-1.0", "Unlicense")

    if ($permissive -contains $spdx) {
        Write-Pass "License: $spdx (permissive)"
        $score += 10; $null = $ok.Add("Permissive license: $spdx")
    } elseif ($spdx -match "GPL") {
        Write-Warn "License: $spdx (copyleft -- check AI OS usage policy)"
        $null = $warns.Add("Copyleft license: $spdx")
    } else {
        Write-Warn "License: $spdx -- verify compatibility"
        $null = $warns.Add("Non-standard license: $spdx")
    }
} catch {
    Write-Warn "No license file found (All Rights Reserved by default)"
    $null = $warns.Add("No license")
}

# ============================
# FINAL VERDICT
# ============================
$score = [math]::Max(0, [math]::Min(100, $score))

Write-Host ""
Write-Host "=================================================" -ForegroundColor Magenta
Write-Host "  SECURITY REPORT: $owner/$repo"                   -ForegroundColor Magenta
Write-Host "  Score: $score / 100"                             -ForegroundColor Magenta
Write-Host "================================================="
Write-Host ""

if ($ok.Count -gt 0) {
    Write-Host "  PASSED ($($ok.Count)):" -ForegroundColor Green
    $ok | ForEach-Object { Write-Host "    + $_" -ForegroundColor Green }
}
if ($warns.Count -gt 0) {
    Write-Host "  WARNINGS ($($warns.Count)):" -ForegroundColor Yellow
    $warns | ForEach-Object { Write-Host "    ! $_" -ForegroundColor Yellow }
}
if ($issues.Count -gt 0) {
    Write-Host "  ISSUES ($($issues.Count)):" -ForegroundColor Red
    $issues | ForEach-Object { Write-Host "    X $_" -ForegroundColor Red }
}

Write-Host ""

if ($issues.Count -gt 0) {
    Write-Host "  VERDICT: BLOCKED -- Do NOT ingest. Fix issues first." -ForegroundColor Red
    $verdict = "BLOCKED"
} elseif ($score -ge 70) {
    Write-Host "  VERDICT: APPROVED -- Safe to ingest into plugins/" -ForegroundColor Green
    $verdict = "APPROVED"
} elseif ($score -ge 40) {
    Write-Host "  VERDICT: REVIEW -- Ingest to plugins/experimental/ first" -ForegroundColor Yellow
    $verdict = "REVIEW"
} else {
    Write-Host "  VERDICT: REJECT -- Too many unknowns. Manual inspection required." -ForegroundColor Red
    $verdict = "REJECT"
}

Write-Host "=================================================" -ForegroundColor Magenta
Write-Host ""

if ($verdict -eq "APPROVED" -and $AutoApprove) {
    Write-Host "  [AUTO-APPROVE] Score $score >= 70. Proceeding." -ForegroundColor Green
    exit 0
} elseif ($verdict -eq "APPROVED") {
    $c = Read-Host "  Proceed with ingest? [Y/N]"
    if ($c -match "^[Yy]$") { exit 0 } else { exit 1 }
} elseif ($verdict -eq "REVIEW") {
    Write-Host "  Tip: Use plugins/experimental/ sandbox first" -ForegroundColor Yellow
    $c = Read-Host "  Proceed to experimental sandbox? [Y/N]"
    if ($c -match "^[Yy]$") { exit 2 } else { exit 1 }
} else {
    exit 1
}
