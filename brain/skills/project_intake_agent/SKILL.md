---
name: project_intake_agent
display_name: Project Intake Agent — Client Brief Collector
version: 1.0.0
tier: 2
category: client-services
description: >
  Thu thập và xử lý yêu cầu project từ client bên ngoài qua bất kỳ channel nào
  (Telegram, Discord, Web). Validate brief, score feasibility, route đến Proposal Engine.
  Triggers: "nhận project", "client gửi brief", "new intake", "project request",
  "có dự án cần làm", "cần thuê AI".
accessible_by:
  - operations
  - orchestrator_pro
  - nullclaw
  - tinyclaw
dependencies:
  - context_manager
  - notification_bridge
load_on_boot: false
---

# Project Intake Agent

## Role

Là **cổng tiếp nhận** đầu tiên khi client liên hệ AI OS Corp.
Thu thập đủ thông tin → validate → score → forward tới Proposal Engine.

## Trigger Phrases

- "Có project muốn hợp tác" → bắt đầu intake flow
- "Cần thuê AI agents" → bắt đầu intake flow  
- "new intake" → manual trigger từ Ops
- "show intakes" → list tất cả pending intakes
- "check intake <ID>" → xem chi tiết 1 intake

## Core Workflow

Khi nhận message từ client (qua bất kỳ channel nào):

### Phase 1: Welcome & Form

```
1. Gửi template welcome (từ CLIENT_INTAKE_GATEWAY.md §3)
2. Set state: COLLECTING
3. Wait for client responses (timeout: 24h)
```

### Phase 2: Collect & Validate

```
Collect 5 fields:
  - project_type     (required)
  - description      (required, min 20 words)
  - timeline         (required, must be future date)
  - budget_range     (required, one of 4 brackets)
  - contact_info     (required)

Nếu thiếu field → hỏi lại cụ thể field đó
Sau 3 lần hỏi lại không có → escalate to ops manually
```

### Phase 3: Score & Route

```
feasibility_score = match_against_skill_registry(brief.project_type, brief.description)

Write to: shared-context/client_intake/YYYY-MM-DD_HHMMSS_<slug>.json
Notify: operations via notification_bridge

IF budget >= "$10k+" OR feasibility < 4:
  → escalate to CEO immediately
ELSE:
  → trigger proposal_engine with intake_id
```

### Phase 4: Confirm to Client

```
"✅ Đã nhận brief của bạn! [INTAKE-ID]
Team sẽ gửi proposal trong 2 giờ làm việc.
Bạn có thể theo dõi status qua [channel]."
```

## Commands (Internal)

| Command | Hành động |
|---------|-----------|
| `list_intakes [status]` | List intakes theo status |
| `view_intake <id>` | Xem chi tiết intake |
| `assign_intake <id> <dept>` | Gán manual cho dept |
| `reject_intake <id> <reason>` | Từ chối với lý do |
| `escalate_intake <id>` | Chuyển lên CEO |

## Output Format

Mỗi intake tạo file theo schema trong `CLIENT_INTAKE_GATEWAY.md §4`.
Index file: `shared-context/client_intake/_index.json`.

## Integration

- **nullclaw**: route Telegram/Discord/WhatsApp messages → skill trigger
- **tinyclaw**: multi-agent intake (nhiều client cùng lúc)  
- **proposal_engine**: auto-triggered sau khi intake complete
- **notification_bridge**: notify ops + CEO

## Error Handling

| Lỗi | Xử lý |
|-----|-------|
| Client không trả lời 24h | Lưu draft, notify ops |
| Feasibility < 4 | Escalate + notify CEO |
| Trùng intake (same client + type) | Merge hoặc hỏi client |
| Channel disconnect | Retry 3 lần → log error |
