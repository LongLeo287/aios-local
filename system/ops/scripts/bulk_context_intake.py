import os
import json
import datetime
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
VAULT_DATA_DIR = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA')
OUTPUT_CATALOG = os.path.join(VAULT_DATA_DIR, 'contextual_files_catalog.md')

# Look for standard directories
WORKFLOW_DIRS = [os.path.join(BASE_DIR, 'system', 'ops', 'workflows'), os.path.join(BASE_DIR, '.agents', 'workflows')]
PACKAGE_DIRS = [os.path.join(BASE_DIR, 'system'), os.path.join(BASE_DIR, 'ecosystem'), os.path.join(BASE_DIR, 'AI OS REMOTE')]
LOG_DIRS = [os.path.join(os.path.expanduser('~'), '.gemini', 'antigravity', 'brain')]

github_pattern = re.compile(r'https?://(?:www\.)?github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+/?')

def scan_for_contextual_files():
    valid_files = set()

    # 1. Workflow MD files
    for w_dir in WORKFLOW_DIRS:
        if not os.path.exists(w_dir): continue
        for root, dirs, files in os.walk(w_dir):
            for file in files:
                if file.endswith('.md'):
                    valid_files.add(os.path.join(root, file))

    # 2. Package.json with Github Repos
    for p_dir in PACKAGE_DIRS:
        if not os.path.exists(p_dir): continue
        for root, dirs, files in os.walk(p_dir):
            # Exclude node_modules to avoid nested madness
            if 'node_modules' in dirs: dirs.remove('node_modules')
            if 'package.json' in files:
                filepath = os.path.join(root, 'package.json')
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        if 'github.com' in f.read():
                            valid_files.add(filepath)
                except: pass

    # 3. Chat Logs (txt/md/json in logs)
    # We will pick up conversation overviews and logs if available
    for l_dir in LOG_DIRS:
        if not os.path.exists(l_dir): continue
        for root, dirs, files in os.walk(l_dir):
            if 'logs' in root or '.system_generated' in root:
                for file in files:
                    if file.endswith(('.txt', '.md', '.json')):
                        valid_files.add(os.path.join(root, file))

    return list(valid_files)

def generate_intake_tickets(files):
    timestamp_base = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    count = 0
    catalog = ["# 📑 Contextual Files Ingest Catalog\n"]

    for i, filepath in enumerate(files):
        # Determine logical type
        logical_type = "DOC"
        if filepath.endswith('.json'):
            if 'package.json' in filepath: logical_type = "STRUCTURE"
            else: logical_type = "CHAT_LOG"
        elif 'log' in filepath.lower():
            logical_type = "CHAT_LOG"
        elif filepath.endswith('.md'):
            logical_type = "WORKFLOW"

        ticket_id = f"KI-CTX-{timestamp_base}{str(i).zfill(4)}"
        safe_name = os.path.basename(filepath).replace(' ', '_')

        ticket_data = {
            "id": ticket_id,
            "type": logical_type,
            "source": f"file://{filepath}",
            "priority": "P2", # Context eval is higher than bulk URL
            "status": "PENDING_EVALUATION",
            "submitted_by": "antigravity-context-extractor",
            "timestamp": datetime.datetime.now().isoformat()
        }

        target_path = os.path.join(VAULT_DATA_DIR, f"{ticket_id}_{safe_name}.json")
        with open(target_path, 'w', encoding='utf-8') as jf:
            json.dump(ticket_data, jf, indent=2)

        catalog.append(f"- **{ticket_id}**: `{filepath}` (Type: {logical_type})")
        count += 1

    with open(OUTPUT_CATALOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(catalog))

    print(f"[SUCCESS] Packaged {count} Contextual Files into Vault/DATA/ tickets.")
    print(f"[*] Catalog saved to: {OUTPUT_CATALOG}")

if __name__ == "__main__":
    files = scan_for_contextual_files()
    generate_intake_tickets(files)
