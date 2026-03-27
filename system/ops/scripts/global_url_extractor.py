import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
EXCLUDE_DIRS = ['.git', 'node_modules', 'venv', '.gemini', 'runtime', 'sandbox', 'AI OS REMOTE']
OUTPUT_FILE = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA', 'master_global_urls.txt')

# Regex for Github URLs strictly matching repos (e.g., https://github.com/user/repo)
github_pattern = re.compile(r'https?://(?:www\.)?github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+/?')
# General valid tools/links
general_pattern = re.compile(r'https?://[a-zA-Z0-9_.-]+\.[a-zA-Z]{2,}(?:/[^\s\)\]\"\']*)?')

def extract_urls(dir_path):
    all_urls = set()
    for root, dirs, files in os.walk(dir_path):
        # Exclude directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            if file.endswith(('.md', '.txt', '.json', '.yaml', '.yml')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                        # Find all URLs
                        gh_matches = github_pattern.findall(content)
                        gen_matches = general_pattern.findall(content)

                        for m in gh_matches:
                            # clean up trailing slashes or punct
                            m = m.strip('.,)"\'\]')
                            all_urls.add(m)

                        # Only add general matches if they look like tool sites, maybe too noisy?
                        # Let's just collect all http for now and we will filter
                        for m in gen_matches:
                            m = m.strip('.,)"\'\]')
                            all_urls.add(m)

                except Exception as e:
                    pass
    return all_urls

def filter_useful_urls(urls):
    filtered = set()
    noisy_domains = [
        'schemas.xmlsoap.org', 'docs.microsoft.com', 'w3.org', 'schemas.microsoft.com',
        'googleapis.com', 'localhost', '127.0.0.1', 'fonts.googleapis', 'npmjs.com'
    ]
    for url in urls:
        url_lower = url.lower()
        if any(noise in url_lower for noise in noisy_domains):
            continue
        filtered.add(url)
    return filtered

if __name__ == "__main__":
    print(f"[*] Scanning entire AI OS directory for URLs...")
    print(f"[*] Base: {BASE_DIR}")

    raw_urls = extract_urls(BASE_DIR)
    clean_urls = filter_useful_urls(raw_urls)

    # Sort them
    sorted_urls = sorted(list(clean_urls))

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for u in sorted_urls:
            f.write(u + '\n')

    print(f"[SUCCESS] Scanned entire AI OS. Found {len(sorted_urls)} unique URLs.")
    print(f"[>] Saved to: {OUTPUT_FILE}")
