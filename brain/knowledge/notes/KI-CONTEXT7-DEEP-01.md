# KI-CONTEXT7-DEEP-01 — Context7: Real-Time Doc Injection cho LLM
**Loại:** Deep Analysis — MCP Integration
**Nguồn:** github.com/upstash/context7 + context7.com/docs + context7.com/docs/api-guide
**Ngày:** 2026-03-23 | **Verdict:** ✅ APPROVE — Tier 1 candidate
**Priority:** P1 — Implement ngay

---

## 1. Vấn đề context7 giải quyết (WHY — Quan trọng nhất)

| Vấn đề | Mô tả | Tác động trong AI OS |
|--------|-------|---------------------|
| ❌ Outdated training data | LLM biết API của Next.js 12, nhưng đang code với Next.js 15 | Agent viết code sai, debug mất giờ |
| ❌ Hallucinated APIs | Agent "bịa" function không tồn tại | Code crash, mất trust |
| ❌ Generic answers | Không biết version-specific behavior | Sai config, deprecated patterns |

**Context7 giải quyết:** Pull docs real-time từ source → inject vào prompt → Agent có thông tin chính xác, hiện tại.

---

## 2. Cách hoạt động (HOW)

```
User prompt: "Create Next.js middleware with JWT check. use context7"
                                    ↓
              context7 nhận thấy từ khóa "use context7"
                                    ↓
              → resolve-library-id("next.js")     → /vercel/next.js
                                    ↓
              → query-docs("/vercel/next.js", "middleware JWT")
                                    ↓
              → Fetch real-time docs từ nextjs.org/docs
                                    ↓
              → Inject docs vào prompt context
                                    ↓
              Agent viết code đúng cú pháp Next.js 15 ✅
```

---

## 3. Hai mode hoạt động

### Mode A: CLI + Skill (Không cần MCP server)
```bash
npx ctx7 setup --claude   # Claude Code
npx ctx7 setup --cursor   # Cursor / Antigravity
npx ctx7 setup             # Auto-detect
```
- Cài Skill vào agent
- Dùng CLI commands: `ctx7 library <name>` và `ctx7 docs <libraryId>`
- **Phù hợp nhất cho AI OS Corp hiện tại** (không cần MCP server riêng)

### Mode B: MCP Server (Full integration)
- Đăng ký Context7 MCP server trong config
- Agent gọi MCP tools trực tiếp
- **Phù hợp cho Phase 2** khi MCP infrastructure đã ổn định

---

## 4. MCP Tools (API)

| Tool | Tham số | Chức năng |
|------|---------|-----------|
| `resolve-library-id` | `libraryName` (required), `query` (required) | Tìm library ID từ tên |
| `query-docs` | `libraryId` (required), `query` (required) | Lấy documentation snippet |

**Library ID format:** `/owner/repo` — ví dụ:
- `/vercel/next.js` → Next.js docs
- `/supabase/supabase` → Supabase docs  
- `/facebook/react` → React docs
- `/mongodb/docs` → MongoDB docs

---

## 5. REST API v2 (Cho custom integration)

### Endpoint 1: Search Library
```
GET /api/v2/libs/search?libraryName=react&query=hooks
Authorization: Bearer CONTEXT7_API_KEY

Response:
[{
  "id": "/facebook/react",
  "name": "React",
  "totalSnippets": 1250,
  "trustScore": 95,
  "benchmarkScore": 88,
  "versions": ["v18.2.0", "v17.0.2"]
}]
```

### Endpoint 2: Get Context (Documentation)
```
GET /api/v2/context?libraryId=/facebook/react&query=useEffect&type=txt
Authorization: Bearer CONTEXT7_API_KEY

Response:
[{
  "title": "Using the Effect Hook",
  "content": "The Effect Hook lets you perform side effects...",
  "source": "react.dev/reference/react/useEffect"
}]
```

### Python workflow mẫu:
```python
import requests
headers = {"Authorization": "Bearer CONTEXT7_API_KEY"}

# 1. Tìm library ID
libs = requests.get("https://context7.com/api/v2/libs/search",
    headers=headers,
    params={"libraryName": "supabase", "query": "auth email"}).json()
lib_id = libs[0]["id"]  # "/supabase/supabase"

# 2. Lấy docs
docs = requests.get("https://context7.com/api/v2/context",
    headers=headers,
    params={"libraryId": lib_id, "query": "email password sign-up"}).json()
```

---

## 6. Rate Limits & Plans

| Tier | Rate limit | Cách dùng |
|------|-----------|-----------|
| Không có API key | Thấp (anonymous) | Demo/test |
| Free API key | Cao hơn | AI OS daily use |
| Enterprise | Không giới hạn | Production scale |

**Action:** Đăng ký free API key tại **context7.com/dashboard**
→ Set `CONTEXT7_API_KEY` vào `MASTER.env`

---

## 7. Tích hợp vào AI OS — Action Plan

### Bước 1: Cài CLI + Skill (Ngay hôm nay)
```bash
# Cho Antigravity (Cursor-compatible)
npx ctx7 setup --cursor

# Cho Claude Code
npx ctx7 setup --claude
```

### Bước 2: Thêm Rule vào GEMINI.md + CLAUDE.md
```
Always use Context7 when needing library/API documentation, code generation,
or setup steps — without requiring explicit user request.
```
*(Rule tự động kích hoạt, không cần user gõ "use context7" mỗi lần)*

### Bước 3: Đăng ký API key
- Truy cập: context7.com/dashboard
- Copy key vào: `d:\AI OS CORP\AI OS\MASTER.env`
- Biến môi trường: `CONTEXT7_API_KEY=xxx`

### Bước 4: Test validation
```bash
ctx7 library next.js "middleware JWT"
ctx7 docs /vercel/next.js "middleware auth"
```

### Bước 5 (Phase 2): Nâng lên MCP mode
- Thêm Context7 MCP server vào MCP config
- Agents sẽ gọi `resolve-library-id` + `query-docs` natively
- Theo dõi: Dept 4 (Registry) quản lý

---

## 8. Libraries AI OS thường dùng — Nên configure

| Library cần | Context7 ID (ước tính) |
|------------|------------------------|
| Next.js | `/vercel/next.js` |
| Supabase | `/supabase/supabase` |
| Firecrawl | Kiểm tra tại context7.com |
| LangChain | `/langchain-ai/langchain` |
| FastAPI | `/tiangolo/fastapi` |
| React | `/facebook/react` |
| Tailwind CSS | `/tailwindlabs/tailwindcss` |
| Prisma | `/prisma/prisma` |
| Cloudflare Workers | `/cloudflare/workers-sdk` |
| Playwright | `/microsoft/playwright` |

---

## 9. Đánh giá Media (Trust Signals)

| Nguồn | Nhận xét |
|-------|---------|
| Better Stack | *"Free Tool Makes Cursor 10x Smarter"* |
| Cole Medin | *"This is Hands Down the BEST MCP Server for AI Coding Assistants"* |
| AICodeKing | *"Makes CLINE 100X MORE EFFECTIVE!"* |
| Income Stream Surfers | *"Context7 + SequentialThinking MCPs: Is This AGI?"* |

**GitHub stats:** ⭐ 50.2k stars · 🍴 2.4k forks · 55 releases · MIT License
**Backed by:** Upstash (production-grade serverless Redis/Kafka company)

---

## 10. So sánh với AI OS hiện tại

| Capability | AI OS hiện tại | AI OS + Context7 |
|-----------|---------------|-----------------|
| Code generation với Next.js 15 | Dùng training data 2024 | Real-time docs 2026 |
| Supabase auth API | Có thể outdated | Luôn version-specific |
| Firecrawl SDK methods | May hallucinate | Exact API |
| Agent viết migration scripts | Generic | Version-aware |

**Kết luận:** Context7 là layer **chống hallucination API** thiết yếu — đặc biệt quan trọng khi AI OS Corp build products với các library thay đổi nhanh (Next.js, Supabase, Tailwind v4...).

---

## 11. Conflicts & Risks

| Risk | Mức độ | Mitigation |
|------|--------|------------|
| API key rate limit | Thấp | Free plan đủ dùng hàng ngày |
| Community-contributed docs có thể sai | Trung bình | Context7 có trustScore và report system |
| Backend/API/crawler là private | Thấp | Không cần self-host — SaaS |
| Phụ thuộc internet | Thấp | Fallback: agent dùng training knowledge nếu ctx7 down |

**Không có conflict với stack hiện tại** (LightRAG, Firecrawl, Mem0).

---

*KI Note version 1.0 | Phân tích: Antigravity | 2026-03-23*
*Ticket: CIV-2026-03-23-BATCH03 | Approved: Pending CEO*
