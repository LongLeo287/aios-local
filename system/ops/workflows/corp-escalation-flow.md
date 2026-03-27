# Department: operations
# corp-escalation-flow.md — L1 → L2 → L3 Escalation Workflow
# Version: 1.0 | Updated: 2026-03-17
# Authority: Tier 2 (Operations) / Corp Mode

---

## Overview

Escalation is how the org handles blockers, failures, and crises.
3 levels — each has a defined responder, SLA, and format.

```
WORKER (L1) ──► MANAGER (same session)
    │ (if unresolved or systemic)
MANAGER (L2) ──► C-SUITE (same session)
    │ (if cross-dept or strategic)
C-SUITE (L3) ──► CEO (blocking — work pauses)
```

**Key principle:** Never escalate past one level unnecessarily.
Escalate to the level that can actually resolve it.

---

## L1 Escalation: Worker → Manager

**Trigger:** Worker hits 2-strike rule on any task
**Responder:** Dept Head (Manager)
**SLA:** Same work session

**Worker writes to `subagents/mq/<dept>_escalation.md`:**
```markdown
## L1 ESCALATION — [TASK-ID] — [DATETIME]

Agent: <worker-agent>
Dept: <dept>
Task: <task-id and 1-line description>

Blocker: <specific reason — tool failure / ambiguous spec / missing resource>

Attempt 1: <what was tried>
  Result: <what failed and why>

Attempt 2: <different approach tried>
  Result: <what failed and why>

Options considered:
  A. <option> — Feasibility: <High/Med/Low>
  B. <option> — Feasibility: <High/Med/Low>

Recommendation: A or B and why

Awaiting manager response.
```

**Manager response options:**
- Unblock: provide missing context/resource → worker retries
- Reassign: different worker or approach
- Defer: not needed this cycle → remove from task queue
- Escalate to L2: if systemic or cross-dept dependency

---

## L2 Escalation: Manager → C-Suite

**Trigger:**
- KPI behind threshold (per kpi_targets.yaml)
- Cross-dept blocker persisting > 2 cycles
- 2+ workers fail same task category
- L1 escalation unresolvable at dept level

**Responder:** Relevant C-Suite member
**SLA:** Same session

**Manager writes to `shared-context/corp/escalations.md`:**
```markdown
## L2 ESCALATION — [ESC-ID] — [DATE]

From: <dept head>
To: <C-Suite role (CTO/CMO/COO/CFO/CSO)>
Priority: HIGH | MEDIUM

Issue: <1-2 sentences>
Evidence:
  - KPI status: <metric> is <value> vs target <target>
  - Root cause hypothesis: <what caused this>
  - What was tried: <list>
  - Cross-dept dependency: <if applicable>

Options:
  A. <resolution option> — Impact: / Risk:
  B. <resolution option> — Impact: / Risk:

Recommendation: <A or B>
Need from C-Suite: <approve A | provide resource X | coordinate with dept Y>
Deadline: <when needed>
```

**C-Suite response (same session):**
- Write decision to escalations.md as response
- If resolved: flag ESC-ID as RESOLVED
- If needs CEO: escalate to L3

---

## L3 Escalation: C-Suite → CEO

**Trigger:**
- Strategic question requiring CEO direction
- Security CRITICAL finding (security_grc can escalate directly)
- Budget overrun > 20%
- Legal issue requiring CEO sign-off
- Cross-org crisis

**Responder:** CEO
**Effect: BLOCKING** — affected work PAUSES until CEO responds

**C-Suite writes to `shared-context/corp/escalations.md`:**
```markdown
## L3 ESCALATION — [ESC-ID] — [DATE]  ⚠️ CEO REQUIRED

From: <C-Suite role>
Priority: CRITICAL | HIGH
Work paused: <list of paused tasks/depts>

Issue: <2-3 sentences — include urgency and scope>
Evidence: <references to data, KPIs, receipts, security scan>

Options analyzed:
  A. <option> — CEO decides: [APPROVE / REJECT / DEFER]
  B. <option> — CEO decides: [APPROVE / REJECT / DEFER]

C-Suite recommendation: <A or B and why>

CEO decision required by: <session deadline or ASAP if CRITICAL>
```

**CEO response:**
- Log decision to `corp/memory/global/decisions_log.md`
- Write response to escalations.md
- Communicate decision to affected C-Suite
- All work resumes on CEO's decision

---

## Security Emergency Path (CRITICAL Only)

security_grc can skip L1/L2 and go DIRECT to L3 for CRITICAL threats:

```
strix-agent detects CRITICAL threat
    │
    v
Write L3 directly to escalations.md (no L1/L2 wait)
    │
    v
Pause ALL affected systems (not just one dept)
    │
    v
CEO notified immediately
```

---

## Escalation ID Convention

```
ESC-<LEVEL>-<DATE>-<SEQ>

Examples:
  ESC-L1-2026-03-17-001
  ESC-L2-2026-03-17-001
  ESC-L3-2026-03-17-001  (CEO required)
```

---

## Escalation Resolution Record

When an escalation is resolved, update the entry in escalations.md:
```markdown
### RESOLVED — [DATE]
Resolved by: <role/agent>
Decision: <what was decided>
Action taken: <what was done>
Outcome: <result after action>
Logged to: corp/memory/global/decisions_log.md (if L3)
```

---

*"Escalation is not failure. Not escalating when you should is."*
