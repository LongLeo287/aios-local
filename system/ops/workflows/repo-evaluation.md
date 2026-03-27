# Department: operations
---
description: Deep evaluation of a repo before deciding to integrate into AI OS
---
# Repo Evaluation Workflow (Pre-Integration Gate)
# Version: 1.0 | 2026-03-23 | Owner: Antigravity + Dept 20 CIV

> **This workflow runs BEFORE `plugin-integration.md`.**
> Purpose: Decide IF a repo should enter AI OS — not HOW to integrate it.
> Output: One of three verdicts: APPROVE / DEFER / REJECT

---

## STEP 1 — Identity & Purpose Analysis

Before touching any code, answer these 5 questions by reading only the README:

```
Q1. What does this repo DO in one sentence?
Q2. What problem does it solve that AI OS doesn't already solve?
Q3. Who built it? (Individual hobbyist vs. company-backed project?)
Q4. When was it last updated? (>12 months stale = caution flag)
Q5. How many stars/forks? (Signal of community trust)
```

**Decision gate:** If you cannot answer Q1 or Q2 clearly → `REJECT` (no clarity = no fit).

---

## STEP 2 — Conflict & Redundancy Check

Cross-reference against what AI OS already has:

```
Check against:
  - plugins/plugin-catalog.md    (existing plugins by category)
  - brain/shared-context/SKILL_REGISTRY.json  (active skills)
  - brain/shared-context/blackboard.json      (planned integrations)

Ask:
  [A] Does AI OS already have a TIER 1 tool that covers this function?
      YES → REJECT (Tier 1 never gets replaced by a newcomer)

  [B] Does AI OS have a TIER 2 tool with similar function?
      YES → Compare quality. Keep the better one. Mark other as ❌ in catalog.

  [C] Is this truly a gap? (Function not covered anywhere)
      YES → Eligible for APPROVE. Continue to Step 3.
```

---

## STEP 3 — Tier Assignment Decision

Determine which tier the repo belongs to IF approved:

```
TIER 1 criteria (Core Infra — always on):
  ✓ System cannot function without it
  ✓ Used by >3 departments or agents
  ✓ Has a stable API / well-maintained upstream
  ✓ No equivalent already in Tier 1
  → Current Tier 1: Mem0, Firecrawl, LightRAG, CrewAI, GitNexus

TIER 2 criteria (Specialized — Lazy-Load):
  ✓ Serves a specific use case (not cross-cutting)
  ✓ Used occasionally, not every session
  ✓ Can be sandboxed safely (see: .agents/workflows/plugin-lazy-load.md)
  → Most repos fall here

TIER 3 criteria (Blacklist):
  ✗ Conflicts with existing Tier 1 tool
  ✗ Unmaintained (last commit >2 years)
  ✗ License incompatible (GPL/AGPL without CEO approval)
  ✗ Duplicate of another catalog entry
  → Mark ❌ in plugin-catalog.md. Do NOT clone.
```

---

## STEP 4 — Integration Cost Estimate

Before approving, estimate the real cost of bringing this repo in:

```
[ ] Does it require installing new system-level dependencies?
[ ] Does it need a port/service (adds to dashboard.ps1 complexity)?
[ ] Does it need an API key (adds to MASTER.env)?
[ ] Does it need a custom adapter to fit the AI OS patterns?
[ ] How long will integration take? (>1 day = flag for CEO review)
```

**Rule:** If total cost is HIGH and value is MEDIUM → `DEFER` for a later phase.

---

## STEP 5 — Verdict & Catalog Update

**ONE of three verdicts:**

| Verdict | Action |
|---------|--------|
| `APPROVE` | Assign Tier. Update catalog to `⚡`. Proceed to `plugin-integration.md`. |
| `DEFER`   | Update catalog to `🔖`. Add note: *"Defer to Phase X — reason"*. |
| `REJECT`  | Update catalog to `❌`. Add note: *"Rejected — reason (e.g., conflict with Firecrawl)"*. |

**Update `plugins/plugin-catalog.md` immediately** — never leave a repo in `⏸️` status after evaluation.

---

## OUTPUT FORMAT CHUẨN — Repo Intake Report

> Áp dụng khi viết Repo Intake Report gửi CEO. Toàn bộ nội dung bằng **tiếng Việt**.

### Cấu trúc tổng thể 1 report:

```
# 📋 Repo Intake Report — YYYY-MM-DD
**CIV Tickets:** BATCH-XX | **Tổng URLs nhận:** N | **Unique repos:** N | **Không đọc được:** N

## PHÂN LOẠI THEO CATEGORY
[OVERVIEW TABLE — Quét nhanh toàn bộ repos]

## CHI TIẾT — APPROVE repos
[DETAIL CARDS — Từng repo APPROVE có đầy đủ thông tin]

## CHI TIẾT — REFERENCE repos
[DETAIL CARDS — Từng repo REFERENCE (ngắn hơn APPROVE)]

## DEFER & REJECT
[TABLE gọn — chỉ cần repo + lý do]

## DEEP ANALYSIS
[Phân tích sâu 2-3 repos APPROVE ưu tiên cao nhất]

## TỔNG KẾT
[Bảng Count/% + Priority Queue]
```

---

### Format DETAIL CARD — mỗi repo APPROVE:

```markdown
### N. Tên-repo-hiển-thị · `org/repo-name`
🔗 https://github.com/org/repo-name

- **Mô tả:** [1 câu mô tả repo làm gì]
- **License:** MIT / Apache / BSL / GPL / Custom
- **Highlights:** [3-5 tính năng/thống kê nổi bật: số releases, contributors, tính năng chính]
- **AI OS Relevance:** ⭐⭐⭐⭐⭐ — [giải thích tại sao phù hợp với AI OS]
- **Action:** → [lệnh cụ thể hoặc bước tiếp theo]
- **Conflict check:** SAFE / ⚠️ [tên tool conflict] — [lý do]
- **Dept:** [Dept X — tên department phụ trách]
- **Tier:** [1 / 2]
```

### Format DETAIL CARD — mỗi repo REFERENCE (ngắn hơn):

```markdown
### N. Tên-repo-hiển-thị · `org/repo-name`
🔗 https://github.com/org/repo-name

- **Mô tả:** [1 câu mô tả repo làm gì]
- **Học gì:** [điểm cần cherry-pick hoặc học]
- **Action:** → [lưu KI vào brain/knowledge/notes/ hoặc cherry-pick pattern]
```

### Overview Table format (đầu report):

```markdown
| # | Repo | Verdict | Phân tích |
|---|------|---------|-----------|
| 1 | `org/repo` *(tag)* | ✅ APPROVE → Dept X | 1 câu ngắn |
```

---

## INTEGRATION TRIGGER

After APPROVE verdict, hand off to the integration workflow:
```
Trigger: aos integrate <plugin_id>
File: ops/workflows/plugin-integration.md
```

---

## EVALUATION PRINCIPLES

```
1. "No clone by default" — reading README ≠ permission to clone.
   Only clone when verdict = APPROVE.

2. "One function, one tool" — if AI OS already has a tool for a job,
   do not add a second tool for the same job without REJECTING the old one first.

3. "Tier 1 is frozen" — do not propose replacing Tier 1 tools.
   You can only ADD to Tier 1 with explicit CEO approval.

4. "Catalog first" — every repo must be in plugin-catalog.md
   with a verdict before any code is read or dependencies are installed.
```

---

*Workflow Owner: Antigravity | Pre-Integration Gate | Created: 2026-03-23*
*"Evaluate before you integrate. Reject before you clone."*
