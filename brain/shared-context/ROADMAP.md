# AI OS Corp — Master Roadmap
# Version: 3.0 | Updated: 2026-03-22 | Authority: Tier 1 (Strategy)

---

## Current System State (2026-03-22)

| Layer | Component | Status | Details |
|-------|-----------|--------|---------|
| Infrastructure | Boot Sequence | ✅ DONE | 9-step boot via GEMINI.md + CLAUDE.md |
| Core Files | SOUL, GOVERNANCE, AGENTS, THESIS | ✅ DONE | Steps 1-5 complete |
| Report Standards | report_formats.md | ✅ DONE | Step 6 — 7 formats defined |
| Corp Mode | org_chart.yaml v2.4 | ✅ DONE | 21 depts, ~80 agent roles |
| Corp Skills | corp_orchestrator, corp_learning_loop | ✅ DONE | Tier 1 skills |
| Skill Registry | SKILL_REGISTRY.json | ✅ DONE | 103+ skills + plugins |
| Skills | brain/skills/ | ✅ DONE | 45 skill modules |
| Plugins | plugins/ | ✅ DONE | 102 plugins |
| Workflows | ops/workflows/ | ✅ DONE | 29 workflows |
| Agents | workforce/agents/ | ✅ DONE | 28 agent dirs |
| Subagents | workforce/subagents/ | ✅ DONE | 38 subagent dirs |
| Security | Strix/GRC scan system | ✅ DONE | 4 gate system + zeroleaks |
| Client Intake | project_intake_agent | ✅ DONE | DORMANT — awaiting bot tokens |

---

## Boot Sequence Progress

| Step | File | Status |
|------|------|--------|
| Step 1 | SOUL.md | ✅ Done |
| Step 2 | GOVERNANCE.md | ✅ Done |
| Step 3 | AGENTS.md | ✅ Done (31 agents, 38 subagents) |
| Step 4 | THESIS.md | ✅ Done (40 pillars, 5 sections) |
| Step 5 | SKILL_REGISTRY.json | ✅ Done |
| Step 6 | report_formats.md | ✅ Done (7 formats) |
| Step 7 | pre-session.md | 🔄 Needs cleanup |
| Step 8 | post-session.md | ✅ Exists |
| Step 9 | blackboard.json | ✅ Exists |

---

## AI OS Corp — Department Readiness

| Dept | Head Agent | Workers | Status |
|------|-----------|---------|--------|
| Engineering | backend-architect-agent | 5 | ✅ Ready |
| QA & Testing | security-engineer-agent | 3 | ✅ Ready (GATE) |
| IT Infrastructure | it-manager-agent | 3 | ✅ Ready |
| Marketing | growth-agent | 5 | ✅ Ready |
| Support | channel-agent | 3 | ✅ Ready |
| Content Review | editor-agent | 4 | ✅ Ready (GATE) |
| Operations | scrum-master-agent | 3 | ✅ Ready |
| HR & People | hr-manager-agent | 4 | ✅ Ready |
| Security & GRC | strix-agent | 5 | ✅ Ready (autonomous) |
| Finance | cost-manager-agent | 3 | ✅ Ready |
| Strategy | product-manager-agent | 4 | ✅ Ready |
| Legal | legal-agent | 3 | ✅ Ready |
| R&D | rd-lead-agent | 4 | ✅ Ready |
| Registry & Capability | registry-manager-agent | 4 | ✅ Ready |
| Asset & Knowledge Library | library-manager-agent | 4 | ✅ Ready |
| OD & Learning | org-architect-agent | 4 | ✅ Ready |
| Planning & PMO | pmo-agent | 3 | ✅ Ready |
| Monitoring & Inspection | monitor-chief-agent | 3 | ✅ Ready |
| System Health | health-chief-agent | 3 | ✅ Ready |
| Content Intake & Vetting | intake-chief-agent | 7 | ✅ Ready |
| Client Reception | project-intake-agent | 3 | 🔴 DORMANT (awaiting bot) |

---

## Active Priorities (Phase 1 — System Hardening)

- [ ] **pre-session.md cleanup** — remove redundant boot steps, align with 9-step sequence
- [ ] **RULE-DYNAMIC-01** — add reference to GOVERNANCE.md header
- [ ] **report_formats.md load test** — verify boot Step 6 reads file correctly
- [ ] **corp/org_chart.yaml sync** — keep in sync with AGENTS.md as agents are added
- [ ] **kpi_targets.yaml review** — verify targets per dept are realistic
- [ ] **escalation_rules.yaml audit** — verify Level 1/2/3 thresholds are correct
- [ ] **Client Reception activation** — get Telegram bot token → activate DORMANT dept

---

## Upcoming Milestones (Phase 2 — Operation)

### Phase 2A: Corp Mode Live Test
- [ ] Activate Corp Mode via `corp_orchestrator.activate_corp_mode`
- [ ] Run first daily brief cycle across all 21 depts
- [ ] Verify KPI scoreboard updates correctly
- [ ] Test escalation flow Level 1 → 2 → 3 → CEO

### Phase 2B: Client Pipeline
- [ ] Activate nullclaw/tinyclaw for Telegram intake
- [ ] Test client brief → proposal_engine → CEO approve flow
- [ ] First live client project via AI OS Corp

### Phase 2C: Learning Loop
- [ ] Run first `corp_learning_loop.run_corp_retro`
- [ ] Verify proposals generated and reach CEO
- [ ] First CEO-approved skill proposal

---

## Capability Matrix (Current)

| Capability | Tools | Status |
|-----------|-------|--------|
| Web Scraping | firecrawl, langextract | ✅ |
| Knowledge RAG | LightRAG, cognee, NotebookLM | ✅ |
| Security Scanning | zeroleaks, cerberus-cve-tool, fbi-watchdog | ✅ |
| Multi-agent Coord | crewai, open-claude-cowork | ✅ |
| AI Model Routing | llm_router, MiniMax-MCP | ✅ |
| Notification Push | notification_bridge (Telegram/Discord/Zalo) | ✅ |
| Skill Generation | skill_generator (8-phase pipeline) | ✅ |
| Client Intake | project_intake_agent + proposal_engine | 🔴 DORMANT |
| Affiliate/Revenue | affiliate-skills, affitor-network | ✅ |
| UI/Design System | ui-ux-pro-max, shadcn, tailwind | ✅ |
| Game Development | godot/unity/unreal/roblox engineers | ✅ |
| Mobile Apps | Android_APK_Modification, mobile-agent | ✅ |

---

## Archive: Legacy Phases (Pre-Corp)

> The following phases were from the BookMark Extension project (completed 2026-03-14).
> These established the AI OS infrastructure now used by AI OS Corp.

- ✅ Phase 8: UI & AI Resource Consolidation
- ✅ Phase 9: Advanced Local Automation (Intel Infrastructure Upgrade)
- ✅ Phase 10: Intelligent Assistant [85%] — superseded by AI OS Corp launch
- ✅ Phase 11: Cognitive Evolution — merged into THESIS.md Pillars 19-20

---

*"The roadmap is not a promise. It is a living direction."*
