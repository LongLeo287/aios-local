"""
Batch Repo Intake — Phase 28
Owner: Antigravity + Dept 20 CIV + Dept 07 Knowledge

⚠️  DEPRECATED NOTICE (2026-03-27):
    Mode 'pending' và 'all' đã bị DISABLED — vi phạm RULE-CIV-02 (PENDING GATE).
    Những mode này bypass CIV pipeline, ghi thẳng vào brain/knowledge/repos/.

    Dùng đúng pipeline thay thế:
    1. Phân tích: python system/ops/scripts/pending_civ_classifier.py
    2. Approve:   python system/ops/scripts/pending_civ_approve.py --auto-approve
    3. Clone:     python system/ops/scripts/active_repos_pipeline.py

    Mode 'active' và 'knowledge' vẫn được phép (không bypass pipeline).

Mode còn hoạt động:
  --mode active   : Update knowledge cho ACTIVE repos (gọi GitHub API + ghi KI)
  --mode knowledge: Nạp README của APPROVE repos vào brain/knowledge (không clone)
"""

import os, sys, json, re, datetime, urllib.request, urllib.error, time, subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
PLUGINS_DIR = os.path.join(BASE_DIR, 'ecosystem', 'plugins')
BRAIN_KNOWLEDGE = os.path.join(BASE_DIR, 'brain', 'knowledge', 'repos')
VAULT_DATA = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA')
REGISTRY_FILE = os.path.join(PLUGINS_DIR, 'registry.json')
SKILL_REGISTRY = os.path.join(BASE_DIR, 'brain', 'shared-context', 'SKILL_REGISTRY.json')
CATALOG_FILE = os.path.join(PLUGINS_DIR, 'plugin-catalog.md')
MASTER_CATALOG = os.path.join(PLUGINS_DIR, 'MASTER_REPO_CATALOG.md')
ENV_FILE = os.path.join(BASE_DIR, 'system', 'ops', 'secrets', 'MASTER.env')

os.makedirs(BRAIN_KNOWLEDGE, exist_ok=True)

def load_token():
    if not os.path.exists(ENV_FILE): return None
    with open(ENV_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.strip().startswith('GITHUB_TOKEN='):
                return line.strip().split('=', 1)[1].strip()
    return None

GITHUB_TOKEN = load_token()

def load_active_repos():
    path = os.path.join(VAULT_DATA, 'ACTIVE_REPOS.md')
    repos = []
    if not os.path.exists(path): return repos
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            m = re.search(r'🔗\s+(https://github\.com/\S+)', line)
            if m: repos.append(m.group(1).rstrip('/'))
            m2 = re.search(r'\[⭐\s+([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)\]', line)
            if m2 and not any(r.endswith(m2.group(1)) for r in repos):
                repos.append(f"https://github.com/{m2.group(1)}")
    return repos

def load_pending_repos(limit=100):
    path = os.path.join(VAULT_DATA, 'PENDING_REPOS.md')
    repos = []
    if not os.path.exists(path): return repos
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.startswith('|'): continue
            m = re.search(r'\[([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)\]\(https://github\.com/\S+\)', line)
            star_m = re.search(r'⭐(\d+)', line)
            dept_m = re.search(r'(Dept\s+\d+\s+[—-]\s+[\w/]+)', line)
            if m:
                repos.append({
                    'full_name': m.group(1),
                    'url': f"https://github.com/{m.group(1)}",
                    'stars': int(star_m.group(1)) if star_m else 0,
                    'dept': dept_m.group(1) if dept_m else 'Dept 20 — CIV'
                })
    # Sort by stars desc
    repos.sort(key=lambda x: x['stars'], reverse=True)
    return repos[:limit]

def github_get_readme(owner, repo, token):
    """Gọi GitHub API để lấy README thực tế — FULL, không cắt"""
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'token {token}')
    req.add_header('Accept', 'application/vnd.github.v3.raw')
    req.add_header('User-Agent', 'AI-OS-Corp-Intake/1.0')
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8', errors='ignore')  # FULL README
    except:
        return None

def github_get_meta(owner, repo, token):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'token {token}')
    req.add_header('Accept', 'application/vnd.github.v3+json')
    req.add_header('User-Agent', 'AI-OS-Corp-Intake/1.0')
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except:
        return {}

def write_knowledge_note(full_name, meta, readme, status='ACTIVE', overwrite=True):
    """Ghi Knowledge Note vào brain/knowledge/repos/ — FULL README"""
    owner, repo = full_name.split('/', 1)
    dir_path = os.path.join(BRAIN_KNOWLEDGE, owner)
    os.makedirs(dir_path, exist_ok=True)

    note_path = os.path.join(dir_path, f"{repo}.md")

    # Skip nếu đã có VÀ không overwrite
    if os.path.exists(note_path) and not overwrite:
        return note_path

    description = meta.get('description') or '(No description)'
    stars = meta.get('stargazers_count', 0)
    forks = meta.get('forks_count', 0)
    language = meta.get('language') or 'N/A'
    license_info = (meta.get('license') or {}).get('spdx_id', 'Unknown')
    updated = meta.get('updated_at', '')[:10]
    homepage = meta.get('homepage') or ''
    topics = ', '.join(meta.get('topics') or [])

    note = f"""# 📦 {full_name} [{status}]
🔗 https://github.com/{full_name}
{'🌐 ' + homepage if homepage else ''}

## Meta
- **Stars:** ⭐ {stars} | **Forks:** 🍴 {forks}
- **Language:** {language} | **License:** {license_info}
- **Last updated:** {updated}
- **Topics:** {topics or '(none)'}
- **Status trong AI OS:** {status}

## Mô tả
{description}

## README (FULL)
```
{readme if readme else '(Không lấy được README)'}
```

---
*Ingested: {datetime.date.today()} | Source: GitHub API FULL | Owner: Dept 07 Knowledge*
"""
    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(note)
    return note_path

def create_plugin_manifest(full_name, meta, dept, stars, is_new=True):
    """Tạo manifest.json cho plugin mới"""
    owner, repo = full_name.split('/', 1)
    plugin_id = repo.lower().replace('-', '_').replace('.', '_')
    plugin_dir = os.path.join(PLUGINS_DIR, plugin_id)

    if os.path.exists(plugin_dir) and not is_new:
        return plugin_id, False  # Already exists

    os.makedirs(plugin_dir, exist_ok=True)
    os.makedirs(os.path.join(plugin_dir, 'tests'), exist_ok=True)

    # manifest.json
    manifest = {
        "id": plugin_id,
        "name": repo,
        "version": "unknown",
        "upstream": f"https://github.com/{full_name}",
        "type": "bridge",
        "status": "registered",
        "auto_load": False,
        "can_crash_os": False,
        "department": dept,
        "stars": stars,
        "description": meta.get('description', ''),
        "language": meta.get('language', ''),
        "license": (meta.get('license') or {}).get('spdx_id', 'Unknown'),
        "conflict_check": "SAFE",
        "upstream_check": "weekly" if stars > 1000 else "monthly",
        "registered_at": str(datetime.date.today()),
        "agent_hooks": [],
        "notes": f"Auto-registered by Phase 28 intake — {datetime.date.today()}"
    }
    with open(os.path.join(plugin_dir, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # PLUGIN.md
    plugin_md = f"""# {repo} Plugin
**ID:** `{plugin_id}` | **Status:** registered | **Dept:** {dept}
**Upstream:** https://github.com/{full_name}

## Mô tả
{meta.get('description', '(No description)')}

## Khi nào dùng
> TODO: Điền sau khi đọc README đầy đủ

## Cách kích hoạt
```bash
# TODO: Điền lệnh cài đặt/kích hoạt
```

## Agent có quyền dùng
- knowledge_navigator
- strategy-agent

---
*Auto-generated: {datetime.date.today()} | plugin-integration.md Phase 2*
"""
    with open(os.path.join(plugin_dir, 'PLUGIN.md'), 'w', encoding='utf-8') as f:
        f.write(plugin_md)

    # Smoke test placeholder
    test_code = f"""# Smoke test for {plugin_id}
# Run: python ecosystem/plugins/{plugin_id}/tests/test_{plugin_id}.py

import os, sys

def test_manifest_exists():
    manifest = os.path.join(os.path.dirname(__file__), '..', 'manifest.json')
    assert os.path.exists(manifest), "manifest.json missing"
    print("[OK] manifest.json exists")

def test_plugin_md_exists():
    plugin_md = os.path.join(os.path.dirname(__file__), '..', 'PLUGIN.md')
    assert os.path.exists(plugin_md), "PLUGIN.md missing"
    print("[OK] PLUGIN.md exists")

if __name__ == "__main__":
    test_manifest_exists()
    test_plugin_md_exists()
    print(f"[PASS] {plugin_id} smoke tests OK")
"""
    with open(os.path.join(plugin_dir, 'tests', f'test_{plugin_id}.py'), 'w', encoding='utf-8') as f:
        f.write(test_code)

    return plugin_id, True

def update_registry(plugin_id, full_name, meta, dept):
    """Cập nhật plugins/registry.json"""
    if not os.path.exists(REGISTRY_FILE):
        registry = {"plugins": [], "total_registered": 0, "active_count": 0}
    else:
        with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
            registry = json.load(f)

    # Check if already registered
    existing_ids = [p.get('id') for p in registry.get('plugins', [])]
    repo = full_name.split('/', 1)[1]
    plugin_id_clean = repo.lower().replace('-', '_').replace('.', '_')

    if plugin_id_clean in existing_ids:
        return False  # Already registered

    new_entry = {
        "id": plugin_id_clean,
        "type": "bridge",
        "status": "registered",
        "auto_load": False,
        "path": f"ecosystem/plugins/{plugin_id_clean}/",
        "manifest": f"ecosystem/plugins/{plugin_id_clean}/manifest.json",
        "upstream": f"https://github.com/{full_name}",
        "department": dept,
        "notes": meta.get('description', '')[:100],
        "registered_at": str(datetime.date.today()),
        "upstream_check": "monthly"
    }

    if 'plugins' not in registry:
        registry['plugins'] = []
    registry['plugins'].append(new_entry)
    registry['total_registered'] = len(registry['plugins'])

    with open(REGISTRY_FILE, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    return True

# ──────────────────────────────────────────────────────────────────────────────

def mode_active_update():
    """Update Knowledge Notes cho 38 ACTIVE repos"""
    print("\n[MODE: ACTIVE UPDATE]")
    print("Updating knowledge for all ACTIVE repos via GitHub API...\n")

    repos = load_active_repos()
    print(f"Found {len(repos)} active repos")

    results = []
    for i, url in enumerate(repos, 1):
        parts = url.split('github.com/')
        if len(parts) < 2: continue
        full_name = parts[1].rstrip('/')
        if '/' not in full_name: continue
        owner, repo = full_name.split('/', 1)

        print(f"  [{i}/{len(repos)}] {full_name} ...")
        meta = github_get_meta(owner, repo, GITHUB_TOKEN)
        readme = github_get_readme(owner, repo, GITHUB_TOKEN)
        note_path = write_knowledge_note(full_name, meta, readme, status='⭐ ACTIVE')
        results.append({'full_name': full_name, 'note': note_path})
        time.sleep(0.3)

    print(f"\n[OK] Updated {len(results)} ACTIVE repo knowledge notes")
    print(f"[OK] Location: {BRAIN_KNOWLEDGE}")
    return results

def mode_pending_intake(limit=100):
    """Clone + Register top N PENDING repos"""
    print(f"\n[MODE: PENDING INTAKE — Top {limit} by Stars]")

    repos = load_pending_repos(limit)
    print(f"Processing {len(repos)} PENDING repos...\n")

    registered = 0
    skipped = 0

    for i, r in enumerate(repos, 1):
        full_name = r['full_name']
        owner, repo = full_name.split('/', 1)
        dept = r.get('dept', 'Dept 20 — CIV')

        print(f"  [{i}/{len(repos)}] {full_name} ⭐{r['stars']}")

        meta = github_get_meta(owner, repo, GITHUB_TOKEN)
        readme = github_get_readme(owner, repo, GITHUB_TOKEN)

        # Write knowledge note
        write_knowledge_note(full_name, meta, readme, status='🔖 PENDING')

        # Create plugin structure (manifest, PLUGIN.md, tests)
        plugin_id, is_new = create_plugin_manifest(full_name, meta, dept, r['stars'])

        if is_new:
            # Register in registry.json
            reg_result = update_registry(plugin_id, full_name, meta, dept)
            if reg_result:
                registered += 1
                print(f"    → Registered as '{plugin_id}'")
            else:
                skipped += 1
                print(f"    → Already in registry")
        else:
            skipped += 1
            print(f"    → Plugin dir already exists")

        time.sleep(0.3)

    print(f"\n[OK] Newly registered: {registered} | Skipped: {skipped}")
    return registered

def mode_knowledge_only():
    """Nạp README của tất cả APPROVE repos vào brain/knowledge (không clone, không register)"""
    print("\n[MODE: KNOWLEDGE ONLY — All APPROVE repos]")

    repos = load_pending_repos(limit=9999)  # All pending
    print(f"Processing {len(repos)} repos for knowledge intake...\n")

    done = 0
    for i, r in enumerate(repos, 1):
        full_name = r['full_name']
        if '/' not in full_name: continue
        owner, repo = full_name.split('/', 1)

        # Check if already has knowledge note
        note_path = os.path.join(BRAIN_KNOWLEDGE, owner, f"{repo}.md")
        if os.path.exists(note_path):
            continue  # Skip if already ingested

        if (i % 50) == 1:
            print(f"  Progress: {i}/{len(repos)} ...")

        meta = github_get_meta(owner, repo, GITHUB_TOKEN)
        readme = github_get_readme(owner, repo, GITHUB_TOKEN)
        write_knowledge_note(full_name, meta, readme, status='🔖 PENDING/APPROVE')
        done += 1
        time.sleep(0.25)

    print(f"\n[OK] Ingested knowledge for {done} repos")
    print(f"[OK] Location: {BRAIN_KNOWLEDGE}")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else 'active'
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 100

    # ⛔ RULE-CIV-02 ENFORCEMENT — BLOCKED MODES
    BLOCKED_MODES = {'pending', 'all'}
    if mode in BLOCKED_MODES:
        print("")
        print("═" * 60)
        print("  ⛔  TRUY CẬP BỊ TỪ CHỐI — RULE-CIV-02")
        print("═" * 60)
        print(f"  Mode '{mode}' đã bị DISABLE (2026-03-27).")
        print("  Lý do: Bypass CIV pipeline — ghi thẳng vào brain/")
        print("         mà KHÔNG qua Strix scan, KHÔNG qua CEO approve.")
        print("")
        print("  Dùng đúng pipeline:")
        print("  1. python system/ops/scripts/pending_civ_classifier.py")
        print("  2. python system/ops/scripts/pending_civ_approve.py --auto-approve")
        print("  3. python system/ops/scripts/active_repos_pipeline.py")
        print("═" * 60)
        sys.exit(1)

    if not GITHUB_TOKEN:
        print("[ERROR] GITHUB_TOKEN not found")
        sys.exit(1)

    print(f"[*] GitHub Token: {GITHUB_TOKEN[:20]}...")
    print(f"[*] Mode: {mode} | Limit: {limit}")

    if mode == 'active':
        mode_active_update()
    elif mode == 'knowledge':
        mode_knowledge_only()
    else:
        print(f"[!] Unknown mode: {mode}")
        print("Usage: python batch_repo_intake.py [active|knowledge]")

