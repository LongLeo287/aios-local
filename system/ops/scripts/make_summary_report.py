"""
Tạo báo cáo tóm tắt gọn nhẹ từ file full 1651 repos.
Chỉ gồm: TỔNG KẾT + OVERVIEW TABLE (tất cả) + Top 50 APPROVE DETAIL CARDS
"""
import os, re, datetime

BASE = r'<AI_OS_ROOT>\storage\vault\DATA'
SRC = os.path.join(BASE, 'repo_intake_report_API_b1651_2026-03-27.md')
ARTIFACTS = r'<USER_PROFILE>\.gemini\antigravity\brain\c62dcae9-e343-4924-9d8a-09cb97db93a4'

with open(SRC, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Extract sections by key markers
overview_lines = []
approve_cards = []
tong_ket = []
deep = []

mode = None
current_card = []

for line in lines:
    if '| # |' in line or '|---|' in line and mode=='overview':
        mode = 'overview'
    if '## PHÂN LOẠI THEO CATEGORY' in line:
        mode = 'overview'
    elif '## CHI TIẾT — APPROVE' in line:
        mode = 'approve'
        approve_cards.append([line])
        continue
    elif '## DEEP ANALYSIS' in line:
        mode = 'deep'
    elif '## TỔNG KẾT' in line:
        mode = 'tong_ket'
    elif '## CHI TIẾT — REFERENCE' in line:
        mode = 'stop_approve'

    if mode == 'overview':
        overview_lines.append(line)
    elif mode == 'approve':
        if line.startswith('### ') and len(approve_cards) > 1:
            approve_cards.append([line])
        elif approve_cards:
            approve_cards[-1].append(line)
    elif mode == 'deep':
        deep.append(line)
    elif mode == 'tong_ket':
        tong_ket.append(line)

# Build compact report - just overview table + top approve + tong ket
date_str = datetime.date.today().strftime('%Y-%m-%d')

report = [f"""# 📋 Repo Intake Report — {date_str} (TÓM TẮT)
> Full report: `storage/vault/DATA/repo_intake_report_API_b1651_2026-03-27.md`
> **Data source: GitHub REST API v3 thực tế**

---

"""]

# Overview table
report.append('\n'.join(overview_lines[:5]))  # section header
report.append('\n')
# Get all table rows
table_rows = [l for l in overview_lines if l.startswith('|')]
report.append('\n'.join(table_rows[:10]))  # Header rows
report.append('\n')

# Count all rows
approve_rows = [l for l in table_rows if '✅' in l]
ref_rows = [l for l in table_rows if '📚' in l]
defer_rows = [l for l in table_rows if '🔖' in l]
reject_rows = [l for l in table_rows if '❌' in l]

report.append('\n'.join(approve_rows))
report.append('\n')
report.append('\n'.join(ref_rows[:100]))  # Lấy 100 REFERENCE đại diện
report.append('\n')
report.append('\n'.join(defer_rows))
report.append('\n')
report.append('\n'.join(reject_rows))
report.append('\n\n---\n\n')

# APPROVE cards - top 50
report.append('## CHI TIẾT — APPROVE repos (Top 50 theo Stars)\n')
for card in approve_cards[1:51]:  # skip section header, take 50
    report.append('\n'.join(card))
    report.append('\n')

report.append('\n---\n\n')

# Deep analysis
if deep:
    report.append('\n'.join(deep))
    report.append('\n\n---\n\n')

# Tong ket
if tong_ket:
    report.append('\n'.join(tong_ket))

full = '\n'.join(report) if isinstance(report, list) else report
# Actually we joined strings so:
full_text = ''.join(report)

OUT = os.path.join(ARTIFACTS, 'repo_intake_summary_2026-03-27.md')
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(full_text)

size_kb = os.path.getsize(OUT) / 1024
print(f"[OK] Summary saved: {OUT}")
print(f"[OK] Size: {size_kb:.0f} KB")
print(f"[OK] APPROVE rows: {len(approve_rows)}")
print(f"[OK] REFERENCE rows: {len(ref_rows)}")
