import os
import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
INPUT_FILE = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA', 'ALL_PENDING_REPOS.txt')
STAGING_DIR = os.path.join(BASE_DIR, 'system', 'security', 'QUARANTINE', 'incoming', 'REPO')

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"[!] File not found: {INPUT_FILE}")
        return

    os.makedirs(STAGING_DIR, exist_ok=True)

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    count = 0

    print(f"[*] Preparing to generate {len(urls)} OFFICIAL CIV intake tickets in QUARANTINE...")

    for i, url in enumerate(urls):
        ticket_id = f"CIV-{date_str}-BATCH-{str(i).zfill(4)}"
        ticket_file = os.path.join(STAGING_DIR, f"{ticket_id}.txt")

        with open(ticket_file, 'w', encoding='utf-8') as f:
            f.write(f"Source: {url}\n")
            f.write("Type: REPO\n")
            f.write("Agent: batch-intake-agent\n")
            f.write("Route: brain/knowledge/repos/\n")
            f.write(f"Date: {date_str}\n")

        count += 1

    print(f"[SUCCESS] Dropped {count} Official CIV Tickets into {STAGING_DIR}")
    print(f"[*] The Strix Security Agent and standard pipeline can now process them legitimately.")

if __name__ == '__main__':
    main()
