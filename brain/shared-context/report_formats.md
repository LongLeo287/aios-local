# report_formats.md — AI OS Master Report Formats
# Version: 2.0 | Authority: Tier 0
# Location: brain/shared-context/report_formats.md  ← CANONICAL SOURCE
# Loaded at: Boot Step 6
# Rune pointer: corp/prompts/runes/report_formats.md → references this file
#
# This file defines ALL output formats used in AI OS:
#   PART A — CEO-Facing Formats (Antigravity → Human/CEO)
#   PART B — Corp System Formats (Agent ↔ Agent / Corp Layer)

---

## CRITICAL RULE (Never Skip)

ALL brainstorms, reports, and analyses TO THE CEO:
1. Write to an artifact `.md` file — NEVER paste inline in chat
2. Call `notify_user` with `PathsToReview` → always use the left panel
3. Wait for CEO feedback before proceeding to implementation

---

# PART A — CEO-Facing Formats (Antigravity → CEO)

## Format Selector

```
What are you presenting to CEO?
│
├─ Exploring a problem / comparing options?
│   └─► FORMAT A1: Visual Brainstorm
│
├─ High-stakes design needing multiple perspectives?
│   └─► FORMAT A2: Multi-Agent Review
│        → Only after FORMAT A1 is confirmed
│
├─ Product feature / new capability discovery?
│   └─► FORMAT A3: BMAD Method
│
├─ Logging a decision already made?
│   └─► FORMAT A4: Decision Log
│
└─ Reporting completed work (post-execution)?
    └─► FORMAT A5: Execution Receipt
```

---

## A1: Visual Brainstorm

**When:** Khám phá vấn đề, so sánh 2–3 hướng, đưa ra khuyến nghị
**Rune:** `corp/prompts/runes/brainstorm_prompt.md`

**Sections:**
1. Mermaid flowchart — tổng quan vấn đề
2. Comparison table — các options (Pros / Cons / Recommendation)
3. Risks & open questions
4. Antigravity's recommendation

---

## A2: Multi-Agent Review

**When:** Kiến trúc phức tạp, rủi ro cao, cần stress-test từ nhiều góc nhìn
**Rune:** `corp/prompts/runes/multi_agent_brainstorm_prompt.md`

**Roles:**
1. **Primary Designer** — thiết kế ban đầu (chạy A1 trước)
2. **Skeptic** — "giả sử cái này fail, tại sao?"
3. **Constraint Guardian** — performance, security, maintainability
4. **User Advocate** — UX, clarity, cognitive load
5. **Arbiter** — final resolution + Decision Log

---

## A3: BMAD Method

**When:** Feature mới, capability mới, xác định scope
**Rune:** `corp/prompts/runes/bmad_prompt.md`

**Sections:**
1. Problem Statement
2. Hypothesis
3. Proposed Experiments / Approaches
4. Success Metrics
5. Go / No-Go recommendation

---

## A4: Decision Log

**When:** Ghi lại quyết định quan trọng đã được chọn
**Rune:** `corp/prompts/runes/decision_log_prompt.md`

**Sections:**
1. Decision Made
2. Alternatives Considered
3. Rationale
4. Risks Acknowledged
5. Owner + Date

---

## A5: Execution Receipt

**When:** Claude Code hoặc Antigravity hoàn thành task
**Rune:** `corp/prompts/runes/execution_receipt_prompt.md`

**Sections:**
1. Task Summary (what was done)
2. Files Changed (with links)
3. Commands Run
4. Verification Result
5. Known Issues / Next Steps

---

# PART B — Corp System Formats (Agent ↔ Corp Layer)

## B1: DAILY_BRIEF — Dept Head → C-Suite

Submitted each cycle by dept heads to C-Suite lead + corp_orchestrator.
**Destination:** `shared-context/corp/daily_briefs/<dept>.md`

```
---
format: DAILY_BRIEF
dept: <department_name>
head_agent: <agent_id>
date: <YYYY-MM-DD>
cycle: <N>
---
## Status: [ON_TRACK | AT_RISK | BEHIND | CRITICAL]
## Metrics
- <metric>: <actual> / <target> → [✅|⚠️|🔴]
## Completed
- [x] <task>
## Blockers
- <blocker> | Severity: [LOW|MEDIUM|HIGH|CRITICAL]
## Handoff to Strategy
- <insights for CSO/strategy dept>
## Tomorrow's Focus
- [ ] <planned_task>
---
```

---

## B2: TASK_RECEIPT — Claude Code → Telemetry

Auto-generated for every autonomous step. Non-negotiable.
**Destination:** `telemetry/receipts/RECEIPT-<date>-<id>.json`
**Writer:** Claude Code only | **Reader:** Antigravity, corp_orchestrator

```json
{
  "receipt_id": "RECEIPT-<YYYYMMDD>-<HHMMSS>-<hash6>",
  "timestamp": "<ISO8601>",
  "agent": "<agent_id>",
  "task_id": "<parent_task_id>",
  "action": "<what was done>",
  "files_modified": ["<path>"],
  "files_created": ["<path>"],
  "files_deleted": [],
  "result": "SUCCESS | PARTIAL | FAILED",
  "error": null,
  "next_step": "<what happens next>",
  "blocked": false,
  "blocked_reason": null
}
```

---

## B3: ESCALATION_REPORT — Any Agent → CEO

**Destination:** `shared-context/corp/escalations.md` (append)
**Level 3 = Telegram ping immediately**

```
---
format: ESCALATION_REPORT
escalation_id: ESC-<YYYYMMDD>-<seq>
level: [1=FYI | 2=Decision needed | 3=URGENT/STOP]
origin_agent: <agent_id>
timestamp: <ISO8601>
---
## Summary
## Context
## Impact
## Options
1. <option_A> → Pros/Cons
2. <option_B> → Pros/Cons
## Recommended Action
## CEO Decision
[ ] APPROVE option A  [ ] APPROVE option B
[ ] REJECT  [ ] DEFER to: <date>
---
```

---

## B4: KPI_SNAPSHOT — corp_orchestrator → CEO

**Trigger:** `show_kpi_board` | `start_daily_cycle` Phase 5
**Writer:** corp_orchestrator skill

```
---
format: KPI_SNAPSHOT
timestamp: <ISO8601>
cycle: <N>
---
## Company Health: [🟢 ON_TRACK | 🟡 AT_RISK | 🔴 CRITICAL]
| Dept | Status | Target | Actual | Gap |
|------|--------|--------|--------|-----|
| Engineering | ✅ | ... | ... | 0 |
| Marketing | ⚠️ | ... | ... | -1 |
## Open Escalations
## Proposals Awaiting CEO
---
```

---

## B5: PROPOSAL — Agent/Dept → CEO

**Destination:** `shared-context/corp/proposals/PROP-<id>.md`
**Approved → logged:** `shared-context/corp/decisions/log.md`

```
---
format: PROPOSAL
proposal_id: PROP-<YYYYMMDD>-<seq>
type: [NEW_SKILL | KPI_REVISION | WORKFLOW_CHANGE | RESOURCE_ADD | STRATEGIC_ESCALATION]
status: PENDING
ceo_decision_required: YES
---
## Title
## Problem
## Evidence
## Proposed Solution
## Expected Outcome
## Risk if NOT Approved
## Resources Required
## CEO Decision
[ ] APPROVE  [ ] REJECT — reason: ___  [ ] MODIFY — feedback: ___
---
```

---

## B6: INCIDENT_REPORT — Security/SRE → CEO

**P1/P2:** `shared-context/corp/escalations.md` + Telegram ping
**P3/P4:** `telemetry/incidents/`

```
---
format: INCIDENT_REPORT
incident_id: INC-<YYYYMMDD>-<seq>
severity: [P1_CRITICAL | P2_HIGH | P3_MEDIUM | P4_LOW]
type: [SECURITY | SYSTEM_FAILURE | DATA | COMPLIANCE | AGENT_MISBEHAVIOR]
status: [OPEN | CONTAINED | RESOLVED]
---
## Summary
## Timeline
## Root Cause
## Impact
## Containment Actions Taken
## Next Steps
## Postmortem Required: [YES | NO]
---
```

---

## B7: PROGRESS_UPDATE — Mid-task → Blackboard

**Trigger:** Every 25% completion or end of sub-phase
**Destination:** `shared-context/blackboard.json` (task_status field)

```
---
format: PROGRESS_UPDATE
task_id: <parent_task_id>
checkpoint: <N of M>
---
## Progress: <N>/<M> (<pct>%)
## Done  ## In Progress  ## Remaining
## Issues
## On Track: [YES | NO | AT_RISK]
---
```

---

# Format Mapping

| Format | Who writes | Who reads | Where stored |
|--------|-----------|-----------|--------------|
| A1 Visual Brainstorm | Antigravity | CEO | artifacts/ |
| A2 Multi-Agent Review | Antigravity | CEO | artifacts/ |
| A3 BMAD Method | Antigravity | CEO | artifacts/ |
| A4 Decision Log | Antigravity | CEO | artifacts/ |
| A5 Execution Receipt | Antigravity / Claude Code | CEO | artifacts/ |
| B1 DAILY_BRIEF | Dept heads | C-Suite | corp/daily_briefs/ |
| B2 TASK_RECEIPT | Claude Code | Antigravity | telemetry/receipts/ |
| B3 ESCALATION_REPORT | Any agent | CEO | corp/escalations.md |
| B4 KPI_SNAPSHOT | corp_orchestrator | CEO | (rendered) |
| B5 PROPOSAL | Any agent/dept | CEO | corp/proposals/ |
| B6 INCIDENT_REPORT | security/sre | CEO | corp/escalations.md |
| B7 PROGRESS_UPDATE | Any agent | Antigravity | blackboard.json |

---

## Global Rules

1. CEO output (A1–A5) → **Vietnamese**, write to artifact file first
2. Corp formats (B1–B7) → **English**, write to designated path
3. No free-form reports to CEO — always use a format above
4. `receipt_id` and `incident_id` must be globally unique (timestamp + 6-char hash)
5. Security P1/P2 → bypass all routing, go directly to CEO + Telegram
6. New formats require CEO approval via B5 PROPOSAL

---

*"Consistent formats turn agent output into institutional intelligence."*
