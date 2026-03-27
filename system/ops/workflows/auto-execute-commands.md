# Department: operations
---
description: Khi CEO đưa ra danh sách commands — tự phân loại, tự chạy, tự đưa vào HUD
---
# ops/workflows/auto-execute-commands.md
# Version: 1.0 | 2026-03-25 | Owner: Antigravity
# Trigger: CEO paste/list commands và nói "tự làm" / "thêm vào hệ thống" / "bạn tự xử lý"

---

## BƯỚC 1 — PHÂN LOẠI COMMAND

Khi CEO đưa ra danh sách commands, Antigravity phân loại ngay:

| Loại | Dấu hiệu | Action |
|------|---------|--------|
| **ONE-TIME** | `--write`, `--fix`, `install`, setup script, migration | ✅ Tự chạy ngay (`SafeToAutoRun: true`) |
| **LONG-RUNNING** | `start_bridges`, `lightrag_server`, server, watch, polling | 🔄 Start background + thêm vào HUD |
| **CLI VERIFY** | `aos.py status`, `aos.py corp start`, health check | ✅ Tự chạy để verify |
| **PANEL ITEM** | Tất cả commands → đều thêm vào `hud/HUD.md` BẢNG ĐIỀU KHIỂN | 📋 Luôn thêm vào HUD |
| **UNSAFE** | `rm -rf`, `drop table`, delete, format, overwrite secrets | ❌ KHÔNG tự chạy — hỏi CEO |

---

## BƯỚC 2 — EXECUTION ORDER

```
1. ONE-TIME scripts → chạy ngay (SafeToAutoRun)
2. CLI VERIFY → chạy để confirm output
3. LONG-RUNNING → start background terminal (nếu cần)
4. TẤT CẢ commands → thêm vào HUD.md BẢNG ĐIỀU KHIỂN
```

---

## BƯỚC 3 — THÊM VÀO HUD

Mọi command CEO đề cập → luôn thêm vào `hud/HUD.md` section phù hợp:

```markdown
### <Category>
| Action | Command | Mô tả |
|--------|---------|-------|
| 🚀/🔄/🎯 **Name** | `command here` | Giải thích ngắn |
```

**Category rules:**
- Corp Cycle → commands `aos.py corp *`
- Telegram/Bridge → commands `start_bridges.py`, bot, notification
- System Maintenance → fix scripts, install, tier, index, hud
- Knowledge/CIV → intake, ingest, crawler

---

## BƯỚC 4 — GHI NHẬN

Sau khi chạy xong:
- ✅ Log vào `telemetry/receipts/cmd_execution_<date>.md`
- ✅ Update `blackboard.json` nếu command thay đổi system state
- ✅ Notify CEO với bảng tóm tắt: command → kết quả

---

## VÍ DỤ THỰC TẾ (2026-03-25)

CEO paste:
```
python fix_skill_tiers.py --write      → ONE-TIME → tự chạy
powershell install_vscode_extensions   → ONE-TIME → tự chạy
python start_bridges.py                → LONG-RUNNING → background + HUD
python aos.py corp start               → CLI VERIFY → tự chạy
```

Antigravity làm:
1. Chạy fix_skill_tiers.py --write (2758 skills fixed ✅)
2. Chạy install_vscode_extensions.ps1 (skip nếu `code` CLI không có)
3. Thêm start_bridges vào HUD.md "Telegram Bridge" section
4. Test `aos.py status` → output verified ✅
5. Báo kết quả cho CEO

---

*Workflow v1.0 | Trigger: "bạn tự làm" / "thêm vào hệ thống" / CEO paste list commands*


---

## HANDOFF — TỰ ĐỘNG, KHÔNG CẦN CEO RA LỆNH

> Khi phát hiện session đang kết thúc, Antigravity TỰ ĐỘNG chạy post-session.md

**Trigger signals:**
- CEO nói: "kết thúc phiên" / "tạm biệt" / "xong rồi" / "end session"
- Task hoàn thành và CEO không hỏi thêm
- Phiên mới bắt đầu (handoff phiên cũ trước)

**Không cần CEO nói:** "handoff" / "update HUD" / "cập nhật blackboard"

Ref: ops/workflows/post-session.md
