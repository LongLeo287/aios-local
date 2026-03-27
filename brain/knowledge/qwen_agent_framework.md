---
source: https://github.com/QwenLM/Qwen-Agent (local clone: D:\Project\DATA\Archive\eco-ingest\Qwen-Agent)
ingested_at: 2026-03-16T10:34:00+07:00
domain: AI|AgentFramework|LLM|Alibaba
trust_level: HIGHEST
vet_status: PASS
tags: [qwen-agent, alibaba, llm-framework, mcp, rag, code-interpreter, browser-agent, qwen3]
---

# Qwen-Agent — Alibaba's AI Agent Framework

**Repo:** https://github.com/QwenLM/Qwen-Agent  
**By:** Alibaba / QwenLM team  
**Backbone:** Qwen models (Qwen3, QwQ-32B, Qwen3.5, Qwen3-Coder)  
**Latest:** Qwen3.5 open-sourced Feb 16, 2026

---

## Tổng quan

Framework phát triển LLM applications với capabilities:
- **Instruction following**
- **Tool usage** (Function Calling, MCP)
- **Planning** (multi-step reasoning)  
- **Memory** (RAG, long-context)

**Production use:** Backend của [Qwen Chat](https://chat.qwen.ai/)

---

## Installation

```bash
pip install -U "qwen-agent[gui,rag,code_interpreter,mcp]"
# Modules:
# [gui]              → Gradio WebUI
# [rag]              → RAG support
# [code_interpreter] → Docker sandbox code execution
# [mcp]              → MCP protocol support
```

---

## Core Example

```python
from qwen_agent.agents import Assistant
from qwen_agent.tools.base import BaseTool, register_tool

# 1. Custom Tool
@register_tool('my_tool')
class MyTool(BaseTool):
    description = 'Tool description for LLM'
    parameters = [{'name': 'input', 'type': 'string', 'required': True}]
    
    def call(self, params: str, **kwargs) -> str:
        # Tool implementation
        return result

# 2. Configure LLM
llm_cfg = {
    'model': 'qwen3-32b',
    'model_type': 'qwen_dashscope',  # or OpenAI-compatible
    # For vLLM/Ollama:
    # 'model_server': 'http://localhost:8000/v1',
    # 'api_key': 'EMPTY',
}

# 3. Create Agent
bot = Assistant(
    llm=llm_cfg,
    system_message="...",
    function_list=['my_tool', 'code_interpreter'],
    files=['./doc.pdf']  # Files agent can read
)

# 4. Run (streaming)
messages = []
for response in bot.run(messages=messages):
    print(response)

# 5. Gradio WebUI (one line)
from qwen_agent.gui import WebUI
WebUI(bot).run()
```

---

## Key Features

### MCP Support
```python
# MCP config format (same as Claude Desktop):
mcp_config = {
    "mcpServers": {
        "memory": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-memory"]},
        "filesystem": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]},
        "sqlite": {"command": "uvx", "args": ["mcp-server-sqlite", "--db-path", "test.db"]}
    }
}
```

### Code Interpreter (Docker Sandboxed)
```python
tools = ['code_interpreter']  # Run code in Docker container
bot = Assistant(llm=llm_cfg, function_list=tools)
# Agent can write + execute Python safely in isolation
```

### RAG for Super-Long Documents (1M tokens)
```python
# Fast RAG solution for 1M token documents
from examples import assistant_rag
# Parallel document QA that outperforms native long-context models
```

### Parallel Function Calls
```python
# Qwen-Agent supports native parallel tool calling
# Default template: nous (recommended for Qwen3)
'generate_cfg': {'fncall_prompt_type': 'nous'}
```

### Browser Assistant (BrowserQwen)
```bash
# browser_qwen/ — Browser automation agent
# Reads web pages, interacts with content
```

---

## Model Compatibility

| Model | Special Notes |
|-------|--------------|
| Qwen3 / Qwen3.5 | Main models, parallel tool calls |
| QwQ-32B | Reasoning model, multi-step tool calls |
| Qwen3-Coder | Use vLLM + `use_raw_api=True` |
| Qwen3-VL | Multimodal: vision tools (zoom, search) |
| Any OpenAI-compatible | Works via `model_server` config |

---

## Comparison với Alternatives

| Framework | Backend LLM | MCP | RAG | Code Exec | GUI |
|-----------|-------------|-----|-----|-----------|-----|
| **Qwen-Agent** | Qwen (any OpenAI compat) | ✅ | ✅ | ✅ Docker | ✅ Gradio |
| LangChain | Any | ❌ native | ✅ | ✅ | ❌ |
| LlamaIndex | Any | ❌ | ✅ | ❌ | ❌ |
| Composio | Any | ✅ | ❌ | ❌ | ❌ |

---

## Relevance cho AI OS

| Feature | AI OS Application |
|---------|-----------------|
| Tool registration pattern | Tham khảo cho skill implementation |
| MCP config (same format) | AI OS đã dùng format này ✅ |
| Docker code interpreter | Isolated code execution cho agents |
| Browser agent | Alternative cho playwright-mcp |
| Qwen local via Ollama | Free local LLM alternative to Claude |

### Local Qwen via Ollama (free alternative)
```python
llm_cfg = {
    'model': 'qwen3:32b',
    'model_server': 'http://localhost:11434/v1',  # Ollama
    'api_key': 'EMPTY',
    'generate_cfg': {'options': {'num_ctx': 32768}}  # 32k context
}
```

---

## References
- [GitHub](https://github.com/QwenLM/Qwen-Agent)
- [Docs](https://qwenlm.github.io/Qwen-Agent/en/)
- [DeepPlanning Benchmark](https://qwenlm.github.io/Qwen-Agent/en/benchmarks/deepplanning/)
- [Qwen Chat](https://chat.qwen.ai)
