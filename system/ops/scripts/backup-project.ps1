param(
    [string]$ProjectPath = ""
)
$ErrorActionPreference = "Continue"
$AiOsRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  AI OS - PROJECT MEMORY BACKUP v3.0" -ForegroundColor Cyan
Write-Host "  (stores brain data inside project)" -ForegroundColor DarkGray
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# [1/4] Identify project
Write-Host "[1/4] Identifying project..." -ForegroundColor Yellow
if (-not $ProjectPath) {
    # Auto-detect projects root (parent of AI OS folder)
    $ProjectsRoot = Split-Path $AiOsRoot -Parent
    Write-Host "  Available projects in $ProjectsRoot:" -ForegroundColor DarkGray
    Get-ChildItem $ProjectsRoot -Directory -EA SilentlyContinue | Where-Object { $_.Name -ne (Split-Path $AiOsRoot -Leaf) } | ForEach-Object {
        Write-Host "    $($_.FullName)"
    }
    Write-Host ""
    $ProjectPath = Read-Host "  Enter project path to backup"
}
if (-not (Test-Path $ProjectPath)) {
    Write-Host "[ABORT] Not found: $ProjectPath" -ForegroundColor Red; exit 1
}
$ProjectName = Split-Path $ProjectPath -Leaf
$MemoryDir   = Join-Path $ProjectPath ".ai-memory"
Write-Host "  [OK] Project: $ProjectName" -ForegroundColor Green
Write-Host "  [OK] Memory : $MemoryDir" -ForegroundColor DarkGray

# [2/4] Detect brain
Write-Host "[2/4] Detecting brain/chat history..." -ForegroundColor Yellow
$BrainRoot = $null
foreach ($c in @("$env:USERPROFILE\.gemini\antigravity\brain", "C:\Users\$env:USERNAME\.gemini\antigravity\brain")) {
    if (Test-Path $c) { $BrainRoot = $c; break }
}
if (-not $BrainRoot) {
    Write-Host "  [WARN] Brain not found. Enter path or Enter to skip:" -ForegroundColor Yellow
    $BrainRoot = Read-Host "  Brain path"
    if (-not (Test-Path $BrainRoot)) { $BrainRoot = $null }
}
if ($BrainRoot) { Write-Host "  [OK] Brain: $BrainRoot" -ForegroundColor Green }
else { Write-Host "  [SKIP] Brain not found." -ForegroundColor DarkGray }

# [3/4] Copy brain INTO project folder
Write-Host "[3/4] Saving brain data into project..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path $MemoryDir -Force | Out-Null

if ($BrainRoot) {
    $AntigravityRoot = Split-Path $BrainRoot -Parent
    # Copy brain sessions
    robocopy $BrainRoot (Join-Path $MemoryDir "brain") /E /R:0 /W:0 /NFL /NDL /NJH /NJS /XD "tempmediaStorage" | Out-Null
    # Copy knowledge items
    $knowledgeDir = Join-Path $AntigravityRoot "knowledge"
    if (Test-Path $knowledgeDir) {
        robocopy $knowledgeDir (Join-Path $MemoryDir "knowledge") /E /R:0 /W:0 /NFL /NDL /NJH /NJS | Out-Null
    }
    $memFiles = (Get-ChildItem $MemoryDir -Recurse -File -EA SilentlyContinue).Count
    $memSize  = [math]::Round(((Get-ChildItem $MemoryDir -Recurse -File -EA SilentlyContinue | Measure-Object -Property Length -Sum).Sum) / 1MB, 1)
    Write-Host "  [OK] $memFiles files, $memSize MB saved to .ai-memory\" -ForegroundColor Green
}

# [4/4] Write config
@{
    project        = $ProjectName
    project_path   = $ProjectPath
    backed_up_at   = $Timestamp
    machine        = $env:COMPUTERNAME
    user           = $env:USERNAME
    brain_sessions = (Get-ChildItem (Join-Path $MemoryDir "brain") -Directory -EA SilentlyContinue | Measure-Object).Count
    restore_cmd    = "Wakeup du an"
} | ConvertTo-Json | Set-Content (Join-Path $MemoryDir "memory_config.json") -Encoding UTF8

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  BACKUP COMPLETE!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  Brain data saved inside: $ProjectPath\.ai-memory\" -ForegroundColor White
Write-Host ""
Write-Host "  To switch machines:" -ForegroundColor Yellow
Write-Host "  1. Copy the entire '$ProjectName' folder to new machine" -ForegroundColor Gray
Write-Host "  2. Open workspace on new machine" -ForegroundColor Gray
Write-Host "  3. Say: Wakeup du an" -ForegroundColor Gray
Write-Host ""