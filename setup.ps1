# ===========================================================
#  AI OS CORP — UNIFIED BOOTSTRAPPER & DASHBOARD
# ===========================================================
$ErrorActionPreference = "Continue"
$RepoRoot = $PSScriptRoot
$AiosRoot = $PSScriptRoot
$Date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Check if OS is already initialized
$ConfigPath = Join-Path $RepoRoot ".aios_config"

if (Test-Path $ConfigPath) {
    # =======================================================
    #  MODE A: DAILY DASHBOARD (ALREADY SETUP)
    # =======================================================
    $Version = "1.9.1"
    $LastUpdate = "2026-03-28"
    
    Clear-Host
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "   ⚙️ AI OS CORP - COGNITIVE OPERATING SYSTEM             " -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "   [Version]     : v$Version" -ForegroundColor Gray
    Write-Host "   [Last Update] : $LastUpdate" -ForegroundColor Gray
    Write-Host "   [System Time] : $Date" -ForegroundColor Gray
    Write-Host "   [Engine]      : Antigravity / Claude Code / Ollama" -ForegroundColor Gray
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   [1] 🚀 Khởi động AI OS (Boot Daily Cycle)" -ForegroundColor Green
    Write-Host "   [2] 📊 Xem Tình trạng Hệ thống (OS Status)" -ForegroundColor Yellow
    Write-Host "   [3] 🔄 Cập nhật (Update AI OS từ Github)" -ForegroundColor Magenta
    Write-Host "   [0] ❌ Thoát" -ForegroundColor Red
    Write-Host ""
    Write-Host "   [Watermark] © 2026 AI OS CORP. All Rights Reserved." -ForegroundColor DarkGray
    Write-Host "----------------------------------------------------------" -ForegroundColor Cyan

    $choice = Read-Host "👉 Chọn chức năng (0-3)"

    if ($choice -eq '1') {
        Write-Host "Đang đánh thức máy chủ Ollama chạy ngầm..." -ForegroundColor Yellow
        Stop-Process -Name "ollama*" -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 1
        Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
        Start-Sleep -Seconds 3

        Write-Host "Đang kích hoạt quy trình Boot Core..." -ForegroundColor Cyan
        Set-Location $AiosRoot
        python system/ops/scripts/aos.py corp start
    } elseif ($choice -eq '2') {
        Write-Host "Đang quét thông tin hệ thống..." -ForegroundColor Cyan
        Set-Location $AiosRoot
        python system/ops/scripts/aos.py status
    } elseif ($choice -eq '3') {
        Write-Host "Đang kiểm tra cập nhật từ kho chứa GitHub..." -ForegroundColor Magenta
        Set-Location $AiosRoot
        git pull origin main
        Write-Host "Cập nhật hoàn tất! Bấm phím bất kỳ để tải lại giao diện..." -ForegroundColor Green
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        .\setup.ps1
    } elseif ($choice -eq '0') {
        Write-Host "OS shutdown signal received." -ForegroundColor DarkGray
    } else {
        Write-Host "Lệnh không hợp lệ!" -ForegroundColor Red
    }
} else {
    # =======================================================
    #  MODE B: FIRST TIME BOOTSTRAPPER (NOT SETUP)
    # =======================================================
    Clear-Host
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "  🌐 AI OS CORP - INITIALIZATION PROTOCOL" -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "   Select Language / Chọn Ngôn Ngữ:" -ForegroundColor Yellow
    Write-Host "   [1] English" -ForegroundColor White
    Write-Host "   [2] Tiếng Việt" -ForegroundColor White
    $Lang = Read-Host "👉 Choice / Chọn (1-2)"
    if ($Lang -ne '1') { $Lang = '2' }
    Clear-Host

    if ($Lang -eq '1') {
        $txtTitle = "⚙️ AI OS CORP - PORTABLE SETUP INSTALLER"
        $txtStep1 = "[1/4] Select AI Model Storage Location (~2GB)..."
        $txtOpt1 = "[1] App-bound (Portable) -> "
        $txtOpt2 = "[2] Default Windows Drive C -> "
        $txtChoice = "Your choice [1 or 2]"
        $txtStep2 = "[2/4] Checking Ollama Engine..."
        $txtNoOllama = "[!] Ollama NOT found. Attempting auto-install..."
        $txtOllamaDown = "[+] Downloading Ollama silently..."
        $txtOllamaFail = "[!] Auto-install failed. Please download manually from https://ollama.com/download"
        $txtOllamaOk = "[✓] Ollama Engine is ready."
        $txtStep3 = "[3/4] Syncing AI Models (gemma2:2b / nomic-embed)..."
        $txtStep4 = "[4/4] Establishing Libraries & Editor Extensions..."
        $txtPyUp  = "  [>] Validating/Updating Python dependencies..."
        $txtExtUp = "  [>] Injecting recommended Editor Extensions..."
        $txtPyReady = "[✓] Python packages are up to date."
        $txtDone = "✅ SETUP COMPLETE! Launching OS Kernel..."
    } else {
        $txtTitle = "⚙️ AI OS CORP - TRÌNH CÀI ĐẶT HỆ THỐNG"
        $txtStep1 = "[1/4] Chọn vị trí lưu Model AI (~2GB)..."
        $txtOpt1 = "[1] Lưu trong lõi AI OS (Portable) -> "
        $txtOpt2 = "[2] Lưu ổ C mặc định -> "
        $txtChoice = "Lựa chọn của bạn [1 hoặc 2]"
        $txtStep2 = "[2/4] Kiểm tra lõi Ollama..."
        $txtNoOllama = "[!] Chưa có Ollama. Đang thử tải tự động..."
        $txtOllamaDown = "[+] Đang tải và cài đặt Ollama ngầm..."
        $txtOllamaFail = "[!] Không thể cài tự động. Vui lòng cài tay từ https://ollama.com/download"
        $txtOllamaOk = "[✓] Hệ thống Ollama đã sẵn sàng."
        $txtStep3 = "[3/4] Đang đồng bộ Models (gemma2:2b / nomic-embed)..."
        $txtStep4 = "[4/4] Thiếp lập Thư viện & Tiện ích Mở rộng (Extensions)..."
        $txtPyUp  = "  [>] Đang kiểm tra/Cập nhật Thư viện Python..."
        $txtExtUp = "  [>] Đang cài đặt các Extension đề xuất..."
        $txtPyReady = "[✓] Thư viện Python đã được cập nhật bản mới nhất."
        $txtDone = "✅ SETUP HOÀN TẤT! Đang nạp Trình khởi động..."
    }

    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "   $txtTitle" -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "   [Version]     : v1.9.1" -ForegroundColor Gray
    Write-Host "   [System Time] : $Date" -ForegroundColor Gray
    Write-Host "   [Root Path]   : $RepoRoot" -ForegroundColor Gray
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host ""

    # STEP 1: MODEL STORAGE
    Write-Host $txtStep1 -ForegroundColor Yellow
    Write-Host "  $txtOpt1 $RepoRoot\OLLAMA_MODELS" -ForegroundColor White
    Write-Host "  $txtOpt2 $env:USERPROFILE\.ollama\models" -ForegroundColor White
    $choice = Read-Host "👉 $txtChoice"
    if ($choice -eq "2") {
        $ModelDir = "$env:USERPROFILE\.ollama\models"
    } else {
        $ModelDir = Join-Path $RepoRoot "OLLAMA_MODELS"
    }
    Write-Host "  [+] Model Path: $ModelDir" -ForegroundColor Green

    # Save Config
    $configPath = Join-Path $RepoRoot ".aios_config"
    "LANGUAGE=$Lang`nOLLAMA_MODELS=$ModelDir" | Set-Content -Path $configPath -Encoding UTF8
    New-Item -ItemType Directory -Force -Path $ModelDir | Out-Null
    $env:OLLAMA_MODELS = $ModelDir
    [Environment]::SetEnvironmentVariable("OLLAMA_MODELS", $ModelDir, "User")
    Write-Host ""

    # STEP 2: OLLAMA CHECK
    Write-Host $txtStep2 -ForegroundColor Yellow
    $ollamaInstalled = $null -ne (Get-Command "ollama" -ErrorAction SilentlyContinue)
    if (-not $ollamaInstalled) {
        Write-Host "  $txtNoOllama" -ForegroundColor Red
        $installerUrl = "https://ollama.com/download/OllamaSetup.exe"
        $installerPath = Join-Path $env:TEMP "OllamaSetup.exe"
        try {
            Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath -UseBasicParsing
            Write-Host "  $txtOllamaDown" -ForegroundColor Magenta
            Start-Process -FilePath $installerPath -ArgumentList "/S" -Wait
            Write-Host "  $txtOllamaOk" -ForegroundColor Green
        }
        catch {
            Write-Host "  $txtOllamaFail" -ForegroundColor Red
            Read-Host "Press Enter to exit..."
            exit 1
        }
    } else {
        Write-Host "  $txtOllamaOk" -ForegroundColor Green
    }
    Write-Host ""

    # STEP 3: SYNC OLLAMA
    Write-Host $txtStep3 -ForegroundColor Yellow
    Stop-Process -Name "ollama*" -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3
    ollama pull gemma2:2b
    ollama pull nomic-embed-text
    Write-Host ""

    # STEP 4: PYTHON DEPENDENCIES & EXTENSIONS
    Write-Host $txtStep4 -ForegroundColor Yellow
    $reqPath = Join-Path $AiosRoot "requirements.txt"
    if (Test-Path $reqPath) {
        Write-Host $txtPyUp -ForegroundColor Gray
        Set-Location $AiosRoot
        pip install -r requirements.txt --upgrade -q
        Write-Host "  $txtPyReady" -ForegroundColor Green
    }

    $codeInstalled = Get-Command "code" -ErrorAction SilentlyContinue
    $extPath = Join-Path $AiosRoot ".vscode\extensions.json"
    if ($codeInstalled -and (Test-Path $extPath)) {
        Write-Host $txtExtUp -ForegroundColor Gray
        try {
            $json = Get-Content $extPath -Raw | ConvertFrom-Json
            if ($json.recommendations) {
                foreach ($ext in $json.recommendations) {
                    Start-Process -FilePath "code" -ArgumentList "--install-extension $ext --force" -WindowStyle Hidden -Wait
                }
                Write-Host "  [✓] Editor Extensions Synced." -ForegroundColor Green
            }
        } catch {}
    }

    # Execute Cognitive Language Sync
    Write-Host "  [>] Synchronizing AI OS Language Core..." -ForegroundColor Gray
    python system/ops/scripts/lang_compiler.py $Lang
    
    [Environment]::SetEnvironmentVariable("AOS_ROOT", $AiosRoot, "User")
    Write-Host "  [✓] AOS_ROOT = $AiosRoot" -ForegroundColor Green
    Write-Host ""

    Write-Host "----------------------------------------------------------" -ForegroundColor Cyan
    Write-Host "   $txtDone" -ForegroundColor Green
    Write-Host "   [Watermark] © 2026 AI OS CORP. All Rights Reserved." -ForegroundColor DarkGray
    Write-Host "----------------------------------------------------------" -ForegroundColor Cyan
    Start-Sleep -Seconds 2

    # Loop back into the same script to show the Daily Dashboard!
    Set-Location $AiosRoot
    .\setup.ps1
}
