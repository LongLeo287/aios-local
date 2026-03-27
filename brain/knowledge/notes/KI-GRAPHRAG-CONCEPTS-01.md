# Knowledge Note: GraphRAG — Community Detection for AI OS Knowledge Graph
# Source: plugins/graphrag (MIT License) — Microsoft Research
# Extracted: 2026-03-23 | By: Antigravity (Knowledge Extraction Pass)
# Status: REFERENCE ONLY — LightRAG covers use case locally. Extract concepts only.

---

## What GraphRAG Does Uniquely vs LightRAG

| Feature | LightRAG (AI OS Tier 1) | GraphRAG (Microsoft) |
|---------|------------------------|---------------------|
| Setup | Local, Ollama | Cloud LLM (expensive) |
| Query modes | naive/local/global/hybrid | local/global |
| Community detection | ❌ Not built-in | ✅ Leiden algorithm |
| Global summarization | Basic global query | Map-reduce over communities |
| Cost | Free (local) | High (LLM API calls per chunk) |
| Speed | Fast | Slow (indexing expensive) |

**Conclusion:** Do NOT replace LightRAG. But learn from GraphRAG's **Community Detection** concept.

---

## Key Concept: Community Detection (Worth Implementing in AI OS)

GraphRAG uses **Leiden Algorithm** to group knowledge graph entities into "communities" — 
thematic clusters that enable better global reasoning (e.g., "What are the major themes in AI OS knowledge?").

**AI OS Application:**
LightRAG's graph index builds entity relationships but does NOT automatically cluster them.
To improve global reasoning, consider adding a post-processing step after `index_brain_knowledge()`:
- Group entities by relationship density (manual community tagging)
- Create `brain/knowledge/communities/` folder with thematic summaries
- Example communities: "Agent Architecture", "Security Policies", "Plugin Ecosystem", "Corp Operations"

**Simple implementation (no GraphRAG required):**
```
After knowledge ingest:
1. Identify top entities from LightRAG graph
2. Tag them into communities manually (or via LLM pass)
3. Write community summary files to brain/knowledge/communities/<community>.md
4. Agents query communities first for global questions, then LightRAG for specific questions
```

---

## Prompt Tuning Insight (from GraphRAG docs)

GraphRAG emphasizes **prompt tuning** for better entity extraction. Apply to AI OS:
- When ingesting documents, the extraction prompt should specify entity types relevant to AI OS
  (Agent, Department, Workflow, Rule, Plugin, Decision, etc.)
- Current LightRAG ingestion uses generic extraction — add entity type hints to improve graph quality

**Recommended entity types for AI OS corpus:**
```python
entity_types = ["agent", "department", "workflow", "rule", "plugin", "decision", "skill", "tool", "service"]
```

---

*GraphRAG tool itself is NOT integrated — too expensive, cloud-dependent.*
*Apply the CONCEPTUAL PATTERNS: community detection + entity-typed extraction.*
