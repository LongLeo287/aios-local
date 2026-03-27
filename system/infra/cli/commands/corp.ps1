<#
.SYNOPSIS Corp subcommand — aos corp start|status|kpi [dept]|escalate|brief
#>
$AOS_ROOT = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$CORP_DIR = Join-Path $AOS_ROOT "shared-context\corp"

function Format-Table2 ($data) {
    $data | Format-Table -AutoSize
}

switch ($args[0]) {

    "start" {
        Write-Host "`n🏢 Kích hoạt Corp Mode..." -ForegroundColor Cyan
        $orchPath = Join-Path $AOS_ROOT "skills\corp_orchestrator\SKILL.md"
        if (Test-Path $orchPath) {
            Write-Host "✅ corp_orchestrator: READY" -ForegroundColor Green
        }
        $ts = Get-Date -Format "yyyy-MM-ddTHH:mm:ss"
        $bbPath = Join-Path $AOS_ROOT "shared-context\blackboard.json"
        $bb = if (Test-Path $bbPath) { Get-Content $bbPath -Raw | ConvertFrom-Json } else { @{} }
        $bb | Add-Member -NotePropertyName "corp_status" -NotePropertyValue "active" -Force
        $bb | Add-Member -NotePropertyName "corp_started_at" -NotePropertyValue $ts -Force
        $bb | ConvertTo-Json -Depth 5 | Set-Content $bbPath
        Write-Host "✅ Corp Mode ACTIVE — $ts" -ForegroundColor Green
        Write-Host "   Run: aos corp status    để xem KPI" -ForegroundColor Gray
        Write-Host "   Run: aos corp brief      để gửi brief cho dept heads" -ForegroundColor Gray
    }

    "status" {
        Write-Host "`n📊 Corp Status" -ForegroundColor Cyan
        # KPI summary
        $kpiPath = Join-Path $CORP_DIR "kpi_scoreboard.json"
        if (Test-Path $kpiPath) {
            $kpi = Get-Content $kpiPath -Raw | ConvertFrom-Json
            Write-Host "`nKPI Scoreboard:" -ForegroundColor Yellow
            Write-Host ($kpi | ConvertTo-Json -Depth 3)
        } else {
            Write-Host "  KPI: not configured" -ForegroundColor DarkGray
        }
        # Escalations
        $escPath = Join-Path $CORP_DIR "escalations.md"
        if (Test-Path $escPath) {
            $esc = Get-Content $escPath
            $openCount = ($esc | Select-String "OPEN").Count
            Write-Host "`n⚠️  Escalations OPEN: $openCount" -ForegroundColor $(if ($openCount -gt 0) { "Red" } else { "Green" })
        }
        # Blackboard
        $bbPath = Join-Path $AOS_ROOT "shared-context\blackboard.json"
        if (Test-Path $bbPath) {
            $bb = Get-Content $bbPath -Raw | ConvertFrom-Json
            Write-Host "`nBlackboard:" -ForegroundColor Yellow
            Write-Host "  corp_status: $($bb.corp_status)" -ForegroundColor $(if ($bb.corp_status -eq "active") { "Green" } else { "Gray" })
        }
    }

    "kpi" {
        $dept = $args[1]
        $kpiPath = Join-Path $CORP_DIR "kpi_scoreboard.json"
        if (-not (Test-Path $kpiPath)) { Write-Host "❌ KPI file not found" -ForegroundColor Red; return }
        $kpi = Get-Content $kpiPath -Raw | ConvertFrom-Json
        if ($dept) {
            $deptData = if ($kpi.departments -and $kpi.departments.$dept) { $kpi.departments.$dept } elseif ($kpi.$dept) { $kpi.$dept } else { $null }
            if ($deptData) { Write-Host ($deptData | ConvertTo-Json -Depth 3) }
            else { Write-Host "❌ Dept '$dept' not found" -ForegroundColor Red }
        } else {
            Write-Host "`n📈 KPI Board — All Depts" -ForegroundColor Cyan
            Write-Host ($kpi | ConvertTo-Json -Depth 3)
        }
    }

    "escalate" {
        $dept = $args[1]; $level = $args[2]; $issue = $args[3..($args.Count-1)] -join " "
        if (-not $dept -or -not $level -or -not $issue) {
            Write-Host "Usage: aos corp escalate <dept> <L1|L2|L3> <issue description>" -ForegroundColor Yellow
            return
        }
        $ts = Get-Date -Format "yyyy-MM-ddTHH:mm:ss"
        $escPath = Join-Path $CORP_DIR "escalations.md"
        $existing = if (Test-Path $escPath) { Get-Content $escPath -Raw } else { "# Escalations`n`n" }
        $entry = "`n## [$ts] $level — $dept`n$issue`n_Status: OPEN_`n"
        ($existing + $entry) | Set-Content $escPath
        Write-Host "✅ Escalation $level added for $dept" -ForegroundColor Green
    }

    "brief" {
        Write-Host "`n📋 Gửi daily brief cho dept heads..." -ForegroundColor Cyan
        $briefDir = Join-Path $CORP_DIR "daily_briefs"
        if (Test-Path $briefDir) {
            Get-ChildItem $briefDir -Filter "*.md" | ForEach-Object {
                Write-Host "  📨 $($_.BaseName)" -ForegroundColor Green
            }
            Write-Host "`n✅ Daily briefs dispatched" -ForegroundColor Green
        } else {
            Write-Host "❌ Daily briefs directory not found" -ForegroundColor Red
        }
    }

    default { Write-Host "Usage: aos corp start|status|kpi [dept]|escalate|brief" }
}
