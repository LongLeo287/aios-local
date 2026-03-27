import os
import json
import datetime
import urllib.parse
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
INPUT_FILE = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA', 'github_repos_only.txt')
VAULT_DATA_DIR = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA')

def sanitize_filename(url):
    name = url.split("github.com/")[-1]
    name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    return name

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"[!] File not found: {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    urls = [line.strip() for line in lines if line.strip()]
    count = 0

    timestamp_base = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    print(f"[*] Preparing to generate {len(urls)} intake tickets...")

    for i, url in enumerate(urls):
        safe_name = sanitize_filename(url)
        # Pad sequence number to avoid collision
        ticket_id = f"KI-{timestamp_base}{str(i).zfill(4)}"

        ticket_data = {
            "id": ticket_id,
            "type": "URL_INTAKE",
            "source": url,
            "priority": "P3", # Global scan gets normal priority
            "status": "PENDING_EVALUATION",
            "submitted_by": "antigravity-global-scanner",
            "timestamp": datetime.datetime.now().isoformat(),
            "validation": {
                "security_scan": "PENDING",
                "content_check": "PENDING",
                "alignment": "PENDING"
            }
        }

        filename = f"{ticket_id}_{safe_name}.json"
        filepath = os.path.join(VAULT_DATA_DIR, filename)

        with open(filepath, 'w', encoding='utf-8') as jf:
            json.dump(ticket_data, jf, indent=2)

        count += 1

    print(f"[SUCCESS] Dropped {count} Master Global Intake Tickets into Vault/DATA/.")
    print(f"[*] The internal departments (Strix, Navigator) will process these queued items iteratively.")

if __name__ == "__main__":
    main()
