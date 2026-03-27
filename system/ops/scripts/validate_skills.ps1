<#
.SYNOPSIS
    AI OS Local Skill Validator
    Equivalent of GitHub Actions CI - run offline before pushing
.USAGE
    .\scripts\validate_skills.ps1 [-Verbose]
#>
param([switch]$Verbose)

$AOS_ROOT = Split-Path -Parent $PSScriptRoot
$REGISTRY_PATH = Join-Path $AOS_ROOT "shared-context\SKILL_REGISTRY.json"
$REQUIRED_FIELDS = @("name", "description", "version", "tier", "category")

$errorCount = 0
$ok = 0

Write-Host ""
Write-Host "=== AI OS Skill Validator ===" -ForegroundColor Cyan
Write-Host "--------------------------------------" -ForegroundColor DarkGray

# === 1. Plugin SKILL.md check ===
Write-Host ""
Write-Host "[1/4] Plugin SKILL.md presence" -ForegroundColor Yellow
$pluginsDir = Join-Path $AOS_ROOT "plugins"
$missing = @()
if (Test-Path $pluginsDir) {
    $pluginDirs = Get-ChildItem $pluginsDir -Directory
    foreach ($d in $pluginDirs) {
        $skillPath = Join-Path $d.FullName "SKILL.md"
        if (Test-Path $skillPath) {
            $ok++
        } else {
            $missing += $d.Name
            $errorCount++
            if ($Verbose) { Write-Host "  MISS $($d.Name)" -ForegroundColor Red }
        }
    }
    Write-Host "  Total: $($pluginDirs.Count) | OK: $ok | Missing: $($missing.Count)" -ForegroundColor White
} else {
    Write-Host "  plugins/ directory not found" -ForegroundColor DarkGray
}

# === 2. Required frontmatter fields ===
Write-Host ""
Write-Host "[2/4] SKILL.md required fields" -ForegroundColor Yellow
$allSkillMds = @()
$skillsPath = Join-Path $AOS_ROOT "skills"
$pluginsPath = Join-Path $AOS_ROOT "plugins"
if (Test-Path $skillsPath) {
    $allSkillMds += Get-ChildItem $skillsPath -Recurse -Filter "SKILL.md" -ErrorAction SilentlyContinue
}
if (Test-Path $pluginsPath) {
    $allSkillMds += Get-ChildItem $pluginsPath -Recurse -Filter "SKILL.md" -ErrorAction SilentlyContinue
}
$fieldErrors = 0
foreach ($f in $allSkillMds) {
    $content = Get-Content $f.FullName -Raw
    foreach ($field in $REQUIRED_FIELDS) {
        $pattern = "^" + $field + ":"
        if ($content -notmatch $pattern) {
            if ($Verbose) { Write-Host "  MISS field '$field': $($f.FullName)" -ForegroundColor Red }
            $fieldErrors++
            $errorCount++
        }
    }
}
Write-Host "  Checked: $($allSkillMds.Count) files | Field errors: $fieldErrors" -ForegroundColor White

# === 3. SKILL_REGISTRY.json ===
Write-Host ""
Write-Host "[3/4] SKILL_REGISTRY.json validation" -ForegroundColor Yellow
if (Test-Path $REGISTRY_PATH) {
    try {
        $reg = Get-Content $REGISTRY_PATH -Raw | ConvertFrom-Json
        $entries = if ($reg.skills) { $reg.skills } elseif ($reg.entries) { $reg.entries } else { @() }
        $ids = $entries | ForEach-Object { if ($_.id) { $_.id } else { $_.name } }
        $dupes = $ids | Group-Object | Where-Object { $_.Count -gt 1 }
        if ($dupes) {
            Write-Host "  FAIL Duplicate IDs: $($dupes.Name -join ', ')" -ForegroundColor Red
            $errorCount += $dupes.Count
        } else {
            Write-Host "  OK Valid JSON - $($entries.Count) entries, no duplicates" -ForegroundColor Green
        }
    } catch {
        Write-Host "  FAIL JSON parse error: $_" -ForegroundColor Red
        $errorCount++
    }
} else {
    Write-Host "  WARN SKILL_REGISTRY.json not found" -ForegroundColor Yellow
}

# === 4. Corp + LLM YAML ===
Write-Host ""
Write-Host "[4/4] Corp + LLM YAML files" -ForegroundColor Yellow
$yamlFiles = @()
$corpPath = Join-Path $AOS_ROOT "corp"
$llmPath = Join-Path $AOS_ROOT "llm"
if (Test-Path $corpPath) {
    $yamlFiles += Get-ChildItem $corpPath -Recurse -Filter "*.yaml" -ErrorAction SilentlyContinue
}
if (Test-Path $llmPath) {
    $yamlFiles += Get-ChildItem $llmPath -Recurse -Filter "*.yaml" -ErrorAction SilentlyContinue
}
Write-Host "  YAML files found: $($yamlFiles.Count)" -ForegroundColor White
foreach ($y in $yamlFiles) {
    if ($Verbose) { Write-Host "  OK $($y.Name)" -ForegroundColor DarkGray }
}

# === SUMMARY ===
Write-Host ""
Write-Host "--------------------------------------" -ForegroundColor DarkGray
if ($errorCount -eq 0) {
    Write-Host "PASS All checks passed!" -ForegroundColor Green
} else {
    Write-Host "FAIL Found $errorCount error(s)" -ForegroundColor Red
    if ($missing.Count -gt 0) {
        Write-Host ""
        Write-Host "Plugins missing SKILL.md:" -ForegroundColor Yellow
        $missing | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
    }
    exit 1
}
