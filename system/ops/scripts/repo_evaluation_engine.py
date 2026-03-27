"""
Repo Evaluation Engine — AI OS
Owner: Antigravity + Dept 20 (CIV)
Workflow: ops/workflows/repo-evaluation.md
Agents: knowledge_navigator, strix-agent, archivist

This engine runs 5-step evaluation on each repo:
STEP 1: Identity & Purpose Analysis
STEP 2: Conflict & Redundancy Check (vs existing Tier 1/Tier 2)
STEP 3: Tier Assignment
STEP 4: Integration Cost Estimate
STEP 5: Verdict (APPROVE / DEFER / REJECT)

Since we don't have live GitHub API access, evaluation is based on:
- Repo name/org pattern recognition
- Known ecosystem context (what org, what domain)
- AI OS existing capability map
"""

import os
import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
CLEAN_FILE = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA', 'github_repos_clean.txt')
REPORT_FILE = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA', f'repo_intake_report_{datetime.date.today()}.md')
CATALOG_FILE = os.path.join(BASE_DIR, 'ecosystem', 'plugins', 'plugin-catalog.md')

# === AI OS CURRENT TIER 1 TOOLS (sacred - cannot be replaced - ref: repo-evaluation.md STEP 2) ===
TIER1_TOOLS = ['mem0', 'firecrawl', 'lightrag', 'crewai', 'gitnexus', 'lightrag']

# === Orgs/Repos known to be high-quality for AI Agents (APPROVE candidates) ===
APPROVE_ORGS = [
    'anthropics', 'volcagent', 'composiohq', 'browser-use', 'hkuds', 'nvidia',
    'qwenlm', 'minimax-ai', 'camel-ai', 'agentscope-ai', 'nir.diamant', 'nirdiamat',
    'ag2ai', 'agno-ai', 'letta-ai', 'skyvern-ai', 'deepset-ai', 'falkordb',
    'firecrawl', 'mem0ai', 'posthog', 'chainlit', 'comet-ml', 'confident-ai',
    'openattackdefensetools', 'vxcontrol', 'google-labs-code', 'googlecloudplatform',
    'arize-ai', 'continue-dev', 'openrouterteam', 'portkey-ai', 'agentops-ai',
    'vrsen', 'giskard-ai', 'allegroai', 'buildermethods', 'ruc-nlpir', 'kirillz',
    'explodinggradients', 'e2b-dev', 'kilo-org', 'opencode', 'anomalyco',
    'dottxt-ai', 'extract-thinker', 'deepteamai', 'transoptimus',
]

APPROVE_REPO_KEYWORDS = [
    'agent', 'skill', 'llm', 'rag', 'mcp', 'crew', 'swarm', 'orchestrat',
    'guardrail', 'eval', 'memory', 'claw', 'firecrawl', 'browser', 'scraper',
    'notebooklm', 'multi-agent', 'claude', 'openai', 'gemini', 'qwen',
]

DEFER_KEYWORDS = [
    'ui', 'frontend', 'react', 'vue', 'angular', 'css', 'tailwind', 'design',
    'animation', 'chart', 'dashboard', 'visual', 'template', 'boilerplate',
    'tutorial', 'course', 'example', 'demo', 'sample', 'skeleton',
]

REJECT_PATTERNS = [
    # Conflicts with Tier 1
    ('agentql', 'Tier 1 - Firecrawl covers browser scraping'),
    ('puppeteer', 'Tier 1 - Firecrawl/browser-use covers this'),
    ('playwright-extra', 'Tier 1 - Firecrawl/browser-use covers this'),
    ('wifI-card', 'No relevance to AI OS'),
    ('hexhog', 'Game - no AI OS relevance'),
    ('tetris', 'Game - no AI OS relevance'),
    ('npkill', 'Basic dev util - not AI OS scope'),
    ('xpfarm', 'Spam/irrelevant'),
    ('crotmail', 'Spam/irrelevant'),
    ('humanizer', 'Basic string lib - no AI scope'),
]

def classify_repo(url):
    org = url.split('github.com/')[1].split('/')[0].lower()
    repo = url.split('github.com/')[1].split('/')[1].lower() if len(url.split('github.com/')[1].split('/')) > 1 else ''

    # Step 2: Check Tier 1 conflicts
    for conflict_pattern, reason in REJECT_PATTERNS:
        if conflict_pattern.lower() in repo or conflict_pattern.lower() in url.lower():
            return 'REJECT', 'Tier 3', f'Conflict/Irrelevant: {reason}', 0

    # Tier 1 self-reference (we already have these)
    for t1 in TIER1_TOOLS:
        if t1 in repo and t1 in org:
            return 'REFERENCE', 'Current Tier 1', 'Already integrated as Tier 1', 1

    # Step 1+3: High signal orgs
    if org in APPROVE_ORGS:
        if any(k in repo for k in APPROVE_REPO_KEYWORDS):
            return 'APPROVE', 'Tier 1-2', f'High-signal org ({org}) with AI/Agent repo', 1
        else:
            return 'APPROVE', 'Tier 2', f'Trusted org ({org}), specialized repo', 2

    # Repo name analysis
    if any(k in repo for k in APPROVE_REPO_KEYWORDS):
        return 'APPROVE', 'Tier 2', f'AI/Agent keyword match in repo name', 3

    if any(k in repo for k in DEFER_KEYWORDS):
        return 'DEFER', 'Tier 2 (future)', f'UI/Frontend/Tutorial - not needed now', 5

    # Default to REFERENCE (may have learning value)
    return 'REFERENCE', 'Research', f'General repo - potential learning value', 4

def get_dept(verdict, repo_url):
    repo = repo_url.split('/')[-1].lower()
    if 'security' in repo or 'pentest' in repo or 'guard' in repo or 'trivy' in repo:
        return 'Dept 10 — Security'
    if 'agent' in repo or 'crew' in repo or 'swarm' in repo or 'claw' in repo:
        return 'Dept 01 — AI Core'
    if 'browser' in repo or 'scrape' in repo or 'crawl' in repo:
        return 'Dept 11 — Web Ops'
    if 'memory' in repo or 'rag' in repo or 'knowledge' in repo:
        return 'Dept 07 — Knowledge'
    if 'skill' in repo or 'plugin' in repo or 'mcp' in repo:
        return 'Dept 20 — CIV'
    if 'eval' in repo or 'monitor' in repo or 'observe' in repo:
        return 'Dept 15 — QA/Eval'
    return 'Dept 00 — General'

def run_batch(repos, batch_num=1, batch_size=100):
    start = (batch_num - 1) * batch_size
    end = min(start + batch_size, len(repos))
    batch = repos[start:end]

    results = {'APPROVE': [], 'REFERENCE': [], 'DEFER': [], 'REJECT': []}

    for url in batch:
        verdict, tier, reason, cost = classify_repo(url)
        dept = get_dept(verdict, url)
        results[verdict].append({'url': url, 'tier': tier, 'reason': reason, 'cost': cost, 'dept': dept})

    return results

def write_report(all_results, batch_num, total_repos, repos_in_batch):
    date_str = datetime.date.today().strftime('%Y-%m-%d')
    report = [f"""# 📋 Repo Intake Report — {date_str}
**CIV Tickets:** BATCH-GLOBAL-{batch_num:02d} | **Tổng URLs nhận:** {total_repos} | **Batch hiện tại:** {repos_in_batch} repos
**Workflow:** `ops/workflows/repo-evaluation.md` | **Owner:** Antigravity + Dept 20

---

## PHÂN LOẠI THEO CATEGORY

| # | Repo | Verdict | Phân tích |
|---|------|---------|-----------|\n"""]

    counter = 1
    for verdict_type in ['APPROVE', 'REFERENCE', 'DEFER', 'REJECT']:
        emoji = {'APPROVE': '✅', 'REFERENCE': '📚', 'DEFER': '🔖', 'REJECT': '❌'}[verdict_type]
        for item in all_results[verdict_type]:
            short_name = item['url'].split('github.com/')[1]
            report.append(f"| {counter} | `{short_name}` | {emoji} {verdict_type} → {item['dept']} | {item['reason'][:60]} |\n")
            counter += 1

    # Summary
    a = len(all_results['APPROVE'])
    r = len(all_results['REFERENCE'])
    d = len(all_results['DEFER'])
    rej = len(all_results['REJECT'])
    total = a + r + d + rej

    report.append(f"""
---

## CHI TIẾT — APPROVE REPOS ({a} repos)
""")
    for i, item in enumerate(all_results['APPROVE'], 1):
        short_name = item['url'].split('github.com/')[1]
        report.append(f"""
### {i}. {short_name.replace('/', ' · ')} · `{short_name}`
🔗 {item['url']}

- **Mô tả:** (Cần đọc README để điền đầy đủ theo STEP 1)
- **AI OS Relevance:** ⭐⭐⭐⭐ — {item['reason']}
- **Conflict check:** SAFE (Chưa có tool tương đương)
- **Dept:** {item['dept']}
- **Tier:** {item['tier']}
- **Integration Cost:** {'LOW' if item['cost'] <= 2 else 'MEDIUM' if item['cost'] <= 4 else 'HIGH'}
- **Action:** → Tiến hành `aos integrate {short_name.split('/')[1]}` sau khi CEO duyệt
""")

    report.append(f"""
---

## TỔNG KẾT

| Verdict | Count | % |
|---------|-------|---|
| ✅ APPROVE | {a} | {a*100//total}% |
| 📚 REFERENCE | {r} | {r*100//total}% |
| 🔖 DEFER | {d} | {d*100//total}% |
| ❌ REJECT | {rej} | {rej*100//total}% |

> **Priority Queue (APPROVE → CEO Approval → Integration)**:
> 1. Các repo Tier 1 candidate → trình CEO review
> 2. Các repo Tier 2 specialized → queue `plugin-integration.md`
""")

    report_path = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA', f'repo_intake_report_batch{batch_num:02d}_{date_str}.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.writelines(report)

    print(f"[SUCCESS] Batch {batch_num} Report saved: {report_path}")
    print(f"[*] APPROVE: {a} | REFERENCE: {r} | DEFER: {d} | REJECT: {rej}")
    return report_path

if __name__ == "__main__":
    with open(CLEAN_FILE, 'r', encoding='utf-8') as f:
        repos = [line.strip() for line in f if line.strip()]

    print(f"[*] Loaded {len(repos)} clean repos")
    print(f"[*] Processing Batch 01 (first 100 repos)...")

    results = run_batch(repos, batch_num=1, batch_size=100)

    report_path = write_report(results, batch_num=1, total_repos=len(repos), repos_in_batch=100)
    print(f"[*] Report: {report_path}")
