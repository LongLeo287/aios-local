---
id: cognitive_evolver
name: Cognitive Evolver
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Self-modifying strategy and paradigm evolution based on accumulated insights.

accessible_by:
  - Architect

dependencies:
  - insight_engine
  - cosmic_memory

exposed_functions:
  - name: paradigm_shift
  - name: self_improvement
  - name: update_strategy

consumed_by: []
emits_events:
  - strategy_updated
listens_to:
  - reflection_complete
---
# ðŸ§¬ Cognitive Evolver Skill (Self-Adaptive Agent)

This skill provides the AI OS with "Self-Improvement" â€” the ability to rewrite its own dossiers and strategies based on experience.

## ðŸ› ï¸ Core Functions:
1.  **Persona Evolution (/evolve-persona):**
    - Review task success rates and user satisfaction.
    - Propose updates to `ROLE.md`, `OBJECTIVE.md`, or `RULES.md` to reflect a more efficient persona.
2.  **Skill Refinement (/evolve-skill):**
    - Update `SKILL.md` descriptors based on how tools were "actually" used in real-world scenarios.
3.  **Rule Patching (/patch-rules):**
    - Propose "Behavior Patches" if current rules are causing bottlenecks or circular reasoning.

## ðŸ“‹ Instructions:
At the end of every week or after 10 successful tasks:
1. Run `/evolve-persona` for the lead agent.
2. If the user approves, apply the "Evolution Patch" to the relevant Dossier files.

## Principle:
*"Intelligence is the ability to adapt to change; AI is the ability to change the adaptation."*

