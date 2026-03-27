#!/usr/bin/env python3
"""
ops/scripts/civ_stats.py — B7: CIV Receipt Dashboard Generator
Scans telemetry/receipts/ → generates brain/knowledge/CIV_STATS.md

Usage:
  python ops/scripts/civ_stats.py
"""
import os
import re
from pathlib import Path
from datetime import datetime
from collections import Counter

ROOT        = Path(__file__).parent.parent.parent
RECEIPTS    = ROOT / "telemetry" / "receipts"
NOTES       = ROOT / "brain" / "knowledge" / "notes"
CIV_OUT     = ROOT / "brain" / "knowledge" / "CIV_STATS.md"

def scan_receipts() -> list:
    items = []
    if not RECEIPTS.exists():
        return items
    for f in RECEIPTS.rglob("*.md"):
        if "archive" in str(f):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            items.append({
                "file": f.name,
                "date": re.search(r"\d{4}-\d{2}-\d{2}", f.name),
                "size": len(content),
                "type": _detect_type(content, f.name),
            })
        except Exception:
            pass
    return items

def _detect_type(content: str, filename: str) -> str:
    fn = filename.lower() + content[:200].lower()
    if "github" in fn or "repo" in fn or "clone" in fn:
        return "REPO"
    if "url" in fn or "crawl" in fn or "web" in fn:
        return "WEB"
    if "skill" in fn:
        return "SKILL"
    if "vscode" in fn or "extension" in fn:
        return "TOOL"
    if "ki" in fn or "knowledge" in fn:
        return "KI"
    return "OTHER"

def count_ki_notes() -> int:
    if not NOTES.exists():
        return 0
    return len(list(NOTES.glob("*.md")))

def main():
    receipts = scan_receipts()
    ki_count = count_ki_notes()

    type_counts = Counter(r["type"] for r in receipts)
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    lines = [
        "# 📊 CIV Stats Dashboard",
        f"*Generated: {now} | Source: telemetry/receipts/*",
        "",
        "---",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total receipts | {len(receipts)} |",
        f"| KI notes in brain | {ki_count} |",
        f"| REPO intakes | {type_counts.get('REPO', 0)} |",
        f"| WEB intakes | {type_counts.get('WEB', 0)} |",
        f"| SKILL intakes | {type_counts.get('SKILL', 0)} |",
        f"| TOOL intakes | {type_counts.get('TOOL', 0)} |",
        f"| Other | {type_counts.get('OTHER', 0)} |",
        "",
        "## Type Distribution",
        "",
        "| Type | Count |",
        "|------|-------|",
    ]
    for t, n in sorted(type_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {t} | {n} |")

    lines += [
        "",
        "## Recent Receipts (last 10)",
        "",
        "| File | Type | Size |",
        "|------|------|------|",
    ]
    for r in sorted(receipts, key=lambda x: x["file"], reverse=True)[:10]:
        lines.append(f"| {r['file']} | {r['type']} | {r['size']} bytes |")

    lines += [
        "",
        "---",
        f"*Run: `python ops/scripts/civ_stats.py` to refresh*"
    ]

    CIV_OUT.parent.mkdir(parents=True, exist_ok=True)
    CIV_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ CIV_STATS.md — {len(receipts)} receipts, {ki_count} KI notes")

if __name__ == "__main__":
    main()
