import re
from collections import Counter

files = [
    r'<AI_OS_ROOT>\storage\vault\DATA\PENDING_REPOS.md',
    r'<AI_OS_ROOT>\storage\vault\DATA\ACTIVE_REPOS.md'
]
dept_counts = Counter()
total = 0

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            for line in file:
                # regex: (Dept \d+) possibly with names like "Dept 07 — Knowledge" or "Dept 04 - Dev"
                m = re.search(r'(Dept\s+\d+\s+[-—]\s+[^|]+)', line)
                if m:
                    dept = m.group(1).strip()
                    dept_counts[dept] += 1
                    total += 1
                else:
                    m2 = re.search(r'(Dept\s+\d+)', line)
                    if m2:
                        dept = m2.group(1).strip()
                        dept_counts[dept] += 1
                        total += 1
    except Exception as e:
        print(e)
        pass

print(f'\n[BÁO CÁO NHANH]\nTổng số Repo khai thác: {total} Repos (PENDING + ACTIVE)')
print('--- Tỉ trọng theo Phòng Ban ---')
for dept, count in dept_counts.most_common():
    print(f'- {dept}: {count} repos')
