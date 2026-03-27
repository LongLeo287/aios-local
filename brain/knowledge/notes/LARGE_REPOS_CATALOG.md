# 📚 Large Repos Catalog — Clone On Demand
# Version: 1.0 | 2026-03-25
# Purpose: Các repo lớn không clone ngay — agent/dept lấy lệnh clone khi cần
# Path: brain/knowledge/notes/LARGE_REPOS_CATALOG.md

---

## Cách sử dụng

> Agent hoặc phòng ban: Tìm repo phù hợp → chạy lệnh clone → thực hiện dự án → xóa sau khi xong (hoặc giữ lại nếu cần tiếp)

```powershell
# Clone về thư mục project cụ thể
# Thay <PROJECT_DIR> bằng tên dự án đang làm

git clone --depth 1 <URL> "D:\AI OS CORP\AI OS\plugins\github-repos\<REPO>"
```

---

## Catalog

| Repo | Dept chủ | Tag | Lý do clone |
|------|----------|-----|-------------|
| `next.js` | Engineering | `FRONTEND` | Khi build web app cho AI OS |
| `excalidraw` | Design / R&D | `UI-TOOL` | Khi cần source code diagram / whiteboard tool |
| `posthog` | Analytics / Ops | `ANALYTICS` | Khi cần self-hosted analytics pipeline |
| `plotly.js` | Data / HUD | `VISUALIZATION` | Khi build dashboard charts |
| `trivy` | Security | `SECURITY` | Khi cần container & secret scanning |
| `developer-roadmap` | Training | `KNOWLEDGE` | Khi onboard agents / cần skill matrix |
| `openai-cookbook` | R&D | `AI-PATTERNS` | Khi research LLM integration patterns |
| `anime.js` | Design / Frontend | `ANIMATION` | Khi build animated UI |
| `agents-course` | Training / R&D | `AI-EDUCATION` | Khi training agents về LLM concepts |
| `gitignore` | Core / DevOps | `TEMPLATE` | Khi setup repo mới |
| `public-apis` | R&D / Integration | `INTEGRATION` | Khi cần tích hợp external APIs |

---

## Chi tiết từng repo

---

### 🔷 next.js — Vercel
**Dept:** Engineering | Product | Frontend
**Size:** ~1.2 GB | **Stars:** 130k+
**Khi nào dùng:** Build web apps, dashboards, frontend cho dự án AI OS Corp

```powershell
# Dùng khi: Build web UI cho AI OS dashboard, customer portal, product frontend
git clone --depth 1 https://github.com/vercel/next.js.git `
    "D:\AI OS CORP\AI OS\plugins\github-repos\next.js"
```

**AI OS Impact:**
- HUD v3 → Next.js real-time dashboard
- Corp dashboard → web interface cho 21 depts
- Product page / landing page

---

### 🔷 excalidraw — Excalidraw Team
**Dept:** Design | R&D | Product
**Size:** ~500 MB | **Stars:** 95k+
**Khi nào dùng:** Whiteboard tool, diagram tool, system architecture drawing

```powershell
# Dùng khi: Cần tool vẽ diagram cho dự án AI OS, system design, wireframe alternative
git clone --depth 1 https://github.com/excalidraw/excalidraw.git `
    "D:\AI OS CORP\AI OS\plugins\github-repos\excalidraw"
```

**AI OS Impact:**
- Thay thế Stitch cho system architecture diagrams
- Board brainstorm nội bộ cho các phòng ban
- Self-hosted lightweight alternative

---

### 🔷 posthog — PostHog
**Dept:** Analytics | Ops | Product
**Size:** ~800 MB | **Stars:** 24k+
**Khi nào dùng:** Self-hosted analytics, event tracking, funnel analysis

```powershell
# Dùng khi: Cần analytics pipeline cho AI OS products, track user events
git clone --depth 1 https://github.com/posthog/posthog.git `
    "D:\AI OS CORP\AI OS\plugins\github-repos\posthog"
```

**AI OS Impact:**
- Track AI OS usage metrics (daily corp cycle, agent calls, skill usage)
- Replace external analytics với self-hosted
- Wire với B5 system_pulse.py

---

### 🔷 plotly.js — Plotly
**Dept:** Data | Analytics | HUD
**Size:** ~400 MB | **Stars:** 17k+
**Khi nào dùng:** Charts, graphs, data visualization cho dashboards

```powershell
# Dùng khi: Build charts cho HUD, KPI dashboard, corp cycle analytics
git clone --depth 1 https://github.com/plotly/plotly.js.git `
    "D:\AI OS CORP\AI OS\plugins\github-repos\plotly.js"
```

**AI OS Impact:**
- HUD v3 charts → KPI scoreboard visualization
- Dept health graphs
- CIV pipeline metrics charts

---

### 🔷 trivy — Aqua Security
**Dept:** Security | DevOps | CIV Pipeline
**Size:** ~600 MB | **Stars:** 24k+
**Khi nào dùng:** Security scan containers, repos, secrets — tích hợp CIV pipeline

```powershell
# Dùng khi: CIV pipeline cần deep security scan repo/container
# Hoặc khi Security dept cần audit tools
git clone --depth 1 https://github.com/aquasecurity/trivy.git `
    "D:\AI OS CORP\AI OS\plugins\github-repos\trivy"
```

**AI OS Impact:**
- CIV Pipeline Phase 2: security scan (thay `vet_repo.ps1`)
- Integrate với `security/QUARANTINE/` workflow
- Auto-scan mọi repo trước khi approve

---

### 🔷 developer-roadmap — Kamran Ahmed
**Dept:** Training | HR | R&D
**Size:** ~300 MB | **Stars:** 310k+
**Khi nào dùng:** Khi onboard agent mới, build skill matrix, training plan

```powershell
# Dùng khi: Training dept cần roadmap reference cho agent capabilities
git clone --depth 1 https://github.com/kamranahmedse/developer-roadmap.git `
    "D:\AI OS CORP\AI OS\plugins\github-repos\developer-roadmap"
```

**AI OS Impact:**
- Training dept: skill gap analysis cho 21 depts
- SKILL_REGISTRY enhancement: map skills to roadmap nodes
- Onboarding guide cho các agent mới

---

### 🔷 openai-cookbook — OpenAI
**Dept:** R&D | Engineering | AI Research
**Size:** ~500 MB | **Stars:** 65k+
**Khi nào dùng:** Research LLM patterns, prompt engineering, RAG techniques

```powershell
# Dùng khi: R&D dept cần reference cho LLM integration, RAG, fine-tuning patterns
git clone --depth 1 https://github.com/openai/openai-cookbook.git `
    "D:\AI OS CORP\AI OS\plugins\github-repos\openai-cookbook"
```

**AI OS Impact:**
- R&D dept: LLM pattern library
- bridge_router.py improvements (new routing strategies)
- RAG patterns → LightRAG enhancement

---

### 🔷 anime.js — Julian Garnier
**Dept:** Design | Frontend | Product
**Size:** ~200 MB | **Stars:** 50k+
**Khi nào dùng:** Khi build animated UI components, HUD animations

```powershell
# Dùng khi: Frontend cần animations cho HUD dashboard, product UI
git clone --depth 1 https://github.com/juliangarnier/anime.git `
    "D:\AI OS CORP\AI OS\plugins\github-repos\anime"
```

**AI OS Impact:**
- HUD v3 real-time animated indicators
- Corp cycle phase progress animations
- Dept health dashboard micro-animations

---

### 🔷 agents-course — HuggingFace
**Dept:** Training | R&D | AI Research
**Size:** ~2 GB (notebooks + models)
**Khi nào dùng:** Training dept cần deep-dive vào AI agent concepts, LLM theory

```powershell
# Dùng khi: Training dept cần full HuggingFace agents curriculum
# Cảnh báo: ~2GB — chỉ clone khi có storage
git clone --depth 1 https://github.com/huggingface/agents-course.git `
    "D:\AI OS CORP\AI OS\plugins\github-repos\agents-course"
```

**AI OS Impact:**
- Agent training curriculum cho 12 placeholder agents
- Reference cho activation_status.json → activating new agents
- Pattern library cho autonomous agent behavior

---

### 🔷 gitignore — GitHub
**Dept:** DevOps | Engineering | All depts
**Size:** ~50 MB (small actually)
**Khi nào dùng:** Setup bất kỳ repo mới, cần .gitignore template

```powershell
# Nhỏ — có thể clone ngay khi cần
git clone --depth 1 https://github.com/github/gitignore.git `
    "D:\AI OS CORP\AI OS\plugins\github-repos\gitignore"
```

**AI OS Impact:**
- Template cho mọi repo mới trong AI OS Corp
- Đặt vào `ops/templates/gitignore/`

---

### 🔷 public-apis — Public APIs
**Dept:** R&D | Integration | Product
**Size:** ~100 MB (chủ yếu markdown)
**Khi nào dùng:** Khi R&D cần tìm API để tích hợp tính năng mới

```powershell
# Dùng khi: Integration dept cần tìm free API cho dự án
git clone --depth 1 https://github.com/public-apis/public-apis.git `
    "D:\AI OS CORP\AI OS\plugins\github-repos\public-apis"
```

**AI OS Impact:**
- R&D dept: nguồn tham khảo API cho tích hợp
- External Integrations wishlist (B12 GitHub, Telegram, etc.)
- Rate-free APIs cho prototyping

---

## Quick Clone Reference

```powershell
# ═══ FRONTEND / UI ════════════════════════════════════════
# next.js — Khi build web app
git clone --depth 1 https://github.com/vercel/next.js.git "D:\AI OS CORP\AI OS\plugins\github-repos\next.js"

# excalidraw — Khi cần whiteboard/diagram tool
git clone --depth 1 https://github.com/excalidraw/excalidraw.git "D:\AI OS CORP\AI OS\plugins\github-repos\excalidraw"

# anime.js — Khi cần animations
git clone --depth 1 https://github.com/juliangarnier/anime.git "D:\AI OS CORP\AI OS\plugins\github-repos\anime"

# plotly.js — Khi cần charts/graphs
git clone --depth 1 https://github.com/plotly/plotly.js.git "D:\AI OS CORP\AI OS\plugins\github-repos\plotly.js"

# ═══ ANALYTICS / MONITORING ═══════════════════════════════
# posthog — Self-hosted analytics
git clone --depth 1 https://github.com/posthog/posthog.git "D:\AI OS CORP\AI OS\plugins\github-repos\posthog"

# ═══ SECURITY ═════════════════════════════════════════════
# trivy — Container/repo security scanner
git clone --depth 1 https://github.com/aquasecurity/trivy.git "D:\AI OS CORP\AI OS\plugins\github-repos\trivy"

# ═══ AI / R&D ══════════════════════════════════════════════
# openai-cookbook — LLM patterns & examples
git clone --depth 1 https://github.com/openai/openai-cookbook.git "D:\AI OS CORP\AI OS\plugins\github-repos\openai-cookbook"

# agents-course — HuggingFace agent curriculum [LARGE ~2GB]
git clone --depth 1 https://github.com/huggingface/agents-course.git "D:\AI OS CORP\AI OS\plugins\github-repos\agents-course"

# ═══ TRAINING / KNOWLEDGE ═════════════════════════════════
# developer-roadmap — Skill matrix & learning paths
git clone --depth 1 https://github.com/kamranahmedse/developer-roadmap.git "D:\AI OS CORP\AI OS\plugins\github-repos\developer-roadmap"

# public-apis — Free API directory
git clone --depth 1 https://github.com/public-apis/public-apis.git "D:\AI OS CORP\AI OS\plugins\github-repos\public-apis"

# gitignore — GitHub templates [NHỎ - clone ngay]
git clone --depth 1 https://github.com/github/gitignore.git "D:\AI OS CORP\AI OS\plugins\github-repos\gitignore"
```

---

## Trigger Rule cho Agents

Khi một agent/dept cần clone, tự chạy lệnh trong section "Quick Clone Reference" theo tag phù hợp:

| Trigger | Tag cần tìm | Action |
|---------|-------------|--------|
| Build web UI | `FRONTEND` | Clone next.js |
| Cần charts | `VISUALIZATION` | Clone plotly.js |
| Security audit | `SECURITY` | Clone trivy |
| Research LLM | `AI-PATTERNS` | Clone openai-cookbook |
| Train agent mới | `AI-EDUCATION` | Clone agents-course |
| Tích hợp external | `INTEGRATION` | Clone public-apis |
| Setup repo | `TEMPLATE` | Clone gitignore |
| Cần analytics | `ANALYTICS` | Clone posthog |
| Cần animations | `ANIMATION` | Clone anime.js |
| Diagram/whiteboard | `UI-TOOL` | Clone excalidraw |

---

*Catalog v1.0 | 2026-03-25 | Owner: content_intake dept*
*Run `python ops/aos.py intake <url>` khi có repo mới cần thêm vào catalog*
