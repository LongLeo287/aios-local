---
name: corp_orchestrator
display_name: Corp Orchestrator — Company-Mode Dispatcher
description: >
  Activates "Corp Mode" in AI OS. Reads the org chart, dispatches the daily brief
  to department heads, monitors escalations and KPI board, and gates CEO approval
  on strategic proposals. Acts as the executive assistant between the Human CEO
  and the 6 AI departments.
version: 1.0.0
author: AI OS Core Team
tier: 1
category: orchestration
tags: [corp, orchestration, dispatch, kpi, escalation, ceo, departments]
accessible_by:
  - Antigravity
  - orchestrator_pro
dependencies:
  - context_manager
  - reasoning_engine
  # data-files (not skill IDs — loaded at runtime):
  # - corp/org_chart.yaml
  # - corp/kpi_targets.yaml
  # - corp/escalation_rules.yaml
exposed_functions:
  - activate_corp_mode
  - dispatch_daily_brief
  - check_escalations
  - show_kpi_board
  - approve_proposal
  - trigger_daily_cycle
load_on_boot: false
---

# Corp Orchestrator — Company-Mode Dispatcher

## Role

Corp Orchestrator is the **executive layer** of AI OS Corp.
It bridges the CEO (human) with the 6 AI departments by:
1. Broadcasting mission and targets to dept heads
2. Monitoring KPI scoreboard and flagging issues
3. Surfacing escalations and proposals to CEO
4. Triggering the daily cycle end-to-end

## Core Logic

### activate_corp_mode
```
1. Read corp/org_chart.yaml               → load company structure
2. Read shared-context/corp/mission.md    → CEO's current mission
3. Read corp/kpi_targets.yaml             → today's targets
4. Read shared-context/corp/escalations.md→ any pending escalations
5. Read shared-context/corp/kpi_scoreboard.json → current KPI state
6. Announce: "Corp Mode active. [N] depts online. [M] escalations pending."
```

### dispatch_daily_brief
```
For each department in org_chart.yaml:
  1. Compose brief (mission + KPI targets + escalations + priority tasks)
  2. Write to: subagents/mq/<dept>_brief.md
  3. Log dispatch to: telemetry/receipts/CORP_BRIEF_<date>.json
```

### check_escalations
```
1. Read shared-context/corp/escalations.md
2. Filter: status == "OPEN"
3. For each open escalation:
   - Check SLA: is it overdue?
   - If Level 3: flag to CEO immediately
   - If Level 1-2: remind dept head / C-Suite
4. Report summary to CEO via Antigravity
```

### show_kpi_board
```
Read shared-context/corp/kpi_scoreboard.json
Format as table:

| Dept | Status | Target | Achieved |
|------|--------|--------|----------|
| Engineering | ✅ | 5 | 5 |
| Marketing   | ⚠️ | 3 | 2 |
...

Overall: [N] on_track | [M] at_risk | [P] behind
```

### approve_proposal
```
Input: proposal file path
1. Read proposal from shared-context/corp/proposals/<file>
2. Present to CEO: key points + recommended action
3. CEO responds: APPROVE | REJECT | MODIFY
4. If APPROVE: write decision to shared-context/corp/decisions/log.md
              update relevant config (kpi_targets.yaml, org_chart.yaml if needed)
5. If REJECT:  archive proposal to shared-context/corp/proposals/rejected/
6. If MODIFY:  loop back to strategy dept with feedback
```

### trigger_daily_cycle
```
Run corp-daily-cycle.md end to end.
Phases 1-7 in sequence as defined in that workflow.
```

## Trigger Phrases

- "activate corp mode" → activate_corp_mode
- "start daily cycle" → trigger_daily_cycle
- "show KPI board" → show_kpi_board
- "any escalations?" → check_escalations
- "review proposal <filename>" → approve_proposal
- "brief <dept> department" → dispatch_daily_brief for that dept

## Integration Points

| System | How |
|--------|-----|
| blackboard.json | Reads active tasks, writes corp_cycle_status |
| subagents/mq/ | Writes dept briefs, reads escalations |
| shared-context/corp/ | All corp data files |
| ORCHESTRATION_SOP.md | Corp daily cycle extends Phase 1-6 loop |
| LEARNING_CYCLE_PROTOCOL.md | Phase 6 of daily cycle invokes this |

---
*"The orchestrator does not do the work. It makes sure the right agents do."*
