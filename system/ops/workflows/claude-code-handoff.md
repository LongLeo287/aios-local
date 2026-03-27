# Department: engineering
---
description: Antigravity â†’ Claude Code CLI handoff â€” quy trÃ¬nh duy nháº¥t, Ä‘áº§y Ä‘á»§
---
# Claude Code Handoff Protocol
# Version: 3.0 | Updated: 2026-03-26 | SINGLE SOURCE OF TRUTH
# Merges: claude-code-handoff.md v2.0 + automated_cli_handoff.md v2.1

// turbo-all

---

## Khi NÃ o Antigravity Handoff Sang Claude Code?

| Task Type | LÃ½ do dÃ¹ng Claude Code |
|---|---|
| Viáº¿t code phá»©c táº¡p (>200 dÃ²ng) | Long-context code generation |
| Multi-file refactoring | DEVELOPER role + bash execution |
| Cháº¡y shell/PS1 commands hÃ ng loáº¡t | Native execution, khÃ´ng cáº§n confirm |
| Táº¡o/debug test suite | QA role + sub-agent isolation |
| Reverse engineering repo cÅ© | RESEARCHER role + file traversal |
| CIV: phÃ¢n tÃ­ch repo phá»©c táº¡p | gitingest + code analysis |
| Dá»n dáº¹p/di dá»i file hÃ ng loáº¡t | Auto-mode, CEO Ä‘Ã£ approve trÆ°á»›c |

---

## Luá»“ng HoÃ n Chá»‰nh (Antigravity â†’ Claude Code â†’ Antigravity)

```
[ANTIGRAVITY]
    â”‚  1. Chuáº©n bá»‹ task (CEO approve hoáº·c Phase 4 daily cycle)
    â”‚  2. Viáº¿t task detail â†’ subagents/mq/claude_code_tasks.md
    â”‚  3. Ghi blackboard.json: handoff_trigger = "READY"
    â”‚  4. Gá»i launcher: ops/scripts/handoff_to_claude_code.ps1
    â–¼
[LAUNCHER SCRIPT â€” 5 Safety Checks]
    â”‚  âœ“ .clauderules tá»“n táº¡i?
    â”‚  âœ“ .claudeignore tá»“n táº¡i?
    â”‚  âœ“ blackboard.json cÃ³ handoff_trigger = "READY"?
    â”‚  âœ“ Gatekeeper GRANT workspace?
    â”‚  âœ“ Git snapshot táº¡o thÃ nh cÃ´ng?
    â”‚  â†’ Chá»n mode: SUPERVISED (1) hoáº·c AUTONOMOUS (2)
    â–¼
[CLAUDE CODE CLI]
    â”‚  Boot: Ä‘á»c CLAUDE.md â†’ blackboard.json â†’ task file
    â”‚  Thá»±c thi task theo role (DEVELOPER/QA/RESEARCHER)
    â”‚  Viáº¿t receipt â†’ telemetry/receipts/
    â”‚  Cáº­p nháº­t blackboard: handoff_trigger = "COMPLETE" | "BLOCKED"
    â–¼
[ANTIGRAVITY]
       Monitor blackboard
       COMPLETE â†’ Ä‘á»c receipt â†’ bÃ¡o CEO (tiáº¿ng Viá»‡t)
       BLOCKED  â†’ Ä‘á»c failure notes â†’ retry hoáº·c escalate
       Reset: handoff_trigger = null
```

---

## Step 1: Antigravity Chuáº©n Bá»‹ Task

### 1a. Viáº¿t task vÃ o queue
File: `subagents/mq/claude_code_tasks.md`
```markdown
# Claude Code Task â€” CC-YYYYMMDD-XXX
Priority: HIGH | MEDIUM | LOW
Roles: DEVELOPER | QA | RESEARCHER

## Context
<ngá»¯ cáº£nh ngáº¯n gá»n>

## Task Steps
- [ ] Step 1: ...
- [ ] Step 2: ...

## Acceptance Criteria
- [ ] TiÃªu chÃ­ 1
- [ ] TiÃªu chÃ­ 2

## RECEIPT (REQUIRED)
Write: telemetry/receipts/<task-id>.md
```

### 1b. Cáº­p nháº­t blackboard
File: `brain/shared-context/blackboard.json`
```json
{
  "handoff_trigger": "READY",
  "source_agent": "Antigravity",
  "target_agent": "Claude Code",
  "task_payload": {
    "task_id": "CC-YYYYMMDD-XXX",
    "description": "<mÃ´ táº£ ngáº¯n>",
    "task_file": "subagents/mq/claude_code_tasks.md",
    "workspace_id": "<PRJ-XXX>",
    "workspace_path": "<AI_OS_ROOT>",
    "priority": "HIGH"
  },
  "blackboard_updated_at": "<ISO 8601>"
}
```

### 1c. Gá»i launcher
```powershell
& "<AI_OS_ROOT>\ops\scripts\handoff_to_claude_code.ps1"
```

---

## Step 2: Chá»n Execution Mode

Launcher hiá»‡n 2 lá»±a chá»n (auto-select SUPERVISED sau 15s):

| Mode | Flag | Khi nÃ o dÃ¹ng |
|---|---|---|
| **SUPERVISED** (default) | `claude` | Task cÃ³ rá»§i ro, cáº§n review |
| **AUTONOMOUS** | `claude --enable-auto-mode` | CEO Ä‘Ã£ approve, task rÃµ rÃ ng |

> âš ï¸ `--dangerously-skip-permissions` Ä‘Ã£ DEPRECATED â€” dÃ¹ng `--enable-auto-mode`

---

## Step 3: Claude Code Boot Khi Nháº­n Handoff

Claude Code tá»± Ä‘á»™ng Ä‘á»c theo thá»© tá»±:
1. `CLAUDE.md` (boot protocol)
2. `brain/shared-context/blackboard.json` â†’ tÃ¬m `handoff_trigger: "READY"`
3. `subagents/mq/claude_code_tasks.md` â†’ task steps
4. Thá»±c thi theo role â†’ viáº¿t receipt â†’ cáº­p nháº­t blackboard

---

## Step 4: Antigravity Nháº­n Káº¿t Quáº£

```
Monitor: brain/shared-context/blackboard.json
  â†’ "COMPLETE" : Ä‘á»c receipt â†’ bÃ¡o CEO báº±ng tiáº¿ng Viá»‡t â†’ reset blackboard
  â†’ "BLOCKED"  : Ä‘á»c blocked_task â†’ retry hoáº·c escalate CEO
  â†’ Reset: { "handoff_trigger": null, "blocked_task": null }
```

---

## Capabilities Cá»§a Claude Code Trong AI OS

```
1. Auto-execute (--enable-auto-mode)     â†’ HÃ ng loáº¡t file ops khÃ´ng cáº§n confirm
2. Sub-agent spawning (isolated context) â†’ Parallel testing, parallel writes
3. Long-context code gen (200K tokens)   â†’ Viáº¿t module lá»›n khÃ´ng bá»‹ truncation
4. DEVELOPER â†’ QA â†’ RESEARCHER roles    â†’ Self-review code vá»«a viáº¿t
5. Native git integration               â†’ Snapshot trÆ°á»›c task, reset --hard náº¿u fail
6. .claude/commands/ slash commands     â†’ /project:aos-intake, /project:vet-repo
```

---

## CIV Integration

Khi Claude Code nháº­n task intake repo:
1. Äá»c `corp/departments/content_intake/WORKER_PROMPT.md` (v1.2)
2. Cháº¡y STEP 0: LightRAG check
3. Fill `_CIV_ANALYSIS.md` 6 cÃ¢u â†’ trigger STEP 3.6 via blackboard

---

*v3.0 | 2026-03-26 | Merged from: claude-code-handoff.md v2.0 + automated_cli_handoff.md v2.1*
*"Antigravity thinks. Claude Code acts. One handoff, one truth."*

