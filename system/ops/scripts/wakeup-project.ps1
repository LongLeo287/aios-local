param(
    [string]$ProjectPath = ""
)
$ErrorActionPreference = "Continue"
$AiOsRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

Write-Host ""
Write-Host "==========================================" -ForegroundColor Magenta
Write-Host "  AI OS - PROJECT WAKEUP v3.0" -ForegroundColor Magenta
Write-Host "  (restores brain data from project)" -ForegroundColor DarkGray
Write-Host "==========================================" -ForegroundColor Magenta
Write-Host ""

# [1/5] Identify project
Write-Host "[1/5] Identifying project..." -ForegroundColor Yellow
if (-not $ProjectPath) {
    # Auto-detect projects root (parent of AI OS folder)
    $ProjectsRoot = Split-Path $AiOsRoot -Parent
    Write-Host "  Available projects in $ProjectsRoot:" -ForegroundColor DarkGray
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
$ProjectName = Split-Path $ProjectPath -Leaf
$MemoryDir   = Join-Path $ProjectPath ".ai-memory"
Write-Host "  [OK] Project: $ProjectName" -ForegroundColor Green

if (-not (Test-Path $MemoryDir)) {
    Write-Host "[ABORT] No .ai-memory folder found in this project." -ForegroundColor Red
    Write-Host "        Run 'Backup du an' first to save brain data." -ForegroundColor Yellow
    exit 1
}

# Read config
$cfg = if (Test-Path "$MemoryDir\memory_config.json") {
    Get-Content "$MemoryDir\memory_config.json" -Raw | ConvertFrom-Json
} else { $null }
if ($cfg) { Write-Host "  [INFO] Backed up: $($cfg.backed_up_at) from $($cfg.machine)" -ForegroundColor DarkGray }

# [2/5] Detect current antigravity root
Write-Host "[2/5] Detecting brain folder on this machine..." -ForegroundColor Yellow
$CurrentAntigravity = $null
foreach ($c in @("$env:USERPROFILE\.gemini\antigravity", "C:\Users\$env:USERNAME\.gemini\antigravity")) {
    if (Test-Path $c) { $CurrentAntigravity = $c; break }
}
if (-not $CurrentAntigravity) {
    $CurrentAntigravity = Read-Host "  Enter antigravity path (e.g. C:\Users\NAME\.gemini\antigravity)"
}
Write-Host "  [OK] $CurrentAntigravity" -ForegroundColor Green

# [3/5] Restore brain sessions (merge)
Write-Host "[3/5] Restoring brain sessions..." -ForegroundColor Yellow
$brainSrc  = Join-Path $MemoryDir "brain"
$brainDest = Join-Path $CurrentAntigravity "brain"
New-Item -ItemType Directory -Path $brainDest -Force | Out-Null
if (Test-Path $brainSrc) {
    Get-ChildItem $brainSrc -Directory | ForEach-Object {
        robocopy $_.FullName (Join-Path $brainDest $_.Name) /E /R:0 /W:0 /NFL /NDL /NJH /NJS | Out-Null
        Write-Host "    [SESSION] $($_.Name)" -ForegroundColor DarkGray
    }
    Write-Host "  [OK] Sessions restored" -ForegroundColor Green
}

# Restore knowledge
$knowledgeSrc  = Join-Path $MemoryDir "knowledge"
$knowledgeDest = Join-Path $CurrentAntigravity "knowledge"
if (Test-Path $knowledgeSrc) {
    robocopy $knowledgeSrc $knowledgeDest /E /R:0 /W:0 /NFL /NDL /NJH /NJS | Out-Null
    Write-Host "  [OK] Knowledge restored" -ForegroundColor Green
}

# [4/5] Auto-seed current session (newest brain folder = current session)
Write-Host "[4/5] Seeding current session..." -ForegroundColor Yellow
$currentSession = Get-ChildItem $brainDest -Directory |
                  Sort-Object LastWriteTime -Descending | Select-Object -First 1
$oldSessions = Get-ChildItem $brainDest -Directory |
               Where-Object { $_.Name -ne $currentSession.Name } |
               ForEach-Object {
                   [PSCustomObject]@{ Dir = $_; Count = (Get-ChildItem $_.FullName -File -EA SilentlyContinue).Count }
               } | Sort-Object Count -Descending | Select-Object -First 1

if ($currentSession -and $oldSessions) {
    Write-Host "  Current ID : $($currentSession.Name)" -ForegroundColor Cyan
    Write-Host "  Source     : $($oldSessions.Dir.Name)" -ForegroundColor DarkGray
    $keyFiles = @("task.md", "walkthrough.md", "implementation_plan.md", "project_analysis.md")
    foreach ($kf in $keyFiles) {
        $src = Join-Path $oldSessions.Dir.FullName $kf
        $dst = Join-Path $currentSession.FullName $kf
        if ((Test-Path $src) -and -not (Test-Path $dst)) {
            Copy-Item $src $dst -Force
            Write-Host "    [SEEDED] $kf" -ForegroundColor Green
        }
    }
} else {
    Write-Host "  [!] Cannot auto-detect current session." -ForegroundColor Yellow
    Write-Host "  Sessions in brain:" -ForegroundColor DarkGray
    Get-ChildItem $brainDest -Directory | Sort-Object LastWriteTime -Descending | ForEach-Object {
        $fc = (Get-ChildItem $_.FullName -File -EA SilentlyContinue).Count
        Write-Host "    $($_.Name)  [$fc files] $($_.LastWriteTime.ToString('yyyy-MM-dd HH:mm'))" -ForegroundColor DarkGray
    }
    Write-Host ""
    $manualId = Read-Host "  Paste your current session ID"
    if ($manualId) {
        $manualDest = Join-Path $brainDest $manualId.Trim()
        New-Item -ItemType Directory -Path $manualDest -Force | Out-Null
        $best = Get-ChildItem $brainDest -Directory | Where-Object { $_.Name -ne $manualId.Trim() } |
                ForEach-Object { [PSCustomObject]@{ Dir=$_; Count=(Get-ChildItem $_.FullName -File -EA SilentlyContinue).Count } } |
                Sort-Object Count -Descending | Select-Object -First 1
        if ($best) {
            @("task.md","walkthrough.md","implementation_plan.md","project_analysis.md") | ForEach-Object {
                $s = Join-Path $best.Dir.FullName $_; $d = Join-Path $manualDest $_
                if ((Test-Path $s) -and -not (Test-Path $d)) { Copy-Item $s $d -Force; Write-Host "    [SEEDED] $_" -ForegroundColor Green }
            }
        }
    }
}

# [5/5] Rebuild registry
Write-Host "[5/5] Rebuilding skill registry..." -ForegroundColor Yellow
$loader = Join-Path $AiOsRoot "scripts\skill_loader.ps1"
if (Test-Path $loader) { & $loader 2>&1 | Select-Object -Last 3 }

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  WAKEUP COMPLETE!" -ForegroundColor Green
Write-Host "  Project '$ProjectName' is ready." -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  - Brain sessions restored from .ai-memory\" -ForegroundColor Gray
Write-Host "  - Current session seeded with context" -ForegroundColor Gray
Write-Host "  - Continue working!" -ForegroundColor Green
Write-Host ""