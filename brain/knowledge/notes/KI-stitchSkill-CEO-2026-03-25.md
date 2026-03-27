# KI Note — arinnem/stitchSkill (CEO's own skill)
# Type: REPO | Source: https://github.com/arinnem/stitchSkill
# CIV Ticket: CIV-2026-03-25-003
# Intake Date: 2026-03-25
# Value Type: SKILL (CRITICAL) — CEO's personal Stitch Wireframe Generator

---

## Summary

**stitchSkill** là Antigravity skill do CEO (arinnem/LongLeo) tự build — tự động tạo wireframe qua Stitch MCP từ tài liệu mô tả phần mềm. **16 screens tự động, không cần click.**

---

## Core Features

| Feature | Mô tả |
|---------|-------|
| 📖 Context extraction | Đọc markdown/docx/txt → trích xuất system context |
| 🎨 Style collection | Screenshots, brand guide, URL reference, hoặc text style |
| 👥 Actor/Journey proposal | Đề xuất actors + journeys → CEO approve trước khi vẽ |
| 🎯 Design System | Colors, fonts, navigation → inject vào mọi screen prompt |
| 📝 Structured prompts | 3-part prompt: Design System + Screen Map + Screen Content |
| 🖼️ Auto-draw | 16 screens liền qua Stitch MCP — không cần click |
| 📊 Project logging | Log toàn bộ trong project folder |

---

## CIV Assessment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Relevance | 10/10 | CEO's own work — directly used in AI OS |
| Security | NONE | Internal CEO project |
| Integration | NONE | Already integrated via Antigravity |
| Value type | SKILL + WORKFLOW |  |

**Verdict:** ✅ APPROVE — Register trong SKILL_REGISTRY + document workflow

---

## Key Insight

Đây là skill bổ sung hoàn hảo cho `google-labs-code/stitch-skills`:
- `stitch-skills` từ Google: low-level design operations
- `stitchSkill` từ CEO: high-level workflow (doc → actors → design system → 16 screens)

**Combined pipeline:** `stitchSkill` → actor approval → `stitch-design` + `stitch-loop` → screens

---

## Action Items

- [ ] Fork/clone arinnem/stitchSkill vào `plugins/stitchSkill/` hoặc `.agents/skills/`
- [ ] Register `stitch-wireframe-generator` trong SKILL_REGISTRY.json
- [ ] Document trong `kho/workflows/` or `ops/workflows/`
- [ ] Wire với `stitch-skills` (enhance-prompt → stitch-design pipeline)

---

*KI Note v1.0 | CIV-2026-03-25-003 | Intake: Antigravity | 2026-03-25*
