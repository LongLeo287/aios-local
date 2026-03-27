@echo off
:: ==========================================================
:: AI OS CORP — NATIVE WINDOWS LAUNCHER (Double-Click Execution)
:: ==========================================================
color 0a
title AI OS CORP - Cognitive Operating System

:: Check for Administrative privileges (Optional, but good for setup)
:: We primarily just need to bypass execution policy for the unified PowerShell script.
echo [AI OS] Tự động cấp quyền và nạp Trình Điều Khiển Hệ Thống...
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "%~dp0setup.ps1"

pause
