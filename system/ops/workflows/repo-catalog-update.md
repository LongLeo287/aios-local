---
description: Cập nhật tự động Master Repo Catalog — verify active repos, bổ sung PENDING, dọn ARCHIVED
department: Dept 20 — CIV (Catalog Intelligence & Versioning)
agent: knowledge_navigator, archivist
trigger: weekly | manual | on_new_url_submitted
---

# Repo Catalog Update Workflow
**Version:** 1.0 | **Owner:** Dept 20 CIV | **Auto-run:** Mỗi Thứ Hai 00:00

---

## MỤC TIÊU

Duy trì `ecosystem/plugins/MASTER_REPO_CATALOG.md` luôn cập nhật và chính xác.
Đảm bảo 3 kho luôn được phân loại đúng:
- ⭐ **ACTIVE** — repos AI OS đang dùng (kiểm tra version mới)
- 🔖 **PENDING** — repos APPROVE chưa cài (hàng chờ CEO)
- ❌ **ARCHIVED** — repos REJECT/DEFER (CEO xem xét lại khi cần)

---

## STEP 1 — Kiểm Tra ACTIVE Repos (Health Check)

```
Agent: knowledge_navigator
Action:
  FOR each repo in ACTIVE_REPOS.md:
    1. Gọi GitHub API: GET /repos/{owner}/{repo}/releases/latest
    2. So sánh version với version đang cài trong ecosystem/plugins/
    3. Nếu có version mới → log vào MASTER_REPO_CATALOG.md (cột "Update Available")
    4. Notify CEO qua Telegram nếu Tier 1 có bản vá bảo mật
```

---

## STEP 2 — Batch Evaluate New URLs

```
Agent: knowledge_navigator + strix-agent
Trigger: Khi CEO gửi URL mới vào hệ thống
Action:
  1. Chạy repo_eval_github_api.py với batch 50 repos mới nhất
  2. Cross-check với plugin-catalog.md (Step 2 của repo-evaluation.md)
  3. Phân loại: APPROVE → PENDING | REJECT/DEFER → ARCHIVED
  4. Update MASTER_REPO_CATALOG.md
```

---

## STEP 3 — Update Catalog & Notify

```
Agent: archivist
Action:
  1. Chạy ops/scripts/build_master_catalog.py
  2. Update MASTER_REPO_CATALOG.md (ACTIVE/PENDING/ARCHIVED counts)
  3. Sync plugin-catalog.md với trạng thái mới
  4. Gửi weekly digest qua Telegram:
     "📊 Repo Catalog Weekly:
      ⭐ ACTIVE: N repos | 🔖 PENDING: N | ❌ ARCHIVED: N
      🆕 Updates available: N repos"
```

---

## STEP 4 — CEO Review Trigger (Manual)

```
CEO Action: "review pending repos" 
→ Hệ thống hiển thị top 10 PENDING sorted by Stars
→ CEO approve/defer từng cái
→ APPROVE → trigger plugin-integration.md
→ DEFER → giữ trong PENDING thêm 30 ngày
```

---

## INTEGRATION TRIGGERS

```yaml
On new URL from CEO:
  - Trigger: repo-evaluation.md (5 bước)
  - Then: build_master_catalog.py
  - Then: Notify CEO kết quả

On weekly schedule:
  - Run: STEP 1 (health check active repos)
  - Run: STEP 3 (rebuild catalog)
  
On CEO command "integrate <repo>":
  - Trigger: plugin-integration.md
  - Move from PENDING → ACTIVE
```

---

## AGENTS PHỤ TRÁCH

| Agent | Nhiệm vụ |
|-------|---------|
| `knowledge_navigator` | Gọi GitHub API, phân tích repo mới |
| `archivist` | Cập nhật catalog, lưu trữ báo cáo |
| `strix-agent` | Security scan repos trước khi APPROVE |
| `strategy-agent` | Ưu tiên hóa PENDING queue cho CEO |

---

*Workflow Owner: Dept 20 CIV | Created: 2026-03-27*
*"Every repo must have a home: ACTIVE, PENDING, or ARCHIVED."*
