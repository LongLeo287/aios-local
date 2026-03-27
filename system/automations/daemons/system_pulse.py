#!/usr/bin/env python3
"""
system/automations/daemons/system_pulse.py — AI OS System Health Pulse Checker (B5)
Chạy mỗi 5 phút. Gửi Telegram alert nếu có issue.

NOTE (2026-03-27): Services giờ chạy từ AI OS REMOTE (<AI_OS_REMOTE_ROOT>)
  - ClawTask :7474   → REMOTE/claws/nullclaw/ hoặc REMOTE/scripts/start_nullclaw.ps1
  - LightRAG :9621   → REMOTE/scripts/lightrag_server.py
  - Telegram Bridge  → REMOTE/infra/channels/start_bridges.py
  script này CHỈ check port (socket ping), không import module nào từ REMOTE.

Usage:
  python system/automations/daemons/system_pulse.py           # One-shot
  python system/automations/daemons/system_pulse.py --loop    # Loop mỗi 5 phút
  python system/automations/daemons/system_pulse.py --quiet   # Chỉ alert khi có issue
"""
import sys
import os
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from urllib.request import urlopen, Request

ROOT = Path(__file__).parent.parent.parent
BB   = ROOT / "brain" / "shared-context" / "blackboard.json"
ENV  = ROOT / ".env"

# Load .env for TELEGRAM creds
def _load_env():
    env = {}
    for path in [ENV, ROOT / "ops" / "secrets" / "MASTER.env"]:
        if path.exists():
            for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                if "=" in line and not line.startswith("#"):
                    k, _, v = line.partition("=")
                    env[k.strip()] = v.strip()
    return env

_ENV = _load_env()
TOKEN   = _ENV.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = _ENV.get("TELEGRAM_CHAT_ID", "")

LOOP_INTERVAL = 300   # 5 minutes
QUIET = "--quiet" in sys.argv

# ─── Checks ──────────────────────────────────────────────────────────────────
def check_port(host: str, port: int, name: str) -> dict:
    import socket
    try:
        with socket.create_connection((host, port), timeout=2):
            return {"name": name, "status": "UP", "ok": True}
    except Exception:
        return {"name": name, "status": "DOWN", "ok": False}

def check_blackboard() -> dict:
    try:
        bb = json.loads(BB.read_text(encoding="utf-8"))
        age_ok = True  # Could check timestamp freshness
        return {"name": "Blackboard", "status": "OK", "ok": True, "cycle": bb.get("corp_cycle_number")}
    except Exception as e:
        return {"name": "Blackboard", "status": f"ERR:{e}", "ok": False}

def check_bridge() -> dict:
    """Check Telegram Bridge via blackboard heartbeat.
    Bridge chạy từ: <AI_OS_REMOTE_ROOT>\infra\channels\start_bridges.py
    """
    try:
        bb = json.loads(BB.read_text(encoding="utf-8"))
        last_msg = bb.get("telegram_last_message", {})
        if last_msg:
            return {"name": "Telegram Bridge (REMOTE)", "status": "SEEN_MSG", "ok": True}
        return {"name": "Telegram Bridge (REMOTE)", "status": "NO_MSG", "ok": True}
    except Exception:
        return {"name": "Telegram Bridge (REMOTE)", "status": "UNKNOWN", "ok": True}

CHECKS = [
    lambda: check_port("127.0.0.1", 11434, "Ollama :11434"),
    # ClawTask chạy từ: AI OS REMOTE/claws/nullclaw/ hoặc REMOTE/scripts/start_nullclaw.ps1
    lambda: check_port("127.0.0.1", 7474,  "ClawTask :7474 (REMOTE)"),
    # LightRAG chạy từ: AI OS REMOTE/scripts/lightrag_server.py
    lambda: check_port("127.0.0.1", 9621,  "LightRAG :9621 (REMOTE)"),
    check_blackboard,
    check_bridge,
]

# ─── Telegram Notify ─────────────────────────────────────────────────────────
def send_telegram(text: str):
    if not TOKEN or not CHAT_ID:
        return
    try:
        payload = json.dumps({"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}).encode()
        req = Request(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        urlopen(req, timeout=5)
    except Exception as e:
        print(f"[Telegram ERR] {e}")

# ─── Run checks ──────────────────────────────────────────────────────────────
def run_pulse() -> list:
    results = []
    for check_fn in CHECKS:
        result = check_fn()
        results.append(result)
        status_icon = "✅" if result["ok"] else "❌"
        if not QUIET or not result["ok"]:
            print(f"  {status_icon} {result['name']}: {result['status']}")
    return results

def format_alert(issues: list) -> str:
    ts = datetime.now().strftime("%H:%M:%S")
    lines = [f"⚠️ *AI OS System Pulse* — {ts}"]
    for issue in issues:
        lines.append(f"  ❌ `{issue['name']}` — {issue['status']}")
    lines.append("\nCheck: `python ops/aos.py status`")
    return "\n".join(lines)

def main():
    loop = "--loop" in sys.argv
    print(f"{'[LOOP] ' if loop else ''}AI OS System Pulse — {datetime.now().strftime('%H:%M:%S')}")

    while True:
        if not QUIET:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Running checks...")
        results = run_pulse()

        issues = [r for r in results if not r["ok"]]
        if issues:
            alert = format_alert(issues)
            send_telegram(alert)
            if not QUIET:
                print(f"\n⚠️  {len(issues)} issue(s) — Telegram alert sent")
        elif not QUIET:
            print(f"✅ All checks passed")

        if not loop:
            break
        print(f"  Next check in {LOOP_INTERVAL}s...")
        time.sleep(LOOP_INTERVAL)

if __name__ == "__main__":
    main()
