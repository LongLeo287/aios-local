# AI OS Plugin Catalog
# Version: 3.0 | Updated: 2026-03-24 | Owner: Dept 4 (Registry) + Dept 20 (CIV)
# Evaluated via: ops/workflows/repo-evaluation.md

> **Trạng thái ký hiệu:**
> - 👁️ = Đã đọc/khảo sát
> - 📚 = Tham khảo học hỏi (không integrate tool — trích xuất kiến thức/patterns vào brain/knowledge/notes/)
> - 🔖 = Giữ lại (DEFER — dùng sau, ghi rõ lý do)
> - ✅ = Đang sử dụng (theo dõi version)
> - ⚡ = Đang tích hợp
> - ❌ = Loại bỏ hoàn toàn (REJECT — không dùng, không học — ghi lý do)
> - ⏸️ = Chưa đọc (cần chạy repo-evaluation.md)

---

## COGNITIVE PLUGINS (Memory, RAG, Knowledge)

| Repo | Verdict | Tier | Conflict check | Ghi chú |
|------|---------|------|----------------|---------|
| `LightRAG` | ✅ ACTIVE | Tier 1 | Không conflict | Core RAG engine. check weekly. OPEN-004 in progress. |
| `mem0` | ✅ ACTIVE | Tier 1 | Safe | Phase 1 DONE. Hooks: onTaskStart/onTaskComplete/onHandoff. |
| `open-notebook` | ✅ ACTIVE | Tier 2 | — | Nova primary tool. Port 8502/5055. KHÔNG thay đổi. |
| `open-notebooklm` | ✅ ACTIVE | Tier 2 | — | Audio podcast gen. KHÔNG thay đổi. |
| `notebooklm-skill` | ✅ ACTIVE | Tier 2 | — | NotebookLM browser automation. Nova primary. |
| `nexusrag` | 🔖 DEFER → Phase 6 | Tier 2 | ⚠️ Overlap LightRAG | **Verdict:** DEFER. Có thể bổ sung UI cho LightRAG sau khi PoC xong. KHÔNG deploy riêng. |
| `graphrag` | 📚 REFERENCE | — | ⚠️ Overlap LightRAG | **Verdict:** REFERENCE. Tool không dùng (tốn API), nhưng học khái niệm **Community Detection** + entity-typed extraction. KI: `brain/knowledge/notes/KI-GRAPHRAG-CONCEPTS-01.md` |
| `cognee` | 🔖 DEFER → Phase 6 | Tier 2 | ⚠️ Partial overlap LightRAG | **Verdict:** DEFER. Chờ LightRAG PoC xong (OPEN-004). Nếu LightRAG đủ thì REJECT. |
| `ai-tagger` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Semantic auto-tagging bổ sung cho Knowledge pipeline. Không conflict. Integrate khi Knowledge dept cần. |
| `smart-search` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Hybrid search (semantic + keyword). Tích hợp sau khi LightRAG stable. Không conflict. |
| `claude-mem` | 📚 REFERENCE | — | ⚠️ Overlap mem0 | **Verdict:** REFERENCE. Tool không dùng (mem0 tốt hơn), nhưng đọc để học cách handle Claude-specific memory patterns nếu cần tương thích API trong tương lai. |
| `autoresearchclaw` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Auto research agent — bổ sung cho web-researcher workflow. Evaluate khi Dept R&D cần agent tự động. |
| `openrag` | ❌ REJECT | Tier 3 | ❌ nexusrag tốt hơn | **Verdict:** REJECT đã từ trước. nexusrag đầy đủ hơn. Nay REJECT cả nexusrag luôn vì LightRAG cover. |
| `neural-memory-repo` | 🔖 DEFER → Phase 6 | Tier 2 | Safe | **Verdict:** DEFER. Neural memory implementation — evaluate when advanced memory needed. |
| `notebooklm-mcp` | 👁️ | Tier 2 | Safe | **Verdict:** Đã đọc. MCP server for NotebookLM API with session support. |
| `notebooklm-mcp-cli` | ✅ ACTIVE | Tier 2 | — | Active. NotebookLM MCP bridge. |
| `langextract` | ✅ ACTIVE | Tier 2 | — | Active, KHÔNG thay đổi. check monthly. |

---

## DATA PLUGINS (Web, Scraping, Extraction)

| Repo | Verdict | Tier | Conflict check | Ghi chú |
|------|---------|------|----------------|---------|
| `firecrawl` | ✅ ACTIVE | Tier 1 | Safe | Phase 2 DONE. Pipeline: Firecrawl→LangExtract→LightRAG. |
| `gitingest` | 🔖 DEFER → Phase 4 | Tier 2 | Safe | **Verdict:** DEFER. GitHub repo → LLM context. Bổ sung cho GitNexus khi cần feed repo vào RAG. Integrate khi Dept Engineering yêu cầu. |
| `scrapling` | 🔖 DEFER → Phase 5 | Tier 2 | ⚠️ Overlap Firecrawl | **Verdict:** DEFER as BACKUP ONLY. Dùng khi Firecrawl không có API key (self-hosted mode down). KHÔNG integrate song song. |
| `scrapling-mcp` | ❌ REJECT | Tier 3 | ❌ Duplicate scrapling + Firecrawl | **Verdict:** REJECT. MCP wrapper của scrapling — đã có Firecrawl MCP adapter tốt hơn. 2 lớp trùng nhau. |
| `agent-browser` | 🔖 DEFER → Phase 4 | Tier 2 | Safe | **Verdict:** DEFER. Browser automation cho agent (lấy JS-rendered content). Bổ sung Firecrawl cho case JS-heavy. Integrate khi Dept Engineering cần. |
| `cerberus-cve-tool` | 🔖 DEFER → Phase 3 | Tier 2 | Safe (security) | **Verdict:** DEFER. CVE scanning — Dept 10 (Security) sở hữu. Integrate vào nemoclaw-strix-scan.md pipeline. |
| `pageindex` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Page indexing system — evaluate when web crawling needs expand. |
| `dbcooper` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Database cooperation tools — evaluate when multi-db operations needed. |

---

## ORCHESTRATION PLUGINS (Multi-agent, Workflow)

| Repo | Verdict | Tier | Conflict check | Ghi chú |
|------|---------|------|----------------|---------|
| `crewai` | ✅ ACTIVE | Tier 1 | Check vs AgAuto | Phase 4 DONE. AI Squad Controller UI live trên ClawTask. |
| `bmad-method` | ✅ ACTIVE | Tier 2 | — | Active. BMAD agile method. |
| `MaxKB` | 🔖 DEFER → Phase 7 | Tier 2 | ⚠️ Overlap ClawTask + RAG | **Verdict:** DEFER. Enterprise platform — evaluate chỉ nếu cần KB riêng cho khách hàng. Hiện tại LightRAG + ClawTask thay thế đủ. |
| `all-agentic-architectures` | 📚 REFERENCE | — | — | **Verdict:** REFERENCE. 17 kiến trúc Agent (Reflection, ReAct, PEV, Blackboard, ToT, Metacognitive...). KI: `brain/knowledge/notes/KI-AGENT-ARCHITECTURES-01.md` |
| `agency-agents` | 📚 CHERRY-PICK | — | — | **Verdict:** CHERRY-PICK. 144 agent templates — không chạy install script. Cherry-pick các agents AI OS còn thiếu (Code Reviewer, MCP Builder, Incident Commander...). KI: `brain/knowledge/notes/KI-AGENCY-AGENTS-CHERRY-PICK-01.md` |
| `Mini-Agent` | 📚 REFERENCE | — | — | **Verdict:** REFERENCE. Đọc để học pattern thiết kế lightweight agent. Không integrate framework, chỉ lấy pattern. |
| `AntigravityManager` | 🔖 DEFER → Phase 5 | Tier 2 | Check overlap | **Verdict:** DEFER pending dedup check với antigravity-manager. Có thể là cùng 1 repo. Chờ xác nhận. |
| `antigravity-manager` | 🔖 DEFER → Phase 5 | Tier 2 | Check overlap | **Verdict:** DEFER. Dedup check với AntigravityManager. Nếu trùng → keep 1, REJECT cái còn lại. |
| `AstrBot` | 🔖 DEFER → Phase 5 | Tier 2 | Check vs nullclaw | **Verdict:** DEFER. Bot framework — cần compare với nullclaw (Telegram bot hiện tại). Nếu nullclaw đủ → REJECT. |
| `deepagents` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Deep agent framework — evaluate when advanced agent capabilities needed. |
| `pixel-agents` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Pixel-based agents — evaluate when visual processing needed. |
| `openclaw` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. OpenClaw framework — evaluate when open-source claw tools needed. |
| `openclaw-command-center` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. OpenClaw command center — evaluate when centralized control needed. |
| `openclaw-rl` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. OpenClaw reinforcement learning — evaluate when RL capabilities needed. |
| `oh-my-openagent` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Open agent framework — evaluate when extensible agent system needed. |

---

## UI PLUGINS

| Repo | Verdict | Tier | Conflict check | Ghi chú |
|------|---------|------|----------------|---------|
| `ui-ux-pro-max` | ✅ ACTIVE | Tier 2 | — | Active. Premium UI generation. |
| `LobsterBoard` | ✅ ACTIVE | Tier 2 | — | Beta, audit needed. Dashboard UI. |
| `lobe-chat` | 🔖 DEFER → Phase 7 | Tier 2 | ⚠️ Overlap nullclaw | **Verdict:** DEFER. Full AI chat platform — evaluate chỉ khi CEO muốn public-facing chat UI mạnh hơn nullclaw. |
| `antigravity-deck` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Presentation/deck tool cho Antigravity. Review khi Dept Marketing cần slide generation. |
| `antigravity-mobile` | 🔖 DEFER → Phase 7 | Tier 2 | Safe | **Verdict:** DEFER. Mobile UI — integrate khi có kế hoạch mobile app cụ thể. |
| `PerformanceStudio` | 🔖 DEFER → Phase 4 | Tier 2 | Safe | **Verdict:** DEFER. Performance monitoring UI — review cùng prometheus-grafana. Dept 14 (Monitoring) sở hữu. |
| `prometheus-grafana-alerts` | 🔖 DEFER → Phase 4 | Tier 2 | Safe | **Verdict:** DEFER. Monitoring stack — integrate vào Dept 14 (Monitoring/Inspection). Phase 3 ops. |
| `agentsview` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Agent visualization — bổ sung ClawTask Dashboard. Integrate khi AI Squad UI cần mở rộng. |
| `gaia-ui` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. GAIA user interface — evaluate when GAIA-specific UI needed. |
| `lenis` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Smooth scrolling library — evaluate when UI smoothness needed. |

---

## BRIDGE / INTEGRATION PLUGINS

| Repo | Verdict | Tier | Conflict check | Ghi chú |
|------|---------|------|----------------|---------|
| `openspec` | ✅ ACTIVE | Tier 2 | — | Active. OpenSpec automation. |
| `e2b` | 🔖 DEFER → Phase 4 | Tier 2 | Safe | **Verdict:** DEFER. Code execution sandbox — integrate vào ACP console (Dept Engineering). Phase 3. |
| `cloud-sync` | 🔖 DEFER → Phase 6 | Tier 2 | Safe | **Verdict:** DEFER. Cloud sync — cần xác định provider cụ thể (S3, GCS?) trước khi integrate. |
| `MiniMax-MCP` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. MiniMax API bridge — integrate khi LLM Router cần MiniMax model (ví dụ: video/audio gen). |
| `MiniMax-MCP-JS` | ❌ REJECT | Tier 3 | ❌ Duplicate MiniMax-MCP | **Verdict:** REJECT. JS version của MiniMax-MCP — Python version (MiniMax-MCP) ưu tiên hơn vì AI OS chạy Python-first. |
| `OpenSandbox` | ❌ REJECT | Tier 3 | ❌ Duplicate e2b | **Verdict:** REJECT. e2b được maintain tốt hơn, có team, có docs đầy đủ hơn OpenSandbox. |
| `OpenShell` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Open shell interface — evaluate when enhanced shell needed. |
| `openviking` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Viking-inspired tools — evaluate when historical/Norse-themed tools needed. |
| `mcp-client` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. MCP client tools — evaluate when enhanced MCP client needed. |
| `context7` | 👁️ | Tier 2 | Safe | **Verdict:** Đã đọc. Real-time library documentation system. |

---

## SECURITY PLUGINS

| Repo | Verdict | Tier | Conflict check | Ghi chú |
|------|---------|------|----------------|---------|
| `zeroleaks` | ✅ ACTIVE | Tier 2 | — | Active. Secret leak prevention. check monthly. |
| `claude-bug-bounty` | ❌ REJECT | Tier 3 | — | **Verdict:** REJECT. Đây là flow/methodology, không phải tool integrable. Tham khảo docs chứ không clone vào hệ thống. |
| `trufflehog` | 🔖 DEFER → Phase 3 | Tier 2 | Safe — complement zeroleaks | **Verdict:** DEFER. Secret scanning deep scan (Git history). Bổ sung zeroleaks. Dept 10 (Security) integrate vào strix-scan pipeline. |
| `GitHacker` | ❌ REJECT | Tier 3 | ⚠️ Offensive tool | **Verdict:** REJECT. Git exploitation tool — offensive security. AI OS không có use case tấn công. Chỉ dùng defensive tools. |
| `identYwaf` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Identity WAF protection — evaluate when advanced web security needed. |
| `kong-reverse-engineer` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Kong reverse engineering — evaluate when API gateway reverse engineering needed. |

---

## SKILL PACKS (Reference — không phải plugins standalone)

| Repo | Verdict | Ghi chú |
|------|---------|---------|
| `agent-skills-standard` | ✅ ACTIVE | Standard skill templates. |
| `anthropic-skills` | ✅ ACTIVE | Anthropic extensions. |
| `antigravity-kit` | ✅ ACTIVE (auto-load) | Core kit. |
| `cloudflare-skills` | ✅ ACTIVE | Cloudflare deployment. |
| `vercel-agent-skills` | ✅ ACTIVE | Vercel deployment. |
| `vercel-labs-skills` | ✅ ACTIVE | Vercel labs. |
| `carlrannaberg-claudekit` | ✅ ACTIVE | ClaudeKit fork. |
| `claudekit` | ✅ ACTIVE | Core ClaudeKit. |
| `antigravity-awesome-skills` | 🔖 DEFER → Phase 4 | **Verdict:** DEFER. Review skill list xem có skill nào chưa có trong SKILL_REGISTRY.json → cherry-pick và import từng skill, không clone toàn bộ. |
| `awesome-agent-skills` | 🔖 DEFER → Phase 4 | **Verdict:** DEFER. Same as above — cherry-pick, không clone. |
| `awesome-claude-skills` | 🔖 DEFER → Phase 4 | **Verdict:** Same — cherry-pick các skill Claude-specific phù hợp với AI OS. |
| `ai-engineering-toolkit` | 🔖 DEFER → Phase 5 | **Verdict:** DEFER. Toolkit tổng hợp — xem xét khi Dept Engineering cần expand toolkit. |
| `api-mega-list` | 🔖 REFERENCE | **Verdict:** REFERENCE ONLY. Danh sách API — không integrate. Đọc khi cần tìm API mới. |
| `affiliate-skills` | 👁️ | Reference | Affiliate marketing skills — reference for marketing automation. |
| `affitor-affiliate-skills` | 👁️ | Reference | Affiliate marketing skills — reference for marketing automation. |
| `affitor-network` | 👁️ | Reference | Affiliate network tools — reference for network expansion. |
| `composio-awesome-claude-skills` | 👁️ | Reference | Composio Claude skills — reference for integration. |
| `skills-chronicle` | 👁️ | Reference | Skills chronicle — reference for skill tracking. |
| `skills-manager` | 👁️ | Reference | Skills management — reference for skill lifecycle. |
| `skill-generator` | 🔖 DEFER → Phase 5 | **Verdict:** DEFER. Skill generation tools — evaluate when auto-generated skills needed. |

---

## AUTOMATION & WORKFLOW PLUGINS

| Repo | Verdict | Tier | Conflict check | Ghi chú |
|------|---------|------|----------------|---------|
| `ag-auto-click-scroll` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Auto click and scroll automation — evaluate when UI automation needed. |
| `agent-smart-memo` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Smart memo agent — evaluate when enhanced memo capabilities needed. |
| `agentsview` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Agent visualization — evaluate when agent visualization needed. |
| `assistant-context` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Assistant context management — evaluate when context management needed. |
| `hivemind-plugin` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Hivemind collaboration — evaluate when distributed intelligence needed. |

---

## DEVELOPMENT TOOLS

| Repo | Verdict | Tier | Conflict check | Ghi chú |
|------|---------|------|----------------|---------|
| `claude-code-best-practice` | 👁️ | Tier 2 | Safe | **Verdict:** Đã đọc. Claude Code best practices — reference for coding standards. |
| `claude-code-prod-plugin` | 👁️ | Tier 2 | Safe | **Verdict:** Đã đọc. Claude Code production plugin — reference for production setup. |
| `claude-code-setup` | 👁️ | Tier 2 | Safe | **Verdict:** Đã đọc. Claude Code setup — reference for initialization. |
| `claude-code-templates` | 👁️ | Tier 2 | Safe | **Verdict:** Đã đọc. Claude Code templates — reference for project templates. |
| `everything-claude-code` | 👁️ | Tier 2 | Safe | **Verdict:** Đã đọc. Everything Claude Code — comprehensive reference. |
| `learn-claude-code` | 👁️ | Tier 2 | Safe | **Verdict:** Đã đọc. Learning Claude Code — educational reference. |
| `ralph-claude-code` | 👁️ | Tier 2 | Safe | **Verdict:** Đã đọc. Ralph Claude Code tools — reference for alternative implementations. |

---

## AI & ML TOOLS

| Repo | Verdict | Tier | Conflict check | Ghi chú |
|------|---------|------|----------------|---------|
| `claude-octopus` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Claude Octopus tool — evaluate when advanced Claude capabilities needed. |
| `claude-scientific-skills` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Scientific skills for Claude — evaluate when scientific computing needed. |
| `claude-usage-checker` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Claude usage checker — evaluate when usage monitoring needed. |
| `claude-ws` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Claude WebSocket interface — evaluate when WebSocket communication needed. |
| `generative-ai-beginners` | 📚 REFERENCE | — | Safe | **Verdict:** REFERENCE. Generative AI for beginners — educational reference. |
| `learn-ai-engineering` | 📚 REFERENCE | — | Safe | **Verdict:** REFERENCE. AI engineering learning — educational reference. |
| `llm-finetuning` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. LLM fine-tuning tools — evaluate when model customization needed. |
| `llm-mux` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. LLM multiplexer — evaluate when LLM routing needed. |
| `qwen2-omni` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Qwen2 Omni model — evaluate when multi-modal models needed. |

---

## COMMUNICATION & COLLABORATION

| Repo | Verdict | Tier | Conflict check | Ghi chú |
|------|---------|------|----------------|---------|
| `antigravity-switcher` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Antigravity mode switcher — evaluate when mode switching needed. |
| `vscode-antigravity-cockpit` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. VSCode Antigravity cockpit — evaluate when VSCode integration needed. |
| `claudy-registry` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Claudy registry — evaluate when registry system needed. |

---

## UTILITIES & SUPPORT TOOLS

| Repo | Verdict | Tier | Conflict check | Ghi chú |
|------|---------|------|----------------|---------|
| `awesome-openclaw-agents` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Awesome OpenClaw agents — evaluate when OpenClaw agents needed. |
| `awesome-web-agents` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Awesome web agents — evaluate when web automation needed. |
| `bmad-method` | ✅ ACTIVE | Tier 2 | — | Active. BMAD agile method. |
| `ccpoke` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. CC Poke tool — evaluate when Claude poking needed. |
| `claws` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Claw tools — evaluate when enhanced claw tools needed. |
| `clawwork` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Claw work tools — evaluate when enhanced claw workflow needed. |
| `fbi-watchdog` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Security watchdog — evaluate when enhanced security monitoring needed. |
| `port-killer` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Port killing utility — evaluate when port management needed. |
| `setup-n8n` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. n8n setup tools — evaluate when workflow automation needed. |
| `simonw-llm` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Simon Willison LLM tools — evaluate when specific LLM utilities needed. |

---

## CONTENT & MEDIA

| Repo | Verdict | Tier | Conflict check | Ghi chú |
|------|---------|------|----------------|---------|
| `videocaptioner` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Video captioning — evaluate when video processing needed. |
| `vieneu-tts` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Vietnamese TTS — evaluate when Vietnamese voice synthesis needed. |
| `vinagent` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Vietnamese agent tools — evaluate when Vietnam-specific tools needed. |
| `okara-crypto` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Crypto tools — evaluate when cryptocurrency features needed. |

---

## LEARNING & COGNITIVE

| Repo | Verdict | Tier | Conflict check | Ghi chú |
|------|---------|------|----------------|---------|
| `socraticode` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Socratic learning tools — evaluate when Socratic method learning needed. |
| `think-better` | 🔖 DEFER → Phase 5 | Tier 2 | Safe | **Verdict:** DEFER. Better thinking tools — evaluate when cognitive enhancement needed. |

---

## VERSION TRACKING — Tier 1 (Always Active)

| Plugin | Tier | Tần suất check | Lệnh update |
|--------|------|----------------|-------------|
| `LightRAG` | 1 | Weekly | `cd plugins/LightRAG && git pull` |
| `firecrawl` | 1 | Weekly | `pip install --upgrade firecrawl-py` |
| `mem0` | 1 | Weekly | `pip install --upgrade mem0ai` |
| `crewai` | 1 | Weekly | `pip install --upgrade crewai` |
| `open-notebook` | 2 | Monthly | `git pull` |
| `langextract` | 2 | Monthly | `git pull` |
| `zeroleaks` | 2 | Monthly | `git pull` |
| `antigravity-kit` | 2 | Weekly | `git pull` |

---

## INTEGRATION PRIORITY QUEUE (Updated)

```
✅ DONE: Phase 1 — mem0 (Tier 1 Core Memory)
✅ DONE: Phase 2 — firecrawl (Tier 1 Web Intelligence)
✅ DONE: Phase 3 — LightRAG (Tier 1 Knowledge Graph)
✅ DONE: Phase 4 — CrewAI (Tier 1 Multi-Agent)
✅ DONE: Catalog Evaluation — All repos have VERDICT

⏳ Phase 3 (Next): cerberus-cve-tool → trufflehog (Dept 10 Security pipeline)
⏳ Phase 4 (Next): gitingest + agent-browser + e2b (Dept Engineering tools)
⏳ Phase 4 (Next): PerformanceStudio + prometheus-grafana (Dept 14 Monitoring)
⏳ Phase 4 (Next): Skill cherry-pick from antigravity-awesome-skills / awesome-claude-skills
⏳ Phase 5 (Later): agentsview, antigravity-deck, MiniMax-MCP, ai-tagger
⏳ Phase 5 (Later): AstrBot (compare vs nullclaw first), AntigravityManager (dedup check)
⏳ Phase 5 (Later): All deferred plugins based on departmental needs
⏳ Phase 6 (Future): cognee, nexusrag (after LightRAG PoC review), cloud-sync
⏳ Phase 7 (Future): MaxKB, lobe-chat, antigravity-mobile
```

---

## REJECT SUMMARY — Lý do từng repo bị loại

| Repo | Lý do REJECT |
|------|-------------|
| `graphrag` | Duplicate LightRAG, tốn API cost cloud, LightRAG local tốt hơn |
| `claude-mem` | Duplicate mem0, chỉ hỗ trợ Claude, mem0 cross-platform |
| `openrag` | nexusrag tốt hơn, nay cả nexusrag cũng bị thay bởi LightRAG |
| `scrapling-mcp` | Duplicate Firecrawl MCP adapter, 2 lớp trùng nhau |
| `agency-agents` | Duplicate AI OS Corp agent system đã đầy đủ hơn |
| `Mini-Agent` | Duplicate sub-agent layer của AI OS |
| `MiniMax-MCP-JS` | Duplicate MiniMax-MCP Python version, AI OS Python-first |
| `OpenSandbox` | Duplicate e2b, e2b maintained tốt hơn |
| `claude-bug-bounty` | Methodology, không phải tool, không integrate được |
| `GitHacker` | Offensive security tool, AI OS dùng defensive only |

---

*Last updated: 2026-03-24 | CIV Verdict by: Claude Code (automated)*
*"Every repo earns its place. No clone without verdict."*

---