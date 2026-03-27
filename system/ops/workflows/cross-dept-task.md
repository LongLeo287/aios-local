# Department: operations
---
description: Cross-dept task protocol — khi 1 task cần 2+ departments phối hợp
---
# ops/workflows/cross-dept-task.md
# Version: 1.0 | 2026-03-25 | Owner: planning_pmo
# Trigger: Task yêu cầu 2+ depts | Coordinator: pmo-agent

---

## Khi nào dùng workflow này?

- Task cần engineering + security (ví dụ: deploy tính năng mới)
- Task cần rd + registry (ví dụ: new skill từ research)
- Task cần content_intake + engineering (ví dụ: tích hợp tool mới)
- Bất kỳ task nào có `cross_dept: true` trong task_backlog.json

---

## BƯỚC 1 — CEO / Coordinator Tạo Cross-Dept Task

```json
{
  "id": "CROSS-001",
  "title": "Task description",
  "depts": ["engineering", "security_grc"],
  "coordinator": "pmo-agent",
  "priority": "HIGH",
  "due": "YYYY-MM-DD",
  "deliverable": "Kết quả cuối cùng cần có"
}
```

Lưu vào: `brain/shared-context/corp/cross_dept_tasks.json`

---

## BƯỚC 2 — pmo-agent Dispatch

1. Đọc cross_dept_tasks.json, lọc tasks OPEN
2. Với mỗi task → tạo sub-task cho từng dept:
   - `subagents/mq/<dept>_tasks.md` ← append cross-dept task
3. Notify mỗi dept qua blackboard: `cross_dept_signal`

```
Ví dụ: CROSS-001 → engineering nhận "Implement feature X"
                  → security_grc nhận "Security review feature X"
```

---

## BƯỚC 3 — Depts Thực Thi Độc Lập

- Mỗi dept viết brief riêng: `BRIEF_<date>_cross_<task_id>.md`
- Không cần chờ dept khác (async)
- Nếu blocked → escalate qua `corp/escalations.md`

---

## BƯỚC 4 — pmo-agent Tổng Hợp Kết Quả

1. Collect all cross-dept briefs cho task_id
2. Verify deliverable đủ chưa
3. Nếu đủ → mark `DONE`, notify CEO qua Telegram
4. Nếu thiếu → ping dept bị lag

```
Slack/Telegram: "✅ CROSS-001 hoàn thành — Engineering + Security đã submit"
hoặc: "⚠️ CROSS-001 lag — security_grc chưa submit (SLA: 2h)"
```

---

## BƯỚC 5 — CEO Approve (nếu cần)

- Task có `ceo_approval: true` → CEO review synthesis brief
- CEO approve → pmo-agent archive → close task
- CEO reject → pmo-agent re-dispatch với feedback

---

## Template: cross_dept_tasks.json

```json
{
  "tasks": [
    {
      "id": "CROSS-001",
      "title": "...",
      "depts": ["dept1", "dept2"],
      "coordinator": "pmo-agent",
      "priority": "HIGH",
      "due": "YYYY-MM-DD",
      "deliverable": "...",
      "ceo_approval": false,
      "status": "OPEN",
      "created": "2026-03-25"
    }
  ]
}
```

---

*Workflow v1.0 | Owner: planning_pmo | Trigger: cross_dept: true in task_backlog*
