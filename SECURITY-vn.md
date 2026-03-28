# Chính Sách Bảo Mật

<div align="center">

[**View English Version**](SECURITY.md)

</div>

---

## 🛡️ Cam Kết Zero-Trust của OmniClaw

OmniClaw được xây dựng dựa trên **Kiến trúc Zero-Trust** (Không tin tưởng bất kỳ ai) cực kỳ nghiêm ngặt. Triết lý cốt lõi của chúng tôi là: máy tính cục bộ (local) của bạn là một pháo đài bất khả xâm phạm. Không một dữ liệu nào — đặc biệt là API keys, biến môi trường (environment variables), hoặc mã nguồn nội bộ — được phép lọt ra ngoài nếu không có sự ủy quyền thủ công, rõ ràng từ chính bạn.

Hệ thống sử dụng các tiến trình chạy ngầm tự động (`omniclaw_cleaner.py`) và các đặc vụ chuyên biệt (**Dept 10 - An Ninh Strix**) để dọn sạch bộ nhớ RAM, cắt xén và viết lại lịch sử git, đồng thời tiêu hủy mọi dữ liệu tạm thời ngay khi phiên làm việc kết thúc.

## Các Phiên Bản Được Hỗ Trợ

Chúng tôi chủ động cung cấp các bản cập nhật và vá lỗi bảo mật cho các phiên bản sau của Nhân hệ điều hành OmniClaw (Core):

| Phiên bản | Trạng thái Hỗ trợ | Ghi chú |
| ------- | ------------------ | ----- |
| 12.0.x  | :white_check_mark: | Chu kỳ hoạt động hiện tại (OmniClaw) |
| < 12.0  | :x:                | Đã lỗi thời (Bản cũ trước khi Đổi tên) |

## 🚨 Báo Cáo Lỗ Hổng Bảo Mật

Nếu bạn phát hiện ra một lỗ hổng bảo mật, một cách để thoát khỏi hộp cát (sandbox escape), hoặc một lỗ hổng khiến Đặc vụ (Agent) có thể vượt qua vòng vây Zero-Trust cục bộ, vui lòng **KHÔNG** mở một Issue công khai trên GitHub. 

Việc tiết lộ công khai lỗ hổng có thể đặt hệ thống của những người dùng khác vào vòng nguy hiểm trước khi bản vá kịp được tung ra.

**Vui lòng báo cáo trực tiếp cho Bộ phận An ninh của chúng tôi (Dept 10):**
1. Truy cập vào **[tab Security](../../security/advisories)** trong repository này.
2. Nhấp vào **Report a vulnerability** để mở một báo cáo bảo mật riêng tư.
3. Cung cấp bản tóm tắt chi tiết về lỗ hổng, bao gồm các bước cụ thể để tái tạo lại lỗi vượt rào đó.

*Hoặc, nếu bạn muốn sử dụng email, vui lòng liên hệ trực tiếp với nhóm bảo trì dự án.*

### Quy trình Tiếp nhận & Xử lý (Triage & Resolution)
1. **Tiếp nhận:** Dept 10 sẽ xác nhận đã nhận được báo cáo lỗ hổng của bạn trong vòng tối đa 48 giờ.
2. **Điều tra:** Đội ngũ nòng cốt của chúng tôi sẽ cô lập vấn đề và xác minh lỗi rò rỉ dữ liệu hoặc thoát hộp cát.
3. **Tiêu diệt:** Một bản vá khẩn cấp (hotfix) sẽ được lập tức phát triển và đẩy thẳng lên nhánh `main`. 
4. **Công bố:** Sau khi bản vá được xác nhận và phân phối an toàn tới người dùng, chúng tôi sẽ công khai lỗ hổng và vinh danh bạn một cách xứng đáng vì công lao phát hiện.

---
*“Không tin tưởng bất kỳ điều gì. Xác minh mọi thứ. Tiêu hủy phần còn lại.”* — **Dept 10 (An Ninh Strix)**
