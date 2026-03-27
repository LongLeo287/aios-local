"""
Chạy toàn bộ 1651 repos qua Engine Phân Tích 5 Bước (tất cả batches).
Output: repo_intake_report_FULL_YYYY-MM-DD.md
"""
import os, sys, datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
CLEAN_FILE = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA', 'ALL_PENDING_REPOS.txt')
REPORT_FILE = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA', f'repo_intake_report_FULL_{datetime.date.today()}.md')

# Import engine
sys.path.insert(0, os.path.dirname(__file__))
from repo_evaluation_engine import classify_repo, get_dept

with open(CLEAN_FILE, 'r', encoding='utf-8') as f:
    repos = [line.strip() for line in f if line.strip()]

print(f"[*] Running full evaluation on {len(repos)} repos...")

results = {'APPROVE': [], 'REFERENCE': [], 'DEFER': [], 'REJECT': []}
for url in repos:
    verdict, tier, reason, cost = classify_repo(url)
    dept = get_dept(verdict, url)
    results[verdict].append({'url': url, 'tier': tier, 'reason': reason, 'cost': cost, 'dept': dept})

a, r, d, rej = len(results['APPROVE']), len(results['REFERENCE']), len(results['DEFER']), len(results['REJECT'])
total = a + r + d + rej

date_str = datetime.date.today().strftime('%Y-%m-%d')
lines = [f"""# 📋 Repo Intake Report FULL — {date_str}
**CIV:** BATCH-GLOBAL-FULL | **Tổng repos sạch:** {total} | **Từ:** 1885 URLs gốc
**Workflow:** `ops/workflows/repo-evaluation.md` | **Owner:** Antigravity + Dept 20 CIV

## TỔNG KẾT

| Verdict | Count | % |
|---------|-------|---|
| ✅ APPROVE | {a} | {a*100//total}% |
| 📚 REFERENCE | {r} | {r*100//total}% |
| 🔖 DEFER | {d} | {d*100//total}% |
| ❌ REJECT | {rej} | {rej*100//total}% |

---

## OVERVIEW — TẤT CẢ REPOS

| # | Repo | Verdict | Dept | Ghi chú |
|---|------|---------|------|---------|
"""]

counter = 1
for vtype in ['APPROVE', 'REFERENCE', 'DEFER', 'REJECT']:
    emoji = {'APPROVE':'✅','REFERENCE':'📚','DEFER':'🔖','REJECT':'❌'}[vtype]
    for item in results[vtype]:
        name = item['url'].split('github.com/')[1]
        note = item['reason'][:70]
        lines.append(f"| {counter} | `{name}` | {emoji} {vtype} | {item['dept']} | {note} |\n")
        counter += 1

lines.append("\n---\n\n## CHI TIẾT — APPROVE REPOS\n")
for i, item in enumerate(results['APPROVE'], 1):
    name = item['url'].split('github.com/')[1]
    lines.append(f"""
### {i}. {name} · `{name}`
🔗 {item['url']}
- **Lý do:** {item['reason']}
- **Dept:** {item['dept']} | **Tier:** {item['tier']}
- **Action:** → Queue `plugin-integration.md` sau CEO sign-off
""")

with open(REPORT_FILE, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"[SUCCESS] Full Report: {REPORT_FILE}")
print(f"APPROVE: {a} | REFERENCE: {r} | DEFER: {d} | REJECT: {rej}")
