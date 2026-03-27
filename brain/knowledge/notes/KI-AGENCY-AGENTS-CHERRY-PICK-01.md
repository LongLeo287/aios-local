# Knowledge Note: Agency Agents — Cherry-Picked Skills for AI OS
# Source: plugins/agency-agents (MIT License) — 144 agents, 12 divisions
# Extracted: 2026-03-23 | By: Antigravity (Knowledge Extraction Pass)
# Status: CHERRY-PICK — Selected agents imported as Skills. Full tool NOT integrated.

---

## Overview
agency-agents contains 144 specialized agent personalities across 12 divisions.
**Key insight:** These are PROMPT TEMPLATES (agent personalities), not code. We can
directly cherry-pick the ones that fill gaps in AI OS Corp's agent roster.

**Gap Analysis — What AI OS Agents LACK vs agency-agents:**

| Division | Gap in AI OS | agency-agents Template to Cherry-Pick |
|----------|-------------|--------------------------------------|
| Engineering | No dedicated Code Reviewer | `engineering-code-reviewer.md` |
| Engineering | No Git Workflow specialist | `engineering-git-workflow-master.md` |
| Engineering | No Database Optimizer | `engineering-database-optimizer.md` |
| Engineering | No Incident Response | `engineering-incident-response-commander.md` |
| Testing | No Evidence Collector (screenshot QA) | `testing-evidence-collector.md` |
| Testing | No Accessibility Auditor | `testing-accessibility-auditor.md` |
| Testing | No Performance Benchmarker | `testing-performance-benchmarker.md` |
| Product | No Behavioral Nudge Engine | `product-behavioral-nudge-engine.md` |
| Specialized | No MCP Builder | `specialized-mcp-builder.md` |
| Specialized | No Workflow Architect | `specialized-workflow-architect.md` |
| Specialized | No Agentic Identity Architect | `specialized-agentic-identity-trust.md` |
| Marketing | No AI Citation Strategist (AEO/GEO) | `marketing-ai-citation-strategist.md` |

---

## Immediate Cherry-Picks (High Value, Low Risk)

### 1. Code Reviewer Agent (Engineering)
**File:** `plugins/agency-agents/engineering/engineering-code-reviewer.md`
**Gap filled:** AI OS QA team reviews output but no dedicated code review agent in Engineering dept.
**Action:** Import personality + workflow into `corp/departments/engineering/` as new worker sub-agent.

### 2. Incident Response Commander (Engineering/SRE)
**File:** `plugins/agency-agents/engineering/engineering-incident-response-commander.md`
**Gap filled:** AI OS has SRE role but no formalized Incident Management workflow.
**Action:** Import into `corp/departments/engineering/` + create `ops/workflows/incident-response.md`.

### 3. Evidence Collector — Screenshot QA (Testing)
**File:** `plugins/agency-agents/testing/testing-evidence-collector.md`
**Gap filled:** QA gate has no visual proof protocol. This agent enforces "screenshot before close".
**Action:** Import into `corp/departments/qa_testing/` + add screenshot requirement to qa-gate.md.

### 4. MCP Builder (Specialized)
**File:** `plugins/agency-agents/specialized/specialized-mcp-builder.md`
**Gap filled:** AI OS has MCP tools but no agent specialized in BUILDING new MCP servers.
**Action:** Import into `brain/agents/` as on-demand specialized agent.

### 5. Workflow Architect (Specialized)
**File:** `plugins/agency-agents/specialized/specialized-workflow-architect.md`
**Gap filled:** AI OS needs an agent that maps ALL paths through a system before code is written.
**Action:** Import into `brain/agents/` as on-demand planning agent.

### 6. AI Citation Strategist (Marketing)
**File:** `plugins/agency-agents/marketing/marketing-ai-citation-strategist.md`
**Gap filled:** AEO/GEO — making AI OS Corp visible in ChatGPT/Claude/Gemini answers.
**Action:** Import into `corp/departments/marketing/` as new worker.

---

## Key Philosophy Extracted (Apply to All AI OS Agents)

1. **Deep Specialization > Generic** — Each agent has ONE very specific role, not "do everything".
2. **Personality-Driven** — Agents have a "voice" and communication style, not just instructions.
3. **Deliverable-Focused** — Every agent specifies CONCRETE outputs, not vague "help with X".
4. **Success Metrics** — Each agent defines measurable quality standards.
5. **Proven Workflows** — Step-by-step processes that have been battle-tested in production.

**Apply this to AI OS Worker Prompts:** Each WORKER_PROMPT.md should have a "Success Metrics" section listing measurable acceptance criteria. Currently missing in most depts.

---

## Integration Instructions for agency-agents Cherry-Picks

```
1. Open source file: plugins/agency-agents/<division>/<agent-file>.md
2. Extract: Identity, Core Mission, Critical Rules, Technical Deliverables, Workflow
3. Create new file: corp/departments/<dept>/<new-worker-name>.md
4. Adapt: Replace LangChain/Claude-specific references with AI OS patterns
5. Register: Add to org_chart.yaml as new worker under target dept
6. Update: SKILL_REGISTRY.json with new agent skill entry
```

---

*Do NOT run agency-agents install scripts (they target ~/.claude/agents/ not AI OS Corp structure)*
*Cherry-pick TEMPLATES ONLY — adapt to AI OS format, not copy-paste verbatim.*
