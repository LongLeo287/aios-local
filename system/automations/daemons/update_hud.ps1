<#
.SYNOPSIS
    AI OS HUD Auto-Update — Tier 3 (2-way HUD engine)
.DESCRIPTION
    Tự động cập nhật hud/HUD.md + hud/STATUS.json sau mỗi cycle/session.
    Đọc từ: ports, blackboard.json, proposals/, escalations.md, SKILL_REGISTRY.json
    Ghi vào: hud/STATUS.json + cập nhật status blocks trong HUD.md
    Tạo snapshot: hud/snapshots/<date>_<time>.md

    Trigger:
    - Phase 7 của corp-daily-cycle.md (cuối mỗi cycle)
    - post-session.md (cuối mỗi session)
    - Manual: powershell ops/scripts/update_hud.ps1

.NOTES
    DO NOT MODIFY hud/HUD.md links section — chỉ update dynamic sections
    v1.0 | 2026-03-24 | Owner: system_health
#>

param(
    [string]$AOS_ROOT = $(if ($env:AOS_ROOT) { $env:AOS_ROOT } else { (Get-Item "$PSScriptRoot\..\..\..").FullName }),
    [switch]$SnapshotOnly,
    [switch]$Quiet
)

Set-StrictMode -Off
$ErrorActionPreference = "SilentlyContinue"

function Write-HUD($msg) {
    if (-not $Quiet) { Write-Host $msg }
}

Write-HUD "=== AI OS HUD UPDATE === $(Get-Date -Format 'HH:mm:ss')"

# ─── 1. CHECK SERVICES (port scan) ───────────────────────────────────────────
$services = @(
    @{ name="Ollama (local LLM)";       port=11434; start_cmd="ollama serve" }
    @{ name="ClawTask API";             port=7474;  start_cmd="auto" }
    @{ name="LightRAG (RAG)";           port=9621;  start_cmd="python ops/scripts/lightrag_server.py" }
    @{ name="open-notebook";            port=5055;  start_cmd="Claude Code RESEARCHER" }
    @{ name="Langfuse (observability)"; port=3100;  start_cmd="docker compose up -d" }
)

$svcResults = @()
foreach ($svc in $services) {
    $alive = $null -ne (Get-NetTCPConnection -LocalPort $svc.port -State Listen -ErrorAction SilentlyContinue)
    $emoji = if ($alive) { "LIVE" } else { "DOWN" }
    if ($svc.port -eq 5055 -and -not $alive) { $emoji = "FALLBACK" }
    $svcResults += @{ name=$svc.name; port=$svc.port; status=$emoji; start_cmd=$svc.start_cmd }
    Write-HUD "  :$($svc.port) $($svc.name): $emoji"
}

# ─── 2. READ BLACKBOARD ──────────────────────────────────────────────────────
$bbPath = "$AOS_ROOT\brain\shared-context\blackboard.json"
$openItems = 0
$cycleNum = "?"
$cycleStatus = "UNKNOWN"
$lastUpdate = ""

if (Test-Path $bbPath) {
    try {
        $bb = Get-Content $bbPath -Raw | ConvertFrom-Json
        $openItems = if ($bb.open_items) { @($bb.open_items | Where-Object { $_.status -ne "CLOSED" }).Count } else { 0 }
        $cycleNum = if ($bb.corp_cycle_number) { $bb.corp_cycle_number } else { "?" }
        $cycleStatus = if ($bb.corp_cycle_status) { $bb.corp_cycle_status } else { "UNKNOWN" }
    } catch { Write-HUD "  [WARN] blackboard.json parse error" }
}

# ─── 3. COUNT PROPOSALS ──────────────────────────────────────────────────────
$proposalPath = "$AOS_ROOT\brain\shared-context\corp\proposals"
$pendingProposals = 0
if (Test-Path $proposalPath) {
    $pendingProposals = (Get-ChildItem $proposalPath -Filter "PROP_*.md" -ErrorAction SilentlyContinue | Measure-Object).Count
}

# ─── 4. COUNT SKILLS ─────────────────────────────────────────────────────────
$skillsCount = (Get-ChildItem "$AOS_ROOT\skills" -Directory -ErrorAction SilentlyContinue | Measure-Object).Count

# ─── 5. COUNT GAPS ───────────────────────────────────────────────────────────
$gapsCount = (Get-ChildItem "$AOS_ROOT\corp\gaps" -Filter "GAP-*.md" -ErrorAction SilentlyContinue | Measure-Object).Count

# ─── 6. LAST RETRO ───────────────────────────────────────────────────────────
$retros = Get-ChildItem "$AOS_ROOT\corp\memory\global" -Filter "RETRO_*.md" -ErrorAction SilentlyContinue | Sort-Object Name -Descending
$lastRetro = if ($retros) { $retros[0].Name -replace "RETRO_","" -replace ".md","" } else { "never" }

# ─── 7. WRITE STATUS.json ────────────────────────────────────────────────────
$ts = Get-Date -Format "yyyy-MM-ddTHH:mm:ss+07:00"
$statusObj = [ordered]@{
    updated              = $ts
    system               = "AI OS Corp"
    version              = "v2.1"
    cycle                = $cycleNum
    corp_cycle_status    = $cycleStatus
    last_retro           = $lastRetro
    open_items           = $openItems
    pending_proposals    = $pendingProposals
    skills_count         = $skillsCount
    gaps_count           = $gapsCount
    departments          = 21
    agents               = 52
    services             = @{}
}

foreach ($svc in $svcResults) {
    $statusObj.services[$svc.name] = @{ port=$svc.port; status=$svc.status }
}

$statusObj | ConvertTo-Json -Depth 5 | 
    Set-Content "$AOS_ROOT\hud\STATUS.json" -Encoding UTF8
Write-HUD "  [OK] STATUS.json updated"

# ─── 8. UPDATE HUD.md — SERVICES TABLE ──────────────────────────────────────
if (-not $SnapshotOnly) {
    $hudPath = "$AOS_ROOT\hud\HUD.md"
    $hudContent = [System.IO.File]::ReadAllText($hudPath, [System.Text.Encoding]::UTF8)

    # Build new services table
    $svcHeader = "| Service | Port | Status | Action |`n|---------|------|--------|--------|"
    $svcRows = @($svcHeader)
    foreach ($svc in $svcResults) {
        $emoji = switch ($svc.status) {
            "LIVE"     { ":green_circle: LIVE" }
            "FALLBACK" { ":yellow_circle: FALLBACK" }
            default    { ":red_circle: DOWN" }
        }
        # Use actual emoji chars
        $emojiChar = switch ($svc.status) {
            "LIVE"     { "LIVE" }
            "FALLBACK" { "FALLBACK" }
            default    { "DOWN" }
        }
        $actionCol = if ($svc.status -eq "LIVE") { "—" } else { "``$($svc.start_cmd)``" }
        $svcRows += "| $($svc.name) | $($svc.port) | $emojiChar | $actionCol |"
    }
    $svcRows += "| Telegram Bot | — | CONFIGURED | @aios_corp_bot |"

    # Replace SERVICES block (between ## SERVICES STATUS and next ---)
    $newSvcBlock = ($svcRows -join "`n")
    $hudContent = $hudContent -replace "(?s)(## SERVICES STATUS\n\n)\|[^`"]+?(\n\n---)", "`$1$newSvcBlock`$2"

    # Update Corp Status cycle number
    $hudContent = $hudContent -replace "(\| Cycle \| )[\d]+ — [\w]+", "`${1}$cycleNum — $cycleStatus"
    $hudContent = $hudContent -replace "(\| Last Retro \| )[\d\-]+", "`${1}$lastRetro"
    $hudContent = $hudContent -replace "(\| Skills \| )[\d]+", "`${1}$skillsCount installed"
    $hudContent = $hudContent -replace "(\| Open Items \| )[\d]+", "`${1}$openItems"

    [System.IO.File]::WriteAllText($hudPath, $hudContent, [System.Text.Encoding]::UTF8)
    Write-HUD "  [OK] HUD.md corp status + services updated"
}

# ─── 9. CREATE SNAPSHOT ──────────────────────────────────────────────────────
$snapshotDir = "$AOS_ROOT\hud\snapshots"
New-Item -ItemType Directory -Force -Path $snapshotDir | Out-Null

$snapshotFile = "$snapshotDir\$(Get-Date -Format 'yyyy-MM-dd_HHmm').md"
$snapshotContent = @"
# HUD Snapshot — $(Get-Date -Format 'yyyy-MM-dd HH:mm')
| Field | Value |
|-------|-------|
| Cycle | $cycleNum — $cycleStatus |
| Last Retro | $lastRetro |
| Open Items | $openItems |
| Pending Props | $pendingProposals |
| Skills | $skillsCount |
| Gaps | $gapsCount |

## Services
$(($svcResults | ForEach-Object { "| $($_.name) | :$($_.port) | $($_.status) |" }) -join "`n")
"@

$snapshotContent | Set-Content $snapshotFile -Encoding UTF8
Write-HUD "  [OK] Snapshot: hud/snapshots/$(Split-Path $snapshotFile -Leaf)"

# ─── 10. NOTIFY (optional Telegram) ─────────────────────────────────────────
$envFile = "$AOS_ROOT\.env"
if (Test-Path $envFile) {
    $envLines = [System.IO.File]::ReadAllLines($envFile, [System.Text.Encoding]::UTF8)
    $TOKEN   = ($envLines | Where-Object { $_ -match "^TELEGRAM_BOT_TOKEN=" }) -replace "^TELEGRAM_BOT_TOKEN=",""
    $CHAT_ID = ($envLines | Where-Object { $_ -match "^TELEGRAM_CHAT_ID=" })   -replace "^TELEGRAM_CHAT_ID=",""

    if ($TOKEN -and $CHAT_ID -and -not $Quiet) {
        $downSvcs = ($svcResults | Where-Object { $_.status -eq "DOWN" } | ForEach-Object { ":$($_.port)" }) -join ", "
        $msg = "=AI OS HUD= Cycle $cycleNum | $cycleStatus`nServices DOWN: $(if($downSvcs){$downSvcs}else{'none'})`nOpen: $openItems items | Props: $pendingProposals | Skills: $skillsCount"
        $body = @{ chat_id=$CHAT_ID; text=$msg } | ConvertTo-Json -Compress
        try {
            Invoke-RestMethod "https://api.telegram.org/bot$TOKEN/sendMessage" `
                -Method POST -Body $body -ContentType "application/json" -TimeoutSec 5
            Write-HUD "  [OK] Telegram notified"
        } catch { Write-HUD "  [WARN] Telegram notify failed" }
    }
}

Write-HUD "`n=== HUD UPDATE COMPLETE === Cycle:$cycleNum | Open:$openItems | Props:$pendingProposals | Skills:$skillsCount"
