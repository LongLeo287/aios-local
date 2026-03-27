import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
TARGET_DIRS = [
    os.path.join(BASE_DIR, 'system', 'ops', 'HUD'),
    os.path.join(BASE_DIR, 'brain', 'knowledge'),
    os.path.join(BASE_DIR, 'storage', 'vault')
]
OUTPUT_FILE = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA', 'master_global_urls.txt')

github_pattern = re.compile(r'https?://(?:www\.)?github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+/?')
general_pattern = re.compile(r'https?://[a-zA-Z0-9_.-]+\.[a-zA-Z]{2,}(?:/[^\s\)\]\"\']*)?')

def extract_urls(targets):
    all_urls = set()
    for t_dir in targets:
        if not os.path.exists(t_dir):
            continue
        for root, dirs, files in os.walk(t_dir):
            for file in files:
                if file.endswith(('.md', '.txt', '.json', '.yaml', '.yml')):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            gh = github_pattern.findall(content)
                            gen = general_pattern.findall(content)
                            for m in gh:
                                all_urls.add(m.strip('.,)"\'\]<>'))
                            for m in gen:
                                all_urls.add(m.strip('.,)"\'\]<>'))
                    except Exception as e:
                        pass
    return all_urls

def filter_useful_urls(urls):
    filtered = set()
    noisy = ['schemas.', 'docs.microsoft', 'w3.org', 'googleapis', 'localhost', '127.0.0.1', 'npmjs.com']
    for url in urls:
        url_lower = url.lower()
        if any(n in url_lower for n in noisy): continue
        filtered.add(url)
    return filtered

if __name__ == "__main__":
    raw_urls = extract_urls(TARGET_DIRS)
    clean_urls = filter_useful_urls(raw_urls)
    sorted_urls = sorted(list(clean_urls))

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for u in sorted_urls:
            f.write(u + '\n')

    print(f"[SUCCESS] Scanned HUD, Brain, Vault. Found {len(sorted_urls)} unique URLs.")
