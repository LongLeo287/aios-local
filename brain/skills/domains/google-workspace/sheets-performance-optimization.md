---
name: sheets_performance_optimization
display_name: Google Sheets Performance Optimization
description: >
  Advanced optimization patterns for Google Sheets projects at scale.
  Covers batch operations, caching strategies, VLOOKUP alternatives,
  and query optimization to handle large datasets efficiently.
version: 1.0.0
author: LongLeo (adapted for AI OS)
tier: 3
category: performance
domain: google-workspace
tags: [google, sheets, performance, optimization, batch, caching]
cost_tier: economy
accessible_by:
  - Developer
  - QA
dependencies:
  - sheets_skill
load_on_boot: false
promoted_from: D:\GA\Workspaces\LongLeo\.claude\skills\
---

# Google Sheets Performance Optimization

## When to Use
Load when Sheets project has > 1000 rows or slow read/write operations.

## Critical Rules (Always Apply)

```
1. NEVER read/write in a loop — always batch
2. Use getValues() once, process in memory, setValues() once
3. Cache frequently-used data with CacheService (6h max)
4. Use QUERY() formula instead of VLOOKUP for large ranges
5. Freeze headers, avoid merged cells (breaks getDataRange)
```

## Batch Read/Write Pattern

```javascript
// BAD: N API calls
for (let i = 1; i <= 1000; i++) {
  sheet.getRange(i, 1).getValue(); // 1000 calls!
}

// GOOD: 1 API call
const allData = sheet.getDataRange().getValues(); // 1 call
allData.forEach(row => { /* process in memory */ });
```

## CacheService Pattern

```javascript
function getCachedData(key, fetchFn, ttl = 21600) {
  const cache = CacheService.getScriptCache();
  const cached = cache.get(key);
  if (cached) return JSON.parse(cached);

  const data = fetchFn();
  cache.put(key, JSON.stringify(data), ttl);
  return data;
}
```

## VLOOKUP → QUERY Migration

```
// Slow VLOOKUP on 5000 rows
=VLOOKUP(A2, Data!A:Z, 5, FALSE)

// Fast QUERY alternative
=QUERY(Data!A:Z, "SELECT E WHERE A = '"&A2&"'", 0)

// Even faster: INDEX/MATCH with sorted data
=INDEX(Data!E:E, MATCH(A2, Data!A:A, 0))
```

## Performance Checklist (QA)
- [ ] No loops with getRange/getValue inside
- [ ] Single getDataRange() at function start
- [ ] CacheService used for static reference data
- [ ] QUERY/INDEX-MATCH instead of VLOOKUP on > 500 rows
