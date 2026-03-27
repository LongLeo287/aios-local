"""
Repo Evaluation Engine — REAL GitHub API Version
Owner: Antigravity + Dept 20 (CIV)
Workflow: ops/workflows/repo-evaluation.md (5 bước chính xác)

Dùng GITHUB_TOKEN từ MASTER.env để gọi GitHub REST API v3:
- GET /repos/{owner}/{repo} → description, stars, forks, license, updated_at, language
- Áp dụng đủ 5 STEP của repo-evaluation.md
- Output: Report chuẩn format CEO (tiếng Việt, đúng DETAIL CARD format)

Rate limit: 5000 requests/hour với PAT → batch 100 repos ~ 15s
"""

import os
import re
import json
import time
import datetime
import urllib.request
import urllib.error

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
CLEAN_FILE = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA', 'github_repos_clean.txt')
ENV_FILE = os.path.join(BASE_DIR, 'system', 'ops', 'secrets', 'MASTER.env')

# Load GITHUB_TOKEN from MASTER.env
def load_token():
    if not os.path.exists(ENV_FILE):
        return None
    with open(ENV_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if line.startswith('GITHUB_TOKEN='):
                return line.split('=', 1)[1].strip()
    return None

GITHUB_TOKEN = load_token()

# === AI OS Tier 1 tools (STEP 2 - Conflict check - SACRED) ===
TIER1 = {
    'mem0': 'Memory Management',
    'firecrawl': 'Web Scraping/Crawling',
    'lightrag': 'RAG Knowledge Graph',
    'crewai': 'Multi-Agent Orchestration',
    'gitnexus': 'Code Analysis/AST'
}

# Domains that map to departments
DEPT_MAP = {
    ('security', 'pentest', 'audit', 'trivy', 'guard', 'scan', 'vulner'): 'Dept 10 — Security',
    ('agent', 'crew', 'swarm', 'multi-agent', 'orchestr', 'claw'): 'Dept 01 — AI Core',
    ('browser', 'scrape', 'crawl', 'playwright', 'puppeteer', 'selenium'): 'Dept 11 — Web Ops',
    ('memory', 'rag', 'knowledge', 'vector', 'embed', 'lightrag'): 'Dept 07 — Knowledge',
    ('skill', 'plugin', 'mcp', 'extension'): 'Dept 20 — CIV',
    ('eval', 'monitor', 'observ', 'trace', 'log'): 'Dept 15 — QA/Eval',
    ('llm', 'model', 'inference', 'train', 'fine'): 'Dept 02 — AI Infra',
    ('data', 'pipeline', 'etl', 'stream'): 'Dept 08 — Data',
    ('ui', 'dashboard', 'frontend', 'react'): 'Dept 05 — UI/UX',
    ('api', 'gateway', 'router', 'proxy'): 'Dept 03 — API',
    ('finance', 'trading', 'stock', 'market'): 'Dept 12 — Finance',
    ('test', 'quality', 'benchmark'): 'Dept 15 — QA',
}

def get_dept(name_str):
    name_lower = name_str.lower()
    for keywords, dept in DEPT_MAP.items():
        if any(k in name_lower for k in keywords):
            return dept
    return 'Dept 00 — General'

def github_api_get(owner, repo, token):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'token {token}')
    req.add_header('Accept', 'application/vnd.github.v3+json')
    req.add_header('User-Agent', 'AI-OS-Corp-Evaluator/1.0')
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {'error': 'NOT_FOUND'}
        elif e.code == 403:
            return {'error': 'RATE_LIMITED'}
        return {'error': f'HTTP_{e.code}'}
    except Exception as e:
        return {'error': str(e)}

def check_conflict(name, description):
    """STEP 2: Conflict & Redundancy Check vs Tier 1"""
    name_l = name.lower()
    desc_l = (description or '').lower()
    for t1_name, t1_func in TIER1.items():
        if t1_name in name_l:
            return f'CONFLICT — Trùng Tier 1 ({t1_func}: {t1_name})'
    # Functional overlap check
    if any(k in name_l or k in desc_l for k in ['firecrawl', 'web scraping', 'web crawl']):
        return f'⚠️ Firecrawl — Kiểm tra trùng lặp Web Scraping'
    if any(k in name_l or k in desc_l for k in ['vector db', 'graphrag', 'lightrag']):
        return f'⚠️ LightRAG — Kiểm tra trùng lặp RAG/KG'
    return 'SAFE'

def assign_tier(data, conflict):
    """STEP 3: Tier Assignment"""
    stars = data.get('stargazers_count', 0)
    forks = data.get('forks_count', 0)
    updated_at = data.get('updated_at', '')

    if 'CONFLICT' in conflict:
        return 'Tier 3 (REJECT)'

    # Check staleness (>24 months = caution)
    if updated_at:
        try:
            last_update = datetime.datetime.strptime(updated_at[:10], '%Y-%m-%d').date()
            age_months = (datetime.date.today() - last_update).days // 30
            if age_months > 24:
                return f'Tier 3 (Stale — {age_months}m không update)'
        except:
            pass

    # Tier 1 potential: high stars, broad utility
    if stars > 5000 and forks > 500:
        return 'Tier 1 Candidate'
    elif stars > 500:
        return 'Tier 2'
    else:
        return 'Tier 2 (Low Signal)'

def cost_estimate(data):
    """STEP 4: Integration Cost"""
    name = (data.get('name') or '').lower()
    lang = (data.get('language') or '')

    cost_flags = []
    if 'docker' in name or 'compose' in name:
        cost_flags.append('Cần Docker')
    if 'api' in name and lang in ['Python', 'JavaScript']:
        cost_flags.append('Cần API key mới')
    if lang not in ['Python', 'JavaScript', 'TypeScript', '']:
        cost_flags.append(f'Ngôn ngữ khác ({lang})')

    if len(cost_flags) >= 2:
        return 'HIGH', cost_flags
    elif len(cost_flags) == 1:
        return 'MEDIUM', cost_flags
    return 'LOW', []

def evaluate_repo(url, token):
    """Full 5-step evaluation using GitHub API"""
    path = url.split('github.com/')[-1].strip('/')
    parts = path.split('/')
    if len(parts) < 2:
        return None
    owner, repo = parts[0], parts[1]

    # Call API
    data = github_api_get(owner, repo, token)

    if 'error' in data:
        return {
            'url': url, 'verdict': 'REJECT',
            'reason': f"API Error: {data['error']}",
            'tier': 'N/A', 'dept': 'N/A', 'cost': 'N/A',
            'stars': 0, 'description': '', 'license': 'Unknown',
            'language': '', 'updated': '', 'conflict': 'N/A'
        }

    name = data.get('full_name', f'{owner}/{repo}')
    description = data.get('description') or ''
    stars = data.get('stargazers_count', 0)
    forks = data.get('forks_count', 0)
    language = data.get('language') or 'N/A'
    license_info = (data.get('license') or {}).get('spdx_id') or 'Unknown'
    updated = data.get('updated_at', '')[:10]
    archived = data.get('archived', False)

    search_str = f"{name} {description}"
    dept = get_dept(search_str)
    conflict = check_conflict(name, description)
    tier = assign_tier(data, conflict)
    cost_level, cost_flags = cost_estimate(data)

    # STEP 5: Verdict
    if 'Tier 3' in tier or 'CONFLICT' in conflict:
        verdict = 'REJECT'
    elif archived:
        verdict = 'REJECT'
        tier = 'Tier 3 (Archived)'
    elif stars < 10 and not description:
        verdict = 'REJECT'
        tier = 'Tier 3 (Empty/No signal)'
    elif any(k in search_str.lower() for k in
             ['agent', 'llm', 'rag', 'mcp', 'skill', 'crew', 'memory', 'crawl', 'eval',
              'monitor', 'observ', 'security', 'pentest', 'guard', 'claude', 'openai',
              'gemini', 'qwen', 'inference', 'embed', 'vector', 'knowledge']):
        verdict = 'APPROVE'
    elif stars > 200:
        verdict = 'REFERENCE'
    elif any(k in search_str.lower() for k in
             ['ui', 'frontend', 'react', 'css', 'design', 'animation', 'tutorial',
              'example', 'demo', 'sample', 'boilerplate', 'template']):
        verdict = 'DEFER'
    else:
        verdict = 'REFERENCE'

    return {
        'url': url, 'name': name, 'verdict': verdict,
        'description': description[:150] if description else '(Không có mô tả)',
        'stars': stars, 'forks': forks,
        'language': language, 'license': license_info,
        'updated': updated, 'conflict': conflict,
        'tier': tier, 'dept': dept,
        'cost': cost_level, 'cost_flags': cost_flags
    }

def write_full_report(all_results, date_str):
    approved = [r for r in all_results if r['verdict'] == 'APPROVE']
    reference = [r for r in all_results if r['verdict'] == 'REFERENCE']
    deferred = [r for r in all_results if r['verdict'] == 'DEFER']
    rejected = [r for r in all_results if r['verdict'] == 'REJECT']

    total = len(all_results)

    lines = [f"""# 📋 Repo Intake Report — {date_str}
**CIV Tickets:** BATCH-GLOBAL-API | **Tổng URLs nhận:** {total} | **Unique repos:** {total} | **Không đọc được:** {len([r for r in all_results if 'API Error' in r.get('reason','')])}
**Workflow:** `ops/workflows/repo-evaluation.md` | **Owner:** Antigravity + Dept 20 (CIV)
**Source:** GitHub REST API v3 — Data thực từng repo

---

## PHÂN LOẠI THEO CATEGORY

| # | Repo | Verdict | Phân tích |
|---|------|---------|-----------|\n"""]

    counter = 1
    for vtype, emoji in [('APPROVE','✅'),('REFERENCE','📚'),('DEFER','🔖'),('REJECT','❌')]:
        for r in all_results:
            if r['verdict'] == vtype:
                name = r.get('name', r['url'].split('github.com/')[-1])
                reason = r.get('description', r.get('reason',''))[:60]
                lines.append(f"| {counter} | `{name}` *(⭐{r.get('stars',0)})* | {emoji} {vtype} → {r.get('dept','N/A')} | {reason} |\n")
                counter += 1

    # APPROVE Detail cards
    lines.append(f"""
---

## CHI TIẾT — APPROVE repos ({len(approved)} repos)
""")
    for i, r in enumerate(approved, 1):
        name = r.get('name', '')
        cost_note = ', '.join(r.get('cost_flags',[])) or 'Không có yêu cầu đặc biệt'
        lines.append(f"""
### {i}. {name.replace('/',  ' · ')} · `{name}`
🔗 {r['url']}

- **Mô tả:** {r.get('description', '(Không có mô tả)')}
- **License:** {r.get('license', 'Unknown')}
- **Highlights:** ⭐ {r.get('stars',0)} stars | 🍴 {r.get('forks',0)} forks | 📅 Updated: {r.get('updated','')} | 💻 {r.get('language','N/A')}
- **AI OS Relevance:** ⭐⭐⭐⭐ — Phù hợp domain AI Agent / OS
- **Conflict check:** {r.get('conflict','SAFE')}
- **Dept:** {r.get('dept','N/A')}
- **Tier:** {r.get('tier','Tier 2')}
- **Integration Cost:** {r.get('cost','LOW')} — {cost_note}
- **Action:** → Queue `plugin-integration.md` sau CEO sign-off
""")

    # REFERENCE cards
    lines.append(f"""
---

## CHI TIẾT — REFERENCE repos ({len(reference)} repos)
""")
    for i, r in enumerate(reference, 1):
        name = r.get('name', '')
        lines.append(f"""
### {i}. {name} · `{name}`
🔗 {r['url']}

- **Mô tả:** {r.get('description','(Không có mô tả)')}
- **Học gì:** Pattern/implementation từ ⭐{r.get('stars',0)} stars repo này
- **Action:** → Lưu KI vào `brain/knowledge/notes/`
""")

    # DEFER & REJECT table
    lines.append(f"""
---

## DEFER & REJECT

| Repo | Verdict | Lý do |
|------|---------|-------|\n""")
    for r in deferred + rejected:
        name = r.get('name', r['url'].split('github.com/')[-1])
        verdict = r['verdict']
        reason = r.get('conflict','') or r.get('reason','') or r.get('tier','')
        lines.append(f"| `{name}` | {'🔖 DEFER' if verdict=='DEFER' else '❌ REJECT'} | {reason[:80]} |\n")

    # Deep Analysis - top 3 by stars
    top3 = sorted(approved, key=lambda x: x.get('stars',0), reverse=True)[:3]
    lines.append(f"""
---

## DEEP ANALYSIS — Top 3 APPROVE ưu tiên cao nhất
""")
    for i, r in enumerate(top3, 1):
        name = r.get('name','')
        lines.append(f"""
### {i}. `{name}` — {r.get('description','')[:100]}
🔗 {r['url']}
- **Stars:** ⭐ {r.get('stars',0)} | **Forks:** 🍴 {r.get('forks',0)}
- **Language:** {r.get('language','N/A')} | **License:** {r.get('license','Unknown')}
- **Last updated:** {r.get('updated','')}
- **Conflict:** {r.get('conflict','SAFE')}
- **Tier recommendation:** {r.get('tier','')}
- **Department:** {r.get('dept','')}
- **Cost:** {r.get('cost','')}
""")

    # Summary
    lines.append(f"""
---

## TỔNG KẾT

| Verdict | Count | % |
|---------|-------|---|
| ✅ APPROVE | {len(approved)} | {len(approved)*100//total if total else 0}% |
| 📚 REFERENCE | {len(reference)} | {len(reference)*100//total if total else 0}% |
| 🔖 DEFER | {len(deferred)} | {len(deferred)*100//total if total else 0}% |
| ❌ REJECT | {len(rejected)} | {len(rejected)*100//total if total else 0}% |

> **Priority Queue:**
> 1. {len([a for a in approved if 'Tier 1' in a.get('tier','')])} repos → Tier 1 Candidate — cần CEO review
> 2. {len([a for a in approved if 'Tier 2' in a.get('tier','')])} repos → Tier 2 — queue `plugin-integration.md`
""")

    return ''.join(lines)

if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("[ERROR] GITHUB_TOKEN not found in MASTER.env")
        exit(1)

    print(f"[*] GitHub Token loaded: {GITHUB_TOKEN[:20]}...")

    with open(CLEAN_FILE, 'r', encoding='utf-8') as f:
        repos = [line.strip() for line in f if line.strip()]

    # For testing, process first 50 repos
    import sys
    batch_size = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    batch = repos[:batch_size]

    print(f"[*] Processing batch of {len(batch)} repos via GitHub API...")
    print(f"[*] Rate limit: 5000 req/hour. ETA: ~{len(batch)*0.3:.0f}s")

    results = []
    for i, url in enumerate(batch):
        r = evaluate_repo(url, GITHUB_TOKEN)
        if r:
            results.append(r)
        if (i+1) % 10 == 0:
            print(f"  [{i+1}/{len(batch)}] {url.split('github.com/')[-1][:50]} → {r['verdict'] if r else 'ERROR'}")
        time.sleep(0.2)  # Be nice to GitHub API

    date_str = datetime.date.today().strftime('%Y-%m-%d')
    report = write_full_report(results, date_str)

    out_path = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA', f'repo_intake_report_API_b{batch_size}_{date_str}.md')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(report)

    approved = len([r for r in results if r['verdict'] == 'APPROVE'])
    ref = len([r for r in results if r['verdict'] == 'REFERENCE'])
    defer = len([r for r in results if r['verdict'] == 'DEFER'])
    rej = len([r for r in results if r['verdict'] == 'REJECT'])

    print(f"\n[SUCCESS] Report saved: {out_path}")
    print(f"APPROVE: {approved} | REFERENCE: {ref} | DEFER: {defer} | REJECT: {rej}")
