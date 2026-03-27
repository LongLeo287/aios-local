# KI-REFERENCE-MISC-01 — Miscellaneous Reference Notes
**Nguồn:** gitagent, wtfjs, gitignore, agentql, tinyfish-cookbook, archon, ag-live-code, seeaifirst, pattern-craft, plotly.js, zixfelw/ag-live-code
**Ngày:** 2026-03-23 | **Verdict:** REFERENCE — quick notes per repo

---

## agentql (tinyfish-io) — GraphQL-like Web Query

### Pattern: Structured Web Extraction
```python
# Thay vì parse HTML manually:
from agentql import query

# Define structure với GraphQL-like syntax
result = query("""
{
    products {
        name
        price
        rating
        in_stock
    }
}
""", url="https://shop.example.com")
```
**AI OS:** Firecrawl đã cover. Biết pattern này nếu cần structured extraction ngoài Firecrawl.

---

## Archon (coleam00) — AI OS Reference Architecture

### Archon OS Structure (học từ)
```
Archon/
├── knowledge/      # Persistent knowledge base (AI OS: brain/)
├── tasks/          # Task queue (AI OS: ClawTask)
├── agents/         # Agent definitions (AI OS: brain/agents/)
├── tools/          # Tool wrappers (AI OS: tools/)
└── memory/         # Memory layer (AI OS: Mem0 + LightRAG)
```
**Takeaway:** AI OS Corp cấu trúc tương đồng Archon. Validated approach. No changes needed.

---

## TinyFish Cookbook (tinyfish-io) — n8n + AgentQL Patterns

### n8n Workflow Patterns cho AI OS
```
Trigger: Webhook hoặc Schedule
   ↓
HTTP Request Node → Firecrawl API
   ↓
Code Node → Process data (Python/JS)
   ↓  
OpenAI/Claude Node → Analyze
   ↓
Slack/Email Node → Notify
```
**AI OS ứng dụng:** DEFER Phase 6 — n8n as automation layer cho recurring Corp tasks.

---

## wtfjs (denysdovhan) — JavaScript Edge Cases

### Top AI OS–relevant JS quirks to remember:
```javascript
// KNOW THESE TO AVOID BUGS:

// 1. typeof null === 'object'  (NOT 'null'!)
typeof null === 'object'  // true — always use `=== null` check

// 2. NaN is not equal to itself
NaN === NaN  // false — use Number.isNaN()

// 3. String + Number
'5' + 3    // '53' (string concat, NOT 8)
'5' - 3    // 2   (coercion to number for -)

// 4. Array sort is alphabetical by default
[1, 10, 9, 2].sort()      // [1, 10, 2, 9] — WRONG!
[1, 10, 9, 2].sort((a,b) => a-b)  // [1, 2, 9, 10] — correct

// 5. 0.1 + 0.2 !== 0.3
0.1 + 0.2 === 0.3  // false → use toFixed() or decimal libraries
```
**AI OS:** Apply khi agent writes JavaScript. framework-standards skill should reference these.

---

## gitignore (github/gitignore) — Templates

### Dùng khi tạo project mới:
```bash
# Node.js project
curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Node.gitignore

# Python project
curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore

# Combined (Node + Python)
wget https://www.toptal.com/developers/gitignore/api/node,python,macos,windows

# AI OS specific ignores (add manually):
echo "ops/secrets/\n*.env\nbrain/private/\ntelemetry/logs/*.log" >> .gitignore
```

---

## pattern-craft (megh-bari) — CSS Patterns

Sử dụng trực tiếp tool web (không clone repo):
```
URL: https://patterncraft.fun
→ Chọn pattern → Copy CSS → Paste vào stylesheet
```
Patterns: Dots, Lines, Crosshatch, Waves, Hexagons, Triangles...

---

## plotly.js — Data Visualization

### Khi AI OS cần chart (dùng CDN, không clone):
```html
<script src="https://cdn.plot.ly/plotly-2.30.0.min.js"></script>
<script>
Plotly.newPlot('myDiv', [{
    x: dates,
    y: kpi_values,
    type: 'scatter',
    mode: 'lines+markers',
    name: 'AI OS KPIs'
}], {
    title: 'AI OS Corp KPI Dashboard',
    template: 'plotly_dark'
});
</script>
```
**AI OS:** Dùng cho KPI visualization dashboard (Dept 9 Analytics).

---

## ag-live-code (zixfelw — VN dev)

Live code viewer tích hợp với Antigravity — agent có thể stream code thay đổi real-time.
**Status:** Track repo — evaluate khi cần real-time code collaboration feature.

*KI Note v1.0 | 2026-03-23 | Consolidated misc references*
