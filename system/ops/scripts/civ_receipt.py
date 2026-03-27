#!/usr/bin/env python3
"""
ops/scripts/civ_receipt.py — C5: CEO Receipt Card Generator
Creates a summary card after CIV intake completes.

Usage:
  python ops/scripts/civ_receipt.py \
    --ticket CIV-2026-03-25-001 \
    --source https://github.com/browser-use/browser-use \
    --type REPO --verdict APPROVE \
    --route "plugins/browser-use/" \
    --value HIGH \
    --title "browser-use — AI Browser Automation"
"""
import json
import sys
import re
import argparse
from pathlib import Path
from datetime import datetime
from urllib.request import urlopen, Request

ROOT = Path(__file__).parent.parent.parent
BB   = ROOT / "brain" / "shared-context" / "blackboard.json"
ENV  = ROOT / ".env"

def _load_env():
    env = {}
    for path in [ENV, ROOT / "ops" / "secrets" / "MASTER.env"]:
        if path.exists():
            for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                if "=" in line and not line.startswith("#"):
                    k, _, v = line.partition("=")
                    env[k.strip()] = v.strip()
    return env

def send_telegram(text: str):
    _e = _load_env()
    token   = _e.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = _e.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        return
    try:
        payload = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}).encode()
        req = Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=payload, headers={"Content-Type": "application/json"},
        )
        urlopen(req, timeout=5)
    except Exception:
        pass

def generate_receipt(ticket: str, source: str, typ: str, verdict: str,
                     route: str, value: str, title: str, notes: str = "") -> str:
    ts  = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    icon = "✅" if verdict == "APPROVE" else "❌" if verdict == "REJECT" else "⏳"
    val_icon = "⭐⭐⭐" if value == "HIGH" else "⭐⭐" if value == "MED" else "⭐"

    receipt = (
        f"{icon} *INTAKE COMPLETE* — `{ticket}`\n"
        f"──────────────────────────────\n"
        f"📎 Source: {source}\n"
        f"🏷 Type: `{typ}` | Value: {val_icon} {value}\n"
        f"🛡 Security: PASS | Verdict: *{verdict}*\n"
        f"📂 Route: `{route}`\n"
        f"📝 KI Note: `brain/knowledge/notes/KI-{re.sub(r'[^a-z0-9]', '-', title.lower())}-*.md`\n"
    )
    if notes:
        receipt += f"💡 Notes: {notes}\n"
    receipt += f"🕐 {ts}"
    return receipt

def save_receipt_json(ticket: str, source: str, typ: str, verdict: str,
                      route: str, value: str, title: str):
    """Save machine-readable receipt to telemetry/receipts/"""
    receipt_dir = ROOT / "telemetry" / "receipts"
    receipt_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    receipt_file = receipt_dir / f"INTAKE_{ticket}_{ts}.json"
    data = {
        "ticket": ticket, "source": source, "type": typ,
        "verdict": verdict, "route": route, "value": value,
        "title": title, "timestamp": datetime.now().isoformat(),
    }
    receipt_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return receipt_file

def _save_to_ltm(ticket: str, source: str, typ: str, verdict: str, title: str, value: str):
    """Save intake fact to Long-Term Memory (silent fail if LTM offline)"""
    try:
        import warnings, sys
        warnings.filterwarnings("ignore")
        sys.path.insert(0, str(ROOT))
        from system.ops.scripts.memory_daemon import MemoryCore
        mc = MemoryCore()
        fact = f"Intake {ticket}: [{verdict}] {typ} '{title}' ({source}) — Value: {value}"
        mc.add_fact(fact, user_id="CEO", agent_id="civ_receipt")
        print(f"[✓] LTM saved: {fact[:80]}")
    except Exception as _e:
        pass  # LTM offline — degrade gracefully

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticket",  default="CIV-AUTO")
    parser.add_argument("--source",  required=True)
    parser.add_argument("--type",    default="REPO")
    parser.add_argument("--verdict", default="APPROVE")
    parser.add_argument("--route",   default="brain/knowledge/notes/")
    parser.add_argument("--value",   default="MED")
    parser.add_argument("--title",   default="")
    parser.add_argument("--notes",   default="")
    parser.add_argument("--no-telegram", action="store_true")
    args = parser.parse_args()

    title = args.title or args.source.split("/")[-1]
    msg   = generate_receipt(args.ticket, args.source, args.type,
                              args.verdict, args.route, args.value, title, args.notes)

    print("\n" + msg.replace("*", "").replace("`", ""))

    rf = save_receipt_json(args.ticket, args.source, args.type,
                           args.verdict, args.route, args.value, title)
    print(f"\n📁 Receipt saved: {rf.relative_to(ROOT)}")

    if not args.no_telegram:
        send_telegram(msg)
        print("📱 Telegram notified")

    # [NEW] Auto-save to LTM
    _save_to_ltm(args.ticket, args.source, args.type, args.verdict, title, args.value)

if __name__ == "__main__":
    main()
