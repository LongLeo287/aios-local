# 📋 REPO ANALYSIS: paperclipai/paperclip
**Date:** 2026-03-14
**Analyst:** Antigravity (Architect)
**Status:** LEARN (Không clone — học patterns)

---

## 🔗 Source
- **URL:** https://github.com/paperclipai/paperclip
- **Homepage:** https://paperclip.ing
- **Stars:** 22,485 ⭐ | **Forks:** 2,906
- **Language:** TypeScript | **Size:** 6.4 MB
- **Last Updated:** 2026-03-14

---

## 🎯 Mục đích (Purpose)
> "Open-source orchestration for zero-human companies"

Paperclip là một **Control Plane cho doanh nghiệp vận hành bằng AI Agent** — không cần con người giám sát từng bước.
Mục tiêu V1: Quản lý Agent Tasks, Budget, Activity Logs, Approval Gates, và Company-scoped data.

---

## 🏗️ Kiến trúc (Architecture)

```
paperclip/
├── server/        ← Express REST API, orchestration services
├── ui/            ← React + Vite (Board UI)
├── packages/
│   ├── db/        ← Drizzle schema, PGlite migrations
│   ├── shared/    ← Types, constants, validators, API paths
│   ├── adapters/  ← External integrations
│   └── adapter-utils/
├── skills/        ← Agent skill definitions (giống AI OS!)
├── doc/           ← GOAL.md, PRODUCT.md, SPEC.md, DATABASE.md
├── tests/
├── Dockerfile
└── AGENTS.md      ← Hướng dẫn rõ ràng cho AI agents
```

---

## ⚙️ Tech Stack
| Layer | Technology |
|---|---|
| Backend | Node.js + Express + TypeScript |
| Frontend | React + Vite |
| Database | Drizzle ORM + PGlite (embedded PostgreSQL) |
| Build | pnpm mono-repo |
| Testing | Vitest |
| Deploy | Docker |
| AI Config | `.claude/` config, `AGENTS.md` |

---

## 💡 Patterns Đáng Học (Key Learnings)
1. **AGENTS.md Pattern:** Cấu trúc hướng dẫn rõ ràng cho AI contributors — tương tự `agent_behavior.md` của AI OS.
2. **Control Plane Design:** Single-assignee task model + Atomic checkout + Budget hard-stop — tham khảo cho Orchestration.
3. **Company-scoped Multi-tenancy:** Mọi entity đều scoped theo Company — pattern tốt cho multi-project AI OS.
4. **Skills Directory:** Có `skills/` folder tổ chức agent capabilities — xác nhận hướng đi của AI OS.
5. **Verification Loop:** TypeCheck → Test → Build trước khi handoff.

---

## 🔴 Verdict (Quyết định)

| Tiêu chí | Đánh giá |
|---|---|
| Là tool cần chạy? | Có, nhưng phức tạp (PostgreSQL, Docker, pnpm) |
| Thay thế được AI OS không? | Không — khác mục tiêu |
| Cần code của nó? | Không |
| Patterns đáng học? | ✅ **Rất cao** |
| **Quyết định:** | **LEARN — Không clone** |

### Lý do không clone:
- Phụ thuộc nặng: PostgreSQL, Docker, full pnpm mono-repo
- Mục đích khác: Paperclip = product cho công ty; AI OS = hệ điều hành cá nhân
- Kích thước: 6.4 MB + 424 KB lock file

### Cần học gì:
- `AGENTS.md` → Xem như reference chuẩn cho AI Governance doc
- Control plane mental model → Áp dụng cho Orchestration SOP
- Multi-tenant scoping → Tham khảo khi mở rộng registry.json
