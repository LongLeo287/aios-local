# SKILL_LOADING_PROTOCOL.md — Agent Skill Discovery & Loading Standard
# Version: 1.1 | Updated: 2026-03-14
# Authority: Tier 2 (Operations) — Part of AI OS Layer 4

## Purpose

This document answers: **"How does an agent know which skills exist, which ones to load, and how to call them?"**

Without this protocol, agents either hardcode skill IDs (fragile) or load everything (wasteful). The Skill Loading Protocol enables **lazy, demand-driven, dependency-aware** skill loading.

---

## The Discovery Stack

```
┌─────────────────────────────────────────────────────────────┐
│  AGENT needs a capability                                   │
│     │                                                       │
│     ▼                                                       │
│  1. Check loaded skills (in-session cache)                  │
│     │  HIT → use directly                                   │
│     │  MISS ↓                                               │
│  2. Query SKILL_REGISTRY.json                               │
│     │  NOT FOUND → run skill_loader.ps1 to refresh         │
│     │  FOUND ↓                                              │
│  3. Read SKILL.md from skill's path                         │
│     │  Parse exposed_functions + dependencies               │
│     │                                                       │
│  4. Load dependencies first (recursive, breadth-first)      │
│     │                                                       │
│  5. Execute the target skill function                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Protocol

### Step 1 — Need Identification

Before loading any skill, the agent must identify:

```xml
<thought>
  Task: [what I need to accomplish]
  Capability needed: [e.g., "extract facts from a document"]
  Candidate skills: [search SKILL_REGISTRY for matching tags or function names]
  Selection: [chosen skill_id and why]
</thought>
```

### Step 2 — Registry Lookup

```powershell
# Read the registry (always fresh — no caching between sessions)
$registry = Get-Content "d:\Project\AI OS\shared-context\SKILL_REGISTRY.json" | ConvertFrom-Json

# Search by tag
$candidates = $registry.entries | Where-Object { $_.tags -contains "memory" }

# Search by function name
$candidates = $registry.entries | Where-Object { $_.exposed_functions -contains "extract_facts" }

# Search by ID (direct lookup)
$skill = $registry.entries | Where-Object { $_.id -eq "smart_memory" }
```

If skill not found: **run `scripts/skill_loader.ps1` first**, then retry.

### Step 3 — Access Check

Before loading, verify the agent is authorized:

```powershell
$myRole = "Orchestrator"   # Your agent role
$authorized = $skill.accessible_by -contains $myRole -or 
              $skill.accessible_by -contains "All agents"

if (-not $authorized) {
    Write-Host "[BLOCKED] Skill '$($skill.id)' is not accessible by role '$myRole'"
    # Escalate to Antigravity if the skill is needed
}
```

### Step 4 — Dependency Resolution

Load dependencies **before** the target skill, in order:

```powershell
function Load-SkillWithDeps {
    param([string]$SkillId, [string[]]$AlreadyLoaded = @())

    if ($SkillId -in $AlreadyLoaded) { return }  # Prevent circular deps

    $skill = $registry.entries | Where-Object { $_.id -eq $SkillId }
    if (-not $skill) { throw "Skill '$SkillId' not found in registry" }

    # Load dependencies first (recursive)
    foreach ($dep in $skill.dependencies) {
        Load-SkillWithDeps -SkillId $dep -AlreadyLoaded $AlreadyLoaded
    }

    # Now load this skill
    $skillContent = Get-Content $skill.path -Raw
    Write-Host "  [LOADED] $SkillId (Tier $($skill.tier))"
    $AlreadyLoaded += $SkillId

    return $skillContent
}

# Usage:
Load-SkillWithDeps -SkillId "smart_memory"
# Auto-loads: context_manager → smart_memory (in correct order)
```

### Step 5 — Function Invocation

Each skill's `SKILL.md` describes how to invoke its `exposed_functions`. Agents call them by following the instructions in the skill's SKILL.md body:

```xml
<thought>
  Skill: smart_memory
  Function: extract_facts
  Input: [document text]
  Expected output: [bullet list of atomic facts]
  Calling convention: [as described in SKILL.md]
</thought>
```

---

## Tier Loading Strategy

| Tier | Strategy | When |
|------|----------|------|
| **Tier 1** (Core) | **Eager** — load at session start | Always: `context_manager`, `reasoning_engine`, `resilience_engine` |
| **Tier 2** (Enhanced) | **Lazy** — load on first use | When a task requires the capability |
| **Tier 3** (Domain / Plugins) | **Manual** — explicit load only | Only when explicitly needed for the task |

### Tier 1 Boot Sequence (Every Session)

At the start of every session, agents MUST load Tier 1 skills first:

```
Boot order:
  1. context_manager      → Must be first (token budget awareness)
  2. reasoning_engine     → Depends on context_manager
  3. resilience_engine    → No deps, activates circuit breaker
  4. antigravity          → Orchestrator identity (Tier 1, Antigravity sessions only)
```

---

## Domain Skill Loading (Tier 3)

Domain skills live in `skills/domains/<domain>/` as **flat `.md` files** (not SKILL.md inside subfolders).
They are **never auto-loaded** (no eager/lazy). Load only when the project needs it.

### Available Domains & Files

| Domain | Files | Use Case |
|--------|-------|----------|
| `google-workspace` | `gas-skill.md`, `sheets-skill.md`, `sheets-performance-optimization.md` | Google Apps Script, Sheets integration |
| `databases` | `supabase-postgres-best-practices.md` | Supabase / PostgreSQL projects |
| `finance` | `cost-manager-skill.md`, `edge-compute-patterns.md` | AI cost routing, tax edge compute |
| `frontend` | `hitl-gateway-enforcer.md`, `fsd-architectural-linter.md` | Human approval gates, FSD enforcement |
| `pos` | `pos-event-sourcing-auditor.md` | Point-of-sale event sourcing |

### How to Load a Domain Skill

```powershell
# 1. Look up the path in registry
$entry = $registry.entries | Where-Object { $_.id -like "*gas*" }
Write-Host "Path: $($entry.path)"

# 2. Read the skill file directly
$domainSkill = Get-Content $entry.path -Raw
# 3. Follow the instructions in the skill body
```

### Cost Tier Routing (Which LLM to Use)

When a domain skill specifies a `cost_tier`, use it to select the appropriate model:

| cost_tier | Recommended Use | Examples |
|-----------|----------------|----------|
| `economy` | Simple transforms, lookups, formatting | `sheets-skill.md` queries |
| `standard` | Code generation, QA, moderate reasoning | Most domain skills |
| `premium` | Critical decisions, architecture design | `pos-event-sourcing-auditor.md` production decisions |

> **Rule:** Never use a `premium`-tier model for `economy` tasks. Check `cost_tier` field before routing.


## Cross-Skill Output Sharing

When Skill A produces output that Skill B needs:

### Channel A — Blackboard (synchronous, structured)

```json
// Write to shared-context/blackboard.json under skill_outputs:
{
  "skill_outputs": {
    "smart_memory": {
      "result": ["fact 1", "fact 2"],
      "timestamp": "2026-03-14T13:26:00+07:00"
    }
  }
}
```

### Channel B — Message Queue (asynchronous, event-driven)

```
File: subagents/mq/<event_name>_<timestamp>.json
Format: { "event": "facts_extracted", "from": "smart_memory", "payload": [...] }
```

Consuming skill reads from MQ:
```powershell
$events = Get-ChildItem "d:\Project\AI OS\subagents\mq\" -Filter "facts_extracted_*.json"
$latest = $events | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$data   = Get-Content $latest.FullName | ConvertFrom-Json
```

---

## Refreshing the Registry

Registry can become stale when new skills are added. Agents MUST refresh when:

1. A skill lookup fails (ID not in registry)
2. At the start of a session (check `meta.updated` date)
3. Explicitly when running the handoff workflow

```powershell
# Quick refresh (auto-run, no confirmation needed):
& "d:\Project\AI OS\scripts\skill_loader.ps1"
```

After refresh, re-query the registry — new skills will appear.

---

## Skill Status Rules

| Status | Meaning | Agent Action |
|--------|---------|-------------|
| `active` | Fully operational | Load and use normally |
| `beta` | Unstable/experimental | Load with caution, wrap in `<thought>` dry-run |
| `deprecated` | Being phased out | Prefer alternative; do NOT use for new tasks |
| `error` | Failed registry validation | Do NOT load; report to Antigravity |
| `planned` | Not yet implemented | Cannot load; find alternative |

---

## Plugin vs Skill Loading

| Aspect | Skill | Plugin |
|--------|-------|--------|
| Source | `skills/` or `agents/` | `plugins/` |
| Load trigger | Role-based, on-demand | Hook-based or manual |
| Read file | `SKILL.md` | `manifest.json` |
| Output sharing | Blackboard or MQ | Hook return value |
| Failure | Fallback to base behavior | **Silent fail** — OS continues |

---

## Anti-Patterns (Never Do)

```
❌ Hardcoding skill paths — always query SKILL_REGISTRY.json
❌ Loading all skills at startup — only Tier 1 is eager
❌ Loading a skill without checking accessible_by
❌ Calling a skill function without reading its SKILL.md first
❌ Ignoring dependencies — always resolve the full dep chain
❌ Loading a plugin as a skill or vice versa
```

---

*"Self-discovery is not a luxury — it is the foundation of a scalable multi-agent system."*
