# mem0 — AI Agent Long-term Memory Plugin
# AI OS Corp | Cognitive Plugin | v1.0.0

## Purpose

Gives AI agents (ACP, nullclaw, AgAuto) **persistent memory across sessions**.
Agents can remember user preferences, decisions, and ongoing context without re-reading every KI file.

**NOT to be confused with:**
- `claude-mem` — stores Claude Code *tool call observations* (different domain)
- `open-notebook` / `LightRAG` — document/knowledge *retrieval* (different domain)

---

## Agent Usage Guide

### When to Store Memory (`onTaskComplete`)

Store a memory when the task reveals something about the user/corp that is useful long-term:

```python
from mem0_adapter import Mem0Adapter

mem = Mem0Adapter()

# After completing a task where CEO expressed a preference
messages = [{"role": "user", "content": "Always use JSON format for reports"}]
mem.add(messages, user_id="CEO")
```

### When to Search Memory (`onTaskStart`)

At the start of each task, retrieve relevant context:

```python
# Before responding to a task
query = "CEO's preferred report format"
results = mem.search(query, user_id="CEO")
# Inject results into system prompt context
```

### Memory Categories (auto-classified by mem0)

| Category | Example |
|----------|---------|
| Preferences | "CEO wants JSON format" |
| Decisions | "Approved mem0 integration Phase 1" |
| Constraints | "Never use hidden windows for services" |
| Context | "ClawTask runs on port 7474" |

---

## Integration Points

### ACP (openclaw/src/acp)
- `onTaskStart`: Load CEO memories → inject into system prompt
- `onTaskComplete`: Extract and store new facts from conversation

### nullclaw gateway
- `onHandoff`: Package memories for cross-agent context

---

## Setup

```bash
# Install dependency
pip install mem0ai

# Test installation
python plugins/mem0/tests/test_mem0_adapter.py
```

**Config location:** `plugins/mem0/manifest.json` → `config` section

**Storage location:** `brain/memory/mem0/` (local vector store)

---

## Telemetry

Every activation logs to: `telemetry/receipts/mem0/YYYY-MM-DD.jsonl`

Format:
```json
{"timestamp": "...", "agent": "acp", "action": "search", "query": "...", "results_count": 3}
```

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-03-23 | Initial integration — ACP hooks |

---

*Security scan: CLEAR | License: Apache-2.0 | Registered: 2026-03-23*
