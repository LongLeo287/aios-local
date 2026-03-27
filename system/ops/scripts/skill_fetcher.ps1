<#
.SYNOPSIS
    AI OS - External Skill Fetcher
    Fetches skill files from external sources (GitHub, web) defined in EXTERNAL_SKILL_SOURCES.yaml.
    All fetched skills land in skills/experimental/ for review before promotion.
.DESCRIPTION
    Safe, manual-only fetch. Never auto-fetches. Always requires user confirmation trigger.
    Source catalog: shared-context/EXTERNAL_SKILL_SOURCES.yaml
.USAGE
    .\scripts\skill_fetcher.ps1 -SourceId "gh:bmad-code-org/BMAD-METHOD"
    .\scripts\skill_fetcher.ps1 -ListSources
    .\scripts\skill_fetcher.ps1 -SourceId "..." -DryRun
.NOTES
    Version: 1.0 | Updated: 2026-03-14
    Safety: GATE-4 applies. Only fetches from EXTERNAL_SKILL_SOURCES.yaml trusted/manual sources.
#>

param(
    [string]$SourceId,
    [switch]$ListSources,
    [switch]$DryRun,
    [switch]$Verify
)

$ErrorActionPreference = "Stop"

# ---- PATHS (portable - auto-detect from script location) ----
$AiOsRoot        = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$SourceCatalog   = Join-Path $AiOsRoot "shared-context\EXTERNAL_SKILL_SOURCES.yaml"
$ExperimentalDir = Join-Path $AiOsRoot "skills\experimental"
$Timestamp       = Get-Date -Format "yyyyMMdd-HHmmss"

Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "  AI OS EXTERNAL SKILL FETCHER                   " -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# ---- HELPER: Parse YAML source catalog (simple line parser) ----
function Get-SourceList {
    param([string]$CatalogPath)
    if (-not (Test-Path $CatalogPath)) {
        Write-Host "[ERROR] EXTERNAL_SKILL_SOURCES.yaml not found at: $CatalogPath" -ForegroundColor Red
        exit 1
    }
    $content = Get-Content $CatalogPath -Raw
    $sources = @()
    $blocks = $content -split "  - source_id:"
    foreach ($block in $blocks | Select-Object -Skip 1) {
        $lines = $block -split "`n"
        $id     = ($lines[0] -replace '"', '').Trim()
        $name   = ($lines | Where-Object { $_ -match "^\s+name:" } | Select-Object -First 1) -replace '^\s+name:\s*"?', '' -replace '"', ''
        $url    = ($lines | Where-Object { $_ -match "^\s+canonical_url:" } | Select-Object -First 1) -replace '^\s+canonical_url:\s*"?', '' -replace '"', ''
        $status = ($lines | Where-Object { $_ -match "^\s+status:" } | Select-Object -First 1) -replace '^\s+status:\s*', ''
        $method = ($lines | Where-Object { $_ -match "^\s+fetch_method:" } | Select-Object -First 1) -replace '^\s+fetch_method:\s*', ''
        $sources += [PSCustomObject]@{
            id     = $id.Trim()
            name   = $name.Trim()
            url    = $url.Trim()
            status = $status.Trim()
            method = $method.Trim()
        }
    }
    return $sources
}

# ---- LIST SOURCES ----
if ($ListSources) {
    $sources = Get-SourceList $SourceCatalog
    Write-Host "Available sources in EXTERNAL_SKILL_SOURCES.yaml:`n" -ForegroundColor Yellow
    Write-Host ("{0,-45} {1,-10} {2}" -f "Source ID", "Status", "Name")
    Write-Host ("-" * 80)
    foreach ($s in $sources) {
        $color = switch ($s.status) {
            "trusted"     { "Green" }
            "manual"      { "Yellow" }
            "quarantined" { "Red" }
            default       { "Gray" }
        }
        Write-Host ("{0,-45} " -f $s.id) -NoNewline
        Write-Host ("{0,-10} " -f $s.status) -ForegroundColor $color -NoNewline
        Write-Host $s.name
    }
    Write-Host ""
    Write-Host "To fetch: skill_fetcher.ps1 -SourceId `"<source_id>`"" -ForegroundColor Cyan
    exit 0
}

# ---- REQUIRE SOURCE ID ----
if (-not $SourceId) {
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  skill_fetcher.ps1 -ListSources"
    Write-Host "  skill_fetcher.ps1 -SourceId `"gh:bmad-code-org/BMAD-METHOD`""
    Write-Host "  skill_fetcher.ps1 -SourceId `"...`" -DryRun"
    exit 0
}

# ---- VALIDATE SOURCE ----
$sources = Get-SourceList $SourceCatalog
$source = $sources | Where-Object { $_.id -eq $SourceId } | Select-Object -First 1

if (-not $source) {
    Write-Host "[ERROR] Source ID not found: $SourceId" -ForegroundColor Red
    Write-Host "Run -ListSources to see available sources." -ForegroundColor Yellow
    exit 1
}

if ($source.status -eq "quarantined") {
    Write-Host "[BLOCKED] Source '$SourceId' is quarantined. Security review required before fetching." -ForegroundColor Red
    exit 1
}

Write-Host "Source: $($source.name)" -ForegroundColor White
Write-Host "URL:    $($source.url)" -ForegroundColor DarkGray
Write-Host "Method: $($source.method)" -ForegroundColor DarkGray
Write-Host "Status: $($source.status)" -ForegroundColor $(if ($source.status -eq "trusted") { "Green" } else { "Yellow" })
Write-Host ""

# ---- GATE-4: Safety Check ----
Write-Host "[GATE-4] External fetch requires confirmation." -ForegroundColor Yellow
Write-Host "         Fetched content will land in: skills\experimental\" -ForegroundColor Yellow
Write-Host "         It will NOT be auto-registered until you review and promote it." -ForegroundColor Yellow
Write-Host ""

if (-not $DryRun) {
    $confirm = Read-Host "Proceed? (y/N)"
    if ($confirm -ne "y" -and $confirm -ne "Y") {
        Write-Host "[ABORTED] User cancelled fetch." -ForegroundColor Yellow
        exit 0
    }
}

# ---- DESTINATION ----
$destFolder = Join-Path $ExperimentalDir ("FETCHED_" + ($SourceId -replace "[^a-zA-Z0-9]", "_") + "_$Timestamp")

if ($DryRun) {
    Write-Host "[DRY-RUN] Would create: $destFolder" -ForegroundColor DarkCyan
    Write-Host "[DRY-RUN] Would fetch from: $($source.url)" -ForegroundColor DarkCyan
    Write-Host "[DRY-RUN] No files written." -ForegroundColor DarkCyan
    exit 0
}

New-Item -ItemType Directory -Path $destFolder -Force | Out-Null

# ---- FETCH (GitHub API method) ----
if ($source.method -like "github_api*") {
    $repoPath = $source.url -replace "https://github.com/", ""
    $apiUrl   = "https://api.github.com/repos/$repoPath/zipball/main"
    $zipPath  = Join-Path $env:TEMP "aios_fetch_$Timestamp.zip"

    Write-Host "Fetching from GitHub: $apiUrl" -ForegroundColor Yellow

    try {
        Invoke-WebRequest -Uri $apiUrl -OutFile $zipPath -UseBasicParsing `
            -Headers @{ "User-Agent" = "AI-OS-Skill-Fetcher/1.0"; "Accept" = "application/vnd.github+json" }

        Expand-Archive -Path $zipPath -DestinationPath $destFolder -Force
        Remove-Item $zipPath -Force

        Write-Host "[OK] Fetched and extracted to: $destFolder" -ForegroundColor Green

        # ---- SECURITY SCAN ----
        Write-Host "Running security scan..." -ForegroundColor Yellow
        $mdFiles = Get-ChildItem $destFolder -Recurse -Filter "*.md" | Measure-Object
        $jsFiles = Get-ChildItem $destFolder -Recurse -Include "*.js","*.ts","*.py","*.ps1" | Measure-Object
        Write-Host "  .md files: $($mdFiles.Count) | Script files: $($jsFiles.Count)"
        if ($jsFiles.Count -gt 0) {
            Write-Host "  [WARN] Script files detected. Review manually before using." -ForegroundColor Yellow
        }

    } catch {
        Write-Host "[ERROR] Fetch failed: $_" -ForegroundColor Red
        Remove-Item $destFolder -Recurse -Force -ErrorAction SilentlyContinue
        exit 1
    }
} elseif ($source.method -eq "html_crawl") {
    Write-Host "[INFO] html_crawl method: manual fetch recommended for: $($source.url)" -ForegroundColor Yellow
    Write-Host "       Open URL in browser, copy relevant SKILL.md content manually." -ForegroundColor DarkGray
    exit 0
} else {
    Write-Host "[WARN] Fetch method '$($source.method)' not yet automated. Manual fetch required." -ForegroundColor Yellow
    exit 0
}

# ---- REPORT ----
Write-Host ""
Write-Host "=================================================" -ForegroundColor Green
Write-Host "  FETCH COMPLETE" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Destination : $destFolder"
Write-Host "  Next steps  :"
Write-Host "    1. Review files in: $destFolder"
Write-Host "    2. Create a SKILL.md with proper frontmatter"
Write-Host "    3. Move to skills\core\ or skills\domains\<domain>\"
Write-Host "    4. Run: skill_loader.ps1  (rebuild registry)"
Write-Host ""
