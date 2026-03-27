@echo off
REM —————————————————————————————————————————————————————————————————————————
REM  AI OS Corp — Start Infrastructure
REM  Starts: API Bridge (port 7000), 3x MCP Servers
REM  Note: ClawTask (7474) is the main hub -- start via launcher\START AI OS.ps1
REM  Usage: scripts\start-infrastructure.bat
REM —————————————————————————————————————————————————————————————————————————

REM Auto-detect AOS root from script location (scripts\ lives inside ops\)
FOR %%I IN ("%~dp0\..\..") DO SET AOS_ROOT=%%~fI
SET SCRIPTS_DIR=%AOS_ROOT%\ops\scripts
SET LOGS_DIR=%AOS_ROOT%\ops\telemetry\logs

if not exist "%LOGS_DIR%" mkdir "%LOGS_DIR%"

echo.
echo  â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
echo.

REM â”€â”€â”€ Load env â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
if not exist "%AOS_ROOT%\.env" (
    echo  [ERROR] .env file not found at %AOS_ROOT%\.env
    exit /b 1
)

REM â”€â”€â”€ 1. API Bridge (port 7000) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
echo  [1/4] Starting API Bridge on port 7000...
start "AOS-API-Bridge" /min cmd /c "node "%AOS_ROOT%\api\server.js" > "%LOGS_DIR%\api-bridge.log" 2>&1"
timeout /t 1 /nobreak > nul
echo      OK â€” http://localhost:7000

REM â”€â”€â”€ 2. MCP: aos-workspace â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
echo  [2/4] Starting MCP: aos-workspace...
start "MCP-aos-workspace" /min cmd /c "node "%AOS_ROOT%\mcp\servers\aos-workspace\index.js" 2> "%LOGS_DIR%\mcp-aos-workspace.log""
timeout /t 1 /nobreak > nul
echo      OK â€” stdio (Claude Code MCP)

REM â”€â”€â”€ 3. MCP: skill-registry â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
echo  [3/4] Starting MCP: skill-registry...
start "MCP-skill-registry" /min cmd /c "node "%AOS_ROOT%\mcp\servers\skill-registry\index.js" 2> "%LOGS_DIR%\mcp-skill-registry.log""
timeout /t 1 /nobreak > nul
echo      OK â€” stdio (Claude Code MCP)

REM â”€â”€â”€ 4. MCP: corp-data â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
echo  [4/5] Starting MCP: corp-data...
start "MCP-corp-data" /min cmd /c "node "%AOS_ROOT%\mcp\servers\corp-data\index.js" 2> "%LOGS_DIR%\mcp-corp-data.log""
timeout /t 1 /nobreak > nul
echo      OK â€” stdio (Claude Code MCP)

echo.
echo  â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
echo  Services running:
echo    ClawTask Hub     : http://localhost:7474/         (main control)
echo    API Bridge       : http://localhost:7000/health
echo    9Router (LLM)    : http://localhost:20128
echo    Ollama           : http://localhost:11434
echo    nullclaw (Bot)   : http://localhost:3000/health
echo    open-notebook UI : http://localhost:8502
echo    open-notebook API: http://localhost:5055/health
echo  â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
echo.
echo  Logs: %LOGS_DIR%\
echo  Press any key to exit this window (services keep running)...
pause > nul

