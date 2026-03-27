# Firecrawl — Web Intelligence Plugin

## Mục đích
Biến bất kỳ website nào thành LLM-ready markdown/JSON.  
Dùng để: crawl documentation, thu thập competitive intel, ingest web data vào RAG.

## Conflict Check — CLEARED ✅
| Plugin | Kết quả | Lý do |
|--------|---------|-------|
| `langextract` | ✅ SAFE | langextract **extract entities từ text**, firecrawl **fetch text từ web** — complementary |
| `scrapling` | ⚠️ PARTIAL | scrapling = fallback khi không có API key |
| `agent-browser` | ✅ SAFE | agent-browser = JS-heavy sites, firecrawl = standard sites |

## Hooks cho Agents

```python
from plugins.firecrawl.firecrawl_adapter import get_firecrawl

fc = get_firecrawl()

# onResearch: lấy nội dung 1 URL
content = fc.scrape_url("https://docs.anthropic.com/claude")

# onCrawlDocs: crawl toàn bộ site
pages = fc.crawl_site("https://docs.example.com", limit=100)

# onExtractData: extract theo schema
data = fc.extract_structured("https://shop.com/product", schema={"name": "str", "price": "float"})

# Batch scrape nhiều URLs
results = fc.batch_scrape(["https://url1.com", "https://url2.com"])

# Map sitemap
urls = fc.map_site("https://example.com")
# Map sitemap
urls = fc.map_site("https://example.com")
```

## Cách dùng CLI (Claude Code Skill)
Đã tích hợp firecrawl CLI thông qua branch `CLAUDE.md`.
Agents (Claude Code, Antigravity) có thể gọi trực tiếp trong terminal:
```bash
firecrawl https://example.com --only-main-content
firecrawl search "query" --limit 5
firecrawl agent "Research topic"
```

```
Firecrawl (fetch) → LangExtract (entities) → LightRAG (index) → MaxKB (serve)
```

```python
# Research pipeline hoàn chỉnh
crawl_result = fc.crawl_site("https://competitor.com", limit=50)
for page in crawl_result:
    lightrag.insert(page)  # vào knowledge graph
```

## Setup

```bash
pip install firecrawl-py
```

Thêm vào `ops/secrets/MASTER.env`:
```
FIRECRAWL_API_KEY=fc-your-key-here
```

Lấy API key: https://firecrawl.dev → Free tier: 500 credits/month

## Noop Mode
Nếu chưa cài `firecrawl-py` hoặc chưa có API key → adapter tự động chạy noop mode (trả về empty, không crash).

## Telemetry
- Hook `onResearch`: log URL được crawl
- Không lưu content trừ khi agent chỉ định `output_dir`

## Version
- **1.0.0** — 2026-03-23, Phase 2 initial integration
