# KI-TOKEN-REDUCTION-01 — Token Reduction Strategies (code-review-graph + agents-course)
**Nguồn:** tirth8205/code-review-graph + huggingface/agents-course
**Ngày:** 2026-03-23 | **Verdict:** REFERENCE — áp dụng ngay vào AI OS

---

## 1. Code Review Graph — 6.8× Token Reduction

### Vấn đề
Code review thông thường: dump toàn bộ file vào context → tốn nhiều tokens.

### Giải pháp: Local Knowledge Graph
```python
# Thay vì: load full codebase vào context
# → Build dependency graph trước, chỉ load relevant nodes

from code_review_graph import CodeGraph

graph = CodeGraph("./src")
graph.build()  # One-time indexing

# Khi review 1 file:
relevant_files = graph.get_related("auth.py", depth=2)
# Returns: auth.py + trực tiếp imports + direct callers ONLY
# NOT: toàn bộ 500 files
```

**6.8× reduction:** 50,000 tokens → ~7,400 tokens cho cùng review quality.

### Apply trong AI OS
- `Understand-Anything` skill đã cover use case này
- Pattern: mọi codebase analysis task → build graph trước → query graph
- Tools: `ctx7` cho library docs + knowledge graph cho local code

---

## 2. HuggingFace Agents Course — Key Patterns

### Tool Use Pattern (smolagents)
```python
from smolagents import tool, CodeAgent

@tool
def search_web(query: str) -> str:
    """Search the web for current information"""
    return firecrawl.search(query)

@tool
def query_knowledge_base(question: str) -> str:
    """Query AI OS knowledge base"""
    return lightrag.query(question)

agent = CodeAgent(
    tools=[search_web, query_knowledge_base],
    model=claude_model
)
```
**AI OS pattern:** Wrap Firecrawl + LightRAG + Mem0 như @tools → inject vào agent.

### Memory Patterns (3 types)
```
1. In-context memory   → Conversation history (ephemeral)
2. External memory     → Vector DB (Mem0, LightRAG) — persistent
3. Episodic memory     → Past task outcomes → decisions_log.md
```
**AI OS status:**
- ✅ In-context: implemented
- ✅ External: Mem0 + LightRAG active
- ⚠️ Episodic: `decisions_log.md` exists but not systematically linked

### Multi-Agent Pattern (LangGraph style)
```python
# Orchestrator routes to specialists
def route_task(task):
    if "code" in task:      return coding_agent
    if "search" in task:    return research_agent
    if "finance" in task:   return finance_agent
    return general_agent
```
**AI OS:** Dept routing trong Corp Cycle đã implement này.

### ReAct Pattern (Reason + Act)
```
THOUGHT: Tôi cần tìm security vulnerabilities trong repo này
ACTION: trivy_scan(repo_url)
OBSERVATION: Found 2 HIGH CVEs in lodash 4.17.x
THOUGHT: CVEs có fix không?
ACTION: ctx7_docs("/npm/lodash", "CVE fix version")
OBSERVATION: Fixed in lodash 4.17.21
FINAL: Upgrade lodash to 4.17.21
```
**AI OS ứng dụng:** GEMINI.md đã có "Read first, Act second, Report always" — đây là ReAct pattern chính xác.

---

## Actionable Takeaways

| Insight | Apply Where | Priority |
|---------|------------|---------|
| Knowledge graph trước khi analyze codebase | Understand-Anything skill | P1 (already doing) |
| @tool decorator pattern cho Tier 1 services | Firecrawl/LightRAG wrappers | P1 (already done) |
| Episodic memory → decisions_log link | post-session workflow | P2 |
| Token budgeting 6.8× reduction | All code analysis tasks | P2 |

*KI Note v1.0 | 2026-03-23*
*Source: tirth8205/code-review-graph + huggingface/agents-course*
