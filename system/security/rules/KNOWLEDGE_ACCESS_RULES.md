# KNOWLEDGE_ACCESS_RULES.md — AI OS Knowledge Base Governance
# Version: 1.0 | Created: 2026-03-16
# Authority: Tier 2 (Operations)
# Enforced by: Knowledge Agent, Repo Ingest Agent

---

## Purpose

Governs how agents access, query, and operate on the 127-repo knowledge base
in `knowledge/repos/`, `plugins/`, and `REMOTE/claws/`.

---

## 1. Query-First Rule (MANDATORY)

Before searching ANY external source, agents MUST query internally:

```
Step 1: SKILL_REGISTRY.json → search by id, name, category, domain
Step 2: knowledge/github_repos_index.md → search by repo name / category
Step 3: knowledge/non_cloneable_repos_analysis.md → web-analyzed repos
Step 4: knowledge/knowledge_index.md → all other knowledge docs
Step 5: Only if not found → search external (web_intelligence skill)
```

**Violation:** Calling web search without first checking internal knowledge = Rule Violation.

---

## 2. Trust Levels for Repos

| Source | Trust Level | Execution Allowed? |
|--------|-------------|-------------------|
| `plugins/` (with manifest.json) | HIGH | ✅ Yes (post-Gatekeeper) |
| `REMOTE/claws/` (Claw variants) | MEDIUM | ⚠️ Review SKILL.md first |
| `knowledge/repos/` | REFERENCE | ❌ Read-only, never execute |
| `knowledge/non_cloneable_repos_analysis.md` | REFERENCE | ❌ Read-only, documentation only |
| `knowledge_web` entries (SKILL_REGISTRY) | LOW | ❌ URL reference only |

---

## 3. New Repo Ingestion Checklist

Before adding a new repo to AI OS:

```
[1] Security Scan (MANDATORY)
    → Run: skill_sentry 9-layer analysis on repo URL
    → Minimum score: 60+ to proceed
    → Score < 40: BLOCK + notify user

[2] Classification
    → Tier 1 (plugins/): Agent-executable tools, skills, frameworks
    → Tier 2 (knowledge/repos/): Reference, learning material
    → Tier 3 (REMOTE/claws/): Claw/agentic runtimes

[3] Manifest Creation (for Tier 1 only)
    → Create plugins/<name>/manifest.json following PLUGIN_SPEC.md

[4] SKILL_REGISTRY Registration
    → Add entry to shared-context/SKILL_REGISTRY.json
    → source field: "plugin" | "knowledge_ref" | "knowledge_web"

[5] Knowledge Index Update
    → Add one-line entry to knowledge/knowledge_index.md

[6] Gatekeeper Verification
    → Run gatekeeper.ps1 before first execution
```

---

## 4. Knowledge Base Statistics (as of 2026-03-16)

| Location | Count | Content |
|----------|-------|---------|
| `plugins/` (root) | 44 | Agent-executable plugins |
| `REMOTE/claws/` | 13 | Claw variant runtimes |
| `knowledge/repos/` | 70 | Reference repos |
| **Total physical dirs** | **127** | |
| SKILL_REGISTRY entries | 189 | 41 skills + 56 plugins + 69 refs + 23 web |
| Indexed repos (github_repos_index) | 177 | From Github.txt |
| Web-analyzed repos | 23 | From non_cloneable_repos_analysis.md |

---

## 5. Knowledge Update Cycle

- **Every session:** Check `knowledge/knowledge_index.md` for new entries
- **Weekly:** Run `scripts/skill_loader.ps1` to rebuild SKILL_REGISTRY from filesystem
- **Monthly:** Review `knowledge/LEARNING_LOG.md` for unused repos → archive or document

---

## 6. Prohibited Operations on Knowledge Base

| Action | Rule |
|--------|------|
| Execute code from `knowledge/repos/` directly | ❌ FORBIDDEN |
| Delete items from `knowledge/repos/` without backup | ❌ FORBIDDEN (Tier 3 approval) |
| Modify SKILL_REGISTRY.json `source` field to "plugin" for web entries | ❌ FORBIDDEN |
| Use knowledge_web URLs as if they are installed capabilities | ❌ FORBIDDEN |
| Clone a new repo without security scan | ❌ FORBIDDEN |

---

*"Knowledge is power. Governed knowledge is reliable power."*
