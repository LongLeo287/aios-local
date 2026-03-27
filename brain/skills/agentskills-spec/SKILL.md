---
name: AgentSkills Specification
description: Official Anthropic agentskills.io specification ingested into AI OS. Defines the standard interface, lifecycle, and metadata format for agent skills. Used by Skill Creator Ultra and all skill-aware agents.
department: registry_capability
tier: 1
category: specification
status: active
tags: [spec, agentskills, anthropic, standard, skill-lifecycle]
---

# AgentSkills Specification

**Repo:** `brain/skills/agentskills-spec`
**Type:** Specification / reference document
**Source:** `https://github.com/agentskills/agentskills` (Anthropic)
**Delivered by:** `ingest-router-agent` (CIV-2026-03-17-001)
**Department:** Registry & Capability
**Tier:** 1 — foundational specification

## What it is

The authoritative **agentskills.io specification** from Anthropic, copied into AI OS brain. Defines:

- Standard skill YAML/Markdown metadata schema
- Skill lifecycle states: `draft → active → deprecated`
- Tool interface contracts for skill invocation
- Agent capability declaration format
- Tier classification system (1–5)

## Contents

| File | Purpose |
|------|---------|
| `CIV-DELIVERY.md` | Delivery receipt from ingest-router-agent |

## Usage by AI OS

All SKILL.md files in AI OS follow this spec:
```yaml
---
name: <skill name>
description: <1-line description>
department: <dept_id>
tier: 1-5
category: <category>
status: active|deprecated|draft
tags: [...]
---
```

## AI OS Integration
- **Owner:** `registry_capability` department
- **Read by:** Skill Creator Ultra, SKILL_REGISTRY.json builder, ClawTask Skills panel
- **Purpose:** Ensures all 44+ AI OS skills conform to the same schema
- **Used in:** `/api/aios/skills` endpoint for validation
