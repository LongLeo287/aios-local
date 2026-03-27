import os
import json
import datetime
import urllib.parse

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
VAULT_DATA_DIR = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA')
TARGET_FILE = os.path.join(VAULT_DATA_DIR, 'missing_repos.txt')

def main():
    os.makedirs(VAULT_DATA_DIR, exist_ok=True)
    print(f"[{datetime.datetime.now().isoformat()}] STARTING BULK INTAKE V2 (TOTAL EXTINCTION)...")

    if not os.path.exists(TARGET_FILE):
        print(f"[ERROR] Could not find {TARGET_FILE}")
        return

    # Read the text file containing the URLs
    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f.readlines() if line.strip() and line.strip().startswith('http')]

    print(f"[*] Discovered {len(urls)} URLs inside {TARGET_FILE}.")

    count = 0
    for idx, url in enumerate(urls):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + f"{idx:03d}"
        ki_id = f"KI-{timestamp}"

        # Parse the repo name or path to use in the filename
        parsed = urllib.parse.urlparse(url)
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) >= 2:
            safe_name = f"{path_parts[-2]}_{path_parts[-1]}"
        elif len(path_parts) == 1 and path_parts[0]:
            safe_name = path_parts[0]
        else:
            safe_name = "url_entry"

        # Dọn dẹp tên file
        safe_name = "".join(c for c in safe_name if c.isalnum() or c in ('_', '-'))

        ticket = {
            "id": ki_id,
            "source_type": "url_repo_bulk",
            "source": url,
            "submitted_by": "antigravity-bulk-intake-v2",
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "PENDING_CLASSIFICATION",
            "metadata_hints": {
                "knowledge_type": "RESEARCH_OR_TOOL",
                "suggested_domains": ["general"],
                "ceo_notes": "Bulk ingestion from missing_repos.txt backlog. Tự động nhận diện Domain và đẻ Agent mới nếu trống."
            }
        }

        filename = f"{ki_id}_{safe_name}.json"
        filepath = os.path.join(VAULT_DATA_DIR, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(ticket, f, indent=4, ensure_ascii=False)

        print(f"  [+] Prepared Ticket: {filename} -> {url}")
        count += 1

    print(f"\n[SUCCESS] Dropped {count} Massive Intake Tickets into {VAULT_DATA_DIR}.")
    print("Daemon 'auto_evolution_engine' should now detect ALL 91 tickets and swallow them into the knowledge pipeline.")

if __name__ == "__main__":
    main()
