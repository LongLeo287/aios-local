#!/usr/bin/env python3
"""
ingest_queued_repos.py — Create SKILL.md for all Queued repos not yet in plugins/
Run: python brain/shared-context/ingest_queued_repos.py
"""
import os, json
from datetime import datetime

AIOS_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
PLUGINS   = os.path.join(AIOS_ROOT, "plugins")
TODAY     = datetime.now().strftime("%Y-%m-%d")

REPOS = [
    {
        "dir": "mem0",
        "name": "Mem0 (AI Memory)",
        "tier": 1,
        "cat": "ai-memory",
        "dept": "rd, engineering",
        "stars": "22k",
        "desc": "Persistent AI memory layer: +26% accuracy vs OpenAI Memory, 91% faster, 90% fewer tokens. Python/JS SDK. Drop-in replacement for LangChain/LlamaIndex memory.",
        "url": "https://github.com/mem0ai/mem0",
        "tags": ["memory", "ai-memory", "rag", "persistent", "sdk"],
        "usage": "Agent memory layer — drop-in for all AI OS agents needing persistent context across sessions",
        "install": "pip install mem0",
    },
    {
        "dir": "graphrag",
        "name": "Microsoft GraphRAG",
        "tier": 1,
        "cat": "rag-knowledge",
        "dept": "engineering, rd",
        "stars": "21k",
        "desc": "Graph-based RAG from Microsoft Research. Narrative-aware entity extraction + knowledge graph. Local/global search modes. Python indexer + query engine.",
        "url": "https://github.com/microsoft/graphrag",
        "tags": ["rag", "knowledge-graph", "graphrag", "llm", "microsoft"],
        "usage": "Advanced RAG for long-form, narrative-heavy AI OS corpus — complements LightRAG",
        "install": "pip install graphrag",
    },
    {
        "dir": "e2b",
        "name": "E2B Code Sandbox",
        "tier": 1,
        "cat": "sandbox",
        "dept": "engineering, it_infra",
        "stars": "5k",
        "desc": "Open-source cloud sandboxes for AI-generated code. Secure isolated execution. Python + JS SDK. Integrates with OpenAI, Anthropic, LangChain. Self-hostable on AWS/GCP.",
        "url": "https://github.com/e2b-dev/e2b",
        "tags": ["sandbox", "code-execution", "secure", "cloud", "sdk", "ai-code"],
        "usage": "Safe execution of AI-generated code — cloud-scale alternative to OpenSandbox",
        "install": "pip install e2b-code-interpreter",
        "env": "E2B_API_KEY=<key from e2b.dev/dashboard>",
    },
    {
        "dir": "scrapling",
        "name": "Scrapling",
        "tier": 2,
        "cat": "web-scraping",
        "dept": "engineering, rd",
        "stars": "3k",
        "desc": "Effortless web scraping with anti-fingerprinting, proxy support, spiders, MCP server, CLI. Playwright/requests backends. ClaHub-registered skill.",
        "url": "https://github.com/D4Vinci/Scrapling",
        "tags": ["scraping", "web", "playwright", "mcp", "spider", "proxy"],
        "usage": "Web intelligence pipeline — feeds brain/skills/web_intelligence and Blackboard data streams",
        "install": "pip install scrapling",
    },
    {
        "dir": "qwen2-omni",
        "name": "Qwen2.5-Omni (Multimodal)",
        "tier": 2,
        "cat": "llm-multimodal",
        "dept": "rd, engineering",
        "stars": "2k",
        "desc": "End-to-end multimodal LLM: text/image/audio/video input, text+speech output streaming. Thinker-Talker architecture. TMRoPE position embedding. Real-time voice and video chat.",
        "url": "https://github.com/QwenLM/Qwen2.5-Omni",
        "tags": ["llm", "tts", "asr", "multimodal", "qwen", "voice", "video"],
        "usage": "MiniMax TTS alternative — local voice output for AI OS agents; multimodal understanding",
        "install": "pip install transformers torch",
    },
    {
        "dir": "all-agentic-architectures",
        "name": "All Agentic Architectures",
        "tier": 2,
        "cat": "reference",
        "dept": "rd, engineering",
        "stars": "8k",
        "desc": "Comprehensive reference of all agentic AI design patterns: ReAct, Plan+Execute, Reflection, Tool-Use, Multi-Agent, Memory patterns with code examples in Python.",
        "url": "https://github.com/FareedKhan-dev/all-agentic-architectures",
        "tags": ["agentic", "patterns", "reference", "architecture", "multi-agent", "react", "reflection"],
        "usage": "Design reference for AI OS agent architecture — learning resource for skill_generator agent",
        "install": "",
    },
    {
        "dir": "clawwork",
        "name": "ClawWork",
        "tier": 2,
        "cat": "multi-agent",
        "dept": "engineering, rd",
        "stars": "1k",
        "desc": "HKUDS multi-agent work platform. Collaborative agent teams with shared context. Supervisor-worker-executor patterns. Integrates with LightRAG and ClawCode.",
        "url": "https://github.com/HKUDS/ClawWork",
        "tags": ["multi-agent", "clawwork", "team", "supervisor", "hkuds", "collaborative"],
        "usage": "Team orchestration complement to agency-agents — more structured supervisor model",
        "install": "pip install clawwork",
    },
    {
        "dir": "agentsview",
        "name": "AgentsView",
        "tier": 2,
        "cat": "monitoring",
        "dept": "monitoring, engineering",
        "stars": "500",
        "desc": "Real-time agent activity monitoring dashboard. Track agent executions, tool calls, latency, tokens, cost. Multi-LLM support. Web UI with timeline view.",
        "url": "https://github.com/wesm/agentsview",
        "tags": ["monitoring", "agents", "dashboard", "metrics", "tracing", "observability"],
        "usage": "Agent monitoring panel in ClawTask — complements telemetry/receipts system",
        "install": "pip install agentsview",
    },
    {
        "dir": "simonw-llm",
        "name": "Simon W LLM CLI",
        "tier": 2,
        "cat": "cli-tool",
        "dept": "engineering",
        "stars": "4k",
        "desc": "Access 200+ LLMs from terminal. Plugin ecosystem for Ollama/llama.cpp, OpenAI, Anthropic, Gemini, Mistral. Embeddings, conversation logging, Python API.",
        "url": "https://github.com/simonw/llm",
        "tags": ["llm", "cli", "ollama", "openai", "anthropic", "plugins", "embeddings"],
        "usage": "AI OS CLI LLM orchestration — wrap multiple LLM providers from shell scripts and cron jobs",
        "install": "pip install llm",
    },
    {
        "dir": "setup-n8n",
        "name": "Setup N8N Production",
        "tier": 2,
        "cat": "automation",
        "dept": "operations, it_infra",
        "stars": "200",
        "desc": "Production N8N workflow automation setup: Docker Compose, Nginx reverse proxy, SSL, webhook config, persistent data volumes. AI-ready automation infrastructure.",
        "url": "https://github.com/ndoanh266/setup-n8n",
        "tags": ["n8n", "automation", "workflow", "docker", "webhook", "nginx"],
        "usage": "AI OS automation backbone — N8N receives external events and triggers AI agents via webhooks",
        "install": "docker compose up -d  # see repo for .env config",
    },
    {
        "dir": "agent-browser",
        "name": "Agent Browser (Vercel)",
        "tier": 2,
        "cat": "browser-agent",
        "dept": "rd, engineering",
        "stars": "1k",
        "desc": "Playwright-based intelligent browser control for AI agents. Screenshot understanding, form-fill, structured extraction, navigation — OpenAI/Anthropic compatible.",
        "url": "https://github.com/vercel-labs/agent-browser",
        "tags": ["browser", "playwright", "automation", "agent", "vercel", "screenshot"],
        "usage": "Web research automation for AI OS knowledge workers and web-intelligence pipelines",
        "install": "npm install @vercel/agent-browser",
    },
    {
        "dir": "ai-engineering-toolkit",
        "name": "AI Engineering Toolkit",
        "tier": 2,
        "cat": "reference",
        "dept": "rd, engineering",
        "stars": "2k",
        "desc": "Curated toolkit for AI engineers: MLOps, LLM evaluation, inference optimization, observability, data pipelines, prompt engineering. Framework-agnostic.",
        "url": "https://github.com/Sumanth077/ai-engineering-toolkit",
        "tags": ["ai-engineering", "mlops", "evaluation", "reference", "toolkit", "observability"],
        "usage": "Reference for AI OS infra decisions — MLOps, evaluation frameworks, prompt optimization",
        "install": "",
    },
    {
        "dir": "learn-claude-code",
        "name": "Learn Claude Code",
        "tier": 3,
        "cat": "reference",
        "dept": "rd",
        "stars": "500",
        "desc": "Comprehensive Claude Code learning resource by ShareAI Lab: commands, workflows, best practices, advanced patterns. Chinese and English versions.",
        "url": "https://github.com/shareAI-lab/learn-claude-code",
        "tags": ["claude-code", "learning", "reference", "guide", "tutorial"],
        "usage": "Onboarding guide for AI OS agents and developers using Claude Code (Antigravity)",
        "install": "",
    },
    {
        "dir": "trufflehog",
        "name": "TruffleHog (Secret Scanner)",
        "tier": 2,
        "cat": "security",
        "dept": "security_grc, engineering",
        "stars": "16k",
        "desc": "Secret scanning in Git, GitHub, AWS, GCP, file systems. 700+ detectors for all credential types. CI/CD integration. Docker. Real-time streaming mode.",
        "url": "https://github.com/trufflesecurity/trufflehog",
        "tags": ["security", "secrets", "scanning", "credentials", "devsecops", "git", "ci-cd"],
        "usage": "CI/CD security gate — scan AI OS repos + plugins for leaked API keys before every deploy",
        "install": "docker run trufflesecurity/trufflehog git https://github.com/your/repo",
    },
    {
        "dir": "llm-mux",
        "name": "LLM Mux",
        "tier": 2,
        "cat": "llm-routing",
        "dept": "engineering, it_infra",
        "stars": "300",
        "desc": "LLM request multiplexer: route across multiple LLM backends based on load, cost, latency. Failover, caching, load-balancing built-in. Proxy compatible.",
        "url": "https://github.com/nghyane/llm-mux",
        "tags": ["llm", "routing", "multiplexer", "load-balancing", "caching", "failover", "proxy"],
        "usage": "AI OS LLM Router — integrates with brain/skills/llm_router for resilient multi-provider routing",
        "install": "",
    },
    {
        "dir": "pm-skills",
        "name": "PM Skills",
        "tier": 2,
        "cat": "skills-repo",
        "dept": "operations, strategy",
        "stars": "200",
        "desc": "Product manager skills pack for AI agents: roadmap planning, stakeholder management, PRD writing, OKR setting, sprint planning, market analysis prompts.",
        "url": "https://github.com/phuryn/pm-skills",
        "tags": ["product-manager", "skills", "roadmap", "okr", "prd", "strategy", "agile"],
        "usage": "Enhances strategy/product-manager-agent SKILL capability for AI OS Corp planning",
        "install": "",
    },
    {
        "dir": "awesome-agent-skills",
        "name": "Awesome Agent Skills",
        "tier": 2,
        "cat": "catalog",
        "dept": "registry_capability",
        "stars": "400",
        "desc": "Curated list of agent skills, plugins, and tools for all major frameworks: Claude, OpenAI, LangChain, AutoGen, CrewAI, Gemini. Community maintained.",
        "url": "https://github.com/phuryn/awesome-agent-skills",
        "tags": ["curated", "skills", "agents", "catalog", "plugins", "awesome", "cross-framework"],
        "usage": "SKILL_REGISTRY discovery source — monthly scan for new skill IDs to import",
        "install": "",
    },
    {
        "dir": "gaia-ui",
        "name": "Gaia UI",
        "tier": 3,
        "cat": "ui-ux",
        "dept": "engineering",
        "stars": "300",
        "desc": "Modern AI-native React UI component library: streaming chat, agent status indicators, tool call displays, timeline views. Shadcn/RadixUI based.",
        "url": "https://github.com/theexperiencecompany/gaia-ui",
        "tags": ["ui", "react", "ai-chat", "components", "streaming", "design", "shadcn"],
        "usage": "ClawTask UI component inspiration — agent status and streaming response display components",
        "install": "npm install @gaia/ui",
    },
    {
        "dir": "picoclaw",
        "name": "PicoClaw (IoT)",
        "tier": 3,
        "cat": "iot-agent",
        "dept": "engineering",
        "stars": "100",
        "desc": "Lightweight AI agent for embedded/IoT devices. Runs on Raspberry Pi 4+. Minimal footprint (<50MB), MQTT protocol, local tool execution, edge inference.",
        "url": "https://github.com/sipeed/picoclaw",
        "tags": ["iot", "embedded", "raspberry-pi", "mqtt", "lightweight", "edge-ai"],
        "usage": "Edge AI deployments — IoT sensor data ingestion → AI OS telemetry pipeline",
        "install": "pip install picoclaw",
    },
    {
        "dir": "videocaptioner",
        "name": "Video Captioner",
        "tier": 2,
        "cat": "media",
        "dept": "rd, operations",
        "stars": "2k",
        "desc": "AI video subtitle generator and translator. 100+ languages, SRT/VTT/ASS output, batch processing, embed subtitles in video. Local + cloud model support.",
        "url": "https://github.com/WEIFENG2333/VideoCaptioner",
        "tags": ["video", "subtitle", "captioning", "translation", "media", "ai", "srt"],
        "usage": "Media production pipeline — auto-generate multilingual subtitles for AI OS produced content",
        "install": "pip install videocaptioner",
    },
    {
        "dir": "api-mega-list",
        "name": "API Mega List",
        "tier": 2,
        "cat": "reference",
        "dept": "engineering",
        "stars": "500",
        "desc": "Curated 500+ public APIs for AI agents: REST, GraphQL, WebSocket, MCP. Auth methods, rate limits, response formats, use cases all documented.",
        "url": "https://github.com/cporter202/API-mega-list",
        "tags": ["api", "reference", "catalog", "public-apis", "mcp", "rest", "graphql"],
        "usage": "AI OS API discovery — complements public-apis plugin with MCP-specific integrations",
        "install": "",
    },
    {
        "dir": "learn-ai-engineering",
        "name": "Learn AI Engineering",
        "tier": 3,
        "cat": "reference",
        "dept": "rd",
        "stars": "1k",
        "desc": "Structured AI engineering learning path: LLMs, RAG, agents, evaluation, observability, deployment. Project-based curriculum with code examples.",
        "url": "https://github.com/ashishps1/learn-ai-engineering",
        "tags": ["ai-engineering", "learning", "reference", "curriculum", "rag", "llm"],
        "usage": "Onboarding reference for AI OS engineers joining the corp",
        "install": "",
    },
]

created = 0
for r in REPOS:
    plugin_dir = os.path.join(PLUGINS, r["dir"])
    os.makedirs(plugin_dir, exist_ok=True)
    skill_path = os.path.join(plugin_dir, "SKILL.md")

    tags_str = ", ".join(r["tags"])
    tags_list = "[" + ", ".join(r["tags"]) + "]"

    content = f"""---
name: {r['name']}
description: {r['desc']}
department: {r['dept']}
tier: {r['tier']}
category: {r['cat']}
status: active
stars: {r.get('stars', '')}
source: {r['url']}
tags: {tags_list}
ingested: {TODAY}
---

# {r['name']}

> {r['desc']}

**Source:** [{r['url']}]({r['url']})
**Stars:** {r.get('stars', 'N/A')} | **Tier:** {r['tier']} | **Dept:** {r['dept']}

## AI OS Usage
{r['usage']}

"""
    if r.get('install'):
        content += f"""## Quick Install
```bash
{r['install']}
```

"""
    if r.get('env'):
        content += f"""## Environment Variables
```
{r['env']}
```

"""
    content += """## Integration Points
See REPO_REGISTRY.md and FAST_INDEX.json for discovery metadata.

## Key Features
_See source repository README for full feature list and documentation._
"""

    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(content)
    created += 1
    print(f"  [{created:2d}] {r['dir']:35s} tier={r['tier']}  {r['name']}")

print(f"\n✅ Created {created} SKILL.md files in plugins/")
