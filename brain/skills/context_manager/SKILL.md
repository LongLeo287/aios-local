---
id: context_manager
name: Context Manager
version: 1.1.0
tier: 1
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Context compression and token budget management. Must load first at every session.

accessible_by:
  - Orchestrator
  - Claude Code
  - All agents

dependencies: []

exposed_functions:
  - name: compress_context
    description: Reduce token count while preserving semantic density
    input: string (raw context)
    output: string (compressed context)
  - name: budget_tokens
    description: Allocate token budget across task steps
    input: object (task_plan)
    output: object (budget_plan)
  - name: export_context
    description: Package current session context for handoff
    input: null
    output: object (context_snapshot)

consumed_by:
  - reasoning_engine
  - orchestrator_pro

emits_events:
  - context_compressed
  - budget_warning

listens_to:
  - session_start
  - context_overflow
---

# Context Manager Skill

## Purpose

Context Manager is a Tier 1 Core skill -- it MUST be loaded before any other skill.
Ensures agents never run out of token budget mid-task and context is preserved across handoffs.

## Exposed Functions

### compress_context
Applies semantic compression to reduce token count by up to 40%.
Preserves: proper nouns, file paths, IDs, action verbs, numeric values, logical connectors.
Discards: filler phrases, repeated information, decorative language.

### budget_tokens
Given a task plan with N steps, allocates token budget proportionally.
Planning: 10% each | Execution: 20% each | Reporting: 5% each | Buffer: 15%.

### export_context
Packages current session state into a portable snapshot for handoff.
Save output to blackboard.json under task_payload.context_snapshot.

## Load Behavior

- Tier 1 Eager: loaded automatically at session start
- No dependencies: first in boot chain
- Thread-safe: callable from any agent without locking

## Events

- Emits context_compressed: {original_tokens, compressed_tokens, ratio}
- Emits budget_warning: when step exceeds allocated budget by >20%
- Listens session_start: reset internal counters
- Listens context_overflow: trigger emergency compression
