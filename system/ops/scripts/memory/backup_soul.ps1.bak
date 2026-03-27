$geminiDir = "$env:USERPROFILE\.gemini\antigravity"

$conversationsDir = "$geminiDir\conversations"

Write-Host "[MEMORY SYNC] Commencing Backup Ritual..."
Write-Host "Scanning for latest conversation soul..."

# Find most recently modified .pb file (dynamic ID detection)
$latestPb = Get-ChildItem -Path $conversationsDir -Filter "*.pb" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if (-not $latestPb) {
    Write-Host "[ERROR] No conversation found in $conversationsDir"
    exit 1
}

$id = $latestPb.BaseName
Write-Host "[FOUND] Detected Active Conversation ID: $id"

$pbFile = $latestPb.FullName
$brainDir = "$geminiDir\brain\$id"

$currentDir = $PSScriptRoot
$backupZip = "$currentDir\soul_backup.zip"
$tempDir = "$currentDir\temp_soul"

Write-Host "[PREPARE] Creating isolated extraction environment..."
if (Test-Path $backupZip) { Remove-Item $backupZip -Force }
if (Test-Path $tempDir) { Remove-Item $tempDir -Recurse -Force }

New-Item -ItemType Directory -Force -Path "$tempDir\conversations" | Out-Null
New-Item -ItemType Directory -Force -Path "$tempDir\brain" | Out-Null

Write-Host "[COPY] Capturing active memory state..."
Copy-Item -Path $pbFile -Destination "$tempDir\conversations\" -Force

# We copy the CONTENTS of the brain directory (not the directory name itself)
# because on WakeUp, we will inject these contents into a DIFFERENT brain ID directory.
if (Test-Path $brainDir) {
    Copy-Item -Path "$brainDir" -Destination "$tempDir\brain" -Recurse -Force
}

Write-Host "[COMPRESS] Sealing memories into ZIP..."
Compress-Archive -Path "$tempDir\*" -DestinationPath $backupZip -Force

Remove-Item $tempDir -Recurse -Force

Write-Host "`n========================================================"
Write-Host " [SUCCESS] BACKUP COMPLETE!"
Write-Host "========================================================"
Write-Host " Soul securely stored in: \.memory\soul_backup.zip"
Write-Host " Session ID Backed Up: $id"
Write-Host " You can now safely commit and push to Git."
Write-Host "========================================================"
