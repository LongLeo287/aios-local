<#
.SYNOPSIS
    AI OS - Skill and Plugin Auto-Loader (Layer 4)
    Scans skills/ and plugins/ directories, parses SKILL.md / manifest.json,
    and rebuilds shared-context/SKILL_REGISTRY.json automatically.
.DESCRIPTION
    This is the discovery engine of AI OS Layer 4.
    Run it any time a new skill or plugin is added to auto-register it.
    PORTABLE: Auto-detects AI OS root from script location - works anywhere.
.USAGE
    .\scripts\skill_loader.ps1           # Full rebuild
    .\scripts\skill_loader.ps1 -DryRun  # Preview only
    .\scripts\skill_loader.ps1 -Verbose # Show all details
.NOTES
    Updated: 2026-03-14 | Version: 1.2 | Part of AI OS Layer 4
#>

param(
    [switch]$DryRun,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

# ---- PATHS (portable - auto-detect from script location) ----
# scripts/ is always one level below AI OS root
$AiOsRoot      = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$SkillsDir     = Join-Path $AiOsRoot "skills"
$DomainsDir    = Join-Path $AiOsRoot "skills\domains"
$ExperimentalDir = Join-Path $AiOsRoot "skills\experimental"
$PluginsDir    = Join-Path $AiOsRoot "plugins"
$AgentsDir     = Join-Path $AiOsRoot "agents"
$RegistryOut   = Join-Path $AiOsRoot "shared-context\SKILL_REGISTRY.json"
$Timestamp     = Get-Date -Format "yyyy-MM-dd"
$RunTime       = Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"

Write-Host "  [ROOT] $AiOsRoot" -ForegroundColor DarkGray

Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "  AI OS SKILL LOADER -- Layer 4 Cross-Read      " -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# ---- HELPER: Parse single-value YAML key ----
function Get-YamlValue {
    param([string[]]$Lines, [string]$Key)
    $line = $Lines | Where-Object { $_ -match "^$Key\s*:" } | Select-Object -First 1
    if ($line) {
        return ($line -replace "^$Key\s*:\s*", "").Trim().Trim('"')
    }
    return $null
}

# ---- HELPER: Parse list YAML key ----
function Get-YamlList {
    param([string[]]$Lines, [string]$Key)
    $result = @()
    $inBlock = $false
    foreach ($line in $Lines) {
        if ($line -match "^$Key\s*:") { $inBlock = $true; continue }
        if ($inBlock) {
            if ($line -match "^\s+-\s+(.+)") { $result += $Matches[1].Trim() }
            elseif ($line -match "^\S" -and $line -notmatch "^\s+-") { break }
        }
    }
    return $result
}

# ---- PARSER: SKILL.md with YAML frontmatter ----
function ConvertFrom-SkillMd {
    param([string]$FilePath, [string]$SourceDir)

    $content = Get-Content $FilePath -Raw -ErrorAction SilentlyContinue
    if (-not $content) { return $null }

    # Extract YAML block between first two ---
    $yamlBlock = ""
    if ($content -match "(?s)^---\s*\n(.*?)\n---") {
        $yamlBlock = $Matches[1]
    } else {
        return $null
    }

    $lines = $yamlBlock -split "`n"

    $id          = Get-YamlValue $lines "id"
    $name        = Get-YamlValue $lines "name"
    $version     = Get-YamlValue $lines "version"
    $tierRaw     = Get-YamlValue $lines "tier"
    $tier        = if ($tierRaw) { [int]$tierRaw } else { 2 }
    $status      = Get-YamlValue $lines "status"
    $description = Get-YamlValue $lines "description"
    $domain      = Get-YamlValue $lines "domain"
    $costTier    = Get-YamlValue $lines "cost_tier"
    $category    = Get-YamlValue $lines "category"

    $accessibleBy = Get-YamlList $lines "accessible_by"
    $dependencies = Get-YamlList $lines "dependencies"
    $tags         = Get-YamlList $lines "tags"
    $consumedBy   = Get-YamlList $lines "consumed_by"
    $emitsEvents  = Get-YamlList $lines "emits_events"
    $listensTo    = Get-YamlList $lines "listens_to"

    # Parse exposed_functions
    $exposedFunctions = @()
    $inFuncs = $false
    foreach ($line in $lines) {
        if ($line -match "^exposed_functions\s*:") { $inFuncs = $true; continue }
        if ($inFuncs) {
            if ($line -match "^\s+-\s+name:\s+(.+)") {
                $exposedFunctions += $Matches[1].Trim()
            } elseif ($line -match "^\s+-\s+(.+)" -and $line -notmatch "description|input|output") {
                $exposedFunctions += $Matches[1].Trim()
            } elseif ($line -match "^\S" -and $line -notmatch "^\s") { break }
        }
    }

    # Fallback: use `name` as id if `id` field is missing (domain skills use `name`)
    if (-not $id) {
        if ($name) { $id = $name -replace '\s+', '_' -replace '[^a-zA-Z0-9_-]', '' }
        else { return $null }
    }

    return [PSCustomObject]@{
        id                = $id
        name              = if ($name) { $name } else { $id }
        version           = if ($version) { $version } else { "1.0.0" }
        tier              = $tier
        status            = if ($status) { $status } else { "active" }
        source            = "skill"
        path              = $FilePath
        description       = if ($description) { $description } else { "" }
        domain            = if ($domain) { $domain } else { "core" }
        cost_tier         = if ($costTier) { $costTier } else { "standard" }
        category          = if ($category) { $category } else { "" }
        accessible_by     = $accessibleBy
        dependencies      = $dependencies
        exposed_functions = $exposedFunctions
        consumed_by       = $consumedBy
        emits_events      = $emitsEvents
        listens_to        = $listensTo
        tags              = $tags
        _loaded_at        = $RunTime
    }
}

# ---- PARSER: plugin manifest.json ----
function ConvertFrom-PluginManifest {
    param([string]$FilePath)

    $content = Get-Content $FilePath -Raw -ErrorAction SilentlyContinue
    if (-not $content) { return $null }

    try {
        $manifest = $content | ConvertFrom-Json
    } catch {
        return $null
    }

    return [PSCustomObject]@{
        id                = $manifest.id
        name              = $manifest.name
        version           = $manifest.version
        tier              = 3
        status            = $manifest.status
        source            = "plugin"
        path              = $FilePath
        description       = $manifest.description
        accessible_by     = @("Orchestrator")
        dependencies      = if ($manifest.skill_dependencies) { $manifest.skill_dependencies } else { @() }
        exposed_functions = if ($manifest.exposed_api) { $manifest.exposed_api | ForEach-Object { $_.name } } else { @() }
        consumed_by       = @()
        emits_events      = @()
        listens_to        = @()
        tags              = @("plugin", $manifest.type)
        _loaded_at        = $RunTime
    }
}

# ---- SCAN: Skills (skills/, skills/domains/*, skills/experimental/, agents/) ----
$allEntries = @()
$failedDirs = @()

# Core skill dirs (only top-level - domains is handled separately)
[string[]]$coreScanDirs = @()
if (Test-Path $SkillsDir) { $coreScanDirs += $SkillsDir }

# Domain packs: scan each domain subfolder  
[string[]]$domainScanDirs = @()
if (Test-Path $DomainsDir) {
    $domainScanDirs = @(Get-ChildItem -Path $DomainsDir -Directory -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty FullName)
}

# Experimental: flat dir
[string[]]$experimentalScanDirs = @()
if (Test-Path $ExperimentalDir) { $experimentalScanDirs = @($ExperimentalDir) }

# Agents: each agent subfolder
[string[]]$agentScanDirs = @()
if (Test-Path $AgentsDir) {
    $agentScanDirs = @(Get-ChildItem -Path $AgentsDir -Directory -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty FullName)
}

[string[]]$allScanDirs = @($coreScanDirs) + @($domainScanDirs) + @($experimentalScanDirs) + @($agentScanDirs)

Write-Host "Scanning skill directories..." -ForegroundColor Yellow

foreach ($scanDir in $allScanDirs) {
    $isDomainDir = $scanDir -like "*\skills\domains\*"

    if ($isDomainDir) {
        # Domain dirs: scan ALL .md files (named gas-skill.md, sheets-skill.md etc.)
        $mdFiles = Get-ChildItem -Path $scanDir -Filter "*.md" -File -ErrorAction SilentlyContinue
        foreach ($mdFile in $mdFiles) {
            $parsed = ConvertFrom-SkillMd -FilePath $mdFile.FullName -SourceDir $scanDir
            if ($parsed) {
                $allEntries += $parsed
                if ($Verbose) { Write-Host "  [OK] $($parsed.id) [Tier$($parsed.tier)] domain:$($parsed.domain)" -ForegroundColor Green }
            } else {
                if ($Verbose) { Write-Host "  [SKIP] $($mdFile.Name) -- no valid frontmatter" -ForegroundColor DarkGray }
            }
        }
        continue
    }

    # Core / experimental / agents dirs: look for SKILL.md in subdirs
    $directSkill = Join-Path $scanDir "SKILL.md"
    if (Test-Path $directSkill) {
        $parsed = ConvertFrom-SkillMd -FilePath $directSkill -SourceDir (Split-Path $scanDir -Parent)
        if ($parsed) {
            $allEntries += $parsed
            if ($Verbose) { Write-Host "  [OK] $($parsed.id) [Tier$($parsed.tier)] $($parsed.status)" -ForegroundColor Green }
        } else {
            $failedDirs += $scanDir
            Write-Host "  [FAIL] $(Split-Path $scanDir -Leaf) -- no valid YAML frontmatter in SKILL.md" -ForegroundColor Red
        }
        continue
    }

    $subdirs = Get-ChildItem -Path $scanDir -Directory -ErrorAction SilentlyContinue
    foreach ($dir in $subdirs) {
        $skillFile = Join-Path $dir.FullName "SKILL.md"
        if (-not (Test-Path $skillFile)) {
            if ($Verbose) { Write-Host "  [SKIP] No SKILL.md: $($dir.Name)" -ForegroundColor DarkGray }
            continue
        }

        $parsed = ConvertFrom-SkillMd -FilePath $skillFile -SourceDir $scanDir
        if ($parsed) {
            $allEntries += $parsed
            if ($Verbose) { Write-Host "  [OK] $($parsed.id) [Tier$($parsed.tier)] $($parsed.status)" -ForegroundColor Green }
        } else {
            $failedDirs += $dir.FullName
            Write-Host "  [FAIL] $($dir.Name) -- no valid YAML frontmatter in SKILL.md" -ForegroundColor Red
        }
    }
}

# ---- SCAN: Plugins ----
Write-Host "Scanning plugin directories..." -ForegroundColor Yellow

if (Test-Path $PluginsDir) {
    $pluginDirs = Get-ChildItem -Path $PluginsDir -Directory -ErrorAction SilentlyContinue
    foreach ($dir in $pluginDirs) {
        $manifestFile = Join-Path $dir.FullName "manifest.json"
        if (-not (Test-Path $manifestFile)) {
            if ($Verbose) { Write-Host "  [SKIP] No manifest.json: $($dir.Name)" -ForegroundColor DarkGray }
            continue
        }

        $parsed = ConvertFrom-PluginManifest -FilePath $manifestFile
        if ($parsed) {
            $allEntries += $parsed
            if ($Verbose) { Write-Host "  [OK] plugin:$($parsed.id) [Tier3] $($parsed.status)" -ForegroundColor Blue }
        } else {
            $failedDirs += $dir.FullName
            Write-Host "  [FAIL] $($dir.Name) -- invalid manifest.json" -ForegroundColor Red
        }
    }
}

# ---- VALIDATE: Dependency references ----
Write-Host "Validating dependencies..." -ForegroundColor Yellow

$allIds    = $allEntries | ForEach-Object { $_.id }
$depErrors = @()

foreach ($entry in $allEntries) {
    foreach ($dep in $entry.dependencies) {
        if ($dep -notin $allIds) {
            $depErrors += "  [DEP ERROR] '$($entry.id)' depends on '$dep' -- NOT FOUND"
        }
    }
}

if ($depErrors.Count -gt 0) {
    Write-Host "Dependency errors:" -ForegroundColor Red
    $depErrors | ForEach-Object { Write-Host $_ -ForegroundColor Yellow }
} else {
    Write-Host "  [OK] All dependencies resolved" -ForegroundColor Green
}

# ---- BUILD: Load order tiers ----
$tier1 = $allEntries | Where-Object { $_.tier -eq 1 -and $_.status -eq "active" } | ForEach-Object { $_.id }
$tier2 = $allEntries | Where-Object { $_.tier -eq 2 -and $_.status -eq "active" } | ForEach-Object { $_.id }
$tier3 = $allEntries | Where-Object { ($_.tier -eq 3 -or $_.source -eq "plugin") -and $_.status -eq "active" } | ForEach-Object { $_.id }

# ---- BUILD: Registry object ----
$registry = [ordered]@{
    meta = [ordered]@{
        title         = "AI OS -- Master Skill and Plugin Registry"
        version       = "2.1"
        updated       = $Timestamp
        generated_by  = "scripts/skill_loader.ps1"
        spec          = "$AiOsRoot\skills\SKILL_SPEC.md"
        loader        = "$AiOsRoot\scripts\skill_loader.ps1"
        total_entries = $allEntries.Count
        total_skills  = ($allEntries | Where-Object { $_.source -eq "skill" }).Count
        total_plugins = ($allEntries | Where-Object { $_.source -eq "plugin" }).Count
        failed_dirs   = $failedDirs.Count
        dep_errors    = $depErrors.Count
    }
    load_order = [ordered]@{
        tier1_eager  = @($tier1)
        tier2_lazy   = @($tier2)
        tier3_manual = @($tier3)
    }
    entries = @($allEntries)
}

# ---- WRITE or DRY-RUN ----
$json = $registry | ConvertTo-Json -Depth 10

if ($DryRun) {
    Write-Host ""
    Write-Host "=== DRY-RUN (nothing written to disk) ===" -ForegroundColor Magenta
    Write-Host "Would write $($json.Length) bytes to: $RegistryOut" -ForegroundColor Gray
} else {
    $json | Set-Content -Path $RegistryOut -Encoding UTF8
    Write-Host "  [OK] Registry written to: $RegistryOut" -ForegroundColor Green
}

# ---- SUMMARY REPORT ----
Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "  SKILL LOADER REPORT                          " -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "  Total entries  : $($allEntries.Count)" -ForegroundColor White
Write-Host "  Skills loaded  : $(($allEntries | Where-Object { $_.source -eq 'skill' }).Count)" -ForegroundColor Green
Write-Host "  Plugins loaded : $(($allEntries | Where-Object { $_.source -eq 'plugin' }).Count)" -ForegroundColor Blue
Write-Host "  Failed         : $($failedDirs.Count)" -ForegroundColor $(if ($failedDirs.Count -gt 0) { "Red" } else { "Green" })
Write-Host "  Dep errors     : $($depErrors.Count)" -ForegroundColor $(if ($depErrors.Count -gt 0) { "Yellow" } else { "Green" })
Write-Host "  Tier 1 (eager) : $($tier1 -join ', ')" -ForegroundColor Gray
Write-Host "  Tier 2 (lazy)  : $($tier2.Count) skills" -ForegroundColor Gray
Write-Host "  Tier 3 (manual): $($tier3.Count) entries" -ForegroundColor Gray
Write-Host ""
if ($DryRun) {
    Write-Host "  [DRY-RUN] No changes written." -ForegroundColor Magenta
} else {
    Write-Host "  Registry rebuilt successfully." -ForegroundColor Green
}
Write-Host ""
