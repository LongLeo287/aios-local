# Department: operations
# dept-head-brief.md — Department Head Daily Briefing SOP
# Version: 1.0 | Updated: 2026-03-17
# Authority: Tier 2 (Operations)
# Used by: All 6 Department Heads

---

## Purpose

This SOP defines how department heads receive, process, and broadcast
the daily mission to their worker agents.

---

## Step 1: Receive Brief

Read incoming brief from: `subagents/mq/<dept>_brief.md`

Parse:
- Company mission from CEO
- Today's KPI targets
- Active escalations assigned to your dept
- Priority tasks from blackboard.json

---

## Step 2: Assess Capacity

```
For each worker in your dept:
  - Is the agent available? (not blocked from previous cycle)
  - Does the task match agent's specialty?
  - Is there a dependency on another dept?

If dependency: request input via subagents/mq/<dept>_request_<other_dept>.md
```

---

## Step 3: Assign Tasks

Write task assignments to `subagents/mq/<dept>_dispatch.md`:

```
FROM: <dept_head_agent>
TO: <worker_agent>
TASK_ID: CORP-<date>-<dept>-<seq>
PRIORITY: HIGH | MEDIUM | LOW
DESCRIPTION: <clear, atomic task>
EXPECTED_OUTPUT: <what does "done" look like?>
DUE: end of daily cycle
QA_REQUIRED: YES | NO
ESCALATE_TO_ME_IF: [conditions for escalation]
```

---

## Step 4: Monitor

During the cycle, dept head:
- Reads escalation notes from `subagents/mq/<dept>_escalation.md`
- Responds within same session:
  - Can resolve: write guidance, re-assign
  - Cannot resolve: escalate to C-Suite per `corp/escalation_rules.yaml`

---

## Step 5: Write Daily Brief Back

At end of cycle, write to `shared-context/corp/daily_briefs/<dept>.md`:

```markdown
# Daily Brief — <DEPT> — <YYYY-MM-DD>

**Head Agent:** <agent_name>
**Cycle:** <number>

## KPI Results

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| ...    | ...    | ...      | ✅/⚠️/🔴 |

## Summary

<2-3 sentences: what was done, any blockers, key outputs>

## Wins

- <item>

## Blockers

- <issue> [ESCALATED | RESOLVED | PENDING]

## Handoff to Strategy

<key observation for cognitive_reflector — patterns, skill gaps, improvement ideas>
```

---

*"A dept head who doesn't write their brief is invisible to the company."*
