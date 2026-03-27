import os, re
data_dir = r"<AI_OS_ROOT>\storage\vault\DATA"
files = ["github_repos_clean.txt", "ACTIVE_REPOS.md", "PENDING_REPOS.md", "ARCHIVED_REPOS.md"]
total_unique = set()
print("=== THỐNG KÊ REPO ===")
for f in files:
    path = os.path.join(data_dir, f)
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as fr:
        content = fr.read()
        matches = re.findall(r'github\.com/([a-zA-Z0-9_\.-]+/[a-zA-Z0-9_\.-]+)', content)
        clean_matches = [m.lower() for m in matches]
        print(f"File {f}: {len(set(clean_matches))} repos")
        total_unique.update(clean_matches)

print(f"\n=> TỔNG CỘNG UNIQUE: {len(total_unique)} repos")
