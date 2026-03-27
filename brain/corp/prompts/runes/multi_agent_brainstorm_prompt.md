---
description: Multi-Agent structured design review — simulate peer review with 4 constrained agent roles before implementation
---

# multi_agent_brainstorm_prompt.md — Multi-Agent Review Template
# Authority: Tier 2 | Use AFTER Visual Brainstorm (Format 1) is confirmed
# Language: Vietnamese (user-facing sections) | English (agent role labels)

## MANDATORY DELIVERY RULE
Write output to artifact file → notify_user → NEVER paste in chat
Invoke only for high-risk, high-complexity, or high-impact designs.

---

## Cấu Trúc Multi-Agent Review (Bắt Buộc)

### 🎨 Phase 1 — Primary Designer
```
Tóm tắt thiết kế đề xuất (từ brainstorm đã confirm):
- Quyết định kiến trúc chính: [...]
- Assumptions: [...]
- Decision Log (bắt đầu): [...]
```

---

### ⚔️ Phase 2A — Skeptic / Challenger
```
Prompt nội bộ: "Assume this design fails in production. Why?"
```
**Checklist:**
- [ ] Điểm single-of-failure?
- [ ] Phụ thuộc ngoài không kiểm soát được?
- [ ] Assumption sai có thể xảy ra?
- [ ] YAGNI violations?

**Kết quả:** [liệt kê objections cụ thể]

---

### 🔒 Phase 2B — Constraint Guardian
```
Focus: performance · security · reliability · maintainability · cost
```
**Checklist:**
- [ ] Tải tối đa hệ thống chịu được?
- [ ] Data sensitive có được bảo vệ?
- [ ] Có thể maintain sau 6 tháng không?
- [ ] Chi phí vận hành có scale hợp lý?

**Kết quả:** [pass / reject / cần sửa]

---

### 👤 Phase 2C — User Advocate
```
Focus: UX · cognitive load · clarity · error messaging
```
**Checklist:**
- [ ] User hiểu ngay không cần hướng dẫn?
- [ ] Error messages có ý nghĩa?
- [ ] Flow có điểm nào gây nhầm lẫn?

**Kết quả:** [pass / reject / cần sửa]

---

### ⚖️ Phase 3 — Arbiter / Integrator
```
Resolve all objections. Declare: APPROVED | REVISE | REJECT
```

| Objection | Từ | Accept? | Giải quyết |
|-----------|-----|---------|------------|
| [objection] | Skeptic | ✅/❌ | [cách xử lý] |

**Verdict:** [APPROVED / REVISE / REJECT]
**Decision Log (final):** [ghi lại toàn bộ quyết định]

---

*Chỉ sau khi Arbiter tuyên bố APPROVED mới tiến hành implementation.*
