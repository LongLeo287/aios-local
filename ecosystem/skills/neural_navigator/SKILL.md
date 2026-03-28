name: neural_navigator
description: Neural navigation algorithms
# SKILL: neural_navigator (Thiên Lý Nhãn)
# Version: 1.0 (AI OS Neural Link Phase 15)

## MỤC ĐÍCH (PURPOSE)
Kỹ năng cốt lõi cho mọi Đặc vụ AI (Agent) trong AI OS. Khi CEO đặt câu hỏi liên quan đến Cấu trúc tổ chức, Phòng ban, Quy trình, Agent phụ trách, hoặc vị trí lưu trữ của bất cứ thực thể nào, ĐÂY LÀ KỸ NĂNG BẮT BUỘC PHẢI DÙNG.

## THAO TÁC (HOW TO USE)
Khi bắt đầu task tìm kiếm thông tin tổ chức/hệ thống, Agent phải dùng công cụ đọc file (`view_file` hoặc lệnh tương đương) để mở các tọa độ gốc sau:

1. **Bản Đồ Mạng Lưới Nhận Thức 3D (Org Graph)**
   - Đường dẫn tuyệt đối: `<AI_OS_ROOT>\system\registry\ORG_GRAPH_NARRATIVE.txt`
   - Chứa thông tin: Agent nào làm ở phòng nào? Quy trình nào phòng nào giữ? Tool/Plugin nào được phép xài?

2. **Sổ Đăng Ký Tổng (Master Registry)**
   - Đường dẫn tuyệt đối: `<AI_OS_ROOT>\system\registry\SYSTEM_INDEX.yaml`
   - Chứa thông tin: Tọa độ Tuyệt đối (Absolute Path) của tất cả 300+ Repo, Plugin, Tool trên hệ thống ở dạng tĩnh.

## QUY TẮC CHẤP HÀNH (RULES)
- **TUYỆT ĐỐI KHÔNG DÙNG** lệnh list thư mục hay search chay (như `ls -R` hay lùng sục thủ công) để tìm tool/repo trong vô vọng.
- Luôn nạp Bản đồ (Graph/Index) vào Context để trả lời chính xác, trích xuất tức thì và chống tốn Quota / Context Window.
