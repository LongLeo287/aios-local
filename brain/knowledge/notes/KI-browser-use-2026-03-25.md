# KI Note — browser-use/browser-use
# Type: REPO | Source: https://github.com/browser-use/browser-use
# CIV Ticket: CIV-2026-03-25-001
# Intake Date: 2026-03-25
# Value Type: TOOL (HIGH) — AI browser automation library

---

## Summary

**browser-use** là Python library cho phép AI agents tự động hóa browser tasks. Hỗ trợ multi-LLM, self-healing web automation, multi-agent orchestration.

---

## Key Facts

| Field | Value |
|-------|-------|
| Repo | `browser-use/browser-use` |
| Stars | 60,000+ |
| Language | Python (≥ 3.11) |
| License | MIT |
| Type | AI Browser Automation Framework |
| LLM Support | Gemini, Claude, GPT-4o, ChatBrowserUse |
| Install | `uv add browser-use` |

---

## Core Capabilities

- **Browser Agent**: Task description → browser agents tự browse, click, fill forms
- **Multi-LLM**: Gemini 3, Claude Sonnet 4, GPT-4o, ChatBrowserUse (cloud)
- **Self-healing**: Tự fix khi element không tìm thấy
- **Multi-agent**: Chạy nhiều browser agent song song
- **Persistent memory**: Browser state persistence qua sessions
- **Custom tools**: Thêm custom Python functions vào agent
- **MCP support**: Tích hợp với MCP servers

---

## Use Cases cho AI OS

| Use Case | Phù hợp |
|----------|---------|
| Web crawler cho CIV pipeline | ⭐⭐⭐ HIGH — thay thế Firecrawl |
| Auto-fill forms / registration | ⭐⭐⭐ HIGH |
| Research automation | ⭐⭐⭐ HIGH |
| Competitor monitoring | ⭐⭐ MED |
| E-commerce crawling | ⭐⭐ MED |

---

## Integration với AI OS

```python
# Potential: web-crawler agent dùng browser-use
from browser_use import Agent, Browser
from browser_use import ChatGoogle  # gemini-3-flash

async def civ_web_crawler(url: str) -> str:
    agent = Agent(
        task=f"Extract main content, key points, and metadata from {url}",
        llm=ChatGoogle(model="gemini-3-flash"),
    )
    result = await agent.run()
    return result
```

---

## CIV Assessment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Relevance to AI OS | 9/10 | Web-crawler + research automator |
| Security risk | LOW | MIT license, well-maintained |
| Integration effort | MED | Python async, uv install |
| Value type | SKILL + PLUGIN | |

**Verdict:** ✅ APPROVE — Integrate as `web-crawler` agent backend, replace/supplement Firecrawl

---

## Action Items

- [ ] Add `browser-use` to `kho/plugins/registry.json`
- [ ] Create `plugins/browser-use/` directory + skill wrapper
- [ ] Wire to `web-crawler` agent in CIV pipeline
- [ ] Add to `ops/scripts/install_vscode_extensions.ps1` if needed

---

*KI Note v1.0 | CIV-2026-03-25-001 | Intake: Antigravity | 2026-03-25*
