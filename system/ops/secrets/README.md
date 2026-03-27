# =============================================================
# ops/secrets/README.md — Hướng Dẫn Quản Lý Secrets
# =============================================================

## Cấu trúc

```
ops/secrets/
├── MASTER.env          ← Nguồn duy nhất chứa mọi API keys (gitignored)
├── MASTER.env.dpapi    ← Phiên bản mã hoá DPAPI (gitignored)
├── MASTER.env.example  ← Template không có keys thật (có thể commit)
├── encrypt.ps1         ← Mã hoá MASTER.env → MASTER.env.dpapi
├── decrypt.ps1         ← Giải mã + load vào $env:*
├── load-env.ps1        ← Tiện ích cho các script khác import
└── README.md           ← File này
```

---

## Workflow cơ bản

### Lần đầu setup:
```powershell
# Điền keys vào MASTER.env, sau đó mã hoá:
.\ops\secrets\encrypt.ps1
```

### Khi cần thêm / sửa key:
```powershell
# 1. Sửa MASTER.env (plaintext)
# 2. Chạy lại encrypt để cập nhật .dpapi
.\ops\secrets\encrypt.ps1
```

### Load secrets vào terminal:
```powershell
# Dot-source để load vào session hiện tại:
. .\ops\secrets\load-env.ps1

# Kiểm tra:
echo $env:TELEGRAM_BOT_TOKEN
```

### Dùng trong PowerShell script khác:
```powershell
# Ở đầu script, trước khi dùng bất kỳ key nào:
$AiOsRoot = (Resolve-Path (Join-Path $PSScriptRoot ".." "..")).Path
. "$AiOsRoot\ops\secrets\load-env.ps1"

# Sau đó dùng trực tiếp:
$token = $env:TELEGRAM_BOT_TOKEN
```

---

## Bảo mật

| Cơ chế | Mô tả |
|---------|--------|
| **DPAPI** | Windows user-level encryption. Chỉ user đã encrypt mới decrypt được |
| **.gitignore** | `MASTER.env` và `*.dpapi` không bao giờ commit lên git |
| **.claudeignore** | Claude Code không đọc được thư mục này |
| **Scope** | `CurrentUser` — không chia sẻ được dù trên cùng máy |

> ⚠️ MASTER.env.dpapi KHÔNG portable — không thể copy sang máy khác và decrypt.
> Khi đổi máy, cần nhập lại keys vào MASTER.env mới trên máy đó.
