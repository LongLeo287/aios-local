# PHÒNG LỄ TÂN — Client Reception Activation Guide
# Status: 🟡 BUILT — DORMANT (chờ token)
# Khi sẵn sàng: đọc file này và thực hiện theo thứ tự

---

## Trạng Thái Hiện Tại

| Component | Status | File |
|-----------|--------|------|
| Gateway SOP | ✅ Sẵn sàng | `corp/sops/CLIENT_INTAKE_GATEWAY.md` |
| project_intake_agent | ✅ Registered | `skills/project_intake_agent/SKILL.md` |
| proposal_engine | ✅ Registered | `skills/proposal_engine/SKILL.md` |
| nullclaw config | ✅ Sẵn sàng | `REMOTE/claws/nullclaw/configs/client_gateway.json` |
| tinyclaw config | ✅ Sẵn sàng | `REMOTE/claws/tinyclaw/configs/client_gateway.json` |
| Delivery Pipeline | ✅ Sẵn sàng | `corp/sops/DELIVERY_PIPELINE.md` |
| Telegram Bot | 🔴 Cần token | `@BotFather` trên Telegram |
| Discord Bot | 🔴 Cần token | `discord.com/developers` |

---

## Khi Bạn Sẵn Sàng — Checklist Activate

### Bước 1: Lấy Bot Tokens

**Telegram:**
1. Mở Telegram → nhắn tin @BotFather
2. `/newbot` → đặt tên: `AI OS Corp` → username: `AICorpIntakeBot`
3. Copy token (dạng `123456:ABC-DEF...`)

**Discord (optional):**
1. Vào [discord.com/developers](https://discord.com/developers/applications)
2. New Application → Bot → Add Bot → copy token

### Bước 2: Set Environment Variables

```powershell
# Trong PowerShell (Terminal) — thay thế bằng token thật
$env:ANTHROPIC_API_KEY        = "sk-ant-..."
$env:TELEGRAM_CLIENT_BOT_TOKEN = "123456:ABC-..."   # Client bot
$env:TELEGRAM_OPS_BOT_TOKEN    = "654321:XYZ-..."   # Ops bot (optional)
$env:TELEGRAM_OPS_ALLOWED_IDS  = "your_telegram_user_id"

# Optional Discord:
$env:DISCORD_CLIENT_BOT_TOKEN  = "..."
$env:DISCORD_INTAKE_CHANNEL_IDS = "channel_id_here"
```

> Lấy Telegram User ID: nhắn tin @userinfobot

### Bước 3: Khởi Động nullclaw (Client Gateway)

```powershell
# Đổi vào thư mục plugin
cd "D:\Project\AI OS\REMOTE\claws\nullclaw"

# Build binary (nếu chưa có):
# zig build -Doptimize=ReleaseSmall

# Start gateway với config
nullclaw --config "D:\Project\AI OS\REMOTE\claws\nullclaw\configs\client_gateway.json" gateway
```

### Bước 4: Expose qua Tunnel (để Telegram reach được)

```powershell
# Option A — Cloudflare Tunnel (free, ổn định)
cloudflared tunnel --url http://localhost:3100

# Option B — ngrok (đơn giản hơn để test)
ngrok http 3100
```

Copy URL tunnel (vd: `https://abc123.trycloudflare.com`)

### Bước 5: Đăng Ký Webhook

```powershell
# Thay <TOKEN> và <TUNNEL_URL>
Invoke-WebRequest "https://api.telegram.org/bot<TOKEN>/setWebhook?url=<TUNNEL_URL>/telegram/webhook"
```

### Bước 6: Khởi Động tinyclaw (Ops Dashboard)

```powershell
cd "D:\Project\AI OS\REMOTE\claws\tinyclaw"
tinyclaw start --config "D:\Project\AI OS\REMOTE\claws\tinyclaw\configs\client_gateway.json"
tinyclaw office  # Dashboard tại http://localhost:3000
```

### Bước 7: Test

Gửi tin nhắn đến bot Telegram → phải nhận được welcome message:
```
👋 Chào mừng đến AI OS Corp!
Chúng tôi cung cấp giải pháp AI agents cho mọi loại dự án...
```

---

## Lệnh Hàng Ngày (sau khi activate)

```powershell
# Xem intakes mới
cat "D:\Project\AI OS\shared-context\client_intake\_index.json"

# Xem proposal đã tạo
ls "D:\Project\AI OS\shared-context\corp\proposals\"

# Xem revenue
cat "D:\Project\AI OS\shared-context\corp\invoices\_payment_tracker.json"
```

---

*Phòng Lễ Tân sẵn sàng. Cung cấp token bất kỳ lúc nào để kích hoạt.* 🏨
