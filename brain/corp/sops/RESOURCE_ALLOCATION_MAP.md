# AI OS Corp — Resource Allocation Map (v1.0)
# Authority: Registry & Capability Management → COO
# Updated: 2026-03-17
# Source of Truth for: skill ownership, plugin ownership, subagent assignment

---

## LEGEND
- **OWNER**: Phòng ban sở hữu và chịu trách nhiệm tài nguyên này
- **ACCESSIBLE**: Các phòng ban được phép sử dụng (access control)
- **RESTRICTED**: Chỉ owner mới được dùng
- **ALL**: Mọi phòng ban có thể truy cập

---

## SECTION 1 — CORE SKILLS (38 skills in `skills/`)

| Skill ID | Owner Dept | Accessible By | Tier | Category |
|----------|-----------|---------------|------|----------|
| `reasoning_engine` | od_learning | ALL | 1 | cognitive |
| `cognitive_reflector` | strategy | ALL | 2 | cognitive |
| `cognitive_evolver` | od_learning | od_learning, strategy, registry_capability | 2 | cognitive |
| `knowledge_enricher` | asset_library | ALL | 2 | knowledge |
| `context_manager` | operations | ALL | 1 | core |
| `cosmic_memory` | asset_library | asset_library, od_learning, strategy | 2 | memory |
| `smart_memory` | asset_library | ALL | 2 | memory |
| `neural_memory` | asset_library | asset_library, od_learning, system_health | 2 | memory |
| `insight_engine` | strategy | strategy, rd, od_learning | 2 | cognitive |
| `knowledge_navigator` | asset_library | asset_library, support, content_intake | 3 | knowledge |
| `corp_learning_loop` | od_learning | RESTRICTED | 3 | org |
| `skill_generator` | registry_capability | RESTRICTED | 2 | registry |
| `skill_sentry` | security_grc | security_grc, qa_testing | 2 | security |
| `production_qa` | qa_testing | qa_testing, registry_capability | 2 | qa |
| `diagnostics_engine` | system_health | system_health, monitoring_inspection, qa_testing | 2 | health |
| `resilience_engine` | system_health | RESTRICTED | 2 | health |
| `performance_profiler` | qa_testing | qa_testing, engineering, it_infra | 2 | performance |
| `shell_assistant` | it_infra | it_infra, content_intake, engineering | 2 | infrastructure |
| `repo_analyst` | asset_library | asset_library, registry_capability, rd | 3 | analysis |
| `llm_router` | it_infra | RESTRICTED | 1 | infrastructure |
| `orchestrator_pro` | operations | RESTRICTED (CEO/COO layer) | 2 | orchestration |
| `corp_orchestrator` | operations | RESTRICTED | 3 | orchestration |
| `tools_hub` | it_infra | engineering, it_infra | 2 | infrastructure |
| `antigravity` | it_infra | RESTRICTED (system core) | 1 | infrastructure |
| `security_shield` | security_grc | security_grc, qa_testing | 2 | security |
| `apk-modification` | security_grc | RESTRICTED | 2 | security |
| `cybersecurity` | security_grc | security_grc, qa_testing, engineering | 2 | security |
| `visual_excellence` | marketing | marketing, content_review | 2 | creative |
| `ui-ux` | engineering | engineering, marketing | 2 | design |
| `ui-ux-pro-max` | engineering | engineering, marketing | 2 | design |
| `seo-aeo-optimization` | marketing | marketing, content_review | 2 | marketing |
| `accessibility_grounding` | engineering | engineering, qa_testing | 2 | design |
| `web_intelligence` | rd | rd, content_intake, strategy | 2 | research |
| `multi-source-aggregation` | rd | rd, asset_library, content_intake | 2 | research |
| `video-extraction` | rd | rd, engineering | 2 | research |
| `agentskills-spec` | registry_capability | registry_capability, od_learning | 2 | registry |
| `notification_bridge` | operations | operations, support | 2 | channels |
| `channel_manager` | operations | RESTRICTED | 3 | channels |
| `archivist` | operations | RESTRICTED | 2 | memory |

---

## SECTION 2 — SUBAGENTS (38 blueprints in `subagents/`)

| Subagent | Assigned Dept | Primary Skill | Notes |
|----------|--------------|---------------|-------|
| `rapid-prototyper` | engineering | skill_generator | On-demand POC builder |
| `code-reviewer` | engineering | production_qa | Code quality gatekeeper |
| `api-tester` | engineering | production_qa | API endpoint verifier |
| `devops-ops` | engineering | shell_assistant | CI/CD ops specialist |
| `git-workflow-master` | engineering | shell_assistant | Git branching / ops |
| `mcp-builder` | engineering | tools_hub | MCP server construction |
| `database-optimizer` | engineering | diagnostics_engine | DB query optimization |
| `performance-benchmarker` | qa_testing | performance_profiler | Benchmarking specialist |
| `security-auditor` | qa_testing | skill_sentry | Security audit reviewer |
| `compliance-auditor` | qa_testing | production_qa | Policy compliance |
| `incident-response-commander` | security_grc | security_shield | Incident escalation |
| `growth-hacker` | marketing | seo-aeo-optimization | Growth strategy |
| `social-media-strategist` | marketing | visual_excellence | Social content |
| `paid-media-specialist` | marketing | seo-aeo-optimization | Ads & ROI |
| `image-prompt-engineer` | marketing | visual_excellence | AI image generation |
| `support-analyst` | support | knowledge_navigator | Ticket resolution |
| `doc-writer` | content_review | knowledge_enricher | Technical documentation |
| `brand-guardian` | content_review | visual_excellence | Brand voice consistency |
| `data-analyst` | strategy | insight_engine | KPI analysis |
| `researcher` | strategy | web_intelligence | Market research |
| `scientific-researcher` | rd | web_intelligence | Academic research |
| `academic-researcher` | rd | web_intelligence | Literature review |
| `narrative-designer` | rd | insight_engine | Story/content systems |
| `blockchain-engineer` | rd | tools_hub | Blockchain/crypto R&D |
| `godot-engineer` | rd | tools_hub | Game engine R&D |
| `roblox-developer` | rd | tools_hub | Roblox platform R&D |
| `unity-engineer` | rd | tools_hub | Unity game dev |
| `unreal-engineer` | rd | tools_hub | Unreal engine |
| `xr-developer` | rd | tools_hub | XR/AR/VR development |
| `sales-engineer` | marketing | knowledge_navigator | Sales engineering |
| `developer-advocate` | marketing | knowledge_enricher | DevRel & community |
| `product-feedback-analyst` | strategy | insight_engine | User feedback synthesis |
| `cultural-intelligence-analyst` | hr_people | cognitive_reflector | Cross-cultural comms |
| `chief-of-staff` | hr_people | orchestrator_pro | Exec coordination |
| `prompt-engineer` | od_learning | reasoning_engine | Prompt optimization |
| `project-shepherd` | planning_pmo | context_manager | Project lifecycle |
| `ux-designer` | engineering | ui-ux-pro-max | UX research & design |
| `mq` | operations | context_manager | Message queue ops |

---

## SECTION 3 — PLUGINS (88 plugins in `plugins/`)

### Group A — AI/LLM Core Platforms
**Owner:** `it_infra` | **Accessible:** engineering, rd, registry_capability

| Plugin | Purpose |
|--------|---------|
| `openviking` | OpenAI-compatible LLM gateway |
| `openrag` | RAG pipeline framework |
| `nexusrag` | Enterprise RAG system |
| `LightRAG` | Lightweight RAG implementation |
| `cognee` | Knowledge graph + memory |
| `neural-memory-repo` | Neural memory backend |
| `deepagents` | Deep agentic framework |
| `crewai` | Multi-agent crew orchestration |
| `hivemind-plugin` | Swarm intelligence |
| `oh-my-openagent` | OpenAgent platform |
| `openclaw` | Open Claude framework |
| `openclaw-command-center` | Claw control panel |
| `openclaw-rl` | Reinforcement learning module |
| `openspec` | API spec intelligence |

### Group B — Agent Standards & Registries
**Owner:** `registry_capability` | **Accessible:** od_learning, engineering

| Plugin | Purpose |
|--------|---------|
| `agent-skills-standard` | Universal skill spec |
| `skills-chronicle` | Skill version history |
| `skills-manager` | Skill lifecycle manager |
| `skill-generator` | Skill scaffolding tool |
| `claudy-registry` | Claude skill registry |
| `awesome-claude-skills` | Curated skill collection |
| `composio-awesome-claude-skills` | Composio skill library |
| `antigravity-awesome-skills` | Antigravity skill store |
| `vercel-agent-skills` | Vercel agent skills |
| `vercel-labs-skills` | Vercel Labs research skills |
| `awesome-openclaw-agents` | OpenClaw agent catalog |
| `openspec` | API specification skill |

### Group C — Claude Dev Tools
**Owner:** `engineering` | **Accessible:** qa_testing, registry_capability

| Plugin | Purpose |
|--------|---------|
| `carlrannaberg-claudekit` | Extended Claude Code tools |
| `claudekit` | Core Claude toolkit |
| `claude-code-best-practice` | Best practices guide |
| `claude-code-setup` | Dev environment setup |
| `claude-code-prod-plugin` | Production code patterns |
| `ralph-claude-code` | Claude Code extensions |
| `ccpoke` | Notification poking tool |
| `socraticode` | Socratic coding assistant |
| `smart-search` | Intelligent search |
| `think-better` | Structured thinking |
| `dbcooper` | DB query assistant |
| `everything-claude-code` | Comprehensive Claude guide |
| `bmad-method` | Build-Measure-Assert-Deploy |
| `superpowers` | Extended AI capabilities |

### Group D — Security & Penetration Testing 🔒
**Owner:** `security_grc` | **Accessible:** qa_testing ONLY | **Managed by:** `pentest-agent`

| Plugin | Purpose |
|--------|---------|
| `cerberus-cve-tool` | CVE database scanner |
| `claude-bug-bounty` | Bug bounty automation |
| `fbi-watchdog` | Threat intelligence |
| `GitHacker` | Repository security audit |
| `identYwaf` | WAF identification |
| `zeroleaks` | Secret/token leak detection |
| `kong-reverse-engineer` | API gateway analysis |

### Group E — Memory & Context Management
**Owner:** `asset_library` | **Accessible:** operations, od_learning

| Plugin | Purpose |
|--------|---------|
| `claude-mem` | Session memory layer |
| `agent-smart-memo` | Smart memo for agents |
| `assistant-context` | Context injection |
| `cloud-sync` | Cross-machine memory sync |
| `claude-ws` | CEO workspace manager |
| `neural-memory-repo` | Neural memory backend |

### Group F — Web & Data Intelligence
**Owner:** `rd` | **Accessible:** content_intake, asset_library, strategy | **Managed by:** `data-collector-agent`

| Plugin | Purpose |
|--------|---------|
| `firecrawl` | Web crawling & extraction |
| `gitingest` | Git repo ingestion |
| `langextract` | Language extraction |
| `pageindex` | Page indexing engine |
| `autoresearchclaw` | Automated research |
| `public-apis` | Public API directory |

### Group G — Marketing & Affiliate
**Owner:** `marketing` | **Accessible:** finance, strategy | **Managed by:** `affiliate-agent`

| Plugin | Purpose |
|--------|---------|
| `affiliate-skills` | Affiliate marketing skills |
| `affitor-affiliate-skills` | Affitor platform skills |
| `affitor-network` | Affiliate network integrations |
| `okara-crypto` | Crypto marketing tools |

### Group H — UI/UX & Frontend
**Owner:** `engineering` | **Accessible:** marketing, qa_testing

| Plugin | Purpose |
|--------|---------|
| `pixel-agents` | AI pixel/design agents |
| `ui-ux-pro-max` | Pro UI/UX intelligence |
| `vscode-antigravity-cockpit` | VSCode AI cockpit |
| `supoclip` | Screen clip/annotation |
| `open-claude-cowork` | Collaborative coding |

### Group I — Performance & Monitoring
**Owner:** `system_health` | **Accessible:** it_infra, qa_testing, finance

| Plugin | Purpose |
|--------|---------|
| `PerformanceStudio` | Full-stack performance studio |
| `claude-usage-checker` | Token/usage tracker |
| `generative-ai-beginners` | AI literacy training |

### Group J — Agentic Platform Infrastructure
**Owner:** `it_infra` | **Accessible:** operations, engineering, C-Suite

| Plugin | Purpose |
|--------|---------|
| `AntigravityManager` | Core Antigravity manager |
| `AstrBot` | Telegram/Discord bot framework |
| `antigravity-manager` | Antigravity config layer |
| `antigravity-kit` | Dev kit for Antigravity |
| `antigravity-deck` | Dashboard/deck plugin |
| `antigravity-mobile` | Mobile companion |
| `antigravity-switcher` | Model switcher |
| `vinagent` | Vietnamese agent framework |
| `MaxKB` | Knowledge base platform |
| `LobsterBoard` | Agent coordination board |

### Group K — Training & Onboarding
**Owner:** `od_learning` | **Accessible:** hr_people, registry_capability

| Plugin | Purpose |
|--------|---------|
| `llm-finetuning` | Local model fine-tuning |
| `claws` | Claude agent workflows |
| `agency-agents` | Multi-agency patterns |
| `ai-tagger` | Auto-tagging system |

### Group L — Uncategorized / Pending Review
**Status:** Needs CIV pipeline processing | **Route to:** content_intake

| Plugin | Notes |
|--------|-------|
| `agent-smart-memo` | Possibly duplicate with claude-mem |
| `assistant-context` | Overlap check needed |
| `awesome-web-agents` | Route: asset_library or rd |
| `claude-scientific-skills` | Route: rd + security |
| `anthropic-skills` | Route: od_learning (training) |
| `LobsterBoard` | Route: it_infra |

---

## SECTION 4 — AGENTS (26 named agents in `agents/`)

| Agent | Dept | Primary Role | Primary Skill |
|-------|------|-------------|---------------|
| `software-architect-agent` | engineering | CTO co-pilot, architecture decisions | reasoning_engine |
| `backend-architect-agent` | engineering | Head of Engineering | reasoning_engine |
| `frontend-agent` | engineering | UI/UX, React/Vue | ui-ux-pro-max |
| `ai-ml-agent` | engineering | AI/ML integration, RAG | knowledge_enricher |
| `devops-agent` | engineering | CI/CD, Docker | shell_assistant |
| `sre-agent` | engineering | SRE, reliability | diagnostics_engine |
| `mobile-agent` | engineering | iOS/Android | tools_hub |
| `security-engineer-agent` | qa_testing | Head of QA & Testing | production_qa |
| `security_agent` | security_grc | Security operations | security_shield |
| `growth-agent` | marketing | CMO, Head of Marketing | seo-aeo-optimization |
| `content-agent` | marketing | Content creation | visual_excellence |
| `scrum-master-agent` | operations | COO, Head of Operations | orchestrator_pro |
| `channel_agent` | operations | Channel management | channel_manager |
| `archivist` | operations | Knowledge archivist | archivist |
| `cognitive_reflector` | strategy | Strategy analyst | cognitive_reflector |
| `data-agent` | strategy | Data analytics | insight_engine |
| `product-manager-agent` | strategy | CSO, Head of Strategy | reasoning_engine |
| `orchestrator_pro` | operations | CEO co-pilot | orchestrator_pro |
| `superpowers-agent` | qa_testing | QA engineer | production_qa |
| `knowledge_agent` | support | Knowledge retrieval | knowledge_navigator |
| `repo_ingest_agent` | content_intake | Repo ingestion pipeline | shell_assistant |
| `antigravity` | it_infra | Core system agent | antigravity |
| `antigravity-kit-agent` | it_infra | Dev kit orchestrator | tools_hub |
| `ui-ux-agent` | engineering | UX research & design | ui-ux-pro-max |
| `maxkb-agent` | it_infra | MaxKB operations | knowledge_enricher |
| `game-designer-agent` | rd | Game design R&D | tools_hub |

---

## CHANGE LOG

| Date | Change | Authority |
|------|--------|-----------|
| 2026-03-17 | v1.0 created — initial resource allocation map | OD&L Audit |
| 2026-03-17 | Added 3 new workers: pentest-agent, data-collector-agent, affiliate-agent | org_chart.yaml v2.5 |
