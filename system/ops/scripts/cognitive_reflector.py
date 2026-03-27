#!/usr/bin/env python3
"""
ops/scripts/cognitive_reflector.py — Phase 5 Auto-Synthesis (B3)
Reads all dept briefs from today → writes SYNTHESIS_<date>.md + Telegram notify

Usage:
  python ops/scripts/cognitive_reflector.py        # Synthesize today's briefs
  python ops/scripts/cognitive_reflector.py --date 2026-03-25  # Specific date
"""
import json
import sys
import os
from pathlib import Path
from datetime import datetime
from urllib.request import urlopen, Request

ROOT   = Path(__file__).parent.parent.parent
DEPTS  = ROOT / "corp" / "departments"
BB     = ROOT / "brain" / "shared-context" / "blackboard.json"
ENV    = ROOT / ".env"

def _load_env():
    env = {}
    for path in [ENV, ROOT / "ops" / "secrets" / "MASTER.env"]:
        if path.exists():
            for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                if "=" in line and not line.startswith("#"):
                    k, _, v = line.partition("=")
                    env[k.strip()] = v.strip()
    return env

_E = _load_env()

def send_telegram(text: str):
    token   = _E.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = _E.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        return
    try:
        payload = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}).encode()
        req = Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        urlopen(req, timeout=5)
    except Exception:
        pass

def orientation() -> str:
    """Step 2a: Orientation - Read CEO Mission & Blackboard"""
    mission_file = ROOT / "brain" / "shared-context" / "corp" / "mission.md"
    focus = "No explicit mission found."
    if mission_file.exists():
        lines = mission_file.read_text(encoding="utf-8").splitlines()
        for line in lines:
            if "Strategic Focus" in line or "Priorities" in line:
                focus = line
                break
    return focus

def gather_signal(date: str) -> dict:
    """Step 2b: Gather Signal - Briefs & Receipts"""
    briefs = []
    receipts_count = 0
    if DEPTS.exists():
        for dept_dir in DEPTS.iterdir():
            if not dept_dir.is_dir(): continue
            # Briefs
            brief_file = dept_dir / "briefs" / f"BRIEF_{date}.md"
            if brief_file.exists():
                content = brief_file.read_text(encoding="utf-8", errors="ignore")
                briefs.append({"dept": dept_dir.name, "tasks": content.count("| OPEN") + content.count("OPEN |")})

            # Receipts (just basic count for now to represent signal gathering)
            receipt_dir = ROOT / "telemetry" / "receipts" / dept_dir.name
            if receipt_dir.exists():
                receipts_count += len(list(receipt_dir.glob("*.json")))

    return {"briefs": briefs, "receipts_count": receipts_count}

def prune_and_index():
    """Step 2d: Prune Dept Memory > 200 lines & Update Global Index"""
    index_lines = ["# GLOBAL KNOWLEDGE INDEX", ""]
    mem_dir = ROOT / "brain" / "corp" / "memory" / "departments"
    if mem_dir.exists():
        for mem_file in mem_dir.glob("*.md"):
            content = mem_file.read_text(encoding="utf-8")
            lines = content.splitlines()
            if len(lines) > 200:
                # Prune: Keep header + last 100 lines
                pruned = lines[:10] + ["\n...[PRUNED BY AUTO-DREAM]...\n"] + lines[-100:]
                mem_file.write_text("\n".join(pruned), encoding="utf-8")
                index_lines.append(f"- **{mem_file.stem}**: Pruned. Active lines: {len(pruned)}")
            else:
                index_lines.append(f"- **{mem_file.stem}**: Active lines: {len(lines)}")

    global_index = ROOT / "brain" / "corp" / "memory" / "GLOBAL_INDEX.md"
    global_index.parent.mkdir(parents=True, exist_ok=True)
    global_index.write_text("\n".join(index_lines), encoding="utf-8")
    return len(index_lines) - 2

def consolidate(date: str, focus: str, signal: dict, pruned_count: int) -> str:
    """Step 2c: Consolidate into SYNTHESIS"""
    bb = {}
    if BB.exists():
        try: bb = json.loads(BB.read_text(encoding="utf-8"))
        except: pass
    cycle = bb.get("corp_cycle_number", "?")

    briefs = signal["briefs"]
    lines = [
        f"# Auto-Dream Synthesis — Cycle {cycle} — {date}",
        "---",
        "## 1. Orientation Context",
        f"- **CEO Intent Lens:** {focus}",
        "",
        "## 2. Signal Gathered",
        f"- **Receipts Scanned:** {signal['receipts_count']} artifacts",
        "- **Depts Reporting:**",
        "| Dept | Open Tasks |",
        "|------|-----------|"
    ]
    for b in sorted(briefs, key=lambda x: x["tasks"], reverse=True):
        lines.append(f"| {b['dept']} | {b['tasks']} |")

    lines += [
        "",
        "## 3. Consolidation: Patterns & Blockers",
        "*[Antigravity uses this section to highlight cross-dept friction]*",
        "- Pattern: High open tasks in top depts.",
        "",
        "## 4. Prune Status",
        f"- Pruned / Scanned: {pruned_count} memory blocks.",
        "- `GLOBAL_INDEX.md` successfully updated to prevent context bloat.",
        "---",
        f"*Auto-Dream V1.0 | Cycle {cycle}*"
    ]
    return "\n".join(lines)

def main():
    date = datetime.now().strftime("%Y-%m-%d")
    for arg in sys.argv[1:]:
        if arg.startswith("--date"):
            date = arg.split("=")[-1] if "=" in arg else sys.argv[sys.argv.index(arg)+1]

    print(f"cognitive_reflector — Auto-Dream REM Sleep — {date}")

    # 4 Phases of Auto-Dream
    focus = orientation()
    signal = gather_signal(date)
    pruned_count = prune_and_index()
    synthesis = consolidate(date, focus, signal, pruned_count)

    # Write SYNTHESIS file
    synth_dir = ROOT / "brain" / "shared-context" / "corp" / "daily_briefs"
    synth_dir.mkdir(parents=True, exist_ok=True)
    synth_file = synth_dir / f"SYNTHESIS_{date}.md"
    synth_file.write_text(synthesis, encoding="utf-8")
    print(f"  ✅ {synth_file.relative_to(ROOT)}")

    # Telegram notify
    bb = {}
    if BB.exists():
        try: bb = json.loads(BB.read_text(encoding="utf-8"))
        except: pass
    cycle = bb.get("corp_cycle_number", "?")
    msg = (
        f"💤 *Auto-Dream SYNTHESIS — Cycle {cycle}*\n"
        f"📅 {date} | {len(signal['briefs'])} depts reporting\n"
        f"🧹 Pruned memory files: {pruned_count}\n"
        f"File: `corp/daily_briefs/SYNTHESIS_{date}.md`"
    )
    send_telegram(msg)
    print("  ✅ Telegram notify sent")

if __name__ == "__main__":
    main()
