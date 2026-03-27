---
id: resilience_engine
name: Resilience Engine
version: 1.0.0
tier: 1
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Circuit breakers, retry logic, and self-healing protocols.

accessible_by:
  - All agents

dependencies: []

exposed_functions:
  - name: circuit_breaker
  - name: retry_with_backoff
  - name: error_recovery
  - name: fallback_plan

consumed_by:
  - shell_assistant
  - web_intelligence
emits_events:
  - circuit_opened
  - recovery_triggered
listens_to:
  - tool_failed
---
# ðŸ›¡ï¸ Resilience Engine Skill (Circuit Breaker & Self-Healing)

## Description
This skill provides the AI OS with "Survival Instincts" and automated error recovery. It monitors tool failures, manages circuit breakers, and generates recovery patches for systemic issues.

## ðŸ› ï¸ Core Functions:
1.  **Circuit Breaker (/trip):** Monitor tool execution. If a tool fails 2 times with the same error, "trip" the breaker and move to **REASONING** phase to change tactics.
2.  **State Checkpointing (/checkpoint):** Save the current `task.md` and `implementation_plan.md` to `.agents/telemetry/checkpoints/` before high-risk edits.
3.  **Self-Correction (/correct):** After a failure, analyze the "Root Cause" using the [Reasoning Engine](file:///d:/APP/BookMark%20Extension/.agents/skills/reasoning_engine/SKILL.md) and generate a "Recovery Patch."

## ðŸ“‹ Instructions:
If a tool errors:
1. Don't just retry. Check the `resilience_engine` for the **Circuit Breaker** status.
2. If the error is systemic (e.g., API quota, repeated syntax error), SUSPEND execution and notify the user with a "Post-Mortem" report.

## Principle:
*"Stability is the foundation of autonomy."*

