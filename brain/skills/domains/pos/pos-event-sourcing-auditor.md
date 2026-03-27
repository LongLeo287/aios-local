---
name: pos_event_sourcing_auditor
display_name: POS Event Sourcing Auditor
description: >
  Enforces Event Sourcing patterns in Point-of-Sale systems.
  Each transaction (order, payment, refund, cancellation) is logged
  as an immutable event rather than mutating current state.
  For any project implementing POS, retail, or transaction-heavy systems.
version: 1.0.0
author: LongLeo (adapted for AI OS)
tier: 3
category: architecture
domain: pos
tags: [pos, event-sourcing, retail, transactions, audit, immutable-log]
cost_tier: standard
accessible_by:
  - QA
  - Developer
dependencies: []
load_on_boot: false
promoted_from: D:\GA\Workspaces\LongLeo\.claude\skills\
---

# POS Event Sourcing Auditor

## When to Use
Load for projects involving:
- Point-of-Sale systems
- Retail order management
- Any system where transaction history must be immutable

## Core Principle

```
WRONG: Mutate current state (dangerous for auditing)
  orders[id].status = "CANCELLED"  ← destroys history

CORRECT: Append immutable events (Event Sourcing)
  events.append({ type: "ORDER_CANCELLED", orderId, reason, timestamp })
  // Current state = sum of all events
```

## Standard Event Schema

```typescript
interface PosEvent {
  event_id: string;        // UUID
  event_type: PosEventType; // enum
  aggregate_id: string;    // order_id, session_id, etc.
  timestamp: string;       // ISO 8601
  actor: string;           // staff_id or "SYSTEM"
  payload: Record<string, unknown>;
  version: number;         // event sequence number
}

type PosEventType =
  | 'ORDER_CREATED'
  | 'ITEM_ADDED'
  | 'ITEM_REMOVED'
  | 'ORDER_CONFIRMED'
  | 'PAYMENT_RECEIVED'
  | 'ORDER_CANCELLED'
  | 'REFUND_ISSUED'
  | 'SHIFT_OPENED'
  | 'SHIFT_CLOSED';
```

## Audit Rules (QA Checklist)

- [ ] Every state change has a corresponding event record
- [ ] Events are append-only (no UPDATE or DELETE on event log)
- [ ] Each event has a unique, sequential version number per aggregate
- [ ] Payment events include amount, currency, method
- [ ] Cancellation events include cancellation reason
- [ ] Shift events include staff_id and cash reconciliation

## Replay Pattern (Reconstruct Current State)

```typescript
function replayOrder(orderId: string, events: PosEvent[]): OrderState {
  return events
    .filter(e => e.aggregate_id === orderId)
    .sort((a, b) => a.version - b.version)
    .reduce(applyEvent, initialOrderState());
}
```
