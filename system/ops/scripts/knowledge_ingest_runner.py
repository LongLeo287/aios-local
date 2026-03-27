import os
import json
import time
import datetime
import glob
import random

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
VAULT_DATA_DIR = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA')
STAGING_DIR = os.path.join(BASE_DIR, 'brain', 'knowledge', 'staging')
REJECTED_DIR = os.path.join(BASE_DIR, 'system', 'security', 'QUARANTINE', 'REJECTED')
PROCESSED_DIR = os.path.join(BASE_DIR, 'storage', 'vault', 'PROCESSED')

os.makedirs(STAGING_DIR, exist_ok=True)
os.makedirs(REJECTED_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

def print_log(agent, message, color_code="0"):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    # ANSI colors for terminal
    print(f"\033[{color_code}m[{timestamp}] [{agent.upper()}]\033[0m {message}")

def simulate_strix_scan(url):
    # Dummy security scan
    time.sleep(0.5)
    bad_keywords = ['xpfarm', 'hexhog', 'wifi-card', 'leak', 'prompt_leaks']
    for bad in bad_keywords:
        if bad in url.lower():
            return False, f"Malicious/Irrelevant pattern detected ({bad})"
    return True, "Clean"

def simulate_navigator_classification(url):
    time.sleep(0.5)
    url_lower = url.lower()
    if 'browser' in url_lower or 'web-check' in url_lower:
        return {"domain": "web_ops", "dept": "Dept 11", "type": "TOOL", "verdict": "APPROVE"}
    elif 'claw' in url_lower or 'agent' in url_lower:
        return {"domain": "ai_agent", "dept": "Dept 01", "type": "TOOL", "verdict": "APPROVE"}
    elif 'ui' in url_lower or 'animation' in url_lower:
        return {"domain": "frontend", "dept": "Dept 05", "type": "REFERENCE", "verdict": "DEFER"}
    else:
        return {"domain": "general", "dept": "Dept 00", "type": "RESEARCH", "verdict": "REFERENCE"}

def process_ticket(filepath):
    filename = os.path.basename(filepath)
    print_log("system", f"--- NEW TICKET DETECTED: {filename} ---", "35")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    source = data.get("source", "Unknown")
    ki_id = data.get("id", "KI-UNKNOWN")

    print_log("intake-chief", f"Ingesting source: {source}", "36")

    # Phase 2: Security Scan (Strix-Agent)
    print_log("strix-agent", "Running vulnerability & relevance scan...", "31")
    is_safe, sec_reason = simulate_strix_scan(source)
    if not is_safe:
        print_log("strix-agent", f"❌ REJECTED. Reason: {sec_reason}", "31")
        # Move to rejected
        os.rename(filepath, os.path.join(REJECTED_DIR, filename))
        return
    print_log("strix-agent", "✅ PASS. Source is clean.", "32")

    # Phase 3: Classification (Knowledge Navigator)
    print_log("knowledge-navigator", "Analyzing domain gaps and AI OS alignment...", "33")
    analysis = simulate_navigator_classification(source)

    print_log("knowledge-navigator", f"Verdict: {analysis['verdict']} | Type: {analysis['type']} | Target: {analysis['dept']}", "33")

    # Phase 4/5/6: Archiving / Auto-Creation trigger
    if analysis['verdict'] == "APPROVE":
        print_log("archivist", f"Preparing to link {ki_id} into Brain -> triggering agent-auto-create check.", "34")
        new_path = os.path.join(STAGING_DIR, filename)
    else:
        print_log("archivist", f"Routing {ki_id} to passive storage (DEFER/REFERENCE).", "34")
        new_path = os.path.join(PROCESSED_DIR, filename)

    os.rename(filepath, new_path)
    print_log("system", f"Ticket {ki_id} processed successfully.\n", "35")

def main():
    print(f"============================================================")
    print(f"  AI OS AUTO-EVOLUTION ENGINE (KNOWLEDGE INGEST RUNNER)     ")
    print(f"============================================================")

    search_pattern = os.path.join(VAULT_DATA_DIR, 'KI-*_*.json')
    files = glob.glob(search_pattern)
    files.sort()

    if not files:
        print("[!] Vault/DATA/ is empty. No tickets to process.")
        return

    # We process just a batch of 5 to demonstrate the flow to the CEO
    batch_size = 5
    to_process = files[:batch_size]

    print(f"Found {len(files)} total tickets. Processing a batch of {batch_size} for demonstration...\n")

    for fpath in to_process:
        process_ticket(fpath)
        time.sleep(1) # simulate think time

    print(f"Batch complete. {len(files) - batch_size} tickets remaining in Vault/DATA/.")

if __name__ == "__main__":
    main()
