<#
.SYNOPSIS
    AI OS CLI — Điều khiển AI OS từ terminal
.USAGE
    .\cli\aos.ps1 <module> <command> [args]
    
    aos skill list [--tier N] [--category C]
    aos skill health
    aos corp start / status / kpi [dept]
    aos mcp list / start <name> / stop <name>
    aos llm cost / test <provider> / route <task>
    aos api start / stop / status
    aos plugin audit
    aos context export
#>

$AOS_ROOT = Split-Path -Parent $PSScriptRoot
$API_PORT = 7000
$script:ApiProc = $null

# Load subcommand modules
$CmdDir = Join-Path $PSScriptRoot "commands"

function Show-Help {
    Write-Host "`n🤖 AI OS CLI v1.0" -ForegroundColor Cyan
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    Write-Host "START:   aos start                        ← Cognitive Boot (đọc GEMINI/SOUL/...)" -ForegroundColor Green
    Write-Host "SKILL:   aos skill list | health | enable <id>" -ForegroundColor Green
    Write-Host "CORP:    aos corp start | status | kpi [dept]" -ForegroundColor Yellow
    Write-Host "MCP:     aos mcp list | start <name> | stop <name>" -ForegroundColor Magenta
    Write-Host "LLM:     aos llm cost | test <provider> | route <task>" -ForegroundColor Blue
    Write-Host "API:     aos api start | stop | status" -ForegroundColor Cyan
    Write-Host "PLUGIN:  aos plugin list | audit" -ForegroundColor White
    Write-Host "CONTEXT: aos context export" -ForegroundColor Gray
    Write-Host ""
}

function Invoke-Skill { & (Join-Path $CmdDir "skill.ps1") @args }
function Invoke-Corp { & (Join-Path $CmdDir "corp.ps1") @args }
function Invoke-Mcp { & (Join-Path $CmdDir "mcp.ps1") @args }
function Invoke-Llm { & (Join-Path $CmdDir "llm.ps1") @args }

function Invoke-Api {
    param($Cmd)
    switch ($Cmd) {
        "start" {
            $serverJs = Join-Path $AOS_ROOT "api\server.js"
            if (-not (Test-Path $serverJs)) { Write-Host "❌ api/server.js not found" -ForegroundColor Red; return }
            Write-Host "🚀 Starting REST API Bridge on port $API_PORT..." -ForegroundColor Cyan
            Start-Process "node" -ArgumentList $serverJs -PassThru -WindowStyle Hidden | Out-Null
            Start-Sleep 1
            Write-Host "✅ API Bridge running at http://localhost:$API_PORT" -ForegroundColor Green
        }
        "stop" {
            Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object {
                $_.CommandLine -like "*aos*server*"
            } | Stop-Process
            Write-Host "🛑 API Bridge stopped" -ForegroundColor Yellow
        }
        "status" {
            try {
                $r = Invoke-RestMethod "http://localhost:$API_PORT/health" -TimeoutSec 2
                Write-Host "✅ API Bridge: RUNNING — $($r.timestamp)" -ForegroundColor Green
            } catch {
                Write-Host "❌ API Bridge: NOT RUNNING" -ForegroundColor Red
            }
        }
        default { Write-Host "Usage: aos api start|stop|status" }
    }
}

function Invoke-Plugin {
    param($Cmd)
    $pluginsDir = Join-Path $AOS_ROOT "plugins"
    $dirs = Get-ChildItem $pluginsDir -Directory
    switch ($Cmd) {
        "list" {
            Write-Host "`n📦 Plugins ($($dirs.Count) total)" -ForegroundColor Cyan
            foreach ($d in $dirs) {
                $hasSkill = Test-Path (Join-Path $d.FullName "SKILL.md")
                $icon = if ($hasSkill) { "✅" } else { "❌" }
                Write-Host "  $icon $($d.Name)"
            }
        }
        "audit" {
            $missing = $dirs | Where-Object { -not (Test-Path (Join-Path $_.FullName "SKILL.md")) }
            if ($missing.Count -eq 0) {
                Write-Host "✅ All $($dirs.Count) plugins have SKILL.md" -ForegroundColor Green
            } else {
                Write-Host "❌ Missing SKILL.md ($($missing.Count)):" -ForegroundColor Red
                $missing | ForEach-Object { Write-Host "  - $($_.Name)" -ForegroundColor Yellow }
            }
        }
        default { Write-Host "Usage: aos plugin list|audit" }
    }
}

function Invoke-Context {
    param($Cmd)
    switch ($Cmd) {
        "export" {
            $ctxPath = Join-Path $AOS_ROOT "shared-context\AI_OS_CONTEXT.md"
            if (Test-Path $ctxPath) {
                $content = Get-Content $ctxPath -Raw
                $content | Set-Clipboard
                Write-Host "✅ AI_OS_CONTEXT.md copied to clipboard!" -ForegroundColor Green
                Write-Host "   Paste vào ChatGPT, Gemini, hoặc bất kỳ AI nào" -ForegroundColor Gray
            } else {
                Write-Host "❌ AI_OS_CONTEXT.md not found" -ForegroundColor Red
            }
        }
        default { Write-Host "Usage: aos context export" }
    }
}

# === MAIN DISPATCHER ===
if ($args.Count -eq 0) { Show-Help; exit 0 }

$module = $args[0]
$rest = $args[1..($args.Count-1)]

switch ($module) {
    "start"   {
        $pyExe = (Get-Command python -EA SilentlyContinue).Source
        if ($pyExe) {
            & $pyExe (Join-Path $AOS_ROOT "system\ops\scripts\aos_start.py")
        } else {
            Write-Host "❌ Python not found. Cannot run cognitive boot." -ForegroundColor Red
        }
    }
    "skill"   { Invoke-Skill @rest }
    "corp"    { Invoke-Corp @rest }
    "mcp"     { Invoke-Mcp @rest }
    "llm"     { Invoke-Llm @rest }
    "api"     { Invoke-Api $rest[0] }
    "plugin"  { Invoke-Plugin $rest[0] }
    "context" { Invoke-Context $rest[0] }
    "help"    { Show-Help }
    default   {
        Write-Host "❓ Unknown module: $module" -ForegroundColor Red
        Show-Help
    }
}
