---
description: Nova — CEO Standing Order Intake Workflow. Xử lý bất kỳ input nào CEO đưa vào (repo/web/PDF/video/note) và lưu vào kho kiến thức AI OS.
dept: Dept 22 (AI OS Data & Knowledge Upgrade) / Dept 13 (R&D)
agent: Nova (notebooklm-agent)
version: "1.0"
updated: "2026-03-21"
---

# Nova — CEO Standing Order Intake Workflow

Workflow này kích hoạt khi CEO cung cấp bất kỳ link/file/nội dung nào.

## STEP 0 — Nhận input từ CEO
- Đọc `memory/hot-cache.md` → check Pending CEO Inputs
- Xác định loại input (không hỏi CEO):
  - GitHub URL → **REPO**
  - `notebooklm.google.com` URL → **CLOUD NLM NOTEBOOK**
  - Tên miền thông thường (blog, docs, web) → **WEB**
  - Đuôi `.pdf` hoặc path local → **PDF**
  - YouTube / video URL → **VIDEO**
  - DOI / arxiv / pubmed URL → **PAPER**
  - Text thuần / note → **NOTE**

## STEP 1 — Route theo Intake Routing Matrix

| Input Type | Tool (Primary) | Tool (Fallback) | Output |
|------------|----------------|-----------------|--------|
| REPO       | gitingest digest → open-notebook | gitingest URL paste | `repos/YYYY-MM-DD_[name].md` |
| WEB        | firecrawl → open-notebook | read_url_content → open-notebook | `web/YYYY-MM-DD_[topic].md` |
| PDF        | open-notebook upload | pdfplumber → paste text | `docs/YYYY-MM-DD_[name].md` |
| VIDEO      | yt-dlp transcript → open-notebook | YouTube summary API | `media/YYYY-MM-DD_[title].md` |
| PAPER      | open-notebook | notebooklm-skill | `research/YYYY-MM-DD_[topic].md` |
| NOTE       | direct → open-notebook | none | `notes/YYYY-MM-DD_[topic].md` |
| CLOUD NLM  | notebooklm-skill | browser → manual | `web/YYYY-MM-DD_nlm_[title].md` |

## STEP 2 — Ingest vào open-notebook (LOCAL)

Endpoint: `http://localhost:5055`

```bash
# Upload URL
curl -X POST http://localhost:5055/api/sources \
  -H "Content-Type: application/json" \
  -d '{"url": "[URL]", "notebook_id": "[id]"}'

# Upload text
curl -X POST http://localhost:5055/api/sources \
  -H "Content-Type: application/json" \
  -d '{"text": "[content]", "title": "[title]", "notebook_id": "[id]"}'

# Hỏi notebook
curl -X POST http://localhost:5055/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "[question]", "notebook_id": "[id]"}'
```

## STEP 3 — Phân tích & Synthesis

Câu hỏi tiêu chuẩn cho mỗi loại input:
```
REPO:  "What does this repo do? Key architecture, tech stack, novelty?"
WEB:   "Key insights, claims, actionable points? For AI OS context?"  
PDF:   "Main findings, frameworks, applicable methods?"
VIDEO: "Core concepts, timestamps of key points, actionable insights?"
PAPER: "Research question, methodology, results, AI OS application?"
NOTE:  "Context, key points, action items, dept relevance?"
```

## STEP 4 — Tạo KI Artifact (bắt buộc)

Format tên file: `brain/knowledge/[type]/YYYY-MM-DD_[topic]_[dept].md`

Template synthesis artifact:
```markdown
# [Title] — Nova Synthesis
Source: [URL / path]
Date: YYYY-MM-DD | Dept: [dept] | Priority: HIGH (CEO Input)

## TL;DR (5 dòng)
[Quick summary]

## Key Insights
1. [Insight 1]
2. [Insight 2]

## AI OS Application
- Dept [n]: [Specific action recommendation]

## Raw Q&A Log
### Q: [question]
A: [answer]
```

## STEP 5 — Route kết quả đến phòng ban

- Viết request vào `memory/dept-requests/dept[nn]-[name].md`
- Format: `| YYYY-MM-DD | [request] | HIGH | ⏳ Pending |`

## STEP 6 — Lưu vào synthesis-log

```markdown
## [YYYY-MM-DD HH:MM] Session: [topic]
- Source: CEO — LongLeo (Standing Order)
- Input: [type] — [URL/description]
- Plugin used: [tool]
- Output: [artifact path]
- Dept routes: [list]
- Archived: ✅
```

## STEP 7 — Brief CEO

Format báo cáo ngắn:
```
✅ Đã intake: [title]
📁 Archived: brain/knowledge/[path]
🔗 Key insight: [1-2 dòng TL;DR]
🏢 Dept routes: Dept [n] — [action]
```

---

## Quy tắc triển khai

1. **LOCAL FIRST** — open-notebook trước, cloud sau
2. **NO SKIP ARCHIVE** — Mọi input đều phải có KI artifact
3. **CEO IMMEDIATE** — Không delay, không hỏi thêm
4. **2-FAILURE ESCALATE** — Tool fail 2 lần → ghi BLOCKED vào log

---

*Nova Intake Workflow v1.0 | Dept 22 + Dept 13 | 2026-03-21*
