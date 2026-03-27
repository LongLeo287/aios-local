---
id: neural_memory
name: Neural Memory
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Associative neural-network style recall and knowledge graph synthesis.

accessible_by:
  - Researcher
  - Developer

dependencies:
  - context_manager

exposed_functions:
  - name: associative_recall
  - name: graph_synthesis
  - name: semantic_link

consumed_by:
  - insight_engine
  - knowledge_enricher
emits_events:
  - graph_updated
listens_to: []
---
# ðŸ§  Neural Memory Skill (Associative Intelligence)

This skill adds "Synapses" to the AI OS Memory, allowing Agents to associate related concepts dynamically.

## ðŸ› ï¸ Core Functions:
1.  **Link Generation (/link):** Create an entry in `.agents/memory/neural_links/map.json` connecting two facts.
2.  **Thought Propagation (/crawl):** When a fact is recalled, automatically fetch all linked facts within 1 degree of separation.
3.  **Pattern Recognition:** Identify repeating issues across diverse files and create a "Neural Pattern" document.

## ðŸ“‹ Instructions:
During the **ANNOTATE** phase:
1. Don't just save the fact. Ask: "What else does this remind me of in this project?"
2. Create or update the neural map to link this new insight to relevant architecture docs or previous bugs.

## Principle:
*"Intelligence is the density of connections, not just the volume of data."*

