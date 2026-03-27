# AI OS Corp â€” AstrBot Setup Guide
# Dept 03 (IT Infrastructure) | Updated: 2026-03-18

## BÆ°á»›c 1: Láº¥y thÃ´ng tin cáº§n thiáº¿t

### 1.1 Telegram Bot Token
1. Má»Ÿ Telegram â†’ tÃ¬m **@BotFather**
2. Gá»­i: `/newbot`
3. Äáº·t tÃªn bot (vd: `AI OS Corp Bot`)
4. Äáº·t username (vd: `aios_corp_bot`)
5. Copy **TOKEN** dáº¡ng: `7123456789:AABBCc...`

### 1.2 Telegram Admin ID
1. Má»Ÿ Telegram â†’ tÃ¬m **@userinfobot**
2. Gá»­i `/start`
3. Copy **ID** (VD: `12345678`)

### 1.3 LLM API Key (chá»n 1)
- **Gemini** (miá»…n phÃ­): https://aistudio.google.com/apikey
- **Anthropic** (Claude): https://console.anthropic.com

---

## BÆ°á»›c 2: Khá»Ÿi Ä‘á»™ng AstrBot

```powershell
# Má»Ÿ PowerShell, cháº¡y startup script
powershell -ExecutionPolicy Bypass -File "<AI_OS_ROOT>\scripts\startup.ps1"

# Hoáº·c start AstrBot riÃªng
& "<AI_OS_ROOT>\plugins\AstrBot\.venv312\Scripts\astrbot.exe" run
```

AstrBot WebUI sáº½ má»Ÿ táº¡i: **http://localhost:6185/**

---

## BÆ°á»›c 3: Cáº¥u hÃ¬nh qua WebUI (http://localhost:6185/)

### 3.1 ThÃªm LLM Provider
- Menu: **Settings â†’ LLM Providers**
- Add: Gemini (paste API key) hoáº·c Anthropic

### 3.2 Káº¿t ná»‘i Telegram
- Menu: **Settings â†’ Message Platforms**
- Add: **Telegram Bot**
- Paste: **Bot Token** tá»« BÆ°á»›c 1

### 3.3 Set Admin
- Menu: **Settings â†’ Admin**
- Add Telegram ID tá»« BÆ°á»›c 1
- Role: Admin

### 3.4 CÃ i AI OS Corp Plugin
- Copy folder: `<AI_OS_ROOT>\plugins\AstrBot\data\plugins\astrbot_plugin_aios_corp\`
- VÃ o: **Plugins â†’ Local Install**
- Hoáº·c restart AstrBot (auto-detect plugin)

---

## BÆ°á»›c 4: Test qua Telegram

Nháº¯n vÃ o bot Telegram cá»§a báº¡n:
```
/start
/help_aios
/clawtask
/agents
/status
```

---

## Commands AI OS Corp Plugin

| Command | MÃ´ táº£ |
|---------|-------|
| `/clawtask` | Xem toÃ n bá»™ Kanban board |
| `/clawtask todo` | Chá»‰ xem TODO tasks |
| `/clawtask inprogress` | Tasks Ä‘ang cháº¡y |
| `/agents` | Danh sÃ¡ch 10 agents + status |
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
# Táº¡o scheduled task cháº¡y khi Windows boot
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -File `"<AI_OS_ROOT>\scripts\startup.ps1`""
$trigger = New-ScheduledTaskTrigger -AtStartup
Register-ScheduledTask -TaskName "AI OS Corp Startup" -Action $action -Trigger $trigger -RunLevel Highest
```

*Cháº¡y command nÃ y trong PowerShell (Admin) Ä‘á»ƒ auto-start khi báº­t mÃ¡y.*

