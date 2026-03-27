# Department: operations
# corp-daily-cycle.md — AI OS Corp Operating Cycle
# Version: 2.0 | Updated: 2026-03-17
# Authority: Tier 2 (Operations)
# Mode: ON-DEMAND (trigger-based, not scheduled)
# Trigger: "aos corp start" | CEO session activation

---

## Overview

The Corp Cycle is how AI OS Corp runs work — on-demand.
No fixed schedule. CEO triggers when needed.
8 phases (Phase 0 = pre-flight). End-to-end: pre-flight → CEO brief → execution → reflection → next decision.

```
CEO ACTIVATES
    │
[0] PRE-FLIGHT      ── Validate system state before cycle begins
    │
[1] CEO BRIEF       ── CEO reads mission, KPIs, escalations, proposals
    │
[2] C-SUITE DISPATCH ── C-Suite translates strategy → dept goals (blackboard)
    │
[3] DEPT DISPATCH   ── 21 dept heads assign tasks to workers
    │
[4] EXECUTE         ── Workers execute, write receipts
    │
[5] GATE            ── GATE_QA / GATE_CONTENT / GATE_SECURITY / GATE_LEGAL
    │
[6] BRIEF BACK      ── Dept heads write daily_briefs
    │
[7] REFLECT         ── cognitive_reflector + archivist → proposals → CEO
    │
CEO reads proposals → decides → RESET → next cycle
```

---

## Phase 0: PRE-FLIGHT CHECK

**Trigger:** Automatically runs before Phase 1 on every `aos corp start`
**Who:** orchestrator_pro (or Claude Code if orchestrator_pro unavailable)

```
Step 0.1 — Critical file check (STOP if any fail):
  [ ] brain/shared-context/blackboard.json        — readable + valid JSON
  [ ] brain/shared-context/SKILL_REGISTRY.json    — readable + no nulls in load_order
  [ ] brain/shared-context/corp/kpi_scoreboard.json
  [ ] brain/shared-context/corp/escalations.md
  [ ] corp/org_chart.yaml
  [ ] corp/rules/APPROVAL_GATES.md

Step 0.2 — State check (STOP if any fail):
  [ ] blackboard.json corp_cycle_status != "RUNNING"
      (if RUNNING: previous cycle may be stuck — report to CEO before starting)
  [ ] No open L3 escalations in escalations.md
      (if L3 open: do NOT start — CEO must resolve first)
  → On PASS: Set blackboard.json corp_cycle_status = "RUNNING"

Step 0.3 — Skill registry sync (skill-discovery-auto.md):
  → Set blackboard.json skill_registry_status = "UPDATING"
  → registry-manager-agent scans plugins/, tools/, workforce/agents/, subagents/
  → Creates SKILL.md for any folder missing it
  → Rebuilds FAST_INDEX.json
  → Set blackboard.json skill_registry_status = "READY"
  → Report count to blackboard

Step 0.4 — Warning-only checks (log but do NOT stop cycle):
  [ ] corp/memory/departments/<dept>.md exists for each active dept
  [ ] subagents/mq/ directory exists and is readable
  [ ] telemetry/receipts/ directory is writable

On PASS all steps: proceed to Phase 1
On Step 0.1/0.2 FAIL: write to escalations.md + stop cycle + notify CEO
On Step 0.3 FAIL: log warning, proceed with stale SKILL_REGISTRY, mark for manual rebuild
```

---

## Phase 1: CEO BRIEF

**Trigger:** `aos corp start` or CEO activates corp mode
**Ref:** `corp/prompts/CEO_PROMPT.md`

```
CEO reads in order:
1. brain/shared-context/corp/mission.md          ← current strategic direction
2. brain/shared-context/corp/kpi_scoreboard.json ← all 21 dept KPI status
3. brain/shared-context/corp/escalations.md      ← open L2/L3 items
4. brain/shared-context/corp/proposals/          ← pending decisions from last cycle
5. corp/memory/global/decisions_log.md           ← last 5 CEO decisions for context

CEO outputs:
  - Decision on any open proposals → decisions_log.md
  - Mission update if needed → brain/shared-context/corp/mission.md
  - Priority instruction to C-Suite → brain/shared-context/blackboard.json or direct brief
```

---

## Phase 2: C-SUITE DISPATCH

**Who:** CTO | CMO | COO | CFO | CSO
**Ref:** `corp/prompts/CSUITE_PROMPT.md`

```
Each C-Suite member:
1. Read CEO mission + their domain KPIs from brain/shared-context/corp/mission.md
2. Translate CEO intent → dept-level goals for each of their depts
3. Write dept task entries to brain/shared-context/blackboard.json:
   { "dept": "engineering", "goal": "...", "kpi_targets": [...] }
4. Optional: write brief to each dept head via subagents/mq/<dept>_brief.md

CFO additional: check finance/budget status → flag if any dept at >80% budget
COO additional: check Security for any open incidents, HR for agent issues
```

**C-Suite dispatch covers all 21 departments:**
```
CTO:  engineering / qa_testing / it_infra / registry_capability / system_health
CMO:  marketing   / support    / content_review
COO:  operations  / hr_people  / security_grc / asset_library / planning_pmo
      monitoring_inspection / content_intake / client_reception
CFO:  finance
CSO:  strategy    / legal      / rd           / od_learning
```

---

## Phase 3: DEPT DISPATCH

**Who:** All 21 Dept Heads (Managers)
**Ref:** `corp/prompts/MANAGER_PROMPT.md` + dept overlay

```
Each dept head:
1. Read daily brief from blackboard / C-Suite brief
2. Load dept memory: corp/memory/departments/<dept>.md
3. Create atomic task cards to subagents/mq/<dept>_tasks.md
4. Assign each task to appropriate worker agent
5. Set: context, acceptance criteria, LLM tier, qa_required flag
```

**Reference:** task card format in `workflows/corp-task-flow.md`

---

## Phase 4: EXECUTE

**Who:** All Worker Agents
**Ref:** `corp/prompts/WORKER_PROMPT.md` + dept overlay

```
Each worker:
1. Read assigned task card
2. Search SKILL_REGISTRY for matching skill → load SKILL.md
3. Execute in atomic steps
4. Write receipt to telemetry/receipts/<dept>/<T-ID>.json
5. Update task card status: DONE | FAILED
6. If qa_required: route to correct gate queue
7. If 2-strike failure: write L1 escalation

Security special: security_grc scans continuously during Phase 4
Operations: scrum-master-agent monitors blackboard for stuck tasks
```

---

## Phase 5: GATE REVIEW

**Who:** Gate agents in qa_testing / content_review / security_grc / legal
**Ref:** `workflows/corp-gate-flow.md`, `rules/APPROVAL_GATES.md`

```
GATE_QA runs: for all engineering outputs
GATE_CONTENT runs: for all marketing/support content
GATE_SECURITY runs: continuously + on any new tool/plugin
GATE_LEGAL runs: for any agreement or external commitment

Each gate: PASS / FAIL / CONDITIONAL
Failed items: return to worker for fix → re-submit
3rd FAIL on same item: L2 escalation to dept head
```

---

## Phase 6: BRIEF BACK

**Who:** All 21 Dept Heads
**Ref:** `MANAGER_PROMPT.md` brief format

```
Each dept head writes to: shared-context/corp/daily_briefs/<dept>.md

Format includes:
  DATE / DEPT / HEAD
  KPI STATUS: [on_track | at_risk | behind | critical]
  COMPLETED: [list of tasks]
  IN PROGRESS: [list + ETA]
  BLOCKED: [with L1/L2 notes]
  WINS: [notable achievements]
  ESCALATIONS: [reference IDs if any]

Agents must write this even if cycle had zero tasks (write "No tasks this cycle")
```

---

## Phase 7: REFLECT + PROPOSE

**Who:** cognitive_reflector + archivist + strategy/product-manager-agent
**Ref:** `ops/workflows/corp-learning-loop.md`
**Mode: MANDATORY** — runs after every Phase 6 completion. NOT optional.
**Trigger:** Phase 6 complete (all 21 daily_briefs written) → cognitive_reflector auto-starts

```
archivist:
  - Archive telemetry receipts for this cycle
  - Rotate dept memory (if >30d entries)
  - Purge agent memories (if >7d)

cognitive_reflector:
  - Read ALL 21 dept daily_briefs
  - Identify cross-dept patterns, blockers, wins
  - Write: shared-context/corp/proposals/RETRO_<date>.md

strategy/product-manager-agent:
  - Synthesize retro into CEO proposals
  - Write to: shared-context/corp/proposals/PROPOSAL_<date>_<topic>.md
  - Proposals: KPI_CHANGE | NEW_SKILL | ROLE_CHANGE | STRATEGIC

CEO receives proposals → next Phase 1
```

---

## Cycle Reset

After Phase 7:
```
Update: brain/shared-context/corp/kpi_scoreboard.json (actual values from briefs)
Write: corp/memory/departments/<dept>.md (cycle summary by each manager)
Reset: brain/shared-context/blackboard.json corp_cycle_status = "IDLE"
Clear: done task cards from subagents/mq/<dept>_tasks.md
Archive: daily_briefs to archive/daily_briefs/<date>/

[HUD UPDATE — auto, non-blocking]:
  powershell ops/scripts/update_hud.ps1 -Quiet
  → Updates hud/STATUS.json (services, open items, cycle count)
  → Updates hud/HUD.md services + corp status table
  → Creates hud/snapshots/<date>_<time>.md
  → Sends Telegram summary (if configured)
  On failure: skip — do NOT block cycle reset
```

**Note:** At Phase 0 start, set `blackboard.json corp_cycle_status = "RUNNING"`.
This prevents two concurrent cycles. Reset to "IDLE" only after Phase 7 completes.


---

## CLI Trigger Commands

| Command | Phases Run |
|---------|-----------|
| `aos corp start` | Phases 1–7 (full cycle) |
| `aos corp brief` | Phase 1 (CEO brief only) |
| `aos corp dispatch <dept>` | Phase 3 for one dept |
| `aos corp gate qa <T-ID>` | Phase 5 GATE_QA only |
| `aos corp gate security <item>` | Phase 5 GATE_SECURITY only |
| `aos corp kpi` | Show kpi_scoreboard.json |
| `aos corp escalate L3 <msg>` | Write L3 straight to escalations.md |
| `aos corp retro` | Phases 6–7 only (reflect + propose) |
| `aos corp status` | Show cycle status |

---

## Emergency Override

If CEO needs to intervene mid-cycle:
```
1. Write to escalations.md: "CEO OVERRIDE — [reason]"
2. Affected C-Suite pauses dept work immediately
3. CEO decision logged to decisions_log.md
4. Work resumes with new direction
```

---

*"The cycle doesn't run on a clock. It runs when the CEO decides to run it. That's control."*
