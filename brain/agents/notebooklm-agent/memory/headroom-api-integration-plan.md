# Headroom Context Compression — API Bridge Integration Plan
# Source: awesome-llm-apps KI | Target: API Bridge port 7000 | Nova 2026-03-21

## Background
**Headroom** là LLM optimization tool giảm API costs **50-90%** qua intelligent context compression.
Hỗ trợ MCP, persistent memory, và là drop-in wrapper cho existing API calls.

## Cost Problem
AI OS API Bridge (port 7000) routes tất cả LLM calls. Nếu không compress context:
- Long sessions (như Nova CEO intake) → massive token usage
- Multi-agent workflows → context duplicated qua nhiều agents
- 100 repo ingestion batch → có thể tốn nhiều API budget

## Headroom Architecture

```
                        Before Headroom:
Agent → [Full Context 100k tokens] → LLM API → Cost $$$$

                        After Headroom:
Agent → [Full Context] → Headroom Compressor → [Compressed 10-50k] → LLM API → Cost $
                                              ↓
                                    [Persistent Memory Cache]
                                    [MCP Memory Server]
```

## Integration Points với AI OS

### Option A: Middleware tại API Bridge (Port 7000)
```
                AI OS API Bridge (:7000)
                ┌─────────────────────────┐
Agent calls → │  Route → LLM Router     │
              │  │                       │
              │  ▼                       │
              │  Headroom Compressor     │ ← INSERT HERE
              │  │                       │
              │  ▼                       │
              │  LLM Provider (Ollama/   │
              │  Claude/Gemini/etc.)     │
              └─────────────────────────┘
```

### Option B: Per-Agent Wrapper (Nova-specific)
- Nova wraps calls với Headroom trước khi gửi đến API bridge
- Tiết kiệm cho long-running intake sessions

### Option C: MCP Memory Server (Recommended)
- Headroom expose MCP server → AI OS MCP cluster đọc compressed + cached context
- Agents share compressed context → không ai phải re-send full context

## Implementation Steps

### Step 1: Install Headroom
```bash
# Cài từ awesome-llm-apps pattern
pip install headroom-context
# hoặc check repo: advanced_llm_apps/llm_optimization_tools/headroom_context_optimization/
```

### Step 2: Configure for API Bridge
```python
# Trong D:\Project\AI OS\api-bridge\main.py (hoặc tương đương)
from headroom import HeadroomCompressor

compressor = HeadroomCompressor(
    compression_ratio=0.5,      # Target: 50% compression
    persistent_memory=True,     # Cache across sessions
    mcp_enabled=True,           # Expose via MCP
    mcp_port=7010               # Headroom MCP on port 7010
)

# Wrap LLM calls
def route_to_llm(context, model):
    compressed = compressor.compress(context)
    return llm_router.call(compressed, model)
```

### Step 3: Cost Monitoring
```python
# Log cost savings mỗi request
compressor.log_savings()  
# Output: "Saved 67% tokens | Original: 45k | Compressed: 14.8k"
```

## Projected Savings (AI OS Estimate)

| Use Case | Tokens/Session | Savings 60% | Monthly Est. |
|----------|---------------|-------------|--------------|
| Nova CEO intake | 50k | 30k saved | Significant |
| Multi-agent routing | 20k | 12k saved | Medium |
| Batch 2 repo scan | 200k | 120k saved | High |
| **Total estimate** | ~1M/month | **~600k saved** | **$$$ significant** |

## Action Items
- [ ] Locate Headroom source từ awesome-llm-apps repo
- [ ] Review headroom_context_optimization/ directory
- [ ] Test tại Nova's own API calls trước (safe sandbox)
- [ ] Deploy vào API bridge port 7000 sau khi test
- [ ] Monitor cost dashboard (ClawTask port 7474)

## Liên kết
- Source: `brain/knowledge/repos/awesome-llm-apps/` → `advanced_llm_apps/llm_optimization_tools/headroom_context_optimization/`
- API Bridge config: `D:\Project\AI OS\` (check running process)
- Port 7000 = Universal REST API Bridge (confirmed active)
