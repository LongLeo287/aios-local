---
id: orchestrator_pro
name: Orchestrator Pro
display_name: Orchestrator Pro — Task Decomposition & Parallel Execution
description: >-
  Upgrades the agent from Task Follower to Task Architect. Breaks complex
  objectives into MECE parallelizable plans using a shared blackboard.
version: 1.0.0
tier: 2
category: orchestration
domain: core
tags: [orchestration, decomposition, parallel, blackboard, planning]
cost_tier: standard
accessible_by:
  - Antigravity
  - Claude Code
dependencies:
  - context_manager
  - reasoning_engine
exposed_functions:
  - /decompose
  - /parallelise
  - /route-contingency
load_on_boot: false
status: active
---


## Description
This skill upgrades the Agent from "Task Follower" to "Task Architect." It focuses on breaking down complex objectives into actionable, parallelizable plans using a shared blackboard.

## 🛠️ Core Functions:
1.  **Task Decomposition:** Break complex objectives into a MECE (Mutually Exclusive, Collectively Exhaustive) plan.
2.  **Parallel Execution:** Orchestrate multiple subagents for concurrent task handling.
3.  **Shared Blackboard:**
    - Maintain a global state (`.agents/shared-context/blackboard.json`) for inter-agent communication.
    - Post "Knowledge Snippets" for specialized agents to pick up.
4.  **Model Optimization:** Tailor prompts based on the specific LLM being used (Claude, Qwen, or GPT).
5.  **Contingency Routing:** Redirect tasks if a subagent faces a budget block or repetitive failure.

## 📋 Instructions:
At the start of every complex request:
1. Execute `/decompose`.
2. Update the `implementation_plan.md` with a "Parallel Execution Path."
3. Assign sub-agents from `subagents/` if they are available for specific branches.

## Principle:
*"Break the problem until the solution is obvious."*
