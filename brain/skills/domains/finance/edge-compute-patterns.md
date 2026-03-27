---
name: edge_compute_patterns
display_name: Edge Computing & Tax Calculation Patterns
description: >
  Patterns for offloading pure computational logic (tax, pricing formulas,
  currency conversion) to edge-compatible environments for zero-latency results.
  Applicable to any e-commerce, fintech, or retail project with calculation needs.
version: 1.0.0
author: LongLeo (adapted for AI OS — tax values removed, patterns generalized)
tier: 3
category: performance
domain: finance
tags: [edge, tax, pricing, calculation, serverless, performance, fintech]
cost_tier: economy
accessible_by:
  - Developer
dependencies: []
load_on_boot: false
promoted_from: D:\GA\Workspaces\LongLeo\.claude\skills\
---

# Edge Computing & Tax/Pricing Calculation Patterns

## When to Use
Load when project needs fast, server-free computation of:
- Tax calculations (VAT, GST, sales tax)
- Pricing formulas (discounts, tiers, bundles)
- Currency conversion
- Shipping fee calculation

## Core Principle

Move pure math functions to the edge — avoid round-trips to main server:
```
Client → Edge Function (instant calculation) → Response
vs.
Client → API Server → Database → Business Logic → Response (slow)
```

## Universal Tax Calculator Pattern

```typescript
// Works at edge (Cloudflare Workers, Vercel Edge, Deno Deploy)
interface TaxConfig {
  rate: number;          // e.g. 0.10 for 10%
  inclusive: boolean;    // is price tax-inclusive?
  currency: string;      // "USD", "VND", "EUR"
  precision: number;     // decimal places
}

function calculateTax(
  subtotal: number,
  config: TaxConfig
): { tax: number; total: number; subtotalExTax: number } {
  let subtotalExTax: number;
  let tax: number;

  if (config.inclusive) {
    subtotalExTax = subtotal / (1 + config.rate);
    tax = subtotal - subtotalExTax;
  } else {
    subtotalExTax = subtotal;
    tax = subtotal * config.rate;
  }

  const round = (n: number) =>
    Math.round(n * 10 ** config.precision) / 10 ** config.precision;

  return {
    subtotalExTax: round(subtotalExTax),
    tax: round(tax),
    total: round(subtotalExTax + tax),
  };
}
```

## Edge Deployment (Cloudflare Workers)

```typescript
export default {
  async fetch(request: Request): Promise<Response> {
    const { subtotal, taxConfig } = await request.json();
    const result = calculateTax(subtotal, taxConfig);
    return Response.json(result, {
      headers: { 'Cache-Control': 'public, max-age=3600' }
    });
  }
};
```

## When NOT to Use Edge
- Complex business rules that need database lookups
- Calculations requiring user session state
- Scenarios needing audit logs (keep on main server)
