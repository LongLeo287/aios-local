# Department: operations
# corp-task-flow.md — CEO → C-Suite → Manager → Worker → QA Flow
# Version: 1.0 | Updated: 2026-03-17
# Authority: Tier 2 (Operations) / Corp Mode

---

## Overview

This workflow defines how a single piece of work flows through all 5 levels
of AI OS Corp from conception to completion.

```
CEO           ──► WRITE MISSION + PRIORITIES
    │
C-SUITE       ──► TRANSLATE TO DEPT GOALS
    │
DEPT MANAGER  ──► CREATE TASK CARD + ASSIGN WORKER
    │
WORKER        ──► EXECUTE + WRITE RECEIPT
    │
GATE          ──► REVIEW (if qa_required)
    │
MANAGER       ──► RECEIVE RESULT + UPDATE BRIEF
    │
C-SUITE       ──► KPI UPDATE + REPORT TO CEO
    │
CEO           ──► READ RESULTS + NEXT DECISION
```

---

## Step 1: CEO → Mission

CEO writes to `shared-context/corp/mission.md`:
```markdown
## Mission — [DATE]
Strategic Focus: [1-2 sentences]
Priorities this cycle:
  1. [Dept]: [specific goal]
  2. [Dept]: [specific goal]
  3. [Dept]: [specific goal]
Budget constraint: [any cost controls]
Deadline: [if applicable]
```

---

## Step 2: C-Suite → Department Specs (Spec-Driven Intent)

Each C-Suite member reads mission → translates to concrete Spec-Driven Intents:

```
CTO reads → Engineering, QA, IT Specs
CMO reads → Marketing, Support, Content Specs
COO reads → Operations, HR, Security Specs
CFO reads → Finance budget constraints
CSO reads → Strategy, Legal, R&D Specs
```

C-Suite writes to `shared-context/blackboard.json` for each dept:
```json
{
  "dept": "<dept-name>",
  "cycle": "N",
  "spec_intent": "<concise what-to-build spec>",
  "kpi_targets": ["<metric>: <value>"],
  "priority": "HIGH | MEDIUM | LOW",
  "deadline": "<date or ASAP>"
}
```

---

## Step 3: Manager → Spec Card

Dept head reads blackboard → creates actionable Spec Cards for Workers (never micromanage "how" to code, only provide "what" the spec requires):

Write to `subagents/mq/<dept>_tasks.md`:
```markdown
## Spec Card: <ID> — <title>
Assigned to: <worker-agent>
Dept: <dept>
Context: <2-3 sentences of context (include memory reference if relevant)>
Spec / Acceptance Criteria:
  - [ ] <requirement 1>
  - [ ] <requirement 2>
Deadline: <estimate>
LLM tier: economy | balanced | premium
QA required: true | false
Output path: <where to write the output>
Skills suggested: [<skill-id>]
```

---

## Step 4: Worker → Execution

Worker reads task card → executes WORKER_PROMPT.md loop:

```
1. Load SKILL matching task type
2. <thought> dry-run plan </thought>
3. Execute in atomic steps
4. Verify against acceptance criteria
5. Write receipt to telemetry/receipts/<dept>/<T-ID>.json
6. Update task card status: DONE | FAILED
7. If qa_required: true → route to gate
8. If FAILED (2-strike) → write L1 escalation
```

---

## Step 5: Gate Review (if qa_required)

```
Add item to correct gate queue:
  GATE_QA       → subagents/mq/qa_review_queue.md
  GATE_CONTENT  → subagents/mq/gate_content_queue.md
  GATE_SECURITY → automatic (security_grc monitors autonomously)
  GATE_LEGAL    → subagents/mq/legal_review_queue.md

Gate agent runs checklist from APPROVAL_GATES.md:
  PASS        → notify manager. Proceed.
  FAIL        → return to worker with specific fixes required
  CONDITIONAL → proceed with stated conditions

Receipt stored: telemetry/qa_receipts/<gate>/<T-ID>.json
```

---

## Step 6: Manager → Brief Update

After all tasks complete (or cycle ends):
```
Manager writes:
- Updated task statuses in subagents/mq/<dept>_tasks.md
- Daily brief to shared-context/corp/daily_briefs/<dept>.md
- Lesson to corp/memory/departments/<dept>.md (if learned anything)
- Any L2 escalations to shared-context/corp/escalations.md
```

---

## Step 7: C-Suite → KPI Update

```
C-Suite reads all dept briefs in their domain:
1. Update kpi_scoreboard.json with actual values
2. Flag any yellow/red KPIs
3. Write C-Suite dispatch summary
4. Escalate L3 items to CEO if any
```

---

## Step 8: CEO → Decision

CEO reads:
- `shared-context/corp/kpi_scoreboard.json`
- `shared-context/corp/escalations.md`
- `shared-context/corp/proposals/`

CEO decides:
- APPROVE items → log to decisions_log.md
- REJECT with reason → escalations.md response
- DEFER with ETA
- Set next cycle priorities → update mission.md

---

## Task ID Convention

```
<DEPT-ABBR>-<CYCLE>-<SEQ>

Examples:
  ENG-01-001  → Engineering, Cycle 1, Task 1
  MKT-01-003  → Marketing, Cycle 1, Task 3
  SEC-02-001  → Security, Cycle 2, Task 1
  HR-01-002   → HR, Cycle 1, Task 2
```

---

*"A task that doesn't flow through the hierarchy isn't a corporate task. It's chaos."*
