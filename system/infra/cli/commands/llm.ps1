<#
.SYNOPSIS LLM subcommand — aos llm cost|test <provider>|route <task>|list
#>
$AOS_ROOT = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$ROUTER_PATH = Join-Path $AOS_ROOT "llm\router.yaml"
$CONFIG_PATH = Join-Path $AOS_ROOT "llm\config.yaml"

# Cost table (per 1K input tokens, USD)
$CostTable = @(
    [PSCustomObject]@{ Model="minimax-text"; Input=0.0003; Output=0.0009; BestFor="Economy, bulk" }
    [PSCustomObject]@{ Model="claude-haiku"; Input=0.00025; Output=0.00125; BestFor="Quick Q&A" }
    [PSCustomObject]@{ Model="gpt-4o-mini"; Input=0.00015; Output=0.0006; BestFor="General economy" }
    [PSCustomObject]@{ Model="glm-5"; Input=0.0014; Output=0.0014; BestFor="Coding, 205K ctx" }
    [PSCustomObject]@{ Model="kimi-k2.5"; Input=0.0014; Output=0.0014; BestFor="Vision, agents" }
    [PSCustomObject]@{ Model="gpt-4o"; Input=0.005; Output=0.015; BestFor="Premium general" }
    [PSCustomObject]@{ Model="claude-sonnet"; Input=0.003; Output=0.015; BestFor="Premium coding" }
    [PSCustomObject]@{ Model="claude-opus"; Input=0.018; Output=0.09; BestFor="Complex reasoning" }
)

switch ($args[0]) {

    "cost" {
        Write-Host "`n💰 LLM Cost Comparison (per 1K tokens)" -ForegroundColor Cyan
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
        $CostTable | Format-Table -Property Model,
            @{L="Input/1K";E={"`$$($_.Input)"}},
            @{L="Output/1K";E={"`$$($_.Output)"}},
            BestFor -AutoSize
        Write-Host "Tip: minimax-text = cheapest bulk, claude-haiku = cheapest fast" -ForegroundColor DarkGray
    }

    "route" {
        $task = $args[1]
        if (-not $task) { Write-Host "Usage: aos llm route <task-type>" -ForegroundColor Yellow; return }
        if (-not (Test-Path $ROUTER_PATH)) { Write-Host "❌ llm/router.yaml not found" -ForegroundColor Red; return }
        $lines = Get-Content $ROUTER_PATH
        $inTask = $false; $found = @{}
        foreach ($line in $lines) {
            if ($line.Trim() -eq "${task}:") { $inTask = $true; continue }
            if ($inTask -and $line -match "^  (\w+): (.+)") {
                $found[$matches[1]] = $matches[2]
                if ($found.Count -ge 5) { break }
            }
            if ($inTask -and $line -match "^\w" -and $line -notmatch "^\s") { break }
        }
        if ($found.Count -eq 0) { Write-Host "❌ Task type '$task' not in router" -ForegroundColor Red; return }
        Write-Host "`n🎯 LLM Routing: $task" -ForegroundColor Cyan
        Write-Host "  Primary : $($found.primary)" -ForegroundColor Green
        Write-Host "  Backup  : $($found.backup)" -ForegroundColor Yellow
        Write-Host "  Economy : $($found.economy)" -ForegroundColor Gray
        Write-Host "  Dept    : $($found.dept)" -ForegroundColor DarkGray
    }

    "test" {
        $provider = $args[1]
        if (-not $provider) { Write-Host "Usage: aos llm test <provider>" -ForegroundColor Yellow; return }
        Write-Host "🔗 Testing $provider API..." -ForegroundColor Cyan
        $envVars = @{
            "anthropic" = "ANTHROPIC_API_KEY"
            "openai"    = "OPENAI_API_KEY"
            "glm5"      = "GLM5_API_KEY"
            "kimi"      = "KIMI_API_KEY"
            "minimax"   = "MINIMAX_API_KEY"
        }
        $envKey = $envVars[$provider]
        if ($envKey) {
            $val = [System.Environment]::GetEnvironmentVariable($envKey)
            if ($val) { Write-Host "  ✅ $envKey is SET (length: $($val.Length))" -ForegroundColor Green }
            else { Write-Host "  ❌ $envKey not set in environment" -ForegroundColor Red }
        } else {
            Write-Host "  ❓ Unknown provider: $provider" -ForegroundColor Yellow
        }
    }

    "list" {
        Write-Host "`n🤖 LLM Providers" -ForegroundColor Cyan
        @("Anthropic", "OpenAI", "GLM-5 (z.ai)", "Kimi K2.5 (Moonshot)", "MiniMax") |
            ForEach-Object { Write-Host "  • $_" -ForegroundColor White }
        Write-Host "`n  Config: llm/config.yaml" -ForegroundColor DarkGray
        Write-Host "  Router: llm/router.yaml" -ForegroundColor DarkGray
    }

    default { Write-Host "Usage: aos llm cost | route <task> | test <provider> | list" }
}
