<#
.SYNOPSIS
    Register a new project into the AI OS ecosystem.

.DESCRIPTION
    Creates registry.json entry, scaffolds projects/PRJ-XXX/ directory,
    and guides user through workspace setup.

.PARAMETER Id
    Project ID, e.g., PRJ-005

.PARAMETER Name
    Display name of the project

.PARAMETER Path
    Absolute path to the project directory

.PARAMETER Description
    Short one-line description

.PARAMETER Skills
    Array of skill names this project uses (optional)

.PARAMETER ChannelsEnabled
    Whether the project uses remote channel bridges (default: $false)

.PARAMETER DataSources
    Array of data source identifiers (optional)

.EXAMPLE
    .\register_project.ps1 -Id PRJ-005 -Name "My App" -Path "D:\MyApp" -Description "My new project"

.EXAMPLE
    .\register_project.ps1 -Id PRJ-005 -Name "My App" -Path "D:\MyApp" -Description "desc" -Skills @("ui-ux-pro-max","gas-sheets-optimizer") -ChannelsEnabled $true
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Id,

    [Parameter(Mandatory=$true)]
    [string]$Name,

    [Parameter(Mandatory=$true)]
    [string]$Path,

    [Parameter(Mandatory=$true)]
    [string]$Description,

    [string[]]$Skills = @(),

    [bool]$ChannelsEnabled = $false,

    [string[]]$DataSources = @()
)

$ErrorActionPreference = "Stop"
$AiOsRoot = $env:AOS_ROOT
$RegistryPath = "$AiOsRoot\registry.json"
$ProjectsDir = "$AiOsRoot\projects"
$TemplateDir = "$ProjectsDir\TEMPLATE"

# ─── Validate ───────────────────────────────────────────────────────────────
if ($Id -notmatch '^PRJ-\d{3,}$') {
    Write-Error "❌ Id must match pattern PRJ-NNN (e.g., PRJ-005)"
    exit 1
}

if (-not (Test-Path $Path)) {
    Write-Warning "⚠️  Project path does not exist yet: $Path"
    $create = Read-Host "Create directory? (y/n)"
    if ($create -eq 'y') { New-Item -ItemType Directory -Path $Path -Force | Out-Null }
}

# ─── Load & Check registry ───────────────────────────────────────────────────
$registry = Get-Content $RegistryPath -Raw | ConvertFrom-Json
$existing = $registry.PSObject.Properties | Where-Object { $_.Name -eq $Id }

if ($existing) {
    Write-Warning "⚠️  $Id already exists in registry.json. Overwrite? (y/n)"
    $overwrite = Read-Host
    if ($overwrite -ne 'y') { Write-Host "Aborted."; exit 0 }
}

# ─── Prepare registry entry ──────────────────────────────────────────────────
$configPath = "$ProjectsDir\$Id\CLAUDE.md"
$workflowsPath = "$ProjectsDir\$Id\workflows\"

$newEntry = [ordered]@{
    name              = $Name
    path              = $Path
    description       = $Description
    status            = "active"
    skills_used       = $Skills
    channels_enabled  = $ChannelsEnabled
    data_sources      = $DataSources
    contact_agent     = "claude_code"
    config_path       = $configPath
    workflows_path    = $workflowsPath
    registered_at     = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss+07:00")
}

# Add to registry
$registry | Add-Member -MemberType NoteProperty -Name $Id -Value $newEntry -Force

# Save registry.json
$registry | ConvertTo-Json -Depth 5 | Set-Content $RegistryPath -Encoding UTF8
Write-Host "✅ Added $Id to registry.json"

# ─── Scaffold projects/PRJ-XXX/ ──────────────────────────────────────────────
$projectConfigDir = "$ProjectsDir\$Id"
New-Item -ItemType Directory -Path $projectConfigDir -Force | Out-Null
New-Item -ItemType Directory -Path "$projectConfigDir\workflows" -Force | Out-Null

# Copy & customize CLAUDE.md template
$claudeTemplate = Get-Content "$TemplateDir\CLAUDE.md" -Raw
$claudeContent = $claudeTemplate `
    -replace "\[PROJECT_NAME\]", $Name `
    -replace "\[PROJECT_PATH\]", $Path `
    -replace "\[DATE\]", (Get-Date -Format "yyyy-MM-dd") `
    -replace "PRJ-XXX", $Id

Set-Content "$projectConfigDir\CLAUDE.md" -Value $claudeContent -Encoding UTF8
Write-Host "✅ Created $projectConfigDir\CLAUDE.md"

# Copy .clauderules template to project directory if it exists
$destinationClauderules = "$Path\.clauderules"
if (-not (Test-Path $destinationClauderules)) {
    $clauderulesTemplate = Get-Content "$TemplateDir\.clauderules" -Raw
    $clauderulesContent = $clauderulesTemplate `
        -replace "\[PROJECT_NAME\]", $Name `
        -replace "PRJ-XXX", $Id
    Set-Content $destinationClauderules -Value $clauderulesContent -Encoding UTF8
    Write-Host "✅ Created $destinationClauderules"
} else {
    Write-Warning "⚠️  .clauderules already exists in $Path - skipped"
}

# ─── Update blackboard.json ──────────────────────────────────────────────────
$blackboardPath = "$AiOsRoot\shared-context\blackboard.json"
$blackboard = Get-Content $blackboardPath -Raw | ConvertFrom-Json

$blackboard._active_workspace = [ordered]@{
    project_id   = $Id
    name         = $Name
    path         = $Path
    connected_at = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss+07:00")
    gatekeeper   = "GRANT"
}

$blackboard | ConvertTo-Json -Depth 5 | Set-Content $blackboardPath -Encoding UTF8
Write-Host "✅ Updated blackboard.json → active workspace: $Id"

# ─── Summary ─────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " ✅  $Id - $Name - REGISTERED" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Registry:    $RegistryPath"
Write-Host "  Config:      $configPath"
Write-Host "  Workflows:   $workflowsPath"
Write-Host "  Project .clauderules: $destinationClauderules"
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Edit $configPath - add project-specific skills & rules"
Write-Host "  2. Add workflows to $workflowsPath"
Write-Host "  3. Run: .\gatekeeper.ps1 -ProjectId $Id"
Write-Host ""

