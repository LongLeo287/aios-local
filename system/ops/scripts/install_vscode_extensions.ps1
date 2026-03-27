# ops/scripts/install_vscode_extensions.ps1
# AI OS Corp — VS Code Extension Auto-Installer
# Version: 1.0 | 2026-03-25
# Trigger: pre-session.md boot check OR manual run
# Doc: ops/tools/vscode-extensions.md

param(
    [switch]$Quiet,     # Suppress verbose output
    [switch]$Force      # Re-install even if already installed
)

$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$receiptDir = "$root\telemetry\receipts"
$date = Get-Date -Format "yyyy-MM-dd"
$logFile = "$receiptDir\vscode_extensions_$date.log"
$bbPath = "$root\brain\shared-context\blackboard.json"

# Required extensions (ID → friendly name)
$extensions = @(
    [PSCustomObject]@{ Id = "zixfel.ag-auto-click-scroll"; Name = "AG Auto Click Scroll (AI OS core)" },
    [PSCustomObject]@{ Id = "ms-python.python"; Name = "Python" },
    [PSCustomObject]@{ Id = "ms-vscode.powershell"; Name = "PowerShell" },
    [PSCustomObject]@{ Id = "yzhang.markdown-all-in-one"; Name = "Markdown All in One" },
    [PSCustomObject]@{ Id = "redhat.vscode-yaml"; Name = "YAML" }
)

function Write-Log {
    param($msg)
    $ts = Get-Date -Format "HH:mm:ss"
    $line = "[$ts] $msg"
    Add-Content -Path $logFile -Value $line -Encoding UTF8
    if (-not $Quiet) { Write-Host $line }
}

# Check VS Code
$codePath = Get-Command "code" -ErrorAction SilentlyContinue
if (-not $codePath) {
    Write-Log "[SKIP] VS Code 'code' CLI not found. Install VS Code and add to PATH."
    exit 0
}

# Check already installed (if not Force)
$bb = @{}
if (Test-Path $bbPath) {
    try { $bb = Get-Content $bbPath -Raw -ErrorAction SilentlyContinue | ConvertFrom-Json }
    catch { $bb = @{} }
}

if ($bb.vscode_extensions_installed -eq $true -and -not $Force) {
    if (-not $Quiet) { Write-Host "[SKIP] VS Code extensions already installed. Use -Force to reinstall." }
    exit 0
}

# Create receipt dir
New-Item -ItemType Directory -Path $receiptDir -Force | Out-Null
Write-Log "=== AI OS VS Code Extension Installer ==="
Write-Log "Extensions to install: $($extensions.Count)"

$installed = 0
$failed = 0

foreach ($ext in $extensions) {
    $extId = $ext.Id; $name = $ext.Name
    try {
        Write-Log "Installing: $extId ($name)..."
        $result = code --install-extension $extId --force 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Log "  [OK] $extId"
            $installed++
        } else {
            Write-Log "  [WARN] $extId — exit $LASTEXITCODE"
            $failed++
        }
    } catch {
        Write-Log "  [ERR] $extId — $_"
        $failed++
    }
}

Write-Log "=== Done: $installed installed, $failed failed ==="

# Update blackboard
if (Test-Path $bbPath) {
    try {
        $bbRaw = Get-Content $bbPath -Raw -Encoding UTF8 | ConvertFrom-Json
        $bbRaw | Add-Member -NotePropertyName "vscode_extensions_installed" -NotePropertyValue $true -Force
        $bbRaw | Add-Member -NotePropertyName "vscode_extensions_date" -NotePropertyValue $date -Force
        $bbRaw | ConvertTo-Json -Depth 10 | Set-Content $bbPath -Encoding UTF8
        if (-not $Quiet) { Write-Host "[OK] blackboard.json updated" }
    } catch {
        Write-Log "[WARN] Could not update blackboard.json: $_"
    }
}

if (-not $Quiet) {
    Write-Host ""
    Write-Host "Log: $logFile"
    Write-Host "Reload VS Code to activate extensions."
}

