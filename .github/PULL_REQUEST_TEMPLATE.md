---
name: Pull Request
about: Submit a patch, tool, or agent upgrade
---

## 🛠 Lĩnh Vực Cập Nhật / Area of Update
- [ ] Core Infra (Tier 1) / Bootstrapper
- [ ] Plugin / Tool (Tier 2/3)
- [ ] Agent Roster / Role / Prompt
- [ ] System Rules / Governance (`SOUL.md`, `GEMINI.md`, v.v.)
- [ ] Knowledge Bơm vào / RAG Memory

## 📖 Mô Tả Chi Tiết / Description
Vui lòng giải thích ngắn gọn cập nhật này làm gì, tại sao nó cần thiết.

## ✅ Checklist (Bắt Buộc / Mandatory)
- [ ] Đã quét bảo mật (Không nhúng API keys / Mật khẩu cá nhân / `.env`).
- [ ] Các tính năng mới không gọi trực tiếp Root OS commands trừ khi được cho phép (`SafeToAutoRun` strict policies).
- [ ] (Nếu có Plugin Mới) Đã tuân thủ nguyên tắc Lazy-Load 3-Tier.
- [ ] Đã cập nhật `SKILL_REGISTRY.json` hoặc `AGENTS.md` (nếu cần).

## 🧠 Tác Động Giao Tiếp (Phía CEO)
Bản cập nhật này có làm thay đổi cách CEO ra lệnh cho hệ thống không?
(Nếu có, giải thích vắn tắt lệnh mới / luồng thông tin mới).
