# Project Connection Protocol â€” AI OS v3.0
# Authority: Tier 0 (Constitution)
# Updated: 2026-03-16

> **Purpose:** Defines the standard protocol for any external project to connect to and leverage AI OS capabilities (skills, channels, knowledge, agents).

---

## Core Concept

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚              EXTERNAL PROJECT               â”‚
â”‚  (React app, GAS backend, CLI tool, etc.)   â”‚
â”‚                                             â”‚
â”‚  [.agent/CLAUDE.md]  â† reads AI OS skills  â”‚
â”‚  [.clauderules]      â† workspace rules      â”‚
â”‚  [.claudeignore]     â† scope limits         â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                 â”‚ registers via
                 â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚              AI OS CORE                     â”‚
â”‚  registry.json  â† project catalog          â”‚
â”‚  skills/        â† shared capabilities      â”‚
â”‚  knowledge/     â† shared intelligence      â”‚
â”‚  channels/      â† remote bridge (optional) â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## Connection Steps (for a new project)

### Step 1: Register in `registry.json`

Add entry to `<AI_OS_ROOT>\registry.json`:

```json
"PRJ-XXX": {
  "name": "Project Display Name",
  "path": "D:\\path\\to\\project",
  "description": "One-line description",
  "status": "active",
  "skills_used": ["skill-name-1", "skill-name-2"],
  "channels_enabled": false,
  "data_sources": ["google-sheets", "local-sqlite"],
  "contact_agent": "claude_code",
  "config_path": "<AI_OS_ROOT>\\projects\\PRJ-XXX\\CLAUDE.md",
  "workflows_path": "<AI_OS_ROOT>\\projects\\PRJ-XXX\\workflows\\"
}
```

Use `scripts/register_project.ps1 -Id PRJ-XXX -Name "..." -Path "..."` to automate.

---

### Step 2: Create Project Config in `projects/PRJ-XXX/`

```
projects/PRJ-XXX/
â”œâ”€â”€ CLAUDE.md          â† Project-scoped identity (load AI OS skills)
â””â”€â”€ workflows/         â† Project-specific workflows
    â”œâ”€â”€ deploy.md
    â””â”€â”€ debug.md
```

The `CLAUDE.md` must start with:
```markdown
# Project: [Name] â€” AI OS Connected
# PRJ-ID: PRJ-XXX
# reads-from: <AI_OS_ROOT>\CLAUDE.md

## Skills Loaded
- [ui-ux-pro-max](../../skills/domains/frontend/ui-ux-pro-max/SKILL.md)
- [pos-event-sourcing](../../skills/domains/pos/pos-event-sourcing/SKILL.md)
```

---

### Step 3: Configure Project Workspace

In the project directory, create `.clauderules` (or `.agent/CLAUDE.md`):

```markdown
# Workspace Rules â€” [Project Name]
# Connected to AI OS: <AI_OS_ROOT>

## Identity
This workspace is a satellite project of AI OS.
When coding here, Antigravity has full authority per AI OS hierarchy.

## Skills Available
See: <AI_OS_ROOT>\shared-context\SKILL_REGISTRY.json

## Handoff
For complex tasks: follow <AI_OS_ROOT>\workflows\claude_code_handoff.md
```

---

### Step 4: Run Gatekeeper (first access)

```powershell
# From AI OS root
.\gatekeeper.ps1 -ProjectId PRJ-XXX
```

If GRANT â†’ project is active in AI OS ecosystem.

---

## Project Status Lifecycle

```
DRAFT â†’ ACTIVE â†’ MAINTENANCE â†’ ARCHIVED
```

| Status | Meaning |
|--------|---------|
| `draft` | Being set up, not yet registered |
| `active` | Fully connected, regular work happening |
| `maintenance` | Minimal activity, skills still loaded |
| `archived` | No longer active, knowledge preserved |

---

## What AI OS Provides to Connected Projects

| Resource | Location | How to Use |
|----------|----------|------------|
| Skills | `skills/` + `skills/domains/` | Reference in project CLAUDE.md |
| Knowledge | `knowledge/` | Read via knowledge_navigator skill |
| Channel Bridge | `channels/` | Set `channels_enabled: true` in registry |
| Shared Agents | `agents/` | Invoke via blackboard.json |
| Orchestrator | `blackboard.json` | Write task payload â†’ AI OS picks up |

---

## Quick Reference: Auto-Register Script

```powershell
# Táº¡o project má»›i vÃ  register tá»± Ä‘á»™ng:
.\scripts\register_project.ps1 `
  -Id "PRJ-005" `
  -Name "My New Project" `
  -Path "D:\MyProject" `
  -Description "Brief description" `
  -Skills @("ui-ux-pro-max") `
  -Channels $false
```

---

*"Every project is a satellite. AI OS is the operating system they orbit."*

