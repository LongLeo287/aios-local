# AI OS Notebook Agent — Workflow
# Version: 1.0 | Updated: 2026-03-22
# Owner: content_intake (primary trigger), all depts (consumers)
# Tool: Notebook Agent Skill → POST /api/notebook/*
# SLA: extract < 30s | analyze < 120s | save < 5s

---

## OVERVIEW

This workflow defines the complete lifecycle of content through the
AI OS Notebook Agent — from raw input to indexed knowledge.

```
RAW CONTENT (PDF / URL / text)
        │
        ▼
[STEP 1: EXTRACT]
  POST /api/notebook/extract
  Returns: {text, word_count}
        │
        ▼
[STEP 2: ANALYZE]
  POST /api/notebook/analyze
  LLM Route: summary → analysis (if deep requested)
  Returns: {summary, key_points, value_types}
        │
        ▼
[STEP 3: VALIDATE VALUE_TYPE]
  content-validator-agent reads analysis output
  Assigns VALUE_TYPE per CIV-09 + VALUE_ASSESSMENT_ROUTING.md
        │
        ▼
[STEP 4: SAVE]
  POST /api/notebook/save  (if save: true)
  Writes to: ops/runtime/notebooks/<id>.json
  Updates: ops/runtime/blackboard.json
  Sends: Telegram alert (if token set)
        │
        ▼
[STEP 5: ROUTE]
  ingest-router-agent reads VALUE_TYPE from analysis
  Routes per ROUTING MATRIX:
    KNOWLEDGE   → asset_library (knowledge-curator-agent)
    SKILL       → registry_capability (skill-creator-agent)
    WORKFLOW    → operations (archivist-agent)
    RULE_POLICY → rule-builder-agent → COO
    PLUGIN      → registry_capability (plugin-librarian-agent)
    MCP_SERVER  → it_infra (sysadmin-agent)
    DATA_ASSET  → asset_library (asset-tracker-agent)
        │
        ▼
[STEP 6: INDEX]
  knowledge-curator-agent indexes notebook into knowledge/
  Updates: knowledge/knowledge_index.md
  Blackboard entry visible to all agents
```

---

## TRIGGER CONDITIONS

| Trigger | Source Agent | Session Context |
|---------|-------------|-----------------|
| New CIV ticket with DOCUMENT type | intake-agent | civ_ticket ID |
| New CIV ticket with WEB_CONTENT type | intake-agent | civ_ticket ID |
| Research task created by rd dept | research-agent | task_id |
| Competitive analysis requested | market-agent / cognitive_reflector | project_id |
| Retro learning extraction | learning-curator-agent | cycle_id |
| Support query needing KB | knowledge-agent | ticket_id |

---

## AGENT HANDOFF PROTOCOL

### content_intake → notebook_agent → ingest-router-agent

```
intake-agent creates ticket: CIV-YYYY-MM-DD-NNN
        ↓
doc-parser-agent / web-crawler-agent:
  POST /api/notebook/extract {source, type, civ_ticket}
  POST /api/notebook/analyze {source, type, prompt, save: true}
        ↓
Returns: {summary, key_points, value_types, notebook_id}
        ↓
content-validator-agent:
  Reads analysis → Assigns final VALUE_TYPE
  Writes VALIDATION RESULT to ticket
        ↓
ingest-router-agent:
  Routes using VALUE_TYPE routing matrix
  Updates ticket: INGESTED or ENRICHMENT_PENDING
```

### rd / strategy → notebook_agent (research flow)

```
research-agent or market-agent:
  POST /api/notebook/analyze {source: URL, type: url, prompt: research_prompt}
        ↓
Result saved to notebook store
Blackboard updated: notebook_<id>
        ↓
knowledge-curator-agent reads blackboard
  → Adds to knowledge/research/<domain>/
```

---

## SESSION MANAGEMENT

Sessions are tracked per `session_id` in `ops/runtime/notebooks/sessions/`.

Multi-turn example (knowledge-agent doing iterative research):
```
Session: sess-001
Turn 1: /extract {source: doc1.pdf}       → text extracted
Turn 2: /analyze {prompt: "key findings"} → summary
Turn 3: /analyze {prompt: "methodology"}  → deeper analysis
Turn 4: /save {title: "Research Report"}  → saved + blackboard
```

Session expires: 120 minutes inactivity.
Completed sessions archived to `ops/runtime/notebooks/sessions/archive/`.

---

## ERROR HANDLING

| Situation | Fallback |
|-----------|---------|
| LLM unavailable | Extractive summary (TF-IDF, 3-5 sentences) |
| PDF parse fails | Try plain text mode, log warning |
| Blackboard lock timeout | Log warning, skip (non-blocking) |
| Docker full mode fails | Auto-fallback to lite — no interruption |
| Network URL unreachable | Return error, update CIV ticket to PENDING |

---

## MONITORING

health check: GET http://localhost:7474/api/notebook/mode
Expected response: {"mode": "lite", ...} — HTTP 200

Metrics to track (process-monitor-agent):
- notebook_extracted events per cycle
- notebook_analyzed events per cycle
- Average LLM response time per analyze call
- Blackboard write success rate
- Session error rate
