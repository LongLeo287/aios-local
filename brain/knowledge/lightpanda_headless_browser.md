---
source: https://github.com/lightpanda-io/browser
ingested_at: 2026-03-16T10:23:00+07:00
domain: AI|Browser|WebAutomation|Performance
trust_level: HIGH
vet_status: PASS
tags: [headless-browser, zig, playwright, puppeteer, cdp, ai-agents, web-scraping, performance]
---

# Lightpanda — Headless Browser for AI Agents

**Repo:** https://github.com/lightpanda-io/browser  
**Language:** Zig + V8 JavaScript Engine  
**Stage:** Alpha (work in progress, nhưng functional)  
**Focus:** AI agents, LLM training, web scraping at scale

---

## Tổng quan

Lightpanda = headless browser **built from scratch** với mục tiêu:
> "Không cần Chrome overhead để browse web programmatically"

Chrome headless vẫn load toàn bộ rendering pipeline (GPU, fonts, layout...) ngay cả khi không có UI. Lightpanda bỏ phần đó hoàn toàn.

---

## Performance Benchmarks

| Metric | Chrome | Lightpanda | Ratio |
|--------|--------|------------|-------|
| Memory | 100% | ~9-12% | **9-12x less** |
| Startup time | 100% | ~1.5% | **64x faster** |
| Execution speed | 100% | ~9% | **11x faster** |

**Instant startup** = không phải đợi Chrome khởi động mỗi request.

---

## Tech Stack

```
┌─────────────────────────────────────────┐
│  Lightpanda                             │
│                                         │
│  ┌──────────────┐  ┌──────────────────┐ │
│  │ Zig runtime  │  │  V8 JS Engine    │ │
│  │ (memory safe)│  │ (Google's V8)    │ │
│  └──────────────┘  └──────────────────┘ │
│                                         │
│  ┌──────────────────────────────────┐   │
│  │  Chrome DevTools Protocol (CDP)  │   │
│  │  (compatibility layer)           │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
         ↕ CDP Protocol
┌────────────┐ ┌────────────┐ ┌──────────┐
│ Playwright │ │ Puppeteer  │ │ chromedp │
└────────────┘ └────────────┘ └──────────┘
```

**Zig được chọn vì:**
- Performance gần C nhưng memory safe hơn
- Seamless integration với C libraries (V8 là C++)
- Low-level control không có GC overhead

---

## Web API Support

- ✅ JavaScript execution (V8)
- ✅ DOM manipulation
- ✅ Partial Web APIs (growing)
- ✅ Fetch/XHR (network requests)
- ⏳ Full CSS layout (partial, improving)
- ❌ GPU rendering (intentionally excluded)

---

## Compatibility

Dùng **Chrome DevTools Protocol (CDP)** → drop-in replacement trong nhiều cases:

```python
# Playwright — thay Chrome bằng Lightpanda
browser = await playwright.chromium.connect_over_cdp(
    "http://localhost:9222"  # Lightpanda CDP endpoint
)

# Puppeteer
browser = await puppeteer.connect({
    browserWSEndpoint: 'ws://localhost:9222'
})
```

---

## Use Cases Tối Ưu

### 1. AI Agent Web Browsing
```
AI Agent cần browse web → Lightpanda thay Chrome
→ 10x ít RAM → chạy nhiều agents song song hơn
→ Startup instant → agent responsive hơn
```

### 2. LLM Training Data Collection
```
Scrape 1M pages với Chrome: RAM ~200GB, Time ~100h
Scrape 1M pages với Lightpanda: RAM ~20GB, Time ~9h
```

### 3. Web Testing at Scale
```
CI/CD pipeline: 1000 browser tests
Chrome: cần nhiều máy, chậm
Lightpanda: chạy trên 1 máy, nhanh hơn nhiều
```

### 4. MCP Browser Automation
```
MCP server dùng Lightpanda thay Chrome:
→ playwright-mcp hoặc puppeteer-mcp chạy trên Lightpanda
→ AI OS có browser capability nhẹ hơn nhiều
```

---

## Limitations (Alpha Stage)

- ❌ Web APIs chưa đầy đủ (CSS layout partial)
- ❌ Không render visual (intentional)
- ❌ Một số complex JS frameworks có thể gặp issues
- ❌ Chưa có binary release ổn định (phải build từ source)
- ⚠️ Alpha = có thể breaking changes

---

## Build & Run

```bash
# Requirements: Zig + V8
git clone https://github.com/lightpanda-io/browser
cd browser

# Build
zig build

# Run CDP server (default port 9222)
./lightpanda --host 127.0.0.1 --port 9222
```

---

## Relevance cho AI OS

| Aspect | Application |
|--------|-------------|
| Browser tool offline | Lightpanda thay Chrome khi browser tool lỗi |
| MCP server | Playwright MCP chạy trên Lightpanda (lighter) |
| Web scraping | Fetch URL + JS execution không cần Chrome |
| Agent browsing | Nhiều spawn-agent có thể browse song song |

### Tích hợp với spawn-agent
```
spawn-agent → worker dùng Lightpanda thay Chrome
→ Worker pool 10x hiệu quả hơn về memory
→ Nhiều concurrent browser workers hơn
```

### Tích hợp với MCP fetch server
```
Hiện tại: server-fetch (HTML only, no JS)
Upgrade: Lightpanda + playwright-mcp → full JS execution
→ Khi nào Lightpanda stable hơn
```

---

## So sánh Alternatives

| Tool | Language | JS | Memory | CDP Compat | AI-focused |
|------|----------|----|---------|-----------|-----------| 
| Chrome headless | C++ | ✅ Full | Heavy | ✅ Native | ❌ |
| Firefox headless | C++ | ✅ Full | Heavy | ❌ | ❌ |
| **Lightpanda** | **Zig** | **✅ V8** | **🔥 9x less** | **✅** | **✅** |
| jsdom | JS/Node | ❌ | Light | ❌ | ❌ |
| playwright-firefox | C++ | ✅ | Medium | ❌ | ❌ |

---

## Roadmap (Known)
- Full Web API compliance
- Stable binary releases
- Better CSS layout support
- Performance improvements (already fast)
- Official Playwright integration

---

## References
- [GitHub](https://github.com/lightpanda-io/browser)
- [HN Discussion](https://news.ycombinator.com)
- [daily.dev article](https://daily.dev)
- [Official site](https://lightpanda.io)
