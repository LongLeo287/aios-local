# 🤝 Gia Nhập Tập Đoàn (Hướng dẫn Đóng góp cho OmniClaw)

<div align="center">

[**English**](CONTRIBUTING.md)

</div>

---

Lời đầu tiên, cảm ơn bạn đã cân nhắc đóng góp sức lực cho **OmniClaw**. 

Dù bạn ở đây để thiết kế một Phòng ban mới (Custom Agent), tối ưu hóa bộ định tuyến Master Router, hay gia cố lá chắn Zero-Trust, bạn giờ đây đã là một phần của lực lượng lao động OmniClaw. Tài liệu này đóng vai trò như một Sổ tay Doanh nghiệp, hướng dẫn bạn cách nộp code, báo cáo lỗi và mở rộng quy mô Tập đoàn.

## 🏢 1. Định Tuyến Chỉ Thị (Báo cáo Lỗi & Vấn đề)

Trước khi viết bất kỳ dòng code nào, chúng ta cần đảm bảo nỗ lực của bạn được chuyển đến đúng phòng ban tiếp nhận.

*   **Lỗ hổng Bảo mật:** tuyệt đối KHÔNG tạo Issue công khai. Chuyển thẳng báo cáo tới **Dept 10 (An Ninh Strix)** bằng cách làm theo hướng dẫn trong file `SECURITY-vn.md`.
*   **Báo cáo Lỗi (Lõi hệ thống & Đặc vụ):** Sử dụng tính năng Issue của GitHub. Vui lòng cung cấp các bước tái tạo lỗi rõ ràng, đính kèm log từ terminal và chỉ định rõ Phòng ban/Đặc vụ nào đang bị sập.
*   **Yêu cầu Tính năng & Đề xuất Chiến lược:** Định tuyến tới **Dept 05 (Hoạch Định Chiến Lược)** bằng cách mở một chủ đề thảo luận trong tab [Discussions](../../discussions). Hãy trình bày ý tưởng của bạn trước khi bỏ hàng giờ ra để code nó.

## 🛠️ 2. Quy Trình Phát Triển Code

Để nộp mã nguồn vào nhân (kernel) của OmniClaw, hãy tuân thủ nghiêm ngặt giao thức sau:

### Bước 1: Fork & Tạo Nhánh (Branch)
1. Fork repository về máy tính cục bộ của bạn.
2. Tạo một nhánh có cách đặt tên logic dựa trên chuẩn thông thường:
   * `feat/ten-tinh-nang-moi` (Dành cho việc thêm tính năng/đặc vụ mới)
   * `fix/ten-loi-can-sua` (Dành cho việc sửa lỗi bug)
   * `docs/cap-nhat-tai-lieu` (Dành cho việc chỉnh sửa tài liệu)

### Bước 2: Tuân thủ Giao thức Plugin 3 Lớp
OmniClaw là một hệ thống nguyên khối (monolithic). Chúng tôi cực kỳ quan tâm đến việc tối ưu dung lượng RAM và thời gian khởi động.
*   **KHÔNG** nhồi nhét các thư viện nặng (như `torch`, `puppeteer`, `cv2`) vào lõi `omniclaw` toàn cục.
*   Nếu Đặc vụ của bạn cần các thư viện nặng đô, hãy xây dựng nó dưới dạng **Plugin Tier-2 (Lazy-Load)**. Nó phải được chạy trong hộp cát (sandbox) và có hàm tự hủy (teardown) để tự động giải phóng RAM ngay sau khi chạy xong. 
*   *Tham khảo:* Đọc [Hướng dẫn Phát triển Plugin Tier-2](https://github.com/LongLeo287/OmniClaw/wiki) trên Wiki của chúng tôi.

### Bước 3: Môi trường Local Zero-Trust
Trước khi bạn nghĩ đến việc gõ lệnh `git commit`:
*   Đảm bảo **KHÔNG CÓ API KEYS**, file `.env`, hay bất kỳ dữ liệu cá nhân nào bị hardcode trong file.
*   Hệ thống sẽ chạy script Ops cục bộ để dọn dẹp không gian làm việc của bạn. Tiến trình ngầm `omniclaw_cleaner.py` sẽ quét sạch các file tạm (`/.omniclaw_temp`) trước khi đẩy code lên.

## 🤖 3. Khai Sinh Phòng Ban Mới (Thêm Đặc Vụ)

Chúng tôi cực kỳ khuyến khích các lập trình viên mở rộng Tập đoàn bằng cách xây dựng các Đặc vụ chuyên trách mới. Nếu bạn đang thiết kế một Phòng ban mới:

1.  **Đơn nhiệm (Single Responsibility):** Đặc vụ của bạn chỉ được làm *một* việc duy nhất và phải làm việc đó cực kỳ xuất sắc. Đừng tạo ra các đặc vụ kiểu "Dao Thụy Sĩ" (ôm đồm mọi thứ).
2.  **Thực thi Phi trạng thái (Stateless Execution):** Đặc vụ của bạn phải kế thừa từ class `BaseAgent`. Nó sẽ nhận dữ liệu đầu vào (payload), thực thi, trả về kết quả bằng định dạng Markdown thuần túy, và lập tức xóa sạch các biến trong bộ nhớ của nó.
3.  **Tài liệu hóa:** Bạn bắt buộc phải cập nhật file sơ đồ tổ chức `brain/corp/org_chart.yaml` và cung cấp một Quy trình vận hành (SOP) ngắn gọn cho Đặc vụ mới của mình trên Wiki.

## 📜 4. Giao Thức Kéo Mã Nguồn (Dept 09 - Kiểm Duyệt Nội Dung)

Khi bạn đã sẵn sàng gộp (merge) code của mình vào nhánh chính của hệ thống:

1. Mở một Pull Request (PR) trỏ vào nhánh `main`.
2. Đặt tiêu đề PR rõ ràng, theo chuẩn commit (vd: `feat(dept-42): add advanced financial analysis agent`).
3. Điền vào mẫu PR (template) có sẵn, giải thích rõ bạn đã thay đổi *những gì* và *tại sao* điều đó mang lại lợi ích cho hệ điều hành OmniClaw.
4. **Code Review:** PR của bạn sẽ được đội ngũ Nòng cốt (đóng vai trò là **Dept 09 - Kiểm Duyệt Nội Dung**) kiểm tra khắt khe. Chúng tôi sẽ rà soát các lỗi rò rỉ bộ nhớ, tính tuân thủ Zero-Trust và các lỗ hổng tiêm nhiễm prompt (prompt injection vulnerabilities).

---
<div align="center">
  <i>"Code với độ chính xác cao. Thực thi tự trị tuyệt đối."</i><br>
  <b>Chào mừng đến với Tập đoàn OmniClaw.</b>
</div>
