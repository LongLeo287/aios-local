$ErrorActionPreference = "Stop"
$OPENCLAW_DIR = "<AI_OS_ROOT>\plugins\openclaw"

Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "      AI OS CORP - OPENCLAW SUPERVISOR NODE      " -ForegroundColor Magenta
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "[INFRA] Initialize Supervisor Gateway..."
Write-Host "[INFRA] Reading Context: AGENTS.md & 4-Tier Arch"
Write-Host "[INFRA] Connecting to NVIDIA NIM (Llama 405B)..."

Write-Host "[INFRA] Loading Workspace: <AI_OS_ROOT>..." -ForegroundColor Green
$env:OPENCLAW_HOME=$env:AOS_ROOT
Set-Location "<AI_OS_ROOT>\plugins\openclaw"

# Run the OpenClaw Gateway natively using node pointing to the mjs file
Write-Host "[INFRA] Starting OpenClaw Gateway on Port 18789..." -ForegroundColor Yellow
pnpm openclaw gateway --port 18789 --verbose --allow-unconfigured

