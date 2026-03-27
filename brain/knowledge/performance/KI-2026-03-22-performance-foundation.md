---
id: KI-2026-03-22-performance-foundation
type: REFERENCE
domain: performance
dept: all
created: 2026-03-22
foundation: true
tags: ['performance', 'optimization', 'latency', 'fast-index', 'bottleneck']
---

# AI OS Corp — Performance Targets & Optimization

## AI OS Performance

### Service Response Targets
| Service | Target | Current |
|---------|--------|---------|
| ClawTask API :7474 | < 50ms | ~10-30ms |
| FAST_INDEX lookup | < 5ms | O(1) |
| GitNexus :4747 | < 200ms | ~50-100ms |
| LLM (Ollama local) | < 5s first token | ~1-3s |

### Key Optimizations in Place
- **FAST_INDEX.json** — pre-built path index, O(1) lookup vs filesystem scan
- **ClawTask modules** — lazy-load per route, not on startup
- **GitNexus** — AST cached per session, not per request
- **ag-auto-accept** — stdio wrapper, near-zero overhead on process I/O

### Bottlenecks to Watch
- Cold start: ClawTask imports all modules synchronously on boot
- FAST_INDEX rebuild: full filesystem scan (~30s for 130 plugins)
- GraphRAG: very compute-heavy, use LightRAG for latency-sensitive tasks
- Ollama streaming: first token latency depends on GPU VRAM

### Tools
- `gitingest` — converts repos to LLM-ingestible text (reduce context size)
- `e2b` — isolated sandboxed execution (removes local compute burden)
- `scrapling` — fast headless scraping (anti-fingerprint, proxy-ready)

---
*Foundation KI — created 2026-03-22*
