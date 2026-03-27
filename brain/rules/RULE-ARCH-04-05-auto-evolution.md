---
rules:
  - id: RULE-ARCH-04
    name: MANDATORY PRE-FLIGHT SCAN
    severity: CRITICAL
  - id: RULE-ARCH-05
    name: PROACTIVE AUTO-EVOLUTION
    severity: CRITICAL
---
# ARCHITECTURE RULES: EVOLUTION & SYSTEM INTEGRITY

## [RULE-ARCH-04] MANDATORY PRE-FLIGHT SCAN (CHỐNG TRÙNG LẶP)
**Mô tả:** AI có xu hướng "Sáng chế lại bánh xe" (Reinventing the wheel) do Context Window hữu hạn. Đạo luật này nghiêm cấm hành vi đó.

**Lệnh thi hành:**
- TRƯỚC khi một Agent (đặc biệt là Antigravity, Claude Code) đề xuất đẻ ra bất kỳ File, Agent, Quy trình, hay Tool mới nào.
- BẮT BUỘC Agent đó phải chạy lệnh quét toàn bộ AI OS (`grep_search`, `list_dir`, view `ORG_GRAPH.yaml`, `SKILL_REGISTRY.json`, tìm trong `system/ops/workflows/`).
- Mục đích: Xác minh 100% chức năng đó chưa hề tồn tại trong hệ thống.
- Nếu chức năng tương tự đã tồn tại -> Chỉ được phép NÂNG CẤP (Update) file cũ. Tuyệt đối không sinh file mới với tên gọi khác.

## [RULE-ARCH-05] PROACTIVE AUTO-EVOLUTION (TỰ ĐOÁN NHẬN VÀ TIẾN HÓA)
**Mô tả:** AI OS không phải là kho lưu trữ tĩnh, mà là một Sinh Vật Tự Học. Mọi tương tác của CEO chứa đựng Tinh hoa đều phải được Hóa Thạch vĩnh viễn thành Hành vi của Hệ thống.

**Lệnh thi hành:**
- Khi làm việc với CEO, nếu xuất hiện 1 concept mới, 1 kiến thức mới, 1 chiến lược giải quyết mới — AI KHÔNG ĐƯỢC CHỜ LỆNH.
- AI phải chủ động NHẬP MÔN kiến thức đó vào hệ thống:
  - Tự động tạo Phòng Ban mới (`brain/corp/departments/`) nếu concept đòi hỏi một phân khu.
  - Tự động tạo Agent (`brain/agents/`) nếu cần người thực thi.
  - Tự động tạo Rule (`brain/rules/`) hoặc Workflow (`system/ops/workflows/`).
- Sự Cập nhật phải diễn ra ở MỨC ĐỘ AUTO. Câu trả lời chuẩn xác nhất của AI là: *"Em đã tự động thâu nạp kiến thức này và lập ra phòng ban/Agent X để duy trì vĩnh viễn"*.
