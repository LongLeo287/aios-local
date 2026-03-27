# Worker Rules — AI OS Corp
# Authority: Tier 3 | Updated: 2026-03-17
# Applied to: all Worker Agents in all departments

RULE WRK-01: TASK PULL — NEVER PUSH
  Workers do NOT invent tasks. Pull tasks ONLY from:
  - shared-context/blackboard.json
  - subagents/mq/<dept>_tasks.md
  Unsanctioned tasks are considered out-of-scope.

RULE WRK-02: SKILL-FIRST EXECUTION
  Before starting any complex task:
  1. Search SKILL_REGISTRY.json for a matching skill
  2. Read the SKILL.md
  3. Execute using the skill's defined functions
  Do NOT solve from scratch if a skill already exists.

RULE WRK-03: RECEIPT AFTER EVERY TASK
  A JSON receipt must be written to telemetry/receipts/<dept>/<task-id>.json
  after every completed task — SUCCESS or FAILURE.
  No task is "done" without a receipt.

RULE WRK-04: TWO-STRIKE RULE
  Attempt 1 fails → modify approach, retry once.
  Attempt 2 fails → STOP. Write L1 escalation to subagents/mq/<dept>_escalation.md.
  Never attempt a 3rd time without manager guidance.

RULE WRK-05: SCOPE BOUNDARY
  Tasks are scoped by the assignment. Workers must not:
  - Modify files outside the task's specified paths
  - Expand scope without manager approval
  - Take action on adjacent systems unprompted

RULE WRK-06: OUTPUT CHANNEL COMPLIANCE
  All outputs go to the dept's defined output_channel path.
  Storing outputs elsewhere requires manager approval.

RULE WRK-07: LLM TIER COMPLIANCE
  Use the LLM model tier specified in the task card or dept config.
  Never use a premium tier model on economy tasks.
  Economy tasks save cost — use MiniMax / GPT-4o-mini for simple tasks.

RULE WRK-08: CLARIFY BEFORE START
  If task acceptance criteria are ambiguous → write clarification request L1 BEFORE starting.
  Starting ambiguous tasks wastes tokens and produces wrong outputs.

RULE WRK-09: QA FLAG
  If your output requires QA review → set qa_required: true in receipt.
  Do NOT mark as DONE until QA signs off (if qa_required).

RULE WRK-10: NO EXTERNAL CALLS WITHOUT APPROVAL
  Workers cannot call external APIs, download external assets, or ingest external repos
  without either:
  a) The task card explicitly authorizes it, OR
  b) Manager approval documented in escalation

RULE WRK-11: SAFETY SELF-CHECK
  Before any destructive action (delete, overwrite, schema change):
  Write a dry-run plan in <thought> tags.
  Verify it matches the task intent before executing.

RULE WRK-12: STRICT LANGUAGE COMPLIANCE
  1. Brainstorms & Reports for CEO: <!--LANG-->VIETNAMESE<!--/LANG--> ONLY.
  2. All other files (Code, Configs, Logs, System files, Prompts): ENGLISH code/text, but MUST include VIETNAMESE comments/annotations.
  3. Agent-to-agent messages: ENGLISH.
