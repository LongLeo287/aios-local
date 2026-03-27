---
name: observability
description: Track and visualize all LLM calls, tool invocations, and agent actions across AI OS Corp. Supports Langfuse (self-hosted/local) AND LangSmith (cloud). Zero configuration required — noop fallback if not set up.
---

# Observability — AI OS Corp Tracing Layer

## Overview
Dual-mode observability for AI OS:
- **Langfuse** (self-hosted Docker) → local, private, free
- **LangSmith** (cloud) → hosted dashboard, free tier
- **Noop** → zero-config fallback (logs only to console)

## Quick Start — Langfuse Local (Recommended)

### Step 1: Start Langfuse
```bash
cd infra/observability
docker compose up -d
# → Dashboard at http://localhost:3000
# Default login: admin@langfuse.com / password
```

### Step 2: Get API Keys
1. Open http://localhost:3000
2. Go to Settings → API Keys
3. Create Public Key + Secret Key

### Step 3: Add to MASTER.env
```bash
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=http://localhost:3000
OBSERVABILITY_MODE=langfuse
```

### Step 4: Install Python SDK
```bash
pip install langfuse
```

That's it! All instrumented services auto-send traces on next call.

---

## Quick Start — LangSmith Cloud

### Step 1: Get API Key
1. Go to smith.langchain.com
2. Create account → Settings → API Keys

### Step 2: Add to MASTER.env
```bash
LANGSMITH_API_KEY=ls__...
LANGSMITH_PROJECT=ai-os-corp
OBSERVABILITY_MODE=both  # Run langfuse+langsmith simultaneously
```

### Step 3: Install SDK
```bash
pip install langsmith
```

---

## What Gets Traced Automatically

| Service | What's Tracked |
|---------|---------------|
| Firecrawl | scrape_url, crawl_site, extract_structured calls |
| Mem0 | add, search, on_task_start, on_task_complete |
| LightRAG | insert, query (4 modes) |
| CrewAI | Crew runs, agent steps (via LangChain auto-trace) |
| Any @trace decorated function | Inputs, outputs, latency, errors |

## Instrument Custom Code
```python
# Decorator pattern
from plugins.observability.observability_adapter import trace

@trace("my_tool.process")
def process_data(data):
    return result

# Context manager
from plugins.observability.observability_adapter import get_obs

with get_obs().span("custom.operation") as span:
    result = do_something()
    span.update(output=result)

# LLM call logging
get_obs().trace_llm(
    name="claude.chat",
    model="claude-3-5-sonnet",
    input_text=prompt,
    output_text=response,
    tokens_in=850,
    tokens_out=240,
    latency_ms=1200
)
```

## Dashboard Features (Langfuse)
- **Trace list** — every LLM call with input/output
- **Latency charts** — P50/P95/P99 response times
- **Token usage** — cost tracking per model
- **Error rates** — failed calls highlighted
- **Session grouping** — all calls in a Corp Cycle grouped together

## Notes
- `telemetry_enabled: false` in docker-compose → usage stats NOT shared with Langfuse
- All data stays on your machine (self-hosted)
- Source: Langfuse MIT License | LangSmith proprietary free tier
- Owner: Dept 1 (Engineering) + Dept 15 (Finance — for cost tracking)
