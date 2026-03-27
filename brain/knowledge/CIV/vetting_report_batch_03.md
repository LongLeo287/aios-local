# CIV Vetting Report — Batch 3
# Analyst: Content-Analyst-Agent | Dept 06 (Content Review)
# Date: 2026-03-18 | Gate: GATE_CONTENT
# Status: COMPLETE — 10 repos scanned

---

## Executive Summary

Batch 3 covers 10 high-star public repos với focus trên AI framework, RAG, data ingestion, và UI tools. **9/10 APPROVED** for ingestion. **1/10 CONDITIONAL** (license review cần).

---

## Scan Results

| # | Repo | Stars | License | Score | Decision |
|---|------|-------|---------|-------|----------|
| 1 | firecrawl | 94,585 ⭐ | AGPL-3.0 | 82 | ✅ APPROVED — knowledge/ |
| 2 | crewAI | 46,407 ⭐ | MIT | 95 | ✅ APPROVED — plugins/ |
| 3 | lobe-chat | 73,884 ⭐ | Other | 85 | ✅ APPROVED — plugins/ (existing) |
| 4 | LightRAG | 29,524 ⭐ | MIT | 93 | ✅ APPROVED — plugins/ |
| 5 | AstrBot | 25,703 ⭐ | AGPL-3.0 | 78 | ✅ APPROVED — knowledge/ |
| 6 | gitingest | 14,174 ⭐ | MIT | 90 | ✅ APPROVED — plugins/ (existing) |
| 7 | cognee | 14,301 ⭐ | Apache-2.0 | 91 | ✅ APPROVED — plugins/ |
| 8 | lenis | 13,371 ⭐ | MIT | 88 | ✅ APPROVED — knowledge/ (existing) |
| 9 | public-apis | 411,689 ⭐ | MIT | 87 | ✅ APPROVED — knowledge/ |
| 10 | awesome-claude-skills | 45,481 ⭐ | **NO LICENSE** | 72 | ⚠️ CONDITIONAL — GATE_LEGAL pending |

---

## Detailed Assessments

### 1. firecrawl — Score: 82 | ✅ APPROVED
- **Org**: firecrawl (official org)
- **Lang**: TypeScript | **Updated**: 2026-03-18 (active)
- **Description**: Web Data API for AI — Turn websites into LLM-ready markdown
- **Stars**: 94,585 | **Forks**: 6,492
- **License**: AGPL-3.0 — sử dụng reference-only, không embed trong commercial product
- **CIV Notes**: Core tool cho Data-Collector và R&D pipeline. Conflict check: bổ sung cho `gitingest` (repo-level) — firecrawl handles live web, gitingest handles static repos. **No conflict.**
- **Recommendation**: `knowledge/repos/firecrawl-ref` — reference cho web ingestion patterns
- **Dept**: R&D (Dept 13)

---

### 2. crewAI — Score: 95 | ✅ APPROVED (PRIORITY)
- **Org**: crewAIInc (official)
- **Lang**: Python | **Updated**: 2026-03-18 (very active)
- **Description**: Framework for orchestrating role-playing, autonomous AI agents
- **Stars**: 46,407 | **Forks**: 6,260
- **License**: MIT — commercial-friendly ✅
- **CIV Notes**: Already in `plugins/crewai` as reference. Score upgraded from previous listing — confirm MIT license valid. **Sangat phù hợp với AI OS Corp multi-agent model.**
- **Confidence**: crewAI là operational backbone option cho future Corp orchestration
- **Recommendation**: Upgrade to `plugins/crewai` — T2 Skill Tier
- **Dept**: Engineering (Dept 01)

---

### 3. lobe-chat — Score: 85 | ✅ APPROVED (Already in catalog)
- **Org**: lobehub (official)
- **Lang**: TypeScript | **Updated**: 2026-03-18
- **Description**: Multi-agent collaboration, MCP support, AI chat UI
- **Stars**: 73,884 | **Forks**: 14,796
- **License**: Other (custom) — cần check lobehub ToS cho embedding
- **CIV Notes**: Đã có trong catalog. Confirm tiếp tục là reference UI. MCP support = tích hợp trực tiếp với AI OS MCP layer.
- **Recommendation**: Keep as `plugins/lobe-chat` — verify license before production use
- **Dept**: Engineering/UI (Dept 01)

---

### 4. LightRAG — Score: 93 | ✅ APPROVED (PRIORITY)
- **Org**: HKUDS (Hong Kong University)
- **Lang**: Python | **Updated**: 2026-03-18 (very active)
- **Description**: Simple and Fast Retrieval-Augmented Generation (EMNLP 2025 paper)
- **Stars**: 29,524 | **Forks**: 4,228
- **License**: MIT ✅ — academic + commercial
- **CIV Notes**: Đây là state-of-the-art RAG với Graph + Vector hybrid. **Đây là upgrade tier từ openrag/nexusrag trong catalog.**
- **Recommendation**: Promote từ `plugins/LightRAG` (existing) → T2 Skill Tier — **PRIMARY RAG ENGINE**
- **Dept**: Engineering/AI-ML (Dept 01)

---

### 5. AstrBot — Score: 78 | ✅ APPROVED
- **Org**: AstrBotDevs
- **Lang**: Python | **Updated**: 2026-03-18 (active)
- **Description**: Agentic IM Chatbot infrastructure — TG/DC/QQ/WeChat + MCP + LLM
- **Stars**: 25,703 | **Forks**: 1,750
- **License**: AGPL-3.0 — reference only ⚠️
- **CIV Notes**: Interesting — description says "can be your openclaw alternative." Có conflict với `nullclaw`/`tinyclaw` potential. Tuy nhiên vì AI OS đã có gateway riêng, AstrBot nên là **knowledge reference** không phải plugin.
- **Open Issues**: 829 — khá cao, project còn busy
- **Recommendation**: `knowledge/repos/astrbot-ref` — alternative gateway research
- **Dept**: R&D (Dept 13) / Support (Dept 05)

---

### 6. gitingest — Score: 90 | ✅ APPROVED (Already in catalog)
- **Org**: coderamp-labs
- **Lang**: Python | **Updated**: 2026-03-17
- **Description**: Replace 'hub' with 'ingest' in GitHub URL → LLM-ready extract
- **Stars**: 14,174 | **Forks**: 1,044
- **License**: MIT ✅
- **CIV Notes**: Core tool đã trong catalog `plugins/gitingest`. Confirm T2 status. Thiết yếu cho CIV pipeline — dùng để convert repo → text digest trước khi vào NotebookLM.
- **Recommendation**: Keep `plugins/gitingest` — T2, ACTIVE
- **Dept**: R&D / CIV Pipeline

---

### 7. cognee — Score: 91 | ✅ APPROVED (PRIORITY)
- **Org**: topoteretes
- **Lang**: Python | **Updated**: 2026-03-18 (very active)
- **Description**: Knowledge Engine for AI Agent Memory in 6 lines of code
- **Stars**: 14,301 | **Forks**: 1,415
- **License**: Apache-2.0 ✅ — commercial-friendly
- **Topics**: graph-rag, knowledge-graph, neo4j, vector-database, ai-memory
- **CIV Notes**: Đây là **complement cho LightRAG** — cognee xử lý agent persistent memory, LightRAG xử lý document retrieval. Không conflict — synergistic pair.
- **Recommendation**: `plugins/cognee` — T2 Skill, **AGENT MEMORY LAYER**
- **Dept**: Engineering/AI-ML (Dept 01)

---

### 8. lenis — Score: 88 | ✅ APPROVED (Already in catalog)
- **Org**: darkroomengineering
- **Lang**: TypeScript | **Updated**: 2026-03-17
- **Description**: Smooth scroll library
- **Stars**: 13,371 | **Forks**: 530
- **License**: MIT ✅
- **CIV Notes**: Đã trong `knowledge/repos/lenis`. Premium scroll animation cho ClawTask và client-facing UIs. Non-AI utility nhưng UI-critical cho delivery pipeline.
- **Recommendation**: Keep knowledge/ — T3 UI Utility
- **Dept**: Engineering/Frontend (Dept 01)

---

### 9. public-apis — Score: 87 | ✅ APPROVED
- **Org**: public-apis (dedicated org)
- **Lang**: Python | **Updated**: 2026-02-19
- **Description**: Collective list of 1,400+ free APIs across categories
- **Stars**: 411,689 ⭐ — **#1 most-starred repo in this batch**
- **License**: MIT ✅
- **CIV Notes**: Đây là **reference goldmine** cho Research-Agent và Data-Collector. 1400+ APIs catalog = massive resource for automation, data gathering, affiliate research, market intel.
- **Recommendation**: `knowledge/repos/public-apis` — T3 Reference, **HIGH VALUE**
- **Dept**: R&D (Dept 13) / Strategy (Dept 11)

---

### 10. awesome-claude-skills — Score: 72 | ⚠️ CONDITIONAL
- **Org**: ComposioHQ
- **Lang**: Python | **Updated**: 2026-02-19
- **Stars**: 45,481 | **Forks**: 4,612
- **License**: **NO LICENSE** ⚠️
- **Topics**: antigravity, claude-code, claude, mcp, agent-skills
- **CIV Notes**: Có `antigravity` trong topics — directly relevant. Nhưng **NO LICENSE FILE** = không thể legally embed code. Content (markdown/readme) có thể reference, nhưng code extraction bị block theo CIV Rule §3.2.
- **Current Status**: Đã trong catalog như `plugins/awesome-claude-skills`
- **Action Required**: GATE_LEGAL must review — either:
  a) Confirm Composio implicit license (Apache-based org?)
  b) Downgrade to knowledge/ reference only
- **Recommendation**: ⚠️ HOLD — pending GATE_LEGAL

---

## Batch 3 Summary Stats

| Metric | Value |
|--------|-------|
| Total Scanned | 10 |
| APPROVED | 9 |
| CONDITIONAL (GATE_LEGAL) | 1 |
| New to catalog | 3 (firecrawl-ref, astrbot-ref, public-apis) |
| Existing — confirmed promoted | 3 (crewAI T2, LightRAG T2, cognee T2) |
| Total stars gained | ~723,000 ⭐ |

---

## Action Items for Registry-Manager

1. **Promote crewAI → T2** in `SKILL_REGISTRY.json`
2. **Promote LightRAG → T2 PRIMARY RAG** in `SKILL_REGISTRY.json`
3. **Add cognee → T2 AGENT MEMORY** in `SKILL_REGISTRY.json`
4. **Add to REPO_CATALOG**: `firecrawl-ref`, `astrbot-ref`, `public-apis`
5. **GATE_LEGAL**: Check `awesome-claude-skills` license status
6. **Update blackboard.json**: CIV Batch 3 COMPLETE → IDLE

---

*Report signed: Content-Analyst-Agent | Dept 06 | 2026-03-18*
*GATE_CONTENT: ✅ PASSED (pending GATE_LEGAL for item #10)*
