"""
save_session_memory.py — Auto-save session summary to LTM (Long-Term Memory)
Gọi cuối mỗi phiên làm việc để lưu ký ức vĩnh viễn vào MemoryCore.
Usage:
  python save_session_memory.py "Tóm tắt phiên: hoàn thành X, Y, Z"
  python save_session_memory.py --from-blackboard  (auto-read from blackboard.json)
"""
import os
import sys
import json
import warnings
warnings.filterwarnings("ignore")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
BB_PATH = os.path.join(ROOT, "brain", "shared-context", "blackboard.json")

sys.path.insert(0, ROOT)
from system.ops.scripts.memory_daemon import MemoryCore

def save_text(text, user_id="CEO", agent_id="antigravity"):
    core = MemoryCore()
    result = core.add_fact(text, user_id=user_id, agent_id=agent_id)
    print(f"[✓] LTM saved: {text[:80]}...")
    return result

def save_from_blackboard():
    try:
        with open(BB_PATH, 'r', encoding='utf-8-sig', errors='replace') as f:
            bb = json.load(f)

        facts = []

        # Extract active_campaign
        campaign = bb.get("active_campaign")
        if campaign:
            facts.append(f"AI OS đang ở campaign: {campaign}")

        # Extract last_session summary
        last_session = bb.get("last_session", {})
        if last_session:
            ts = last_session.get("timestamp", "unknown")
            summary = last_session.get("summary", "")
            if summary:
                facts.append(f"Phiên làm việc {ts}: {summary}")

        # Extract open_items
        open_items = bb.get("open_items", [])
        if open_items:
            titles = []
            for item in open_items[:5]:
                if isinstance(item, dict):
                    titles.append(item.get("title", str(item)[:50]))
                else:
                    titles.append(str(item)[:50])
            facts.append(f"Việc tồn đọng: {'; '.join(titles)}")

        # Extract corp status
        status = bb.get("system_status", "")
        cycle = bb.get("active_campaign", "")
        if status:
            facts.append(f"System status: {status} | Campaign: {cycle}")

        if facts:
            core = MemoryCore()
            for fact in facts:
                core.add_fact(fact, user_id="CEO", agent_id="postprocess")
                print(f"  [+] {fact[:80]}")
            print(f"[✓] Saved {len(facts)} memory nodes from blackboard")
        else:
            print("[~] No facts to extract from blackboard")

    except Exception as e:
        print(f"[!] Failed to read blackboard: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: save_session_memory.py <text> | --from-blackboard")
        sys.exit(1)

    if sys.argv[1] == "--from-blackboard":
        save_from_blackboard()
    else:
        text = " ".join(sys.argv[1:])
        save_text(text)
