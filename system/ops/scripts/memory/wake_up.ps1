$currentDir = $PSScriptRoot
$backupZip = "$currentDir\soul_backup.zip"
$geminiDir = "$env:USERPROFILE\.gemini\antigravity"


Write-Host "[MEMORY SYNC] Commencing Wake Up Ritual..."

if (-not (Test-Path $backupZip)) {
    Write-Host "[ERROR] No soul_backup.zip found in $currentDir!"
    exit 1
}

Write-Host "[EXTRACT] Expanding Soul into temporary space..."
$tempDir = "$currentDir\temp_wakeup"
if (Test-Path $tempDir) { Remove-Item $tempDir -Recurse -Force }

Expand-Archive -Path $backupZip -DestinationPath $tempDir -Force

Write-Host "[INJECT] Searching for current Active Session to inherit memory..."

# Find the newest .pb file (which will be the current active session ID)
$conversationsDir = "$geminiDir\conversations"
if (-not (Test-Path $conversationsDir)) { New-Item -ItemType Directory -Force -Path $conversationsDir | Out-Null }

$targetPb = Get-ChildItem -Path $conversationsDir -Filter "*.pb" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if (-not $targetPb) {
    Write-Host "[ERROR] No active conversation found to inherit memory. Please start the AI Assistant first."
    Remove-Item $tempDir -Recurse -Force
    exit 1
}

$targetId = $targetPb.BaseName
Write-Host "[TARGET] Found active session ID: $targetId"

# 1. Handle Conversations (.pb file)
$backupPb = Get-ChildItem -Path "$tempDir\conversations" -Filter "*.pb" | Select-Object -First 1
if ($backupPb) {
    Write-Host "         - Overwriting active conversation file..."
    Copy-Item -Path $backupPb.FullName -Destination "$conversationsDir\$targetId.pb" -Force
}

# 2. Handle Brain Directory
$backupBrainDir = Get-ChildItem -Path "$tempDir\brain" -Directory | Select-Object -First 1
$targetBrainDir = "$geminiDir\brain\$targetId"

if (-not (Test-Path $targetBrainDir)) { New-Item -ItemType Directory -Force -Path $targetBrainDir | Out-Null }

if ($backupBrainDir) {
    Write-Host "         - Injecting brain memories into active session..."
    Copy-Item -Path "$($backupBrainDir.FullName)\*" -Destination "$targetBrainDir\" -Recurse -Force
}

Remove-Item $tempDir -Recurse -Force

Write-Host "`n========================================================"
Write-Host " [SUCCESS] WAKE UP COMPLETE!"
Write-Host "========================================================"
Write-Host " Memory successfully inherited into Session ID: $targetId"
Write-Host " Reload the AI extension in VS Code to access chat history."
Write-Host "========================================================"
