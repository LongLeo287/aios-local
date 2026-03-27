# Architect's Handbook: Smart Bookmark Manager

Chào mừng bạn đến với tài liệu hướng dẫn kỹ thuật dành cho lập trình viên. Tài liệu này giải thích các nguyên tắc thiết kế cốt lõi đứng sau Extension này.

## 🏗 Kiến trúc: Domain-Driven Design (DDD)
Chúng ta tách biệt logic thành 4 lớp rõ rệt:
1. **Entities (`src/core/entities`)**: Chứa logic nghiệp vụ thuần túy (ví dụ: `BookmarkEntity` xác định một bookmark hợp lệ).
2. **Repositories (`src/services/BookmarkRepository.js`)**: Lớp truy xuất dữ liệu (Abstraction layer). Không quan tâm dữ liệu đến từ Chrome hay IndexedDB.
3. **Services (`src/services`)**: Xử lý các nghiệp vụ phức tạp liên quan đến bên thứ 3 (Sync, AI, HTML Parsing).
4. **UI Components (`src/ui/components`)**: Hoàn toàn không chứa logic lưu trữ. Chỉ nhận dữ liệu và render.

## 🔌 Hệ thống Plugin
Extension sử dụng mô hình **Event-driven Hooks**. Bạn có thể đăng ký plugin mới tại `PluginManager`:
- `onBeforeCreate`: Tiền xử lý dữ liệu.
- `onCreated`: Gán nhãn AI (Async).
- `onImportComplete`: Xử lý hàng loạt sau khi nạp dữ liệu.

## 💾 Luồng Dữ liệu (Data Flow)
`UI Event` -> `AppController` -> `BookmarkRepository` -> `Storage API` -> `SyncService` -> `Cloud`.

## 🎨 Design System
Hệ thống sử dụng **CSS Variable Tokens**. Mọi thay đổi về màu sắc trong Settings thực chất là thay đổi giá trị của `--accent-primary` trong `:root`.

## 🚀 Định hướng Scalability
Để hỗ trợ tree bookmark cực lớn:
- **Lazy Loading**: Chỉ nạp metadata khi cần thiết.
- **Virtual DOM**: (Sắp triển khai ở Phase 8) Để nâng cao hiệu năng cuộn.

---
*Tài liệu này được biên soạn bởi Senior Architect để làm kim chỉ nam cho quá trình phát triển.*
