# Department: operations
---
description: Tạo phòng ban mới và/hoặc agent mới trong AI OS Corp
---

# AI OS Corp — Quy Trình Tạo Phòng Ban & Agent Mới

## Nguyên tắc bất biến

> **KHÔNG BAO GIỜ tự ý tạo phòng ban/agent mà không có CEO duyệt.**
> Flow bắt buộc: **Phân tích → Đề xuất → CEO duyệt → Execute**

---

## Khi nào mở quy trình này?

| Trigger | Ai khởi động |
|---------|-------------|
| Phát hiện gap khi phân tích repo/URL/tài liệu | Antigravity tự đề xuất |
| CEO hỏi/brainstorm về dept/agent mới | Antigravity phân tích + đề xuất |
| CEO ra lệnh trực tiếp | Bỏ bước Propose, thực thi ngay |

---

## PHASE 1 — Phân Tích & Đề Xuất (Antigravity)

### Bước 1: Kiểm tra agent có sẵn trước
```bash
python system/ops/scripts/create_agent.py --list
python system/ops/scripts/create_agent.py --check <agent-id>
```
- Nếu agent phù hợp **đã tồn tại** → chỉ cần assign vào dept mới (Phase 2B)
- Nếu **chưa có** → cần tạo agent mới (Phase 2A)

### Bước 2: Kiểm tra dept có sẵn
```bash
python system/ops/scripts/propose_dept.py --scan
```

### Bước 3: Tạo proposal và báo CEO
```bash
python system/ops/scripts/propose_dept.py --propose
```
- Proposal được lưu vào: `brain/shared-context/corp/proposals/`
- Antigravity báo CEO: "Tôi đề xuất tạo phòng ban X vì lý do Y, cần CEO duyệt."

---

## PHASE 2A — Tạo Agent Mới (khi chưa có agent phù hợp)

### Bước 4: CEO duyệt proposal

### Bước 5: Scaffold agent
```bash
python system/ops/scripts/create_agent.py \
  --id <agent-id> \
  --dept <dept-name> \
  --tier <2|3> \
  --title "<Agent Title>"
  [--head]   # Nếu là department head
```

**Files tự động tạo:**
- `brain/agents/<agent-id>/AGENT.md` — từ template
- `brain/corp/memory/agents/<agent-id>.md`
- `system/telemetry/receipts/agent_onboard/<agent-id>.json`
- `ecosystem/workforce/agents/<agent-id>/SKILL.md`
- *(Nếu --head)* `brain/corp/departments/<dept>/MANAGER_PROMPT.md`, `WORKER_PROMPT.md`, `rules.md`

---

## PHASE 2B — Assign Agent Có Sẵn Vào Dept

Nếu agent đã có AGENT.md, script tự động:
1. Update trường `Department:` trong AGENT.md
2. Kiểm tra `org_chart.yaml` — báo nếu chưa đăng ký
3. Ghi assignment receipt: `telemetry/receipts/agent_assign/`

---

## PHASE 3 — Tạo & Kích Hoạt Phòng Ban

### Bước 6: CEO approve → auto-execute toàn bộ
```bash
# Approve 1 phòng ban
python system/ops/scripts/propose_dept.py --approve <dept-name>

# Approve tất cả
python system/ops/scripts/propose_dept.py --approve-all
```

**Script tự động chạy 3 bước:**

**STEP 1 — Dept files:**
```
brain/corp/departments/<dept>/MANAGER_PROMPT.md
brain/corp/departments/<dept>/WORKER_PROMPT.md
brain/corp/departments/<dept>/rules.md
brain/corp/memory/departments/<dept>.md
brain/shared-context/corp/daily_briefs/<dept>.md
```

**STEP 2 — Smart agent routing:**
- Agent đã có AGENT.md → assign (2A path)
- Chưa có → gọi `create_agent.py` scaffold (2B path)

**STEP 3 — System registration:**
- `AGENTS.md` → append agent entry (boot Step 4 nhận ra agent)
- `kpi_scoreboard.json` → add dept KPI slot (corp_cycle tracking)
- `blackboard.json` → update `corp_state.total_depts`
- `org_chart.yaml` → **tự động update** bằng ruamel.yaml

---

## PHASE 4 — Manual Verification (luôn làm)

Sau khi script chạy xong, kiểm tra:

```bash
# Check agent profile đủ chưa
python system/ops/scripts/create_agent.py --check <agent-id>

# Check dept files đủ chưa
python system/ops/scripts/propose_dept.py --scan
```

Checklist thủ công:
- [ ] `brain/corp/org_chart.yaml` — agent xuất hiện đúng dept section
- [ ] `brain/shared-context/AGENTS.md` — entry được thêm đúng format
- [ ] `SKILL_REGISTRY.json` — assign skills cho agent mới nếu cần
- [ ] Chạy `boot_check.py` để xác nhận hệ thống nhận ra dept mới

---

## Notes

- **LLM Tier mặc định:** `economy` cho mọi agent mới (upgrade cần CFO+CEO)
- **Autonomy mặc định:** `supervised` — mọi output phải được head agent review
- **Strix Gate:** Agent mới phải qua security scan trước khi trao tool permissions
- **2-Strike Rule:** Fail 2 lần cùng task → set BLOCKED → report Antigravity
