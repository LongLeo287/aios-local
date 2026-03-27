# NotebookLLM — Full Use Case Map trong AI OS Corp
# Version: 1.0 | Created: 2026-03-18
# Scope: Cross-department applications

---

## Triết lý cốt lõi

NotebookLLM = **AI đọc hộ, tổng hợp hộ, trình bày hộ**.
Upload bất kỳ nguồn nào → đặt câu hỏi → nhận output có citation.
Output: Text / Audio / Quiz / Flashcard / Slide structure / Briefing doc / FAQ / Timeline

---

## Map theo Phòng ban

---

### 🔍 CIV — Content Intake & Vetting

| Task | Cách dùng |
|------|-----------|
| Repo analysis | Upload gitingest digest → "Repo này làm gì? Có conflict với hệ thống không?" |
| Routing decision | "Phòng nào nên nhận repo này?" → nhận routing recommendation |
| Quality report | Auto-generate CIV Verdict Report từ README + source tree |
| Batch evaluation | Upload 10 repos → so sánh, rank, chọn best-fit |

---

### 🧪 R&D — Research & Development

| Task | Cách dùng |
|------|-----------|
| Literature synthesis | Upload 20 papers → "Tóm tắt state-of-the-art về X" |
| Repo comparison | Upload 5 repos → "Framework nào phù hợp nhất cho AI OS?" |
| Technology briefing | Upload docs → generate Briefing Doc cho CEO |
| Experiment design | Upload results → "Rút ra được gì? Bước tiếp theo?" |
| 300+ repo ingest | Import từ Google Sheets → synthesize theo theme |

---

### 📋 Strategy & Planning

| Task | Cách dùng |
|------|-----------|
| Market report | Upload competitor analysis → structured report có citation |
| SWOT analysis | Upload internal docs + market data → brainstorm SWOT |
| Roadmap briefing | Upload meeting notes + backlogs → "Ưu tiên gì nhất?" |
| Investor deck prep | Upload financials + milestones → Briefing doc skeleton |
| Decision memo | Upload options analysis → recommendation với pros/cons |

---

### 📣 Marketing & Content

| Task | Cách dùng |
|------|-----------|
| Podcast creation | Upload research paper → Audio Overview (MP3, 2 hosts) |
| Campaign brainstorm | Upload briefs + references → brainstorm angles |
| Content calendar | Upload brand docs + trends → suggest content plan |
| Case study draft | Upload project notes → structured case study |
| FAQ generation | Upload product docs → customer FAQ |

---

### 📚 OD&L — Learning & Development

| Task | Cách dụng |
|------|-----------|
| Onboarding material | Upload SKILL.md files → structured learning guide |
| Quiz generation | Upload training docs → auto-generate quiz cho agents |
| Flashcard deck | Upload dense knowledge → spaced repetition cards |
| Timeline breakdown | Upload process docs → step-by-step timeline |
| Agent training brief | Upload SOUL.md + corp manual → "Agent cần biết gì để onboard?" |

---

### 🔒 Security GRC

| Task | Cách dùng |
|------|-----------|
| Threat report | Upload scan results → executive summary |
| Policy comparison | Upload 2 security policies → diff + recommendations |
| Incident debrief | Upload incident logs → structured timeline + lessons learned |
| Compliance check | Upload SOPs + standards → "Thiếu gì so với ISO 27001?" |

---

### ⚙️ Engineering & DevOps

| Task | Cách dùng |
|------|-----------|
| Code review brief | Upload PR diffs → structured review summary |
| Architecture docs | Upload codebase digest → generate ADR (Architecture Decision Record) |
| Dependency analysis | Upload package files → "Risk nào trong stack hiện tại?" |
| Migration planning | Upload old + new system docs → migration checklist |

---

### 📞 Client Reception (phòng lễ tân)

| Task | Cách dùng |
|------|-----------|
| Proposal research | Upload client brief + AI OS capabilities → draft proposal |
| Client briefing | Upload conversation history → "Client cần gì nhất?" |
| Onboarding doc | Upload approved proposal → client welcome package |

---

### 🏢 CEO / Executive

| Task | Cách dùng |
|------|-----------|
| Weekly digest | Upload all dept reports → 1-page CEO summary |
| Brainstorm session | Upload context docs → structured brainstorm output |
| Board presentation | Upload KPIs + roadmap → slide structure + talking points |
| Decision support | Upload conflicting options → balanced analysis |

---

## Tool Mapping

| Use Case | Tool chính | Pair với |
|----------|-----------|---------|
| Research synthesis | `open-notebook` (self-hosted) | `gitingest` |
| Google NLM query via agent | `notebooklm-skill` | MCP cluster |
| MCP-native integration | `notebooklm-mcp-cli` | MCP servers |
| Podcast/audio output | `open-notebooklm` | Marketing workflow |
| Bulk automation | `notebooklm-py` patterns | R&D pipeline |

---

## Workflow Tiêu Chuẩn

```
[Input: URL / PDF / Repo / Notes / Reports]
         ↓
    gitingest / doc-parser (convert → text)
         ↓
    open-notebook / NotebookLM
         ↓
    [Query: "Generate report / brainstorm / quiz / podcast / FAQ"]
         ↓
    [Output → destination dept]
```

*Owner: cross-departmental | Managed by: R&D primary | 2026-03-18*
