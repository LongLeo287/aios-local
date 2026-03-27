# [RULE-STORAGE-01] Storage Location Protocol
# Issued by: CEO LongLeo | Date: 2026-03-22 | Status: MANDATORY — Không exception
# Scope: Tất cả agents, Antigravity, Nova, và mọi AI OS operations
# Updated: Removed hardcoded paths per RULE-DYNAMIC-01

---

## RULE: All paths must be RELATIVE or discovered DYNAMICALLY
> See RULE-DYNAMIC-01 for full no-hardcode policy.

---

## ✅ ĐÚNG — Project Files → AI OS Workspace Root

**Workspace root** = thư mục chứa `GEMINI.md` + `CLAUDE.md`.
Không hardcode absolute path. Dùng relative path từ workspace root.

```
<AI_OS_ROOT>/                             ← Workspace root (chứa GEMINI.md + CLAUDE.md)
│
├── brain/
│   ├── shared-context/                   ← SHARED — all agents read/write
│   │   ├── blackboard.json               ← Active task state (single source of truth)
│   │   ├── AGENTS.md                     ← Agent roster & authority
│   │   ├── SOUL.md                       ← Platform identity
│   │   ├── GOVERNANCE.md                 ← Safety anchors & rules
│   │   ├── THESIS.md                     ← Strategy pillars
│   │   └── SKILL_REGISTRY.json           ← All skills index
│   │
│   └── knowledge/
│       └── notes/                        ← CEO notes + RULE files (RULE-*.md)
│
├── corp/
│   ├── departments/                      ← Dept configs (count: see org_chart.yaml)
│   ├── memory/                           ← Agent + dept memory
│   └── org_chart.yaml                    ← Authoritative org structure
│
├── ops/
│   ├── scripts/config.json               ← Service ports + URLs (no hardcoding ports!)
│   ├── runtime/                          ← Ephemeral runtime state
│   └── workflows/                        ← Boot + daily cycle workflows
│
├── tools/                                ← ClawTask, MCP servers
├── plugins/                              ← External vetted plugins
└── channels/                             ← Remote bridges (Telegram, Discord, etc.)
```

---

## 🔒 SYSTEM ONLY — AI Tool Data Directories

Đây là **system data của AI tools** — KHÔNG tạo mới, KHÔNG xóa, KHÔNG di chuyển:

```
$env:USERPROFILE\              ← User home (dynamic — không hardcode username)
├── .gemini\                   ← Antigravity brain, memory, session logs
│   └── antigravity\
│       ├── skills\            ← ĐƯỢC PHÉP: mirror từ <AI_OS_ROOT>/plugins/
│       └── brain\             ← Antigravity internal (artifacts, KI system)
├── .claude\                   ← Claude Code session data, memory
├── .codex\                    ← OpenAI Codex data
├── .nullclaw\                 ← NullClaw agent framework data
└── .ollama\                   ← Ollama model weights (KHÔNG xóa — models lớn!)
```

**Exception duy nhất được phép tại $USERPROFILE:**
- `$env:USERPROFILE\.gemini\antigravity\skills\[plugin]` = mirror từ AI_OS_ROOT/plugins/
- Artifact/brain files của conversation Antigravity (system-generated, tự quản lý)

---

## ❌ CẤM

| Forbidden | Lý do |
|-----------|-------|
| Tạo project files tại `$env:USERPROFILE\` | System territory |
| Hardcode `C:\Users\<username>\` trong scripts | Breaks on different machines |
| Hardcode `D:\<absolute>\` trong rule files | Breaks when path changes |
| Tạo files tại Desktop, Downloads, Documents | Không phải workspace |
| Dùng `ops/runtime/blackboard.json` cho boot | Runtime mirror only |

---

## 🔄 KHI ĐƯỜNG DẪN THAY ĐỔI (Machine Migration)

Xem **RULE-DYNAMIC-01** — Section 4: "Procedure — When System Changes"

Tóm tắt:
1. Cập nhật `ops/scripts/config.json` → `workspace_root`
2. Cập nhật file này (RULE-STORAGE-01) nếu cần thêm context
3. Verify boot sequence paths vẫn resolve đúng

---

*Issued: 2026-03-22 | Storage rule version 2.0 — No hardcoded paths.*
