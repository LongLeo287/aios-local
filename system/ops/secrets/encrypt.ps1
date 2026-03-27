# AI OS Corp -- DPAPI Secrets Encryptor
# Encrypts MASTER.env using Windows Data Protection API (DPAPI).
# Only the current Windows user on this machine can decrypt.
#
# Input:  ops\secrets\MASTER.env (plaintext)
# Output: ops\secrets\MASTER.env.dpapi (binary encrypted)
# Usage:  .\ops\secrets\encrypt.ps1

$ErrorActionPreference = "Stop"

$SecretsDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$MasterEnv    = Join-Path $SecretsDir "MASTER.env"
$EncryptedOut = Join-Path $SecretsDir "MASTER.env.dpapi"

Write-Host ""
Write-Host "===========================================
" -ForegroundColor Cyan
Write-Host "  AI OS Corp -- DPAPI Encryption" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Add-Type -AssemblyName System.Security

if (-not (Test-Path $MasterEnv)) {
    Write-Error "[ABORT] MASTER.env not found at: $MasterEnv"
    exit 1
}

$plaintext = Get-Content $MasterEnv -Raw -Encoding UTF8
$bytes     = [System.Text.Encoding]::UTF8.GetBytes($plaintext)

$encrypted = [System.Security.Cryptography.ProtectedData]::Protect(
    $bytes,
    $null,
    [System.Security.Cryptography.DataProtectionScope]::CurrentUser
)

[System.IO.File]::WriteAllBytes($EncryptedOut, $encrypted)

Write-Host "  OK Encrypted: $EncryptedOut" -ForegroundColor Green
Write-Host "  OK Scope: CurrentUser -- only user '$env:USERNAME' on this machine can decrypt" -ForegroundColor Green
Write-Host "  INFO MASTER.env kept as-is (delete manually if you only want .dpapi)" -ForegroundColor DarkGray
Write-Host ""

$loaderPath = Join-Path $SecretsDir "load-env.ps1"
Write-Host "  To load secrets into shell session:" -ForegroundColor Yellow
Write-Host "    . $loaderPath" -ForegroundColor White
Write-Host ""
