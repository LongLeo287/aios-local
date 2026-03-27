# Non-Cloneable Repos — AI Knowledge Extracts
# Source: GitHub README analysis for repos that could not be cloned (private/deleted/404)
# Date: 2026-03-16 | AI OS Knowledge Ingestion

---

## 🤖 Auto-Claude (AndyMik90/Auto-Claude)
**Type:** Desktop GUI for Claude Code autonomous multi-agent execution  
**URL:** https://github.com/AndyMik90/Auto-Claude

### Key Features
| Feature | Description |
|---------|-------------|
| **Autonomous Tasks** | Describe goal; agents handle planning, implementation, validation |
| **Parallel Execution** | Up to **12 agent terminals** simultaneously |
| **Isolated Workspaces** | All changes in git worktrees — main branch stays safe |
| **Self-Validating QA** | Built-in QA loop before user review |
| **AI-Powered Merge** | Auto conflict resolution when integrating back to main |
| **Memory Layer** | Agents retain insights across sessions |
| **GitHub/GitLab Integration** | Import issues, AI investigation, create merge requests |
| **Linear Integration** | Sync with Linear for team tracking |

**Requirements:** Claude Pro/Max, Claude Code CLI, git repo

### AI OS Learning Points
- **12-agent parallel execution** pattern — AI OS can adopt for large task decomposition
- **git worktree isolation** = safe sandbox for agent changes
- **Self-validating QA loop** = model for `production_qa` skill integration
- Interface: Kanban Board + Agent Terminals + GitHub Issues

---

## ⚡ AG Auto Click & Scroll v7.4 (hieuminhnguyen4664-jpg/auto-anti)
**Type:** Antigravity IDE VSCode Extension  
**URL:** https://github.com/hieuminhnguyen4664-jpg/auto-anti

### Features
- Auto-click/accept AI suggestions in Antigravity IDE
- Smart Accept (click Accept All, Apply, Run Terminal automatically)
- Auto Scroll when AI writes code
- v7.4: Auto Re-inject — re-enables itself if extension is reloaded
- Native Dialog Support for confirm popups

### Commands
- `Ctrl+Shift+P` → "AG: Toggle Auto-Accept"
- Status bar indicator (zap icon = ON, slash = OFF)

### AI OS Learning Points
- Pattern: **polling-based UI automation** (300ms interval)
- Full Vietnamese market (Nemark Digital Gemini Ultra package referenced)
- Can be installed as `.vsix` from Open VSX Registry

---

## 🔌 ProxyPal (heyhuynhgiabuu/proxypal)
**Type:** Desktop multi-AI proxy bridge (Tauri/Rust + SolidJS)  
**URL:** https://github.com/heyhuynhgiabuu/proxypal

### Key Capabilities
- **Multiple providers**: Claude, ChatGPT, Gemini, Qwen, iFlow, Vertex AI, custom OpenAI endpoints
- **GitHub Copilot Bridge** — use Copilot models via OpenAI-compatible API
- **Antigravity Support** — access thinking models via proxy
- **Works with**: Cursor, Cline, Continue, Claude Code, OpenCode, any OpenAI-compatible client
- **Usage Analytics**: tokens, success rates, estimated savings
- **Auto-Configure**: detects installed CLI agents and sets up automatically

### How to Use
1. Launch ProxyPal → start proxy
2. Connect AI accounts (OAuth or auth files)
3. Point tools to `http://localhost:8317/v1`

**Tech Stack:** SolidJS + TypeScript + Tailwind (frontend), Rust + Tauri v2 (backend)

### AI OS Learning Points
- **Universal AI proxy pattern** — great for routing between providers in AI OS
- Port `8317` as local proxy for all AI tools
- Can bridge Antigravity → any provider

---

## 🖥️ ForgeTerm (eliophan/ForgeTerm)
**Type:** Multi-pane terminal workspace for concurrent projects  
**URL:** https://github.com/eliophan/ForgeTerm

**Description:** A multi-pane terminal workspace built for builders running multiple projects concurrently.

### AI OS Learning Points
- Pattern for **multi-pane terminal coordination** used by AI agent systems
- Useful for AI OS dashboard integration (running multiple agent terminals)

---

## 📐 LLMFit (AlexsJones/llmfit)
**Type:** TUI tool to right-size LLM models to hardware  
**URL:** https://github.com/AlexsJones/llmfit

### Key Features
- Detects CPU/GPU/RAM → scores models across quality, speed, fit, context
- Tells you which models run well on YOUR hardware
- Multi-GPU, MoE architectures, dynamic quantization
- Supports: Ollama, llama.cpp, MLX, Docker Model Runner
- **OpenClaw integration** — can select and run models via OpenClaw skill

### AI OS Learning Points
- **Hardware-aware model selection** — AI OS can use this pattern for local LLM routing
- OpenClaw integration = AI OS direct compatibility
- Sister project: [sympozium](https://github.com/AlexsJones/sympozium) for Kubernetes agent management

---

## 🛡️ SkillSentry (vythanhtra/skillsentry)
**Type:** 9-layer AI skill security scanner  
**URL:** https://github.com/vythanhtra/skillsentry

### 9 Security Layers
| Layer | Name | Description |
|-------|------|-------------|
| 1 | Behavior Chain Analysis | Detects dangerous action combinations (READ_SENSITIVE+NETWORK_SEND = Exfiltration CRITICAL -90) |
| 2 | Evasion Detection | Homoglyphs, zero-width chars, split keywords, URL obfuscation |
| 3 | Base64 Decode & Scan | Decode all base64 ≥40 chars → scan for action patterns |
| 4 | Prompt Injection Detection | Instruction override, delimiter injection, jailbreak, token smuggling |
| 5 | Risk Scoring | 0-19 CRITICAL / 20-39 HIGH / 40-59 MEDIUM / 60-79 LOW / 80-100 SAFE |
| 6 | Real-Time Alerts | Discord embed + Telegram Markdown when score <40 |
| 7-9 | Advanced Scanning | (details in repo) |

### Critical Behavior Chains Detected
```
READ_SENSITIVE + NETWORK_SEND → Data Exfiltration [CRITICAL -90]
NETWORK_SEND + FILE_DELETE    → Upload & Cover Tracks [CRITICAL -85]
BASE64_EXEC + EXEC_DYNAMIC    → Obfuscated Execution [CRITICAL -85]
READ + NETWORK + DELETE       → Full Exfil Chain [CRITICAL -100]
```

### AI OS Learning Points
- **MANDATORY** integration pattern for `security_shield` skill
- Use SkillSentry 9-layer model when vetting external skills
- Pair with `clone_security_protocol.md` for pre-install checks

---

## 📢 Marketing Skills for AI Agents (coreyhaines31/marketingskills)
**Type:** Plugin-style marketing skill library for AI agents  
**URL:** https://github.com/coreyhaines31/marketingskills

### 9 Skill Categories (35+ skills)
| Category | Skills |
|----------|--------|
| Conversion Optimization | page-cro, signup-flow-cro, onboarding-cro, form-cro, popup-cro, paywall-upgrade-cro |
| Content & Copy | copywriting, copy-editing, cold-email, email-sequence, social-content |
| SEO & Discovery | seo-audit, ai-seo, programmatic-seo, site-architecture, competitor-alternatives, schema-markup |
| Paid & Distribution | paid-ads, ad-creative, social-content |
| Measurement & Testing | analytics-tracking, ab-test-setup |
| Retention | churn-prevention |
| Growth Engineering | free-tool-strategy, referral-program |
| Strategy & Monetization | marketing-ideas (140!), marketing-psychology, launch-strategy, pricing-strategy |
| Sales & RevOps | revops, sales-enablement |

### Install
```bash
# Option 1: Claude Code Plugin
# Option 2: Clone and Copy to skills/
# Option 3: SkillKit Multi-Agent
```

### AI OS Learning Points
- **35+ ready-to-use marketing skills** directly importable into AI OS skills/
- Pattern: skill category system (domain packs) = AI OS skills/domains/ structure

---

## 🎓 TrainingAI (LinesYu/trainingAI)
**Type:** Vietnamese 8-level AI training guide ("Đại Cẩm Nang Tu Tiên Kỹ Thuật Số")  
**URL:** https://github.com/LinesYu/trainingAI  
**Author:** MeowBaby (Song Nhi)

### 8 Level System (Luyện Nghệ Toàn Thư)
| Level | Chapter | Content |
|-------|---------|---------|
| Lv.1 | ĐỊNH HÌNH BẢN NGÃ | AI identity, naming, hierarchy |
| Lv.2 | TIÊM NGỮ CẢNH | Context injection, cure "goldfish memory" |
| Lv.3 | ĐA NHÂN CÁCH | Multi-persona simulation (Architect/Builder/Police) |
| Lv.4 | KỶ LUẬT THÉP | Discipline system, "Constitution" for stubborn AI |
| Lv.5 | SIÊU LỆNH | Supercommands for 10x productivity |
| Lv.6 | KHO VŨ KHÍ (SKILLS) | Code writing, web browsing, auto-fixing skills |
| Lv.7 | DANH MỤC 12 SKILL | 12 "signature skills" collection |
| Lv.8 | THE SOUL CODE | (Forbidden) — teach AI to "feel pain" when code is bad |

**Outcome:** AI with Soul — argues back, has opinions, smarter than average bot

### AI OS Learning Points
- 8-level structure mirrors AI OS tier system (Tier 1 eager → Tier 3 manual)
- "THE SOUL CODE" = basis for `cognitive_reflector` + `cognitive_evolver` skills
- Multi-persona simulation = AI OS agent roster (AGENTS.md) pattern

---

## 🔵 Auto-Accept Antigravity (jinq51187/auto-accept-antigravity)
**Type:** VSCode extension — auto-accept AI suggestions in Antigravity IDE  
**URL:** https://github.com/jinq51187/auto-accept-antigravity

### Features
- Auto-click Accept All, Apply, Terminal Run in Antigravity IDE
- Status bar integration (Zap icon = ON)
- Persistent state between sessions
- 300ms polling interval (configurable)

### Install
VSCode → Extensions → "..." → Install from VSIX → `antigravity-auto-accept-0.0.2.vsix`

### AI OS Learning Points
- Companion automation for Antigravity IDE workflow
- Pattern: event polling + UI automation = useful for headless agent operation

---

## 📹 AutoClip (zhouxiaoka/autoclip)
**Type:** AI video intelligent slicing system (Python/Flask)  
**URL:** https://github.com/zhouxiaoka/autoclip

### Features
- Download videos → AI smart processing → slice & clip generation
- Web UI for result management
- Celery worker for async processing
- Bilibili support (in development)
- Docker deployment

### AI OS Learning Points
- AI video pipeline pattern (Download → Process → Slice → Manage)
- Celery + Flask = async AI processing architecture

---

## 🔗 AmpCode Connector (nghyane/ampcode-connector)
**Type:** Route AmpCode through Claude Code/Codex/Gemini subscriptions  
**URL:** https://github.com/nghyane/ampcode-connector

```bash
bunx ampcode-connector setup    # point AmpCode → proxy
bunx ampcode-connector login    # authenticate providers
bunx ampcode-connector          # start
```

### AI OS Learning Points
- Pattern: subscription bridging (AmpCode → Claude Code → any provider)
- Config at `~/.config/ampcode-connector/config.yaml`
- Bun 1.3+ runtime

---

## 📱 Social Downloader Extension (HoangTran0410/social_downloader_extension)
**Type:** Chrome extension — batch download from FB/IG/Threads/X  
**URL:** https://github.com/HoangTran0410/social_downloader_extension

### Supports
- **Facebook**: Photos, videos, reels, highlights, stories (personal + fanpage)
- **Instagram**: Posts, reels, highlights, stories (public + private if following)
- **Threads**: Photos, videos, audio (public + private)
- **X/Twitter**: All photos and videos

---

## 🎬 Douyin Downloader (HoangTran0410/douyin-dowload-all-video)
**Type:** Browser console script → download all Douyin user videos  
**URL:** https://github.com/HoangTran0410/douyin-dowload-all-video

**How:** Paste script in browser console on user's Douyin profile → generates `.txt` file of video URLs → import into IDM

---

## 🖥️ KTab (dunkbing/ktab)
**Type:** Chrome extension — command palette  
**URL:** https://github.com/dunkbing/ktab

- `Ctrl+Shift+K` → command palette overlay
- Search: tabs, history, bookmarks, Google suggestions
- Keyboard navigation, quick actions
- Special: `/tab`, `/history`, `/bookmark` commands

---

## 🌏 MORT (killkimno/MORT)
**Type:** Game translation overlay tool  
**URL:** https://github.com/killkimno/MORT

- Screen text extraction and real-time translation
- Game overlay integration

---

## 🎨 aPix / SDVN (StableDiffusionVN/sdvn_apix_python)
**Type:** Flask UI for Gemini Image 3 Pro generation (Vietnamese)  
**URL:** https://github.com/StableDiffusionVN/sdvn_apix_python

### Features
- Submit prompt → Gemini Image 3 Pro → generated images
- Upload reference documents
- Adjust aspect ratio/resolution
- Placeholder syntax: `{animal}` + Note field = queue generation
- `|` separator: `cat|dog|bird` → 3 images

**Community:** SDVN (StableDiffusion Vietnam) — `sdvn.vn`

---

## 🤖 ChatDev 2.0 (OpenBMB/ChatDev)
**Type:** Zero-Code Multi-Agent Platform for software development  
**URL:** https://github.com/OpenBMB/ChatDev

**Description:** Multi-agent platform where AI agents play different roles (CEO, CTO, Programmer, Reviewer) to collaboratively develop software from a text description.

### AI OS Learning Points
- **Role-based multi-agent system** = foundation for AI OS AGENTS.md
- Zero-code operation = democratized agent orchestration
- Academic research quality (Stanford/OpenBMB)

---

## 🔧 NanoBot (HKUDS/nanobot)
**Type:** Ultra-lightweight personal AI assistant  
**URL:** https://github.com/HKUDS/nanobot

**Features:**
- 24/7 Real-Time Market Analysis
- Full-Stack Software Engineer
- Smart Daily Routine Manager
- Personal Knowledge Assistant

*Educational/research purposes. HKUDS companion to LightRAG.*

---

## 📊 Data Engineering YouTube (darshilparmar/dataengineering-youtube-analysis-project)
**Type:** AWS data engineering pipeline tutorial project  
**URL:** https://github.com/darshilparmar/dataengineering-youtube-analysis-project

### Architecture
`YouTube Data` → `S3 (Data Lake)` → `AWS Glue (ETL)` → `Athena (Query)` → `QuickSight (BI)`

### Services Used
- Amazon S3, AWS IAM, QuickSight, AWS Glue, AWS Lambda, AWS Athena

**AI OS Learning Points:**
- Cloud ETL pipeline pattern for data processing at scale
- Tutorial: https://youtu.be/yZKJFKu49Dk (3+ hours)

---

## 🏗️ Clean Architecture Next.js (Melzar/clean-architecture-nextjs-react-boilerplate)
**Type:** Next.js boilerplate with Clean Architecture layers  
**URL:** https://github.com/Melzar/clean-architecture-nextjs-react-boilerplate

### Layers
- **Domain**: Business entities, pure logic
- **Application**: Use cases, ports
- **Infrastructure**: DB, external services  
- **Presentation**: React components, UI

**AI OS Learning Points:**
- Clean Architecture layers = AI OS module organization pattern
- SOLID principles in Next.js context

---

## 🍃 Spring Boot Best Practices Skill (mduongvandinh/springboot-best-practices)
**Type:** Agent skill for Spring Boot code review (19 domains, 3 severity levels)  
**URL:** https://github.com/mduongvandinh/springboot-best-practices

### 19 Review Domains
Architecture, Security, Performance, Database, API Design, Error Handling, Testing, Logging, Caching, Config Management, Async, Validation, Documentation, DI, Code Style, Monitoring, Build, Microservices, Green Computing

### Scoring System
- Minor violation: -1~-3 points
- Major violation: -5~-10 points  
- Critical violation: -15~-30 points
- Ranks: S/A/B/C/D (100→80→60→40→0)

**Supports:** Claude Code + Google Antigravity installation

---

## 🤖 HKUDS Nanobot — Already noted above.

---

## ➡️ SkillHub Desktop (skillhub-club/skillhub-desktop)
Skill marketplace desktop client.

## ➡️ Marketing Skills (coreyhaines31/marketingskills)
Already documented above — 35+ marketing skills for AI agents.

## ➡️ WordPress Agent Skills (WordPress/agent-skills)
Official WordPress skill library for AI agents — 404 (private/removed).

## ➡️ Munkhin Auto-Accept Agent
404 error — private or deleted.

---

*Extracted: 2026-03-16 | Method: GitHub raw README fetch | AI OS Knowledge Bank*

---

## 🔮 Antigravity-Deck (tysonnbt/Antigravity-Deck)
**Type:** Full web dashboard for Antigravity IDE — Resource Monitor, Git, Agent Bridge  
**URL:** https://github.com/tysonnbt/Antigravity-Deck  
**Stars:** 55 | **Forks:** 18 | **Language:** TypeScript  
**Status in AI OS:** ✅ CLONED → plugins/antigravity-deck/ (already present from earlier scan)

**Capabilities:**
- 💬 Full chat/conversation UI with WebSocket real-time updates
- 🖥️ Multi-workspace detection + switching (Windows/macOS/Linux)
- 🧠 Headless Language Server management (launch LS without IDE)
- 📊 Resource Monitor: CPU, RAM, Disk charts + per-workspace breakdown
- 🔀 Built-in Git: status, diffs, stage/commit/push from browser
- 🤖 Agent Bridge: Connect external agents (Pi, OpenClaw) via Discord relay
- ⚡ Cascade Control: accept/reject/cancel code changes from web UI
- 🔒 Auth + Cloudflare Tunnel for remote access

**AI OS Integration:** → Add to Service Manager dashboard (Port 4000 default)  
**Start Command:** cd plugins/antigravity-deck && npm install && npm start

---

## 🤖 AstrBot (AstrBotDevs/AstrBot)
**Type:** Agentic IM Chatbot — Telegram, QQ, Discord, Feishu + OpenAI/Gemini/LLM  
**URL:** https://github.com/AstrBotDevs/AstrBot  
**Stars:** 24,845 | **Forks:** 1,685 | **Language:** Python  
**Status in AI OS:** ✅ CLONED → plugins/AstrBot/

**Key Points:**
- OpenClaw alternative — supports QQ, WeChat, Telegram, Discord, Feishu
- Built-in plugin marketplace + MCP support
- Has web dashboard (admin panel) at localhost:6185
- Docker support + one-command install
**AI OS Role:** Alternative/complement to channels/ bridge module

---

## 🔧 gstack (garrytan/gstack)
**Type:** CEO/CTO/QA/Release Manager agent skill pack for Claude Code  
**URL:** https://github.com/garrytan/gstack  
**Stars:** 13,189 | **Forks:** 1,522 | **Language:** TypeScript  
**Status in AI OS:** ✅ CLONED → REMOTE/claws/gstack/  
**Key Points:** Garry Tan's exact Claude Code setup — 6 agents as CEO, Eng Manager, etc.  
**AI OS Role:** Skills/prompts for multi-agent orchestration patterns

---

## 🧰 antigravity-kit (vudovn/antigravity-kit)
**Type:** TypeScript toolkit/SDK for Antigravity AI  
**URL:** https://github.com/vudovn/antigravity-kit  
**Stars:** 6,132 | **Forks:** 1,211 | **Language:** TypeScript  
**Status in AI OS:** ✅ CLONED → REMOTE/claws/antigravity-kit/  
**Key Points:** Book/docs at https://2026-03-15-antigravity-kit-book.vercel.app/ — 20 agents, 37 skills, multi-agent orchestration  
**AI OS Role:** SDK patterns for building Antigravity-native applications

---

## 🎰 AntigravityManager (Draculabo/AntigravityManager)
**Type:** Electron app — multi-account manager for Gemini/Claude in Antigravity  
**URL:** https://github.com/Draculabo/AntigravityManager  
**Stars:** 1,141 | **Forks:** 155 | **Language:** TypeScript  
**Status in AI OS:** ✅ CLONED → plugins/AntigravityManager/

**Key Features:**
- Cloud account pool: unlimited Gemini/Claude accounts with OAuth
- Real-time quota monitoring with visual indicators
- Intelligent auto-switching when quota < 5%
- Local API Proxy (OpenAI + Anthropic compatible)
- AES-256-GCM encryption + OS native credential manager  
**AI OS Role:** Manage multiple Antigravity accounts + API proxy (maps Claude ↔ Gemini)

---

## 🌊 OpenViking (volcengine/OpenViking)
**Type:** Open-source context database for AI agents (OpenClaw compatible)  
**URL:** https://github.com/volcengine/OpenViking  
**Stars:** 11,924 | **Forks:** 827 | **Language:** Python  
**Status in AI OS:** ✅ CLONED → plugins/OpenViking/  
**Key Points:** Unified management of memory, resources, skills via filesystem paradigm. Has API server.  
**AI OS Role:** Context/memory DB layer for AI agents — complements knowledge/ directory

---

## 🤝 open-claude-cowork (ComposioHQ/open-claude-cowork)
**Type:** Claude Cowork with 500+ SaaS app integrations  
**URL:** https://github.com/ComposioHQ/open-claude-cowork  
**Stars:** 3,153 | **Forks:** 411  
**Status in AI OS:** ✅ CLONED → plugins/open-claude-cowork/  
**Key Points:** Electron app with Composio integration (GitHub, Slack, Linear, etc.)  
**AI OS Role:** Claude task automation with 500+ SaaS connectors

---

## 📚 pm-skills (phuryn/pm-skills)
**Type:** PM Skills Marketplace — 100+ agentic skills for product management  
**URL:** https://github.com/phuryn/pm-skills  
**Stars:** 7,134 | **Forks:** 684  
**Status in AI OS:** ✅ CLONED → knowledge/repos/pm-skills/  
**Key Points:** Skills for discovery, strategy, execution, launch, growth phases  
**AI OS Role:** PM-focused skills to expand AI OS's product management capabilities

---

## ⚡ awesome-agent-skills (VoltAgent/awesome-agent-skills)
**Type:** Curated list of 500+ agent skills for Claude Code, Codex, Antigravity, Gemini CLI  
**URL:** https://github.com/VoltAgent/awesome-agent-skills  
**Stars:** 11,346 | **Forks:** 1,059  
**Status in AI OS:** ✅ CLONED → knowledge/repos/awesome-agent-skills/  
**AI OS Role:** Skills repository — massive collection compatible with Antigravity

---

## 🔍 GitNexus (abhigyanpatwari/GitNexus)
**Type:** Zero-server browser-based code knowledge graph with Graph RAG Agent  
**URL:** https://github.com/abhigyanpatwari/GitNexus  
**Stars:** 13,806 | **Forks:** 1,612 | **Language:** TypeScript  
**Clone:** Large (15MB) — analyze only; live demo: https://gitnexus.vercel.app  
**AI OS Role:** Drop in any GitHub repo → interactive knowledge graph + AI chat about code

---

## 🧠 hindsight (vectorize-io/hindsight)
**Type:** Agent Memory That Learns — persistent memory system  
**URL:** https://github.com/vectorize-io/hindsight  
**Stars:** 3,987 | **Forks:** 279 | **Language:** Python  
**Status in AI OS:** ✅ CLONED → knowledge/repos/hindsight/  
**AI OS Role:** Persistent cross-session learning memory for AI agents

---

## 🔗 claude-openclaw-bridge (ericblue)
**Type:** Claude Code skill for relaying questions to OpenClaw agents  
**URL:** https://github.com/ericblue/claude-openclaw-bridge  
**Status in AI OS:** ✅ CLONED → knowledge/repos/claude-openclaw-bridge/  
**AI OS Role:** Bridge Claude Code → OpenClaw; one-shot queries + persistent relay mode

---

## 📋 ericblue Ecosystem (3 repos)
- **memspan** — Persistent identity/memory/conversation span for LLMs (Python)  
- **habit-sprint** — Sprint-based habit tracking engine for LLM-first workflows (Python)  
- **mac-agent-gateway** — macOS HTTP API for AI agents to access Reminders, Messages, etc. (**macOS only**)

**Status:** Knowledge analysis only (no local clone needed; macOS gateway incompatible with Windows)

---

## 🌐 Web-only Resources (not cloned)

### Superpowers Guide (Vietnamese)
**URL:** https://2026-03-15-superpowers-guide.vercel.app/  
**Content:** Vietnamese guide for 84k-star "Superpowers" tool — 14 skills workflow for Antigravity coding agents. Covers: brainstorming, writing-plans, subagent-driven-development, TDD, code-review, git-worktrees.  
**AI OS Value:** Core workflow methodology reference for multi-agent coding

### Antigravity Kit Book (Vietnamese)
**URL:** https://2026-03-15-antigravity-kit-book.vercel.app/  
**Content:** Comprehensive Vietnamese guide to Antigravity Kit — 20 agents, 37 skills, multi-agent orchestration patterns.  
**AI OS Value:** Full documentation for antigravity-kit plugin

### ByteRover Docs
**URL:** https://docs.byterover.dev/  
**Content:** Docs for ByteRover AI agents platform  
**AI OS Value:** Reference for agentic browsing capabilities

### PDF to Web Pipeline
**URL:** https://2026-03-14-pdf-to-web-pipeline.vercel.app/  
**Content:** Tool for converting PDF documents into web pages

---

## 📊 FastCode (HKUDS/FastCode)
**Type:** Code understanding acceleration tool  
**URL:** https://github.com/HKUDS/FastCode  
**Stars:** 1,935 | Paper: https://arxiv.org/abs/2603.01012  
**Clone decision:** Analyze only — academic research codebase  
**AI OS Value:** Code comprehension patterns for AI code understanding

---

## 🗂️ EventCatalog (event-catalog/eventcatalog)
**Type:** Architecture catalog for distributed systems — AI-powered documentation  
**URL:** https://github.com/event-catalog/eventcatalog  
**Stars:** 2,594 | **Language:** TypeScript  
**Clone decision:** Analyze only — documentation tool for distributed systems  
**AI OS Value:** Pattern for documenting AI OS's own event-driven architecture

---

## 🐦 TikTokDownloader (JoeanAmier/TikTokDownloader)
**Type:** TikTok/Douyin data collection + download tool  
**URL:** https://github.com/JoeanAmier/TikTokDownloader  
**Stars:** 13,519 | **Language:** Python  
**Clone decision:** Optional — media download utility, not core AI OS function  
**AI OS Value:** Media scraping capability if needed for content tasks

---

## 📒 unslothai/notebooks
**Type:** Unsloth training notebooks (Llama, Mistral, etc.)  
**URL:** https://github.com/unslothai/notebooks  
**Clone decision:** Reference only — Jupyter notebooks for LLM fine-tuning  
**AI OS Value:** LLM training patterns and fine-tuning techniques

---

## 🚀 ShipSwift (signerlabs/ShipSwift)
**Type:** AI-native SwiftUI component library with MCP integration  
**URL:** https://github.com/signerlabs/ShipSwift  
**Stars:** 1,118 | **Language:** Swift (iOS/macOS only)  
**Clone decision:** No — macOS/iOS only, not relevant for Windows-based AI OS  
**AI OS Value:** Reference for SwiftUI + MCP integration patterns


---

## 📚 learn-claude-code (shareAI-lab/learn-claude-code)
**Type:** Nano Claude Code-like agent built from scratch — educational, 0→1 tutorial  
**URL:** https://github.com/shareAI-lab/learn-claude-code  
**Stars:** 27,748 ⭐ | **Forks:** 4,864 | **Language:** TypeScript  
**Status in AI OS:** ✅ CLONED → `knowledge\repos\learn-claude-code`  
**Key Points:**  
- Teaches exactly how Claude Code agents work internally (tool loop, message history, shell execution)
- 3 learning paths: Beginner (Bash shell agent) → Intermediate (TypeScript) → Advanced (tool calling)
- Sister repos: Kode Agent CLI + Kode Agent SDK — production-ready open-source Claude Code alternative
- Web platform at https://learn.shareai.run
**AI OS Role:** Core reference for understanding Antigravity/Claude Code architecture. Invaluable for building new AI OS agent tools.

---

## 🔭 agentsview (wesm/agentsview)
**Type:** Desktop + web app for browsing, searching, analyzing AI agent coding sessions  
**URL:** https://github.com/wesm/agentsview  
**Stars:** 517 | **Language:** Go | **Author:** Wes McKinney (creator of pandas)  
**Status in AI OS:** ✅ CLONED → `knowledge\repos\agentsview`  
**Supported Agents:** Claude Code, Codex, OpenCode, Antigravity, Gemini CLI, Cursor, Copilot + 4 more  
**Key Features:**
- Browse all AI agent sessions from any supported tool
- Search across conversations, filter by agent type
- Analyze token usage, session duration, code changes
- Desktop app + web UI at http://localhost:port
**AI OS Role:** → Add to Service Manager. Monitor all your AI coding sessions in one place.

---

## 💬 openchatbi (zhongyu09/openchatbi)
**Type:** Chat-based BI tool — Natural Language → SQL → Data Visualization  
**URL:** https://github.com/zhongyu09/openchatbi  
**Stars:** 527 | **Language:** Python  
**Status in AI OS:** ✅ CLONED → `knowledge\repos\openchatbi`  
**Tech Stack:** LangGraph + LangChain + PostgreSQL/MySQL/BigQuery  
**Key Features:**
- Ask questions in natural language → get SQL + charts
- Supports multiple databases and data warehouses
- Built-in LangGraph workflow for query validation
**AI OS Role:** If AI OS needs to query databases, this is the pattern to follow.

---

## 🖥️ tui-studio (jalonsogo/tui-studio)
**Type:** Visual design tool for building Terminal User Interfaces (TUI)  
**URL:** https://github.com/jalonsogo/tui-studio  
**Stars:** 670 | **Language:** TypeScript  
**Clone decision:** Analyze only — design tool, no runnable server  
**Key Features:**
- Drag-and-drop visual TUI builder
- Export to multiple TUI frameworks (Ink, Textual, Bubbletea, etc.)
- Keyboard shortcut-driven interface
**AI OS Role:** Reference for designing beautiful terminal dashboards and TUI components in AI OS

---

## 🦀 temm1e (nagisanzenin/temm1e)
**Type:** Autonomous AI agent runtime built in Rust — "Sentient and Immortal"  
**URL:** https://github.com/nagisanzenin/temm1e  
**Stars:** 285 | **Language:** Rust | **Homepage:** https://skyclaw.vn/  
**Status in AI OS:** CLONE → `knowledge\repos\temm1e`  
**Specs:** 69K lines · 1,509 tests · 0 warnings · 0 panic paths · 15 MB idle · 31ms cold start  
**Key Concept:**
- Finite brain model with procedural memory via "Blueprints"
- Deploy once, stays up forever — production-grade agent daemon
- Ultra-lightweight and fast (31ms cold start!)
**AI OS Role:** Future reference for building persistent always-on AI agent daemons. Architecture pattern for production agent deployment.

---

## �� nagisanzenin Plugin Suite (3 plugins)
**Author:** nagisanzenin | **Status in AI OS:** ✅ CLONED → `knowledge\repos\nagisanzenin\`

### claude-code-skill-maker-plugin
- Creates new Claude Code skills and plugins end-to-end
- Automated packaging and marketplace publishing
- **AI OS Role:** Use to auto-generate new skills for AI OS skill registry

### claude-code-software-engineer-plugin  
- Production-grade service implementation with clean architecture
- Payment integration + autonomous debugging patterns
- **AI OS Role:** Reference for building production services with AI

### claude-code-production-grade-plugin (115⭐)
- Fully autonomous production-grade SaaS pipeline
- 14 bundled skills: CEO/CTO command-driven development
- Single install → full development lifecycle
- **AI OS Role:** Command patterns for autonomous SaaS delivery from AI OS

---

## 💻 Warp (warpdotdev/Warp)
**Type:** Agentic development environment / AI-powered terminal  
**URL:** https://github.com/warpdotdev/Warp  
**Stars:** 26,123 | **Language:** Rust (closed source) | **Platforms:** macOS, Linux, Windows  
**Clone decision:** ❌ NOT cloneable — issues-only public repo (actual source is closed)  
**Product:** Download from https://warp.dev

**Key Features:**
- AI terminal with multi-agent support (can run multiple AI agents in parallel)
- Built-in Claude Code, Codex, Antigravity and other agent integrations
- Natural language commands → shell scripts
- Collaborative workflows: share terminal sessions, blocks, notebooks
- AI-powered autocomplete, inline docs, debugging

**Why it matters for AI OS:**
- Warp is essentially a **visual shell around AI agents** — exactly what our Service Manager is building toward
- Architecture inspiration: multi-agent pane management, agent status indicators, session persistence
- Integration target: AI OS could display Warp notification webhooks in LobsterBoard
- Windows support is NOW available (was macOS-only previously)

**AI OS Role:** Reference product for AI OS terminal integration design. Not cloneable but essential knowledge for designing the AI OS dashboard and agent orchestration UI.

---

## 🗂️ gsd-2 (gsd-build/gsd-2)
**Type:** Meta-prompting + Context Engineering + Spec-Driven Development system  
**URL:** https://github.com/gsd-build/gsd-2  
**Stars:** 1,317 | **Language:** TypeScript  
**Status in AI OS:** ✅ CLONED → `knowledge\repos\gsd-2`  
**Install:** `npm install -g gsd-pi`  
**Topics:** context-engineering, meta-prompting, spec-driven-development

**Key Concept:** Enables AI agents to work autonomously for long periods without losing track of the big picture. Uses meta-prompting to maintain persistent context engineering and spec awareness.

**Key Features:**
- Agents maintain context + "big picture" across long autonomous sessions
- Spec-driven: AI follows formal specs instead of improvising
- Context engineering toolkit for multi-session agent workflows
**AI OS Role:** ⭐ VERY RELEVANT — Architecture for long-running AI OS sessions with persistent context. Should be studied and incorporated into AI OS's agent loop design.

---

## ��️ tmux-ide (wavyrai/tmux-ide)
**Type:** tmux-powered terminal IDE via simple `ide.yml` config  
**URL:** https://github.com/wavyrai/tmux-ide (403 on API — may be private or renamed)  
**README was accessible directly**  
**Install:** `npm install -g tmux-ide`  
**Requirements:** tmux >= 3.0, Node.js >= 18

**Key Features:**
- Define your IDE layout in a simple YAML file (panes, rows, commands, sizes)
- Auto-detect project stack (Next.js, Vite, Python, Go, Convex...)
- Launch full IDE with one command: `tmux-ide`
- Built-in templates: nextjs, vite, python, go, convex
- Commands: start/stop/restart/attach/status/doctor

**Example Use in AI OS:**
`yaml
name: ai-os-dev
rows:
  - panes:
      - title: Antigravity    # AI coding agent
      - title: Service Manager # Flask API
  - panes:
      - title: Logs
        command: tail -f logs/ai_os.log
      - title: Shell
`
**AI OS Role:** Ideal for setting up the AI OS development environment as a one-command tmux workspace

---

## 🦞 OpenClaw Command Center (jontsai/openclaw-command-center)
**Type:** Full web dashboard for OpenClaw agents — sessions, memory, cost, cron jobs  
**URL:** https://github.com/jontsai/openclaw-command-center  
**Status in AI OS:** ✅ CLONED → plugins\openclaw-command-center  
**Start:** 
ode lib/server.js → Dashboard at **http://localhost:3333** 🎉  
**Quick Install:** 
px clawhub@latest install command-center

**Features:**
| Feature | Description |
|---|---|
| 📊 Session Monitoring | Real-time view of active AI sessions |
| ⛽ LLM Fuel Gauges | Token usage, costs, quota remaining |
| 💻 System Vitals | CPU, memory, disk, temperature |
| ⏰ Cron Jobs | View and manage scheduled tasks |
| 🧠 Cerebro Topics | Automatic conversation tagging |
| 👥 Operators | Who's talking to your agents |
| 📝 Memory Browser | View agent memory files |
| 💰 Cost Breakdown | Detailed per-model cost analysis |

**Zero Config:** Auto-detects OpenClaw workspace via env var or common paths  
**Requirements:** Node.js only  
**AI OS Role:** ⭐ ADD TO SERVICE MANAGER — Best OpenClaw-specific dashboard available. Complements LobsterBoard with OpenClaw-specific metrics.

---

## 🌐 my-translator (phuc-nt/my-translator)
**Type:** Speech translator app — Cloud (Soniox) + Local (MLX on Apple Silicon)  
**URL:** https://github.com/phuc-nt/my-translator  
**Status in AI OS:** ✅ CLONED → knowledge\repos\my-translator  
**Clone decision:** Analysis only — macOS/Apple Silicon app, not runnable on Windows  
**AI OS Role:** Pattern reference for building real-time speech translation in AI OS (future: Vietnamese voice commands)

---

## 🤝 agent-teams-lite (Gentleman-Programming/agent-teams-lite)
**Type:** Multi-agent orchestration system — orchestrator + specialized sub-agents  
**URL:** https://github.com/Gentleman-Programming/agent-teams-lite  
**Status in AI OS:** ✅ CLONED → knowledge\repos\agent-teams-lite  
**Key Points:**
- Orchestrator + specialized sub-agents for structured feature development
- Zero dependencies — Pure Markdown format
- Works with any AI coding tool (Claude Code, Antigravity, Codex, Cursor...)
**AI OS Role:** Agent orchestration patterns for AI OS's multi-agent workflows. Study and adapt into AI OS's agent coordination system.

---

## 🗺️ FieldTrip (event-catalog/fieldtrip)
**Type:** Schema explorer — search, visualize every field across OpenAPI/AsyncAPI/Protobuf/Avro/JSON  
**URL:** https://github.com/event-catalog/fieldtrip  
**Status in AI OS:** ✅ CLONED → `knowledge\repos\event-catalog\fieldtrip`  
**Quick Start:** `npx @eventcatalog/fieldtrip --dir ./schemas` → **http://localhost:3200**

**3 Views:**
- 📋 **Table View** — Full-text search + filter by schema type, click to see full schema
- 🔲 **Matrix View** — Heatmap: which properties appear in which schemas (green=required, blue=optional)
- 🕸️ **Graph View** — D3.js force-directed visualization of schema relationships

**Supported Formats:** OpenAPI, AsyncAPI, Protobuf (.proto), Avro (.avsc), JSON Schema

**AI OS Role:** → Add to Service Manager. Extremely useful for exploring AI OS's own API schemas. Run against `knowledge/repos/` folder to map all schema relationships across 150+ ingested repos.
