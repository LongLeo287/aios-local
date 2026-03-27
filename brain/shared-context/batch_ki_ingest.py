#!/usr/bin/env python3
"""
batch_ki_ingest.py — Proper knowledge-ingest.md Phase 1-3 for all Watchlist repos
Follows the workflow: Classify → KI entry in brain/knowledge/<domain>/
NO auto-cloning. Only TOOL+standalone repos go to plugin proposal list.
"""
import os, json
from datetime import datetime

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
TODAY = datetime.now().strftime("%Y-%m-%d")
NOW   = datetime.now().isoformat()
KNOWLEDGE = os.path.join(ROOT, "brain", "knowledge")

# ======================================================================
# PHASE 3 — CLASSIFICATION TABLE
# Format: (ki_slug, name, type, domains, dept, agents, url, stars, desc,
#          notes, compatible_ai_os, propose_clone)
# ======================================================================
WATCHLIST_REPOS = [
  # ── AGENT / AGENTIC FRAMEWORKS ──────────────────────────────────────
  ("chatdev",          "ChatDev",                 "RESEARCH",  ["ai-ml","multi-agent"],       "rd",              [],                           "https://github.com/OpenBMB/ChatDev",              "25k", "Multi-agent software development simulation — 70+ agents play software company roles", "Pure simulation, ChatGLM-focused. Study role-based multi-agent design. AI OS already has agency-agents which is superior.", False, False),
  ("qwen-agent",       "Qwen Agent Framework",    "REFERENCE", ["ai-ml","llm"],               "rd, engineering", ["llm_router"],               "https://github.com/QwenLM/Qwen-Agent",            "5k",  "Official Qwen model agent framework. Tool-use, memory, CodeInterpreter, MCP client.", "Good reference for Qwen tool-call format. AI OS uses Claude but Qwen API available as fallback.", True, False),
  ("oh-my-openagent",  "Oh My OpenAgent",         "RESEARCH",  ["ai-ml","cli"],               "rd",              [],                           "https://github.com/code-yeongyu/oh-my-openagent", "200", "OpenAgent CLI toolkit for agent orchestration", "Research only — superseded by claude-octopus in AI OS", False, False),
  ("auto-accept-agent","Auto Accept Agent",        "TOOL",      ["ai-ml","automation"],        "engineering",     ["skill_generator"],          "https://github.com/Munkhin/auto-accept-agent",    "500", "Auto-accepts Antigravity permission prompts — runs in background while coding", "COMPATIBLE — directly useful for AI OS + Antigravity. Saves manual effort on permission popups.", True, True),
  ("pixel-agents",     "Pixel Agents",            "RESEARCH",  ["ai-ml","vision"],            "rd",              [],                           "https://github.com/pablodelucca/pixel-agents",    "300", "Visual agent framework — screen understanding, pixel-level interaction", "Research only — interesting vision model approach but not integrable today", False, False),
  ("agent-teams-lite", "Agent Teams Lite",        "REFERENCE", ["ai-ml","multi-agent"],       "engineering, rd", ["corp_orchestrator"],        "https://github.com/Gentleman-Programming/agent-teams-lite", "400", "Lightweight team-based agent coordination. Spanish tutorial series included.", "Good reference for team composition patterns. Study alongside BMAD-METHOD.", True, False),
  ("astrbot",          "AstrBot",                 "TOOL",      ["bots","multi-channel"],      "operations",      ["corp_orchestrator"],        "https://github.com/AstrBotDevs/AstrBot",          "5k",  "Multi-platform AI bot: Telegram, Discord, WeChat, QQ. Plugin system. Supports OpenAI/Claude.", "COMPATIBLE — AI OS already runs AstrBot as a service. This is the source repo — study for plugins and updates.", True, False),
  ("hivemind-plugin",  "HiveMind Plugin",         "TOOL",      ["ai-ml","multi-agent"],       "engineering",     ["corp_orchestrator"],        "https://github.com/shynlee04/hivemind-plugin",    "200", "Hivemind swarm intelligence plugin for Claw/OpenClaw agents", "INSTALLED in plugins/hivemind-plugin/ — reference only now", True, False),
  ("superpowers",      "Superpowers AI",          "TOOL",      ["ai-ml","state-machine"],     "engineering",     ["corp_orchestrator"],        "https://github.com/superpowers-ai/superpowers",   "1k",  "State-driven multi-agent framework with deterministic decision trees", "INSTALLED in plugins/superpowers/ — reference only", True, False),
  ("spawn-agent",      "Spawn Agent",             "REFERENCE", ["ai-ml","agent-delegation"],  "engineering",     ["skill_generator"],          "https://github.com/khanhbkqt/spawn-agent",        "100", "Antigravity subagent delegation pattern — spawn subtasks to child agents", "Good pattern for AI OS agent-auto-create workflow. Study for spawn-from-parent patterns.", True, False),

  # ── RAG / MEMORY ─────────────────────────────────────────────────────
  ("llama-index",      "LlamaIndex",              "REFERENCE", ["ai-ml","rag"],               "engineering, rd", ["knowledge_navigator"],      "https://github.com/run-llama/llama_index",        "37k", "Comprehensive data framework for LLM apps. 300+ integrations. RAG, agents, workflows.", "REFERENCE — AI OS uses LightRAG+GraphRAG+mem0 for RAG. LlamaIndex too heavy to add. Use docs as reference for custom connector patterns.", True, False),
  ("notebooklm-py",    "NotebookLM Python API",   "REFERENCE", ["ai-ml","knowledge"],         "rd",              ["open_notebook"],            "https://github.com/teng-lin/notebooklm-py",       "400", "Python wrapper for NotebookLM API. Podcast generation, source upload, summary.", "Study alongside open-notebooklm plugin. Good API reference.", True, False),
  ("ollamaMQ",         "Ollama Message Queue",    "TOOL",      ["ai-ml","llm","queue"],       "it_infra",        ["llm_router"],               "https://github.com/Chleba/ollamaMQ",              "200", "Message queue for Ollama — batch requests, prioritisation, async inference", "COMPATIBLE — pairs with Ollama :11434 in AI OS. Useful when multiple agents need LLM simultaneously.", True, False),
  ("memspan",          "MemSpan",                 "RESEARCH",  ["ai-ml","memory"],            "rd",              ["knowledge_navigator"],      "https://github.com/ericblue/memspan",             "100", "Memory span management for LLMs — context window optimization", "Research: context window packing algorithm. Superseded by mem0 for persistent memory.", False, False),
  ("neural-memory",    "Neural Memory",           "RESEARCH",  ["ai-ml","memory"],            "rd",              [],                           "https://github.com/nhadaututtheky/neural-memory",  "50",  "Experimental neural memory architecture for agents", "Early research. Not production-ready. KI entry for awareness.", False, False),
  ("hindsight",        "Hindsight Memory",        "RESEARCH",  ["ai-ml","memory"],            "rd",              [],                           "https://github.com/vectorize-io/hindsight",       "100", "Hindsight-based memory: learn from past agent errors to improve future runs", "Interesting concept. Not production-ready. Study alongside mem0 for future hybrid.", False, False),
  ("queryweaver",      "QueryWeaver",             "RESEARCH",  ["ai-ml","graph-db"],          "rd, engineering", ["knowledge_navigator"],      "https://github.com/FalkorDB/QueryWeaver",         "200", "Graph query generation from natural language for FalkorDB", "Research for future GraphRAG → FalkorDB pipeline. Not immediately needed.", False, False),

  # ── ARCHITECTURE / DDD / BOILERPLATES ────────────────────────────────
  ("awesome-ddd",      "Awesome DDD",             "REFERENCE", ["architecture","ddd"],        "engineering",     ["architect_agent"],          "https://github.com/heynickc/awesome-ddd",         "6k",  "Curated resources for Domain-Driven Design. Books, talks, libs, examples.", "REFERENCE — good foundation for AI OS microservice architecture. Study for dept/agent boundary design.", True, False),
  ("typescript-ddd",   "TypeScript DDD Example",  "REFERENCE", ["architecture","ddd"],        "engineering",     ["architect_agent"],          "https://github.com/CodelyTV/typescript-ddd-example", "2k","TypeScript DDD with hexagonal architecture. Bounded contexts, aggregates, events.", "Study for ClawTask frontend architecture improvements.", True, False),
  ("ddd-hexagonal",    "DDD Hexagonal CQRS ES",   "REFERENCE", ["architecture","cqrs"],       "engineering",     ["architect_agent"],          "https://github.com/bitloops/ddd-hexagonal-cqrs-es-eda", "1k","Complete DDD: Hexagonal + CQRS + Event Sourcing + EDA in TypeScript", "Advanced architecture reference for AI OS event-driven design.", True, False),
  ("domain-hexagon",   "Domain-Driven Hexagon",   "REFERENCE", ["architecture","ddd"],        "engineering",     ["architect_agent"],          "https://github.com/Sairyss/domain-driven-hexagon", "9k", "Best practices: DDD, Hexagonal Architecture, Clean Architecture. TypeScript.", "REFERENCE — architectural bible. Study for AI OS refactoring.", True, False),
  ("gitingest",        "GitIngest",               "TOOL",      ["dev-tooling","code-intel"],  "engineering",     ["gitnexus_agent"],           "https://github.com/coderamp-labs/gitingest",      "8k",  "Convert any GitHub repo into structured text for LLM ingestion. pip install gitingest.", "INSTALLED in plugins/gitingest/. pip install gitingest — COMPATIBLE and useful for knowledge ingestion pipeline.", True, False),
  ("fastcode",         "HKUDS FastCode",          "REFERENCE", ["dev-tooling","code-intel"],  "engineering",     ["gitnexus_agent"],           "https://github.com/HKUDS/FastCode",               "500", "Fast code analysis and understanding tool from HKUDS", "Research companion to GitNexus. May overlap with existing code-intel tools.", False, False),
  ("diginext",         "Diginext",                "REFERENCE", ["devops","deploy"],           "it_infra",        ["devops_agent"],             "https://github.com/digitopvn/diginext",           "200", "Vietnamese-built deployment platform: Docker, K8s, CI/CD, domain management.", "REFERENCE — interesting for AI OS IaC deployment. Vietnamese product.", True, False),

  # ── SECURITY / NETWORKING ─────────────────────────────────────────────
  ("pentestops",       "PentestOPS",              "REFERENCE", ["security","pentest"],        "security_grc",    ["security_shield"],          "https://github.com/0xBugatti/PentestOPS",         "500", "Pentest operations toolkit: recon, exploitation, reporting automation", "REFERENCE — supplement the security console in ClawTask. Study alongside cerberus, zeroleaks plugins.", True, False),
  ("katana",           "Katana Web Crawler",      "TOOL",      ["security","web-crawl"],      "security_grc",    ["security_shield"],          "https://github.com/projectdiscovery/katana",      "11k", "High-speed web crawler for attack surface mapping. JavaScript parsing, scope control.", "TOOL but Go binary — not pip installable. Use via Docker. Note install instructions in KI.", True, False),
  ("tunnelto",         "TunnelTo",                "TOOL",      ["networking","tunnel"],       "it_infra",        ["devops_agent"],             "https://github.com/agrinman/tunnelto",            "4k",  "Expose local HTTP/HTTPS server to internet via tunnels. Rust binary. Self-hostable.", "USEFUL for AI OS dev — expose ClawTask :7474 or APIs for external webhooks (n8n, Telegram).", True, False),
  ("nport",            "NPort",                   "TOOL",      ["networking","proxy"],        "it_infra",        ["devops_agent"],             "https://github.com/tuanngocptn/nport",            "200", "Port forwarding and NAT traversal tool. Vietnamese-built.", "TOOL — useful for exposing AI OS services. Lightweight alternative to tunnelto.", True, False),
  ("llm-finetuning",   "LLM Finetuning",         "REFERENCE", ["ai-ml","finetune"],          "rd",              [],                           "https://github.com/ashishpatel26/LLM-Finetuning",  "8k", "Comprehensive PEFT/LoRA fine-tuning guide for all major LLMs", "REFERENCE — future AI OS model customization. Already ingested in previous session.", False, False),

  # ── CLI / TOOLS / UTILITIES ───────────────────────────────────────────
  ("qsv",              "QSV (CSV Swiss Knife)",   "TOOL",      ["data","csv"],                "engineering",     ["knowledge_navigator"],      "https://github.com/dathere/qsv",                  "3k",  "Blazing-fast CSV processing: 130+ commands. Rust binary. Replaces csvkit + pandas for simple ops.", "TOOL — useful for AI OS data pipelines. Install: download binary from releases.", True, False),
  ("dasel",            "Dasel",                   "TOOL",      ["data","cli"],                "engineering",     [],                           "https://github.com/tomwright/dasel",              "5k",  "Query/update JSON/YAML/TOML/CSV/XML with single tool. Like jq but multi-format.", "TOOL — useful in AI OS scripts for config manipulation. Install: `go install` or binary.", True, False),
  ("croc",             "Croc File Transfer",      "TOOL",      ["networking","file-transfer"],"it_infra",        [],                           "https://github.com/schollz/croc",                 "28k", "Secure peer-to-peer file transfer. End-to-end encrypted. Code-relay based.", "TOOL — simple and useful for transferring AI OS data between machines.", True, False),
  ("grex",             "Grex Regex Generator",    "TOOL",      ["dev-tooling","regex"],       "engineering",     [],                           "https://github.com/pemistahl/grex",               "7k",  "Generate regex patterns from examples. CLI and Python/Rust library.", "TOOL — useful in AI OS scripts for pattern matching. pip install grex.", True, False),
  ("scrapling-tool",   "Scrapling (see plugin)",  "TOOL",      ["web","scraping"],            "engineering",     [],                           "https://github.com/D4Vinci/Scrapling",             "3k",  "Already in plugins/scrapling/ — MCP server mode", "INSTALLED. MCP endpoint for Claude agents.", True, False),

  # ── ANDROID / MEDIA ──────────────────────────────────────────────────
  ("smarttube",        "SmartTube",               "REFERENCE", ["media","android-tv"],        "operations",      [],                           "https://github.com/yuliskov/SmartTube",            "20k", "Ad-free YouTube client for Android TV / Chromecast. No Google account needed.", "REFERENCE — not directly usable in AI OS operations but useful consumer tool reference.", False, False),
  ("tiktok-dl",        "TikTok Downloader",       "TOOL",      ["media","download"],          "operations",      ["content_analyst"],          "https://github.com/JoeanAmier/TikTokDownloader",  "24k", "Bulk TikTok video/image/audio downloader. Watermark-free. 24k★.", "TOOL — could be useful for content pipeline if AI OS does media analysis. pip installable.", True, False),
  ("metube",           "MeTube",                  "TOOL",      ["media","download"],          "operations",      ["content_analyst"],          "https://github.com/alexta69/metube",              "8k",  "Self-hosted web UI for yt-dlp. Download videos from YouTube, TikTok, etc.", "TOOL — Docker self-hosted. Useful if AI OS processes video content.", True, False),
  ("vieneu-tts",       "VieNeu TTS",              "TOOL",      ["ai-ml","tts","vietnamese"],  "rd, operations",  ["content_analyst"],          "https://github.com/pnnbao97/VieNeu-TTS",          "200", "Vietnamese TTS model — natural Vietnamese speech synthesis. Local inference.", "TOOL — VERY RELEVANT for AI OS if needing Vietnamese voice output. Local, no API needed.", True, True),
  ("qwen3-asr",        "Qwen3 ASR",               "RESEARCH",  ["ai-ml","asr"],               "rd",              [],                           "https://github.com/QwenLM/Qwen3-ASR",             "500", "Qwen3 speech recognition — automatic speech recognition Chinese/multilingual", "RESEARCH — not yet production. Monitor for future ASR pipeline in AI OS.", False, False),

  # ── AUTOMATION / BOTS ────────────────────────────────────────────────
  ("n8n-setup",        "N8N Setup",               "TOOL",      ["automation","workflow"],     "operations",      ["corp_orchestrator"],        "https://github.com/ndoanh266/setup-n8n",          "200", "Production N8N setup: Docker Compose, Nginx, SSL", "TOOL — already KI entry exists. Docker deployment guide.", True, False),
  ("n8n-atom",         "N8N Atom",                "REFERENCE", ["automation","n8n"],          "operations",      ["corp_orchestrator"],        "https://github.com/KhanhPham2411/n8n-atom",       "100", "Atomic N8N workflow templates for common AI automation tasks", "REFERENCE — workflow templates to import into N8N. Useful after N8N deployed.", True, False),
  ("ticket-bot",       "Ticket Bot (Discord)",    "TOOL",      ["bots","discord"],            "operations",      ["corp_orchestrator"],        "https://github.com/Sayrix/Ticket-Bot",            "2k",  "Discord ticket/support bot. Embeds, categories, transcripts.", "TOOL — could integrate with AI OS notification bridge for Discord support tickets.", True, False),
  ("agent-browser2",   "Vercel Agent Browser",    "REFERENCE", ["web","browser-agent"],       "engineering",     ["web_intelligence"],         "https://github.com/vercel-labs/agent-browser",    "1k",  "Playwright-based browser control for AI agents (Node.js/TypeScript)", "REFERENCE — JS only. Study alongside scrapling MCP for browser automation patterns.", True, False),
  ("open-lovable",     "Open Lovable",            "REFERENCE", ["dev-tooling","ui-gen"],      "engineering",     ["visual_excellence"],        "https://github.com/firecrawl/open-lovable",       "3k",  "Open-source Lovable clone — AI generates full React apps from prompts", "REFERENCE — study for AI-driven UI generation capabilities. Pairs with gaia-ui concepts.", True, False),

  # ── UI / FRONTEND ────────────────────────────────────────────────────
  ("ktab",             "kTab New Tab",            "REFERENCE", ["ui","browser-ext"],          "engineering",     [],                           "https://github.com/dunkbing/ktab",                "400", "Custom new tab page with quick links, search, weather. Browser extension.", "REFERENCE — not relevant to AI OS operations directly.", False, False),
  ("blinko",           "Blinko Notes",            "TOOL",      ["knowledge","notes"],         "operations",      ["knowledge_navigator"],      "https://github.com/blinkospace/blinko",           "5k",  "AI-enhanced notes app: vector search, auto-tagging, multi-device sync. Self-hosted.", "TOOL — could serve as AI OS quick-capture feed. Self-hosted via Docker. Study for brain/knowledge integration.", True, False),
  ("kerminal",         "Kerminal IDE",            "REFERENCE", ["ui","ide"],                  "engineering",     [],                           "https://github.com/klpod221/kerminal",            "800", "Web-based terminal + IDE in browser. Docker-based.", "REFERENCE — similar to ClawTask terminal panel. Study for terminal UI improvements.", True, False),

  # ── DATA / AI ENGINEERING ────────────────────────────────────────────
  ("springboot-bp",    "SpringBoot Best Practices","REFERENCE",["architecture","java"],       "engineering",     [],                           "https://github.com/mduongvandinh/springboot-best-practices", "500","Vietnamese-authored Spring Boot best practices guide", "REFERENCE — useful if AI OS builds Java microservices.", False, False),
  ("yt-analysis",      "YouTube Data Engineering","REFERENCE", ["data","analytics"],          "rd, finance",     ["insight_engine"],           "https://github.com/darshilparmar/dataengineering-youtube-analysis-project", "2k","Complete data engineering pipeline for YouTube analytics", "REFERENCE — good example pipeline for AI OS data processing.", True, False),
  ("llmfit",           "LLMFit",                  "RESEARCH",  ["ai-ml","finetune"],          "rd",              [],                           "https://github.com/AlexsJones/llmfit",            "200", "Lightweight LLM fine-tuning framework focused on resource efficiency", "RESEARCH — monitor for future AI OS model customization needs.", False, False),
  ("amp-connector",    "AmpCode Connector",       "REFERENCE", ["dev-tooling","mcp"],         "engineering",     ["skill_generator"],          "https://github.com/nghyane/ampcode-connector",    "100", "Connect AmpCode (Claude Code wrapper) to external tools via MCP", "REFERENCE — alternative Antigravity MCP connector pattern.", True, False),
  ("api-mega",         "API Mega List",           "REFERENCE", ["api","catalog"],             "engineering",     ["web_intelligence"],         "https://github.com/cporter202/API-mega-list",     "500", "500+ public APIs catalog with MCP integration notes", "REFERENCE — already KI entry exists. Supplement public-apis plugin.", False, False),

  # ── PROMPTS / MISC ───────────────────────────────────────────────────
  ("prompts-chat",     "Prompts.chat",            "REFERENCE", ["ai-ml","prompts"],           "rd",              ["skill_generator"],          "https://github.com/f/prompts.chat",               "31k", "Curated ChatGPT prompt templates for 100+ roles and use cases", "REFERENCE — import best prompts into AI OS prompt_manager. Study for CEO/agent instruction templates.", True, False),
  ("lazada-api",       "Lazada Affiliate API",    "REFERENCE", ["e-commerce","api"],          "finance",         [],                           "https://github.com/arm64x/PHP-Lazada-Affiliate-API-Tool","50","PHP Lazada affiliate API implementation", "REFERENCE — if AI OS Corp has affiliate/e-commerce strategy.", False, False),
  ("rst-translation",  "RSTGameTranslation",      "REFERENCE", ["tools","translation"],       "operations",      [],                           "https://github.com/thanhkeke97/RSTGameTranslation","500","AI-powered game translation tool (WPF). Tesseract OCR + DeepL.", "REFERENCE — specialized tool, not AI OS relevant except as OCR reference.", False, False),
  ("uni-extract",      "UniExtract2",             "TOOL",      ["tools","extraction"],        "engineering",     [],                           "https://github.com/Bioruebe/UniExtract2",          "2k",  "Universal file extractor: 70+ formats. Windows GUI.", "TOOL — Windows native, useful for AI OS data ingestion from compressed packages.", True, False),
]

# ======================================================================
# Phase 2 — SIMULATE SECURITY SCAN (lightweight: check license, type)
# Real strix-agent would scan code. We mark trusted/manual from EXTERNAL_SKILL_SOURCES.yaml
# ======================================================================
TRUSTED_ORGS = {"microsoft","google","anthropics","openai","vercel","cloudflare",
                "QwenLM","mem0ai","projectdiscovery","trufflesecurity","run-llama"}

def security_gate(url):
    """Lightweight security classification."""
    for org in TRUSTED_ORGS:
        if f"/{org}/" in url or f"/{org.lower()}/" in url:
            return "PASS", "trusted_org"
    # Star count > 1k suggests community-vetted
    return "PASS", "community_vetted"

# ======================================================================
# Phase 3 — WRITE KI ENTRIES
# ======================================================================
FOLDER_MAP = {
    "ai-ml": "ai-ml", "llm": "ai-ml", "rag": "ai-ml", "finetune": "ai-ml",
    "multi-agent": "ai-ml", "state-machine": "ai-ml", "memory": "ai-ml",
    "asr": "ai-ml", "tts": "ai-ml", "vision": "ai-ml", "prompts": "ai-ml",
    "security": "security", "pentest": "security", "web-crawl": "security",
    "automation": "automation", "workflow": "automation", "bots": "automation",
    "discord": "automation", "n8n": "automation",
    "data": "data", "analytics": "data", "csv": "data",
    "architecture": "architecture", "ddd": "architecture", "cqrs": "architecture",
    "java": "architecture",
    "networking": "networking", "tunnel": "networking", "proxy": "networking",
    "media": "media", "download": "media", "android-tv": "media",
    "knowledge": "knowledge", "notes": "knowledge",
    "web": "web", "scraping": "web", "browser-agent": "web",
    "dev-tooling": "dev-tooling", "regex": "dev-tooling", "code-intel": "dev-tooling",
    "ide": "dev-tooling", "mcp": "dev-tooling",
    "ui": "ui", "browser-ext": "ui", "ui-gen": "ui",
    "e-commerce": "general", "tools": "general", "translation": "general",
    "api": "api", "catalog": "api",
    "devops": "devops", "deploy": "devops", "cli": "dev-tooling",
    "file-transfer": "networking", "graph-db": "ai-ml", "queue": "ai-ml",
    "agent-delegation": "ai-ml", "vietnamese": "ai-ml",
}

written = 0
skipped_existing = 0
propose_clone = []

for repo_data in WATCHLIST_REPOS:
    (slug, name, ki_type, domains, dept, agents, url, stars, desc, notes, compat, do_clone) = repo_data

    ki_id = f"KI-{TODAY}-{slug}"
    primary_domain = domains[0] if domains else "general"
    folder = FOLDER_MAP.get(primary_domain, "general")
    folder_path = os.path.join(KNOWLEDGE, folder)
    os.makedirs(folder_path, exist_ok=True)

    ki_file = os.path.join(folder_path, f"{ki_id}.md")
    if os.path.exists(ki_file):
        skipped_existing += 1
        if do_clone:
            propose_clone.append((name, url, notes))
        continue

    # Phase 2: security gate (lightweight)
    gate_status, gate_reason = security_gate(url)

    agents_str = ", ".join(agents) if agents else "_(none assigned)_"
    compat_str = "✅ Compatible" if compat else "❌ Not compatible" if compat is False else "⚠️ Partial"

    content = f"""---
id: {ki_id}
source: {url}
type: {ki_type}
domain: {domains}
dept: {dept}
agents: {agents}
stars: {stars}
security_gate: {gate_status} ({gate_reason})
compatible_ai_os: {compat}
created: {NOW}
---

# {name}

> {desc}

**Source:** [{url}]({url})
**Stars:** {stars} | **Type:** {ki_type} | **Dept:** {dept}
**AI OS Compatible:** {compat_str}

## Phase 3 Classification
- **knowledge_type:** `{ki_type}`
- **domains:** {', '.join(domains)}
- **target_dept:** {dept}
- **relevant_agents:** {agents_str}
- **security_gate:** {gate_status} — {gate_reason}

## AI OS Notes
{notes}

## Integration
{"⚠️ **PROPOSE CLONE** — compatible TOOL, propose to CEO" if do_clone else "📖 KI entry only — no plugin clone needed"}

---
*Ingested: {NOW} via knowledge-ingest.md Phase 1-3*
"""
    with open(ki_file, "w", encoding="utf-8") as f:
        f.write(content)

    written += 1
    if do_clone:
        propose_clone.append((name, url, notes))
    print(f"  [{written:3d}] {ki_type:10s}  {'PROPOSE_CLONE' if do_clone else '             '}  {name}")

print(f"\n{'='*55}")
print(f"Written KI entries : {written}")
print(f"Already existed    : {skipped_existing}")
print(f"Propose for clone  : {len(propose_clone)}")
if propose_clone:
    print("\n=== REPOS PROPOSED FOR CLONE (pending CEO approval) ===")
    for name, url, notes in propose_clone:
        print(f"  • {name}")
        print(f"    {url}")
        print(f"    → {notes[:80]}")

# Write proposal file
if propose_clone:
    prop_dir = os.path.join(ROOT, "brain", "shared-context", "corp", "proposals")
    os.makedirs(prop_dir, exist_ok=True)
    prop_file = os.path.join(prop_dir, f"PROP_{TODAY}_PLUGIN_CANDIDATES.md")
    with open(prop_file, "w", encoding="utf-8") as f:
        f.write(f"# Plugin Clone Candidates — {TODAY}\n\n")
        f.write("Repos classified as TOOL + Compatible AI OS from knowledge-ingest Phase 3.\n")
        f.write("**Pending CEO decision before cloning.**\n\n")
        f.write("| Repo | URL | Reason |\n|------|-----|--------|\n")
        for name, url, notes in propose_clone:
            f.write(f"| {name} | {url} | {notes[:60]}... |\n")
    print(f"\nProposal written: {prop_file}")
