---
id: archivist
name: Archivist
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: File organization, log rotation, and knowledge indexing across workspaces.

accessible_by:
  - Orchestrator

dependencies:
  - smart_memory
  - knowledge_enricher

exposed_functions:
  - name: index_workspace
  - name: rotate_logs
  - name: aggregate_docs
  - name: purify_workspace

consumed_by: []
emits_events:
  - workspace_indexed
  - logs_rotated
listens_to:
  - session_end
---

# Archivist Agent Skill

## Purpose

Archivist is the AI OS "librarian" -- it keeps the workspace clean, organized, and fully indexed.
Runs at `session_end` or triggered manually by Orchestrator.

## Exposed Functions

### index_workspace
Scans the target workspace and builds/updates a file index in `shared-context/`.
Output: `{ files_indexed: N, new_files: [], modified: [] }`

### rotate_logs
Compresses and archives log files older than 7 days.
Writes rotated archives to `DATA/Archive/`.

### aggregate_docs
Merges fragmented documentation files into a single coherent document.
Uses smart_memory to detect duplicate content.

### purify_workspace
Removes: temp files, .DS_Store, __pycache__, empty directories.
Always dry-runs first, reports what will be deleted, waits for approval (HITL Tier 2).

## Dependencies

- smart_memory: needed to detect what has changed since last index
- knowledge_enricher: needed to enrich metadata during indexing
