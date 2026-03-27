#!/usr/bin/env python3
"""
AI OS V3.1 — Telegram Bot Dispatch
Path: system/ops/telegram_dispatch.py
Author: Antigravity (2026-03-26)

Đây là module gửi thực tế lên Telegram Bot của AI OS Corp.
Dùng python-telegram-bot hoặc raw HTTP request.
"""

import os
import json
import datetime
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
ENV_FILE = ROOT / ".env"

# ─── Load ENV ────────────────────────────────────────────────────────────────
def load_env(path=ENV_FILE):
    env = {}
    if not path.exists():
        return env
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env

ENV = load_env()
BOT_TOKEN = ENV.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID   = ENV.get("TELEGRAM_CHAT_ID", "")

# ─── PRIORITY ICONS ──────────────────────────────────────────────────────────
ICONS = {
    "CRITICAL": "🚨",
    "HIGH":     "⚠️",
    "INFO":     "📊",
    "LOW":      "💬",
    "OK":       "✅",
    "DONE":     "🎯",
}

# ─── CORE SEND ───────────────────────────────────────────────────────────────
def send_telegram(text: str, parse_mode="Markdown") -> dict:
    """Gửi message qua Telegram Bot API (raw HTTP)"""
    if not BOT_TOKEN or not CHAT_ID:
        print(f"[TELEGRAM-SKIP] No BOT_TOKEN/CHAT_ID configured. Message: {text[:60]}")
        return {"ok": False, "reason": "no_credentials"}

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = json.dumps({
        "chat_id":    CHAT_ID,
        "text":       text,
        "parse_mode": parse_mode
    }).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=payload,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            print(f"[TELEGRAM-OK] Sent to {CHAT_ID}: {text[:60]}...")
            return result
    except Exception as e:
        print(f"[TELEGRAM-ERR] Failed: {e}")
        return {"ok": False, "error": str(e)}


def notify(title: str, body: str, priority: str = "INFO") -> dict:
    """High-level notify: format + send"""
    icon = ICONS.get(priority, "•")
    ts   = datetime.datetime.now().strftime("%H:%M")

    msg = f"{icon} *{title}*\n{body}\n_⏰ {ts} | AI OS V3.1_"
    return send_telegram(msg)


def send_system_status():
    """Gửi daily system status digest"""
    try:
        status_path = ROOT / "system" / "hud" / "STATUS.json"
        with open(status_path, encoding="utf-8-sig") as f:
            s = json.load(f)

        msg = (
            f"📊 *AI OS V3.1 — System Status*\n\n"
            f"• 🤖 Agents: `{s.get('agents', 'N/A')}`\n"
            f"• 🧠 Skills:  `{s.get('skills', 'N/A')}`\n"
            f"• 🔌 MCPs:   `{s['kho']['mcp']['servers']}`\n"
            f"• 📦 Plugins: `{s['kho']['plugins']['plugins']}`\n"
            f"• ♻️ Cycle:  `{s.get('cycle', 'N/A')}`\n"
            f"• 🔄 Reconnect: `{s.get('v31_reconnect', 'N/A')}`\n\n"
            f"_Updated: {s.get('last_hud_update', 'unknown')}_"
        )
        return send_telegram(msg)
    except Exception as e:
        return {"ok": False, "error": str(e)}


def alert_task_dispatched(task_id: str, agent: str, skill: str) -> dict:
    return notify(
        title=f"Task Dispatched: {task_id}",
        body=f"→ Agent: `{agent}`\n→ Skill: `{skill}`",
        priority="INFO"
    )


def alert_task_blocked(task_id: str, agent: str, reason: str) -> dict:
    return notify(
        title=f"⛔ BLOCKED: {task_id}",
        body=f"Agent: `{agent}`\nReason: {reason}\n→ Manual review needed",
        priority="HIGH"
    )


def alert_security(issue: str, severity: str = "CRITICAL") -> dict:
    return notify(
        title=f"Security Alert [{severity}]",
        body=issue,
        priority="CRITICAL"
    )


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "status":
        result = send_system_status()
        print(json.dumps(result, indent=2))

    elif cmd == "test":
        result = notify(
            title="AI OS V3.1 — Test Notification",
            body="✅ Telegram dispatch đã kết nối thành công!",
            priority="OK"
        )
        print(json.dumps(result, indent=2))

    elif cmd == "alert":
        msg = sys.argv[2] if len(sys.argv) > 2 else "Manual alert from AI OS"
        priority = sys.argv[3] if len(sys.argv) > 3 else "INFO"
        result = notify("Manual Alert", msg, priority)
        print(json.dumps(result, indent=2))

    else:
        print("Usage: python telegram_dispatch.py [status|test|alert <msg> <priority>]")
