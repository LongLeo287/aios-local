# AI OS Corp -- DPAPI Secrets Decryptor
# Decrypts MASTER.env.dpapi and loads secrets into $env:* variables.
# Must be dot-sourced to affect the calling session.
#
# Usage:
#   . .\ops\secrets\decrypt.ps1
#   . .\ops\secrets\decrypt.ps1 -ShowKeys

param(
    [switch]$ShowKeys
)

$ErrorActionPreference = "Stop"

$SecretsDir    = Split-Path -Parent $MyInvocation.MyCommand.Path
$EncryptedFile = Join-Path $SecretsDir "MASTER.env.dpapi"
$FallbackPlain = Join-Path $SecretsDir "MASTER.env"

Add-Type -AssemblyName System.Security

$plaintext = $null

if (Test-Path $EncryptedFile) {
    Write-Host "  Decrypting MASTER.env.dpapi (DPAPI)..." -ForegroundColor Cyan
    $encrypted = [System.IO.File]::ReadAllBytes($EncryptedFile)
    $bytes     = [System.Security.Cryptography.ProtectedData]::Unprotect(
        $encrypted,
        $null,
        [System.Security.Cryptography.DataProtectionScope]::CurrentUser
    )
    $plaintext = [System.Text.Encoding]::UTF8.GetString($bytes)
    Write-Host "  OK Decrypted successfully" -ForegroundColor Green
} elseif (Test-Path $FallbackPlain) {
    Write-Host "  WARNING No .dpapi found -- loading MASTER.env plaintext" -ForegroundColor Yellow
    $plaintext = Get-Content $FallbackPlain -Raw -Encoding UTF8
} else {
    Write-Error "[ABORT] No secrets file found. Expected: $EncryptedFile"
    exit 1
}

$loadedKeys = @()
foreach ($line in ($plaintext -split "`n")) {
    $line = $line.Trim()
    if ($line -eq "" -or $line.StartsWith("#")) { continue }
    if ($line -match "^([A-Z0-9_]+)=(.+)$") {
        $key   = $Matches[1]
        $value = $Matches[2].Trim()
        Set-Item -Path "env:$key" -Value $value
        $loadedKeys += $key
    }
}

if ($ShowKeys) {
    Write-Host ""
    Write-Host "  Loaded $($loadedKeys.Count) secrets into session:" -ForegroundColor DarkGray
    foreach ($k in $loadedKeys) { Write-Host "    - $k" -ForegroundColor DarkGray }
}

Write-Host "  OK $($loadedKeys.Count) secrets loaded into env vars" -ForegroundColor Green
