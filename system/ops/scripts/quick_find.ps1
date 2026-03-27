#!/usr/bin/env pwsh
# quick_find.ps1 â€" AI OS Fast Retrieval CLI
# Version: 1.0 | Created: 2026-03-22
# Owner: registry_capability (registry-manager-agent)
#
# USAGE:
#   .\quick_find.ps1 "security scanning"       â†' find by keyword/capability
#   .\quick_find.ps1 -domain cybersecurity      â†' list all tools in domain
#   .\quick_find.ps1 -agent strix-agent         â†' list agent's skills
#   .\quick_find.ps1 -skill security_shield     â†' show path + info
#   .\quick_find.ps1 -rebuild                   â†' rebuild FAST_INDEX.json

param(
  [Parameter(Position=0)] [string]$Query,
  [string]$Domain,
  [string]$Agent,
  [string]$Skill,
  [switch]$Rebuild,
  [switch]$All
)

$ROOT = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$INDEX_PATH = "$ROOT\brain\shared-context\FAST_INDEX.json"

function Write-Header($text) {
  Write-Host "`nâ"â"â" $text â"â"â"" -ForegroundColor Cyan
}

function Write-Result($label, $value) {
  Write-Host "  " -NoNewline
  Write-Host "[$label]" -ForegroundColor Yellow -NoNewline
  Write-Host " $value"
}

function Load-Index {
  if (-not (Test-Path $INDEX_PATH)) {
    Write-Host "âš ï¸  FAST_INDEX.json not found. Run with -Rebuild first." -ForegroundColor Red
    exit 1
  }
  return Get-Content $INDEX_PATH -Raw | ConvertFrom-Json
}

# === REBUILD ===
if ($Rebuild) {
  Write-Host "ðŸ"„ Rebuilding FAST_INDEX.json..." -ForegroundColor Yellow
  & "$PSScriptRoot\build_fast_index.ps1"
  exit 0
}

$idx = Load-Index
Write-Host "ðŸ" AI OS Fast Retrieval" -ForegroundColor Green
Write-Host "   Index: v$($idx._meta.version) | Skills: $($idx._meta.total_skills) | Plugins: $($idx._meta.total_plugins)"

# === ALL DOMAINS ===
if ($All) {
  Write-Header "All Domains"
  $idx.domain.PSObject.Properties | ForEach-Object {
    Write-Host "  $($_.Name):" -ForegroundColor Cyan
    $_.Value | ForEach-Object { Write-Host "    â†' $_" }
  }
  exit 0
}

# === DOMAIN LOOKUP ===
if ($Domain) {
  Write-Header "Domain: $Domain"
  $skills = $idx.domain.$Domain
  if ($skills) {
    $skills | ForEach-Object {
      $path = $idx.paths.$_
      Write-Result $_ $(if ($path) { $path } else { "(path unknown)" })
    }
  } else {
    Write-Host "  Domain '$Domain' not found. Available:" -ForegroundColor Yellow
    $idx.domain.PSObject.Properties.Name | ForEach-Object { Write-Host "    â€¢ $_" }
  }
  exit 0
}

# === AGENT LOOKUP ===
if ($Agent) {
  Write-Header "Agent Skills: $Agent"
  $skills = $idx.agent.$Agent
  if ($skills) {
    $skills | ForEach-Object {
      $path = $idx.paths.$_
      Write-Result $_ $(if ($path) { $path } else { "brain/skills/$_/SKILL.md" })
    }
  } else {
    Write-Host "  Agent '$Agent' not found." -ForegroundColor Yellow
    Write-Host "  Known agents:" -ForegroundColor Yellow
    $idx.agent.PSObject.Properties.Name | ForEach-Object { Write-Host "    â€¢ $_" }
  }
  exit 0
}

# === SKILL PATH LOOKUP ===
if ($Skill) {
  Write-Header "Skill: $Skill"
  $path = $idx.paths.$Skill
  if ($path) {
    Write-Result "PATH" "$ROOT\$($path -replace '/','\')"
    # Show brief description if SKILL.md exists
    $fullPath = "$ROOT\$($path -replace '/','\')"
    if (Test-Path $fullPath) {
      $content = Get-Content $fullPath -TotalCount 8 -ErrorAction SilentlyContinue
      if ($content) {
        Write-Host "`n  Preview:"
        $content | ForEach-Object { Write-Host "    $_" }
      }
    }
  } else {
    Write-Host "  Skill '$Skill' not found in index." -ForegroundColor Yellow
  }
  # Show which domains and agents use this skill
  Write-Host "`n  Used in domains:" -ForegroundColor Yellow
  $idx.domain.PSObject.Properties | Where-Object { $Skill -in $_.Value } | ForEach-Object {
    Write-Host "    â€¢ $($_.Name)"
  }
  Write-Host "`n  Used by agents:" -ForegroundColor Yellow
  $idx.agent.PSObject.Properties | Where-Object { $Skill -in $_.Value } | ForEach-Object {
    Write-Host "    â€¢ $($_.Name)"
  }
  exit 0
}

# === KEYWORD/CAPABILITY QUERY ===
if ($Query) {
  Write-Header "Query: '$Query'"
  $queryLower = $Query.ToLower()
  $found = @{}

  # 1. Exact keyword match
  $idx.keyword.PSObject.Properties | ForEach-Object {
    if ($queryLower -like "*$($_.Name)*" -or $_.Name -like "*$queryLower*") {
      $found[$_.Value] = "keyword:$($_.Name)"
    }
  }

  # 2. Domain match
  $idx.domain.PSObject.Properties | ForEach-Object {
    if ($_.Name -like "*$queryLower*") {
      $_.Value | ForEach-Object { $found[$_] = "domain:$($_.Name)" -as [string] }
    }
  }

  # 3. Skill path match
  $idx.paths.PSObject.Properties | ForEach-Object {
    if ($_.Name -like "*$queryLower*") {
      $found[$_.Name] = "name match"
    }
  }

  if ($found.Count -gt 0) {
    Write-Host "  Found $($found.Count) matches:" -ForegroundColor Green
    $found.GetEnumerator() | ForEach-Object {
      $path = $idx.paths."$($_.Key)"
      $displayPath = if ($path) { $path } else { "brain/skills/$($_.Key)/" }
      Write-Result $_.Key "â† $($_.Value) | $displayPath"
    }
  } else {
    Write-Host "  No direct matches for '$Query'." -ForegroundColor Yellow
    Write-Host "  Try: .\quick_find.ps1 -All   (list all domains)" -ForegroundColor Gray
    Write-Host "  Or:  .\quick_find.ps1 -Domain <domain>" -ForegroundColor Gray
  }

  # Always show protocol hint
  Write-Host "`n  ðŸ'¡ Retrieval Protocol: brain/knowledge/RETRIEVAL_PROTOCOL.md" -ForegroundColor DarkGray
  exit 0
}

# Default: show help
Write-Host "`nUSAGE:" -ForegroundColor Yellow
Write-Host "  .\quick_find.ps1 'security scanning'     â†' keyword/capability search"
Write-Host "  .\quick_find.ps1 -Domain cybersecurity   â†' domain tool list"
Write-Host "  .\quick_find.ps1 -Agent strix-agent      â†' agent skill list"
Write-Host "  .\quick_find.ps1 -Skill security_shield  â†' skill path + info"
Write-Host "  .\quick_find.ps1 -All                    â†' all domains"
Write-Host "  .\quick_find.ps1 -Rebuild                â†' refresh index"
Write-Host "`nAvailable domains:" -ForegroundColor Cyan
$idx.domain.PSObject.Properties.Name | ForEach-Object { Write-Host "  â€¢ $_" }

