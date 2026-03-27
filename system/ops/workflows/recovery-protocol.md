# Department: operations
---
description: How to recover agent state after a session reset, context compression, or context rot
---

# Recovery Protocol — AI OS Corp
# Version: 2.0 | Updated: 2026-03-22
# Authority: Tier 2 (Operations)
# Trigger: Automatically by CLAUDE.md boot fallback | Manually when agent detects context rot

---

## What is Context Rot?

Context rot = agent loses awareness of:
- Current active task or cycle phase
- Recent decisions or changes
- Which governance rules apply right now

Signs: agent asks questions already answered, re-does completed work, ignores open blockers.

---

## Recovery Steps

### Step 1: Re-Boot from CLAUDE.md

Follow the full boot sequence in `CLAUDE.md` Section 2:

```
STEP 1  → Read CLAUDE.md                        (this re-grounds you)
STEP 2  → Read brain/shared-context/SOUL.md     (identity + values)
STEP 3  → Read brain/shared-context/GOVERNANCE.md
STEP 4  → Read brain/shared-context/AGENTS.md
STEP 5  → Read brain/shared-context/THESIS.md
STEP 6  → Read brain/shared-context/report_formats.md
STEP 7  → Read brain/shared-context/blackboard.json   ← KEY: find current task
STEP 8  → Read brain/shared-context/SKILL_REGISTRY.json
```

---

### Step 2: Read Blackboard State

`brain/shared-context/blackboard.json` tells you:

| Field | Meaning |
|-------|---------|
| `handoff_trigger` | READY / COMPLETE / BLOCKED / CYCLE_START / null |
| `task_payload.task_id` | Active task ID |
| `task_payload.task_file` | Path to task definition |
| `task_payload.workspace_path` | Where to work |
| `corp_state.corp_cycle_status` | IDLE / RUNNING |
| `open_items[]` | Pending items this cycle |

---

### Step 3: Check Subagent Message Queue

Read messages addressed to you:
```
subagents/mq/claude_code_tasks.md         ← tasks from C-Suite/managers
subagents/mq/<dept>_escalation.md         ← pending L1 escalations
subagents/mq/BOOT_SYNC_*.md               ← boot sync messages
```

---

### Step 4: Check Recent Receipts

```
telemetry/receipts/                        ← what was completed last session
brain/shared-context/corp/daily_briefs/   ← what depts reported
```

---

### Step 5: State Re-Broadcast

After reading the above, briefly state reconstructed context to CEO:

```
"Context recovered.
 Current cycle: [N] | Status: [corp_cycle_status]
 Active task: [task_id] — [description]
 Last action: [from most recent receipt]
 Open blockers: [from open_items or escalations]
 Ready to continue."
```

---

## Emergency Recovery (BLOCKED state)

If blackboard shows `handoff_trigger: "BLOCKED"`:

```
1. Read: blocked_task.reason + escalation_ref
2. Read: subagents/mq/<dept>_escalation.md for full context
3. Check: has manager responded? (look for response below the L1 escalation)
4. If YES → read manager instructions → resume with new approach
5. If NO  → report BLOCKED status to CEO, await instruction
6. Do NOT retry the same failed approach
```

---

## Git Rollback (if files corrupted)

If file system state is corrupted from a failed Claude Code run:

```powershell
cd <workspace_path>
git log --oneline -5              # find last good snapshot commit
git reset --hard <commit-hash>    # roll back to that state
```

Snapshots are created by `claude_code_handoff.md` Step 1 before each run.

---

*"A recovered agent that knows where it is — is better than a confused agent that keeps going."*
