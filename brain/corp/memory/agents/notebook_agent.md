# Notebook Agent — Always-Load Memory
# Version: 2.0 | Updated: 2026-03-22
# Load at boot for: doc-parser-agent, web-crawler-agent, knowledge-agent,
#                   research-agent, knowledge-curator-agent, learning-curator-agent

---

## IDENTITY & ROLE

Notebook Agent = AI OS built-in content processing engine.
Always available. No Docker required.
Single entry point at PORT 7474 → /api/notebook/*

---

## CURRENT MODE (runtime-check required)

GET http://localhost:7474/api/notebook/mode

Lite mode:  Always on. Extract + Analyze + Save + List.
Full mode:  Docker + open-notebook running. Nova Agent, RAG, web UI.
Offline:    No ClawTask running. Cannot use notebook API.

---

## API CHEATSHEET

| Task | Endpoint |
|------|----------|
| Check mode | GET /api/notebook/mode |
| Extract text | POST /api/notebook/extract |
| Analyze & summarize | POST /api/notebook/analyze |
| Save result | POST /api/notebook/save |
| List notebooks | GET /api/notebook/list |
| Get notebook | GET /api/notebook/<id> |

---

## NOTEBOOK STORE

Local path: ops/runtime/notebooks/
Sessions:   ops/runtime/notebooks/sessions/
Blackboard: ops/runtime/blackboard.json (key: "notebook_<id>", "last_notebook_id")

---

## RULES TO REMEMBER

- Only process content that passed CIV intake (RULE CIV-01)
- Always write to blackboard after save
- For sensitive/confidential docs: request local LLM (prefer_local: true)
- PDF needs pypdf installed: pip install pypdf>=4.0.0
- Extractive fallback always available — never fail silently
- Docker auto-detected — never manually override mode

---

## CONNECTED DEPARTMENTS

| Dept | Agent | Uses Notebook For |
|------|-------|-------------------|
| content_intake | doc-parser-agent | Extract PDF/DOCX |
| content_intake | web-crawler-agent | Extract URL |
| asset_library | knowledge-curator-agent | Index after intake |
| support | knowledge-agent | Query saved notebooks |
| rd | research-agent | Store literature review |
| strategy | market-agent | Competitive analysis |
| od_learning | learning-curator-agent | Store retro insights |

---

## LLM ROUTING DEFAULTS

Summarize → summary route (claude-haiku / qwen-fast local)
Deep analysis → analysis route (claude-opus)
Classify → classification route (gpt-4o-mini)
Sensitive → local_fallback (deepseek-reason)

---

## ENRICHMENT LOG

[DATE-ENHANCED: 2026-03-22] — Initial memory created.
  Connected: llm_router, blackboard_lock, telegram_notify
  Mode: 2-tier (lite always-on + Docker full extension)
