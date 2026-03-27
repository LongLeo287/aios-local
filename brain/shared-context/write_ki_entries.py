#!/usr/bin/env python3
"""
write_ki_entries.py — Write brain/knowledge KI entries for 15 LEARN-ONLY repos
These repos are classified as REFERENCE/RESEARCH in knowledge-ingest.md Phase 3.
No clone needed — knowledge extracted into structured KI entries.
"""
import os, json
from datetime import datetime

AIOS_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
TODAY     = datetime.now().strftime("%Y-%m-%d")
NOW       = datetime.now().isoformat()

LEARN_REPOS = [
    {
        "ki_id":   f"KI-{TODAY}-simonw-llm",
        "name":    "Simon W LLM CLI",
        "type":    "TOOL",
        "domain":  ["ai-ml", "llm", "cli"],
        "dept":    "engineering",
        "agents":  ["llm_router"],
        "install": "pip install llm",
        "desc":    "Access 200+ LLMs from terminal. Plugin system for Ollama/llama.cpp, OpenAI, Anthropic, Gemini, Mistral. Embeddings, conversation logging, Python API.",
        "url":     "https://github.com/simonw/llm",
        "notes":   "No clone needed — install via pip. Use in AI OS scripts: `import llm; model = llm.get_model('claude-3-5-sonnet')`. Useful for llm_router to route between models.",
    },
    {
        "ki_id":   f"KI-{TODAY}-trufflehog",
        "name":    "TruffleHog Secret Scanner",
        "type":    "TOOL",
        "domain":  ["security", "devsecops", "ci-cd"],
        "dept":    "security_grc",
        "agents":  ["security_shield", "fbi-watchdog"],
        "install": "docker run trufflesecurity/trufflehog git <repo-url>",
        "desc":    "700+ detectors for secrets/credentials in Git/GitHub/AWS/GCP/files. 16k★. Go binary — use via Docker or binary download. CI/CD integration.",
        "url":     "https://github.com/trufflesecurity/trufflehog",
        "notes":   "Run before any plugin is added to AI OS. Add to CI/CD: `trufflehog git plugins/<plugin>`. Best practice: scan on every new repo ingest.",
    },
    {
        "ki_id":   f"KI-{TODAY}-setup-n8n",
        "name":    "Setup N8N Production",
        "type":    "TOOL",
        "domain":  ["automation", "workflow", "devops"],
        "dept":    "operations",
        "agents":  ["corp_orchestrator"],
        "install": "cd plugins/setup-n8n && docker compose up -d",
        "desc":    "Production N8N setup with Docker Compose, Nginx, SSL, webhook config. AI-ready automation infrastructure for triggering agents.",
        "url":     "https://github.com/ndoanh266/setup-n8n",
        "notes":   "Deploy to trigger AI OS agents from external webhooks. N8N workflows can call ClawTask API (:7474) as HTTP node. Config: set WEBHOOK_URL to ClawTask base URL.",
    },
    {
        "ki_id":   f"KI-{TODAY}-qwen2-omni",
        "name":    "Qwen2.5-Omni Multimodal LLM",
        "type":    "RESEARCH",
        "domain":  ["ai-ml", "llm", "multimodal", "tts", "asr"],
        "dept":    "rd",
        "agents":  ["llm_router", "content_analyst"],
        "install": "pip install transformers torch  # needs A100+ GPU",
        "desc":    "End-to-end multimodal LLM (text/image/audio/video → text+speech). Thinker-Talker architecture. Real-time streaming. TMRoPE position embedding. 7B-72B models.",
        "url":     "https://github.com/QwenLM/Qwen2.5-Omni",
        "notes":   "Requires high-end GPU. Use via Aliyun Model Studio API for production. MiniMax API is current replacement for TTS. Track for future local multimodal model use.",
        "key_concepts": ["Thinker-Talker architecture", "TMRoPE", "streaming audio output", "omni modality"],
    },
    {
        "ki_id":   f"KI-{TODAY}-llm-mux",
        "name":    "LLM Mux",
        "type":    "PATTERN",
        "domain":  ["ai-ml", "llm", "infrastructure", "load-balancing"],
        "dept":    "engineering",
        "agents":  ["llm_router"],
        "install": "# Custom setup — see repo docs",
        "desc":    "LLM request multiplexer pattern: route across multiple LLM backends by load/cost/latency. Failover, caching. Implements proxy-compatible API.",
        "url":     "https://github.com/nghyane/llm-mux",
        "notes":   "Pattern reference for brain/skills/llm_router. Key learning: implement fallback chain (Anthropic → OpenAI → Ollama). Cache frequent queries with TTL.",
        "key_concepts": ["fallback chain", "cost-based routing", "latency tracking", "response caching"],
    },
    {
        "ki_id":   f"KI-{TODAY}-agent-browser",
        "name":    "Vercel Agent Browser",
        "type":    "TOOL",
        "domain":  ["web-automation", "browser", "ai-agent"],
        "dept":    "engineering",
        "agents":  ["web_intelligence", "autoresearchclaw"],
        "install": "npm install @vercel/agent-browser",
        "desc":    "Playwright-based intelligent browser control: screenshot understanding, form-fill, structured data extraction, navigation. AI-native browser API.",
        "url":     "https://github.com/vercel-labs/agent-browser",
        "notes":   "JS/TS only. Consider for Node.js workflows. Pairs with web_intelligence skill for structured web data extraction. Alternative to raw Playwright.",
    },
    {
        "ki_id":   f"KI-{TODAY}-ai-engineering-toolkit",
        "name":    "AI Engineering Toolkit",
        "type":    "REFERENCE",
        "domain":  ["ai-ml", "mlops", "evaluation", "ai-engineering"],
        "dept":    "rd",
        "agents":  ["insight_engine", "cognitive_reflector"],
        "install": "",
        "desc":    "Curated AI engineering patterns: MLOps, LLM evaluation, inference optimization, observability, prompt engineering, data pipelines. Framework-agnostic.",
        "url":     "https://github.com/Sumanth077/ai-engineering-toolkit",
        "notes":   "Key patterns: eval-driven dev, observability-first, prompt versioning. Apply when designing new AI OS features. Ref for CIV metrics design.",
        "key_concepts": ["eval-driven development", "LLM observability", "inference caching", "prompt versioning"],
    },
    {
        "ki_id":   f"KI-{TODAY}-learn-claude-code",
        "name":    "Learn Claude Code",
        "type":    "REFERENCE",
        "domain":  ["ai-ml", "claude-code", "developer-experience"],
        "dept":    "rd",
        "agents":  ["skill_generator", "cognitive_evolver"],
        "install": "",
        "desc":    "Comprehensive Claude Code guide: commands, CLAUDE.md setup, MCP config, advanced workflows, multi-agent patterns. Chinese + English.",
        "url":     "https://github.com/shareAI-lab/learn-claude-code",
        "notes":   "Key takeaways: use /compact for context, custom slash-commands in .claude/commands/, extended thinking for complex tasks, git worktrees for parallel agents.",
        "key_concepts": ["/compact", "custom slash-commands", "extended thinking", "git worktrees for parallelism"],
    },
    {
        "ki_id":   f"KI-{TODAY}-videocaptioner",
        "name":    "Video Captioner",
        "type":    "TOOL",
        "domain":  ["media", "ai-ml", "subtitle"],
        "dept":    "operations",
        "agents":  ["content_analyst"],
        "install": "pip install videocaptioner",
        "desc":    "AI subtitle generator: 100+ languages, SRT/VTT output, batch processing, local WhisperX + cloud model support. 2k★.",
        "url":     "https://github.com/WEIFENG2333/VideoCaptioner",
        "notes":   "Use for AI OS media content production. Install via pip, works locally with WhisperX (no GPU needed for small files). Add to content pipeline.",
    },
    {
        "ki_id":   f"KI-{TODAY}-pm-skills",
        "name":    "PM Skills",
        "type":    "REFERENCE",
        "domain":  ["product-management", "strategy", "skills"],
        "dept":    "strategy",
        "agents":  ["strategy/product-manager-agent"],
        "install": "",
        "desc":    "Product manager skill pack: roadmap, PRD writing, OKR, stakeholder management, sprint planning prompts for AI agents.",
        "url":     "https://github.com/phuryn/pm-skills",
        "notes":   "Import key prompts into strategy/product-manager-agent AGENT.md skill section. Useful: OKR template, PRD structure, stakeholder matrix.",
    },
    {
        "ki_id":   f"KI-{TODAY}-awesome-agent-skills",
        "name":    "Awesome Agent Skills",
        "type":    "REFERENCE",
        "domain":  ["skills", "catalog", "registry"],
        "dept":    "registry_capability",
        "agents":  ["skill_generator", "skill_sentry"],
        "install": "",
        "desc":    "Curated cross-framework agent skills: Claude, OpenAI, LangChain, AutoGen, CrewAI, Gemini. Community maintained 400★.",
        "url":     "https://github.com/phuryn/awesome-agent-skills",
        "notes":   "Run monthly: check for new skill IDs to import into SKILL_REGISTRY.json. Use as discovery source for ingest_queued_repos.py.",
    },
    {
        "ki_id":   f"KI-{TODAY}-gaia-ui",
        "name":    "Gaia UI",
        "type":    "REFERENCE",
        "domain":  ["ui", "react", "design"],
        "dept":    "engineering",
        "agents":  ["visual_excellence"],
        "install": "npm install @gaia/ui",
        "desc":    "AI-native React components: streaming chat, agent status, tool call displays, timeline. Shadcn/RadixUI based. 300★.",
        "url":     "https://github.com/theexperiencecompany/gaia-ui",
        "notes":   "Design reference for ClawTask UI upgrades. Key components: streaming response display, agent activity timeline. Use as inspiration not dependency.",
    },
    {
        "ki_id":   f"KI-{TODAY}-api-mega-list",
        "name":    "API Mega List",
        "type":    "REFERENCE",
        "domain":  ["api", "integration", "catalog"],
        "dept":    "engineering",
        "agents":  ["web_intelligence", "knowledge_navigator"],
        "install": "",
        "desc":    "500+ public APIs: REST/GraphQL/WebSocket/MCP, auth methods, rate limits. Useful for AI OS knowledge workers finding data sources.",
        "url":     "https://github.com/cporter202/API-mega-list",
        "notes":   "Check before building new AI OS integrations — likely already an API exists. Complement to public-apis plugin.",
    },
    {
        "ki_id":   f"KI-{TODAY}-picoclaw",
        "name":    "PicoClaw (IoT)",
        "type":    "RESEARCH",
        "domain":  ["iot", "embedded", "edge-ai"],
        "dept":    "rd",
        "agents":  [],
        "install": "pip install picoclaw",
        "desc":    "Lightweight Claw agent for embedded/IoT. Raspberry Pi 4+. MQTT, <50MB footprint, local tool execution, edge inference.",
        "url":     "https://github.com/sipeed/picoclaw",
        "notes":   "Low priority for current AI OS (Windows-based). Track for future edge deployments. No agent needed — route to engineering dept head if ever needed.",
    },
    {
        "ki_id":   f"KI-{TODAY}-learn-ai-engineering",
        "name":    "Learn AI Engineering",
        "type":    "REFERENCE",
        "domain":  ["ai-engineering", "curriculum", "learning"],
        "dept":    "rd",
        "agents":  ["cognitive_evolver"],
        "install": "",
        "desc":    "AI engineering learning path: LLMs, RAG, agents, evaluation, deployment. Project-based curriculum with code examples. 1k★.",
        "url":     "https://github.com/ashishps1/learn-ai-engineering",
        "notes":   "Onboarding reference for new AI OS collaborators. Key modules: RAG patterns, agent evaluation, LLM inference optimization.",
    },
]

# Create knowledge domain dirs
KNOWLEDGE_BASE = os.path.join(AIOS_ROOT, "brain", "knowledge")
domain_dirs = {
    "ai-ml": "ai-ml", "security": "security", "automation": "automation",
    "media": "media", "strategy": "strategy", "catalog": "catalog",
    "ui": "ui", "api": "api", "iot": "iot", "skills": "skills", "general": "general",
}
for d in set(domain_dirs.values()):
    os.makedirs(os.path.join(KNOWLEDGE_BASE, d), exist_ok=True)

os.makedirs(os.path.join(KNOWLEDGE_BASE, "staging"), exist_ok=True)

INDEX_PATH = os.path.join(KNOWLEDGE_BASE, "INDEX.md")
index_entries = []

written = 0
for repo in LEARN_REPOS:
    # Determine domain folder
    primary_domain = repo["domain"][0] if repo["domain"] else "general"
    folder_map = {
        "ai-ml": "ai-ml", "llm": "ai-ml", "multimodal": "ai-ml",
        "security": "security", "devsecops": "security",
        "automation": "automation", "workflow": "automation",
        "media": "media", "subtitle": "media",
        "product-management": "strategy", "strategy": "strategy",
        "skills": "skills", "catalog": "catalog", "registry": "catalog",
        "ui": "ui", "react": "ui", "design": "ui",
        "api": "api", "integration": "api",
        "iot": "iot", "embedded": "iot",
        "ai-engineering": "ai-ml", "curriculum": "ai-ml",
        "web-automation": "ai-ml", "browser": "ai-ml",
    }
    domain_folder = folder_map.get(primary_domain, "general")
    os.makedirs(os.path.join(KNOWLEDGE_BASE, domain_folder), exist_ok=True)

    # Write KI entry
    ki_path = os.path.join(KNOWLEDGE_BASE, domain_folder, f"{repo['ki_id']}.md")
    concepts = "\n".join(f"- {c}" for c in repo.get("key_concepts", [])) or "_See source URL_"
    agents_list = ", ".join(repo["agents"]) if repo["agents"] else "_(none assigned)_"

    content = f"""---
id: {repo['ki_id']}
source: {repo['url']}
type: {repo['type']}
domain: {repo['domain']}
dept: {repo['dept']}
agents: {repo['agents']}
created: {NOW}
---

# {repo['name']}

> {repo['desc']}

**Source:** [{repo['url']}]({repo['url']})
**Type:** {repo['type']} | **Dept:** {repo['dept']}
**Relevant Agents:** {agents_list}

## AI OS Notes
{repo['notes']}

## Install / Use
```
{repo.get('install') or '# Reference only — no install needed'}
```

## Key Concepts
{concepts}

## Cross-links
- SKILL.md: `plugins/{repo['ki_id'].split('-', 3)[-1]}/SKILL.md`
- FAST_INDEX: keyword `{repo['name'].lower().replace(' ', '_')[:20]}`
"""
    with open(ki_path, "w", encoding="utf-8") as f:
        f.write(content)

    index_entries.append(f"| [{repo['ki_id']}]({domain_folder}/{repo['ki_id']}.md) | {repo['name']} | {repo['type']} | {repo['dept']} | {TODAY} |")
    written += 1
    print(f"  [{written:2d}] {repo['type']:10s}  {repo['ki_id']}")

# Append to INDEX.md
header_needs_writing = not os.path.exists(INDEX_PATH) or os.path.getsize(INDEX_PATH) == 0
with open(INDEX_PATH, "a", encoding="utf-8") as f:
    if header_needs_writing:
        f.write("# brain/knowledge INDEX\n\n| KI ID | Name | Type | Dept | Date |\n|-------|------|------|------|------|\n")
    f.write("\n".join(index_entries) + "\n")

print(f"\n✅ Wrote {written} KI entries to brain/knowledge/")
print(f"   INDEX.md updated with {written} new entries")
