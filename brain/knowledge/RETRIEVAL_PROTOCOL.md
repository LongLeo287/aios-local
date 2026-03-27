---
id: KI-RETRIEVAL-PROTOCOL-001
type: LESSON
domain: [meta, retrieval, performance, accuracy]
created: 2026-03-22
version: 1.0
authority: Antigravity (self-learned from GitNexus + LightRAG)
applies_to: [Antigravity, all agents needing fast data retrieval]
---

# Fast & Accurate Data Retrieval — Operating Protocol

> Học từ: GitNexus (graph code intelligence) + LightRAG (graph-RAG framework)
> Áp dụng: mỗi khi cần tìm dữ liệu trong AI OS Corp hoặc bất kỳ codebase nào

---

## Core Shift in Thinking

| ❌ Cách cũ (chậm, không chính xác) | ✅ Cách mới (nhanh, graph-native) |
|------------------------------------|----------------------------------|
| "Tìm file chứa X" | "Tìm **flow/process** liên quan đến X" |
| Đọc toàn bộ file để hiểu | **Context overview trước** (150 tokens), chi tiết sau |
| Sửa rồi mới nghĩ ảnh hưởng | **Impact analysis trước**, rồi mới sửa |
| Keyword grep trong 100+ files | Domain → CAPABILITY_MAP → jump thẳng |
| Đọc mọi thứ để tìm pattern | Graph traversal: follow edges, không brute-force |

---

## Protocol 1 — TÌM FILE / THÔNG TIN (Find)

```
BƯỚC 1: Phân loại domain trước (30 giây)
  → Là skill/plugin? → CAPABILITY_MAP.md section tương ứng
  → Là workflow? → AI_OS_SYSTEM_MAP.md Section 4
  → Là agent/dept? → AI_OS_SYSTEM_MAP.md Section 2 hoặc AGENTS.md
  → Là shared state? → AI_OS_SYSTEM_MAP.md Section 8

BƯỚC 2: Narrowing (chỉ đọc nếu domain đã rõ)
  → find_by_name với exact pattern (không dùng * nếu biết tên)
  → grep_search với term cụ thể trong folder đúng (không search toàn repo)
  → Không đọc file nếu chưa biết nó có liên quan

BƯỚC 3: Confidence check
  → Confidence cao (domain match rõ) → proceed
  → Confidence thấp (domain mơ hồ) → readAI_OS_SYSTEM_MAP.md trước
  → Không tìm thấy → query: CAPABILITY_MAP decision tree
```

---

## Protocol 2 — HIỂU HỆ THỐNG / CODE (Explore)

Học từ `gitnexus-exploring.md`:

```
ĐÚNG THỨ TỰ:
1. Context overview trước (~150 tokens)
   → AI OS: đọc AI_OS_SYSTEM_MAP.md → biết toàn bộ cấu trúc
   → Codebase: gitnexus://repo/{name}/context → staleness + stats

2. Query concept → tìm flows liên quan
   → GitNexus: gitnexus_query({query: "authentication"})
     → Trả về: processes grouped by execution flow
   → AI OS: grep_search trong folder đúng, không scan everything

3. Context(symbol) → 360° view của 1 element
   → GitNexus: gitnexus_context({name: "validateUser"})
     → Callers (ai gọi nó), Callees (nó gọi ai), Processes (nó thuộc flow nào)
   → AI OS: grep_search(symbol, SearchPath=AI OS root) → xem ai reference đến nó

4. Full trace chỉ khi cần
   → GitNexus: READ gitnexus://repo/{name}/process/{name}
   → AI OS: view_file chỉ những file đã identify ở bước 3
```

**Key rule:** Process/flow trước, file sau. "Nó thuộc workflow nào?" trước "nó ở file nào?"

---

## Protocol 3 — TRƯỚC KHI THAY ĐỔI (Impact Analysis)

Học từ `gitnexus-impact-analysis.md`:

```
PHẢI làm trước mọi thay đổi quan trọng:

gitnexus_impact({target: "X", direction: "upstream"})

Depth interpretation:
  d=1 → WILL BREAK   — direct callers/importers (phải fix ngay)
  d=2 → LIKELY AFFECTED — indirect deps (phải test)
  d=3 → MAY NEED TESTING — transitive effects (monitor)

Risk levels:
  <5 symbols, <2 processes     → LOW     → safe to proceed
  5-15 symbols, 2-5 processes  → MEDIUM  → careful, test after
  >15 symbols hoặc many flows  → HIGH    → plan, announce trước
  Core path (auth, CEO data)   → CRITICAL → CEO approval required

Áp dụng trong AI OS:
  Trước khi sửa org_chart.yaml → ai đọc nó? (d=1: tất cả 21 depts)
  Trước khi sửa blackboard.json → ai writes/reads? (d=1: mọi agent)
  Trước khi xoá plugin → gitnexus_impact hoặc grep_search(plugin_id, SearchPath=AI OS)
  Trước khi sửa SKILL_REGISTRY.json → ai load skill này? (accessible_by[])
```

---

## Protocol 4 — DEBUG / TRACE ROOT CAUSE

Học từ `gitnexus-debugging.md`:

```
Triệu chứng → Flow → Symbol → Root cause

1. Identify symptom (error message, wrong output, missing data)
2. Query flow: "which workflow/process involves this symptom?"
   → GitNexus: gitnexus_query({query: "error symptom text"})
   → AI OS: grep_search("error keyword") in ops/workflows/ + corp/departments/
3. Context on suspect: callers + callees
   → Callers = who triggered the bug
   → Callees = what the bug called (often the real problem)
4. Trace: read only the source files at the node where symptom occurs
5. Fix at root (d=1 of the fix), not symptom

Pattern by symptom type:
  Error message   → query for error text → context on throw site
  Wrong value     → context on function → trace callees for data flow
  Missing data    → find writer (who sets it?) → find reader (who reads it?)
  Stale cache     → find which agent updates it → check rotation schedule
  Silent fail     → find isolation boundary (plugin quarantine? 2-strike?)
```

---

## Protocol 5 — QUERY GRAPH SEMANTICALLY (LightRAG)

Học từ `lightrag_rag_framework.md`:

```
Khi có LightRAG running (localhost:5055):

5 modes (chọn đúng mode = tiết kiệm cost + tăng accuracy):

local   → Biết chính xác entity: "what does knowledge_navigator do?"
global  → Summary/pattern: "what are common patterns across all agents?"
hybrid  → local + global combined
naive   → Quick vector search only (fast, cheap, less accurate)
mix     → BEST for unknown queries: graph + vector + rerank → 95%+ accuracy

Sử dụng:
  Câu hỏi về entity cụ thể → local (cheapest)
  Câu hỏi tổng quan → global
  Câu hỏi không biết category → mix (tốn hơn nhưng chính xác nhất)
  Always enable_rerank=True khi accuracy quan trọng

Entity graph thinking:
  Không nghĩ: "text chunk nào nói về X?"
  Nghĩ: "entity X có relationship gì với Y và Z?"
  → Extract: entities + relationships từ content
  → Query: traverse graph edges, không scan all chunks
```

---

## Protocol 6 — CYPHER GRAPH QUERY (Raw precision)

Học từ `gitnexus-guide.md` và LightRAG Neo4j integration:

```cypher
-- Skill được dùng bởi agents nào?
MATCH (a:Agent)-[:USES]->(s:Skill {id: "security_shield"})
RETURN a.id, a.dept

-- Flow nào gọi function này?
MATCH (f:Function {name: "validate_user"})<-[:CALLS]-(caller)
RETURN caller.name, caller.filePath

-- Chain đầy đủ từ A đến B
MATCH path = (a)-[:CALLS*1..3]->(b:Function {name: "processPayment"})
RETURN [n IN nodes(path) | n.name] AS call_chain

-- Blast radius depth 2
MATCH (target {name: "X"})<-[:DEPENDS_ON*1..2]-(dep)
RETURN dep.name, length(path) AS depth
ORDER BY depth
```

**Dùng cypher khi:** Pattern matching thông thường không đủ chính xác. Raw traversal = deterministic result.

---

## Summary — Decision Tree

```
CẦN THÔNG TIN GÌ?
    │
    ├── Tìm skill/plugin/tool → CAPABILITY_MAP.md (domain section)
    │
    ├── Hiểu hệ thống → AI_OS_SYSTEM_MAP.md (đọc section phù hợp)
    │
    ├── Tìm file cụ thể → find_by_name (exact) hoặc grep_search (keyword trong folder đúng)
    │
    ├── Hiểu code/workflow → Process first: "belongs to which flow?" → then trace
    │
    ├── Trước khi sửa → Impact analysis: d=1 WHO BREAKS, d=2 LIKELY, d=3 MONITOR
    │
    ├── Debug → Symptom → Flow → Context(symbol) → Callees → Root cause
    │
    └── Semantic search (LightRAG on) → mix mode + reranker → 95%+ accuracy
```

---

## Key Numbers

| Metric | Value |
|--------|-------|
| Keyword matching accuracy | ~65% |
| CAPABILITY_MAP lookup | ~90% |
| LightRAG mix mode | ~95% |
| LightRAG + reranker | ~97% |
| GitNexus graph query | ~95% (code) |
| Cypher direct traversal | ~99% (deterministic) |
| Context overview cost | ~150 tokens |
| Full file read cost | 500-5000 tokens |
| **Savings using Protocol 1-3** | **60-80% fewer tokens** |

---

*Retrieval Protocol v1.0 | 2026-03-22*  
*Learned from: GitNexus (gitnexus-exploring, gitnexus-impact-analysis, gitnexus-debugging, gitnexus-guide) + LightRAG KI*  
*Applied by: Antigravity + all dept head agents*
