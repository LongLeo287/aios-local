import os
import re
import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
REPORT_FILE = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA', f'repo_intake_report_FULL_{datetime.date.today()}.md')
QUARANTINE_DIR = os.path.join(BASE_DIR, 'system', 'security', 'QUARANTINE', 'incoming', 'REPO')
REF_CATALOG_FILE = os.path.join(BASE_DIR, 'brain', 'knowledge', 'notes', 'REFERENCE_REPOS_CATALOG.md')

def process_report():
    if not os.path.exists(REPORT_FILE):
        print(f"[!] Report not found: {REPORT_FILE}")
        return

    with open(REPORT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # The report contains blocks like:
    # ## CHI TIẾT — APPROVE REPOS
    # ### 1. some/repo
    # 🔗 https://github.com/some/repo

    # Extract APPROVE URLs (they are in the "CHI TIẾT — APPROVE REPOS" section)
    # Actually, we can just extract from the OVERVIEW table!
    # Format in table: | 1 | `org/repo` | ✅ APPROVE | Dept | Reason |
    # But wait, the report has URLs in the table? No, it has `name`.
    # Let's just find lines that look like 🔗 https://github.com/...

    # We can parse the full list by splitting the document.
    approve_urls = []
    reference_urls = []

    with open(REPORT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_section = None
    for line in lines:
        if "## CHI TIẾT — APPROVE REPOS" in line:
            current_section = "APPROVE"
            continue

        # The REFERENCE repos are only in the overview table.
        # Format: | 100 | `org/repo` | 📚 REFERENCE | Dept 00 — General | Reason |
        if "📚 REFERENCE" in line and "|" in line:
            parts = line.split("|")
            if len(parts) >= 4:
                repo_code = parts[2].strip()
                # repo_code is like `org/repo`
                repo_name = repo_code.replace("`", "")
                reference_urls.append(f"https://github.com/{repo_name}")

        # We can also extract APPROVE from the table to be safe!
        if "✅ APPROVE" in line and "|" in line:
            parts = line.split("|")
            if len(parts) >= 4:
                repo_code = parts[2].strip()
                repo_name = repo_code.replace("`", "")
                approve_urls.append(f"https://github.com/{repo_name}")

    # Deduplicate while preserving order
    approve_urls = list(dict.fromkeys(approve_urls))
    reference_urls = list(dict.fromkeys(reference_urls))

    print(f"[*] Found {len(approve_urls)} APPROVED repos in the report.")
    print(f"[*] Found {len(reference_urls)} REFERENCE repos in the report.")

    # 1. PROCESS APPROVE REPOS -> Write to QUARANTINE tickets & APPROVED_REPOS list
    os.makedirs(QUARANTINE_DIR, exist_ok=True)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")

    count_tickets = 0
    approved_list_file = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA', 'APPROVED_REPOS.txt')
    with open(approved_list_file, 'w', encoding='utf-8') as app_f:
        for i, url in enumerate(approve_urls):
            app_f.write(f"{url}\n")
            ticket_id = f"CIV-{date_str}-APPROVED-{str(i).zfill(4)}"
            ticket_file = os.path.join(QUARANTINE_DIR, f"{ticket_id}.txt")

            with open(ticket_file, 'w', encoding='utf-8') as f:
                f.write(f"Source: {url}\n")
                f.write("Type: REPO\n")
                f.write("Agent: batch-intake-agent\n")
                f.write("Route: brain/knowledge/repos/\n")
                f.write(f"Date: {date_str}\n")
            count_tickets += 1

    print(f"[SUCCESS] Dropped {count_tickets} CIV Tickets into {QUARANTINE_DIR}")
    print(f"[SUCCESS] Saved {count_tickets} approved URLs to {approved_list_file}")


    # 2. PROCESS REFERENCE REPOS -> Write to Markdown Catalog
    os.makedirs(os.path.dirname(REF_CATALOG_FILE), exist_ok=True)
    with open(REF_CATALOG_FILE, 'w', encoding='utf-8') as f:
        f.write("# 📚 AI OS Reference Repositories Catalog\n")
        f.write(f"> Generated on: {date_str} from intake backlog evaluation.\n")
        f.write("> Total: 1,444 repos. Trạng thái: Chỉ lưu trữ để tham khảo (chưa clone).\n\n")

        for url in reference_urls:
            f.write(f"- {url}\n")

    print(f"[SUCCESS] Saved {len(reference_urls)} links to {REF_CATALOG_FILE}")

if __name__ == '__main__':
    process_report()
