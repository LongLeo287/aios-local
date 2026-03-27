---
id: reasoning_engine
name: Reasoning Engine
version: 1.0.0
tier: 1
status: active
author: AI OS Core Team
updated: 2026-03-14
description: First-principles problem decomposition and technical logic chains.

accessible_by:
  - Orchestrator
  - Claude Code
  - Antigravity

dependencies:
  - context_manager

exposed_functions:
  - name: decompose_problem
  - name: evaluate_tradeoffs
  - name: chain_of_thought

consumed_by:
  - orchestrator_pro
  - insight_engine
  - production_qa
  - security_shield
emits_events: []
listens_to: []
---
# ðŸ§  Reasoning Engine Skill (Think Better)

This skill upgrades the Agent's cognitive process, moving from generic responses to high-fidelity engineering reasoning.

## ðŸ› ï¸ Frameworks:
- **MECE (Issue Tree):** Use this to break down complex tasks into independent sub-tasks.
- **Weighted Matrix:** Use this when choosing between multiple implementation options ($A$ vs $B$).
- **Pre-Mortem:** Ask: "Imagine it's 6 months from now and this feature failed. Why did it happen?"
- **Logic Tree:** Visualize the dependencies of a problem.

## ðŸ“‹ Instructions:
When faced with a "What should I do?" or "Which way is better?" request:
1.  **Categorize:** Is it a *Decision* (Options) or a *Problem* (Root Cause)?
2.  **Apply Framework:**
    - If Decision: Use `/make-decision` (Weighted Matrix).
    - If Problem: Use `/problem-solving-pro` (Issue Tree + MECE).
3.  **Check Biases:** Cross-reference [Cognitive Biases](file:///d:/APP/BookMark%20Extension/.agents/rules/cognitive_biases.md).
4.  **Journal:** Output a "Decision Journal" block explaining the *Why* behind the *What*.

## Commands:
- `/make-decision`: Triggers weighted comparison.
- `/problem-solving-pro`: Triggers root-cause analysis.

