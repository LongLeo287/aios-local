# AI OS Learning Log
# Version: 1.0 | Created: 2026-03-16
# Updated by: Knowledge Agent, Archivist
# Purpose: Track what the AI OS learns each session and from which source

---

## Format

Each entry:
```
### YYYY-MM-DD — Session ID or Task Name
**Source:** repo name / knowledge doc / external URL
**Category:** agent_framework | security | memory | web | dev_tool | ...
**Key Learnings:**
- [bullet] What was learned
**Applied In:** task name or "not applied yet"
```

---

## 2026-03-16 — AI OS Full System Upgrade + Repo Ingestion

### Auto-Claude (AndyMik90/Auto-Claude)
**Source:** knowledge/non_cloneable_repos_analysis.md
**Category:** agent_framework
**Key Learnings:**
- 12-agent parallel execution pattern using git worktrees for isolation
- Self-validating QA loop before user review → apply to production_qa skill
- Memory layer across agent sessions → link to cosmic_memory skill
- Kanban board as agent task board UI → potential dashboard widget
**Applied In:** Not applied yet — architecture inspiration

### ProxyPal (heyhuynhgiabuu/proxypal)
**Source:** knowledge/non_cloneable_repos_analysis.md
**Category:** ai_proxy
**Key Learnings:**
- Multi-AI proxy pattern: Claude/ChatGPT/Gemini → single endpoint localhost:8317/v1
- Tauri + SolidJS for desktop app combining Rust backend + JS frontend
- Auto-detect installed CLI agents and configure them automatically
**Applied In:** channels/ bridge router concept

### SkillSentry (vythanhtra/skillsentry)
**Source:** knowledge/non_cloneable_repos_analysis.md
**Category:** security
**Key Learnings:**
- 9-layer security model: behavior chains, evasion, base64, prompt injection
- Risk scoring 0-100 with threshold blocks at 20/40
- Specific dangerous patterns: READ_SENSITIVE + NETWORK_SEND = Data Exfiltration -90pts
**Applied In:** skills/skill_sentry/SKILL.md, agents/security_agent/SKILL.md, rules/clone_security_protocol.md

### TrainingAI / 8-Level Vietnamese AI Guide (LinesYu/trainingAI)
**Source:** knowledge/non_cloneable_repos_analysis.md
**Category:** ai_learning, system_design
**Key Learnings:**
- 8-level mastery framework: Identity→Context→Multi-Persona→Discipline→Supercommands→Skills→Catalog→Soul Code
- "Soul Code" concept: teach AI to feel "pain" when code quality degrades
- Multi-persona simulation: Architect + Builder + Police roles simultaneously
**Applied In:** cognitive_reflector + cognitive_evolver skills (inspiration)

### marketingskills (coreyhaines31/marketingskills)
**Source:** knowledge/non_cloneable_repos_analysis.md
**Category:** skills_library
**Key Learnings:**
- 35+ ready-to-use marketing skills in 9 categories (CRO/SEO/Copy/RevOps/etc.)
- Plugin-style skill library — installable per-domain
- Claude Code + Antigravity compatible installation
**Applied In:** Not applied yet — available for future marketing/SaaS tasks

### ChatDev 2.0 (OpenBMB/ChatDev)
**Source:** knowledge/non_cloneable_repos_analysis.md
**Category:** agent_framework
**Key Learnings:**
- Role-based multi-agent: CEO (requirements) + CTO (architecture) + Programmer (implementation) + Reviewer (QA)
- Zero-code from text description → production-ready software
- Academic-grade reliability (Stanford/OpenBMB backing)
**Applied In:** AGENTS.md role design inspiration

### Repo Ingestion Session (127 repos)
**Source:** D:\LongLeo\Project\DATA\Github.txt + Google Sheets
**Category:** system_upgrade
**Key Learnings:**
- AI OS can absorb 127 repos (44 plugins + 13 claws + 70 refs) in systematic batch
- --depth=1 cloning is optimal for speed without losing usability
- Non-cloneable repos (private/deleted) can still yield knowledge via README fetch
- SKILL_REGISTRY JSON is the single source of truth for all capabilities
**Applied In:** SKILL_REGISTRY.json (189 entries), github_repos_index.md, knowledge_index.md

---

*Add new entries after each session where new knowledge was acquired.*
*Format: ### YYYY-MM-DD — Task Name*
