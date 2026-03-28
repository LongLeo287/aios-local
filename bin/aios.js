#!/usr/bin/env node
const { execSync } = require('child_process');
const path = require('path');

const args = process.argv.slice(2);
if (args.length > 1) {
    console.warn(`⚠️ [Cảnh báo] Lệnh thừa đoạn: "${args.slice(1).join(' ')}" - sẽ bị bỏ qua.`);
}
const command = args[0] || 'start';

const rootDir = path.resolve(__dirname, '..');
const setupPath = path.join(rootDir, 'setup.ps1');

if (command === 'setup' || command === 'start') {
    console.log("🚀 [AI OS] Đang nạp Trình Điều Khiển Hệ Thống (Kernel)...");
    try {
        const { execFileSync } = require('child_process');
        execFileSync('powershell', ['-ExecutionPolicy', 'Bypass', '-File', setupPath], { stdio: 'inherit', cwd: rootDir });
    } catch (e) {
        console.error("❌ [AI OS] Quá trình thực thi bị gián đoạn hoặc lỗi.");
        console.error(`Chi tiết lỗi: ${e.message}`);
        process.exit(1);
    }
} else {
    console.log(`Lệnh không hợp lệ: aios ${command}`);
    console.log(`Vui lòng dùng: aios (Khởi động bảng điều khiển)`);
}
