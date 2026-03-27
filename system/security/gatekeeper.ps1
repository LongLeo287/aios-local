<#
.SYNOPSIS
    AI OS Gatekeeper — validates workspace identity before agent execution.
.DESCRIPTION
    Reads registry.json and validates the --CheckID parameter.
    Rejects commands if the ID is invalid or the workspace path does not exist.
.PARAMETER CheckID
    The project identifier (e.g., PRJ-001).
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$CheckID
)

$ErrorActionPreference = "Stop"

# Resolve paths
$ScriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
# ScriptDir is security/. Root is one level up.
$RootDir = Split-Path -Parent $ScriptDir
$RegistryPath = Join-Path $RootDir "core\registry.json"

# Load registry
if (-not (Test-Path $RegistryPath)) {
    Write-Error "[GATEKEEPER] FATAL: registry.json not found at $RegistryPath"
    exit 1
}

$Registry = Get-Content $RegistryPath -Raw | ConvertFrom-Json

# Validate project ID
if (-not ($Registry.PSObject.Properties.Name -contains $CheckID)) {
    Write-Error "[GATEKEEPER] DENY: Unknown project ID '$CheckID'. Valid IDs: $($Registry.PSObject.Properties.Name -join ', ')"
    exit 2
}

$Workspace = $Registry.$CheckID
$WorkspacePath = $Workspace.path

# Validate workspace path exists
if (-not (Test-Path $WorkspacePath)) {
    Write-Error "[GATEKEEPER] DENY: Workspace path does not exist: $WorkspacePath"
    exit 3
}

# Success - output validated project info
Write-Host '============================================'
Write-Host ' AI OS GATEKEEPER - GRANT'
Write-Host '============================================'
Write-Host " Workspace ID   : $CheckID"
Write-Host " Workspace Name : $($Workspace.name)"
Write-Host " Workspace Path : $WorkspacePath"
Write-Host '============================================'

# Return workspace path for downstream use
return $WorkspacePath
