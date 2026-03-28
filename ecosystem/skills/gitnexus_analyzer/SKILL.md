name: gitnexus_analyzer
description: GitNexus repository parsing bridge for deep code analysis and dependencies
# SKILL: gitnexus_analyzer (Thấu Thị Mã)
# Version: 1.0 (AI OS Neural Link Phase 15)

## MỤC ĐÍCH (PURPOSE)
Giao thức bọc (Wrapper) để sử dụng `GitNexus MCP`. Cung cấp cho các Agent khả năng hiểu cấu trúc Cây Cú pháp Trừu tượng (AST) của các repository thay vì vồ vập đọc code (cat/grep) theo chuỗi văn bản. Giúp nắm trọn dependencies, luồng logic các hàm và quan hệ biến mà không sợ cháy bộ nhớ (Context Overflow).

## THAO TÁC (HOW TO USE)
- **Tọa độ Kho tàng**: `<AI_OS_ROOT>\brain\knowledge\repos\GitNexus`
- **Kích hoạt khi**: Cần phân tích sâu 1 Repository (vd: Tìm xem hàm `login` gọi đến module nào, hoặc trace chain of dependencies của 1 file lớn).
- **Lệnh giao tiếp**: Chạy GitNexus MCP Server theo dạng kiến trúc MCP, hoặc giao tiếp qua Command Line/Node tùy biến được định nghĩa sẵn tại repo.
- (Agent nên tham chiếu file `knowledge.md` trong thư mục GitNexus trước khi gọi tool để nắm syntax chuẩn xác nhất của phiên bản hiện tại).

## QUY TẮC CHẤP HÀNH (RULES)
- Hạn chế dùng `grep` hay `cat` cày cuốc toàn bộ source code khi kho mã nguồn quá lớn (>100 files).
- Ưu tiên kích phát `GitNexus` để trích xuất Khung Xương (AST Skeleton) của phần mềm nhằm tối ưu quota và nâng tầm tư duy hệ thống.
