# SUBAGENT PROTOCOL
# Version: 1.0 | Owner: Claude Code (Tier 2)
# Purpose: Rules for sub-agent spawning in Claude Code CLI

## Rule 1: Always pass context explicitly
Sub-agents do NOT inherit parent context.
Pass: task_id, workspace_path, acceptance_criteria, files_to_read

## Rule 2: Circuit Breaker
Failure 1 → alternative approach
Failure 2 → STOP, update blackboard status=BLOCKED

## Rule 3: Write receipt on completion
Path: telemetry/receipts/<dept>/<task_id>_<timestamp>.json
