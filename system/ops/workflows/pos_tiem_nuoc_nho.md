# Department: operations
---
description: POS Tiá»‡m NÆ°á»›c Nhá» v5 â€” workflow cho má»i tÃ¡c vá»¥ phÃ¡t triá»ƒn vÃ  maintain
project_id: PRJ-003
workspace: d:\Tiem_Nuoc_Nho_v5
registered: 2026-03-14
---

# POS Tiá»‡m NÆ°á»›c Nhá» v5 â€” Development Workflow

## Boot Sequence (before any POS task)

1. Read `d:\Tiem_Nuoc_Nho_v5\.agent\CLAUDE.md` for full project context
2. Run `npx tsc --noEmit` to verify current build status
3. Check branch: confirm working on the correct feature area

## Architecture Quick Reference

| Layer | Files | Notes |
|-------|-------|-------|
| UI | `src/components/*.tsx` | React + Tailwind v4 |
| State | `src/context/*.tsx` | Cart, Data, Auth contexts |
| Types | `src/types.ts` | Shared interfaces |
| GAS | External Google Apps Script | Webhook â†’ Sheets |

## Standard Dev Loop

```
1. Make change to component
2. npx tsc --noEmit          â† verify types compile
3. npm run dev               â† verify visual result
4. Fix any lint warnings     â† Tailwind v4 class names
```

## Tailwind v4 Class Mapping (common mistakes)

| Old (v3) | New (v4) |
|----------|----------|
| `flex-shrink-0` | `shrink-0` |
| `flex-grow` | `grow` |
| `bg-gradient-to-r` | `bg-linear-to-r` |
| `z-[60]` | `z-60` |
| `z-[100]` | `z-100` |

## Key Business Logic Files

- **Cart.tsx** â€” branch selector, order form, QR payment interception
  - `BRANCHES` const at top of file (edit for actual branch names)
  - `handleCheckout` intercepts for QR payment
  - Submit requires: `tableNumber` + `branch` (both non-empty)
- **GlobalQrModal.tsx** â€” VietQR integration
  - MoMo: BIN `970454`, account `0769284483`
  - Timo: BIN `963388`, account `8007041038207`
- **CartItemRow.tsx** â€” compact item card (~70px height)

## Handoff to Claude Code

When delegating a POS coding task:

```json
{
  "task_payload": {
    "workspace_id": "PRJ-003",
    "workspace_path": "d:\\Tiem_Nuoc_Nho_v5",
    "task_file": "d:\\Tiem_Nuoc_Nho_v5\\.agent\\tasks\\[task-name].md"
  }
}
```

Update `<AI_OS_ROOT>\shared-context\blackboard.json` accordingly.

## Active Skills for This Project

- `ui-ux-pro-max` â€” loaded from `.agent/skills/`
- `pos_event_sourcing_auditor` â€” available in AI OS `skills/domains/pos/`

