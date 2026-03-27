# WORKFLOW.md — AI OS Operational Workflow (Event-Driven)
# Version: 3.0 | Updated: 2026-03-17
# Authority: Tier 2 (Operations)
# Replaces: v2.0 (missing corp triggers, 13-dept awareness)
# Reference: ORCHESTRATION_SOP.md v4 for full 6-phase details

---

## Overview

AI OS operates on **triggers and events** — not fixed time schedules.
Two operational modes run in parallel:

```
MODE A: PERSONAL AI OS  ─── Antigravity + Claude Code + Gemini
  Individual project work, research, development

MODE B: CORP MODE       ─── CEO + C-Suite + 13 Departments
  Organizational work, managed by on-demand corp cycle
```

Any agent reads this file to understand what to do at each lifecycle stage.

---

## TRIGGER MAP: PERSONAL AI OS

### Trigger 1: Session Start
**When:** User says "start / khởi động / read AI OS / boot"

```
BOOT sequence (strict order):
1. Read d:\Project\AI OS\CLAUDE.md                  [ecosystem map]
2. Read d:\Project\AI OS\rules\CLAUDE_CODE_MANAGER.md [if Claude Code]
3. Read shared-context/SKILL_REGISTRY.json           [skill graph]
4. Read corp/org_chart.yaml                          [current team]
5. Execute: workflows/pre-session.md                 [session init]
6. Announce: "Boot complete. [N] skills loaded. Status: [IDLE|ACTIVE]"
```

### Trigger 2: New Task Request
**When:** User describes something to build, fix, or analyze

```
ANALYZE → PLAN → DELEGATE (see ORCHESTRATION_SOP.md Phase 2-4)
Key steps:
- Antigravity: cross-session recall via smart_memory + cosmic_memory
- Antigravity: brainstorm Visual-First in Vietnamese
- User: review + approve (HITL gate)
- Antigravity: write implementation_plan.md + task.md
- Antigravity: trigger handoff_to_claude_code.ps1
```

### Trigger 3: Claude Code Returns
**When:** blackboard.json handoff_trigger = "COMPLETE" or "BLOCKED"

```
REPORT sequence:
1. Read blackboard.json result.summary       [English from Claude Code]
2. Read telemetry/receipts/ for this run     [step-by-step evidence]
3. Run cognitive_reflector.reflect_on_task   [extract lessons]
4. Run cosmic_memory.extract_observation     [long-term memory update]
5. Generate Vietnamese Mermaid report for user
6. Reset blackboard: handoff_trigger = null, status = IDLE
7. Execute: workflows/post-session.md        [close hook]
```

### Trigger 4: External Knowledge Ingestion
**When:** User provides any URL/repo/document to ingest

```
EXECUTE: workflows/ingest-external.md (SECURITY MODE: ALWAYS ON)
- TYPE A (URL/Article): fetch → screen → classify → ingest as .md
- TYPE B (GitHub Repo): quarantine clone → vet_repo.ps1 → GATE_SECURITY → extract
- TYPE C (Document): file safety → scan → classify
- TYPE D (Video): concept extraction only, no download
```

### Trigger 5: Session End
**When:** User says "end / kết thúc / close"

```
Execute: workflows/post-session.md
- Save context snapshot → blackboard.json context field
- Rotate old receipts (archivist)
- Update knowledge_index.md if new knowledge created
- Write handoff notes
```

---

## TRIGGER MAP: CORP MODE

### Trigger C1: CEO Activates Corp
**When:** User says "aos corp start" or "khởi động corp mode"

```
1. Paste (or reference) corp/prompts/CEO_PROMPT.md into session
2. CEO reads:
   - shared-context/corp/mission.md
   - shared-context/corp/kpi_scoreboard.json
   - shared-context/corp/escalations.md
   - shared-context/corp/proposals/ (pending decisions)
3. Execute: workflows/corp-daily-cycle.md Phase 1 (BRIEF)
```

### Trigger C2: Activate a Department
**When:** CEO or C-Suite directs a dept head to activate

```
1. Load: corp/departments/<dept>/MANAGER_PROMPT.md
2. Manager loads: corp/memory/departments/<dept>.md
3. Manager pulls tasks from shared-context/blackboard.json
4. Execute: workflows/corp-task-flow.md (DISPATCH phase)
```

### Trigger C3: Worker Receives Task
**When:** Task appears in subagents/mq/<dept>_tasks.md

```
1. Load: corp/prompts/WORKER_PROMPT.md
2. Load dept overlay: corp/departments/<dept>/WORKER_PROMPT.md (if exists)
3. Search SKILL_REGISTRY for relevant skill
4. Execute: workflows/corp-task-flow.md (EXECUTE phase)
5. Write receipt to telemetry/receipts/<dept>/
```

### Trigger C4: QA Gate Triggered
**When:** Any output has qa_required: true in receipt, OR gate item arrives

```
Execute: workflows/corp-gate-flow.md
Gates: GATE_QA | GATE_CONTENT | GATE_SECURITY | GATE_LEGAL
No item bypasses a blocking gate.
```

### Trigger C5: Escalation Occurs
**When:** Worker hits 2-strike rule, OR KPI is behind threshold

```
Execute: workflows/corp-escalation-flow.md
L1: Worker → Manager (same session)
L2: Manager → C-Suite (logs to escalations.md)
L3: C-Suite → CEO (blocks affected work)
```

### Trigger C6: Daily Retro (On-Demand)
**When:** CEO says "run retro" or "aos corp retro"

```
Execute: workflows/corp-daily-cycle.md Phase 6–7
cognitive_reflector + archivist run reflection
Strategy dept produces proposals → CEO queue
```

---

## Infrastructure Maintenance (On-Demand)

| Task | Command | When |
|------|---------|------|
| Rebuild skill registry | `skill_loader.ps1` | After adding/modifying skills |
| Fetch external skills | `skill_fetcher.ps1` | When new capability needed |
| Archive old receipts | `aos corp archive` | When telemetry/ is large |
| Learning cycle | `aos corp retro` | Weekly or when prompted |
| Security scan | `strix-agent` | Any new external plugin/repo |
| Memory rotation | `archivist` | Monthly or when prompted |
| KPI update | `aos corp kpi` | After any dept cycle |

---

*"The system responds to events, not clocks. Two modes, one operating system."*
