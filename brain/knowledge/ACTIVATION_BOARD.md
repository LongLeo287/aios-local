# 🚦 ACTIVATION BOARD — AI OS Services & Dashboards
# Cập nhật: 2026-03-16
# Mọi thứ cần kích hoạt / mở localhost phải có ở bảng này

> **Quy tắc:** Trước khi dùng bất kỳ plugin nào dưới đây, phải chạy lệnh khởi động.
> Các service này KHÔNG tự chạy — cần kích hoạt thủ công hoặc cấu hình auto-start.

---

## 🟢 Đang chạy / Always-On

| Service | URL | Port | Ghi chú |
|---------|-----|------|---------|
| **AI OS Dashboard** | http://127.0.0.1:19000 | 19000 | Tự khởi động qua pre-session.md |

---

## 🔴 Cần kích hoạt thủ công

### 🦞 LobsterBoard — Dashboard tổng hợp AI usage
```bash
cd "D:\LongLeo\Project\AI OS\plugins\LobsterBoard"
cp config.example.json config.json   # lần đầu tiên
# Sửa config.json: city, API keys muốn dùng
node server.cjs
```
| | |
|-|-|
| **URL** | http://localhost:3000 |
| **Port** | 3000 |
| **Cần** | Node.js ≥ 18 |
| **Lý do dùng** | Monitor Antigravity + Claude Code + Gemini + Cursor + Copilot usage từ 1 màn hình |
| **Widget đặc biệt** | Antigravity widget: `antigravity-usage login` → xem Gemini 3 + Claude usage |

---

### 📡 Remote Bridge (Channels) — Zalo / Telegram / Discord / Facebook

> **Trạng thái hiện tại (2026-03-16):** Channels CHƯA ĐƯỢC CẤU HÌNH
> Chạy `python channels/health_check.py` để kiểm tra.

```bash
# 1. Điền token vào .env (bắt buộc trước khi chạy)
# TELEGRAM_BOT_TOKEN=your_token  ← từ @BotFather
# DISCORD_BOT_TOKEN=your_token   ← từ Discord Developer Portal
# ZALO_ACCESS_TOKEN=your_token   ← từ Zalo OA
# MESSENGER_ACCESS_TOKEN=token   ← từ Facebook Developer Portal

# 2. Health check
python "D:\Project\AI OS\channels\health_check.py"

# 3. Telegram (dễ nhất, không cần ngrok):
python "D:\Project\AI OS\channels\telegram_bridge.py"

# 4. Tất cả cùng lúc:
python "D:\Project\AI OS\channels\start_bridges.py"

# 5. Cần URL public cho Zalo & Facebook → chạy ngrok trước:
python "D:\Project\AI OS\channels\ngrok_connector.py"
```

| | |
|-|-|
| **Port** | 5001 (webhook server cho Zalo/FB) |
| **Cần** | Token trong `.env` (TELEGRAM_BOT_TOKEN, v.v) |
| **Kiểm tra trạng thái** | `python channels/health_check.py` |
| **Upgrade path** | PicoClaw (Go) — 8 channels incl. QQ/LINE/WeChat — xem `knowledge/claws_evaluation.md` |

---

### 🔍 LightRAG — Local RAG (Retrieval-Augmented Generation)
```bash
cd "D:\LongLeo\Project\AI OS\plugins\LightRAG"
pip install -r requirements.txt   # lần đầu
python -m lightrag.api.lightrag_server
```
| | |
|-|-|
| **Port** | 9621 (mặc định) |
| **URL** | http://localhost:9621 |
| **Cần** | Python, embedding model |

---

### 🕷️ Firecrawl — Web Crawler API
```bash
cd "D:\LongLeo\Project\AI OS\plugins\firecrawl"
npm install   # lần đầu
npm run dev
```
| | |
|-|-|
| **Port** | 3002 (mặc định) |
| **URL** | http://localhost:3002 |
| **Cần** | Node.js |

---

### 🤖 MCP Server Bridge
```bash
cd "D:\LongLeo\Project\AI OS\mcp"
# Xem README.md trong thư mục mcp/ để biết lệnh cụ thể
```
| | |
|-|-|
| **Port** | Xem mcp/README.md |
| **Cần** | Node.js hoặc Python |

---

## ⚙️ Auto-Start (Cấu hình 1 lần)

### Dùng pm2 (khởi động cùng Windows):
```bash
npm install -g pm2

# LobsterBoard
pm2 start "D:\LongLeo\Project\AI OS\plugins\LobsterBoard\server.cjs" --name lobsterboard

# Remote Bridge
pm2 start "python D:\LongLeo\Project\AI OS\channels\start_bridges.py" --name aios-channels

# Lưu để tự chạy khi khởi động Windows
pm2 startup
pm2 save
```

### Kiểm tra tất cả bằng PowerShell:
```powershell
# Xem các port đang chạy
@(19000, 3000, 3002, 5001, 9621) | ForEach-Object {
    $conn = Get-NetTCPConnection -LocalPort $_ -ErrorAction SilentlyContinue
    $status = if ($conn) { "✅ RUNNING" } else { "❌ STOPPED" }
    Write-Host "$status  port $_"
}
```

---

## 📋 Khi thêm plugin/service mới có localhost

> **Rule:** Khi nạp bất kỳ plugin nào có server/dashboard/localhost mới, BẮT BUỘC thêm vào bảng này.
>
> Template để thêm:
> ```
> ### 🔷 [Tên plugin] — [Mô tả ngắn]
> \```bash
> cd "D:\LongLeo\Project\AI OS\plugins\<name>"
> [lệnh khởi động]
> \```
> | URL | http://localhost:<port> |
> | Port | <number> |
> | Cần | [dependencies] |
> | Lý do | [tại sao dùng] |
> ```

---

*Cập nhật file này mỗi khi thêm plugin mới có yêu cầu kích hoạt.*
