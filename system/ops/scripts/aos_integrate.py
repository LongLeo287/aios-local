import os, sys, json, re, urllib.request, urllib.error, datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
PLUGINS_DIR = os.path.join(BASE_DIR, 'ecosystem', 'plugins')
VAULT_DATA = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA')
REGISTRY_FILE = os.path.join(PLUGINS_DIR, 'registry.json')
ENV_FILE = os.path.join(BASE_DIR, 'system', 'ops', 'secrets', 'MASTER.env')
PENDING_FILE = os.path.join(VAULT_DATA, 'PENDING_REPOS.md')
ACTIVE_FILE = os.path.join(VAULT_DATA, 'ACTIVE_REPOS.md')

def get_github_token():
    env_token = os.environ.get('GITHUB_TOKEN')
    if env_token: return env_token
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): continue
                if '=' in line:
                    key, val = line.split('=', 1)
                    key = key.replace('export ', '').strip()
                    if key == 'GITHUB_TOKEN':
                        return val.strip().strip('"\'')
    return None

def fetch_repo_meta(full_name, token):
    url = f"https://api.github.com/repos/{full_name}"
    req = urllib.request.Request(url)
    if token: req.add_header('Authorization', f'token {token}')
    req.add_header('User-Agent', 'AI-OS-Corp-Integrate/1.0')
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        print(f"Lỗi fetch meta {full_name}: {e}")
        return None

def fetch_repo_readme(full_name, token):
    url = f"https://api.github.com/repos/{full_name}/readme"
    req = urllib.request.Request(url)
    if token: req.add_header('Authorization', f'token {token}')
    req.add_header('Accept', 'application/vnd.github.v3.raw')
    req.add_header('User-Agent', 'AI-OS-Corp-Integrate/1.0')
    try:
        with urllib.request.urlopen(req) as r:
            return r.read().decode('utf-8', errors='ignore')
    except Exception:
        return ""

def integrate_repo(full_name):
    print(f"🔄 Đang tiến hành nạp Repo: {full_name}...")
    if not isinstance(full_name, str) or full_name.count('/') != 1:
        print(f"❌ Lỗi: '{full_name}' không đúng định dạng owner/repo!")
        return False
    
    parts = full_name.split('/')
    if not parts[0].strip() or not parts[1].strip():
        print(f"❌ Lỗi: '{full_name}' không đúng định dạng owner/repo (rỗng)!  ")
        return False

    token = get_github_token()
    meta = fetch_repo_meta(full_name, token)
    if not meta: return False

    owner, repo_name = full_name.split('/')
    readme = fetch_repo_readme(full_name, token)

    # 1. Tạo Ecosystem Plugin Folder
    plugin_dir = os.path.join(PLUGINS_DIR, repo_name)
    os.makedirs(plugin_dir, exist_ok=True)
    os.makedirs(os.path.join(plugin_dir, 'tests'), exist_ok=True)

    manifest = {
        "id": repo_name,
        "name": meta.get('name', repo_name),
        "version": "1.0.0",
        "type": "data",
        "status": "active",
        "description": meta.get('description', ''),
        "auto_load": False,
        "can_crash_os": False
    }
    with open(os.path.join(plugin_dir, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    with open(os.path.join(plugin_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(readme[:1000] + "\n\n...(truncated for AI OS Ecosystem)...")

    with open(os.path.join(plugin_dir, 'PLUGIN.md'), 'w', encoding='utf-8') as f:
        f.write(f"# Plugin: {repo_name}\n\nAuto-generated integration stub.")

    # 2. Cập nhật Registry
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
            registry = json.load(f)
    else:
        registry = {"total_registered": 0, "active_count": 0, "plugins": []}

    if not any(p['id'] == repo_name for p in registry['plugins']):
        registry['plugins'].append({
            "id": repo_name,
            "type": "data",
            "status": "active",
            "auto_load": False,
            "path": f"plugins/{repo_name}/",
            "manifest": f"plugins/{repo_name}/manifest.json",
            "notes": meta.get('description', ''),
            "registered_at": datetime.datetime.now().strftime("%Y-%m-%d")
        })
        registry['total_registered'] = len(registry['plugins'])
        registry['active_count'] = len([p for p in registry['plugins'] if p['status'] == 'active'])
        with open(REGISTRY_FILE, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)

    # 3. Chuyển từ PENDING sang ACTIVE
    if os.path.exists(PENDING_FILE):
        with open(PENDING_FILE, 'r', encoding='utf-8') as f:
            pending_lines = f.readlines()
        with open(PENDING_FILE, 'w', encoding='utf-8') as f:
            for line in pending_lines:
                if full_name not in line:
                    f.write(line)

    with open(ACTIVE_FILE, 'a', encoding='utf-8') as f:
        desc = meta.get('description', '').replace('|', '')
        f.write(f"| {registry['active_count']} | [{full_name}]({meta.get('html_url')}) | ⭐{meta.get('stargazers_count')} | Dept 00 — General | {desc} |\n")

    print(f"✅ Hoàn tất Integrate: {repo_name}")
    return True

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for repo in sys.argv[1:]:
            integrate_repo(repo)
    else:
        print("Sử dụng: python aos_integrate.py <owner/repo> ...")
