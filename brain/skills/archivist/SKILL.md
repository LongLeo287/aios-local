---
id: archivist
name: Archivist
display_name: Archivist — Workspace Organization & Knowledge Indexing
description: >-
  Keeps the workspace clean and searchable. Auto-sorts logs, archives tasks,
  indexes knowledge, and runs recursive knowledge sync after every task.
version: 1.0.0
tier: 2
category: memory
domain: core
tags: [archiving, knowledge, indexing, cleanup, memory]
cost_tier: economy
accessible_by:
  - Antigravity
  - Claude Code
dependencies:
  - context_manager
exposed_functions:
  - /organize
  - /migrate
  - /aggregate
  - /index
  - /knowledge-sync
load_on_boot: false
status: active
---

This skill provides the AI OS with "Organizational Instincts" — keeping the workspace clean and searchable by automatically sorting logs, archiving tasks, and indexing knowledge.

## 🛠️ Core Functions

1. **Auto-Sorting (/organize):**
   - Identify old `.log`, `.tmp`, or duplicated `.md` files.
   - Move old sprint plans, brainstorming sessions, and completed tasks to `archive/`.
   - Categorize markdown files by topic (plans, brainstorms, media).
2. **Cross-Session Preservation (/migrate):**
   - Automatically ingest data from previous AI OS brains (e.g., Gemini/Claude cache folders) into the central project `archive/`.
   - Filter out `.resolved` and `.metadata` system cache files during migration.
3. **File Aggregation & Cleanup (/aggregate):**
   - Regularly monitor the project for scattered `.md`, `.log`, and task reporting files.
   - Analyze and compile these scattered documents into a single master summary document (e.g., a Phase Summary).
   - Delete the old, individual files to reduce file count and maintain architectural cleanliness.
4. **Knowledge Indexing (/index):**
   - Update the `project_map.md` or a central index to make search easier.
   - Link new library files to the Governance Anchor.

5. **Recursive Knowledge Update (/knowledge-sync):**
   - **Trigger:** Automatically runs at the end of every completed task (post-`[REFLECTION]` mode).
   - **Process:**
     1. Scan `memory/daily/` for new facts extracted during the task.
     2. Classify facts by domain: `architecture`, `api`, `ui`, `governance`, `lessons`.
     3. Merge validated facts into the corresponding file in `knowledge/` (create if absent).
     4. Deduplicate — if a fact already exists in `knowledge/`, skip or update timestamp.
     5. Update `knowledge_index.md` with new entries and cross-references.
   - **Output:** Updated `knowledge/` files and refreshed `knowledge_index.md`.
   - **Validation:** Each merged fact must include source task reference and extraction date.
   - **Purpose:** Ensures the knowledge base is self-improving — every task makes the system smarter.

## 📋 Instructions

- Run `/organize` at the end of every major Phase or when the `.agents/tasks/` directory exceeds 10 files.
- Run `/knowledge-sync` automatically after every task completion to keep `knowledge/` current.

## Principle
*"A clean system is a predictable system. A learning system is an unstoppable one."*
