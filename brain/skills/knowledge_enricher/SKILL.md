---
id: knowledge_enricher
name: Knowledge Enricher
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Metadata enrichment and contextual cross-linking of knowledge entries.

accessible_by:
  - Researcher

dependencies:
  - web_intelligence
  - neural_memory

exposed_functions:
  - name: metadata_enrichment
  - name: contextual_linking
  - name: backfill_knowledge

consumed_by:
  - archivist
emits_events:
  - knowledge_enriched
listens_to: []
---
# ðŸ§  Knowledge Enricher Skill (Context Hub)

This skill enables the Agent to perform the **ANNOTATE** step of the SFUA loop, ensuring the project's "Second Brain" grows after every task.

## Capabilities:
1. **Insight Extraction:** Identify non-obvious technical constraints, library quirks, or "gotchas" discovered during execution.
2. **Standardization:** Document new patterns in `.agents/knowledge/standards/`.
3. **Memory Persistence:** Create or update entries in `.agents/docs/memory/` to help future Agents avoid repeating mistakes.

## Instructions:
When a task is marked as [x], execute this skill:
1. Review terminal logs and file diffs for any unexpected behavior you had to fix.
2. If you found a specific version requirement or a Chrome API limitation, write a small `.md` file in `.agents/knowledge/api_references/`.
3. Update `.agents/docs/memory/README.md` with a summary of the new knowledge added.

## Protocol:
SEARCH -> FETCH -> USE -> **ANNOTATE (This Skill)**

