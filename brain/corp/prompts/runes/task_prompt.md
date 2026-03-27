# task_prompt.md — Mẫu Điền execution_template.md
# Authority: Tier 2 | Dùng bởi: Antigravity (Phase 3 — sau khi user duyệt plan)

## Hướng Dẫn

Sau khi người dùng duyệt brainstorm, Antigravity điền template này
và lưu vào workspace của dự án (KHÔNG lưu trong AI OS core).
File này là task_file được đặt trong blackboard.json.

---

## Cách Điền

```
Thay thế tất cả [placeholder] bằng thông tin thực tế.
Mỗi STEP phải có: Role, Depends on, Input, Action, Output, Success.
Luôn có STEP QA Final và STEP FINAL (Synthesis).
```

---

## Template (Copy và Điền)

```markdown
TASK_ID     : TASK-[YYYYMMDD]-[NNN]
WORKSPACE   : [đường dẫn tuyệt đối đến workspace dự án]
PRIORITY    : HIGH | MEDIUM | LOW
CREATED_AT  : [ISO 8601]
APPROVED_BY : Antigravity (user approved [ngày])
PROJECT     : [tên dự án]
PHASE       : [Phase X: Tên phase]
BACKGROUND  : [1-3 câu context]
GOAL        : [1 câu: thế nào là xong]
CONSTRAINTS :
  - [constraint 1]
  - [constraint 2]

---

### STEP 1: [Tên mô tả]
Role        : RESEARCHER | DEVELOPER | QA
Depends on  : none
Input       : [gì]
Action      : [làm gì cụ thể]
Output      : [cái gì được tạo ra]
Success     : [kiểm tra thế nào biết thành công]

QA Checklist:
- [ ] [check cụ thể 1]
- [ ] [check cụ thể 2]

---

### STEP 2: [Tên mô tả]
Role        : DEVELOPER
Depends on  : STEP 1
[... tương tự ...]

---

### STEP N: QA Final Review
Role        : QA
Depends on  : ALL previous DEVELOPER steps
Action      : Full QA pass on all outputs
Success     : All critical checks pass, no regressions

---

### STEP FINAL: Synthesis & Handoff
Role        : DEVELOPER (acting as Manager)
Depends on  : STEP N
Action      : Aggregate receipts → update blackboard.json
Output      : blackboard.json result.summary updated
```

---

## Sau Khi Điền

1. Lưu file vào: `[workspace]/task_file.md`
2. Cập nhật `blackboard.json`:
   ```json
   {
     "handoff_trigger": "READY",
     "task_file": "[workspace]/task_file.md"
   }
   ```
3. Chạy `handoff_to_claude_code.ps1`
