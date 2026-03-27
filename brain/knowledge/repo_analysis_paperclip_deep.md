# 🔬 DEEP ANALYSIS: paperclipai/paperclip → Personal AI OS Patterns
**Date:** 2026-03-14
**Iteration:** Deep Dive v2

---

## Patterns ĐÃ BIẾT (từ lần trước)
1. AGENTS.md Pattern
2. Control Plane Design (Single-assignee, Atomic checkout)
3. Company-scoped Multi-tenancy
4. Skills Directory
5. Multi-tenant scoping / Control plane mental model

---

## 🆕 Patterns MỚI PHÁT HIỆN

### 6. PARA Memory System (`skills/para-memory-files/SKILL.md`)
**Nguồn:** Tiago Forte's PARA methodology (Projects, Areas, Resources, Archives)
- File-based memory với vector search tích hợp
- Lệnh: `vsearch "conceptual question"` → semantic search thuần
- Memory theo ngày: `$AGENT_HOME/memory/YYYY-MM-DD.md`
- Superseded file pattern: Đánh dấu file cũ bằng `supersededBy:` tag
- **Áp dụng AI OS:** Cấu trúc lại `AI OS/memory/` theo PARA (Projects/Areas/Resources/Archives) thay vì `core/tenants/`

---

### 7. Agent Inbox & Wake Model (Heartbeat Pattern)
**Nguồn:** `SKILL.md` + `SPEC.md`
- **Thin ping heartbeat:** Khi nhận wake signal, agent chủ động fetch task từ `/api/agents/me/inbox-lite`
- **Inbox-lite endpoint:** API trả về danh sách task nhỏ gọn, agent chỉ pull khi cần
- **Run Identity:** Mỗi lần chạy có `PAPERCLIP_RUN_ID` để trace
- **Áp dụng AI OS:** Thiết kế `pre-session.md` hook tương tự — pull task từ `task.md` thay vì polling API

---

### 8. Blocker Communication Pattern
**Nguồn:** `skills/paperclip/SKILL.md`
> "If you are blocked at any point, you MUST update the issue with a comment that explains the blocker and who needs to act."
- Khi bị block, agent KHÔNG dừng — viết blocker comment, đổi status, và handoff explicitly
- **Áp dụng AI OS:** Thêm vào `CIRCUIT BREAKER` rule: khi thất bại 2 lần, ghi `<blocker>` tag vào `task.md` và notify user với action required cụ thể.

---

### 9. Issue Lifecycle State Machine
**Nguồn:** `doc/TASKS.md`
- Core entity: **Issue** (đơn vị công việc)
- States: `backlog → todo → in_progress → done / cancelled`
- **Single-assignee invariant:** Chỉ 1 agent/người hold issue tại một thời điểm
- **Checkout semantic:** Lấy issue = lock exclusive, không ai khác được động
- **Áp dụng AI OS:** Formalize task states trong `task.md` thay vì chỉ `[ ]` / `[x]` → dùng `[backlog]`, `[todo]`, `[/]`, `[x]`, `[blocked]`

---

### 10. MCP Function Contracts (`doc/TASKS-mcp.md`)
**Nguồn:** Paperclip publish task system qua MCP protocol
- Định nghĩa function contracts: create_issue, update_issue, list_issues, checkout_issue
- Có cursor-based pagination
- **Áp dụng AI OS:** AI OS hiện có MCP config nhưng chưa có function contracts rõ ràng. Tạo `AI OS/mcp/contracts.md` để document các tool functions chuẩn.

---

### 11. Deployment Modes Design
**Nguồn:** `doc/DEPLOYMENT-MODES.md`
- **Operator mode:** Full control, board access
- **Agent mode:** API key bearer, scoped access
- **Public mode:** External exposure với auth gates
- **Áp dụng AI OS:** Phân biệt rõ 2 modes trong Gatekeeper: `OPERATOR` (Antigravity có toàn quyền) vs `AGENT` (Claude Code chỉ được workspace được assign)

---

### 12. Approval Gate + Budget Hard-Stop
**Nguồn:** `AGENTS.md` → "Approval gates for governed actions" + "Budget hard-stop auto-pause"
- Hành động quan trọng phải qua gate (Tier 3/4 trong AI OS đã có)
- **Budget hard-stop:** Khi agent vượt quá ngưỡng (token/cost), tự pause và report
- **Áp dụng AI OS:** Thêm khái niệm "budget" vào CIRCUIT BREAKER — định nghĩa ngưỡng: max 5 tool calls cho 1 sub-task trước khi phải report

---

### 13. Activity Logging cho Mutating Actions
**Nguồn:** `AGENTS.md` section 8
> "write activity log entries for mutations"
- Mọi action ghi hoặc xóa file phải có activity log entry
- **Áp dụng AI OS:** Tạo `AI OS/memory/activity.log` — ghi từng action của agent theo format timestamp + action + file_affected

---

### 14. Spec-Driven Development
**Nguồn:** `doc/SPEC.md` (26KB) + `doc/SPEC-implementation.md` (25KB)
- SPEC.md = long-horizon vision (không thay đổi thường xuyên)
- SPEC-implementation.md = V1 concrete build contract (cụ thể, có thể thay đổi)
- **Áp dụng AI OS:** AI OS chưa có SPEC.md tách biệt. Cần tách `THESIS.md` thành `THESIS.md` (vision dài hạn) và `SPEC-current.md` (giai đoạn hiện tại đang build)

---

### 15. CliHub / Published Skills Ecosystem (`doc/CLIPHUB.md` - 13KB)
**Nguồn:** ClipHub = marketplace cho Paperclip skills
- Agents có thể install skills từ hub: `clip install <skill-name>`
- Skills có metadata: name, description, version, dependencies
- **Áp dụng AI OS:** `AI OS/plugins/` hiện có nhưng chưa có registry chuẩn. Tạo `plugins/plugin_registry.json` với format: name, version, source, installed_at

---

### 16. OpenClaw Onboarding Pattern (`doc/OPENCLAW_ONBOARDING.md`)
**Nguồn:** Template onboarding cho AI runtime mới (Claude, Gemini, etc.)
- Tài liệu hướng dẫn từng bước cho AI agent mới gia nhập system
- **Áp dụng AI OS:** Tạo `AI OS/rules/ONBOARDING.md` — tài liệu read-first cho bất kỳ AI mới nào (hiện AGENTS.md + SOUL.md đóng vai này nhưng chưa có flow rõ)

---

## 📊 Summary Table

| # | Pattern | Nguồn | Ưu tiên áp dụng |
|---|---|---|---|
| 6 | PARA Memory System | skills/para-memory-files | 🔴 HIGH |
| 7 | Agent Inbox / Heartbeat | SKILL.md + SPEC | 🟡 MEDIUM |
| 8 | Blocker Communication | SKILL.md | 🔴 HIGH |
| 9 | Issue Lifecycle State Machine | TASKS.md | 🔴 HIGH |
| 10 | MCP Function Contracts | TASKS-mcp.md | 🟡 MEDIUM |
| 11 | Deployment Modes | DEPLOYMENT-MODES.md | 🟡 MEDIUM |
| 12 | Budget Hard-Stop | AGENTS.md | 🔴 HIGH |
| 13 | Activity Logging | AGENTS.md | 🟢 LOW |
| 14 | Spec-Driven Development | SPEC.md | 🔴 HIGH |
| 15 | Skills Ecosystem/Registry | CLIPHUB.md | 🟡 MEDIUM |
| 16 | Onboarding Pattern | OPENCLAW_ONBOARDING.md | 🟢 LOW |
