# pos_dev_workflow.md â€” POS Feature Development SOP
# Managed by: <AI_OS_ROOT>\projects\PRJ-004\workflows\

## Phase 1: RESEARCH

```
1. Read CLAUDE.md â†’ check KEY DECISIONS before touching existing code
2. Read the target file top-to-bottom
3. Identify: Which hooks? Which context? Which child components?
```

## Phase 2: PLAN

```xml
<thought>
  Intent: [what this feature does]
  Files to modify: [list]
  Risks: [what could break]
  Test plan: [how to verify]
</thought>
```

## Phase 3: EXECUTE

For every file modified:
1. Read file first
2. Make change
3. `npx tsc --noEmit --skipLibCheck` â†’ must stay at 0 errors
4. Check `http://localhost:3000` â†’ visual pass

**Component Rules:**
- New state: declare after existing useState calls
- New handlers: `useCallback` with correct deps
- New JSX: mobile-first (375px), dark mode variants
- Animations: `<motion.div>` + `AnimatePresence`

## Phase 4: QA (5-Point)

| # | Check |
|---|---|
| 1 | Correctness â€” does it do what was requested? |
| 2 | Regression â€” did existing features break? |
| 3 | Mobile â€” works on 375px? |
| 4 | Dark Mode â€” looks correct? |
| 5 | TypeScript â€” zero errors? |

## Phase 5: RECEIPT (MANDATORY â€” Auto-Write After Every Feature)

> This step is NOT optional. Every completed feature generates a receipt.
> Receipts feed the AI OS Learning Cycle â†’ knowledge base.

### Receipt File Naming
```
<AI_OS_ROOT>\telemetry\receipts\
PRJ004_YYYYMMDD_NNN_<feature_slug>.json
Example: PRJ004_20260316_003_qr_checkout.json
```

### Receipt JSON Schema
```json
{
  "receipt_id": "PRJ004-YYYYMMDD-NNN",
  "project_id": "PRJ-004",
  "project_name": "Tiem Nuoc Nho v5",
  "timestamp": "<ISO 8601>",
  "executed_by": "Antigravity | Claude Code",
  "task_type": "FEATURE | REFACTOR | BUGFIX | INFRASTRUCTURE",
  "task_title": "<one-line description>",

  "context": "<why this was needed>",

  "changes": {
    "<filename>": ["<change 1>", "<change 2>"]
  },

  "verification": {
    "typescript_errors_before": 0,
    "typescript_errors_after": 0,
    "method": "npx tsc --noEmit --skipLibCheck",
    "result": "EXIT_CODE_0"
  },

  "outcome": "SUCCESS | PARTIAL | FAILURE",
  "notes": "<lessons, caveats, context for future agents>",

  "patterns_discovered": [
    "<reusable pattern or lesson learned>"
  ],

  "knowledge_candidate": true,
  "knowledge_tags": ["<tag1>", "<tag2>", "pos"]
}
```

### Also update CLAUDE.md
Move the completed feature from `PENDING FEATURES` to `COMPLETED FEATURES` in:
`<AI_OS_ROOT>\projects\PRJ-004\CLAUDE.md`



---

## POS Code Patterns

### New Modal
```tsx
// State
const [showModal, setShowModal] = useState(false)
// Wrapper: fixed inset-0 bg-black/40 backdrop-blur-sm z-50
// Sheet: rounded-t-[40px] w-full max-w-md
```

### Order History action
```tsx
const { updateOrderStatus } = useData()
await updateOrderStatus(orderId, newStatus)
// Toast on success/failure
```

### GAS API call
```typescript
const res = await fetch(`${appsScriptUrl}?action=getOrders`)
const data = await res.json()
if (data.result !== 'success') throw new Error(data.error)
```

