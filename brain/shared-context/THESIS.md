# AI OS Core Strategy (THESIS.md)
# Version: 2.0 | Updated: 2026-03-24

This document defines the fundamental principles of the **AI Operating System** integrated into this project.

## 1. The 10 Pillars

1. **AI Agents = Digital Workforce:** Specialized roles in `subagents/`.
2. **Markdown = Operating System:** Human-readable coordination.
3. **Filesystem = Coordination Layer:** Transparent tool interaction.
4. **Context = Intelligence:** Proactive retrieval using **Hybrid Search** (Lexical + Semantic).
5. **Memory = Long-term Edge:** Fact-based storage (ASM Style).
6. **Observability = Performance:** Continuous profiling.
7. **Async/MQ = Scalability:** Decoupled agent communication.
8. **Neural Links = Association:** Connected intelligence.
9. **Resilience = Stability:** Circuit breakers and self-healing.
10. **Autonomy = Orchestration:** Self-decomposing tasks.
11. **Accountability = Verification:** Receipt-based task logging.
12. **Reflection = Wisdom:** Periodically thinking about lessons learned (Smallville style).
13. **Connectivity = Expansion:** Web and Cloud as secondary memory (Firecrawl & GDrive).
14. **Diagnostics = Health:** Continuous self-auditing (React Doctor style).
15. **Patterns = Efficiency:** Recognizing DSA patterns to solve faster (DSA Engine).
16. **Persistence = Eternity:** Observation-based long-term memory (Cosmic Memory).
17. **Security = Integrity:** Defensive auditing and anti-exploit (Security Shield).
18. **Operations = Continuity:** Job scheduling and automated alerting (XYOPS style).
19. **Evolution = Adaptation:** Self-modifying dossiers and strategies (Cognitive Evolver).
20. **Insight = Intuition:** Cross-domain pattern discovery (Insight Engine).
21. **Reconnaissance = Visibility:** Deep web crawling and form mapping (Katana Protocol).
22. **Accountability = Sustainability:** Economic token budgeting and survival metrics (ClawWork Style).
23. **Command = Authority:** Shell mastery and automated diagnostics (Copilot-CLI Style).
24. **Identity = DNA:** Consistent persona, tone, and strategic approach (SOUL Protocol).
25. **Governance = Constitution:** Hard rules, safety tiers, and risk management (AGENTS Protocol).
26. **Retrieval = Relationship:** GraphRAG and semantic layer indexing (QueryWeaver Protocol).
27. **Bridge = Connection:** Remote agent control and push notifications (ccpoke Protocol).
28. **Grounding = Evidence:** Source-grounded reasoning and multi-doc synthesis (NotebookLM Style).
29. **Aesthetics = WOW:** Cinematic scroll-driven UI and premium visual storytelling (Kino Protocol).
30. **Efficiency = Focus:** Accessibility Tree parsing for 90% token reduction (PinchTab Protocol).
31. **Automation = Continuity:** Smart Hooks for session-start awareness and end-session handoff (Continuity Protocol).
32. **Portability = Universal:** Cross-agent skill deployment (ClaudeKit Protocol).
33. **Scaling = On-Demand:** Lazy-loading of skill instructions to preserve context window (Vercel Agent Protocol).
34. **Synergy = Orchestration:** Multi-agent prompts synchronized via the Router-Worker-QA loop (Agent Fusion Protocol).
35. **Corp Mode = Structure:** Virtual AI company with C-suite agents running autonomous departments via daily brief → KPI → retro cycles (Corp Orchestrator Protocol).
36. **Intake = Client Gateway:** Structured client brief collection, feasibility scoring, and proposal routing as the first gate for all external requests (Project Intake Protocol).
37. **Cowork = Parallelism:** Multi-agent parallel execution with shared context, enabling simultaneous specialist collaboration on complex tasks (Cowork Protocol).
38. **HITL = Safety Gate:** Human-in-the-loop approval checkpoints before high-stakes autonomous actions — no agent bypasses the CEO gate (HITL Gateway Protocol).
39. **Economy = Efficiency:** Route each request to the cheapest capable LLM — balancing quality, speed, and token cost (LLM Router Protocol).
40. **Agile = Velocity:** Sprint-based delivery with structured BMAD planning — from brief to backlog to shipped feature (BMAD Protocol).

### 📐 The LLM Triangle (Core Engineering)
- **SOP (Standard Operating Procedure):** Our `workflows/` and `corp/prompts/runes/`.
- **Engineering:** Our `skills/`, `subagents/mq/`, and `telemetry/`.
- **Context:** Our `brain/shared-context/`, `brain/memory/`, and `brain/knowledge/`.

## 2. Shared Context & Infrastructure

- **`brain/shared-context/`** — Global strategies, thesis, governance, agent roster
- **`subagents/mq/<dept>_brief.md`** — The "Nervous System" for task passing between agents
- **`corp/prompts/runes/`** — Standardized ritual prompts and SOP templates
- **`telemetry/receipts/`** — Cryptographically-auditable task receipts (JSON, per step)
- **`brain/skills/`** — 45+ loaded skill modules, queried via `SKILL_REGISTRY.json`
- **`plugins/`** — managed via kho/plugins/registry.json (7 tier1, 7 tier2) (firecrawl, LightRAG, crewai, zeroleaks, etc.)
- **`brain/shared-context/report_formats.md`** — Standard output formats all agents must use when reporting to CEO (loaded at boot Step 6)

All Agents must adhere to the global **Shared Context**:
- **SOUL.md**: Core identity, values, and behavioral constraints
- **GOVERNANCE.md**: Hard rules, safety tiers, escalation policy, security guardrails
- **AGENTS.md**: Full agent/subagent roster, dept assignments, skills, plugins
- **THESIS.md** *(this file)*: Strategic pillars and architectural philosophy

## 3. Knowledge Base (The "What")

Immutable references for the AI OS technical landscape. Loaded on-demand by agents.

| Source | Content | Access |
|--------|---------|--------|
| `brain/skills/` | 14 active installed skills (SKILL_REGISTRY.json) (SKILL.md per skill) | via SKILL_REGISTRY.json |
| `brain/knowledge/` | Agent-curated knowledge index | via knowledge_navigator skill |
| `plugins/` | managed via kho/plugins/registry.json (7 tier1, 7 tier2) (firecrawl, LightRAG, cognee, etc.) | via knowledge_navigator |
| `brain/shared-context/` | GOVERNANCE, AGENTS, SOUL, THESIS | loaded at boot |
| `brain/agents/` | 99 agent definitions (brain/agents/) | loaded at boot |
| `brain/agents/` | 52 named agents across 21 depts | loaded on-demand |
| `ops/workflows/` | SOP workflow files | loaded on-demand |
| `corp/org_chart.yaml` | Corp Mode company structure | via corp_orchestrator |
| `corp/kpi_targets.yaml` | KPI targets per department | via corp_orchestrator |
| `SKILL_REGISTRY.json` | Master registry of all 14 active skills + 8 kho (rules/prompts/memory/plugins/mcp/llm/cicd/brain) | queried at boot |

## 4. Memory (The "Record")

A recursive history of growth — multi-layer, multi-timeframe.

| Layer | Location | Type | Managed by |
|-------|----------|------|------------|
| **Working Memory** | `brain/memory/session/` | current context | context_manager skill |
| **Short-term** | `brain/memory/` | task outputs, receipts | Claude Code |
| **Long-term (Semantic)** | `brain/knowledge/` | enriched knowledge | archivist + knowledge_enricher |
| **Long-term (Neural)** | neural_memory skill | associative graph | neural_memory skill |
| **Cross-session** | cosmic_memory skill | observations, reflections | cognitive_reflector |
| **Corp History** | `brain/memory/corp_history/` | dept briefs, retros | corp_learning_loop skill |
| **Receipts** | `telemetry/receipts/` | step-by-step audit trail | Claude Code (write), Antigravity (read) |
| **Archive** | `telemetry/archive/` | rotated old receipts | archivist skill |

### Memory Write Rules
- Only Claude Code may write to `telemetry/receipts/`
- Only archivist may rotate archives
- Tier 0 files are **read-only for all agents** — CEO modifies only
- cosmic_memory writes cross-session observations after `cognitive_reflector.reflect()`

---

## 5. Operating Principles (The "How")

Non-negotiable behavioral rules for all AI OS agents. These complement GOVERNANCE.md.

### Language Policy (RULE-LANG-01)
| Audience | Language |
|----------|----------|
| CEO output (Antigravity → Human) | **Vietnamese** |
| System files, code, receipts, logs | **English** |
| Agent-to-agent communication | **English** |
| Boot files, SOUL, THESIS, GOVERNANCE | **English** |

### Execution Rules

| Rule | Policy |
|------|--------|
| **2-Strike Rule** | Claude Code: FAIL 1 → try different approach → FAIL 2 → BLOCKED, stop and report |
| **Receipt-per-Action** | Every autonomous action must produce a JSON receipt in `telemetry/receipts/` |
| **Boot Fallback** | Missing boot file → log warning, skip step, report to CEO. Never assume defaults |
| **Security Gate** | New plugin/tool/integration → Strix/GRC scan FIRST before activation |
| **Tier 0 Protection** | No AI agent may self-modify Tier 0 files. CEO only |

### HITL Trigger Threshold

CEO approval required BEFORE agent proceeds when:
- Action modifies Tier 0 or Tier 1 files
- Budget impact > threshold defined in `corp/kpi_targets.yaml`
- External connection not previously approved
- New agent/plugin activation
- Security incident or Level 3 escalation

### Reporting Standards

All CEO-facing reports must follow formats in `brain/shared-context/report_formats.md`.
Key formats: `DAILY_BRIEF`, `TASK_RECEIPT`, `ESCALATION_REPORT`, `KPI_SNAPSHOT`, `PROPOSAL`.
