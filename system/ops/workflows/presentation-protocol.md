# Department: operations
---
description: Full presentation protocol — all 5 formats for brainstorms, reports, analyses. Every agent must follow this when communicating with the user.
---

# Presentation Protocol — Complete Reference
# All agents read this. No exceptions.

---

## CARDINAL RULE

1. **NO MARKDOWN FORMATTING ALLOWED.** Do not use `#`, `*`, `**`, `|` tables, or fenced code blocks for styling in user-facing reports and brainstorms. Use spacing, ALL CAPS for emphasis, and emojis (✅, ⚠️, ❌, 📌) for structure.
2. **NEVER present brainstorms, reports, or analysis inline in chat.** Always write content to an artifact file and notify the user.

---

## FORMAT SELECTOR (Quick Reference)

| Situation | Format | Rune to load |
|-----------|--------|-------------|
| Exploring a problem, comparing options | **1 — Visual Brainstorm** | `runes/brainstorm_prompt.md` |
| Complex design needing stress-testing | **2 — Multi-Agent Review** | `runes/multi_agent_brainstorm_prompt.md` |
| New product feature / capability discovery | **3 — BMAD Method** | `runes/bmad_prompt.md` |
| Recording a finalized decision | **4 — Decision Log** | `runes/decision_log_prompt.md` |
| Reporting completed task execution | **5 — Execution Receipt** | `runes/execution_receipt_prompt.md` |
| Báo cáo nghiệm thu Data/Repo/URL (CIV) | **6 — Dashboard Analytics Report** | Tự kích hoạt khi chạy luồng CIV Intake |

Full selector logic: `runes/report_formats.md`

---

## FORMAT 1 — Visual Brainstorm & Report (CEO-Approved 2026-03-19)

**When:** Any brainstorm, analysis, proposal, or strategic report delivered to CEO.

**Delivery:** Always artifact `.md` + `notify_user`. Never inline in chat.

**Structure — Combine elements based on content type:**

| Element | Format | Use When |
|---|---|---|
| **Architecture/Flow** | Mermaid diagram (fixed at top, outside Carousel) | Always required |
| **Comparison/Options** | Carousel (multi-slide, fenced with 4 backticks) | Comparing 2+ options or feature lists |
| **Risks/Decisions** | Alert blocks `> [!WARNING]` `> [!IMPORTANT]` | Risks, budget gates, CEO approval needed |
| **Roadmap/Phases** | ASCII Timeline (`──►`) | Step-by-step delivery, day-by-day rollout |
| **Data/Specs** | Markdown Tables + `---` dividers + emoji headers | KPIs, specs, structured data |

**Mermaid Safety Rules (prevents Parse Errors):**
- NO `\n` inside node labels
- NO `===` arrows — use `==>` instead
- NO parentheses `()` or colons `:` in node labels
- Use `["Label - Sublabel"]` pattern (dash as separator)

**Language:** Vietnamese for all user-facing content.

Close with: *"Chờ Sếp phản hồi chốt phương án trước khi thực thi."*



---

## FORMAT 2 — Multi-Agent Review

**When:** High-stakes design, architecture decisions, complex systems
**Pre-condition:** FORMAT 1 must be completed and confirmed first
**Structure:**

1. **Primary Designer** — owns the design, runs FORMAT 1
2. **Skeptic** — "assume this fails, why?"
3. **Constraint Guardian** — performance, security, cost, maintainability
4. **User Advocate** — UX, cognitive load, clarity
5. **Arbiter** — resolves objections, declares APPROVED / REVISE / REJECT

---

## FORMAT 3 — BMAD Method

**When:** New product capabilities, feature scoping, hypothesis-driven planning
**Structure:**

1. **Problem Statement** — what problem, who is affected, impact
2. **Hypothesis** — "We believe [solution] will help [user] achieve [outcome]"
3. **Approaches** — 2-3 options with effort/risk/confidence
4. **Success Metrics** — baseline, target, how to measure
5. **Go / No-Go** — recommendation with conditions

---

## FORMAT 4 — Decision Log

**When:** A significant decision has been finalized — must be recorded
**Structure:**

1. **Decision Made** — clear 1-2 sentence statement
2. **Alternatives Considered** — table with why each was rejected
3. **Rationale** — why this option was chosen
4. **Risks Acknowledged** — with mitigations
5. **Review Condition** — when to reconsider this decision

---

## FORMAT 5 — Execution Receipt

**When:** After completing a significant task execution
**Structure:**

1. **Task Summary** — what was done, status (COMPLETED / PARTIAL / FAILED)
2. **Files Changed** — table with path, change type, notes
3. **Commands Run** — exact commands executed
4. **Verification Result** — tests passed/failed
5. **Next Steps** — what to do next

---

## Language Rules (HARD RULES)

| Content type | Language | Target Audience | Delivery |
|-------------|----------|-----------------|---------|
| Brainstorms, Proposal & Reports | **Vietnamese** | Sếp / CEO | artifact + notify_user |
| System Files, Code, Configs, Tasks | **English w/ Vietnamese Comments** | Machine Core / Agents | write directly |
| Agent-to-agent messages | **English** | Agents | inline |
| Short conversational replies | **Vietnamese** | Sếp / CEO | inline in chat only |

**CRITICAL RULE:** EVERY file generated (except CEO reports) MUST be in English but heavily annotated/commented in Vietnamese to explain the logic to the CEO.

---

## FORMAT 6 — Dashboard Analytics Report (CIV / Intake)

**When:** Reporting batch content intake (CIV) of Repos, URLs, Data, PDFs, Images. Tự kích hoạt 100% tự động bởi `content-analyst-agent` hoặc `ANTIGRAVITY` khi Intake Cycle kết thúc. Không cần đợi lệnh từ CEO.
**Structure:**

1. **Header Block:** (GitHub Alert `> [!NOTE]`) — Tổng hợp Ticket, Tổng số lượng, Thành công/Thất bại.
2. **Mermaid Pie Chart:** Thống kê phân loại dữ liệu nạp vào theo tỷ lệ % (APPROVE, REFERENCE, DEFER, REJECT).
3. **Priority Alert:** (GitHub Alert `> [!IMPORTANT]`) — Kê biên danh sách ưu tiên cao nhất (Priority 1) kèm hành động.
4. **Carousel Bảng Dữ liệu:** 4 dấu backticks (` ` ` `carousel), chia các hạng mục logic bằng `<!-- slide -->`. Bên trong là Bảng (Table) kèm trạng thái Emoji.
5. **Reject Warning:** (GitHub Alert `> [!WARNING]`) — Kê biên hạng mục bị trục xuất khỏi hệ thống.
6. **Mermaid Flowchart:** Sơ đồ mạng lưới mũi tên chứng minh toàn bộ dữ liệu đã được AI OS xử lý khép kín.

**Rule Tối Thượng Format 6:**
- Cấm tuyệt đối dùng Heading Markdown (`#`).
- Mọi tiêu đề phải in hoa toàn bộ (ALL CAPS) + Emoji đứng trước.
- Giọng văn: "Đốc Tướng" (Tiếng Việt) ngắn gọn, đi thẳng vào vấn đề.

---

## File Naming Convention

```
reports/brainstorm_[topic]_[YYYY-MM-DD].md
reports/decision_log_[topic]_[YYYY-MM-DD].md
reports/receipt_[task]_[YYYY-MM-DD].md
```
