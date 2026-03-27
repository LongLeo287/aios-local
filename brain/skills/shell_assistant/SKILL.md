---
id: shell_assistant
name: Shell Assistant
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Shell mastery and automated script execution with safety guards.

accessible_by:
  - DevOps
  - Developer
  - Claude Code

dependencies:
  - resilience_engine

exposed_functions:
  - name: execute_command
  - name: generate_script
  - name: parse_output
  - name: safe_run

consumed_by:
  - orchestrator_pro
emits_events:
  - command_executed
  - command_failed
listens_to: []
---
# ðŸš Shell Assistant Skill (Terminal Autonomy)

## Description
This skill provides the AI OS with "Command Mastery" â€” safely generating, explaining, and executing shell commands with absolute clarity and safety guardrails.

## ðŸ› ï¸ Core Functions:
1.  **Command Generation (/suggest-cmd):**
    - Translate natural language tasks into precise shell commands (Copilot-CLI style).
    - Support Git, NPM, File manipulation, and OS-specific commands.
2.  **Safety Loop (/explain-cmd):**
    - Explain the impact of a command before execution.
    - Warn if a command touches restricted zones or contains destructive flags (e.g., `rm -rf /`).
3.  **Error Diagnostics (/debug-shell):**
    - Automatically parse `stderr` from failed commands and propose a fix.

## ðŸ“‹ Instructions:
1. When a task requires terminal action, always `/suggest-cmd` first.
2. Never execute a destructive command without an explicitly documented rationale.
3. Log successful complex command chains to the `Knowledge Hub`.

## Principle:
*"The shell is an instrument; play it with precision, not guesswork."*

