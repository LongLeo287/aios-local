# ⚖️ MA TRẬN LUẬT (DEPARTMENTAL RULES)
**Chức năng:** Thư mục này chứa các quy định, ranh giới quyền hạn, và SOP cấp độ Hệ thống dành riêng cho từng Phòng ban và Agent, thuộc kiến trúc Neural Link (AI OS Corp).

## 🗂️ Quy Hoạch Không Gian Luật
Để giữ cho `CLAUDE.md` và `GEMINI.md` gọn nhẹ (chỉ chứa System Boot Protocol), mọi Rule chi tiết về đặc vụ hoặc phòng ban sẽ được lưu tại đây. AI Agent chỉ tải tệp Rule của phòng ban nó vào bộ nhớ khi được kích hoạt.

### 🛡️ Cấu Trúc Rule Chuẩn (Đề Xuất):
Tên file: `[dept_id]_rules.md` (vd: `engineering_rules.md`, `qa_testing_rules.md`)

```markdown
# LUẬT PHÒNG BAN: [TÊN PHÒNG]
**Mã phòng:** `[dept_id]`

## 1. Phạm Vi Quyền Hạn (Scope of Authority)
- [Liệt kê các thư mục được phép đọc/ghi]
- [Liệt kê các thao tác cấm kỵ (Blacklist)]

## 2. Tiêu Chuẩn Phê Duyệt (Approval Gates)
- [Liệt kê các workflow cần qua bước QA/Security]
- Mọi code commit phải có dấu của `[agent_name]`.

## 3. Chính Sách Bộ Nhớ (Memory Policy)
- Bộ nhớ của phòng này được cách ly tại `brain/memory/[dept_id]/`.
- Cấm Agent phòng này đọc trộm Memory của `[phòng_ban_khác]`.
```

## 🔄 Liên Kết (Mapping)
Các tệp Rule này tự động được Ánh xạ (Map) vào Đồ thị Tổ chức thông qua nhánh `rules` (trong tương lai, khi Org Mapper cập nhật v4.0). Tạm thời, Agent tự tìm đọc file Rule của phòng mình theo nguyên tắc `Tên Phòng + _rules.md`.
