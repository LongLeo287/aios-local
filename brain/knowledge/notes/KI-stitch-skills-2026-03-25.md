# KI Note — google-labs-code/stitch-skills
# Type: REPO | Source: https://github.com/google-labs-code/stitch-skills
# CIV Ticket: CIV-2026-03-25-002
# Intake Date: 2026-03-25
# Value Type: SKILLS (CRITICAL) — Google official Stitch agent skills

---

## Summary

**stitch-skills** là repo chính thức từ Google Labs chứa các agent skills cho Stitch MCP. 7 skills sẵn sàng dùng với `npx skills add`.

---

## Available Skills

| Skill | Mô tả | Relevance |
|-------|-------|-----------|
| `stitch-design` | Unified entry point — prompt enhancement + design system + Stitch MCP | ⭐⭐⭐ CRITICAL |
| `stitch-loop` | Multi-page website từ 1 prompt | ⭐⭐⭐ CRITICAL |
| `design-md` | Tạo DESIGN.md từ Stitch project | ⭐⭐⭐ HIGH |
| `enhance-prompt` | Vague → polished Stitch-optimized prompt | ⭐⭐⭐ HIGH |
| `react-components` | Stitch screens → React component systems | ⭐⭐ HIGH |
| `remotion` | Walkthrough videos từ Stitch project | ⭐ MED |
| `shadcn-ui` | shadcn/ui integration expert | ⭐⭐ MED |

---

## Install

```bash
# Install all Stitch skills globally
npx skills add google-labs-code/stitch-skills --skill stitch-design --global
npx skills add google-labs-code/stitch-skills --skill stitch-loop --global
npx skills add google-labs-code/stitch-skills --skill design-md --global
npx skills add google-labs-code/stitch-skills --skill enhance-prompt --global
```

---

## CIV Assessment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Relevance to AI OS | 10/10 | CEO đang dùng Stitch MCP |
| Security risk | NONE | Official Google source |
| Integration effort | LOW | npx install |
| Value type | SKILLS |  |

**Verdict:** ✅ APPROVE — Install tất cả, đặc biệt `stitch-design` + `stitch-loop` + `enhance-prompt`

---

## Action Items

- [ ] Run: `npx skills add google-labs-code/stitch-skills --skill stitch-design --global`
- [ ] Run: `npx skills add google-labs-code/stitch-skills --skill stitch-loop --global`
- [ ] Run: `npx skills add google-labs-code/stitch-skills --skill enhance-prompt --global`
- [ ] Run: `npx skills add google-labs-code/stitch-skills --skill design-md --global`
- [ ] Add entries to `brain/shared-context/SKILL_REGISTRY.json`
- [ ] Register in `kho/plugins/registry.json`

---

*KI Note v1.0 | CIV-2026-03-25-002 | Intake: Antigravity | 2026-03-25*
