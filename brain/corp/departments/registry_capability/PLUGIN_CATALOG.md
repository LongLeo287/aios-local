# AI OS Corp — Plugin Catalog (v1.0)
# Owner: Registry & Capability Management
# Updated: 2026-03-17
# Total: 88 plugins in plugins/ directory

---

## Quick Navigation

| Group | Owner | Count |
|-------|-------|-------|
| [A - AI/LLM Core](#group-a) | it_infra | 14 |
| [B - Agent Standards](#group-b) | registry_capability | 12 |
| [C - Claude Dev Tools](#group-c) | engineering | 14 |
| [D - Security](#group-d) | security_grc | 7 |
| [E - Memory/Context](#group-e) | asset_library | 6 |
| [F - Web & Data](#group-f) | rd | 6 |
| [G - Marketing/Affiliate](#group-g) | marketing | 4 |
| [H - UI/UX Frontend](#group-h) | engineering | 5 |
| [I - Performance/Monitoring](#group-i) | system_health | 3 |
| [J - Agentic Platform](#group-j) | it_infra | 10 |
| [K - Training/Onboard](#group-k) | od_learning | 4 |
| [L - Pending Review](#group-l) | content_intake | 3 |

---

## Group A — AI/LLM Core Platforms {#group-a}

**Owner:** `it_infra` | **Gate:** GATE_SECURITY
**Accessible by:** engineering, rd, registry_capability
**Managed by:** Head of IT Infrastructure

| Plugin | Status | Tier | Purpose |
|--------|--------|------|---------|
| `openviking` | active | 2 | OpenAI-compatible LLM gateway + OpenViking RAG |
| `openrag` | active | 2 | RAG pipeline framework |
| `nexusrag` | active | 2 | Enterprise-grade RAG system |
| `LightRAG` | active | 2 | Lightweight RAG implementation |
| `cognee` | active | 2 | Knowledge graph + agentic memory |
| `neural-memory-repo` | active | 2 | Neural memory backend |
| `deepagents` | active | 2 | Deep agentic reasoning framework |
| `crewai` | active | 2 | Multi-agent crew orchestration |
| `hivemind-plugin` | active | 3 | Swarm intelligence coordination |
| `oh-my-openagent` | active | 3 | OpenAgent platform integrations |
| `openclaw` | active | 2 | Open Claude agentic framework |
| `openclaw-command-center` | active | 2 | OpenClaw control panel |
| `openclaw-rl` | active | 3 | Reinforcement learning module |
| `openspec` | active | 3 | API specification intelligence |

---

## Group B — Agent Standards & Registries {#group-b}

**Owner:** `registry_capability` | **Gate:** none (internal)
**Accessible by:** od_learning, engineering
**Managed by:** registry-manager-agent

| Plugin | Status | Tier | Purpose |
|--------|--------|------|---------|
| `agent-skills-standard` | active | 1 | Universal agent skill specification |
| `skills-chronicle` | active | 2 | Skill version history & changelog |
| `skills-manager` | active | 2 | Skill lifecycle manager |
| `skill-generator` | active | 2 | Skill scaffolding tool |
| `claudy-registry` | active | 2 | Claude skill registry |
| `awesome-claude-skills` | active | 3 | Curated skill collection |
| `composio-awesome-claude-skills` | active | 3 | Composio skill library |
| `antigravity-awesome-skills` | active | 3 | Antigravity skill store |
| `vercel-agent-skills` | active | 3 | Vercel agent skills |
| `vercel-labs-skills` | active | 3 | Vercel Labs research skills |
| `awesome-openclaw-agents` | active | 3 | OpenClaw agent catalog |
| `agent-smart-memo` | active | 3 | Smart memo for agents |

---

## Group C — Claude Dev Tools {#group-c}

**Owner:** `engineering` | **Gate:** GATE_QA
**Accessible by:** qa_testing, registry_capability
**Managed by:** backend-architect-agent

| Plugin | Status | Tier | Purpose |
|--------|--------|------|---------|
| `carlrannaberg-claudekit` | active | 3 | Extended Claude Code tools (diff views, memory shortcuts) |
| `claudekit` | active | 3 | Core Claude toolkit |
| `claude-code-best-practice` | active | 2 | Best practices guide for Claude Code |
| `claude-code-setup` | active | 2 | Dev environment setup |
| `claude-code-prod-plugin` | active | 2 | Production code patterns |
| `ralph-claude-code` | active | 3 | Claude Code extensions |
| `ccpoke` | active | 3 | Notification poking tool |
| `socraticode` | active | 3 | Socratic coding assistant |
| `smart-search` | active | 3 | Intelligent codebase search |
| `think-better` | active | 3 | Structured thinking for agents |
| `dbcooper` | active | 3 | DB query assistant |
| `everything-claude-code` | active | 2 | Comprehensive Claude guide |
| `bmad-method` | active | 2 | Build-Measure-Assert-Deploy methodology |
| `superpowers` | active | 2 | Extended AI capabilities |

---

## Group D — Security & Penetration Testing {#group-d}

**Owner:** `security_grc` | **Gate:** GATE_SECURITY (RESTRICTED)
**Accessible by:** qa_testing ONLY
**Managed by:** `pentest-agent` (new — added 2026-03-17)

| Plugin | Status | Tier | Purpose |
|--------|--------|------|---------|
| `cerberus-cve-tool` | active | 2 | CVE database scanner |
| `claude-bug-bounty` | active | 2 | Bug bounty automation |
| `fbi-watchdog` | active | 2 | Threat intelligence monitoring |
| `GitHacker` | active | 2 | Repository security audit |
| `identYwaf` | active | 2 | WAF identification |
| `zeroleaks` | active | 2 | Secret/token leak detection |
| `kong-reverse-engineer` | active | 3 | API gateway analysis |

---

## Group E — Memory & Context Management {#group-e}

**Owner:** `asset_library` | **Gate:** none
**Accessible by:** operations, od_learning
**Managed by:** library-manager-agent

| Plugin | Status | Tier | Purpose |
|--------|--------|------|---------|
| `claude-mem` | active | 2 | Session memory persistence layer |
| `cloud-sync` | active | 2 | Cross-machine memory synchronization |
| `claude-ws` | active | 2 | CEO workspace manager |
| `assistant-context` | active | 3 | Context injection for assistants |
| `neural-memory-repo` | active | 2 | Neural memory backend (also in Group A) |
| `open-claude-cowork` | active | 3 | Collaborative coding context |

---

## Group F — Web & Data Intelligence {#group-f}

**Owner:** `rd` | **Gate:** GATE_SECURITY (for scraped content)
**Accessible by:** content_intake, asset_library, strategy
**Managed by:** `data-collector-agent` (new — added 2026-03-17)

| Plugin | Status | Tier | Purpose |
|--------|--------|------|---------|
| `firecrawl` | active | 2 | Web crawling & structured extraction |
| `gitingest` | active | 2 | Git repository ingestion |
| `langextract` | active | 2 | Language/document extraction |
| `pageindex` | active | 3 | Page indexing engine |
| `autoresearchclaw` | active | 3 | Automated research pipeline |
| `public-apis` | active | 3 | Public API directory & catalog |

---

## Group G — Marketing & Affiliate {#group-g}

**Owner:** `marketing` | **Gate:** GATE_CONTENT
**Accessible by:** finance, strategy
**Managed by:** `affiliate-agent` (new — added 2026-03-17)

| Plugin | Status | Tier | Purpose |
|--------|--------|------|---------|
| `affiliate-skills` | active | 3 | Affiliate marketing automation |
| `affitor-affiliate-skills` | active | 3 | Affitor platform skills |
| `affitor-network` | active | 3 | Affiliate network integrations |
| `okara-crypto` | active | 3 | Crypto marketing tools |

---

## Group H — UI/UX & Frontend {#group-h}

**Owner:** `engineering` | **Gate:** GATE_QA
**Accessible by:** marketing, qa_testing
**Managed by:** frontend-agent / ui-ux-agent

| Plugin | Status | Tier | Purpose |
|--------|--------|------|---------|
| `pixel-agents` | active | 2 | AI pixel/design agents |
| `ui-ux-pro-max` | active | 2 | Pro UI/UX design intelligence |
| `vscode-antigravity-cockpit` | active | 3 | VSCode AI cockpit extension |
| `supoclip` | active | 3 | Screen clip/annotation tool |
| `LobsterBoard` | active | 3 | Agent coordination board UI |

---

## Group I — Performance & Monitoring {#group-i}

**Owner:** `system_health` | **Gate:** none
**Accessible by:** it_infra, qa_testing, finance
**Managed by:** health-chief-agent

| Plugin | Status | Tier | Purpose |
|--------|--------|------|---------|
| `PerformanceStudio` | active | 2 | Full-stack performance studio |
| `claude-usage-checker` | active | 2 | Token/API usage tracker |
| `generative-ai-beginners` | active | 3 | AI literacy & training materials |

---

## Group J — Agentic Platform Infrastructure {#group-j}

**Owner:** `it_infra` | **Gate:** GATE_SECURITY
**Accessible by:** operations, engineering, C-Suite
**Managed by:** it-manager-agent

| Plugin | Status | Tier | Purpose |
|--------|--------|------|---------|
| `AntigravityManager` | active | 1 | Core Antigravity manager |
| `AstrBot` | active | 2 | Telegram/Discord bot framework |
| `antigravity-manager` | active | 1 | Antigravity config layer |
| `antigravity-kit` | active | 2 | Dev kit for Antigravity |
| `antigravity-deck` | active | 2 | Dashboard/deck plugin |
| `antigravity-mobile` | active | 3 | Mobile companion app |
| `antigravity-switcher` | active | 2 | AI model switcher |
| `vinagent` | active | 3 | Vietnamese agent framework |
| `MaxKB` | active | 2 | Enterprise knowledge base platform |
| `deepagents` | active | 2 | (also listed in Group A) |

---

## Group K — Training & Onboarding {#group-k}

**Owner:** `od_learning` | **Gate:** none
**Accessible by:** hr_people, registry_capability
**Managed by:** training-agent

| Plugin | Status | Tier | Purpose |
|--------|--------|------|---------|
| `llm-finetuning` | active | 2 | Local model fine-tuning pipeline |
| `claws` | active | 2 | Claude agent workflow patterns |
| `agency-agents` | active | 3 | Multi-agency coordination patterns |
| `ai-tagger` | active | 3 | Automatic content tagging |

---

## Group L — Pending Review / Uncategorized {#group-l}

**Status:** Route to `content_intake` for CIV processing
**Note:** These may overlap with existing resources — apply "train, don't overwrite" rule

| Plugin | Pending Route | Notes |
|--------|--------------|-------|
| `anthropic-skills` | od_learning | Training material — check overlap with skills/ |
| `claude-scientific-skills` | rd + security_grc | Dual purpose — split routing needed |
| `awesome-web-agents` | asset_library OR rd | Classify after CIV review |

---

## CHANGE LOG

| Date | Change |
|------|--------|
| 2026-03-17 | v1.0 created — initial 88-plugin catalog with group ownership |
| 2026-03-17 | Added pentest-agent (Group D), data-collector-agent (Group F), affiliate-agent (Group G) |
