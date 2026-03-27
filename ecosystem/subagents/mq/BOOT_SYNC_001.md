# TASK: BOOT-SYNC-001 — Sync CLAUDE.md Boot Sequence
# From: Antigravity | Date: 2026-03-22 | Priority: HIGH

## Context
GEMINI.md boot sequence has been updated with 2 new steps.
CLAUDE.md must match identically.

New rules created:
- `brain/knowledge/notes/RULE-STORAGE-01-storage-location.md` (existing)
- `brain/knowledge/notes/RULE-STRUCTURE-01-system-structure.md` (new, created 2026-03-22)

## What to do

In `CLAUDE.md`, find this section in the BOOT SEQUENCE block:

```
STEP 9   ──► Load Skill Registry                    [brain/shared-context/SKILL_REGISTRY.json]
STEP 10  ──► Begin work
```

Add 2 lines between them so it becomes:

```
STEP 9   ──► Load Skill Registry                    [brain/shared-context/SKILL_REGISTRY.json]
STEP 9.5 ──► Load Storage Rule                      [brain/knowledge/notes/RULE-STORAGE-01-storage-location.md]
STEP 9.6 ──► Load Structure Rule                    [brain/knowledge/notes/RULE-STRUCTURE-01-system-structure.md]
STEP 10  ──► Begin work
```

## After completing
Update `brain/shared-context/blackboard.json`:
- Set `handoff_trigger` to `"COMPLETE"`
- Add to `milestones_achieved`: `"Cycle 6: Boot sequence synced (CLAUDE.md + GEMINI.md unified)"`
- Remove `handoff_task` block (task done)
