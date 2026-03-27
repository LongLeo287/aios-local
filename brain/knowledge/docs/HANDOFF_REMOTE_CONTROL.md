# AI OS Corp — Remote Control System HANDOFF
# Project: nullclaw Telegram Bot + Automation Gateway
# Owner: CEO @LongLeo | Assigned: Scrum-Master (COO)
# Date: 2026-03-18 | Status: LIVE ✅

---

## 🎯 Project Overview

nullclaw adalah gateway tự động hóa chính của AI OS Corp — kết nối Telegram của CEO (@LongLeo) với toàn bộ hệ thống AI agents. CEO điều khiển mọi thứ qua chat.

---

## 📦 Stack Hiện Tại

| Component | Status | Location | Port |
|-----------|--------|----------|------|
| **nullclaw** (Telegram gateway) | 🟢 LIVE | `REMOTE/claws/nullclaw/` | 3000 |
| **AstrBot v4.20.1** | 🟡 INSTALLED | `plugins/AstrBot/` + `runtime/astrbot/` | 6185 |
| **ClawTask Dashboard** | 🟢 LIVE | `tools/clawtask/` | 7474 |
| **LightRAG** | ⚫ IDLE | `plugins/LightRAG/` | — |
| **cognee** | ⚫ IDLE | `plugins/cognee/` | — |

---

## 🤖 Bot Credentials (SECURE)

```
Platform:    Telegram
Bot Token:   [REDACTED_TELEGRAM_TOKEN]
Admin ID:    646106732 (@LongLeo)
LLM:         Gemini 2.0 Flash ([REDACTED_GEMINI_API_KEY])
Config:      C:\Users\VUA2HAND\.nullclaw\config.json
Binary:      D:\Project\AI OS\REMOTE\claws\nullclaw\zig-out\bin\nullclaw.exe
```

Full credentials: `D:\Project\AI OS\secrets\.env.telegram`

---

## 🚀 Startup Commands

```powershell
# Khởi động hệ thống đầy đủ
powershell -ExecutionPolicy Bypass -File "D:\Project\AI OS\scripts\startup.ps1"

# Chỉ nullclaw bot
& "D:\Project\AI OS\REMOTE\claws\nullclaw\zig-out\bin\nullclaw.exe" gateway

# Chỉ ClawTask Dashboard
python -m http.server 7474 --directory "D:\Project\AI OS\tools\clawtask"

# Check bot status
& "D:\Project\AI OS\REMOTE\claws\nullclaw\zig-out\bin\nullclaw.exe" status
```

---

## 📋 Sprint Tasks (Scrum-Master quản lý)

### 🔴 HIGH — Ngay bây giờ

- [ ] **TG-001** Test bot hoạt động: @LongLeo nhắn → bot reply Gemini
- [ ] **TG-002** Thêm AI OS Corp system prompt chi tiết hơn vào config
- [ ] **TG-003** Auto-start bot khi Windows boot (Task Scheduler)

### 🟡 MEDIUM — Sprint này

- [ ] **AOS-004** AstrBot WebUI config: thêm Telegram token qua http://localhost:6185/
- [ ] **AOS-005** Plugin `astrbot_plugin_aios_corp` — test /clawtask command
- [ ] **AOS-006** Sync ClawTask → JSON file để plugin đọc được
- [ ] **REG-007** SKILL_REGISTRY.json update — promote LightRAG + cognee + crewAI lên T2
- [ ] **LEG-008** GATE_LEGAL review `awesome-claude-skills` license

### 🔵 LOW — Backlog

- [ ] **INF-009** Thêm Discord channel vào nullclaw config
- [ ] **INF-010** Setup Tailscale tunnel để truy cập remote (không chỉ localhost)
- [ ] **INF-011** nullclaw heartbeat.md — autonomous proactive checks
- [ ] **INF-012** LightRAG integration — RAG pipeline cho Research Agent
- [ ] **INF-013** cognee integration — Agent Memory Engine
- [ ] **INF-014** Zalo OA bot evaluation (cần business account)
- [ ] **INF-015** CIV Batch 4 planning

---

## 🔄 SOPs (Standard Operating Procedures)

### SOP-BOT-01: Khởi động bot hàng ngày

1. Open PowerShell as Admin
2. `& "D:\Project\AI OS\REMOTE\claws\nullclaw\zig-out\bin\nullclaw.exe" gateway`
3. Telegram → nhắn "status" → confirm reply

### SOP-BOT-02: Restart khi bot không phản hồi

1. `taskkill /F /IM nullclaw.exe`
2. Chờ 2 giây
3. Khởi động lại theo SOP-BOT-01

### SOP-BOT-03: Update config (system prompt, model, tools)

1. Edit `C:\Users\VUA2HAND\.nullclaw\config.json`
2. Restart bot theo SOP-BOT-02
3. Test bằng tin nhắn Telegram

### SOP-CONFIG-01: Rebuild nullclaw binary

```powershell
powershell -ExecutionPolicy Bypass -File "D:\Project\AI OS\scripts\build-nullclaw.ps1"
```

---

## 🗺️ Roadmap

| Milestone | Target | Status |
|-----------|--------|--------|
| nullclaw Telegram bot LIVE | Mar 2026 | ✅ DONE |
| AstrBot WebUI configured | Mar 2026 | 🟡 IN PROGRESS |
| ClawTask ↔ Bot sync | Apr 2026 | ⚫ PLANNED |
| LightRAG RAG pipeline | Apr 2026 | ⚫ PLANNED |
| Discord + multi-channel | Apr 2026 | ⚫ PLANNED |
| Zalo OA integration | Q2 2026 | ⚫ PLANNED |
| Full autonomous operation | Q2 2026 | ⚫ PLANNED |

---

## 📝 Agent Notes

### Orchestrator_Pro (CEO Assistant)
> Khi CEO nhắn qua Telegram, bot hiện tại connect trực tiếp Gemini 2.0 Flash. Chưa có memory persistence giữa các session — cần setup SQLite memory backend.

### Scrum-Master (COO)
> Quản lý sprint tasks trong file này và ClawTask dashboard (localhost:7474). Priority: TG-001 test live, sau đó TG-003 auto-start.

### Sw-Architect (CTO)
> nullclaw config hiện tại dùng Gemini OpenAI-compatible endpoint. Có thể switch sang Anthropic bất kỳ lúc nào bằng cách update `models.providers` và `agents.defaults.model.primary`.

### Registry-Manager
> REG-007 pending: promote LightRAG (T2 Primary RAG) + cognee (T2 Agent Memory) + crewAI (T2 Orchestration) trong SKILL_REGISTRY.json.
