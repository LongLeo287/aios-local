---
source: https://github.com/ringhyacinth/Star-Office-UI
ingested_at: 2026-03-15T04:44:00+07:00
domain: AI|Frontend|Multi-Agent|UI-UX|Security
trust_level: HIGH
vet_status: PASS (Read-only web fetch + raw source code analysis)
license: MIT (Code) | Non-Commercial (Art Assets)
stars: 4.7K | forks: 530 | watchers: 23
authors: Ring Hyacinth (@ring_hyacinth), Simon Lee (@simonxxoo) + 3 contributors
stack: Python/Flask + Vanilla HTML/JS + Phaser (game engine) + Electron (optional)
---

# Star Office UI — Deep Technical Analysis

## Tổng quan

Star Office UI là **pixel-art AI agent dashboard** biến trạng thái làm việc của AI Agent thành không gian văn phòng ảo sinh động.
Tích hợp sâu với OpenClaw, nhưng hoạt động độc lập hoàn toàn nếu không có OpenClaw.

---

## Architecture (Backend)

### Tech Stack
- **Backend:** Python 3 / Flask (lightweight REST API)
- **Frontend:** HTML + Vanilla JS + Phaser.js (pixel-art game engine)
- **Optional:** Electron (desktop widget mode)
- **State Storage:** Simple JSON files (không cần DB)
- **Image Gen:** Gemini API (optional, isolated `venv`)

### Module Structure (Tách biệt rõ ràng)
```
backend/
├── app.py              # Core Flask app + all route handlers
├── security_utils.py   # Password validation, production detection
├── memo_utils.py        # PII redaction + memory file parsing
└── store_utils.py       # File I/O helpers (state, agents, assets, config)
```

### State Machine (6 trạng thái canonical)
```python
VALID_AGENT_STATES = frozenset({"idle", "writing", "researching", "executing", "syncing", "error"})
WORKING_STATES = frozenset({"writing", "researching", "executing"})  # auto-idle TTL áp dụng ở đây
STATE_TO_AREA_MAP = {
    "idle":        "breakroom",
    "writing":     "writing",
    "researching": "writing",
    "executing":   "writing",
    "syncing":     "writing",
    "error":       "error",
}
```
→ **Single source of truth** — Chỉ một nơi duy nhất define states. Rất sạch.

### Concurrency Protection (Thread Safety)
```python
join_lock = threading.Lock()
# Guard join-agent critical section to enforce per-key concurrency under parallel requests
```
→ Dùng threading.Lock để tránh race condition khi nhiều Guest Agent join cùng lúc.

---

## API Reference (đầy đủ)

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/health` | GET | Health check |
| `/status` | GET | Lấy trạng thái agent chính |
| `/set_state` | POST | Đặt trạng thái agent chính |
| `/agents` | GET | Danh sách tất cả agents trong office |
| `/join-agent` | POST | Guest Agent tham gia office |
| `/agent-push` | POST | Guest Agent đẩy trạng thái mới |
| `/leave-agent` | POST | Guest Agent rời office |
| `/yesterday-memo` | GET | Lấy "Nhật ký hôm qua" |
| `/config/gemini` | GET/POST | Quản lý Gemini API key |
| `/assets/generate-rpg-background/poll` | GET | Polling tiến trình tạo ảnh AI |

### State Push Pattern (cực kỳ đơn giản)
```python
# set_state.py → HTTP POST → backend ghi vào state.json → frontend polling → cập nhật UI
POST /set_state
{"state": "researching"}  # hoặc bất kỳ state nào trong VALID_AGENT_STATES
```

---

## Security Implementation (Đáng học)

### 1. `security_utils.py` — Sạch và tái sử dụng được
```python
def is_production_mode() -> bool:
    env = (os.getenv("STAR_OFFICE_ENV") or os.getenv("FLASK_ENV") or "").strip().lower()
    return env in {"prod", "production"}

def is_strong_secret(secret: str) -> bool:
    # Tối thiểu 24 ký tự + không chứa từ yếu
    weak_markers = {"change-me", "dev", "example", "test", "default"}
    return len(secret) >= 24 and not any(m in secret.lower() for m in weak_markers)

def is_strong_drawer_pass(pwd: str) -> bool:
    return pwd != "1234" and len(pwd) >= 8
```
→ Rất clean, unit-testable. Tách biệt validation logic khỏi route handler.

### 2. Session Hardening
```python
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=is_production_mode(),  # chỉ bật HTTPS trong production
    PERMANENT_SESSION_LIFETIME=timedelta(hours=12),
)
```

### 3. Secret Key Strategy
```python
app.secret_key = (
    os.getenv("FLASK_SECRET_KEY") 
    or os.getenv("STAR_OFFICE_SECRET") 
    or "star-office-dev-secret-change-me"
)
```
→ Dev có thể chạy ngay, production phải đặt env var.

---

## Memory Integration (Kết nối với `memory/*.md`)

### `memo_utils.py` — PII Redaction
Hệ thống tự động đọc file nhật ký từ `memory/*.md` (ngày hôm qua) và hiển thị bản tóm tắt đã được **redact PII**:

```python
def sanitize_content(text: str) -> str:
    text = re.sub(r'ou_[a-f0-9]+', '[用户]', text)        # OpenID
    text = re.sub(r'user_id="[^"]+"', 'user_id="[隐藏]"', text)
    text = re.sub(r'/root/[^"\s]+', '[路径]', text)        # File paths
    text = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '[IP]', text)
    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[邮箱]', text)
    text = re.sub(r'1[3-9]\d{9}', '[手机号]', text)
    return text
```

### Memory File Reading Strategy
```python
MEMORY_DIR = os.path.join(os.path.dirname(ROOT_DIR), "memory")  # ../memory/*.md
```
→ Đọc từ thư mục `memory/` nằm ngoài gốc project. **Khớp với AI OS memory pattern.**

### "Yesterday Memo" Display Logic
1. Lấy ngày hôm qua (`get_yesterday_date_str()`)
2. Tìm file `.md` tương ứng trong `memory/`
3. Parse: bỏ headers (`#`), lấy bullet points và dòng > 10 ký tự
4. Redact PII, truncate > 40 ký tự
5. Thêm một câu danh ngôn ngẫu nhiên từ "kho trí tuệ" 10 câu
6. Hiển thị lên card "Hôm qua đã làm gì"

---

## SKILL.md — OpenClaw Convention (Tương đồng AI OS)

SKILL.md trong Star Office UI là một bộ chỉ dẫn cho OpenClaw Agent:
- Giải thích một câu "Đây là gì"
- Hướng dẫn agent tự deploy từng bước
- Chỉ định cách đặt cấu hình, bảo mật
- Hướng dẫn mời Guest Agent tham gia

**Đây chính là pattern AI OS Skill đang dùng, xác nhận chúng ta đi đúng hướng.**

---

## Điểm Mạnh (Học từ đây)

| Điểm mạnh | Mô tả |
|-----------|-------|
| **State Machine đơn giản** | frozenset + dict map — Không over-engineer |
| **Security Module tách biệt** | `security_utils.py` — Testable, reusable |
| **PII Redaction** | `memo_utils.py` — Regex-based, hiệu quả |
| **Thread Safety** | threading.Lock cho join endpoint |
| **Cloudflare Tunnel** | Simple public access solution |
| **Polling thay vì WebSocket** | Frontend polling đơn giản, không cần infra phức tạp |
| **Env-based production detection** | Không hardcode env, linh hoạt |
| **Modular utilities** | security_utils, memo_utils, store_utils — dễ test riêng |

## Điểm Yếu / Giới Hạn

| Giới hạn | Ghi chú |
|----------|---------|
| **No DB** | State lưu trong JSON — OK cho 1 agent, có thể có race condition nếu nhiều agent ghi đồng thời |
| **Polling thay vì Push** | Frontend poll mỗi X giây — không realtime thực sự |
| **Art assets non-commercial** | Không dùng được trong sản phẩm thương mại |
| **Desktop Pet thử nghiệm** | macOS-centric, chưa stable trên Windows |
| **Gemini API phụ thuộc** | AI room design chỉ hoạt động với Gemini key |

---

## Áp Dụng Vào AI OS

| Concept | Cách áp dụng |
|---------|--------------|
| **State API Pattern** | Thêm `/set_state` endpoint vào AI OS để track Agent mode |
| **Memory→Daily Card** | Đọc `memory/daily/*.md` → hiển thị "Yesterday" summary khi boot |
| **PII Redaction** | Áp dụng `sanitize_content()` vào AI OS khi render memory cho user |
| **Security Utils** | Copy pattern `security_utils.py` → tạo `scripts/security_helpers.ps1` |
| **Threading Lock** | Áp dụng mutex/lock khi nhiều Agent cùng write blackboard |
| **SKILL.md Doc Pattern** | Đã confirm convention, AI OS skills đang đúng hướng |

---

## References
- [GitHub Repo](https://github.com/ringhyacinth/Star-Office-UI)
- [English README](https://github.com/ringhyacinth/Star-Office-UI/blob/master/README.en.md)
- [Backend source: app.py](https://github.com/ringhyacinth/Star-Office-UI/blob/master/backend/app.py)
- [Backend source: security_utils.py](https://github.com/ringhyacinth/Star-Office-UI/blob/master/backend/security_utils.py)
- [Backend source: memo_utils.py](https://github.com/ringhyacinth/Star-Office-UI/blob/master/backend/memo_utils.py)
- [SKILL.md](https://github.com/ringhyacinth/Star-Office-UI/blob/master/SKILL.md)
- [Changelog March 2026](https://github.com/ringhyacinth/Star-Office-UI/blob/master/docs/CHANGELOG_2026-03.md)
