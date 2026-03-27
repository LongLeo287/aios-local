# Department: operations
# corp-learning-loop.md — Post-Cycle Reflection & Memory Update
# Version: 1.0 | Updated: 2026-03-17
# Authority: Tier 2 (Operations) / Strategy + Operations
# Agents: cognitive_reflector + archivist

---

## Overview

The learning loop runs after every corp cycle.
Its purpose: extract wisdom from this cycle → feed it back into memory → improve next cycle.

```
ALL DEPT DAILY BRIEFS
    │
    v
[1] ARCHIVIST    ── Collect + archive telemetry
    │
    v
[2] REFLECTOR    ── Pattern analysis across all depts
    │
    v
[3] MEMORY UPDATE ── Write lessons to dept + global memory
    │
    v
[4] PROPOSALS    ── Strategy dept writes CEO proposals
    │
    v
CEO reads → decides → cycle improves
```

**Trigger (2 modes):**
- **MANDATORY** — Automatically runs as Phase 7 of every `corp-daily-cycle.md` (after Phase 6 BRIEF BACK)
- **ON-DEMAND** — CEO triggers manually with `aos corp retro` to run reflection outside main cycle

Both modes run identical phases. In mandatory mode, cognitive_reflector starts immediately after all 21 dept daily_briefs are written.

---

## Phase 1: Archive (archivist)

```
1. Collect: all shared-context/corp/daily_briefs/*.md for this cycle
2. Archive telemetry:
   - Move telemetry/receipts/<dept>/* → archive/receipts/<YYYY-MM>/<dept>/
   - (if receipt age > 30 days)
3. Rotate dept memory files:
   - For each corp/memory/departments/<dept>.md:
     → Entries older than 30 days → summarize, move to knowledge/
4. Purge agent session memory:
   - corp/memory/agents/*.md entries older than 7 days → delete
5. Write archivist receipt: telemetry/archivist_log.md
```

---

## Phase 2: Auto-Dream Consolidation (cognitive_reflector)

cognitive_reflector triggers a 4-step "REM Sleep" process to extract wisdom without bloating memory.

### Step 2a: Orientation (Định hướng)
- Reads `shared-context/corp/mission.md` (CEO Intent).
- Reads `shared-context/blackboard.json` (Cycle context).
- Sets the "Focus Lens" for what signals matter.

### Step 2b: Gather Signal (Gom Tín Hiệu Thô)
- Scans `telemetry/receipts/<dept>/` for tasks completed this cycle.
- Scans `corp/daily_briefs/BRIEF_<date>.md` for anomalies.

### Step 2c: Consolidation (Hợp Nhất)
- Synthesizes findings into `shared-context/corp/daily_briefs/SYNTHESIS_<date>.md`.
- Formats cross-dept blockers, global wins, and skill gaps.

### Step 2d: Prune & Index (Tỉa rác và Đánh Chỉ Mục)
- Scans `corp/memory/departments/<dept>.md`.
- If a memory file exceeds 200 lines, it forcibly truncates and summarizes the oldest entries.
- Updates the `corp/memory/GLOBAL_INDEX.md` (Hard cap < 100 lines) to map where concepts are stored.

---

## Output format (`SYNTHESIS_<date>.md`):
```markdown
# Auto-Dream Synthesis — [DATE]

## 1. Orientation Context
- Focused on: [CEO Mission snippet]

## 2. Signal Gathered
| Dept | Receipts Scanned | Brief Status |
|------|-----------------|--------------|
| ...  | ...             | ...          |

## 3. Consolidation: Patterns & Blockers
- [Pattern]: affected [N] depts.
- Win: [What worked well]

## 4. Prune Status
- Pruned [N] old memory blocks.
- `GLOBAL_INDEX.md` updated.
```

---

## Phase 3: External Knowledge Ingestion (Optional)

### 3a. Dept Memory (Manager writes)

Each dept manager writes to `corp/memory/departments/<dept>.md`:
```markdown
## Cycle [N] — [DATE]

Goals achieved: [list]
Goals missed: [list] — Root cause: [1 line]
Patterns observed: [actionable facts]
Cross-dept dependencies this cycle: [what we needed from others]
Lessons for next cycle: [specific changes to how we work]
Next cycle focus: [top 3]
```

### 3b. Global Memory (CEO or C-Suite writes)

For significant lessons, write to `corp/memory/global/decisions_log.md`:
```markdown
## [DATE] — [TITLE]
Type: LESSON_LEARNED
Context: [what happened]
Lesson: [distilled fact — 1-2 sentences]
Applied to: [which depts or agents]
```

### 3c. Agent Memory (auto-expiry managed by archivist)

Each agent who was active this cycle updates `corp/memory/agents/<agent>.md`:
```markdown
## [DATE] — Task: <task>
Outcome: SUCCESS | PARTIAL | FAILED
Key lesson: [1 sentence]
Next time: [what to do differently]
```

---

## Phase 4: Proposals to CEO

Strategy dept (product-manager-agent) synthesizes retro findings into:
1. **KPI Change proposals** — if targets are consistently wrong
2. **New skill proposals** — if skill gap found
3. **Agent/Role change proposals** — if a function is missing or misassigned
4. **Strategic proposals** — if pattern reveals strategic risk or opportunity

Each proposal follows format from `corp/departments/strategy/MANAGER_PROMPT.md`
Stored in: `shared-context/corp/proposals/PROPOSAL_<date>_<topic>.md`

---

## Learning Loop Schedule

| When | Trigger | Depth |
|------|---------|-------|
| After each active corp cycle (mandatory) | corp-daily-cycle Phase 7 | Light (skip archive if same-session) |
| On-demand standalone | `aos corp retro` | Light (skip archive) |
| Weekly | `aos corp retro --full` | Full (archive + rotate memory) |
| Monthly | Archivist scheduled | Deep (purge + global summary) |

---

## Feedback Loop: How Proposals Reach Next Cycle Phase 1

```
Phase 7 (THIS cycle) completes
    │
cognitive_reflector writes → shared-context/corp/proposals/RETRO_<date>.md
product-manager-agent writes → shared-context/corp/proposals/PROPOSAL_<date>_*.md
    │
    ▼
Cycle resets: blackboard.json corp_cycle_status = "IDLE"
    │
    ▼
NEXT CYCLE Phase 0 (Pre-flight) → Phase 1 (CEO BRIEF)
    │
CEO reads in Phase 1:
  4. shared-context/corp/proposals/    ← ✅ proposals from this retro are HERE
  3. shared-context/corp/escalations.md
    │
CEO decides → feeds into Phase 2 C-Suite dispatch → cycle improves
```

This closes the loop: every cycle's lessons feed directly into the next cycle's CEO brief.

---

## KPI Table — fix in corp-learning-loop

Note: Phase 2 KPI Summary table says `[all 21 depts]` — should be **all 21 depts**.
When writing RETRO, include all 21 departments in the KPI table.

---

*"A system that doesn't learn from its mistakes gets dumber every cycle. The loop is how we get smarter."*
