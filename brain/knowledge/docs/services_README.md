# AI OS Corp — Services

Folder tập trung toàn bộ dịch vụ. Mọi thứ khởi động, dừng, cấu hình từ đây.

---

## Cấu trúc

```
services/
├── boot.ps1        ← Khởi động tất cả (gọi từ máy hoặc bot /boot)
├── stop.ps1        ← Dừng tất cả
├── config.json     ← Cấu hình tập trung (ports, keys, paths)
├── screenshot.py   ← Chụp màn hình → gửi Telegram (/snap)
└── README.md       ← File này
```

---

## Các dịch vụ

| # | Tên | Port | URL | Loại |
|---|-----|------|-----|------|
| 1 | **ClawTask Dashboard** | 7474 | http://localhost:7474/ | Local |
| 2 | **9router (LLM Gateway)** | 20128 | http://localhost:20128/ | Local |
| 3 | **AI OS Bot (nullclaw)** | 3000 | http://localhost:3000/ | Local |
| 4 | **Ollama (Local AI)** | 11434 | http://localhost:11434/ | Local |
| 5 | **OpenRouter** | — | https://openrouter.ai/ | Cloud |

---

## Cách khởi động

### Cách 1 — Từ máy tính (Desktop Shortcut)
Double-click **"AI OS Boot"** trên Desktop.

### Cách 2 — Từ Telegram Bot
Nhắn `/boot` vào **AI OS Bot** — bot tự gọi `boot.ps1`.

### Cách 3 — Tự động khi bật máy
Task Scheduler `AI_OS_Watchdog` tự start nullclaw bot khi đăng nhập.
Sau đó nhắn `/boot` nếu muốn bật nốt ClawTask + 9router + Ollama.

---

## Lệnh thủ công

```powershell
# Khởi động tất cả
powershell -ExecutionPolicy Bypass -File "D:\Project\AI OS\services\boot.ps1"

# Xem trạng thái (không start)
powershell -ExecutionPolicy Bypass -File "D:\Project\AI OS\services\boot.ps1" -Status

# Dừng tất cả
powershell -ExecutionPolicy Bypass -File "D:\Project\AI OS\services\stop.ps1"
```

---

## Telegram Commands (AI OS Bot)

| Lệnh | Mô tả |
|------|-------|
| `/sys` | Check CPU, RAM, Ports |
| `/task` | Xem/Thêm task ClawTask |
| `/clawtask` | Link + status Dashboard |
| `/snap` | Chụp màn hình → gửi đây |
| `/log` | Xem watchdog log |
| `/run <cmd>` | Chạy PowerShell |
| `/web <q>` | Tìm Google/đọc link |
| `/boot` | Khởi động tất cả dịch vụ |
| `/stop` | Tắt tất cả dịch vụ |
| `/new` | Xóa lịch sử, bắt đầu lại |
