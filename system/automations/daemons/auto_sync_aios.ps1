$env:PYTHONIOENCODING = "utf-8"
$ScriptDir = Split-Path $MyInvocation.MyCommand.Path
$BaseDir = Split-Path $ScriptDir -Parent | Split-Path -Parent | Split-Path -Parent
$InjectorScript = Join-Path $BaseDir "system\ops\scripts\aios_context_injector.py"
$env:AOS_ROOT = $BaseDir

Write-Host "Starting AI OS Context Auto-Sync loop (every 60s) from $BaseDir ..."

while ($true) {
    try {
        Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Syncing tasks..."
        python $InjectorScript
    } catch {
        Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Sync failed: $_"
    }
    Start-Sleep -Seconds 60
}
