# ORCHESTRATION_SOP.md — AI OS Master Operational Loop
# Version: 4.0 | Updated: 2026-03-17
# Authority: Tier 2 (Operations)
# Replaces: v3.0 (6-dept structure, no corp mode awareness)
#
# Two parallel loops: Personal AI OS loop + Corp Mode loop.

---

## Part A: PERSONAL AI OS — 6-Phase Loop

```
USER TRIGGER
    │
    v
[1] BOOT        ── Read CLAUDE.md, load skills, load org_chart
    │
    v
[2] ANALYZE     ── Cross-session recall, scan workspace
    │
    v
[3] PLAN        ── Antigravity brainstorms → User reviews → chốt
    │
    v   (user approved)
[4] DELEGATE    ── Auto-handoff to Claude Code (fully automatic)
    │
    v
[5] EXECUTE     ── Claude Code sub-agents work, write receipts
    │
    v
[6] REPORT      ── Read receipts → synthesize → Vietnamese Mermaid → USER
    │
    v
LOOP RESET
```

### Phase 1: BOOT
**Trigger:** "start / khởi động / boot / read AI OS"
**Goal:** Full OS context before any work

```
1. Read d:\Project\AI OS\CLAUDE.md
2. Read rules\CLAUDE_CODE_MANAGER.md   (if Claude Code session)
3. Load SKILL_REGISTRY.json            (verify skill graph current)
4. Read corp/org_chart.yaml            (current 13-dept structure)
5. Execute: workflows/pre-session.md
6. Announce: "Boot complete. [N] skills | Corp: [N depts active]"
```

### Phase 2: ANALYZE
**Goal:** Situational awareness before planning

```
1. Scan workspace structure
2. Recall: smart_memory (last session) + cosmic_memory (long-term)
3. Read shared-context/THESIS.md
4. Read open task.md files
5. Check telemetry/receipts/ for last run results
6. <thought> internal analysis: state / open / blockers / recommended focus </thought>
```

### Phase 3: PLAN (Human-in-the-Loop)
**Gate: USER must approve before Phase 4**

```
3a. Antigravity self-brainstorm:
    - Mermaid diagram: phases/flows
    - Table: options with tradeoffs
    - Risks and open questions
    - Vietnamese to user

3b. User reviews → Approve | Edit | Back-and-forth

3c. On approval:
    - Finalize implementation_plan.md
    - Finalize task.md (atomic steps + agent assignments)
    - Write blackboard.json: { handoff_trigger: "READY", ... }
```

### Phase 4: DELEGATE (Fully Automatic)
**Trigger:** blackboard.json handoff_trigger == "READY" + user approved
**No human intervention in this phase**

```
1. Run: scripts\handoff_to_claude_code.ps1
   CHECK 1: .clauderules exists
   CHECK 2: .claudeignore exists
   CHECK 3: blackboard.json = READY
   CHECK 4: Gatekeeper GRANT for workspace
   CHECK 5: Git snapshot in target workspace

2. Launch: claude --dangerously-skip-permissions "[startup prompt]"
   Claude Code reads .clauderules → reads blackboard.json → [EXECUTION] mode
```

### Phase 5: EXECUTE (Claude Code Autonomous)

```
For each step in task.md:
  1. Read step requirements
  2. Assign to role:
     [DEVELOPER]  → implement / write / code
     [QA]         → validate output
     [RESEARCHER] → gather context
  3. Execute with Circuit Breaker
  4. Write receipt: telemetry/receipts/STEP_<id>_<ts>.json
  5. Update task.md checkbox [x]
  6. FAIL x2 → blackboard handoff_trigger = "BLOCKED", stop

On completion:
  blackboard.json: { handoff_trigger: "COMPLETE", result: { ... } }
```

### Phase 6: REPORT
**Trigger:** blackboard.json handoff_trigger == "COMPLETE"

```
1. Read blackboard.json result.summary     (English from Claude Code)
2. Read telemetry/receipts/* for this run
3. cognitive_reflector.reflect_on_task
4. cosmic_memory.extract_observation
5. smart_memory.consolidate_memory
6. Generate Vietnamese Mermaid report to user
7. Reset: blackboard handoff_trigger = null, status = IDLE
8. Run: skill_loader.ps1
9. Run: archivist.rotate_logs
```

---

## Part B: CORP MODE — 7-Phase Daily Cycle

> Full detail in: `workflows/corp-daily-cycle.md`

```
[C1] CEO BRIEF     ── CEO reads mission, KPIs, escalations
      │
[C2] C-SUITE DISPATCH ── C-Suite translates strategy → dept goals
      │
[C3] DEPT DISPATCH ── Dept heads assign tasks to workers
      │
[C4] EXECUTE       ── Workers execute, write receipts
      │
[C5] GATE          ── GATE_QA / GATE_CONTENT / GATE_SECURITY / GATE_LEGAL
      │
[C6] BRIEF BACK    ── Dept heads write daily_briefs
      │
[C7] REFLECT + PROPOSE ── cognitive_reflector → proposals → CEO
      │
CEO decides → next cycle
```

### Corp Trigger Commands

| Command | Action |
|---------|--------|
| `aos corp start` | Begin Phase C1–C7 |
| `aos corp brief <dept>` | Brief one dept |
| `aos corp gate qa <item>` | Trigger GATE_QA |
| `aos corp kpi` | Show KPI scoreboard |
| `aos corp escalate L3 <msg>` | Write L3 escalation |
| `aos corp retro` | Run Phase C6–C7 only |

---

## Part C: Failure Handling

| Failure | Where | Action |
|---------|-------|--------|
| Skill not found | Phase 1 | `skill_loader.ps1` retry |
| User rejects plan | Phase 3 | Regenerate, back to 3a |
| Gatekeeper DENY | Phase 4 | Stop. Report to user. Check registry |
| Claude Code BLOCKED | Phase 5 | Read failure notes. User decides |
| Incomplete receipts | Phase 6 | Report partial, flag missing |
| GATE_QA FAIL | Corp C5 | Return to worker, fix, re-submit |
| L3 escalation open | Corp any | Block affected work. CEO responds |
| Security CRITICAL | Corp any | Pause all affected. Notify CEO immediately |

---

## Part D: Language Policy

| Phase | Language |
|-------|---------|
| Boot/Analyze (internal) | English in `<thought>` tags |
| Plan brainstorm to user | Vietnamese |
| Plan files (impl_plan, task.md) | English |
| Delegate/Execute (blackboard, receipts, code) | English |
| Claude Code → Antigravity report | English |
| Antigravity → User report | Vietnamese Mermaid |
| Corp brief files (daily_briefs) | English |
| Corp proposals to CEO | Vietnamese summary + English detail |
| Worker receipts | English JSON |

---

*"The loop is not a circle. It is a spiral — each cycle leaves the system smarter."*
