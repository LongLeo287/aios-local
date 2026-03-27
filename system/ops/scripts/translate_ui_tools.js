const fs = require('fs');
const path = require('path');

const targetFile = 'd:\\AI OS CORP\\AI OS\\plugins\\openclaw\\ui\\src\\ui\\views\\agents-panels-tools-skills.ts';
let content = fs.readFileSync(targetFile, 'utf8');

const replacements = [
  ['Tool Access', 'Quyền Truy Cập Công Cụ (Tool Access)'],
  ['Profile + per-tool overrides for this agent.', 'Hồ sơ công cụ + Ghi đè cấu hình cho Agent này.'],
  ['</span> enabled.', '</span> đã cấp quyền.'],
  ['>Enable All<', '>Bật Tất Cả<'],
  ['>Disable All<', '>Tắt Tất Cả<'],
  ['>Reload Config<', '>Tải Lại Cấu Hình<'],
  ['"Saving…" : "Save"', '"Đang Lưu..." : "Lưu Thay Đổi"'],
  ['Load the gateway config to adjust tool profiles.', 'Vui lòng tải cấu hình Gateway để điều chỉnh.'],
  ['This agent is using an explicit allowlist in config. Tool overrides are managed in the Config tab.', 'Agent này đang sử dụng danh mục chỉ định cố định. Các tinh chỉnh Tool được quản lý ở tab Config.'],
  ['Global tools.allow is set. Agent overrides cannot enable tools that are globally blocked.', 'Hệ thống đang khoá tool toàn cục. Không thể bật các tool đã bị Admin khoá.'],
  ['Loading runtime tool catalog…', 'Đang tải danh sách công cụ hệ thống...'],
  ['Could not load runtime tool catalog. Showing built-in fallback list instead.', 'Không thể tải danh mục công cụ. Đang hiển thị danh sách dự phòng.'],
  ['<div class="label">Profile</div>', '<div class="label">Hồ Sơ (Profile)</div>'],
  ['<div class="label">Source</div>', '<div class="label">Nguồn cấu hình</div>'],
  ['<div class="label">Status</div>', '<div class="label">Trạng thái</div>'],
  ['>unsaved<', '>K.Lưu (unsaved)<'],
  ['<div class="label">Quick Presets</div>', '<div class="label">Cấu Hình Nhanh (Presets)</div>'],
  ['>Inherit<', '>Kế Thừa<'],
  ['<div class="card-title">Skills</div>', '<div class="card-title">Kỹ Năng Kích Hoạt (Skills)</div>'],
  ['Per-agent skill allowlist and workspace skills.', 'Danh sách File Kỹ năng cấp phép riêng cho Agent và Workspace.'],
  ['>Reset<', '>Khôi Phục<'],
  ['title="Remove per-agent allowlist and use all skills"', 'title="Xoá danh sách cấp phép riêng và dùng tất cả kỹ năng"'],
  ['"Loading…" : "Refresh"', '"Đang Tải..." : "Làm Mới"'],
  ['Load the gateway config to set per-agent skills.', 'Vui lòng tải cấu hình Gateway để cấp phép Skill.'],
  ['This agent uses a custom skill allowlist.', 'Agent này đang sử dụng danh sách Skills tùy chỉnh.'],
  ['All skills are enabled. Disabling any skill will create a per-agent allowlist.', 'Tất cả kỹ năng đang bật. Tắt bất kỳ kỹ năng nào sẽ kích hoạt chế độ Cấp phép riêng lẻ.'],
  ['Load skills for this agent to view workspace-specific entries.', 'Tải kỹ năng để xem các tính năng dành riêng cho nhóm.'],
  ['<span>Filter</span>', '<span>Bộ Lọc</span>'],
  ['placeholder="Search skills"', 'placeholder="Tìm kiếm kỹ năng..."'],
  ['} shown<', '} đang hiển thị<'],
  ['No skills found.', 'Không tìm thấy kỹ năng nào.'],
  ['Missing: ${', 'Thiếu File (Missing): ${'],
  ['Reason: ${', 'Hệ thống đánh giá: ${'],
  // Extra checks for internal text
  ['"agent override"', '"ghi đè cục bộ"'],
  ['"global default"', '"mặc định hệ thống"'], 
  ['"default"', '"mặc định"']
];

replacements.forEach(([eng, vie]) => {
  content = content.replace(new RegExp(eng.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), vie);
});

fs.writeFileSync(targetFile, content);
console.log('UI text successfully translated to Vietnamese.');
