---
id: KI-2026-03-22-design-foundation
type: REFERENCE
domain: design
dept: all
created: 2026-03-22
foundation: true
tags: ['design', 'ui', 'ux', 'css', 'clawtask', 'dashboard']
---

# AI OS Corp — UI/UX Design Standards

## AI OS Corp Design System

### Color Palette (ClawTask Dashboard)
- Background: `#070710` (deep dark)
- Surface: `#0d0d1c`
- Accent: `#c8b5ff` (purple, `--sidebar-accent`)
- Online: `#06d6a0` (green, `--col-review`)
- Warning: `#ffd166` (yellow, `--col-inprogress`)
- Blocked: `#ff6b6b` (red, `--col-blocked`)

### Typography
- Display: `Space Grotesk` (headers)
- Monospace: `Space Mono` (code, metadata)
- UI: `Segoe UI` fallback

### Component Patterns
- CSS variables for all colors (no hardcoded hex in JS)
- `var(--panel-padding)` for consistent spacing
- `var(--border)` for surface borders

### Key UI Files
- `tools/clawtask/index.html` — main CEO dashboard (5000+ lines)
- All panels: ctrl-panel pattern with ctrl-header

---
*Foundation KI — created 2026-03-22*
