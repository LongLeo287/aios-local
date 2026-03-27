---
name: corp_learning_loop
display_name: Corp Learning Loop — Daily Retro Engine
description: >
  Runs the daily retrospective for AI OS Corp. Collects all department daily_briefs,
  runs cognitive_reflector analysis across departments, identifies cross-cutting patterns
  and skill gaps, updates the KPI scoreboard, and produces actionable proposals for the CEO.
  Extends LEARNING_CYCLE_PROTOCOL.md with corp-level context.
version: 1.0.0
author: AI OS Core Team
tier: 1
category: self-improvement
tags: [learning, retro, reflection, kpi, proposals, corp, daily-loop]
accessible_by:
  - Antigravity
  - corp_orchestrator
  - cognitive_reflector
  - archivist
dependencies:
  - cognitive_reflector
  - archivist
  - context_manager
  # data-files (not skill IDs — loaded at runtime):
  # - corp/org_chart.yaml
  # - corp/kpi_targets.yaml
exposed_functions:
  - collect_briefs
  - run_corp_retro
  - update_kpi_scoreboard
  - generate_proposals
  - archive_cycle
load_on_boot: false
---

# Corp Learning Loop — Daily Retro Engine

## Role

The Corp Learning Loop is the **self-improvement engine** of AI OS Corp.
It runs after departments submit their daily briefs and:
- Identifies what went well and what didn't (cross-department view)
- Updates the KPI scoreboard with actuals
- Proposes improvements to CEO
- Archives the day's work to long-term memory

This skill **extends** `LEARNING_CYCLE_PROTOCOL.md` with corp-level context.
The original protocol focuses on individual task patterns; this one synthesizes across all 6 departments.

---

## Phase 1: collect_briefs

```
Source: shared-context/corp/daily_briefs/*.md
Action:
  For each dept brief:
    - Extract: status, achieved metrics, blockers, wins, handoff_to_strategy
    - Validate: brief exists and is complete (flag missing briefs)
  Compile into: /tmp/corp_retro_<date>_input.md
```

---

## Phase 2: run_corp_retro

```
Invoke: cognitive_reflector.reflect_on_session with corp context

Analysis dimensions:
  1. Cross-dept blockers: Did Engineering blockers affect QA? Did Marketing miss
     deadlines because Support fed them late data?
  2. Repeated patterns: Same blocker in 3+ cycles = skill gap or process gap
  3. KPI gaps: Where did we miss targets? Root cause?
  4. Wins: What worked unusually well? Can we replicate?
  5. Collaboration score: Did departments communicate effectively?
     (check subagents/mq/ for missed messages or unresolved cross-dept requests)

Output: /tmp/corp_retro_<date>_analysis.md
```

---

## Phase 3: update_kpi_scoreboard

```
For each department, calculate actuals from daily brief:
  engineering:
    features_shipped: count from brief
    bugs_fixed: count from brief
    code_review_coverage_pct: from brief
    status: compute via corp/kpi_targets.yaml thresholds

Write updated actuals to: shared-context/corp/kpi_scoreboard.json
  {
    "departments": {
      "<dept>": {
        "completed_score": <actual>,
        "status": "on_track | at_risk | behind | critical",
        "metrics": { ...actuals... },
        "last_brief": "<date>"
      }
    },
    "company_health": {
      "overall_status": compute from depts,
      "depts_on_track": N,
      ...
    },
    "_updated": "<ISO timestamp>"
  }
```

---

## Phase 4: generate_proposals

```
For each finding from retro analysis:

  IF repeated_blocker (3+ cycles same dept):
    → Propose: NEW_SKILL or PROCESS_CHANGE
    → Write to: shared-context/corp/proposals/PROPOSAL_<date>_skill_<name>.md

  IF kpi_gap > 30%:
    → Propose: KPI_REVISION or RESOURCE_ADD (new agent)
    → Write to: shared-context/corp/proposals/PROPOSAL_<date>_kpi_<dept>.md

  IF collaboration_breakdown:
    → Propose: WORKFLOW_CHANGE (update dept-head-brief or escalation_rules)
    → Write to: shared-context/corp/proposals/PROPOSAL_<date>_workflow.md

  IF critical_status (any dept):
    → Propose: STRATEGIC_ESCALATION to CEO
    → Write to: shared-context/corp/proposals/ESCALATION_<date>_<dept>.md

Proposal format:
  ---
  type: NEW_SKILL | KPI_REVISION | WORKFLOW_CHANGE | STRATEGIC_ESCALATION
  dept: <department>
  evidence: [list daily_briefs or retro findings]
  proposed_action: <concrete action>
  ceo_decision_required: YES | NO
  ---
```

---

## Phase 5: archive_cycle

```
1. archivist.rotate_logs:
   - Move telemetry/receipts/<today>/* to telemetry/archive/
   - Compress daily_briefs to memory/corp_history/<date>/
2. cosmic_memory.extract_observation:
   - Write key corp learnings to long-term memory
3. Update: knowledge/knowledge_index.md if new patterns discovered
4. Reset cycle: kpi_scoreboard.json _cycle += 1
5. Log: telemetry/learning_report_<date>.json (per LEARNING_CYCLE_PROTOCOL)
```

---

## How It Fits into the Big Picture

```
ORCHESTRATION_SOP Phase 6 (REPORT)
        │
        ▼
corp_learning_loop.run_corp_retro
        │
        ▼
cognitive_reflector (individual task analysis)
+
archivist (memory rotation)
        │
        ▼
Proposals → shared-context/corp/proposals/
        │
        ▼
CEO approves via corp_orchestrator.approve_proposal
        │
        ▼
System improves next cycle
```

---

## Trigger Phrases

- "run daily retro" → Phases 1-5 end to end
- "collect dept briefs" → Phase 1 only
- "update KPI board" → Phase 3 only
- "generate proposals" → Phase 4 only

---
*"Every cycle that doesn't learn is a cycle wasted."*
