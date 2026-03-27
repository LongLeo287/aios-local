# AI OS Corp — AstrBot Setup Guide
# Dept 03 (IT Infrastructure) | Updated: 2026-03-18

## Bước 1: Lấy thông tin cần thiết

### 1.1 Telegram Bot Token
1. Mở Telegram → tìm **@BotFather**
2. Gửi: `/newbot`
3. Đặt tên bot (vd: `AI OS Corp Bot`)
4. Đặt username (vd: `aios_corp_bot`)
5. Copy **TOKEN** dạng: `7123456789:AABBCc...`

### 1.2 Telegram Admin ID
1. Mở Telegram → tìm **@userinfobot**
2. Gửi `/start`
3. Copy **ID** (VD: `12345678`)

### 1.3 LLM API Key (chọn 1)
- **Gemini** (miễn phí): https://aistudio.google.com/apikey
- **Anthropic** (Claude): https://console.anthropic.com

---

## Bước 2: Khởi động AstrBot

```powershell
# Mở PowerShell, chạy startup script
powershell -ExecutionPolicy Bypass -File "D:\Project\AI OS\scripts\startup.ps1"

# Hoặc start AstrBot riêng
& "D:\Project\AI OS\plugins\AstrBot\.venv312\Scripts\astrbot.exe" run
```

AstrBot WebUI sẽ mở tại: **http://localhost:6185/**

---

## Bước 3: Cấu hình qua WebUI (http://localhost:6185/)

### 3.1 Thêm LLM Provider
- Menu: **Settings → LLM Providers**
- Add: Gemini (paste API key) hoặc Anthropic

### 3.2 Kết nối Telegram
- Menu: **Settings → Message Platforms**
- Add: **Telegram Bot**
- Paste: **Bot Token** từ Bước 1

### 3.3 Set Admin
- Menu: **Settings → Admin**
- Add Telegram ID từ Bước 1
- Role: Admin

### 3.4 Cài AI OS Corp Plugin
- Copy folder: `D:\Project\AI OS\plugins\AstrBot\data\plugins\astrbot_plugin_aios_corp\`
- Vào: **Plugins → Local Install**
- Hoặc restart AstrBot (auto-detect plugin)

---

## Bước 4: Test qua Telegram

Nhắn vào bot Telegram của bạn:
```
/start
/help_aios
/clawtask
/agents
/status
```

---

## Commands AI OS Corp Plugin

| Command | Mô tả |
|---------|-------|
| `/clawtask` | Xem toàn bộ Kanban board |
| `/clawtask todo` | Chỉ xem TODO tasks |
| `/clawtask inprogress` | Tasks đang chạy |
| `/agents` | Danh sách 10 agents + status |
| `/status` | System health check |
| `/civ` | Xem CIV batch reports |
| `/help_aios` | Help menu |

---

## Ports

| Service | Port | URL |
|---------|------|-----|
| ClawTask Dashboard | 7474 | http://localhost:7474/ |
| AstrBot WebUI | 6185 | http://localhost:6185/ |

---

## Auto-startup (Windows Task Scheduler)

```powershell
# Tạo scheduled task chạy khi Windows boot
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -File `"D:\Project\AI OS\scripts\startup.ps1`""
$trigger = New-ScheduledTaskTrigger -AtStartup
Register-ScheduledTask -TaskName "AI OS Corp Startup" -Action $action -Trigger $trigger -RunLevel Highest
```

*Chạy command này trong PowerShell (Admin) để auto-start khi bật máy.*
