---
source: https://github.com/HKUDS/LightRAG (local clone: D:\Project\DATA\Archive\eco-ingest\LightRAG)
ingested_at: 2026-03-16T10:34:00+07:00
domain: AI|RAG|KnowledgeGraph|Memory
trust_level: HIGHEST
vet_status: PASS
tags: [lightrag, rag, graph-rag, knowledge-graph, neo4j, python, fastapi, memory, retrieval]
---

# LightRAG — Graph-Based RAG Framework

**Repo:** https://github.com/HKUDS/LightRAG  
**Language:** Python (async/await throughout)  
**Backend:** FastAPI + React 19 WebUI  
**Storage:** 10+ backends (Neo4j, PostgreSQL, MongoDB, Redis, Milvus, Qdrant, Faiss...)

---

## Core Concept

> "RAG với knowledge graph — extract entities + relationships từ documents, build graph, query graph + vector đồng thời."

Thay vì chỉ embed text chunks (naive RAG), LightRAG:
1. Extract **entities** và **relationships** từ documents
2. Build **knowledge graph** từ entities/relations
3. Truy vấn bằng **5 modes** kết hợp graph + vector

---

## 5 Query Modes

| Mode | Description | Use case |
|------|-------------|----------|
| `local` | Focus specific entities | Specific facts |
| `global` | Community/summary-level | Broad overview |
| `hybrid` | Local + Global | General purpose |
| `naive` | Direct vector search only | Simple retrieval |
| `mix` | KG + vector integrated | **Best (với reranker)** |

---

## Architecture

```python
# 4 Storage Types (pluggable backends):
KV_STORAGE      → LLM cache, text chunks, doc info
VECTOR_STORAGE  → Entity/relation/chunk embeddings  
GRAPH_STORAGE   → Entity-relation graph (Neo4j/NetworkX/Memgraph)
DOC_STATUS      → Processing status tracking
```

### Initialization (Critical Pattern)
```python
from lightrag import LightRAG
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed

rag = LightRAG(
    working_dir="./rag_storage",
    llm_model_func=gpt_4o_mini_complete,
    embedding_func=openai_embed,
    workspace="project_name",      # Data isolation per project
)

# REQUIRED — must call before any operations
await rag.initialize_storages()

# Insert
await rag.ainsert("Text content")
await rag.ainsert(["Text 1", "Text 2"])  # Batch

# Query
from lightrag import QueryParam
result = await rag.aquery(
    "Your question",
    param=QueryParam(mode="mix", enable_rerank=True)
)

# Cleanup
await rag.finalize_storages()
```

---

## LLM Support

```python
# 9+ LLM providers:
lightrag/llm/
├── openai.py    (GPT-4, GPT-4o)
├── ollama.py    (Local models)
├── gemini.py    (Google Gemini)
├── anthropic.py (Claude)
├── bedrock.py   (AWS)
├── azure.py
└── ...
```

**Requirements:**
- Minimum 32B parameters recommended
- 32KB context minimum, 64KB recommended
- Avoid reasoning models during indexing phase

---

## API Server

```bash
# Setup
cp env.example .env  # Configure LLM + storage

# Build WebUI  
cd lightrag_webui && bun install --frozen-lockfile && bun run build

# Run
lightrag-server                                    # Production
uvicorn lightrag.api.lightrag_server:app --reload  # Dev
```

REST API + Ollama-compatible API + React WebUI

---

## Production Storage Config

```python
# Production setup (PostgreSQL + Neo4j):
rag = LightRAG(
    working_dir="./storage",
    workspace="production",
    kv_storage="PGKVStorage",
    vector_storage="PGVectorStorage",
    graph_storage="Neo4JStorage",
    doc_status_storage="PGDocStatusStorage",
)
```

---

## Common Gotchas

```
Error: AttributeError __aenter__ hoặc KeyError history_messages
→ Quên gọi await rag.initialize_storages()

Error: Kết quả embed lạ sau switch model
→ Phải clear data directory khi đổi embedding model

Error: Ollama 8k context
→ Thêm llm_model_kwargs={"options": {"num_ctx": 32768}}
```

---

## Relevance cho AI OS

| Feature | AI OS Application |
|---------|-----------------|
| Graph-based memory | Upgrade `.ai-memory/` từ JSON → LightRAG graph |
| Multi-modal retrieval | Query conversation history smarter |
| Document ingestion | Process knowledge/*.md files vào graph |
| Hybrid search | Better than keyword search trong blackboard |
| WebUI | Dashboard cho memory visualization |

### Integration Pattern
```python
# AI OS Memory upgrade:
rag = LightRAG(
    working_dir="D:/Project/AI OS/.ai-memory/lightrag/",
    workspace="ai_os",
    # Local LLM với Ollama:
    llm_model_func=ollama_model_complete,
    embedding_func=ollama_embed,
)
# Ingest tất cả knowledge files → graph
await rag.ainsert([open(f).read() for f in knowledge_files])
# Query
result = await rag.aquery("best pattern for sub-agent", param=QueryParam(mode="mix"))
```

---

## References
- [GitHub](https://github.com/HKUDS/LightRAG)
- [Paper](https://arxiv.org/abs/2410.05779)
- [Docs](https://lightrag.github.io)
