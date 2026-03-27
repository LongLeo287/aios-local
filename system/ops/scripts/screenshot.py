#!/usr/bin/env python3
"""
AI OS Corp â€” Screenshot & Send to Telegram
Usage: python screenshot.py <chat_id>
"""
import sys
import os
import mss
from PIL import Image
import requests
from datetime import datetime

TOKEN = "[REDACTED]"
CHAT_ID = sys.argv[1] if len(sys.argv) > 1 else "646106732"
OUT = os.path.join(os.environ.get("TEMP", "/tmp"), "aios_snap.png")

# Capture screen
with mss.mss() as sct:
    monitor = sct.monitors[1]  # Primary monitor
    raw = sct.grab(monitor)
    img = Image.frombytes("RGB", raw.size, raw.bgra, "raw", "BGRX")
    # Scale down for Telegram (max 1280px wide)
    w, h = img.size
    if w > 1280:
        scale = 1280 / w
        img = img.resize((1280, int(h * scale)), Image.LANCZOS)
    img.save(OUT, "PNG", optimize=True)

# Send to Telegram
ts = datetime.now().strftime("%H:%M:%S")
with open(OUT, "rb") as f:
    resp = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
        data={"chat_id": CHAT_ID, "caption": f"ðŸ“¸ Screenshot lÃºc {ts}"},
        files={"photo": f},
        timeout=30
    )

if resp.ok:
    print(f"Screenshot sent to chat {CHAT_ID}")
else:
    print(f"ERROR: {resp.text}")

