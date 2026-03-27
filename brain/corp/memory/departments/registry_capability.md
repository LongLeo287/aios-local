# Memory: registry_capability department
# Type: department
# Dept Number: 4
# Retention: 30d rolling
# Updated: 2026-03-23

## Always-Load Context

- Dept: Registry & Capability Management (Dept 4)
- Reports to: CTO
- Core responsibility: Own and enforce plugin intake, registry, and skill lifecycle.

## SOP â€” Plugin Governance (RULE-TIER-01 + RULE-PROCESS-01)

### Owned Assets
- `plugins/plugin-catalog.md` â€” Source of truth for all repo statuses
- `brain/shared-context/SKILL_REGISTRY.json` â€” Registry of all active ecosystem/skills/plugins
- `plugins/registry.json` â€” Machine-readable plugin registry

### Key Constraints
1. **Never register a plugin without APPROVE verdict** from Dept 20 (CIV) via `ops/workflows/repo-evaluation.md`.
2. **Never activate a plugin** without Security CLEAR from Dept 10 (Strix).
3. Every skill must pass `SKILL_SPEC.md` + `validate_skills.ps1` before `status: active`.
4. `auto_load: false` is the DEFAULT for all new plugins â€” never override without CEO approval.
5. Tier 1 list is FROZEN: {Mem0, Firecrawl, LightRAG, CrewAI, GitNexus}. Additions require CEO approval.
6. Tier promotion (T2â†’T1) requires CTO sign-off.
7. Deprecation is graceful: 1 cycle notice before removal.

### Workflow Sequence (Must Follow In Order)
```
INCOMING REPO REQUEST
  â†’ Dept 20 (CIV): GATE 1 â€” repo-evaluation.md
  â†’ Dept 10 (Security): Phase 1 Security Scan
  â†’ Dept 4 (Registry): Phases 2â€“7 of plugin-integration.md
  â†’ Update catalog âš¡ â†’ âœ…
  â†’ Register in SKILL_REGISTRY.json
  â†’ Hook into GEMINI.md + CLAUDE.md rules
```

### Version Tracking (Active Tier 1 Plugins)
| Plugin | Track | Command |
|--------|-------|---------|
| mem0 | Weekly | `pip show mem0ai` |
| firecrawl | Weekly | `pip show firecrawl-py` |
| crewai | Weekly | `pip show crewai` |
| LightRAG | Weekly | `cd ecosystem/plugins/LightRAG && git log -1` |
| GitNexus | Monthly | `git log -1` |

## Rolling Memory (30-day):
â†’ [2026-03-23] 3-Tier Architecture enforced. RULE-TIER-01 added to GEMINI.md + CLAUDE.md.
â†’ [2026-03-23] repo-evaluation.md created as mandatory GATE 1 (Owner: Dept 20).
â†’ [2026-03-23] plugin-integration.md updated with PRE-GATE notice.


