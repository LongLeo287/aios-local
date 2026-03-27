param(
    [string]$ProjectPath = ""
)
$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "==========================================" -ForegroundColor Magenta
Write-Host "  AI OS - UNIFIED WAKEUP v4.0" -ForegroundColor Magenta
Write-Host "  (Restores active session from project)" -ForegroundColor DarkGray
Write-Host "==========================================" -ForegroundColor Magenta
Write-Host ""

$AiOsRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

# [1/5] Identify Project
Write-Host "[1/5] Identifying project..." -ForegroundColor Yellow
if (-not $ProjectPath) {
    $ProjectsRoot = Split-Path $AiOsRoot -Parent
    Write-Host "  Available projects in $($ProjectsRoot):" -ForegroundColor DarkGray
    Get-ChildItem $ProjectsRoot -Directory -EA SilentlyContinue | Where-Object { $_.Name -ne (Split-Path $AiOsRoot -Leaf) } | ForEach-Object {
        $hasMemory = Test-Path (Join-Path $_.FullName ".ai-memory")
        $tag = if ($hasMemory) { "[HAS BACKUP]" } else { "" }
        Write-Host "    $($_.FullName)  $tag" -ForegroundColor $(if ($hasMemory) { "Green" } else { "Gray" })
    }
    Write-Host ""
    $ProjectPath = Read-Host "  Enter project path to restore"
}

if (-not (Test-Path $ProjectPath)) {
    Write-Host "[ABORT] Not found: $ProjectPath" -ForegroundColor Red; exit 1
}

# [CORE PROTECTION RULE] NEVER wakeup the AI OS library itself
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
$MemoryDir   = Join-Path $ProjectPath ".ai-memory"
Write-Host "  [OK] Project: $ProjectName" -ForegroundColor Green

if (-not (Test-Path $MemoryDir)) {
    Write-Host "[ABORT] No .ai-memory folder found in this project." -ForegroundColor Red
    exit 1
}

$cfg = if (Test-Path "$MemoryDir\memory_config.json") {
    Get-Content "$MemoryDir\memory_config.json" -Raw | ConvertFrom-Json
} else { $null }

if ($cfg) { 
    Write-Host "  [INFO] Backup from: $($cfg.backed_up_at) (Machine: $($cfg.machine))" -ForegroundColor DarkGray 
}

# [2/5] Detect Current AI Environment
Write-Host "[2/5] Locating Active AI Session..." -ForegroundColor Yellow
$geminiDir = ""
foreach ($c in @("$env:USERPROFILE\.gemini\antigravity", "C:\Users\$env:USERNAME\.gemini\antigravity")) {
    if (Test-Path $c) { $geminiDir = $c; break }
}

if (-not $geminiDir) {
    Write-Host "[ABORT] Cannot find Antigravity directory!" -ForegroundColor Red
    exit 1
}

$conversationsDir = "$geminiDir\conversations"
$targetPb = Get-ChildItem -Path $conversationsDir -Filter "*.pb" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if (-not $targetPb) {
    Write-Host "[ERROR] No active conversation found to inherit memory. Please start the AI Assistant first." -ForegroundColor Red
    exit 1
}

$targetId = $targetPb.BaseName
Write-Host "  [OK] Injecting into Session ID: $targetId" -ForegroundColor Cyan

# [3/5] Restore Session
Write-Host "[3/5] Injecting Brain Memories..." -ForegroundColor Yellow
$ActiveSessionDir = Join-Path $MemoryDir "active_session"

if (-not (Test-Path $ActiveSessionDir)) {
    Write-Host "[ERROR] Legacy backup format detected (No active_session folder)." -ForegroundColor Red
    Write-Host "Please re-run Backup on the original machine using the new v4.0 script." -ForegroundColor Yellow
    exit 1
}

# 1. Overwrite conversation (.pb)
$backupPb = Get-ChildItem -Path "$ActiveSessionDir\conversations" -Filter "*.pb" | Select-Object -First 1
if ($backupPb) {
    Write-Host "  - Restoring Chat History (.pb)..." -ForegroundColor DarkGray
    Copy-Item -Path $backupPb.FullName -Destination "$conversationsDir\$targetId.pb" -Force
}

# 2. Inject brain folder
$backupBrainDir = "$ActiveSessionDir\brain"
$targetBrainDir = "$geminiDir\brain\$targetId"

if (-not (Test-Path $targetBrainDir)) { New-Item -ItemType Directory -Force -Path $targetBrainDir | Out-Null }

if (Test-Path $backupBrainDir) {
    Write-Host "  - Overwriting Brain Artifacts..." -ForegroundColor DarkGray
    Copy-Item -Path "$backupBrainDir\*" -Destination "$targetBrainDir\" -Recurse -Force
}

Write-Host "  [OK] Session restored" -ForegroundColor Green

# [4/5] Restore Knowledge
Write-Host "[4/5] Syncing global knowledge..." -ForegroundColor Yellow
$knowledgeSrc  = Join-Path $MemoryDir "knowledge"
$knowledgeDest = Join-Path $geminiDir "knowledge"
if (Test-Path $knowledgeSrc) {
    robocopy $knowledgeSrc $knowledgeDest /E /R:0 /W:0 /NFL /NDL /NJH /NJS | Out-Null
    Write-Host "  [OK] Knowledge restored" -ForegroundColor Green
} else {
    Write-Host "  [SKIP] No knowledge to sync" -ForegroundColor DarkGray
}

# [5/5] Rebuild Registry
Write-Host "[5/5] Rebuilding skill registry..." -ForegroundColor Yellow
$loader = Join-Path $AiOsRoot "scripts\skill_loader.ps1"
if (Test-Path $loader) { & $loader 2>&1 | Select-Object -Last 3 }

Write-Host "`n========================================================" -ForegroundColor Green
Write-Host " [SUCCESS] WAKE UP COMPLETE!" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
Write-Host "  Memory successfully injected into current session." -ForegroundColor White
Write-Host "  Target Session: $targetId" -ForegroundColor Cyan
Write-Host "  Project: $ProjectName" -ForegroundColor Cyan
Write-Host ""
Write-Host "  [!] ACTION REQUIRED: " -ForegroundColor Yellow
Write-Host "  Reload the AI extension view or restart VS Code to" -ForegroundColor Gray
Write-Host "  see the restored chat history and artifacts." -ForegroundColor Gray
Write-Host "========================================================" -ForegroundColor Green
Write-Host ""
