---
id: orchestrator_pro
name: Orchestrator Pro
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Full multi-agent orchestration -- decompose, delegate, monitor, synthesize.

accessible_by:
  - Antigravity

dependencies:
  - reasoning_engine
  - smart_memory
  - notification_bridge
  - shell_assistant

exposed_functions:
  - name: decompose_task
  - name: delegate_to_agent
  - name: monitor_progress
  - name: synthesize_report

consumed_by: []
emits_events:
  - task_delegated
  - phase_complete
listens_to:
  - task_complete
  - task_failed
---

# Orchestrator Pro Agent Skill

## Purpose

Orchestrator Pro is the AI OS "conductor" -- it breaks complex tasks into
parallel/sequential steps, assigns them to the right agents, monitors progress,
and synthesizes a final report. Called exclusively by Antigravity.

## Exposed Functions

### decompose_task
Takes a high-level task description, uses reasoning_engine to break it into
atomic steps with: agent assignment, estimated tokens, dependencies, success criteria.
Output: `task_plan[]` written to blackboard.json.

### delegate_to_agent
Reads task_plan and writes a handoff payload to blackboard.json for each step.
For Claude Code steps: writes `handoff_trigger: "READY"` to trigger `handoff_to_claude_code.ps1`.
For other agents: posts event to `subagents/mq/`.

### monitor_progress
Polls blackboard.json and telemetry/receipts/ for status updates.
Triggers `notification_bridge.send_alert` on stall (no progress after 5 min).
Activates `resilience_engine.circuit_breaker` on BLOCKED status.

### synthesize_report
Reads all receipts from completed steps.
Merges into a unified report using smart_memory.consolidate_memory.
Triggers `cognitive_reflector.reflect_on_task` on completion.
Output: full report in user's language (Vietnamese by default).

## Orchestration Pattern

```
Antigravity
    -> decompose_task (reasoning_engine)
    -> delegate_to_agent (blackboard handoff)
        -> Claude Code (execution)
        -> Other agents (via MQ)
    -> monitor_progress (polling + alerts)
    -> synthesize_report (smart_memory + reflection)
    -> report to user (Vietnamese)
```
