<#
.SYNOPSIS Skill subcommand — aos skill list|health|enable <id>
#>
$AOS_ROOT = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$REGISTRY_PATH = Join-Path $AOS_ROOT "shared-context\SKILL_REGISTRY.json"

switch ($args[0]) {

    "list" {
        if (-not (Test-Path $REGISTRY_PATH)) { Write-Host "❌ Registry not found" -ForegroundColor Red; return }
        $reg = Get-Content $REGISTRY_PATH -Raw | ConvertFrom-Json
        $entries = if ($reg.skills) { $reg.skills } elseif ($reg.entries) { $reg.entries } else { @() }
        # Filter args
        $filterTier = $null; $filterCat = $null
        for ($i = 1; $i -lt $args.Count; $i++) {
            if ($args[$i] -eq "--tier" -and $args[$i+1]) { $filterTier = [int]$args[$i+1] }
            if ($args[$i] -eq "--category" -and $args[$i+1]) { $filterCat = $args[$i+1] }
        }
        if ($filterTier) { $entries = $entries | Where-Object { $_.tier -eq $filterTier } }
        if ($filterCat) { $entries = $entries | Where-Object { $_.category -eq $filterCat } }
        Write-Host "`n📚 Skills ($($entries.Count))" -ForegroundColor Cyan
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
        $entries | ForEach-Object {
            $status = if ($_.status -eq "active" -or -not $_.status) { "✅" } else { "⏸️" }
            $id = if ($_.id) { $_.id } else { $_.name }
            Write-Host "  $status [T$($_.tier)] $id — $($_.category)" -ForegroundColor $(if ($_.tier -eq 1) { "Yellow" } elseif ($_.tier -eq 2) { "White" } else { "Gray" })
        }
    }

    "health" {
        Write-Host "`n🏥 Skill Health Check..." -ForegroundColor Cyan
        if (-not (Test-Path $REGISTRY_PATH)) { Write-Host "❌ Registry not found" -ForegroundColor Red; return }
        $reg = Get-Content $REGISTRY_PATH -Raw | ConvertFrom-Json
        $entries = if ($reg.skills) { $reg.skills } elseif ($reg.entries) { $reg.entries } else { @() }
        $ok = 0; $fail = 0
        foreach ($s in $entries) {
            $name = if ($s.id) { $s.id } else { $s.name }
            $pathVal = $s.path
            if ($pathVal) {
                $fullPath = Join-Path $AOS_ROOT $pathVal "SKILL.md"
                if (Test-Path $fullPath) { $ok++ }
                else { Write-Host "  ❌ Missing: $name ($pathVal)" -ForegroundColor Red; $fail++ }
            } else { $ok++ }
        }
        Write-Host "`n✅ OK: $ok   ❌ Issues: $fail" -ForegroundColor $(if ($fail -eq 0) { "Green" } else { "Yellow" })
    }

    "enable" {
        $id = $args[1]
        if (-not $id) { Write-Host "Usage: aos skill enable <id>" -ForegroundColor Yellow; return }
        Write-Host "✅ Skill '$id' marked active" -ForegroundColor Green
        Write-Host "   (Update SKILL_REGISTRY.json to persist)" -ForegroundColor Gray
    }

    default { Write-Host "Usage: aos skill list [--tier N] [--category C] | health | enable <id>" }
}
