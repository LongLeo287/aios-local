name: gcp_deploy_skill
description: GCP deployment commands and instructions for architect agents
# gcp_deploy_skill
**ID:** `gcp_deploy_skill` | **Type:** Bridge | **Dept:** Dept 03 — IT Infra

## Mô tả
Bộ kỹ năng chuẩn chỉnh dành cho đặc vụ `gcp_architect` để tự động hóa việc đưa Source code lên nền tảng Google Cloud (đặc biệt là Cloud Run / App Engine) thông qua bộ công cụ `gcloud CLI`.
Được cấu trúc theo định dạng phân quyền từ `spawn_agent_skill.md` nhằm bảo đảm việc deploy (Worker Agent) không làm rác bộ nhớ của Môi trường Lõi (Orchestrator).

## Tính năng (Features)
1. **Cloud Run Auto-Build:** Bọc lệnh `gcloud run deploy [SERVICE] --source .`. Phù hợp khi project có sẵn Dockerfile hoặc để Google's buildpacks tự động build image.
2. **App Engine Deploy:** Bọc lệnh `gcloud app deploy app.yaml`. Dành cho App Engine Standard/Flexible.
3. **Context Isolation (Delegation):** Tách bạch hàng trăm dòng log trace ra khỏi Session Memory.

## Prompt / Delegation Template
Khi Orchestrator/Main Agent (`Antigravity` hoặc `Claude Code`) muốn deploy app, Mẫu giao việc cho Tướng `gcp_architect` (Worker) phải tuân theo format Isolation sau:

```markdown
## DELEGATION TASK

**Goal:** Deploy dự án [Tên_Thư_Mục] lên mạng lưới Google Cloud.

**Scope:**
- Project directory: `[Thư/mục/của/code]`
- Tên dịch vụ Cloud Run: `[Tên Service]`
- Chỉ dùng Shell trực tiếp, không spawn thêm file trung gian trừ phi thiết yếu.

**Constraints:**
- Tuyệt đối KHÔNG in ra Console toàn bộ stack trace của gcloud CLI nếu thành công. 
- Giữ session sạch nhất có thể.

**Expected Output:**
- [ ] Link HTTPS của Service Cloud Run đã live.
- [ ] Status Code của lần curl thử đầu tiên (ví dụ 200 OK).
- [ ] Kết thúc Delegate Worker Task.
```

## Cách kích hoạt
Skill này dựa trên System Prompt thuần (Cognitive Skill), ép Agent dùng ngữ pháp shell CLI chuẩn.
- Đảm bảo OS có sẵn `gcloud` và đã được Login (`gcloud auth login`).
- Agent đọc cấu trúc này làm kim chỉ nam thực thi trực tiếp trên terminal bằng Shell block.

---
*Created: 2026-03-27 | Based on: Google Developer MCP + spawn-agent architecture*
