# CONTRIBUTING.md — How to Add Repos, Skills & Agents to AI OS
# Version: 1.0 | Created: 2026-03-16

---

## 🎯 Overview

This guide explains how to extend AI OS with new repositories, skills, and agents.
Following these steps ensures security, discoverability, and proper governance.

---

## 📦 Adding a New Repository

### Option A: Clone into plugins/ (agent-executable)
Use when: it has SKILL.md, manifest.json, or can be called by agents
```powershell
# 1. Security check (MANDATORY)
# → Run: agents/security_agent → scan_repo("<url>")
# → Minimum score: 60

# 2. Clone
git clone --depth=1 <url> "D:\LongLeo\Project\AI OS\plugins\<name>"

# 3. Create manifest
# → plugins/<name>/manifest.json (see PLUGIN_SPEC.md)

# 4. Register in SKILL_REGISTRY.json
# → shared-context/SKILL_REGISTRY.json → add entry with source="plugin"

# 5. Update knowledge index
# → knowledge/knowledge_index.md → add one-line reference
```

### Option B: Clone into knowledge/repos/ (reference only)
Use when: it's a learning resource, not directly callable
```powershell
git clone --depth=1 <url> "D:\LongLeo\Project\AI OS\knowledge\repos\<name>"
# Register with source="knowledge_ref" in SKILL_REGISTRY.json
```

### Option C: Clone into REMOTE/claws/ (Claw variants)
Use when: it's a Claude/AI runtime variant
```powershell
git clone --depth=1 <url> "D:\LongLeo\Project\AI OS\REMOTE\claws\<name>"
# Register with category="claw_variant" in SKILL_REGISTRY.json
```

### Option D: Web Analysis (can't clone — private/deleted)
```
1. Fetch: https://raw.githubusercontent.com/<owner>/<repo>/main/README.md
2. Create: knowledge/<name>_analysis.md
3. Register: SKILL_REGISTRY.json with source="knowledge_web"
4. Reference: knowledge/knowledge_index.md
```

---

## 🔧 Creating a New Skill

Skills live in `skills/` and expose functions to all agents.

### Structure
```
skills/<skill_name>/
├── SKILL.md        ← Required: manifest + function docs
├── __init__.py     ← Optional: Python module
└── README.md       ← Optional: user-facing docs
```

### SKILL.md Template
```yaml
---
name: my_skill
version: 1.0
tier: 3
category: <category>
description: One-sentence description
exposed_functions:
  - function_name
dependencies:
  - other_skill_id
---

# My Skill

## Purpose
...

## Exposed Functions

### function_name(arg: type) → return_type
...
```

### Registration
Add to `shared-context/SKILL_REGISTRY.json`:
```json
{
  "id": "my_skill",
  "name": "My Skill",
  "version": "1.0",
  "tier": 3,
  "status": "active",
  "source": "skill",
  "path": "skills/my_skill/SKILL.md",
  "description": "...",
  "category": "...",
  "domain": "internal",
  "cost_tier": "free"
}
```

---

## 🤖 Creating a New Agent

Agents live in `agents/` (primary) or `subagents/` (support roles).

### Structure
```
agents/<agent_name>/
└── SKILL.md        ← Required: role + capabilities + governance
```

### SKILL.md Template
```yaml
---
name: my_agent
version: 1.0
tier: <1|2|3>
description: Role description
---

# My Agent

## Role
...

## Tier
...

## Capabilities
### function_name() → type
...

## Activation
Triggered by: ...

## Dependencies
- skill_name

## Governance
...
```

### Registration
1. Add to `shared-context/AGENTS.md` agent roster table
2. Add to `CLAUDE.md` agent roster table
3. Add to SKILL_REGISTRY.json with source="agent"

---

## 🔐 Security Requirements

ALL additions must pass:
1. Security Agent scan (minimum score: 60)
2. Review of SKILL.md for dangerous patterns
3. No hardcoded tokens or paths
4. Declared license

---

## 📝 Checklist Before Submitting

```
[ ] Security scan passed (score ≥ 60)
[ ] SKILL.md / manifest.json created
[ ] SKILL_REGISTRY.json updated
[ ] knowledge_index.md updated
[ ] AGENTS.md updated (for agents)
[ ] CLAUDE.md directory map updated (if new directory)
[ ] version.json updated
```

---

*"A well-documented addition is a gift to future agents."*
