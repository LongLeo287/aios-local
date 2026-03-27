# Distilled Insights from Brain Sessions (03/2026)
# Source: .gemini/antigravity/brain/ — Sessions tháng 3/2026
# Generated: 2026-03-26 | By: facility-agent (Dept 22) + learning-agent (Dept 14)
# Policy: APPEND ONLY — không ghi đè kiến thức hiện tại

---

## 1. GitNexus — Bài Học Kinh Nghiệm

**Vấn đề được ghi nhận:**
- CDP port 9222 thường xuyên trả lỗi 403 Forbidden khi Browser automation cố connect
- `gitnexus serve :4747` bị crash sau một khoảng thời gian idle — cần restart daemon
- Proxy endpoint `/api/gitnexus/api/repos` trả 502 khi server offline

**Giải pháp đã tìm ra:**
- Luôn kiểm tra `http://127.0.0.1:9222/json/version/` trước khi dùng Browser tool
- Restart gitnexus bằng `gitnexus serve` trước mỗi session CodeIntel
- Dùng cache-buster `?t=<timestamp>` khi reload trang để tránh stale cache

**AI OS Impact:**
- `it-manager-agent` cần thêm health check cho gitnexus vào Phase 0 (System Health)
- Nên thêm auto-restart logic cho gitnexus vào `launcher/START AI OS.ps1`

---

## 2. Browser Automation — Lỗi Phổ Biến

**Patterns lỗi được ghi nhận:**
- `ERR_CONNECTION_REFUSED` khi dev server (Vite/Next.js) chưa khởi động
- Mixed Content/HTTPS issue khi embed HTTP resource trong HTTPS page
- Browser tool mất nhiều lần retry (4+ lần) với các domain external

**Best Practices rút ra:**
- Luôn verify server đang chạy TRƯỚC khi mở browser (`Test-NetConnection`)
- Dùng `http://127.0.0.1` thay vì `http://localhost` để tránh DNS lookup issues
- Timeout 30s là không đủ cho các trang React/Svelte — tăng lên 60s

---

## 3. Dự Án Tiệm Nước Nhỏ v5 — Kiến Trúc

**Ghi nhận từ analysis.md (14/03):**
- Web Fullstack với LadybugDB (custom storage layer)
- AI OS integration điểm: client-facing + agent-assisted workflows
- Cấu trúc: Frontend SPA + Backend Python FastAPI

**Status tại thời điểm đó:** Đang phân tích cấu trúc code

---

## 4. AI OS Architecture — Snapshot 03/2026

**Từ các scratchpad sessions:**
- AI OS có 567,772 nodes và 1,472,756 edges trong GitNexus Code Intel (14/03)
- nullclaw: 335 nodes, 319 edges (nhỏ hơn nhiều so với AI OS)
- Sigma.js + graphology + ForceAtlas2 là tech stack cho LiveMap visualization

---

## 5. ClawTask — Bugs Đã Fix

**Session 21/03:**
- Task checklist rendering issue (resolved)
- Browser CDP connection reliability improved after session

---

*Note: Screenshots và media files (*.webp, *.png) đi kèm các sessions này đã được xóa để tiết kiệm dung lượng sau khi đã distill kiến thức vào file này.*
