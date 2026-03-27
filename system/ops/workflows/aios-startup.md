# Department: operations
---
description: AI OS Corp V3.1 — Quy trình khởi động toàn hệ thống, từ boot AI agent đến Corp Daily Cycle
---

# 🚀 AI OS STARTUP — Quy Trình Khởi Động Hệ Thống
**Version:** 1.0 | **Date:** 2026-03-26 | **Authority:** Tier 0  
**Trigger:** Đầu mỗi ngày làm việc hoặc khi mở session mới  
**Script tự động:** `python system/ops/aios_startup.py`

---

## TỔNG QUAN — 3 Giai Đoạn Khởi Động

```
GIAI ĐOẠN 1: SYSTEM BOOT        (30 giây)
  → Kiểm tra services, files, ports
  → Tự động khởi động services thiếu

GIAI ĐOẠN 2: AGENT BOOT         (1-2 phút)  
  → Load context 9-step sequence (GEMINI.md)
  → Register session vào blackboard
  → Kiểm tra escalations, KPI, proposals

GIAI ĐOẠN 3: CORP ACTIVATION    (theo yêu cầu)
  → CEO quyết định: Corp Cycle hay Direct Task
  → Trigger: "aos corp start" hoặc task trực tiếp
```

---

## GIAI ĐOẠN 1 — SYSTEM BOOT

### BƯỚC 1.1: Khởi Động Tự Động (chạy script)

```powershell
# Lệnh duy nhất cần nhớ:
python system/ops/aios_startup.py

# Hoặc full verbose:
python system/ops/aios_startup.py --verbose

# Chỉ kiểm tra không khởi động:
python system/ops/aios_startup.py --check-only
```

### BƯỚC 1.2: Script Kiểm Tra (tự động)

Script sẽ tự động kiểm tra và báo cáo:

| Service | Port | Auto-Start? |
|---------|------|-------------|
| Ollama (local LLM) | 11434 | ❌ Thủ công |
| ClawTask API | 7474 | ✅ Tự động |
| GitNexus | 4747 | ✅ Tự động |
| ag-auto-accept | 7476 | ✅ Tự động |
| LightRAG (RAG) | 9621 | ✅ Tự động |
| Telegram Bot | — | ✅ Verify token |

### BƯỚC 1.3: File Integrity Check

Script kiểm tra 6 file quan trọng (STOP nếu thiếu):

```
✅ brain/shared-context/blackboard.json
✅ brain/shared-context/SKILL_REGISTRY.json
✅ brain/shared-context/corp/kpi_scoreboard.json
✅ brain/shared-context/corp/escalations.md
✅ brain/corp/org_chart.yaml (relative corp/)
✅ GEMINI.md
```

---

## GIAI ĐOẠN 2 — AGENT BOOT (GEMINI.md 9-Step Sequence)

> **Áp dụng cho:** Antigravity (Gemini) | Bắt buộc mỗi session

```
STEP 1  → Read GEMINI.md               ← ENTRY POINT (file này)
STEP 2  → Load SOUL.md                 ← Identity & Core Values
STEP 3  → Load GOVERNANCE.md           ← Rules & Authority
STEP 4  → Load AGENTS.md               ← 99 Agent Roster
STEP 5  → Load THESIS.md               ← Strategy & 40 Pillars
STEP 6  → Load report_formats.md       ← Output Format Guide
STEP 7  → Check blackboard.json        ← Active tasks & state
STEP 8  → Load SKILL_REGISTRY.json     ← 20 Skills available
STEP 9  → BEGIN WORK                   ← Sẵn sàng nhận lệnh
```

**Rules bắt buộc:**
- Skip bất kỳ step → Vi phạm governance. Log warning + report CEO.
- File missing → Skip step, continue, báo CEO.
- HARD RULE: Không đọc sai boot file (Gemini ≠ Claude Code).

### BƯỚC 2.1: Đọc Blackboard State

```json
// Đọc brain/shared-context/blackboard.json
{
  "open_items": [...],          // ← Việc còn tồn đọng
  "active_campaign": "...",     // ← Campaign đang chạy
  "handoff_trigger": "IDLE",    // ← IDLE = sẵn sàng
  "corp_cycle_status": "IDLE"   // ← IDLE = OK start cycle
}
```

**STOP nếu:** `corp_cycle_status = "RUNNING"` → Cycle trước chưa xong!

### BƯỚC 2.2: Register Session

```json
// Update blackboard.json:
{
  "target_agent": "Antigravity",
  "status": "ACTIVE",
  "session_start": "<ISO timestamp>",
  "handoff_trigger": "ACTIVE"
}
```

### BƯỚC 2.3: CEO Briefing (auto-generated)

```
📊 AI OS Corp Status — <DATE>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏢 System:   <overall_status from kpi_scoreboard>
🔋 Services: <N> LIVE | <M> DOWN
📋 Blackboard: <summary từ last session>
⚠️  Open Items: <N> pending tasks
📌 Escalations: <L2/L3 nếu có>
🎯 Campaign: <active_campaign>
🧠 Skills: <N> available
🔌 MCPs: 8 configured

→ Sẵn sàng nhận lệnh. Corp Cycle hay Direct Task?
```

---

## GIAI ĐOẠN 3 — CORP ACTIVATION

### Option A: Corp Daily Cycle (khuyến nghị buổi sáng)

```powershell
aos corp start   # Full 8-phase cycle
# OR
python ops/aos.py corp start
```

Flow: Phase 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7  
Xem chi tiết: `system/ops/workflows/corp-daily-cycle.md`

### Option B: Status Check nhanh

```powershell
python system/ops/aios_orchestrator.py once   # Update HUD + Telegram
python ops/scripts/system_pulse.py            # Health check 5-min
python ops/scripts/dept_health.py             # 21 dept health
```

### Option C: Nhiệm Vụ Trực Tiếp (Direct Task)

CEO giao task trực tiếp → Antigravity plan → Handoff Claude Code

```
1. Antigravity: Plan + write implementation_plan.md
2. CEO: Approve (LGTM)
3. Antigravity: Write blackboard.json handoff_trigger=ACTIVE
4. Claude Code: Execute + write receipts
5. Antigravity: Review + report Vietnamese
```

---

## QUICK REFERENCE — LỆNH KHỞI ĐỘNG

```powershell
# === KHỞI ĐỘNG NHANH (1 lệnh) ===
python system/ops/aios_startup.py

# === ORCHESTRATOR ===
python system/ops/aios_orchestrator.py once      # Update HUD + dispatch
python system/ops/aios_orchestrator.py routes    # Xem 77 routing rules

# === TELEGRAM ===
python system/ops/telegram_dispatch.py status    # Gửi system status
python system/ops/telegram_dispatch.py test      # Test kết nối

# === CORP CYCLE ===
python ops/aos.py corp start    # Full cycle
python ops/aos.py corp brief    # CEO brief only
python ops/aos.py status        # Current status

# === SERVICES THỦ CÔNG ===
python system/ops/scripts/lightrag_server.py          # LightRAG :9621
docker compose up -d infra/observability/             # Langfuse :3100
```

---

## SƠ ĐỒ KHỞI ĐỘNG

```
CEO mở máy
    │
    ▼
[TERMINAL] python system/ops/aios_startup.py
    │
    ├─ [1.1] Check blackboard.json       ✅ PASS / ❌ STOP
    ├─ [1.2] Check 6 critical files      ✅ PASS / ⚠️ WARN
    ├─ [1.3] Check ports                 ✅ LIVE  / 🔴 DOWN
    ├─ [1.4] Check SKILL_REGISTRY        ✅ FRESH / ⚠️ OLD
    ├─ [1.5] Update HUD STATUS.json      ✅ DONE
    └─ [1.6] Send Telegram boot report   ✅ SENT
    │
    ▼
[AI AGENT] Antigravity đọc GEMINI.md
    │
    ├─ STEP 2: SOUL.md          ← Identity
    ├─ STEP 3: GOVERNANCE.md    ← Rules
    ├─ STEP 4: AGENTS.md        ← Roster
    ├─ STEP 5: THESIS.md        ← Strategy
    ├─ STEP 6: report_formats   ← Output format
    ├─ STEP 7: blackboard.json  ← State check
    ├─ STEP 8: SKILL_REGISTRY   ← Load skills
    └─ STEP 9: BEGIN WORK
    │
    ▼
[CEO] Nhận briefing từ Antigravity:
    │
    ├─ Corp Cycle? → "aos corp start"
    ├─ Direct Task? → Mô tả task
    └─ Status Check? → "aos status" hoặc HUD
```

---

## CÁC TRƯỜNG HỢP ĐẶC BIỆT

### Trường hợp 1: Blackboard `corp_cycle_status = "RUNNING"`
```
→ Cycle trước chưa xong. KHÔNG start cycle mới.
→ Đọc escalations.md để hiểu tình trạng.
→ CEO quyết định: Reset hay tiếp tục?
→ Reset: Set blackboard corp_cycle_status = "IDLE"
```

### Trường hợp 2: Có L3 Escalation mở
```
→ KHÔNG start Corp Cycle.
→ Báo cáo CEO ngay lập tức.
→ CEO resolve L3 trước khi start.
```

### Trường hợp 3: Service quan trọng DOWN
```
Ollama DOWN → Không dùng local LLM được. Dùng API thay thế.
ClawTask DOWN → Mất task tracking. Chạy: npm start --prefix ecosystem/tools/clawtask
LightRAG DOWN → CIV pipeline bị ảnh hưởng. Fallback: Claude Code RESEARCHER
Telegram DOWN → Mất notification. Check .env BOT_TOKEN.
```

### Trường hợp 4: SKILL_REGISTRY > 7 ngày chưa cập nhật
```
→ Warning. Không STOP.
→ Chạy: python system/ops/aios_orchestrator.py once (tự update)
→ Hoặc: powershell ops/scripts/skill_loader.ps1
```

---

## SECURITY CHECKLIST (mỗi boot)

```
☐ SkillSentry 9-layer scanner: ACTIVE (passive monitoring)
☐ Không có credentials trong project files
☐ .env không được commit vào git
☐ Strix-agent sẵn sàng scan tool mới
☐ GEMINI.md có "HARD RULE" còn hiệu lực
```

---

## SESSION CLOSE PROTOCOL

Khi kết thúc session (đọc `post-session.md` để chi tiết):

```
1. Update blackboard.json:
   - status: "IDLE"
   - handoff_trigger: "COMPLETE" hoặc "BLOCKED"
   - summary: <tóm tắt session>

2. Mark tasks trong ClawTask: done/blocked

3. L2/L3 issues → write to corp/escalations.md

4. Auto: powershell ops/scripts/update_hud.ps1 (HUD snapshot)
```

---

*v1.0 | 2026-03-26 | AI OS Corp V3.1 | Owner: Antigravity*  
*Xem thêm: GEMINI.md, antigravity-boot.md, pre-session.md, corp-daily-cycle.md*
