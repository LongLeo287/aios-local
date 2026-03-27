import os
import re
import json
import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
INPUT_FILE = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA', 'github_repos_only.txt')
CLEAN_FILE = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA', 'github_repos_clean.txt')
REPORT_DIR = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA')

# Known real user/org names to exclude from our filter (false positives)
FAKE_USERS = [
    'YOUR-USERNAME', 'YOUR_USERNAME', 'YOUR_ORG', 'your-user', 'your-username', 'your_github_username',
    'username', 'owner', 'company', 'example', 'acme-corp', 'anotherowner',
    'GITHUB_REPOSITORY', '<USER>', '<REPO>', '<YOURr', 'api-playground',
    'articles', 'en', 'docs', 'gh-aw', 'gists', 'blog', 'enterprise', 'enterprise-server',
    'apps', 'app', 'topics', 'admin', 'authorizations', 'code-security', 'applications',
    'activities', 'advisories', 'assets', 'codes_of_conduct', 'copilot', 'PR',
    'Ticket', 'PrivateCrypMix', 'Owner',
]

# Fake repo names
FAKE_REPOS = [
    'issues', 'discussions', 'pulls', 'hooks', 'releases', 'blob', 'tree', 'linear.app',
    'forking', 'installation', 'grants', 'introduction', 'reference',
]

def is_valid_repo(url):
    # Must have exactly 2 path segments after github.com
    path = url.split('github.com/')[-1].strip('/')
    if '<' in path or '>' in path or '{' in path or '${' in path:
        return False

    parts = path.split('/')
    if len(parts) < 2:
        return False

    user, repo = parts[0], parts[1]

    if user.lower() in [f.lower() for f in FAKE_USERS]:
        return False

    if repo.lower() in [r.lower() for r in FAKE_REPOS]:
        return False

    # Must have real username pattern (alphanumeric+dots+dashes)
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9\.\-\_]+$', user):
        return False

    # repo name must be valid
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9\.\-\_]+$', repo.rstrip('.')):
        return False

    # Remove .git suffix duplicates
    return True

def clean_repos():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        raw = [line.strip() for line in f if line.strip()]

    # Normalize - strip .git, trailing backticks/chars
    seen = set()
    clean = []
    for url in raw:
        url = url.rstrip('.`\\'
)
        if url.endswith('.git'):
            url = url[:-4]
        # Strip auth trailing chars
        url = url.split('#')[0].split('?')[0].strip('.,)"\'"')

        if not is_valid_repo(url):
            continue

        # Deduplicate
        key = url.lower()
        if key not in seen:
            seen.add(key)
            clean.append(url)

    clean.sort()

    with open(CLEAN_FILE, 'w', encoding='utf-8') as f:
        for u in clean:
            f.write(u + '\n')

    print(f"[*] Raw URLs: {len(raw)}")
    print(f"[*] Clean & Unique Repos: {len(clean)}")
    print(f"[*] Rejected (template/fake/noise): {len(raw) - len(clean)}")
    print(f"[>] Saved to: {CLEAN_FILE}")
    return clean

if __name__ == "__main__":
    clean_repos()
