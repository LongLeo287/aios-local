# ðŸš€ CLAUDE.md â€” Tiem Nuoc Nho v5 (PRJ-004)
# Version: 1.1 | Updated: 2026-03-16
# Authority: Tier 0 (Project Constitution)
# Location: <AI_OS_ROOT>\projects\PRJ-004\   â—„ Managed by AI OS
# Workspace: D:\Tiem_Nuoc_Nho_v5\

> **THIS IS THE FIRST FILE YOU READ** when working on this project.
> Managed centrally by AI OS. Do NOT move to project folder.

---

## âš¡ BOOT SEQUENCE

```
STEP 1 â”€â”€â–º Read this CLAUDE.md                          [THIS FILE â€” in AI OS\projects\PRJ-004\]
STEP 2 â”€â”€â–º Read AI OS Master                            [<AI_OS_ROOT>\CLAUDE.md]
STEP 3 â”€â”€â–º Validate workspace via Gatekeeper            [gatekeeper.ps1 -CheckID PRJ-004]
STEP 4 â”€â”€â–º Read AI OS AGENTS.md                         [<AI_OS_ROOT>\shared-context\AGENTS.md]
STEP 5 â”€â”€â–º Check Blackboard for pending tasks           [<AI_OS_ROOT>\shared-context\blackboard.json]
STEP 6 â”€â”€â–º Begin work
```

---

## ðŸª PROJECT IDENTITY

| Field | Value |
|---|---|
| **Project ID** | PRJ-004 |
| **Name** | Tiem Nuoc Nho v5 |
| **Type** | POS / Quáº£n lÃ½ Ä‘Æ¡n hÃ ng quÃ¡n nÆ°á»›c |
| **Stack** | React 18 + TypeScript + Vite + Express + Google Apps Script |
| **Backend** | Google Sheets as database, GAS as API layer |
| **Dev URL** | http://localhost:7475 (port 7475 â€” Playwright-accessible) |
| **Start** | `npm run dev` in `D:\Tiem_Nuoc_Nho_v5` |
| **Config** | `<AI_OS_ROOT>\projects\PRJ-004\` |
| **Workflows** | `<AI_OS_ROOT>\projects\PRJ-004\workflows\` |

---

## ðŸ—‚ï¸ WORKSPACE STRUCTURE

```
D:\Tiem_Nuoc_Nho_v5\             â—„ Source code only
â”œâ”€â”€ .clauderules                  â—„ ONLY AI OS file here (Claude Code requirement)
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ components/
â”‚   â”‚   â”œâ”€â”€ Menu.tsx              â—„ Menu grid + item add flow
â”‚   â”‚   â”œâ”€â”€ Cart.tsx              â—„ Cart + checkout + edit modal
â”‚   â”‚   â”œâ”€â”€ CartItemRow.tsx       â—„ Individual cart row
â”‚   â”‚   â”œâ”€â”€ OrderHistory.tsx      â—„ Order management dashboard
â”‚   â”‚   â”œâ”€â”€ Invoice.tsx           â—„ Invoice view
â”‚   â”‚   â””â”€â”€ GlobalQrModal.tsx     â—„ QR payment modal (Momo/Timo)
â”‚   â”œâ”€â”€ context/
â”‚   â”‚   â”œâ”€â”€ CartContext.tsx       â—„ Cart state management
â”‚   â”‚   â”œâ”€â”€ DataContext.tsx       â—„ Orders & menu data (GAS API)
â”‚   â”‚   â”œâ”€â”€ UIContext.tsx         â—„ UI state (FAB, dark mode)
â”‚   â”‚   â””â”€â”€ AuthContext.tsx       â—„ Auth state
â”‚   â””â”€â”€ types.ts                  â—„ Shared TypeScript types
â”œâ”€â”€ DATA/GAS/                     â—„ Google Apps Script source
â”œâ”€â”€ backend/                      â—„ Express server (API proxy)
â””â”€â”€ server.ts                     â—„ Dev server entry point
```

---

## ðŸ”‘ KEY DECISIONS (Locked â€” Do NOT Reverse)

1. **Card tap = instant add** to cart (no popup), quantity 1, default options
2. **`+` button** only appears for items with customizations (`hasCustomizations: true`)
3. **Takeaway/Dine-in** selection happens at CHECKOUT, not per-item
4. **Split dialog** appears when editing a multi-quantity cart item with changed options
5. **No Topping module** â€” customer decided toppings are not needed
6. **GAS = Backend** â€” all data reads/writes go through Google Apps Script URL

---

## âœ… COMPLETED FEATURES

- [x] Menu quick-add (tap card â†’ instant cart)
- [x] `+` button â†’ QuantityModal â†’ CustomizationModal flow
- [x] Edit cart item with Split dialog
- [x] Subtotal always visible (sticky footer)
- [x] Code audit â€” all orphaned states/components removed
- [x] TypeScript: 0 compile errors

---

## âœ… ALL FEATURES COMPLETE

- [x] QR Code checkout integration (GlobalQrModal connected in Cart.tsx L862)
- [x] Order History fast-action buttons (Nháº­n / HoÃ n táº¥t / Há»§y â€” OrderHistory.tsx L221)
- [x] Cart auto-save to localStorage (CartContext.tsx L21)
- [x] TypeScript: 0 compile errors (tsc --noEmit exit 0)

---

## ðŸ¤– AGENT BEHAVIOR FOR THIS PROJECT

- **Language:** Vietnamese for user-facing messages, English for code/comments
- **Brand color:** `#C9252C` (red) â€” use consistently
- **UI framework:** Tailwind CSS + Framer Motion (`motion/react`)
- **Data layer:** `useData()` hook from `DataContext.tsx`
- **Cart operations:** `useCart()` hook from `CartContext.tsx`

---

## âš ï¸ HARD RULES

1. Never modify `DATA/GAS/` scripts without testing on staging sheet
2. Never commit API keys or GAS URLs to git
3. Always run `npx tsc --noEmit` after any TypeScript change
4. Always test on mobile viewport (375px) â€” this is a mobile-first POS

---

*"Every cup of water is an order. Every order is a story. Make the system serve the story."*

