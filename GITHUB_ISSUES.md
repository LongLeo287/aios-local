# GitHub Issues — AI OS Code Review
> Copy từng section dưới đây, tạo issue tại: https://github.com/LongLeo287/aios-local/issues/new

---

## ISSUE 1 of 9

**Title:** `[CRITICAL][server.js] CORS Wildcard + No Body Size Limit + No Rate Limiting`

**Labels:** `bug`, `security`

**Body:**
```
## 🔴 Critical Security Issues — `system/infra/api/server.js`

**Review date:** 2026-03-28

---

### C1 — CORS Wildcard `*` (Line 20-26)

```javascript
const CORS = {
  "Access-Control-Allow-Origin": "*",  // ← NGUY HIỂM
};
```

**Rủi ro:** Bất kỳ website nào cũng có thể gửi request đến API này → CSRF, data exfiltration.
**Fix:** Whitelist origin từ env var `ALLOWED_ORIGINS`.

---

### C2 — Không Giới Hạn Request Body Size (Line 41-48)

```javascript
req.on("data", chunk => body += chunk);  // ← Không giới hạn!
```

**Rủi ro:** Attacker gửi GB-sized request → memory exhaustion, crash toàn bộ API server.
**Fix:** Thêm `MAX_BODY_SIZE = 1MB`, destroy request nếu vượt ngưỡng.

---

### C3 — Không Có Rate Limiting / Authentication (All endpoints)

- Không có rate limiting
- Không có API key validation
- `/api/corp/escalate` có thể bị flood → file system đầy
- Các endpoint GET bị DDoS dễ dàng

**Fix:** Thêm rate-limit middleware + API key header check.
```

---

## ISSUE 2 of 9

**Title:** `[HIGH][server.js] Unvalidated Input Write to File + JSON Parse No Try-Catch + Manual YAML Parsing`

**Labels:** `bug`, `security`

**Body:**
```
## 🟠 High Issues — `system/infra/api/server.js`

**Review date:** 2026-03-28

---

### C4 — Unvalidated Input Write to File System (Line 95-105)

```javascript
const { dept, level, issue } = body;
// Không sanitize "issue"!
const entry = `\n## [${ts}] ${level} — ${dept}\n${issue}\n_Status: OPEN_\n`;
fs.writeFileSync(escPath, existing + entry);
```

**Rủi ro:** `issue` không validate về length → resource exhaustion. Injection nếu file được parse sau này.
**Fix:** Validate `issue.length <= 5000`, strip control characters.

---

### C5 — JSON Parse Không Có Try-Catch (Line 34)

```javascript
function readJson(filePath) {
  return fs.existsSync(filePath) ? JSON.parse(fs.readFileSync(filePath, "utf-8")) : null;
  //                                ↑ File bị corrupt → uncaught exception → crash server!
}
```

**Rủi ro:** `blackboard.json` hoặc `SKILL_REGISTRY.json` bị corrupt → API server crash hoàn toàn.
**Fix:** Wrap `JSON.parse` trong `try-catch`, return `null` khi lỗi.

---

### C7 — Manual YAML Parsing với Regex Lỏng (Line 137-148)

```javascript
const [k, v] = line.trim().split(": ");  // ← Value chứa ": " → split sai!
result[k] = v;                           // ← v có thể undefined → crash!
```

**Fix:** Dùng `js-yaml` npm package thay regex thủ công.

---

### L4 — parseBody() Silent Error (Line 46)

```javascript
try { resolve(JSON.parse(body)); } catch { resolve({}); }  // ← Không log gì!
```

**Impact:** Invalid JSON body được treat như empty object → subtle bugs khó debug.
**Fix:** Log warning khi parse fail.

---

### L5 — Query Parameter Filter Không Validate (Line 66-68)

```javascript
if (query.tier) entries = entries.filter(s => String(s.tier) === query.tier);
```

**Fix:** Validate `query.tier` nằm trong tập `['0','1','2','3','4']` trước khi filter.

---

### S5 — Không Có Audit Logging Cho Write Operations

`/api/corp/escalate` ghi file nhưng không log IP requester, timestamp, nội dung.
**Fix:** Ghi audit log trước khi `fs.writeFileSync()`.
```

---

## ISSUE 3 of 9

**Title:** `[HIGH][batch_repo_intake.py] Bare except: Swallows All Exceptions`

**Labels:** `bug`

**Body:**
```
## 🟠 High — `system/ops/scripts/batch_repo_intake.py`

**Review date:** 2026-03-28

### C6 — Silent Exception Swallowing (Line 86-90)

```python
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode('utf-8', errors='ignore')
except:  # ← Bare except! Nuốt MỌI lỗi kể cả KeyboardInterrupt!
    return None
```

**Rủi ro:**
- Không biết có lỗi xảy ra
- Không thể debug khi fails
- Nuốt cả `KeyboardInterrupt`, `SystemExit`

**Fix:**
```python
except (urllib.error.URLError, urllib.error.HTTPError, socket.timeout) as e:
    print(f"[WARN] Failed to fetch {owner}/{repo}: {e}", file=sys.stderr)
    return None
```

Pattern này lặp lại nhiều chỗ trong file — cần audit toàn bộ `except:` bare clauses.
```

---

## ISSUE 4 of 9

**Title:** `[HIGH][aos_integrate.py] Unvalidated CLI Arg Split + Broken .env Parser`

**Labels:** `bug`

**Body:**
```
## 🟠 High — `system/ops/scripts/aos_integrate.py`

**Review date:** 2026-03-28

### C9 — Unvalidated CLI Argument Split (Line 49)

```python
owner, repo_name = full_name.split('/')  # ← Nếu không có '/' → ValueError crash!
```

Input từ `sys.argv` không được validate trước khi unpack. Bất kỳ string không có `/` → crash.

**Fix:**
```python
if '/' not in full_name or full_name.count('/') != 1:
    print(f"[ERROR] Invalid format: '{full_name}'. Expected: owner/repo")
    continue
owner, repo_name = full_name.split('/')
```

---

### C10 — .env Parser Thiếu Sót (Line 11-17)

```python
def get_github_token():
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('GITHUB_TOKEN='):
                    return line.strip().split('=', 1)[1]
    return None
```

**Vấn đề:**
- Không skip comment lines bắt đầu bằng `#`
- Không skip blank lines
- `GITHUB_TOKEN=` (empty value) → return `""` — truthy nhưng invalid
- Không có error handling nếu file read fail

**Fix:** Dùng `python-dotenv` library hoặc thêm proper validation.
```

---

## ISSUE 5 of 9

**Title:** `[HIGH][sync_identity_1_1.js] Hardcoded Placeholder <AI_OS_ROOT> Never Replaced`

**Labels:** `bug`

**Body:**
```
## 🟠 High — `system/ops/scripts/sync_identity_1_1.js`

**Review date:** 2026-03-28

### C8 — Hardcoded Placeholder (Line 4)

```javascript
const rootDir = '<AI_OS_ROOT>';  // ← Template placeholder chưa được thay thế!
```

Script này sẽ **fail hoàn toàn** khi chạy vì `<AI_OS_ROOT>` không phải path hợp lệ trên bất kỳ OS nào.

**Fix Option A** (dynamic):
```javascript
const rootDir = path.resolve(__dirname, '../../..');
```

**Fix Option B** (env-based):
```javascript
const rootDir = process.env.AI_OS_ROOT || path.resolve(__dirname, '../../..');
```

Cần audit toàn bộ codebase tìm các placeholder `<AI_OS_ROOT>` chưa được replace khác.
```

---

## ISSUE 6 of 9

**Title:** `[MEDIUM][aios_orchestrator.py] Silent LTM Module Import Failure`

**Labels:** `bug`

**Body:**
```
## 🟡 Medium — `system/ops/aios_orchestrator.py`

**Review date:** 2026-03-28

### L1 — Silent Module Import Failure (Line 27-37)

```python
try:
    from system.ops.scripts.memory_daemon import MemoryCore as _MemoryCore
    from system.ops.scripts.agent_bus import AgentBus as _AgentBus
    _MEMORY_CORE = _MemoryCore()
    _AGENT_BUS   = _AgentBus()
    _LTM_ONLINE  = True
except Exception as _e:
    _LTM_ONLINE = False   # ← _e bị nuốt hoàn toàn, không ai biết tại sao LTM offline!
    _MEMORY_CORE = None
    _AGENT_BUS   = None
```

Graceful degradation là tốt, nhưng việc không log exception khiến việc debug rất khó khi LTM bị offline trong production.

**Fix:**
```python
except Exception as _e:
    import sys
    print(f"[WARN] LTM components unavailable: {type(_e).__name__}: {_e}", file=sys.stderr)
    _LTM_ONLINE = False
    _MEMORY_CORE = None
    _AGENT_BUS   = None
```
```

---

## ISSUE 7 of 9

**Title:** `[MEDIUM][system_pulse.py] Telegram Credentials Not Validated + No Message Length Check`

**Labels:** `bug`

**Body:**
```
## 🟡 Medium — `system/automations/daemons/system_pulse.py`

**Review date:** 2026-03-28

### L2 — Telegram Credentials Không Validate (Line 42-43)

```python
TOKEN   = _ENV.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = _ENV.get("TELEGRAM_CHAT_ID", "")
```

Khi `TOKEN=""`, `send_telegram()` vẫn được gọi và tạo URL invalid → Telegram API reject với HTTP error nhưng không ai biết.

**Fix:**
```python
TOKEN   = _ENV.get("TELEGRAM_BOT_TOKEN") or ""
CHAT_ID = _ENV.get("TELEGRAM_CHAT_ID") or ""
if not TOKEN or not CHAT_ID:
    print("[WARN] Telegram credentials not configured. Alerts disabled.", file=sys.stderr)
```

---

### L3 — Message Length Không Validate (Line 89-101)

Telegram API giới hạn 4096 ký tự/message. Nếu message dài hơn → API reject silently, alert bị mất.

**Fix:**
```python
def send_telegram(text: str):
    if not TOKEN or not CHAT_ID:
        return
    if len(text) > 4096:
        text = text[:4093] + "..."
    # ... rest of function
```
```

---

## ISSUE 8 of 9

**Title:** `[MEDIUM][SKILL_REGISTRY.json] dependabot-secretary skill exists on disk but not registered`

**Labels:** `bug`, `documentation`

**Body:**
```
## 🟡 Medium — `brain/shared-context/SKILL_REGISTRY.json`

**Review date:** 2026-03-28

### S2 — Skill Registry Mismatch

| | Count |
|---|---|
| Skills trên disk (`ecosystem/skills/`) | 29 |
| Skills trong registry | 28 |
| **Thiếu** | **1** |

**Skill bị thiếu:** `dependabot-secretary`
- File tồn tại: `ecosystem/skills/dependabot-secretary/SKILL.md` ✅
- Trong SKILL_REGISTRY.json: ❌ KHÔNG CÓ

**Impact:** Skill này không thể được discover tự động bởi agent routing engine.

**Fix:** Thêm entry cho `dependabot-secretary` vào `brain/shared-context/SKILL_REGISTRY.json` với đầy đủ fields: `id`, `name`, `description`, `tier`, `category`, `status`, `path`.
```

---

## ISSUE 9 of 9

**Title:** `[MEDIUM][CLAUDE.md] Missing CLAUDE_CODE_TASKS.md + UTF-8 Encoding Corruption`

**Labels:** `bug`, `documentation`

**Body:**
```
## 🟡 Medium — `CLAUDE.md` + `.clauderules`

**Review date:** 2026-03-28

### S1 — CLAUDE_CODE_TASKS.md Bị Thiếu

`CLAUDE.md` Step 9 yêu cầu:
> ⚡ READ & AUTO-EXECUTE TASK QUEUE [CLAUDE_CODE_TASKS.md]

Nhưng file này **KHÔNG TỒN TẠI** trong repo.

Mỗi lần boot → fallback mechanism được trigger → warning logged → CEO cần được thông báo.

**Fix:** Một trong hai:
1. Tạo `CLAUDE_CODE_TASKS.md` với template rỗng (preferred)
2. Remove/comment out reference trong `CLAUDE.md` Step 9

---

### S4 — UTF-8 Encoding Corruption

**Files bị ảnh hưởng:** `CLAUDE.md`, `.clauderules`

Ký tự tiếng Việt/Unicode bị garble:
- `→` hiển thị thành `Ã¢â€â€™`
- `—` hiển thị thành `Ã¢â‚¬â€œ`
- `✅` bị corrupt thành multi-byte garbage

**Nguyên nhân:** Files được lưu với encoding Windows-1252 hoặc Latin-1, sau đó re-read as UTF-8.

**Impact:** Boot protocols và governance rules có thể bị misread bởi tools xử lý text (CI/CD, grep, diff tools).

**Fix:** Convert toàn bộ sang UTF-8 without BOM:
```bash
# PowerShell
Get-Content CLAUDE.md -Encoding UTF8 | Set-Content CLAUDE.md -Encoding UTF8NoBOM
```
```

---

## TÓM TẮT

| # | File | Severity | Issues |
|---|------|----------|--------|
| 1 | `system/infra/api/server.js` | 🔴 Critical | CORS wildcard, no body limit, no rate limiting |
| 2 | `system/infra/api/server.js` | 🟠 High | Unvalidated file write, JSON parse no try-catch, manual YAML |
| 3 | `system/ops/scripts/batch_repo_intake.py` | 🟠 High | Bare except swallows all errors |
| 4 | `system/ops/scripts/aos_integrate.py` | 🟠 High | Split crash, broken .env parser |
| 5 | `system/ops/scripts/sync_identity_1_1.js` | 🟠 High | Hardcoded `<AI_OS_ROOT>` placeholder |
| 6 | `system/ops/aios_orchestrator.py` | 🟡 Medium | Silent LTM import failure |
| 7 | `system/automations/daemons/system_pulse.py` | 🟡 Medium | Telegram no validation |
| 8 | `brain/shared-context/SKILL_REGISTRY.json` | 🟡 Medium | dependabot-secretary unregistered |
| 9 | `CLAUDE.md` + `.clauderules` | 🟡 Medium | Missing boot file + UTF-8 corruption |

**Tổng:** 5 Critical, 6 High, 8 Medium issues
