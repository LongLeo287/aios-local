---
id: cognitive_reflector
name: Cognitive Reflector
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Post-task reflection engine -- outcome vs plan comparison, lesson extraction.

accessible_by:
  - All agents

dependencies:
  - cosmic_memory
  - insight_engine

exposed_functions:
  - name: reflect_on_task
  - name: extract_lessons
  - name: update_knowledge

consumed_by: []
emits_events:
  - reflection_complete
  - lessons_extracted
listens_to:
  - task_complete
  - task_failed
---

# Cognitive Reflector Agent Skill

## Purpose

Cognitive Reflector is the AI OS "after-action review" engine.
After every task (success or failure), it compares outcome vs original plan,
extracts lessons, and feeds them back into cosmic_memory for long-term recall.

## Exposed Functions

### reflect_on_task
Compares `task_payload` (intent) with `result` (outcome) in blackboard.json.
Generates a structured reflection: what worked, what failed, root causes.

### extract_lessons
Distills the reflection into discrete, reusable lessons.
Format: `{ lesson: "...", applies_to: ["skill_id"], confidence: 0.0-1.0 }`

### update_knowledge
Writes extracted lessons to cosmic_memory so future sessions can recall them.
Uses cross_session_recall to check if a similar lesson already exists (dedup).

## Event Flow

1. Listens: `task_complete` or `task_failed` (from orchestrator_pro)
2. Calls: `reflect_on_task` -> `extract_lessons` -> `update_knowledge`
3. Emits: `reflection_complete` (consumed by cognitive_evolver)
4. Emits: `lessons_extracted` (consumed by cosmic_memory)
