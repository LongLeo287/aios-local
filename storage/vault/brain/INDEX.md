# KHO BRAIN — Knowledge Index
# Version: 1.0 | 2026-03-24 | Owner: asset_library + rd
# Index of all brain/ content — knowledge, agents, shared-context

---

## SHARED CONTEXT (brain/shared-context/)

| File | Purpose | Updated By |
|------|---------|-----------|
| blackboard.json | Active tasks + corp state | All agents |
| SOUL.md | Identity + values | CEO |
| GOVERNANCE.md | Authority structure | CEO |
| AGENTS.md | Agent roster (redirect to brain/agents/) | registry_capability |
| THESIS.md | 40 pillars + strategy | CEO |
| SKILL_REGISTRY.json | All 14+ skills index | skill-discovery-auto |
| FAST_INDEX.json | Optimized skill lookup | skill-discovery-auto |
| report_formats.md | Output format templates | Antigravity |
| corp/ | KPI, mission, escalations, proposals, briefs | C-Suite + dept heads |

## KNOWLEDGE NOTES (brain/knowledge/notes/)

Naming: `RULE-<ID>.md`, `KI-<TOPIC>-<ID>.md`

| File Pattern | Purpose |
|-------------|---------|
| RULE-STORAGE-01-*.md | Storage location rule |
| RULE-STRUCTURE-01-*.md | System structure rule |
| RULE-DYNAMIC-01-*.md | No-hardcode rule |
| KI-*.md | Knowledge items from research/analysis |

## AGENT DEFINITIONS (brain/agents/)

48 agent definition files — each defines:
- Agent name, role, authority level
- Tools available
- Memory path
- Escalation path

## LIGHTRAG DATABASE (brain/knowledge/lightrag_db/)

Created by: `python ops/scripts/lightrag_server.py` then POST /init
Index type: Hybrid (local + global graph)
Working dir: brain/knowledge/lightrag_db/
Query via: POST http://localhost:9621/query { "query": "...", "mode": "mix" }

## ADDING TO BRAIN

1. Knowledge item: brain/knowledge/notes/KI-<topic>-<id>.md
2. After writing: index via POST http://localhost:9621/insert (if LightRAG running)
3. Registry entry: update kho/brain/registry.json (future)
4. For skills: use skill-discovery-auto.md to auto-index

## BRAIN HEALTH CHECK

- LightRAG running? GET http://localhost:9621/health → { "status": "ok" }
- LightRAG initialized? POST http://localhost:9621/init
- Query test: POST http://localhost:9621/query { "query": "test", "mode": "local" }
