# Technical Specification: Phase 8 (Hardening & Scalability)

Tài liệu này cung cấp hướng dẫn kỹ thuật chi tiết để triển khai các tính năng trong Phase 8.

---

## 1. End-to-End Encryption (BM-021)
Mục tiêu: Mã hóa dữ liệu bookmark trước khi đưa lên `chrome.storage.sync`.

### Luồng xử lý (Logic Flow)
1. **Khởi tạo**: Người dùng nhập mật khẩu (Passphrase) qua Settings.
2. **Key Derivation**: Sử dụng `PBKDF2` (với `SHA-256` và `Salt`) để tạo ra một đối tượng `CryptoKey` mạnh từ mật khẩu.
3. **Mã hóa (Encryption)**:
   - Thuật toán đề xuất: `AES-GCM` (256-bit).
   - Trước khi gọi `SyncService.syncChange`, dữ liệu JSON sẽ được mã hóa thành một mảng bytes (Base64).
4. **Lưu trữ**: Chỉ bản mã (Ciphertext) và IV (Initialization Vector) được lưu lên cloud.
5. **Giải mã (Decryption)**: Khi kéo dữ liệu từ thiết bị khác, yêu cầu user nhập Passphrase để giải mã cục bộ.

### Công nghệ sử dụng
- Web Crypto API (`window.crypto.subtle`).

---

## 2. Virtual Scrolling Implementation (BM-022)
Mục tiêu: Đảm bảo UI mượt mà với 10,000+ bookmark.

### Nguyên lý kỹ thuật
Thay vì render toàn bộ 10,000 `div` vào DOM, chúng ta chỉ duy trì khoảng 20-30 `div` tương ứng với vùng nhìn thấy (Viewport).

### Các bước triển khai
1. **Cố định Item Height**: Mỗi dòng bookmark/folder phải có chiều cao cố định (ví dụ: `40px`).
2. **Container Wrapper**: Một div mẹ có `overflow-y: auto` và tổng chiều cao là `count * 40px`.
3. **Dynamic Rendering**:
   - Khi user cuộn: Tính toán `scrollTop`.
   - Xác định `startIndex = Math.floor(scrollTop / 40)`.
   - Xác định `endIndex = startIndex + (viewportHeight / 40)`.
4. **Render Slice**: Chỉ render các Entity trong khoảng `[startIndex, endIndex]`.
5. **Transform/Offset**: Sử dụng `transform: translateY(...)` để đặt các item vào đúng vị trí trong vùng cuộn.

---

## 3. Automated Local Backup (BM-023)
Mục tiêu: Chống mất dữ liệu hoàn toàn.

### Logic
- Sử dụng `chrome.alarms` để lên lịch chạy ngầm hàng tuần.
- Task sẽ tự động gọi `repo.getTree()`, chuyển đổi thành JSON và lưu vào `File System Access API` hoặc tải xuống tự động dưới dạng `.json`.

---

## 4. Technical Debt Audit (BM-024)
- **Refactoring**: Tách các callback lồng nhau (callback hell) sang `async/await`.
- **Typing**: Chuyển dần sang mô hình chặt chẽ hơn để tránh lỗi `undefined` khi truy cập bookmark properties.

---
*Tài liệu này được soạn thảo để cung cấp Blueprint cho lập trình viên thực thi.*
