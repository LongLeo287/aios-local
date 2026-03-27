# [HANDOFF] Chiến Dịch Giao Việc: Xây Dựng Kỹ Năng (Skills) Cho GCP Architect

**Từ:** Antigravity (Kiến trúc sư trưởng)
**Đến:** Claude Code CLI (Kỹ sư triển khai)
**Mục tiêu:** Xây dựng toàn bộ Hồ sơ (Profile) và Mã kỹ năng (Skills Code) cho Đặc vụ `gcp_architect` dựa trên các tài liệu tiêu chuẩn `Open Standard` của AI OS V3.1 và trí tuệ từ Google Developer MCP.

---

## 🛠️ Tri thức nền tảng (Claude Code bắt buộc phải đọc trước khi Code)
Mở và ngấu nghiến 3 tài liệu sau để nắm được luật lệ Code của Sếp (AI OS):
1. `d:\AI OS CORP\AI OS\brain\knowledge\agent_skills_open_standard.md` (LUẬT CODE SKILL)
2. `d:\AI OS CORP\AI OS\brain\knowledge\spawn_agent_skill.md` (HƯỚNG DẪN TẠO SKILL)
3. Tra cứu `google-developer-knowledge` MCP để cào tài liệu mới nhất về: *gcloud CLI, Cloud Run, Cloud Build.*

## 📋 Hạng mục Công Việc (Task Queue)
- [ ] **Khởi tạo hệ thống Skill:** Trong thư mục `ecosystem/skills/`, hãy tạo một bộ Skill mới tên là `gcp_deploy_skill`. Bộ code này phải đúng 100% chuẩn Open Standard (như có `schema.json`, `index.py`, `README.md`).
- [ ] **Code hóa logic:** Viết code Python bên trong Skill này để thực thi lệnh `gcloud builds submit` và `gcloud run deploy`. Không được bịa lệnh! Phải dùng MCP Google Dev để tra API gcloud trước.
- [ ] **Gắn Skill vào Cấy ghép (Bind):** Sửa đổi file `ecosystem/subagents/gcp_architect/agent.yaml` và `prompts/system_prompt.md` để kết nối thẳng con Subagent này vào cái Skill `gcp_deploy_skill` vừa tạo.
- [ ] **Kiểm tra chéo:** Đảm bảo code chạy mượt mà trên môi trường Local (giả lập) hoặc ít nhất không dính lỗi Cú pháp lệnh Google.
- [ ] **Báo cáo:** Ghi kết quả "Hoàn Tất Mĩ Mãn" vào `brain/shared-context/blackboard.json` (sửa `handoff_trigger` thành `DONE`).

> ⚠ **CLAUDE CODE CLI CHÚ Ý:** Tuyệt đối không xóa bất cứ file System nào. Code xong nhớ báo cáo lại cho Master (Sếp).

---

## TASK-CC-0326-BOOT-FIX: Sync CLAUDE.md Cycle Number
**Status:** READY
**Priority:** P1
**Assigned:** Claude Code CLI
**Created:** 2026-03-26T19:16:00+07:00

### Task
Fix CLAUDE.md header: Cycle 8 (2026-03-23) -> Cycle 11 (2026-03-26)

### Steps
1. Doc file CLAUDE.md tai root: d:\AI OS CORP\AI OS\CLAUDE.md
2. Tim dong: # AI OS CORP | Cycle 8 | Last synced: 2026-03-23
3. Thay thanh: # AI OS CORP | Cycle 11 | Last synced: 2026-03-26
4. Luu file UTF-8
5. Verify: git diff CLAUDE.md

### Receipt
system/telemetry/receipts/RECEIPT_CC0326_claude_md_sync.md
