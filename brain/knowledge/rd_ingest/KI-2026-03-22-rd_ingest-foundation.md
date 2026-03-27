---
id: KI-2026-03-22-rd-ingest-foundation
type: REFERENCE
domain: rd_ingest
dept: all
created: 2026-03-22
foundation: true
tags: ['rd', 'research', 'ingest', 'backlog', 'pipeline']
---

# AI OS Corp — R&D Ingest Queue & Research Backlog

## R&D Ingest Tracking

### Recently Ingested (2026-03-22)
| Repo | Type | Action |
|------|------|--------|
| mem0 | TOOL | Cloned → plugins/ |
| graphrag | TOOL | Cloned → plugins/ |
| e2b | TOOL | Cloned → plugins/ |
| scrapling | TOOL | Cloned (has MCP) → plugins/ |
| lightrag | REFERENCE | KI entry only (HKUDS, 35k⭐) |
| NemoClaw | REFERENCE | KI entry (NVIDIA 4-layer sandbox) |
| ClawWork | REFERENCE | Cloned for study (HKUDS task framework) |
| prometheus-grafana | TOOL | Cloned → plugins/ (AI OS monitoring) |
| vieneu-tts | TOOL | Cloned → plugins/ (local Vietnamese TTS) |

### Ingest Workflow
See `ops/workflows/knowledge-ingest.md` for the complete 4-step process:
1. Classify: TOOL / REFERENCE / RESEARCH
2. Write KI entry to brain/knowledge/<domain>/
3. Clone only if: TOOL + compatible AI OS + standalone
4. CEO approval for high-impact repos

### Research Backlog Topics
- [ ] Agentic evaluation frameworks (AgentBench, GAIA)
- [ ] Multimodal agent vision tools
- [ ] Cost tracking / token budget management for agents
- [ ] Long-context agents (>200K tokens)

---
*Foundation KI — created 2026-03-22*
