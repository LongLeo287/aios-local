param(
    [string]$ProjectPath = ""
)
$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  AI OS - UNIFIED MEMORY BACKUP v4.0" -ForegroundColor Cyan
Write-Host "  (Stores active session into project)" -ForegroundColor DarkGray
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

$AiOsRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"

# [1/4] Identify Project
Write-Host "[1/4] Identifying project..." -ForegroundColor Yellow
if (-not $ProjectPath) {
    # If not provided, detect from AI OS parent dir
    $ProjectsRoot = Split-Path $AiOsRoot -Parent
    Write-Host "  Available projects in $($ProjectsRoot):" -ForegroundColor DarkGray
    Get-ChildItem $ProjectsRoot -Directory -EA SilentlyContinue | Where-Object { $_.Name -ne (Split-Path $AiOsRoot -Leaf) } | ForEach-Object {
        Write-Host "    $($_.FullName)"
    }
    Write-Host ""
    $ProjectPath = Read-Host "  Enter project path to backup"
}
if (-not (Test-Path $ProjectPath)) {
    Write-Host "[ABORT] Not found: $ProjectPath" -ForegroundColor Red; exit 1
}

# [CORE PROTECTION RULE] NEVER backup the AI OS library itself
# Normalize paths to handle trailing slashes
$normAiOsRoot = $AiOsRoot.TrimEnd('\').ToLower()
$normProjectPath = (Resolve-Path $ProjectPath).Path.TrimEnd('\').ToLower()

if ($normProjectPath.StartsWith($normAiOsRoot)) {
    Write-Host ""
    Write-Host "[ABORT] VĂN BẢN HỆ THỐNG TỪ CHỐI!" -ForegroundColor Red
    Write-Host "Không thể thực hiện Backup/Wakeup trên chính bản thân hệ thống lõi AI OS." -ForegroundColor Yellow
    Write-Host "Chức năng này CHỈ DÀNH RIÊNG cho Project." -ForegroundColor Gray
    Write-Host ""
    exit 1
}

$ProjectName = Split-Path $ProjectPath -Leaf
$MemoryDir = Join-Path $ProjectPath ".ai-memory"
# Unified approach: save the *specific* active session instead of all brains
$ActiveSessionDir = Join-Path $MemoryDir "active_session"

Write-Host "  [OK] Project: $ProjectName" -ForegroundColor Green
Write-Host "  [OK] Memory : $MemoryDir" -ForegroundColor DarkGray

# [2/4] Detect Active Brain and Conversation
Write-Host "[2/4] Detecting active session..." -ForegroundColor Yellow

$geminiDir = ""
foreach ($c in @("$env:USERPROFILE\.gemini\antigravity", "C:\Users\$env:USERNAME\.gemini\antigravity")) {
    if (Test-Path $c) { $geminiDir = $c; break }
}

if (-not $geminiDir) {
    Write-Host "[ABORT] Cannot find Antigravity directory!" -ForegroundColor Red
    exit 1
}

$conversationsDir = "$geminiDir\conversations"
$brainRoot = "$geminiDir\brain"

# Find most recently modified .pb file (dynamic ID detection)
$latestPb = Get-ChildItem -Path $conversationsDir -Filter "*.pb" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if (-not $latestPb) {
    Write-Host "[ERROR] No active conversation found in $conversationsDir" -ForegroundColor Red
    exit 1
}

$activeId = $latestPb.BaseName
Write-Host "  [OK] Active Session ID: $activeId" -ForegroundColor Green

# [3/4] Copy Active Session into Project
Write-Host "[3/4] Saving to project memory..." -ForegroundColor Yellow

# Clean up old active_session backup if it exists
if (Test-Path $ActiveSessionDir) { Remove-Item $ActiveSessionDir -Recurse -Force | Out-Null }
New-Item -ItemType Directory -Path $ActiveSessionDir -Force | Out-Null
New-Item -ItemType Directory -Path "$ActiveSessionDir\conversations" -Force | Out-Null
New-Item -ItemType Directory -Path "$ActiveSessionDir\brain" -Force | Out-Null

# Copy the .pb file
Copy-Item -Path $latestPb.FullName -Destination "$ActiveSessionDir\conversations\" -Force

# Copy the specific brain folder
$activeBrainDir = Join-Path $brainRoot $activeId
if (Test-Path $activeBrainDir) {
    Copy-Item -Path "$activeBrainDir\*" -Destination "$ActiveSessionDir\brain\" -Recurse -Force
}

# (Optional but useful) Copy global knowledge
$knowledgeDest = Join-Path $MemoryDir "knowledge"
if (Test-Path $knowledgeDest) { Remove-Item $knowledgeDest -Recurse -Force | Out-Null }
$knowledgeSrc = Join-Path $geminiDir "knowledge"
if (Test-Path $knowledgeSrc) {
    robocopy $knowledgeSrc $knowledgeDest /E /R:0 /W:0 /NFL /NDL /NJH /NJS | Out-Null
    Write-Host "  [OK] Knowledge synchronized" -ForegroundColor Green
}

# [4/4] Write Config
@{
    project        = $ProjectName
    project_path   = $ProjectPath
    backed_up_at   = $Timestamp
    machine        = $env:COMPUTERNAME
    user           = $env:USERNAME
    session_id     = $activeId
    restore_cmd    = "Wakeup du an"
} | ConvertTo-Json | Set-Content (Join-Path $MemoryDir "memory_config.json") -Encoding UTF8

Write-Host ""
Write-Host "========================================================" -ForegroundColor Green
Write-Host " [SUCCESS] BACKUP COMPLETE!" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
Write-Host "  Active session securely saved to: $ProjectPath\.ai-memory\" -ForegroundColor White
Write-Host "  To restore on another machine:" -ForegroundColor Yellow
Write-Host "  1. Copy the '$ProjectName' folder" -ForegroundColor Gray
Write-Host "  2. Run 'Wakeup du an' or use wakeup.ps1" -ForegroundColor Gray
Write-Host "========================================================" -ForegroundColor Green
Write-Host ""
