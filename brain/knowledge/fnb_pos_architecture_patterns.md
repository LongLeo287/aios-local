# F&B POS System — Tiệm Nước Nhỏ v5 Architecture Patterns

**Project ID:** PRJ-003/004 | **Stack:** React 19 + Vite + GAS + Google Sheets

> Reusable architectural patterns from a production F&B POS system.
> Applicable to any F&B order management, café POS, or small business web app.

---

## 1. Architecture Overview

```
Frontend (React 19 + Vite)          Backend (Google Apps Script)
─────────────────────────           ────────────────────────────
CartContext.tsx                      Main.gs (API router)
  └→ DataContext.tsx ──POST──────→  OrderService.gs
       (appsScriptUrl)              InventoryService.gs
                                    StaffService.gs
                                    DashboardService.gs
                                         │
                                    Google Sheets (12 sheets)
```

**Key innovation:** No dedicated backend server needed. GAS acts as the API layer,
and Google Sheets is the database. Zero hosting cost. Works on mobile via PWA.

---

## 2. State Management Pattern (React Contexts)

| Context | Responsibility |
|---------|---------------|
| `CartContext.tsx` | Cart state, auto-save to localStorage |
| `DataContext.tsx` | All GAS CRUD operations, menu/order data |
| `AuthContext.tsx` | Staff login, role-based permissions |
| `UIContext.tsx` | Modal state, toast notifications |
| `ThemeContext.tsx` | Dark/light mode |

**Pattern: Auto-save Cart to survive page refresh**
```tsx
// CartContext.tsx — prevents F5 data loss
const [cart, setCart] = useState<CartItem[]>(() => {
  const saved = localStorage.getItem('cart_autosave');
  return saved ? JSON.parse(saved) : [];
});

useEffect(() => {
  localStorage.setItem('cart_autosave', JSON.stringify(cart));
}, [cart]);
```

---

## 3. GAS Backend Pattern (Serverless API Router)

```javascript
// Main.gs — single entry point
function doPost(e) {
  const payload = JSON.parse(e.postData.contents);
  const action  = payload.action;

  const routes = {
    'getOrders':             () => getOrdersData(),
    'createOrder':           () => createNewOrder(payload),
    'updateOrderStatus':     () => updateOrderStatus(payload),
    'deleteOrder':           () => deleteOrder(payload),
    'updateInventory':       () => updateInventoryItem(payload),
    'createNhapKho':         () => createNhapKho(payload),
    'processOrderInventory': () => processOrderInventory(payload),
  };

  if (routes[action]) {
    return ContentService.createTextOutput(
      JSON.stringify({ result: 'success', data: routes[action]() })
    ).setMimeType(ContentService.MimeType.JSON);
  }
  return errorResponse('Unknown action: ' + action);
}
```

---

## 4. Order Lifecycle (Event Sourcing Pattern)

```
[Chờ xử lý]  →  [Đang làm]  →  [Hoàn thành]  →  Finance logged
      │                              │                  │
      └─────────────────→  [Đã hủy] ┘         inventory deducted
                                                (via DINH_LUONG matrix)
```

**14-column ORDERS sheet schema:**
```
A: ORDER_ID  B: TIMESTAMP  C: TABLE_NO  D: ITEMS(JSON)
E: SUBTOTAL  F: DISCOUNT   G: VAT       H: THANH_TIEN
I: TRANG_THAI  J: THANH_TOAN  K: CUSTOMER  L: PHONE
M: NOTES  N: PAYMENT_STATUS
```

---

## 5. Inventory Deduction via Recipe Matrix (DINH_LUONG)

```
ORDERS.ITEMS ──→ DINH_LUONG lookup ──→ NGUYEN_LIEU deduction

                DINH_LUONG sheet:
                ma_mon | ten_mon | ma_nl | ten_nl | dinh_luong
                CF01   | Cà phê  | NL001 | Hạt cà phê | 18 (gram)

When order "Hoàn thành":
  processOrderInventory({type: 'deduct'})
  → Reads ITEMS from ORDERS
  → Looks up DINH_LUONG for each menu ID
  → updateInventoryItem({ma_nl, quantityChange: -dinh_luong * qty})

When order "Đã hủy":
  processOrderInventory({type: 'refund'})
  → Same flow with positive quantityChange (restore)
```

**Safety:** Throws error if `ton_kho < 0` — never allows negative inventory.

---

## 6. Vietnamese Tax Logic (HKD — Hộ Kinh Doanh)

```javascript
// Smart progressive tax for small businesses in Vietnam
const NGUONG_THUE = 500_000_000;  // 500M VND/year threshold
const THUE_SUAT  = 0.039;          // 3.9% = 2.4% VAT + 1.5% PIT

// Only applies above threshold, and only on the excess amount
if (doanhThuNam > NGUONG_THUE) {
  thueMon = Math.round(thanhTien * THUE_SUAT);
} else if (doanhThuNam + thanhTien > NGUONG_THUE) {
  const phanVuot = doanhThuNam + thanhTien - NGUONG_THUE;
  thueMon = Math.round(phanVuot * THUE_SUAT);
}
doanhThuNam tracked via DASHBOARD!B2 cell
```

---

## 7. QR Payment Integration (VietQR)

```tsx
// GlobalQrModal.tsx — supports MoMo and Timo
// VietQR API: no backend needed, generate inline QR

const accounts = {
  momo: { number: '0769284483', bank: 'MM' },
  timo: { number: '8007041038207', bank: 'TIMO' }
};

// Cart.tsx trigger pattern:
const [showQr, setShowQr] = useState(false);
// After order submit with 'Chuyển khoản':
{showQr && <GlobalQrModal isOpen={showQr} onClose={() => setShowQr(false)} />}
```

---

## 8. Design System Tokens

| Token | Value |
|-------|-------|
| Brand red | `#C9252C` |
| Dark background | `bg-black / bg-stone-950` |
| Cards | `rounded-2xl border-stone-100 dark:border-stone-800` |
| CSS framework | Tailwind CSS v4 |
| Animation | Framer Motion (`motion/react`) |
| Icons | Lucide React |
| Chart | Recharts + D3 |
| **CRITICAL** | Use `bg-linear-to-r` NOT `bg-gradient-to-r` in Tailwind v4 |

---

## 9. Multi-Role Auth Pattern

```
Roles: 'staff' | 'manager'

Manager only:
  - deleteOrder()
  - Access to MenuManager.tsx (menu CRUD)
  - Access to FinanceDashboard.tsx
  - Salary/payroll management

Staff:
  - Order taking, status updates
  - Inventory view (read-only)
  - Own timesheet only
```

---

## 10. Real-Time Sync (WebSocket)

```javascript
// server.ts — Vite + Express hybrid server on port 3000
// When new order arrives:
wss.broadcast({ type: 'NEW_ORDER_NOTIFICATION', payload: order });

// Frontend subscribes:
// All tabs open on the POS auto-refresh order list
// Critical for multi-cashier scenarios
```

---

## 11. Key File Sizes (as reference)

| Component | Size | Notes |
|-----------|------|-------|
| `StaffView.tsx` | 171KB | All-in-one staff dashboard |
| `Menu.tsx` | 60KB | Full menu catalog + search |
| `Cart.tsx` | 58KB | Order form + QR payment |
| `DataContext.tsx` | 24KB | All GAS integration |
| `OrderService.gs` | 16KB | Full order CRUD + finance |
| `SetupService.gs` | 24KB | Sheet initialization scripts |

---

## Applicable Patterns for AI OS

1. **GAS as serverless backend** — Zero cost API tier for Vietnamese small businesses
2. **Recipe matrix deduction** — Reusable for any F&B inventory system
3. **Progressive tax calculation** — HKD tax logic for Vietnamese sole traders
4. **Auto-save Cart pattern** — `localStorage` + `useEffect` F5-proof cart
5. **Context separation** — 5 contexts, each owns exactly one domain
6. **Role-based POS** — staff/manager split without external auth providers
