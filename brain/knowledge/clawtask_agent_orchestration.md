# Knowledge File: ClawTask — AI Agent Task Orchestration Platform
# Source: https://vnrom.net/2026/03/clawtask-nen-tang-dieu-phoi-cong-viec-cho-ai-agents-khong-chi-la-mot-kanban-board/
# Ingested: 2026-03-19 | Tier: T1 (Internal — AI OS Corp uses ClawTask)
# Author: Duy Nghiện (vnROM)

---

## SUMMARY

ClawTask là nền tảng **điều phối công việc cho AI agents** — không phải Kanban thông thường. Được thiết kế cho mô hình **human + AI agent collaboration**, nơi agent có trạng thái, workflow có checkpoint, và con người có thể can thiệp đúng lúc.

**AI OS Corp đang dùng ClawTask tại:** `d:\Project\AI OS\tools\clawtask\`
**Server:** `clawtask_api.py` — chạy cổng 7474

---

## TẠI SAO CLAWTASK KHÁC BIỆT

Tools quản lý task truyền thống (Trello, Notion, Jira) được thiết kế cho **con người**. ClawTask được thiết kế cho **human + AI agent collaboration**.

| Vấn đề với tools cũ | Giải pháp ClawTask |
|--------------------|-------------------|
| Agent không có cơ chế nhận việc chuẩn | API/MCP layer cho agent đăng ký + nhận task |
| Không có luồng dừng để hỏi con người | **Clarification Flow** — workflow pause chính xác |
| Không có chỗ lưu output trung gian | **Notebook layer** per task |
| Không track task bị blocked thực sự | Task states: todo/inprogress/blocked/review/done |
| Thiếu recurring workflows | **Recurring task definitions** |

---

## 5 TÍNH NĂNG CORE

### 1. Task Lifecycle Management
Agent là worker có trạng thái, không chỉ là chatbot:
```
todo → inprogress → [blocked/review] → done
                 ↕
          awaiting_clarification  (NEW — cần implement)
```

### 2. Clarification Flow ⭐ (Tính năng quan trọng nhất)
Khi agent thiếu thông tin → tạo clarification tied to task → workflow PAUSE → human respond → agent tiếp tục.

Thay vì: đoán bừa / fail im lặng / output sai.

```
Agent hits blocker
  → POST /api/tasks/:id/clarification
  → {"question": "...", "context": "...", "blocking": true}
  → Dashboard hiện thị badge 🔴 NEEDS CLARIFICATION
  → Human responds via dashboard
  → Agent polls GET /api/tasks/:id/clarifications
  → Agent continues with answer
```

### 3. Notebook Layer
Lưu output trung gian: research notes, reasoning chains, audit checklists, analysis logs.

```
POST /api/tasks/:id/note
  → {"content": "...", "type": "reasoning|research|checkpoint"}
```

### 4. Recurring Tasks
Auto-generate tasks theo lịch: daily briefs, server checks, SLA reviews, weekly reports.

### 5. MCP + REST Endpoints
```
POST /mcp/*              — MCP protocol
/api/mcp hoặc /mcp/rpc  — streamable RPC
REST API chuẩn          — bất kỳ agent nào HTTP được đều dùng được
```

---

## AI OS CORP — TRẠNG THÁI TÍCH HỢP

| Tính năng | Status | File |
|-----------|--------|------|
| Basic task CRUD | ✅ Implemented | clawtask_api.py |
| Agent briefing | ✅ Implemented | /api/agent-briefing/:id |
| GitNexus proxy | ✅ Implemented | /api/gitnexus/* |
| Change alerts | ✅ Implemented | /api/intel/change-alert |
| Clarification flow | 🔶 ADDED 2026-03-19 | clawtask_api.py |
| Notebook layer | 🔶 ADDED 2026-03-19 | clawtask_api.py |
| Recurring tasks | ⬜ Planned | — |
| MCP protocol | ⬜ Planned | — |

---

## THIẾT KẾ CLARIFICATION FLOW (AI OS Corp)

```
Mapping department → clarification targets:
- engineering tasks     → CTO
- finance tasks         → CFO
- client tasks          → COO → CEO
- security tasks        → CSO → COO
- content tasks         → content_review dept head
- default               → department head
```

---

## LIÊN KẾT

- Bài viết: https://vnrom.net/2026/03/clawtask-nen-tang-dieu-phoi-cong-viec-cho-ai-agents-khong-chi-la-mot-kanban-board/
- Tool path: `d:\Project\AI OS\tools\clawtask\`
- API file: `d:\Project\AI OS\tools\clawtask\clawtask_api.py`
- Liên quan: `planning_pmo` department (owner của ClawTask)
- Liên quan: `monitoring_inspection` (consumes ClawTask data)

---

## TAGS
`task-orchestration` `ai-agents` `workflow` `kanban` `clarification` `human-in-the-loop` `MCP` `REST-API` `T1-internal`
