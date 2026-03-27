# Department: operations
# execution_template.md -- Standard Task Format for Claude Code (Phase 5)
# Version: 1.0 | Updated: 2026-03-14
# Authority: Tier 2 (Operations)
#
# HOW TO USE:
# Antigravity fills this template and saves it as the task_file in blackboard.json
# Claude Code reads this file at the start of Phase 5 and follows it exactly.
# DO NOT deviate from this structure.

---

## Task Header (Filled by Antigravity)

```
TASK_ID     : <unique ID e.g. TASK-20260314-001>
WORKSPACE   : <absolute path to target workspace>
PRIORITY    : HIGH | MEDIUM | LOW
CREATED_AT  : <ISO 8601>
APPROVED_BY : Antigravity (user approved in Phase 3)
```

---

## Context (Filled by Antigravity)

```
PROJECT     : <project name>
PHASE       : <current project phase e.g. "Phase 10: Intelligent Assistant">
BACKGROUND  : <1-3 sentences: what is this task part of>
GOAL        : <1 sentence: what success looks like>
CONSTRAINTS :
  - <constraint 1 e.g. "Do not modify production database">
  - <constraint 2>
```

---

## Skills Available (Auto-populated by skill_loader)

Claude Code reads from `<AI_OS_ROOT>\shared-context\SKILL_REGISTRY.json`

Key skills for this task:
```
- context_manager   (Tier 1, always loaded)
- reasoning_engine  (Tier 1, always loaded)
- resilience_engine (Tier 1, always loaded)
- <skill_id>        (load when role requires -- see SUBAGENT_PROTOCOL.md)
```

---

## Steps (Filled by Antigravity, executed by Claude Code)

Each step follows the format below. Claude Code executes in order.

---

### STEP 1: <Descriptive Title>

```
Role        : DEVELOPER | QA | RESEARCHER
Depends on  : none | STEP <N>
Input       : <what this step receives as input>
Action      : <specific action -- be precise>
Output      : <what this step must produce>
Success     : <how to verify this step passed>
```

**QA Checklist for this step:**
- [ ] <specific check 1>
- [ ] <specific check 2>

---

### STEP 2: <Descriptive Title>

```
Role        : DEVELOPER | QA | RESEARCHER
Depends on  : STEP 1
Input       : STEP 1 output
Action      : <specific action>
Output      : <what this step must produce>
Success     : <verification criteria>
```

**QA Checklist for this step:**
- [ ] <specific check>

---

### STEP N: QA Final Review

```
Role        : QA
Depends on  : ALL previous DEVELOPER steps
Input       : All DEV receipts from this run
Action      : Run full QA pass on all outputs
Output      : Final QA report (PASS | PARTIAL | FAIL)
Success     : All critical checks pass
```

**QA Final Checklist:**
- [ ] All STEP outputs exist and are correct
- [ ] No regressions introduced
- [ ] All receipts written to telemetry/receipts/
- [ ] task.md checkboxes updated

---

### STEP FINAL: Synthesis & Handoff

```
Role        : DEVELOPER (acting as Manager)
Depends on  : STEP N (QA Final Review)
Input       : All receipts from this run
Action      : Aggregate receipts, write synthesis to blackboard.json
Output      : blackboard.json updated with:
              handoff_trigger: "COMPLETE" | "BLOCKED"
              result.summary: English text summary
              result.files_modified: [list]
              result.outcome: SUCCESS | PARTIAL | FAILURE
Success     : blackboard.json updated, Antigravity can read it
```

---

## Receipts Location

All receipts for this task go to:
```
<workspace_path>\telemetry\receipts\<ROLE>_<step>_<timestamp>.json
```

If folder doesn't exist, CREATE IT before writing first receipt.

---

## Error Handling Reference

If any step FAILS twice:
1. Write receipt with status: "BLOCKED"
2. Set blackboard.json handoff_trigger: "BLOCKED"
3. Include failure details in result.notes
4. STOP. Do not continue.

Refer to: `corp/rules/CLAUDE_CODE_MANAGER.md` for full fix-retry loop.

---

## Example: Filled Template

```
TASK_ID     : TASK-20260314-001
WORKSPACE   : D:\APP\BookMark Extension
PRIORITY    : HIGH
GOAL        : Implement semantic search in the bookmark extension popup

STEP 1:
Role        : RESEARCHER
Action      : Read existing search code in popup.js and service-worker.js
              Query smart_memory for any previous research on embedding-based search
Output      : Research notes on current search implementation + recommended approach

STEP 2:
Role        : DEVELOPER
Depends on  : STEP 1
Action      : Implement SemanticSearchService.js using the approach from STEP 1
              Add embedding generation on bookmark save
Output      : SemanticSearchService.js created

STEP 3:
Role        : QA
Depends on  : STEP 2
Action      : Test semantic search with 3 sample queries
              Check: correct results returned, no performance regression
Output      : QA receipt with test results

STEP 4:
Role        : DEVELOPER (fix if QA FAIL)
Depends on  : STEP 3 result
Action      : Fix issues from QA receipt if any
Output      : Fixed SemanticSearchService.js

STEP FINAL:
Role        : DEVELOPER
Action      : Synthesize all receipts, update blackboard.json
```

---

*"A task without a template is ambition without direction."*

