# CLAUDE_CODE_MANAGER.md â€” Claude Code Fix-Retry Loop Rules
# Version: 1.0 | Created: 2026-03-22
# Referenced by: system/ops/workflows/execution_template.md
# Authority: Tier 2 (Operations)

---

## Overview

This document defines how Claude Code handles task failures, retries, and escalations.
Every task follows the 2-Strike Rule â€” fail twice â†’ BLOCKED â†’ report.

---

## Fix-Retry Loop (Standard)

```
TASK STARTS
    â”‚
    â–¼
ATTEMPT 1
    â”‚
    â”œâ”€â”€ SUCCESS â†’ write receipt â†’ update blackboard â†’ DONE
    â””â”€â”€ FAIL
          â”‚
          â–¼
       Diagnose root cause:
         â–¡ Missing file/resource?  â†’ check paths, read RULE-STORAGE-01
         â–¡ Wrong tool?             â†’ check SKILL_REGISTRY for alternative
         â–¡ Spec ambiguous?         â†’ re-read task_file, check context
         â–¡ Permission error?       â†’ check gatekeeper, verify workspace
         â–¡ Syntax/logic error?     â†’ fix and retry
          â”‚
          â–¼
ATTEMPT 2 (different approach from Attempt 1)
    â”‚
    â”œâ”€â”€ SUCCESS â†’ write receipt â†’ update blackboard â†’ DONE
    â””â”€â”€ FAIL
          â”‚
          â–¼
       2-STRIKE RULE TRIGGERED
          â”‚
          â–¼
       Set blackboard.json: handoff_trigger = "BLOCKED"
       Write L1 escalation to: subagents/mq/<dept>_escalation.md
       STOP â€” do not attempt again without explicit instruction
```

---

## 2-Strike Rule Details

| Strike | Action | Required |
|--------|--------|---------|
| Strike 1 | Diagnose + try different approach | Mandatory |
| Strike 2 | Write L1 escalation with both attempts documented | Mandatory |
| After Strike 2 | STOP â€” set BLOCKED, wait for manager response | Mandatory |

**NEVER:** retry the same approach that failed twice.
**NEVER:** attempt a third time without manager instruction.
**NEVER:** mark task DONE if it didn't fully complete.

---

## L1 Escalation Format

Write to `subagents/mq/<dept>_escalation.md`:

```markdown
## L1 ESCALATION â€” [TASK-ID] â€” [DATETIME]

Agent: claude_code
Task: [task-id] â€” [1-line description]

Attempt 1:
  Approach: [what was tried]
  Result: [error message or outcome]
  Root cause hypothesis: [why it failed]

Attempt 2:
  Approach: [different approach]
  Result: [error message or outcome]
  Root cause hypothesis: [why it also failed]

Blocker: [specific reason â€” tool failure | ambiguous spec | missing resource | permission denied]

Options:
  A. [option] â€” Feasibility: [High/Med/Low]
  B. [option] â€” Feasibility: [High/Med/Low]

Recommendation: [A or B and why]

Files affected: [list any files partially modified]
Rollback needed: YES | NO

Awaiting manager response.
```

---

## Blackboard BLOCKED State

When escalating, update `brain/shared-context/blackboard.json`:

```json
{
  "handoff_trigger": "BLOCKED",
  "blocked_task": {
    "task_id": "<TASK-ID>",
    "blocked_at": "<ISO8601>",
    "reason": "<1-line reason>",
    "escalation_ref": "subagents/mq/<dept>_escalation.md"
  }
}
```

---

## Resuming After BLOCKED

Claude Code resumes a BLOCKED task ONLY when:
1. Manager writes response to `subagents/mq/<dept>_escalation.md`
2. Blackboard `handoff_trigger` is reset to `"RESUME"` by manager
3. New approach or resource is explicitly provided

On resume: read the manager response â†’ attempt 3 (with new approach) â†’ if fails again â†’ L2 escalation.

---

## File Operation Safety Rules

Before any destructive file operation (delete, overwrite, move):
```
â–¡ Is this file in the authorized workspace? (check gatekeeper)
â–¡ Is there a backup or is this recoverable from git?
â–¡ Did the task spec explicitly authorize this operation?

If any answer is NO â†’ ask CEO before proceeding
```

---

## Receipt Format (on DONE)

Write to `telemetry/receipts/<dept>/<TASK-ID>.json`:

```json
{
  "task_id": "<TASK-ID>",
  "agent": "claude_code",
  "workspace": "<path>",
  "started_at": "<ISO8601>",
  "completed_at": "<ISO8601>",
  "attempts": 1,
  "outcome": "SUCCESS",
  "files_modified": ["<path1>", "<path2>"],
  "notes": "<optional>"
}
```

---

*"Two strikes and you stop. Escalate. Let a human help. That is wisdom, not weakness."*

