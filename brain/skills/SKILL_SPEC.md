# SKILL_SPEC.md â€” AI OS Skill Schema Standard
# Version: 1.1 | Updated: 2026-03-14

## Purpose

This document defines the **mandatory schema** for every OS-level skill in `AI_OS_ROOT\skills\`.
All skills MUST conform to this spec. Non-conforming skills will be rejected by the Skill Loader.

---

## Required Directory Structure

```
skills/
â””â”€â”€ <skill_id>/
    â”œâ”€â”€ SKILL.md          [REQUIRED] â€” Manifest & instructions
    â”œâ”€â”€ README.md         [REQUIRED] â€” Human-readable usage guide
    â”œâ”€â”€ schema.json       [REQUIRED] â€” Machine-readable metadata
    â””â”€â”€ tests/            [OPTIONAL] â€” Validation scripts
        â””â”€â”€ test_<skill_id>.ps1
```

---

## SKILL.md â€” Manifest Format

Every `SKILL.md` MUST begin with the following YAML frontmatter block:

```yaml
---
id: <skill_id>                     # Unique snake_case identifier
name: <Human Readable Name>
version: <SemVer e.g. 1.0.0>
tier: <1|2|3>                      # 1=Core, 2=Enhanced, 3=Domain/Manual
status: <active|deprecated|beta>
author: AI OS Core Team
updated: <YYYY-MM-DD>

# DOMAIN (new in v1.1)
domain: core | google-workspace | databases | finance | frontend | pos | <custom>
# domain=core â†’ lives in skills/core/
# domain=<other> â†’ lives in skills/domains/<domain>/
# load_on_boot: false for ALL domain skills (never auto-loaded)

# COST TIER (new in v1.1)
cost_tier: economy | standard | premium
# economy = cheap inference tasks (lookups, formatting)
# standard = reasoning, code generation
# premium = critical decisions, complex architecture

# LOAD BEHAVIOR
load_on_boot: <true|false>        # true = Tier 1 eager, false = all others

# WHO CAN USE THIS SKILL
accessible_by:
  - Orchestrator
  - Claude Code
  - <other agent roles>

# WHAT THIS SKILL NEEDS TO LOAD FIRST
dependencies:
  - <skill_id_1>
  - <skill_id_2>

# WHAT THIS SKILL PROVIDES
exposed_functions:
  - name: <function_name>
    description: <what it does>
    input: <input type/format>
    output: <output type/format>

# WHAT READS/CONSUMES THIS SKILL
consumed_by:
  - <skill_id or agent_role>

# WHAT EVENTS THIS SKILL EMITS (for MQ)
emits_events:
  - <event_name>

# WHAT EVENTS THIS SKILL LISTENS TO
listens_to:
  - <event_name>

# TAGS (for filtering and discovery)
tags: [<category_tag>, <domain_tag>]
---
```

Followed by the full instruction body in English.

---

## schema.json â€” Machine-Readable Metadata

```json
{
  "id": "<skill_id>",
  "name": "<Human Readable Name>",
  "version": "<SemVer>",
  "tier": 1,
  "status": "active",
  "path": "AI_OS_ROOT\\skills\\<skill_id>\\SKILL.md",
  "accessible_by": ["Orchestrator", "Claude Code"],
  "dependencies": [],
  "exposed_functions": [
    {
      "name": "<fn_name>",
      "description": "<what it does>",
      "input": "<type>",
      "output": "<type>"
    }
  ],
  "consumed_by": [],
  "emits_events": [],
  "listens_to": [],
  "tags": ["<category_tag>"]
}
```

---

## Skill Tier Definitions

| Tier | Name | Description | Load Strategy |
|------|------|-------------|---------------|
| **1** | Core | Always-available foundational skills | Eager-load on boot |
| **2** | Enhanced | Domain-specific, loaded when role requires | Lazy-load on demand |
| **3** | Domain/Manual | Project-specific, external, or experimental | Manual-load only |

**Domain skill location:**
- `domain: core` â†’ `skills/[skill_id]/SKILL.md`
- `domain: google-workspace` â†’ `skills/domains/google-workspace/<skill>.md`
- `domain: databases` â†’ `skills/domains/databases/<skill>.md`
- `domain: finance` â†’ `skills/domains/finance/<skill>.md`
- `domain: frontend` â†’ `skills/domains/frontend/<skill>.md`
- `domain: pos` â†’ `skills/domains/pos/<skill>.md`
- Proposals â†’ `skills/experimental/PROPOSAL_<name>_<date>.md`

**Cost tier guide:**
- `economy` = simple lookups, formatting, data transforms
- `standard` = code generation, QA reviews, research
- `premium` = architecture decisions, critical path planning

---

## Skill Categories (Tags)

| Tag | Skills |
|-----|--------|
| `memory` | `smart_memory`, `cosmic_memory`, `neural_memory` |
| `reasoning` | `reasoning_engine`, `insight_engine`, `cognitive_evolver` |
| `execution` | `shell_assistant`, `web_intelligence`, `performance_profiler` |
| `quality` | `production_qa`, `diagnostics_engine`, `security_shield` |
| `data` | `knowledge_enricher`, `context_manager` |
| `ui` | `visual_excellence`, `accessibility_grounding` |
| `ops` | `resilience_engine`, `notification_bridge` |
| `agent` | `archivist`, `orchestrator_pro`, `antigravity` |
| `google-workspace` | `gas_skill`, `sheets_skill`, `sheets_performance_optimization` |
| `databases` | `supabase_postgres_best_practices` |
| `finance` | `cost_manager_skill`, `edge_compute_patterns` |
| `frontend` | `hitl_gateway_enforcer`, `fsd_architectural_linter` |
| `pos` | `pos_event_sourcing_auditor` |

---

## Cross-Skill Communication Protocol

Skills communicate through two channels:

### 1. Shared Context (synchronous)
Read/write to `shared-context/blackboard.json` for task coordination:
```json
{
  "skill_outputs": {
    "<skill_id>": {
      "result": "<value>",
      "timestamp": "<ISO 8601>"
    }
  }
}
```

### 2. Message Queue (asynchronous)
Post events to `subagents/mq/` for decoupled skill-to-skill messaging:
- Event format: `{ "event": "<name>", "from": "<skill_id>", "payload": {} }`
- Skills declare `emits_events` and `listens_to` in their frontmatter

---

## Validation Rules

The Skill Loader script (`scripts/skill_loader.ps1`) enforces:

1. `SKILL.md` MUST exist and contain valid YAML frontmatter
2. `schema.json` MUST exist and be valid JSON
3. `README.md` MUST exist (can be minimal)
4. `id` in frontmatter MUST match directory name
5. `tier` MUST be 1, 2, or 3
6. `status` MUST be `active`, `deprecated`, or `beta`
7. All `dependencies` MUST resolve to existing skill IDs
8. `accessible_by` MUST reference valid agent roles

Skills failing validation are marked `"status": "error"` in `SKILL_REGISTRY.json`.

---

## Example: Minimal Compliant Skill

```
skills/
â””â”€â”€ example_skill/
    â”œâ”€â”€ SKILL.md       # With YAML frontmatter
    â”œâ”€â”€ README.md      # Usage instructions
    â””â”€â”€ schema.json    # Machine metadata
```

`skills/example_skill/SKILL.md`:
```yaml
---
id: example_skill
name: Example Skill
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
accessible_by:
  - Orchestrator
  - Claude Code
dependencies:
  - context_manager
exposed_functions:
  - name: run_example
    description: Runs the example operation
    input: string (task description)
    output: string (result summary)
consumed_by: []
emits_events: []
listens_to: []
---

# Example Skill

[Full instruction body here]
```

---

*"A skill without a spec is a tool no one can trust."*

