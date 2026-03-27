---
id: cosmic_memory
name: Cosmic Memory
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Observation-based long-term memory for cross-session recall (Smallville style).

accessible_by:
  - Architect
  - Orchestrator

dependencies:
  - smart_memory

exposed_functions:
  - name: extract_observation
  - name: cross_session_recall
  - name: generate_reflection

consumed_by:
  - cognitive_evolver
emits_events:
  - observation_stored
listens_to:
  - reflection_complete
---
# ðŸŒŒ Cosmic Memory Skill (Persistent Wisdom)

This skill provides the AI OS with "Long-term Wisdom" â€” the ability to remember findings, hacks, and architectural decisions across sessions.

## ðŸ› ï¸ Core Functions:
1.  **Observation extraction (/observe):**
    - After every tool execution or task completion, extract a "Lesson Learned".
    - Compress the lesson into a structured fact.
2.  **Cosmic Storage (/remember):**
    - Save extracted lessons to the persistent store (`.agents/memory/cosmic_store.db` or `progress.md`).
    - Use the **RALPH Loop** philosophy: Externalize state so next sessions are primed.
3.  **Wisdom Retrieval (/recall):**
    - On every `SessionStart`, search the store for relevant past findings.
    - Inject "Context Fragments" into the current prompt to avoid repeat mistakes.

## ðŸ“‹ Instructions:
1. Always run `/observe` after a successful complex refactor.
2. Use `/remember --critical` for architectural decisions.
3. Before admitting defeat on a bug, `/recall` past similar failures.

## Principle:
*"Memory is not a log; it is a filter."*

