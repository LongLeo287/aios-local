# SKILL: OpenClaw Core Tools
# Thẩm quyền: Worker & Manager
# Mô tả: Bộ công cụ CLI mạnh mẽ cho phép Agent lướt web, chạy code, hoặc quản lý memory.

## Cài đặt & Require
- Dành cho các Agent chạy trong môi trường có cài đặt `openclaw` CLI.
- Xác nhận tool đã có sẵn trên máy bằng lệnh `npx openclaw status` (nếu dùng local) hoặc gọi `openclaw` trực tiếp.

## Cách Dùng

### 1. Trình Duyệt & Lướt Web (Browser & Search)
Bạn có thể đọc nội dung một URL một cách đáng tin cậy:
```bash
openclaw tools call web_fetch url="https://example.com"
```
Quét nội dung tìm kiếm (Semantic Search):
```bash
openclaw tools call web_search query="latest framework changes"
```

### 2. Thực thi Shell Code an toàn (Exec)
```bash
openclaw tools call exec command="ls -la"
```

### 3. Đánh Chỉ Mục (Memory Indexing)
Nếu bạn thay đổi file trí nhớ trong thư mục `/memory/`, bạn cần bảo OpenClaw chạy index lại để Vector Search hoạt động:
```bash
openclaw memory index
```

### 4. Semantic Search trong Memory nội bộ
Nếu bạn cần lục lại bài học cũ liên quan tới một Topic:
```bash
openclaw memory search "khái niệm cognitive reflection"
```

## Chú ý (Việt ngữ)
> **Dành cho Agent (Tự ngẫm):** Đây là công cụ hệ thống rất sâu. Chỉ dùng khi có chỉ thị rõ ràng hoặc khi các công cụ built-in của LLM không đủ năng lực (ví dụ cần bypass captcha, cần load Vector DB).
