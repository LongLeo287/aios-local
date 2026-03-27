# Architecture: MCP Server Bridge (Phase 9)

**BM-025** - Cho phép các AI Agent (Claude Desktop, IDEs) đọc và tìm kiếm trong kho bookmark của bạn một cách an toàn.

---

## 🏗️ Tổng quan Hệ thống (System Overview)
MCP Server là một ứng dụng chạy cục bộ (Local) giúp thu hẹp khoảng cách giữa dữ liệu trong Chrome Extension và AI Agent.

### 1. Luồng dữ liệu (Data Pipeline)
1. **Extension**: Tự động xuất file `bookmarks.json` định kỳ (BM-023).
2. **MCP Server**: Lắng nghe (Watch) file JSON này.
3. **AI Agent**: Gửi yêu cầu qua giao thức MCP (JSON-RPC) để truy vấn dữ liệu.

---

## 🔌 Các Tool được cung cấp (Exposed Tools)
Server sẽ "khoe" các khả năng sau cho AI:

### `search_bookmarks`
- **Input**: `query` (string)
- **Output**: Danh sách các bookmark có tiêu đề hoặc URL khớp với từ khóa.

### `get_bookmarks_by_tag`
- **Input**: `tag` (string)
- **Output**: Danh sách các bookmark đã được AI Tagger gán nhãn tương ứng.

### `summarize_bookmarks`
- **Input**: `folder_id` (string)
- **Output**: Bản tóm tắt nhanh về nội dung chính của một thư mục (dựa trên metadata).

---

## 🛠️ Stack Đề xuất (Suggested Tech Stack)
- **Runtime**: Node.js (với `@modelcontextprotocol/sdk`).
- **Storage**: Đọc trực tiếp file `bookmarks.json`.
- **Search Engine**: `fuse.js` cho tìm kiếm mờ (fuzzy search) tại local server.

---

## 🔒 Bảo mật (Security)
- **Local-Only**: Server chỉ chấp nhận kết nối từ chính máy tính của người dùng (localhost).
- **Read-Only**: Ở giai đoạn này, MCP Server chỉ có quyền Đọc, không có quyền Sửa/Xóa để đảm bảo an toàn dữ liệu.

---
*Bản thiết kế này biến kho bookmark của bạn thành một "External Memory" thực thụ cho AI.*
