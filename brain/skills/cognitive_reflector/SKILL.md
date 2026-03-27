---
id: cognitive_reflector
name: Cognitive Reflector
display_name: Cognitive Reflector — Metacognition & Self-Reflection
description: >-
  Enables AI OS metacognition. Scans memory and telemetry to identify patterns,
  mistakes, and breakthroughs. Promotes high-value reflections to long-term memory.
version: 1.0.0
tier: 2
category: memory
domain: core
tags: [reflection, metacognition, self-improvement, patterns, memory]
cost_tier: economy
accessible_by:
  - Antigravity
  - Claude Code
dependencies:
  - smart_memory
  - cosmic_memory
exposed_functions:
  - /reflect
  - /consolidate-wisdom
  - /patch-behavior
load_on_boot: false
status: active
---


This skill enables the AI OS to perform "Metacognition" — thinking about its own thoughts and processes to improve long-term performance.

## 🛠️ Core Functions:
1.  **Reflection (/reflect):**
    - Scan `memory/daily/` and `telemetry/logs/`.
    - Identify recurring patterns, mistakes, or breakthroughs.
    - Generate a `reflections.md` file in the current task directory.
2.  **Wisdom Consolidation:**
    - High-value reflections are "promoted" to `shared-context/STRATEGY.md` or `knowledge-base/best_practices.md`.
3.  **Behavior Patching:**
    - If a reflection identifies a rule that causes issues, propose a patch in `.agents/prompts/adaptive_patches/`.

## 📋 Instructions:
After completing any Task (Task Name marked [x]):
1. Trigger `/reflect`.
2. Analyze: "What worked?", "What failed?", "What would I do differently?".
3. Document the "Lesson Learned" in the **Task Receipt**.

## Principle:
*"Experience is raw data; Reflection is wisdom."*
