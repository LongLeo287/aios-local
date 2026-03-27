---
name: MaxKB Knowledge Base Platform
tier: 2
source: https://github.com/1Panel-dev/MaxKB
version: latest
status: ingested
ingested: 2026-03-17
security: PASS (manual review - 9 false positives: CJK i18n unicode + standard Vue JWT auth)
---

# MaxKB — Enterprise AI Knowledge Base & RAG Platform

## What It Is
MaxKB ("Max Knowledge Brain") là nền tảng open-source xây dựng AI agents doanh nghiệp với RAG pipeline hoàn chỉnh. 20k+ GitHub stars. Stack: Vue.js + Python/Django + LangChain + PostgreSQL/pgvector.

## Core Capabilities

### RAG Pipeline
- Upload tài liệu / crawl web tự động
- Auto text splitting, vectorization, indexing
- Reduce LLM hallucination, Q&A chất lượng cao

### Agentic Workflow Engine
- Visual workflow builder (drag & drop)
- Function library tích hợp
- **MCP tool-use support** — tương thích AI OS MCP ecosystem
- Orchestration AI phức tạp không cần code

### Model Support (Model-Agnostic)
- Private: DeepSeek, Llama, Qwen (via Ollama)
- Public: OpenAI, Claude, Gemini, AWS Bedrock
- Multi-modal: text, image, audio, video

### Knowledge Base Features
- Multi-type: General / Web / Lark / Workflow KB
- Tag management, batch export
- Embedding + reranker models

## AI OS Integration

### Kết nối với AI OS
- **RAG Agent**: `subagents/rag-specialist/` có thể dùng MaxKB làm backend
- **MCP Bridge**: MaxKB MCP support → tích hợp với `tools/mcp_ecosystem_overview.md`
- **Complement**: NexusRAG (high-perf local) + MaxKB (enterprise UI + multi-user) = bộ đôi RAG
- **Deploy**: Docker-based, tích hợp với `devops-agent`

### Activation (local deploy)
```bash
# Deploy via Docker
docker compose up -d

# Hoặc qua 1Panel app store với Ollama + Llama 3
```

## Use Cases trong AI OS
- Enterprise knowledge search agent
- Internal company Q&A bot với UI đẹp
- Multi-user knowledge base với phân quyền
- Scientific research agent backend (dùng với claude-scientific-skills)

## Security Notes
- 9 CRITICAL → all confirmed FALSE POSITIVES:
  - `localStorage.getItem` = Vue.js JWT session management (standard)
  - Unicode escapes = CJK/Chinese i18n strings in TypeScript
- Không có crypto miner, không có cookie theft thật, không có supply chain attack
