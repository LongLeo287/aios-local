$env:PYTHONIOENCODING = "utf-8"
$ScriptDir = Split-Path $MyInvocation.MyCommand.Path
$BaseDir = Split-Path $ScriptDir -Parent | Split-Path -Parent
$InjectorScript = Join-Path $ScriptDir "aios_context_injector.py"

Write-Host "Starting AI OS Context Auto-Sync loop (every 60s)..."

while ($true) {
    try {
        Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Syncing tasks..."
        python $InjectorScript
    } catch {
        Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Sync failed: $_"
    }
    Start-Sleep -Seconds 60
}
