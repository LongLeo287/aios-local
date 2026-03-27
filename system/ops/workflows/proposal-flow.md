# Department: operations
---
description: AI OS Proposal handling workflow — từ proposal creation đến CEO decision
---
# ops/workflows/proposal-flow.md
# Version: 1.0 | 2026-03-24 | Owner: strategy + C-Suite
# Purpose: Xử lý 5 loại proposals đang pending + standard flow

---

## PROPOSAL TYPES

| Type | Owner | Format | Priority |
|------|-------|--------|----------|
| KPI_CHANGE | strategy | PROPOSAL_KPI_*.md | HIGH |
| NEW_SKILL | registry_capability | PROPOSAL_SKILL_*.md | MEDIUM |
| ROLE_CHANGE | od_learning + hr | PROPOSAL_ROLE_*.md | MEDIUM |
| STRATEGIC | product-manager-agent | PROPOSAL_STRAT_*.md | HIGH |
| NEW_DEPT | od_learning | PROPOSAL_DEPT_*.md | HIGH |

---

## STANDARD PROPOSAL FLOW

```
STEP 1: CREATION (Agent → Proposal file)
  Agent writes proposal to:
  brain/shared-context/corp/proposals/PROP_<date>_<topic>.md
  Format required:
    ## PROPOSAL: <title>
    Owner: <agent>
    Date: <ISO date>
    Type: <KPI_CHANGE | NEW_SKILL | ROLE_CHANGE | STRATEGIC | NEW_DEPT>
    Priority: <HIGH | MEDIUM | LOW>

    ## Problem
    <what gap/issue triggered this>

    ## Proposed Solution
    <concrete change>

    ## Impact
    <expected outcome>

    ## Resources Required
    <cost, time, agents needed>

    ## Decision Required By
    <date or cycle>

STEP 2: NOTIFICATION (notification-bridge → Telegram)
  notification-bridge sends:
  { priority: "HIGH", type: "CEO_PROPOSAL",
    title: "[PROP] <topic>",
    body: "<agent> submitted proposal — decisions needed" }

STEP 3: CEO REVIEW (Phase 1 of next cycle)
  CEO reads corp/proposals/ during BRIEF phase
  CEO adds decision to each file:
    ## CEO DECISION
    - Status: APPROVED | REJECTED | DEFERRED
    - Date: <date>
    - Notes: <rationale>

STEP 4: EXECUTION (if APPROVED)
  CEO types: "execute PROP_<date>_<topic>"
  Antigravity reads proposal → routes to owning agent
  Agent executes → writes receipt to telemetry/receipts/
  Updates: corp/memory/global/decisions_log.md

STEP 5: ARCHIVE
  Completed proposals → corp/proposals/archive/DONE_<date>_<topic>.md
  Register in: corp/memory/global/decisions_log.md
```

---

## PENDING PROPOSALS (as of Cycle 11)

| Proposal | Owner | Type | Action |
|---------|-------|------|--------|
| PROP_2026-03-22_SKILL_TIER_BATCH | registry | NEW_SKILL | CEO: APPROVE or DEFER |
| PROP_2026-03-22_AOS_CLI | engineering | STRATEGIC | CEO: APPROVE or DEFER |
| PROP_2026-03-22_DEEPAGENTS_AUTOSTART | rd | STRATEGIC | CEO: APPROVE or DEFER |
| PROP_2026-03-23_OBSERVABILITY_LAYER | rd + engineering | STRATEGIC | CEO: APPROVE or DEFER |
| PROP_2026-03-23_4C_VERIFICATION_GATES | security | STRATEGIC | CEO: APPROVE or DEFER |

**CEO Action:** Đọc từng file trong `brain/shared-context/corp/proposals/` và reply `## CEO DECISION`.

---

## PROPOSAL FAST TRACK (emergency)

```
CEO types: "prop emergency: <description>"
→ Antigravity immediately creates PROP_<date>_EMERGENCY_<topic>.md
→ Routes to relevant C-Suite agent for quick assessment (< 30 min)
→ CEO decides immediately
→ Execute same session
```

---

## DEFERRED PROPOSAL REVIEW

```
Phase 1 of every cycle:
  cognitive_reflector scans corp/proposals/
  Finds proposals with Status=DEFERRED AND age > 3 cycles
  → Re-surfaces to CEO as reminder
  → Format: "[OVERDUE PROP] <title> — deferred X cycles ago"
```
