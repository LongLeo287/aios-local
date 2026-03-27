# AI OS — Distribution & Publishing Plan
# Status: DRAFT | Saved: 2026-03-24 | For: CEO Brainstorm
# Retrieve khi cần: "tìm plan publish AI OS"

---

## BỐI CẢNH

AI OS Corp hiện chạy full local trên máy CEO.
Vấn đề: hệ thống nặng (~GB do plugins, vector DB, models) → không thể push raw lên GitHub.
Câu hỏi cốt lõi: **Distribute AI OS cho user khác như thế nào?**

---

## KIẾN TRÚC PHÂN PHỐI (2-Tier)

### Tier 1 — GitHub Core (~5MB)
```
Gồm: Tất cả code/config/markdown — KHÔNG có data/models

✅ corp/           — 21 dept prompts, rules, sops
✅ brain/          — agents defs, shared-context, governance
✅ ops/            — scripts, workflows (37), configs
✅ kho/            — registries (rules/prompts/plugins/mcp/llm/agents)
✅ hud/            — HUD.md template
✅ skills/         — SKILL.md files only (no heavy code)
✅ security/       — vet_repo.ps1
✅ .env.example    — template keys (không có giá trị thật)
✅ requirements.txt — pinned dependencies
✅ README.md        — setup guide

❌ .env            — gitignore (secrets)
❌ plugins/        — gitignore (100+ repos, GB size)
❌ brain/knowledge/lightrag_db/ — gitignore (vector DB)
❌ infra/          — gitignore (Docker images, binaries)
❌ telemetry/      — gitignore (logs)
❌ security/QUARANTINE/incoming/ — gitignore (quarantine data)
```

### Tier 2 — Setup Script (user tự cài)
```powershell
# ops/scripts/setup.ps1
# User clone repo → chạy script này 1 lần → full system ready

1. pip install -r requirements.txt          (lightrag, mem0, supabase...)
2. ollama pull gemma2:2b                    (local LLM)
3. ollama pull nomic-embed-text             (embeddings)
4. Clone plugins từ plugin-manifest.json   (optional: user chọn tier1/tier2)
5. Copy .env.example → .env               (user điền keys)
6. python ops/scripts/lightrag_server.py  (init LightRAG fresh DB)
7. Run ops/scripts/update_hud.ps1          (first HUD snapshot)
```

---

## OPTIONS PHÂN PHỐI

### Option A — Open Source (GitHub Public)
```
Pros:  Community mở, dễ chia sẻ, SEO tốt
Cons:  Code/prompts lộ, competitor copy được
Best for: Template/skeleton version (không có CEO data/customization)
```

### Option B — Private Repo + Invite
```
Pros:  Kiểm soát access, bảo mật cao
Cons:  Giới hạn collaborators (GitHub Free: 3 người)
Best for: CEO và team internal (<5 người)
```

### Option C — GitHub Template Repo
```
Pros:  User click "Use this template" → clone về → setup
Cons:  Cần maintain 2 versions (template + CEO private)
Best for: Phân phối cho clients hoặc bán AI OS template
```

### Option D — Packaged Release (ZIP)
```
Pros:  Full system, không cần git knowledge
Cons:  Nặng nếu include data, update khó
Best for: CEO muốn trao tay cho client không tech-savvy
```

### Option E — Docker (Tương lai)
```
Pros:  One-click deploy, isolate environment
Cons:  Cần Docker knowledge, nặng image
Best for: Cloud deployment (VPS, server)
Files: docker-compose.yml + Dockerfile
Ref:  PROP_2026-03-23_OBSERVABILITY_LAYER (đã pending)
```

---

## PHÂN LOẠI USER

| User Type | Muốn gì | Solution |
|-----------|---------|---------|
| CEO (chính mình) | Backup + version | Private GitHub + git push |
| Team internal | Cùng dùng | Private repo + invite + shared .env |
| Client chuyên nghiệp | System đã configured | Option D (ZIP) hoặc E (Docker) |
| Developer/Builder | Tự customize | Option A/C (template) |
| Không tech | Plug-and-play | Cần build Setup Wizard (tương lai) |

---

## ROADMAP PUBLISH

### Phase 1 — Ngay bây giờ (30 phút)
```
[x] Tạo .gitignore chuẩn
[x] requirements.txt (pinned)
[x] .env.example
[ ] git commit + push lên private repo
```

### Phase 2 — Ngắn hạn
```
[ ] ops/scripts/setup.ps1 (bootstrap script)
[ ] README.md chuyên nghiệp (install guide, architecture overview)
[ ] plugin-manifest.json (list plugins với download URL)
[ ] ops/workflows/export_ai_os_template.md (đã có workflow này)
```

### Phase 3 — Trung hạn (khi có user khác)
```
[ ] Tách thành GitHub Template repo
[ ] Tạo CHANGELOG.md (version history)
[ ] Video demo / documentation site
[ ] Pricing model (nếu bán)
```

### Phase 4 — Dài hạn (scale)
```
[ ] Docker Compose full stack
[ ] One-click VPS deploy (Digital Ocean App Platform, Railway)
[ ] Setup Wizard UI (web-based)
[ ] Multi-tenant architecture (nhiều CEO cùng chạy)
```

---

## FILES CẦN LÀM NGAY (khi CEO quyết định push)

| File | Mô tả | Thời gian |
|------|-------|----------|
| `.gitignore` | Exclude plugins/, DB, secrets | 5 phút |
| `requirements.txt` | pip dependencies pinned | 5 phút |
| `.env.example` | Template keys | 5 phút |
| `ops/scripts/setup.ps1` | Bootstrap full install | 30 phút |
| `README.md` | Architecture + install guide | 20 phút |

**Tổng:** ~1 giờ → AI OS sẵn sàng distribute

---

## CÂU HỎI CHO BRAINSTORM (khi CEO cần quyết định)

1. Mục tiêu distribute: cho team nội bộ hay cho client/cộng đồng?
2. Có muốn monetize AI OS template không?
3. Phần nào của AI OS là "secret" (CEO customization) và phần nào là "template"?
4. Cloud deploy hay local-only?
5. Target user: technical (developer) hay non-technical?

---

*Plan v1.0 | 2026-03-24 | Retrieve: "aos plan publish" hoặc đọc file này*
*Location: brain/knowledge/notes/KI-PUBLISH-PLAN-2026-03-24.md*
