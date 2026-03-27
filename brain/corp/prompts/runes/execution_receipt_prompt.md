---
description: Execution Receipt — post-execution report after Claude Code or Antigravity completes a task. Required for all significant executions.
---

# execution_receipt_prompt.md — Execution Receipt Template
# Authority: Tier 2 | Use when: task execution is complete
# Language: <!--LANG-->Vietnamese<!--/LANG--> (user-facing) | English (technical field labels)

## MANDATORY DELIVERY RULE
Write to artifact file → notify_user → NEVER paste in chat

---

## ✅ Execution Receipt

**Task:** [tên task]
**Executed by:** [Antigravity / Claude Code]
**Date:** [YYYY-MM-DD HH:MM]
**Status:** [COMPLETED ✅ / PARTIAL ⚠️ / FAILED ❌]

---

### 📋 Tóm Tắt

> [Mô tả ngắn gọn những gì đã làm — 2-3 câu]

---

### 📁 Files Đã Thay Đổi

| File | Loại thay đổi | Ghi chú |
|------|--------------|---------|
| [path/to/file.py] | Created / Modified / Deleted | [...] |
| [path/to/file.md] | Created / Modified / Deleted | [...] |

---

### ⚡ Lệnh Đã Chạy

```bash
# Liệt kê các command đã execute
$ [command 1]
$ [command 2]
```

---

### 🧪 Kết Quả Kiểm Tra

| Test / Verification | Kết quả | Ghi chú |
|--------------------|---------|---------|
| [build / test / manual check] | ✅ Pass / ❌ Fail | [...] |

---

### ⚠️ Vấn Đề Còn Lại

- [Issue 1] — Priority: High/Med/Low
- [Issue 2] — Priority: High/Med/Low

---

### ➡️ Bước Tiếp Theo Đề Xuất

1. [...]
2. [...]
