import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
INPUT_FILE = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA', 'master_global_urls.txt')
OUTPUT_FILE = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA', 'github_repos_only.txt')

# Matches exact github repo (user/repo), ignoring deep links to /tree/ or /blob/ or /issues/
# We just want the base repo url
gh_repo_pattern = re.compile(r'https?://(?:www\.)?github\.com/([a-zA-Z0-9_.-]+)/([a-zA-Z0-9_.-]+)$')

def filter_github_repos():
    repos = set()
    invalid_users = ['features', 'pricing', 'about', 'contact', 'login', 'explore', 'topics', 'trending']

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            url = line.strip()
            # If it has deeper paths, strip them to get the base repo
            # e.g. https://github.com/foo/bar/blob/main/readme -> https://github.com/foo/bar
            # First, filter to make sure the root domain is github
            if re.search(r'^https?://(?:www\.)?github\.com', url, re.IGNORECASE):
                # Remove trailing slash
                if url.endswith('/'):
                    url = url[:-1]

                parts = url.split('github.com/')
                if len(parts) == 2:
                    path_parts = parts[1].split('/')
                    if len(path_parts) >= 2:
                        user = path_parts[0]
                        repo = path_parts[1]

                        if user.lower() in invalid_users:
                            continue

                        # Format the pure repo URL
                        pure_url = f"https://github.com/{user}/{repo}"
                        # Clean up repo name of any hash, query param, or punctuation
                        pure_url = pure_url.split('#')[0].split('?')[0].strip('.,)"\'\]<>')

                        repos.add(pure_url)

    sorted_repos = sorted(list(repos))
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for r in sorted_repos:
            f.write(r + '\n')

    print(f"[*] Total Raw URLs: 98594")
    print(f"[*] Filtered Github Repos: {len(sorted_repos)}")
    print(f"[*] Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    filter_github_repos()
