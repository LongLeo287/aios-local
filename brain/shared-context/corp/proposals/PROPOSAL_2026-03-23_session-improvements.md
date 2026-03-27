# CEO Proposals — 2026-03-23
# Source: RETRO_2026-03-23.md
# Written by: strategy/product-manager-agent (Antigravity)
# Status: PENDING CEO DECISION

---

## PROP-2026-03-23-001 — Agent Cherry-Pick from agency-agents
**Priority:** HIGH
**Type:** AGENT_ROSTER_CHANGE
**Context:** Session 2026-03-23 identified 6 agent roles missing from AI OS Corp roster. Source: `plugins/agency-agents` (144 agents, MIT License, battle-tested).
**Proposal:**
Import the following 6 agent templates (adapt to AI OS format — NOT install scripts):
1. Code Reviewer → `corp/departments/engineering/` (Dept 1)
2. Incident Response Commander → `corp/departments/engineering/` + `ops/workflows/incident-response.md`
3. Evidence Collector (Screenshot QA) → `corp/departments/qa_testing/` (Dept 2)
4. MCP Builder → `brain/agents/` (on-demand)
5. Workflow Architect → `brain/agents/` (on-demand)
6. AI Citation Strategist (AEO/GEO) → `corp/departments/marketing/` (Dept 6)
**Effort:** Medium (1 session)
**Impact:** Fill structural gaps in Engineering, QA, Marketing depts.
**Decision needed:** APPROVE / DEFER / REJECT

---

## PROP-2026-03-23-002 — Agent Architecture Patterns → WORKER_PROMPTs
**Priority:** MEDIUM
**Type:** NEW_SKILL / PROMPT_UPGRADE
**Context:** Session 2026-03-23 extracted 17 agent architecture patterns. 5 patterns can be immediately applied to existing WORKER_PROMPTs to improve output quality.
**Proposal:**
1. **Reflection Step** — Add to Legal, Strategy, Architecture WORKER_PROMPTs: "Review your output against acceptance criteria and revise once before submitting."
2. **Ensemble for CEO Proposals** — Never single-agent proposals. Before writing a PROPOSAL: run through R&D + Strategy + Legal agents, cognitive_reflector synthesizes.
3. **Metacognitive Escalation Rule** — Add to ALL WORKER_PROMPTs: "If confidence < 70%, write L1 escalation instead of proceeding."
4. **PEV acceptance criteria** — Strengthen QA gate: require explicit acceptance criteria on every task card.
5. **Tree of Thoughts** — For multi-option CEO decisions, generate 3+ paths and present comparison.
**Effort:** Low (update prompts in 1 session)
**Impact:** Higher quality outputs, fewer gate failures, fewer L1 escalations.
**Decision needed:** APPROVE / DEFER / REJECT

---

## PROP-2026-03-23-003 — Knowledge Graph Community Clustering
**Priority:** MEDIUM
**Type:** NEW_SKILL
**Context:** GraphRAG review revealed LightRAG lacks community detection (thematic clustering). After OPEN-004 completes, this would improve global reasoning queries.
**Proposal:**
1. Create `brain/knowledge/communities/` folder.
2. After `index_brain_knowledge()` runs, group top entities into thematic communities:
   - Agent_Architecture, Security_Policies, Plugin_Ecosystem, Corp_Operations, Knowledge_Pipeline
3. Write summary MD per community for faster global queries.
**Effort:** Low-Medium
**Dependencies:** OPEN-004 (LightRAG PoC) must complete first.
**Decision needed:** APPROVE (begin after OPEN-004) / DEFER / REJECT

---

*Proposals ready for CEO review in next Corp Cycle Phase 1*
*Filed: 2026-03-23T15:55:00+07:00*
