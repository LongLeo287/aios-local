---
id: notebook_agent
name: Notebook Agent
version: 2.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-22
description: >
  Built-in knowledge processing engine for AI OS.
  Extracts, analyzes, and stores content from PDF, URL, and plain text.
  Always available (no Docker required). Integrates with llm_router,
  blackboard, telegram_notify. Docker extends to full Nova Agent mode.

api_base: "http://localhost:7474/api/notebook"
mode_endpoint: "GET /api/notebook/mode"

accessible_by:
  - content_intake      # PRIMARY: doc-parser-agent, web-crawler-agent
  - asset_library       # knowledge-curator-agent, repo-analyst-agent
  - support             # knowledge-agent, support-analyst
  - rd                  # research-agent, data-collector-agent, academic-researcher
  - strategy            # market-agent, cognitive_reflector, researcher
  - od_learning         # learning-curator-agent, training-agent
  - engineering         # ai-ml-agent (RAG integration)
  - monitoring_inspection # process-monitor-agent

dependencies:
  - llm_router          # Smart LLM provider selection per task type
  - knowledge_enricher  # Web + document extraction layer
  - context_manager     # Session management, ticket coordination
  - blackboard_lock     # Shared agent state write-back
  - telegram_notify     # Completion alerts (optional, requires token)

exposed_functions:
  - name: extract
    endpoint: "POST /api/notebook/extract"
    description: "Extract raw text from PDF path, URL, or plain text body"
    input: "{source, type: 'pdf'|'url'|'text', notebook_id?}"
    output: "{text, word_count, source_type, extracted_at}"

  - name: analyze
    endpoint: "POST /api/notebook/analyze"
    description: "Analyze + summarize extracted content using best available LLM"
    input: "{source, type, prompt?, session_id?, save: bool}"
    output: "{summary, key_points, notebook_id, llm_provider, confidence}"

  - name: save
    endpoint: "POST /api/notebook/save"
    description: "Save analysis result to local notebook store + post to blackboard"
    input: "{title, content, source, tags?}"
    output: "{notebook_id, path, blackboard_updated}"

  - name: list
    endpoint: "GET /api/notebook/list"
    description: "List all saved notebooks with metadata"
    output: "[{id, title, source, created_at, tags}]"

  - name: get
    endpoint: "GET /api/notebook/<id>"
    description: "Retrieve full notebook content by ID"
    output: "{id, title, content, source, analysis, session_history}"

  - name: mode
    endpoint: "GET /api/notebook/mode"
    description: "Check current mode: lite (always) or full (Docker)"
    output: "{mode, capabilities, departments, llm}"

consumed_by:
  - intake-agent          # Stage + ticket creation
  - doc-parser-agent      # PDF/DOCX extraction
  - web-crawler-agent     # URL article extraction
  - knowledge-curator-agent  # Index cleared content
  - research-agent        # Literature review storage
  - knowledge-agent       # Query for support answers

emits_events:
  - notebook_extracted    # After extract completes
  - notebook_analyzed     # After analysis completes
  - notebook_saved        # After save + blackboard write
  - notebook_full_mode    # When Docker upgrade detected

listens_to:
  - civ_ticket_received   # content_intake trigger
  - enrichment_requested  # OD&L training-agent trigger

session:
  enabled: true
  schema: "corp/memory/agents/notebook_agent_session.json"
  ttl_minutes: 120
  store: "ops/runtime/notebooks/sessions/"

memory:
  agent_memory: "corp/memory/agents/notebook_agent.md"
  dept_memory: "corp/memory/departments/content_intake.md"
  notebook_store: "ops/runtime/notebooks/"
  blackboard: "ops/runtime/blackboard.json"

llm_routing:
  extract: "economy"         # Fast, cheap — text extraction only
  summarize: "summary"       # claude-haiku / gpt-4o-mini
  analyze_deep: "analysis"   # claude-opus for deep analysis
  classify: "classification" # gpt-4o-mini / haiku

rules:
  - "NEVER process content that has not passed CIV intake (RULE CIV-01)"
  - "ALWAYS write analysis to blackboard after save (blackboard_lock)"
  - "ALWAYS log session events to ops/runtime/notebooks/sessions/"
  - "PREFER local LLM (Ollama) for sensitive documents"
  - "FALL BACK to extractive summary if no LLM is available"
  - "Docker full mode auto-detected — no manual switch needed"

ci:
  test_script: "tools/clawtask/tests/test_notebook_agent.py"
  health_endpoint: "GET /api/notebook/mode"
  expected_mode: "lite"  # Always passes even without Docker
---

# 📓 Notebook Agent Skill

Core content processing engine for AI OS. Always available as the **lite agent**.
Upgrades automatically to **full Nova Agent** when Docker is running.

## When to Use

Trigger this skill when an agent needs to:
- Extract text from a PDF, URL, or raw text block
- Summarize or analyze a document with LLM assistance
- Save analysis results to AI OS knowledge store
- Query a previously saved notebook for answers
- Check mode status (lite vs. full)

## Usage Pattern

### 1. Content Intake Flow (doc-parser-agent / web-crawler-agent)

```bash
# Step 1: Extract
POST /api/notebook/extract
{
  "source": "QUARANTINE/incoming/documents/report.pdf",
  "type": "pdf",
  "civ_ticket": "CIV-2026-03-22-001"
}

# Step 2: Analyze
POST /api/notebook/analyze
{
  "source": "QUARANTINE/incoming/documents/report.pdf",
  "type": "pdf",
  "prompt": "Classify VALUE_TYPE per CIV-09. Summarize key points.",
  "save": true
}

# Step 3: Route result using VALUE_TYPE from analysis
```

### 2. Research Agent Flow (research-agent / academic-researcher)

```bash
POST /api/notebook/analyze
{
  "source": "https://arxiv.org/abs/...",
  "type": "url",
  "prompt": "Extract research findings, methodology, and applicability to AI OS",
  "save": true
}
```

### 3. Support Agent Query (knowledge-agent)

```bash
GET /api/notebook/list
# Find relevant notebook by title/tags

GET /api/notebook/<id>
# Retrieve full content for answer synthesis
```

### 4. Strategy / Competitive Research (market-agent / cognitive_reflector)

```bash
POST /api/notebook/analyze
{
  "source": "https://competitor.com/pricing",
  "type": "url",
  "prompt": "Identify competitive positioning, pricing model, feature gaps vs AI OS"
}
```

## Mode Detection

```
GET /api/notebook/mode →
{
  "mode": "lite",          # or "full" when Docker up
  "departments": {
    "llm_router": true,
    "blackboard": true,
    "telegram": false      # activate via MASTER.env token
  },
  "capabilities": ["PDF extract", "URL extract", "analyze", "save", "list"],
  "llm": {"provider": "9router"}  # or "ollama", or {} (extractive fallback)
}
```

## Blackboard Write Format

After every `save`, the skill writes to `blackboard.json`:

```json
{
  "notebook_<id>": {
    "title": "...",
    "source": "...",
    "summary": "first 500 chars...",
    "ts": "2026-03-22T01:00:00"
  },
  "last_notebook_id": "<id>"
}
```

All agents that read `blackboard.json` gain automatic awareness of the latest analysis.

## LLM Routing

| Task | Route Key | Model (default) |
|------|-----------|-----------------|
| Fast extraction | `economy` | minimax-text / qwen-fast |
| Summarize | `summary` | claude-haiku |
| Deep analysis | `analysis` | claude-opus |
| Classify VALUE_TYPE | `classification` | gpt-4o-mini |
| Sensitive docs | local_fallback | deepseek-reason (local) |

## Error Handling

| Error | Response |
|-------|----------|
| PDF extraction fails | Return `{error, fallback: "plain text mode"}` |
| LLM unavailable | Extractive summary (sentences scored by TF-IDF) |
| Blackboard lock timeout | Log warning, continue (non-blocking) |
| Docker full mode fails | Graceful fallback to lite mode |
