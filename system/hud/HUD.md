# AI OS HUD â€” HEAD-UP DISPLAY
# Version: 2.0 | 2026-03-24 | CEO reads nÃ y má»—i session
# Update: Phase 7 (RETRO) + post-session.md â†’ hud/STATUS.json
# Path: <AI_OS_ROOT>\hud\HUD.md

---

## CORP STATUS

| Field | Value |
|-------|-------|
| Cycle | 11 â€” ACTIVE |
| Last Retro | 2026-03-23 |
| Depts Active | 21 / 21 |
| Agents Total | 52 |
| Skills | 14 installed |
| System Version | AI OS v2.1 |

---



## ðŸŽ›ï¸ Báº¢NG ÄIá»€U KHIá»‚N â€” QUICK COMMANDS

### Boot AI OS
| Action | Command | MÃ´ táº£ |
|--------|---------|-------|
| ðŸ§  **Cognitive Boot** | `python system/ops/scripts/aos_start.py` | 9 bÆ°á»›c Ä‘á»c context (GEMINI/SOUL/GOVERNANCE/...) |


### Corp Cycle
| Action | Command | MÃ´ táº£ |
|--------|---------|-------|
| ðŸš€ **Start Cycle** | `python ops/aos.py corp start` | Phase 0+1: Boot + CEO Brief |

### B1-B12 Cycle 12 (added 2026-03-25)
| Action | Command | MÃ´ táº£ |
|--------|---------|-------|
| ðŸ“Š **B4 Dept Health** | `python ops/scripts/dept_health.py` | Health dashboard 21 depts |
| ðŸ’“ **B5 System Pulse** | `python ops/scripts/system_pulse.py` | 1-shot health check |
| ðŸ” **B5 Pulse Loop** | `python ops/scripts/system_pulse.py --loop` | 5-min auto check |
| ðŸ“š **B6 KI Index** | `python ops/scripts/ki_indexer.py` | Rebuild KI_INDEX.md |
| ðŸ“¦ **B7 CIV Stats** | `python ops/scripts/civ_stats.py` | Rebuild CIV_STATS.md |
| ðŸ“ **B2 Write Briefs** | `python ops/scripts/brief_writer.py` | Auto-write 21 dept briefs |
| ðŸ§  **B3 Synthesis** | `python ops/scripts/cognitive_reflector.py` | Phase 5 synthesis |
| ðŸ“¤ **Dispatch** | `python ops/aos.py corp dispatch` | Phase 2-3: Dispatch 21 depts |
| ðŸ”„ **Retro + HUD** | `python ops/aos.py corp retro` | Phase 5-7: Synthesis + Retro |
| ðŸ“Š **Status** | `python ops/aos.py status` | Xem cycle status |
| ðŸ“¬ **Proposals** | `python ops/aos.py proposals` | List pending proposals |
| âœ… **Approve Proposal** | `python ops/aos.py proposals approve <id>` | Approve 1 proposal |
| ðŸ–¥ï¸ **HUD Update** | `python ops/aos.py hud update` | Update HUD dashboard |

### Telegram Bridge
| Action | Command | MÃ´ táº£ |
|--------|---------|-------|
| ðŸ¤– **Start All Bridges** | `python infra/channels/start_bridges.py` | Telegram + DeepAgents + ClawTask watcher |
| ðŸ“± **Telegram Only** | `python infra/channels/start_bridges.py telegram` | Chá»‰ Telegram bot |
| ðŸ”‡ **No ClawTask** | `python infra/channels/start_bridges.py --no-clawtask` | Bridge khÃ´ng theo dÃµi ClawTask |
| ðŸ” **Check Config** | `python infra/channels/config.py` | Verify tokens + credentials |

### System Maintenance
| Action | Command | MÃ´ táº£ |
|--------|---------|-------|
| ðŸŽ¯ **Fix Skill Tiers** | `python brain/shared-context/fix_skill_tiers.py --write` | Batch-fix skills thiáº¿u tier |
| ðŸ”Œ **Install VS Code Ext** | `powershell ops/scripts/install_vscode_extensions.ps1` | Auto-install extensions |
| ðŸ“¡ **Start LightRAG** | `python ops/scripts/lightrag_server.py` | RAG server :9621 |
| ðŸ” **Rebuild Index** | `python ops/aos.py rebuild-index` | Rebuild FAST_INDEX |
| ðŸ—‚ï¸ **HUD Snapshot** | `powershell ops/scripts/update_hud.ps1` | Force update HUD |

### Knowledge Intake (CIV)
| Action | Command | MÃ´ táº£ |
|--------|---------|-------|
| ðŸ“¥ **Intake link** | Paste link trá»±c tiáº¿p | CIV pipeline auto-trigger |
| ðŸ” **View A-Z Flow** | [FLOW_AZ.md](../ops/workflows/FLOW_AZ.md) | Full system workflow |
| ðŸ“‹ **Escalations** | [escalations.md](../brain/shared-context/corp/escalations.md) | HITL queue |
---

## QUY TRÃŒNH Váº¬N HÃ€NH (WORKFLOWS)

### CORE â€” Báº¯t buá»™c biáº¿t

| Workflow | File | Trigger |
|----------|------|---------|
| **A-Z Flow (full)** | [FLOW_AZ.md](../ops/workflows/FLOW_AZ.md) | Reference tá»•ng thá»ƒ |
| **Corp Daily Cycle** | [corp-daily-cycle.md](../ops/workflows/corp-daily-cycle.md) | `"aos corp start"` |
| **CIV / Intake** | [content-intake-flow.md](../ops/workflows/content-intake-flow.md) | Báº¥t ká»³ link/repo/URL nÃ o |
| **Pre-Session** | [pre-session.md](../ops/workflows/pre-session.md) | Äáº§u má»—i session |
| **Post-Session** | [post-session.md](../ops/workflows/post-session.md) | Cuá»‘i má»—i session |
| **Notification Bridge** | [notification-bridge.md](../ops/workflows/notification-bridge.md) | Táº¥t cáº£ alerts |
| **Antigravity Boot** | [antigravity-boot.md](../ops/workflows/antigravity-boot.md) | Boot Antigravity |

### AGENT & KNOWLEDGE

| Workflow | File | Trigger |
|----------|------|---------|
| Agent Auto-Create | [agent-auto-create.md](../ops/workflows/agent-auto-create.md) | GAP â†’ [A] |
| Agent Workflow | [agent-workflow.md](../ops/workflows/agent-workflow.md) | Agent task start |
| Claude Code Handoff | [claude-code-handoff.md](../ops/workflows/claude-code-handoff.md) | Code task |
| Automated CLI Handoff | [automated_cli_handoff.md](../ops/workflows/automated_cli_handoff.md) | CLI handoff |
| Skill Discovery Auto | [skill-discovery-auto.md](../ops/workflows/skill-discovery-auto.md) | Phase 0 + Phase 8 |
| Knowledge Ingest | [knowledge-ingest.md](../ops/workflows/knowledge-ingest.md) | `"aos ingest <src>"` |
| Knowledge Distribution | [knowledge-distribution-flow.md](../ops/workflows/knowledge-distribution-flow.md) | Post-CIV |
| Ingest External | [ingest-external.md](../ops/workflows/ingest-external.md) | External data |

### CORP GOVERNANCE

| Workflow | File | Trigger |
|----------|------|---------|
| Corp Escalation | [corp-escalation-flow.md](../ops/workflows/corp-escalation-flow.md) | L3/L4 issue |
| Corp Gate Flow | [corp-gate-flow.md](../ops/workflows/corp-gate-flow.md) | Approval gates |
| Corp Learning Loop | [corp-learning-loop.md](../ops/workflows/corp-learning-loop.md) | `"aos retro"` |
| Corp Task Flow | [corp-task-flow.md](../ops/workflows/corp-task-flow.md) | Task assignment |
| Dept Head Brief | [dept-head-brief.md](../ops/workflows/dept-head-brief.md) | Phase 3 |
| QA Gate | [qa-gate.md](../ops/workflows/qa-gate.md) | Phase 5 |
| Delegation SOP | [DELEGATION_SOP.md](../ops/workflows/DELEGATION_SOP.md) | Task delegation |
| Swarm Dispatch | [swarm-dispatch.md](../ops/workflows/swarm-dispatch.md) | Multi-agent tasks |

### SECURITY & INFRA

| Workflow | File | Trigger |
|----------|------|---------|
| Repo Evaluation | [repo-evaluation.md](../ops/workflows/repo-evaluation.md) | Pre-integration |
| Plugin Integration | [plugin-integration.md](../ops/workflows/plugin-integration.md) | Post evaluation |
| Nemoclaw Strix Scan | [nemoclaw-strix-scan.md](../ops/workflows/nemoclaw-strix-scan.md) | Security scan |
| Secrets Management | [secrets-management.md](../ops/workflows/secrets-management.md) | Credentials |
| Backup Project | [backup-project.md](../ops/workflows/backup-project.md) | Backup |
| Recovery Protocol | [recovery-protocol.md](../ops/workflows/recovery-protocol.md) | Disaster recovery |
| Project Reset | [project_reset_protocol.md](../ops/workflows/project_reset_protocol.md) | Full reset |

### SPECIALIZED

| Workflow | File | Trigger |
|----------|------|---------|
| Launch MCP Claude | [launch-mcp-claude.md](../ops/workflows/launch-mcp-claude.md) | MCP startup |
| Presentation Protocol | [presentation-protocol.md](../ops/workflows/presentation-protocol.md) | CEO presentation |
| Supabase Debug | [supabase-debug.md](../ops/workflows/supabase-debug.md) | DB issues |
| Wakeup Project | [wakeup-project.md](../ops/workflows/wakeup-project.md) | Project resume |
| Export AI OS Template | [export_ai_os_template.md](../ops/workflows/export_ai_os_template.md) | Template export |
| Execution Template | [execution_template.md](../ops/workflows/execution_template.md) | Task template |
| **Auto-Execute Commands** | [auto-execute-commands.md](../ops/workflows/auto-execute-commands.md) | CEO paste commands â†’ tá»± phÃ¢n loáº¡i + cháº¡y |

---

## PHÃ’NG BAN (21 DEPARTMENTS)

### TIER 1 â€” CORE BUSINESS

| # | Dept | Head Agent | Manager Prompt | Worker Prompt | Rules |
|---|------|-----------|----------------|---------------|-------|
| 01 | Engineering | backend-architect | [MANAGER](../corp/departments/engineering/MANAGER_PROMPT.md) | [WORKER](../corp/departments/engineering/WORKER_PROMPT.md) | [rules](../corp/departments/engineering/rules.md) |
| 02 | QA Testing | test-manager | [MANAGER](../corp/departments/qa_testing/MANAGER_PROMPT.md) | [WORKER](../corp/departments/qa_testing/WORKER_PROMPT.md) | [rules](../corp/departments/qa_testing/rules.md) |
| 03 | IT Infra | it-manager | [MANAGER](../corp/departments/it_infra/MANAGER_PROMPT.md) | [WORKER](../corp/departments/it_infra/WORKER_PROMPT.md) | [rules](../corp/departments/it_infra/rules.md) |
| 04 | Marketing | growth-agent | [MANAGER](../corp/departments/marketing/MANAGER_PROMPT.md) | [WORKER](../corp/departments/marketing/WORKER_PROMPT.md) | [rules](../corp/departments/marketing/rules.md) |
| 05 | Support | channel-agent | [MANAGER](../corp/departments/support/MANAGER_PROMPT.md) | [WORKER](../corp/departments/support/WORKER_PROMPT.md) | [rules](../corp/departments/support/rules.md) |
| 06 | HR & People | hr-manager | [MANAGER](../corp/departments/hr_people/MANAGER_PROMPT.md) | [WORKER](../corp/departments/hr_people/WORKER_PROMPT.md) | [rules](../corp/departments/hr_people/rules.md) |
| 07 | Security/GRC | strix-agent | [MANAGER](../corp/departments/security_grc/MANAGER_PROMPT.md) | [WORKER](../corp/departments/security_grc/WORKER_PROMPT.md) | [rules](../corp/departments/security_grc/rules.md) |
| 08 | Finance | cost-manager | [MANAGER](../corp/departments/finance/MANAGER_PROMPT.md) | [WORKER](../corp/departments/finance/WORKER_PROMPT.md) | [rules](../corp/departments/finance/rules.md) |
| 09 | Planning/PMO | pmo-agent | [MANAGER](../corp/departments/planning_pmo/MANAGER_PROMPT.md) | [WORKER](../corp/departments/planning_pmo/WORKER_PROMPT.md) | [rules](../corp/departments/planning_pmo/rules.md) |
| 10 | Monitoring | monitor-agent | [MANAGER](../corp/departments/monitoring_inspection/MANAGER_PROMPT.md) | [WORKER](../corp/departments/monitoring_inspection/WORKER_PROMPT.md) | [rules](../corp/departments/monitoring_inspection/rules.md) |
| 11 | Operations | ops-agent | [MANAGER](../corp/departments/operations/MANAGER_PROMPT.md) | [WORKER](../corp/departments/operations/WORKER_PROMPT.md) | [rules](../corp/departments/operations/rules.md) |

### TIER 2 â€” SPECIALIZED

| # | Dept | Head Agent | Manager Prompt | Worker Prompt | Rules |
|---|------|-----------|----------------|---------------|-------|
| 12 | Legal | legal-agent | [MANAGER](../corp/departments/legal/MANAGER_PROMPT.md) | [WORKER](../corp/departments/legal/WORKER_PROMPT.md) | [rules](../corp/departments/legal/rules.md) |
| 13 | R&D | rd-lead | [MANAGER](../corp/departments/rd/MANAGER_PROMPT.md) | [WORKER](../corp/departments/rd/WORKER_PROMPT.md) | [rules](../corp/departments/rd/rules.md) |
| 14 | OD/Learning | learning-agent | [MANAGER](../corp/departments/od_learning/MANAGER_PROMPT.md) | [WORKER](../corp/departments/od_learning/WORKER_PROMPT.md) | [rules](../corp/departments/od_learning/rules.md) |
| 15 | Client Reception | reception-agent | [MANAGER](../corp/departments/client_reception/MANAGER_PROMPT.md) | [WORKER](../corp/departments/client_reception/WORKER_PROMPT.md) | [rules](../corp/departments/client_reception/rules.md) |
| 16 | Strategy | product-manager | [MANAGER](../corp/departments/strategy/MANAGER_PROMPT.md) | [WORKER](../corp/departments/strategy/WORKER_PROMPT.md) | [rules](../corp/departments/strategy/rules.md) |
| 17 | System Health | system-health | [MANAGER](../corp/departments/system_health/MANAGER_PROMPT.md) | [WORKER](../corp/departments/system_health/WORKER_PROMPT.md) | [rules](../corp/departments/system_health/rules.md) |
| 18 | Content Review | review-chief | [MANAGER](../corp/departments/content_review/MANAGER_PROMPT.md) | [WORKER](../corp/departments/content_review/WORKER_PROMPT.md) | [rules](../corp/departments/content_review/rules.md) |

### TIER 3 â€” GOVERNANCE

| # | Dept | Head Agent | Manager Prompt | Worker Prompt | Rules | CI/CD |
|---|------|-----------|----------------|---------------|-------|-------|
| 19 | Content Intake/CIV | civ-agent | [MANAGER](../corp/departments/content_intake/MANAGER_PROMPT.md) | [WORKER](../corp/departments/content_intake/WORKER_PROMPT.md) | [rules v1.2](../corp/departments/content_intake/rules.md) | [intake-pipeline](../kho/cicd/pipelines/intake-pipeline.md) |
| 20 | Registry/Capability | registry-manager | [MANAGER](../corp/departments/registry_capability/MANAGER_PROMPT.md) | [WORKER](../corp/departments/registry_capability/WORKER_PROMPT.md) | [rules](../corp/departments/registry_capability/rules.md) | [skill-pipeline](../kho/cicd/pipelines/skill-pipeline.md) |
| 21 | Asset Library | library-manager | [MANAGER](../corp/departments/asset_library/MANAGER_PROMPT.md) | [WORKER](../corp/departments/asset_library/WORKER_PROMPT.md) | [rules](../corp/departments/asset_library/rules.md) | â€” |

---

## AGENTS (52 AGENTS)

**Full registry:** [kho/agents/registry.json](../kho/agents/registry.json)
**Org chart:** [corp/org_chart.yaml](../corp/org_chart.yaml)
**Definitions:** [brain/agents/](../brain/agents/)

### KEY AGENTS â€” Quick Reference

| Agent | Dept | Role | Definition |
|-------|------|------|------------|
| **strix-agent** | Security/GRC | GATE: all new tools/plugins | [brain/agents/](../brain/agents/) |
| **civ-agent** | Content Intake | GATE: all external content | [MANAGER](../corp/departments/content_intake/MANAGER_PROMPT.md) |
| **cognitive_reflector** | PMO/Strategy | Cross-dept synthesis + RETRO | [brain/agents/](../brain/agents/) |
| **registry-manager** | Registry | Skill/plugin registry | [MANAGER](../corp/departments/registry_capability/MANAGER_PROMPT.md) |
| **content-analyst-agent** | CIV | 6-question analysis | [WORKER](../corp/departments/content_intake/WORKER_PROMPT.md) |
| **skill-creator-agent** | Registry | New skill creation | [WORKER](../corp/departments/registry_capability/WORKER_PROMPT.md) |
| **backend-architect-agent** | Engineering | Head of engineering | [MANAGER](../corp/departments/engineering/MANAGER_PROMPT.md) |
| **test-manager-agent** | QA | QA gate owner | [MANAGER](../corp/departments/qa_testing/MANAGER_PROMPT.md) |
| **web_researcher** | R&D | Firecrawl specialist | [brain/agents/](../brain/agents/) |
| **rd-lead-agent** | R&D | Research + experiments | [MANAGER](../corp/departments/rd/MANAGER_PROMPT.md) |

### CIV PIPELINE AGENTS

| Agent | Role |
|-------|------|
| intake-agent | Create CIV ticket |
| classifier-agent | Classify type (REPO/WEB/DOC...) |
| repo-fetcher | Clone repo to QUARANTINE |
| web-crawler | Firecrawl extraction |
| doc-parser | Extract text from docs |
| content-analyst-agent | 6-question analysis |
| content-validator | Quality score + VALUE_TYPE |
| ingest-router | Route to destination |

---

## KHO (STORAGE REPOSITORIES)

| Kho | Index | Registry | Purpose |
|-----|-------|---------|---------|
| Rules | [kho/rules/INDEX.md](../kho/rules/INDEX.md) | â€” | Táº¥t cáº£ rules |
| Prompts | [kho/prompts/INDEX.md](../kho/prompts/INDEX.md) | â€” | CEO/CSUITE/MANAGER/WORKER |
| Memory | [kho/memory/INDEX.md](../kho/memory/INDEX.md) | â€” | Blackboard + dept memories |
| Plugins | [kho/plugins/INDEX.md](../kho/plugins/INDEX.md) | [registry.json](../kho/plugins/registry.json) | 14 tier1/tier2 |
| MCP | [kho/mcp/INDEX.md](../kho/mcp/INDEX.md) | [registry.json](../kho/mcp/registry.json) | 5 MCP servers |
| LLM | [kho/llm/INDEX.md](../kho/llm/INDEX.md) | [registry.json](../kho/llm/registry.json) | 7 providers |
| CI/CD | [kho/cicd/INDEX.md](../kho/cicd/INDEX.md) | â€” | 4 pipelines |
| Brain | [kho/brain/INDEX.md](../kho/brain/INDEX.md) | â€” | Knowledge + KI notes |
| Agents | [kho/agents/INDEX.md](../kho/agents/INDEX.md) | [registry.json](../kho/agents/registry.json) | 52 agents |
| Workflows | [kho/workflows/INDEX.md](../kho/workflows/INDEX.md) | â€” | 37 workflows |

---

## SYSTEM REFERENCES

| Document | Path | Purpose |
|----------|------|---------|
| Master System Map | [MASTER_SYSTEM_MAP.md](../MASTER_SYSTEM_MAP.md) | Full system overview |
| Antigravity Boot Rules | [GEMINI.md](../GEMINI.md) | Session governance |
| Claude Code Boot | [CLAUDE.md](../CLAUDE.md) | Claude Code rules |
| Claude Code Constitution | [.clauderules](../.clauderules) | Hard prohibitions |
| Soul / Identity | [SOUL.md](../brain/shared-context/SOUL.md) | Values + personality |
| Governance | [GOVERNANCE.md](../brain/shared-context/GOVERNANCE.md) | Authority structure |
| Thesis (40 Pillars) | [THESIS.md](../brain/shared-context/THESIS.md) | Strategic pillars |
| Skill Registry | [SKILL_REGISTRY.json](../brain/shared-context/SKILL_REGISTRY.json) | Active skills |
| Blackboard | [blackboard.json](../brain/shared-context/blackboard.json) | Live system state |
| KPI Scoreboard | [kpi_scoreboard.json](../brain/shared-context/corp/kpi_scoreboard.json) | 21 dept KPIs |
| Escalations | [escalations.md](../brain/shared-context/corp/escalations.md) | Open L2/L3 |
| Mission | [mission.md](../brain/shared-context/corp/mission.md) | Strategic direction |
| Gaps Register | [gaps_register.md](../corp/memory/global/gaps_register.md) | GAP proposals |
| Decisions Log | [decisions_log.md](../corp/memory/global/decisions_log.md) | CEO decisions |
| HUD Status (JSON) | [STATUS.json](STATUS.json) | Machine-readable state |

---

*HUD v2.1 | 2026-03-25 | Báº¢NG ÄIá»€U KHIá»‚N: 15 commands | 37 workflows | 21 depts | 99 agents | 8 kho*
*Update trigger: Phase 7 RETRO â†’ auto-write hud/snapshots/<date>.md*

### ðŸ“¦ Repo On-Demand
| Action | Command |
|--------|---------|
| Detect repos | `python ops/scripts/repo_resolver.py "mÃ´ táº£ dá»± Ã¡n"` |
| By dept | `python ops/scripts/repo_resolver.py --dept engineering` |
| Project init | `python ops/aos.py project init <name> --dept <dept> --clone` |
| View catalog | `brain/knowledge/notes/LARGE_REPOS_CATALOG.md` |

