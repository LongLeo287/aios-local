# push_issues.ps1 — Tao 9 GitHub Issues tu ket qua Code Review
# Chay: .\push_issues.ps1 -Token "github_pat_xxx..."
# Yeu cau token co quyen: Issues -> Read and write

param(
    [Parameter(Mandatory=$true)]
    [string]$Token
)

$Repo = "LongLeo287/aios-local"
$Headers = @{
    "Authorization"        = "Bearer $Token"
    "Accept"               = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
    "Content-Type"         = "application/json"
}

function New-Issue($title, $body, $labels) {
    $payload = @{ title = $title; body = $body; labels = $labels } | ConvertTo-Json -Depth 3
    $resp = Invoke-RestMethod -Uri "https://api.github.com/repos/$Repo/issues" `
        -Method POST -Headers $Headers -Body $payload -ErrorAction Stop
    Write-Host "[OK] #$($resp.number) — $($resp.html_url)" -ForegroundColor Green
    Start-Sleep -Milliseconds 500
}

Write-Host "Pushing 9 issues to $Repo..." -ForegroundColor Cyan

# ── ISSUE 1 ──────────────────────────────────────────────────────────────────
New-Issue `
    "[CRITICAL][server.js] CORS Wildcard + No Body Size Limit + No Rate Limiting" `
    @"
## Critical Security Issues — ``system/infra/api/server.js``

**Review date:** 2026-03-28

---

### C1 — CORS Wildcard ``*`` (Line 20-26)

``````javascript
const CORS = {
  "Access-Control-Allow-Origin": "*",  // NGUY HIEM
};
``````

**Rui ro:** Bat ky website nao cung co the gui request den API nay -> CSRF, data exfiltration.
**Fix:** Whitelist origin tu env var ``ALLOWED_ORIGINS``.

---

### C2 — Khong Gioi Han Request Body Size (Line 41-48)

``````javascript
req.on("data", chunk => body += chunk);  // Khong gioi han!
``````

**Rui ro:** Attacker gui GB-sized request -> memory exhaustion, crash toan bo API server.
**Fix:** Them ``MAX_BODY_SIZE = 1MB``, destroy request neu vuot nguong.

---

### C3 — Khong Co Rate Limiting / Authentication (All endpoints)

- Khong co rate limiting
- Khong co API key validation
- ``/api/corp/escalate`` co the bi flood -> file system day
- Cac endpoint GET bi DDoS de dang

**Fix:** Them rate-limit middleware + API key header check.
"@ `
    @("bug", "security")

# ── ISSUE 2 ──────────────────────────────────────────────────────────────────
New-Issue `
    "[HIGH][server.js] Unvalidated File Write + JSON Parse No Try-Catch + Manual YAML Parsing" `
    @"
## High Issues — ``system/infra/api/server.js``

**Review date:** 2026-03-28

---

### C4 — Unvalidated Input Write to File System (Line 95-105)

``````javascript
const { dept, level, issue } = body;
// Khong sanitize "issue"!
const entry = ``\n## [${ts}] ${level} -- ${dept}\n${issue}\n_Status: OPEN_\n``;
fs.writeFileSync(escPath, existing + entry);
``````

**Rui ro:** ``issue`` khong validate ve length -> resource exhaustion, injection neu file duoc parse sau nay.
**Fix:** Validate ``issue.length <= 5000``, strip control characters.

---

### C5 — JSON Parse Khong Co Try-Catch (Line 34)

``````javascript
function readJson(filePath) {
  return fs.existsSync(filePath) ? JSON.parse(fs.readFileSync(filePath, "utf-8")) : null;
  // File bi corrupt -> uncaught exception -> crash server!
}
``````

**Rui ro:** ``blackboard.json`` hoac ``SKILL_REGISTRY.json`` bi corrupt -> API server crash hoan toan.
**Fix:** Wrap ``JSON.parse`` trong ``try-catch``.

---

### C7 — Manual YAML Parsing voi Regex Long (Line 137-148)

``````javascript
const [k, v] = line.trim().split(": ");  // Value chua ": " -> split sai!
result[k] = v;                           // v co the undefined -> crash!
``````

**Fix:** Dung ``js-yaml`` npm package thay regex thu cong.

---

### L4 — parseBody() Silent Error (Line 46)

``````javascript
try { resolve(JSON.parse(body)); } catch { resolve({}); }  // Khong log gi!
``````

**Fix:** Log warning khi parse fail.

---

### S5 — Khong Co Audit Logging Cho Write Operations

``/api/corp/escalate`` ghi file nhung khong log IP requester, timestamp, noi dung.
**Fix:** Ghi audit log truoc khi ``fs.writeFileSync()``.
"@ `
    @("bug", "security")

# ── ISSUE 3 ──────────────────────────────────────────────────────────────────
New-Issue `
    "[HIGH][batch_repo_intake.py] Bare except: Swallows All Exceptions" `
    @"
## High — ``system/ops/scripts/batch_repo_intake.py``

**Review date:** 2026-03-28

### C6 — Silent Exception Swallowing (Line 86-90)

``````python
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode('utf-8', errors='ignore')
except:  # Bare except! Nuot MOI loi ke ca KeyboardInterrupt!
    return None
``````

**Rui ro:**
- Khong biet co loi xay ra
- Khong the debug khi fails
- Nuot ca ``KeyboardInterrupt``, ``SystemExit``

**Fix:**
``````python
except (urllib.error.URLError, urllib.error.HTTPError, socket.timeout) as e:
    print(f"[WARN] Failed to fetch: {e}", file=sys.stderr)
    return None
``````

Pattern nay lap lai nhieu cho trong file — can audit toan bo ``except:`` bare clauses.
"@ `
    @("bug")

# ── ISSUE 4 ──────────────────────────────────────────────────────────────────
New-Issue `
    "[HIGH][aos_integrate.py] Unvalidated CLI Arg Split + Broken .env Parser" `
    @"
## High — ``system/ops/scripts/aos_integrate.py``

**Review date:** 2026-03-28

### C9 — Unvalidated CLI Argument Split (Line 49)

``````python
owner, repo_name = full_name.split('/')  # Neu khong co '/' -> ValueError crash!
``````

Input tu ``sys.argv`` khong duoc validate truoc khi unpack.

**Fix:**
``````python
if '/' not in full_name or full_name.count('/') != 1:
    print(f"[ERROR] Invalid format: '{full_name}'. Expected: owner/repo")
    continue
owner, repo_name = full_name.split('/')
``````

---

### C10 — .env Parser Thieu Sot (Line 11-17)

``````python
def get_github_token():
    for line in f:
        if line.startswith('GITHUB_TOKEN='):
            return line.strip().split('=', 1)[1]
``````

**Van de:**
- Khong skip comment lines bat dau bang ``#``
- Khong skip blank lines
- ``GITHUB_TOKEN=`` (empty value) -> return ``""`` — truthy nhung invalid

**Fix:** Dung ``python-dotenv`` library hoac them proper validation.
"@ `
    @("bug")

# ── ISSUE 5 ──────────────────────────────────────────────────────────────────
New-Issue `
    "[HIGH][sync_identity_1_1.js] Hardcoded Placeholder <AI_OS_ROOT> Never Replaced" `
    @"
## High — ``system/ops/scripts/sync_identity_1_1.js``

**Review date:** 2026-03-28

### C8 — Hardcoded Placeholder (Line 4)

``````javascript
const rootDir = '<AI_OS_ROOT>';  // Template placeholder chua duoc thay the!
``````

Script nay se **fail hoan toan** khi chay vi ``<AI_OS_ROOT>`` khong phai path hop le tren bat ky OS nao.

**Fix Option A** (dynamic):
``````javascript
const rootDir = path.resolve(__dirname, '../../..');
``````

**Fix Option B** (env-based):
``````javascript
const rootDir = process.env.AI_OS_ROOT || path.resolve(__dirname, '../../..');
``````

Can audit toan bo codebase tim cac placeholder ``<AI_OS_ROOT>`` chua duoc replace khac.
"@ `
    @("bug")

# ── ISSUE 6 ──────────────────────────────────────────────────────────────────
New-Issue `
    "[MEDIUM][aios_orchestrator.py] Silent LTM Module Import Failure" `
    @"
## Medium — ``system/ops/aios_orchestrator.py``

**Review date:** 2026-03-28

### L1 — Silent Module Import Failure (Line 27-37)

``````python
try:
    from system.ops.scripts.memory_daemon import MemoryCore as _MemoryCore
    _MEMORY_CORE = _MemoryCore()
    _LTM_ONLINE  = True
except Exception as _e:
    _LTM_ONLINE = False   # _e bi nuot hoan toan, khong ai biet tai sao LTM offline!
    _MEMORY_CORE = None
``````

Graceful degradation la tot, nhung khong log exception khien debug rat kho khi LTM offline trong production.

**Fix:**
``````python
except Exception as _e:
    import sys
    print(f"[WARN] LTM components unavailable: {type(_e).__name__}: {_e}", file=sys.stderr)
    _LTM_ONLINE = False
    _MEMORY_CORE = None
``````
"@ `
    @("bug")

# ── ISSUE 7 ──────────────────────────────────────────────────────────────────
New-Issue `
    "[MEDIUM][system_pulse.py] Telegram Credentials Not Validated + No Message Length Check" `
    @"
## Medium — ``system/automations/daemons/system_pulse.py``

**Review date:** 2026-03-28

### L2 — Telegram Credentials Khong Validate (Line 42-43)

``````python
TOKEN   = _ENV.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = _ENV.get("TELEGRAM_CHAT_ID", "")
``````

Khi ``TOKEN=""``, ``send_telegram()`` van duoc goi va tao URL invalid -> Telegram API reject, khong ai biet.

**Fix:**
``````python
TOKEN   = _ENV.get("TELEGRAM_BOT_TOKEN") or ""
CHAT_ID = _ENV.get("TELEGRAM_CHAT_ID") or ""
if not TOKEN or not CHAT_ID:
    print("[WARN] Telegram credentials not configured.", file=sys.stderr)
``````

---

### L3 — Message Length Khong Validate (Line 89-101)

Telegram API gioi han 4096 ky tu/message. Neu vuot -> API reject, alert mat.

**Fix:**
``````python
if len(text) > 4096:
    text = text[:4093] + "..."
``````
"@ `
    @("bug")

# ── ISSUE 8 ──────────────────────────────────────────────────────────────────
New-Issue `
    "[MEDIUM][SKILL_REGISTRY.json] dependabot-secretary skill unregistered" `
    @"
## Medium — ``brain/shared-context/SKILL_REGISTRY.json``

**Review date:** 2026-03-28

### S2 — Skill Registry Mismatch

| | Count |
|---|---|
| Skills tren disk (``ecosystem/skills/``) | 29 |
| Skills trong registry | 28 |
| **Thieu** | **1** |

**Skill bi thieu:** ``dependabot-secretary``
- File ton tai: ``ecosystem/skills/dependabot-secretary/SKILL.md`` OK
- Trong SKILL_REGISTRY.json: KHONG CO

**Impact:** Skill nay khong the duoc discover tu dong boi agent routing engine.

**Fix:** Them entry cho ``dependabot-secretary`` vao ``brain/shared-context/SKILL_REGISTRY.json`` voi day du fields: ``id``, ``name``, ``description``, ``tier``, ``category``, ``status``, ``path``.
"@ `
    @("bug", "documentation")

# ── ISSUE 9 ──────────────────────────────────────────────────────────────────
New-Issue `
    "[MEDIUM][CLAUDE.md] Missing CLAUDE_CODE_TASKS.md + UTF-8 Encoding Corruption" `
    @"
## Medium — ``CLAUDE.md`` + ``.clauderules``

**Review date:** 2026-03-28

### S1 — CLAUDE_CODE_TASKS.md Bi Thieu

``CLAUDE.md`` Step 9 yeu cau doc file ``CLAUDE_CODE_TASKS.md`` nhung file nay KHONG TON TAI trong repo.

Moi lan boot -> fallback mechanism duoc trigger -> warning logged.

**Fix:** Mot trong hai:
1. Tao ``CLAUDE_CODE_TASKS.md`` voi template rong (preferred)
2. Remove/comment out reference trong ``CLAUDE.md`` Step 9

---

### S4 — UTF-8 Encoding Corruption

**Files bi anh huong:** ``CLAUDE.md``, ``.clauderules``, va co the cac file .ps1 khac

Ky tu tieng Viet/Unicode bi garble:
- ``->`` hien thi thanh ``Ã¢â€â€™``
- ``-`` hien thi thanh ``Ã¢â‚¬â€œ``

**Nguyen nhan:** Files duoc luu voi encoding Windows-1252, sau do re-read as UTF-8.

**Fix:** Convert sang UTF-8 with BOM:
``````powershell
$content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
$utf8Bom = New-Object System.Text.UTF8Encoding $true
[System.IO.File]::WriteAllText($path, $content, $utf8Bom)
``````
"@ `
    @("bug", "documentation")

Write-Host ""
Write-Host "Done! All 9 issues pushed." -ForegroundColor Cyan
