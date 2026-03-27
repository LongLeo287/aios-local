"""
Master Repo Catalog Builder — Phase 27
Owner: Antigravity + Dept 20 CIV + Dept 00 OPS

Mục tiêu:
1. Cross-check 1651 repos đã phân tích với ecosystem/plugins (34 repos đang active)
2. Tạo 3 kho:
   - ⭐ ACTIVE (repo đang dùng trong AI OS - đánh dấu sao, luôn update)
   - 🔖 PENDING (APPROVE nhưng chưa cài - xếp hàng chờ CEO)
   - ❌ ARCHIVED (REJECT/DEFER - gom về 1 nơi để CEO xem xét lại)
3. Tạo Catalog chính: ecosystem/plugins/MASTER_REPO_CATALOG.md
4. Update plugin-catalog.md với trạng thái ⭐ cho repos active
"""
import os, json, datetime, re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
PLUGINS_DIR = os.path.join(BASE_DIR, 'ecosystem', 'plugins')
VAULT_DATA = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA')
FULL_REPORT = os.path.join(VAULT_DATA, 'repo_intake_report_API_b1651_2026-03-27.md')
CATALOG_OUT = os.path.join(PLUGINS_DIR, 'MASTER_REPO_CATALOG.md')
ACTIVE_OUT = os.path.join(VAULT_DATA, 'ACTIVE_REPOS.md')
PENDING_OUT = os.path.join(VAULT_DATA, 'PENDING_REPOS.md')
ARCHIVED_OUT = os.path.join(VAULT_DATA, 'ARCHIVED_REPOS.md')

# ── 1. Detect ACTIVE repos from filesystem ──────────────────────────────────
def get_active_plugins():
    """Scan ecosystem/plugins for installed plugins"""
    active = {}
    if not os.path.exists(PLUGINS_DIR):
        return active
    for name in os.listdir(PLUGINS_DIR):
        full_path = os.path.join(PLUGINS_DIR, name)
        if os.path.isdir(full_path):
            # Try to find GitHub URL from package.json or README
            gh_url = None
            for fname in ['package.json', 'pyproject.toml', 'setup.py', 'README.md', 'readme.md']:
                fpath = os.path.join(full_path, fname)
                if os.path.exists(fpath):
                    try:
                        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                            txt = f.read()
                            m = re.search(r'https://github\.com/([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)', txt)
                            if m:
                                gh_url = f"https://github.com/{m.group(1)}"
                                break
                    except:
                        pass
            active[name] = {'path': full_path, 'github': gh_url}
    return active

# ── 2. Parse full API report ─────────────────────────────────────────────────
def parse_report():
    """Parse the full API report to get all repo results"""
    if not os.path.exists(FULL_REPORT):
        print(f"[!] Full report not found: {FULL_REPORT}")
        return []

    repos = []
    with open(FULL_REPORT, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Parse overview table rows
    for line in lines:
        line = line.strip()
        if not line.startswith('|'):
            continue
        parts = [p.strip() for p in line.split('|') if p.strip()]
        if len(parts) < 4:
            continue
        if parts[0] == '#' or parts[0].startswith('---'):
            continue
        try:
            num = int(parts[0])
        except:
            continue

        repo_cell = parts[1]
        verdict_cell = parts[2]
        note = parts[3] if len(parts) > 3 else ''

        # Extract org/repo from backtick
        m = re.search(r'`([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)`', repo_cell)
        if not m:
            continue
        full_name = m.group(1)

        # Stars
        star_m = re.search(r'⭐(\d+)', repo_cell)
        stars = int(star_m.group(1)) if star_m else 0

        verdict = 'REFERENCE'
        if '✅' in verdict_cell or 'APPROVE' in verdict_cell:
            verdict = 'APPROVE'
        elif '❌' in verdict_cell or 'REJECT' in verdict_cell:
            verdict = 'REJECT'
        elif '🔖' in verdict_cell or 'DEFER' in verdict_cell:
            verdict = 'DEFER'

        dept = ''
        dept_m = re.search(r'Dept\s+\d+\s+[—-]\s+[\w/]+', verdict_cell)
        if dept_m:
            dept = dept_m.group(0)

        repos.append({
            'num': num,
            'full_name': full_name,
            'url': f"https://github.com/{full_name}",
            'stars': stars,
            'verdict': verdict,
            'dept': dept,
            'note': note[:80]
        })

    return repos

# ── 3. Cross reference active plugins with report results ────────────────────
def build_catalog(active_plugins, all_repos):
    active_catalog = []
    pending_catalog = []
    archived_catalog = []

    # Map by full_name
    active_names = set()
    for plugin_name, plugin_info in active_plugins.items():
        gh = plugin_info.get('github', '')
        if gh:
            name = gh.split('github.com/')[-1].rstrip('/')
            active_names.add(name.lower())
        active_names.add(plugin_name.lower())

    for repo in all_repos:
        fn = repo['full_name'].lower()
        repo_name = fn.split('/')[-1] if '/' in fn else fn

        # Check if installed
        is_active = fn in active_names or repo_name in active_names

        if is_active:
            repo['status'] = '⭐ ACTIVE'
            active_catalog.append(repo)
        elif repo['verdict'] == 'APPROVE' or repo['verdict'] == 'REFERENCE':
            repo['status'] = '🔖 PENDING'
            pending_catalog.append(repo)
        else:
            repo['status'] = '❌ ARCHIVED'
            archived_catalog.append(repo)

    # Add active plugins not in report
    for plugin_name, plugin_info in active_plugins.items():
        fn = plugin_name.lower()
        if not any(fn in r['full_name'].lower() or fn in r['full_name'].lower().split('/')[-1] for r in all_repos):
            active_catalog.append({
                'full_name': f"local/{plugin_name}",
                'url': plugin_info.get('github', '#'),
                'stars': 0,
                'verdict': 'ACTIVE',
                'dept': 'Dept 20 — CIV',
                'note': f'Installed locally at ecosystem/plugins/{plugin_name}',
                'status': '⭐ ACTIVE'
            })

    return active_catalog, pending_catalog, archived_catalog

# ── 4. Write all output files ─────────────────────────────────────────────────
def write_master_catalog(active, pending, archived):
    date_str = datetime.date.today().strftime('%Y-%m-%d')

    # === MASTER CATALOG ===
    lines = [f"""# 🗂️ MASTER REPO CATALOG — AI OS Corp
**Updated:** {date_str} | **Owner:** Dept 20 CIV + Antigravity
**Automation:** `ops/scripts/repo_eval_github_api.py` → auto-refresh hàng tuần

---

## THỐNG KÊ

| Kho | Count | Trạng thái |
|-----|-------|-----------|
| ⭐ ACTIVE | {len(active)} | Đang dùng trong AI OS |
| 🔖 PENDING | {len(pending)} | Đã APPROVE, chưa cài đặt |
| ❌ ARCHIVED | {len(archived)} | REJECT/DEFER — CEO xem xét lại |

---

## ⭐ REPO ĐANG ACTIVE TRONG AI OS

> Các repo này cần được update thường xuyên. Mỗi tuần Dept 20 CIV kiểm tra version mới.

| # | Repo | Stars | Dept | Ghi chú |
|---|------|-------|------|---------|
"""]
    for i, r in enumerate(active, 1):
        lines.append(f"| {i} | [⭐ {r['full_name']}]({r['url']}) | {r['stars']} | {r.get('dept','Dept 20 CIV')} | {r['note'][:60]} |\n")

    lines.append(f"""
---

## 🔖 PENDING — Đã APPROVE, Chờ CEO Duyệt Cài Đặt

> Tổng {len(pending)} repos. Priority: sort theo Stars. Dept phụ trách: Dept 20 CIV.
> Trigger: `aos integrate <plugin_id>` sau khi CEO sign-off.

| # | Repo | Stars | Dept | Ghi chú |
|---|------|-------|------|---------|
""")
    pending_sorted = sorted(pending, key=lambda x: x.get('stars',0), reverse=True)
    for i, r in enumerate(pending_sorted[:200], 1):  # Top 200 by stars
        lines.append(f"| {i} | [{r['full_name']}]({r['url']}) | ⭐{r['stars']} | {r.get('dept','')} | {r['note'][:60]} |\n")
    if len(pending) > 200:
        lines.append(f"\n> ... và {len(pending)-200} repos khác. Xem full list tại `PENDING_REPOS.md`\n")

    lines.append(f"""
---

## ❌ ARCHIVED — REJECT/DEFER

> Tổng {len(archived)} repos. Gom về đây để CEO xem xét lại khi cần.
> Không clone, không cài đặt cho đến khi CEO unarchive.

| # | Repo | Verdict | Lý do |
|---|------|---------|----|
""")
    for i, r in enumerate(archived[:100], 1):
        lines.append(f"| {i} | [{r['full_name']}]({r['url']}) | {r['verdict']} | {r['note'][:70]} |\n")
    if len(archived) > 100:
        lines.append(f"\n> ... và {len(archived)-100} repos khác. Xem full list tại `ARCHIVED_REPOS.md`\n")

    lines.append("""
---

## QUY TRÌNH TỰ ĐỘNG CẬP NHẬT

```yaml
Automation: repo_catalog_updater
Trigger: weekly (mỗi Thứ Hai 00:00)
Steps:
  1. Chạy repo_eval_github_api.py (batch 50 repos)
  2. Cross-check với ecosystem/plugins
  3. Cập nhật MASTER_REPO_CATALOG.md
  4. Notify CEO qua Telegram nếu có repo ACTIVE có version mới
Agent: Dept 20 CIV (knowledge_navigator + archivist)
```
""")

    with open(CATALOG_OUT, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    # === ACTIVE REPOS (full detail) ===
    with open(ACTIVE_OUT, 'w', encoding='utf-8') as f:
        f.write(f"# ⭐ ACTIVE REPOS — AI OS Corp ({date_str})\n\n")
        f.write(f"> {len(active)} repos đang được sử dụng trong AI OS\n\n")
        for i, r in enumerate(active, 1):
            f.write(f"## {i}. {r['full_name']} ⭐\n")
            f.write(f"🔗 {r['url']}\n")
            f.write(f"- **Stars:** {r['stars']} | **Dept:** {r.get('dept','')}\n")
            f.write(f"- **Status:** {r['status']}\n")
            f.write(f"- **Note:** {r['note']}\n\n")

    # === PENDING REPOS ===
    with open(PENDING_OUT, 'w', encoding='utf-8') as f:
        f.write(f"# 🔖 PENDING REPOS — AI OS Corp ({date_str})\n\n")
        f.write(f"> {len(pending)} repos đã APPROVE chờ CEO duyệt cài đặt.\n")
        f.write(f"> Sắp xếp theo Stars (ưu tiên cao nhất lên đầu)\n\n")
        f.write("| # | Repo | Stars | Dept | Note |\n")
        f.write("|---|------|-------|------|------|\n")
        for i, r in enumerate(pending_sorted, 1):
            f.write(f"| {i} | [{r['full_name']}]({r['url']}) | ⭐{r['stars']} | {r.get('dept','')} | {r['note'][:70]} |\n")

    # === ARCHIVED REPOS ===
    with open(ARCHIVED_OUT, 'w', encoding='utf-8') as f:
        f.write(f"# ❌ ARCHIVED REPOS — AI OS Corp ({date_str})\n\n")
        f.write(f"> {len(archived)} repos bị REJECT/DEFER. CEO xem xét lại khi cần.\n\n")
        f.write("| # | Repo | Verdict | Note |\n")
        f.write("|---|------|---------|------|\n")
        for i, r in enumerate(archived, 1):
            f.write(f"| {i} | [{r['full_name']}]({r['url']}) | {r['verdict']} | {r['note'][:70]} |\n")

    print(f"[OK] MASTER_REPO_CATALOG.md → {CATALOG_OUT}")
    print(f"[OK] ACTIVE_REPOS.md     → {ACTIVE_OUT}")
    print(f"[OK] PENDING_REPOS.md    → {PENDING_OUT}")
    print(f"[OK] ARCHIVED_REPOS.md   → {ARCHIVED_OUT}")

if __name__ == "__main__":
    print("[*] Scanning active plugins...")
    active_plugins = get_active_plugins()
    print(f"[*] Found {len(active_plugins)} plugins in ecosystem/plugins")

    print("[*] Parsing full API report...")
    all_repos = parse_report()
    print(f"[*] Parsed {len(all_repos)} repos from report")

    print("[*] Building catalog...")
    active, pending, archived = build_catalog(active_plugins, all_repos)
    print(f"[*] ACTIVE: {len(active)} | PENDING: {len(pending)} | ARCHIVED: {len(archived)}")

    print("[*] Writing output files...")
    write_master_catalog(active, pending, archived)
    print("[SUCCESS] Master Repo Catalog built!")
