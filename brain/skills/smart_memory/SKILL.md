---
id: smart_memory
name: Smart Memory
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: ASM-style fact extraction and selective recall across sessions.

accessible_by:
  - Orchestrator
  - Claude Code

dependencies:
  - context_manager

exposed_functions:
  - name: extract_facts
  - name: recall_selective
  - name: consolidate_memory

consumed_by:
  - orchestrator_pro
  - archivist
  - cosmic_memory
emits_events:
  - facts_extracted
listens_to:
  - task_complete
---
# ðŸ§  Smart Memory Skill (ASM Implementation)

## Description
This skill implements the **Smart Memory Layer**, focusing on high-density fact extraction, long-term consolidation, and low-latency recall of project-specific information.

## ðŸ› ï¸ Core Functions:
1.  **Fact Extraction (/extract-fact):** Identify "immutable truths" in the conversation and save them to `.agents/memory/daily/`.
    - *Format:* `FACT: [Topic] - [Description] - [Context/File]`
2.  **Selective Recall (/recall):** Search `memory/` for keywords related to the current task. **ONLY** fetch the matching files.
3.  **Consolidation (/consolidate):** Clean up the `daily/` folder by merging related facts and moving them to `long-term/`.

## ðŸ“‹ Instructions:
Before ending a session:
1. Scan your terminal logs and edits.
2. Ask: "What did I learn that is universal to this project, not just this task?"
3. Save these as individual small files (leaf nodes) in `memory/daily/` with descriptive names (e.g., `chrome_tabs_api_quirk.md`).

## Protocol:
*"Store Facts, not Noise. Recall relevance, not History."*

