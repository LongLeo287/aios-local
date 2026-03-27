@echo off
echo Running Memory Sync Backup...
powershell -ExecutionPolicy Bypass -File "%~dp0backup.ps1"
pause
