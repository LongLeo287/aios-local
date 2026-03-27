import os
import shutil
from datetime import datetime

# Scan Targets (Local Core)
LOCAL_ZONES = {
    "knowledge": r"<AI_OS_ROOT>\brain\knowledge\repos",
    "plugins": r"<AI_OS_ROOT>\ecosystem\plugins",
    "tools": r"<AI_OS_ROOT>\ecosystem\tools"
}

# Destinations (Remote Ecosystem)
REMOTE_ZONES = {
    "knowledge": r"<AI_OS_REMOTE_ROOT>\brain\knowledge\repos",
    "plugins": r"<AI_OS_REMOTE_ROOT>\ecosystem\plugins",
    "tools": r"<AI_OS_REMOTE_ROOT>\ecosystem\tools"
}

# Keywords to detect Remote/UI stuff
REMOTE_KEYWORDS = [
    'ui', 'dashboard', 'web', 'frontend', 'app', 'next.js', 'react', 'tailwind',
    'css', 'html', 'viewer', 'visual', 'chart', 'plotly', 'excalidraw', 'animation',
    'cms', 'posthog', 'kanban', 'hub', 'front-end', 'ux'
]

# Ensure Destinations Exist
for path in REMOTE_ZONES.values():
    if not os.path.exists(path):
        os.makedirs(path)

moved_count = 0
retained_count = 0
report_data = []

print("Starting GLOBAL REPO SCAN...")

for zone_name, local_path in LOCAL_ZONES.items():
    if not os.path.exists(local_path):
        continue

    for item in os.listdir(local_path):
        src = os.path.join(local_path, item)
        if not os.path.isdir(src):
            continue

        is_remote = any(k in item.lower() for k in REMOTE_KEYWORDS)

        if is_remote:
            dst = os.path.join(REMOTE_ZONES[zone_name], item)
            try:
                shutil.move(src, dst)
                report_data.append(f"- [MOVED -> REMOTE] {zone_name.upper()}/{item}")
                moved_count += 1
            except Exception as e:
                report_data.append(f"- [ERROR] Failed to move {item}: {e}")
        else:
            retained_count += 1

# Generate Report
report_path = r"<AI_OS_ROOT>\storage\vault\DATA\global_repo_audit.md"
with open(report_path, "w", encoding="utf-8") as f:
    f.write("# 🌐 C-SUITE DASHBOARD: GLOBAL REPO PURGE\n")
    f.write(f"> **Date Executed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write(f"## 1. 🧹 KẾT QUẢ ĐẠI THANH TRỪNG\n")
    f.write(f"- Thống kê có **{retained_count + moved_count} Repos** nằm rải rác trong Lõi.\n")
    f.write(f"- Đã bứng gốc và di dời **{moved_count} Repos** liên quan tới UI/Remote.\n")
    f.write(f"- Giữ lại **{retained_count} Repos** thuần Backend tại Local.\n\n")

    f.write("## 2. 🚚 CHI TIẾT TÀN DƯ BỊ DI DỜI\n")
    for line in report_data:
        f.write(line + "\n")

print(f"\n[DONE] Global Scan complete. {moved_count} exiled. Report: {report_path}")
