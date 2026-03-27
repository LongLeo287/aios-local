---
name: Experimental Skills
description: Staging area for experimental and fetched skills. Supabase agent skills (FETCHED_gh_supabase_agent_skills_20260320) have been promoted to brain/skills/domains/databases/supabase-agent-skills/. Staging area is now clear.
department: rd, registry_capability
tier: 3
category: experimental
status: active
tags: [experimental, staging, supabase, fetched, promoted]
---

# Experimental Skills

**Repo:** `brain/skills/experimental`
**Type:** Staging area / skill inbox
**Department:** R&D / Registry & Capability
**Tier:** 3 — experimental, not production-ready
**Status:** Draft

## What it is

A sandbox staging area for skills fetched from external sources or generated experimentally. Skills here are:
1. **Fetched** from GitHub/web automatically by `ingest-router-agent`
2. **Under review** — not yet integrated into FAST_INDEX or SKILL_REGISTRY
3. **Pending promotion** to stable domain directories

## Current Contents

### `FETCHED_gh_supabase_agent_skills_20260320-092430/`
Supabase agent skills fetched from GitHub on 2026-03-20 09:24:30.

**To process:**
```bash
# Review and promote to brain/skills/domains/databases/
mv "brain/skills/experimental/FETCHED_gh_supabase_agent_skills_20260320-092430" \
   "brain/skills/domains/databases/supabase-agent-skills-v2"

# Then update FAST_INDEX.json
python brain/registry/build_index.py
```

## Processing Workflow

```
External source → ingest-router-agent → experimental/ (stage)
     ↓ review
  domains/<domain>/ (promote) → FAST_INDEX + SKILL_REGISTRY
```

## AI OS Integration
- **Owner:** `registry_capability` + R&D
- **Auto-ingest:** `ingest-router-agent` deposits here
- **Review by:** CEO / Registry dept before promotion
- **ClawTask:** Not listed in production Skills panel until promoted
