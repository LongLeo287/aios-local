#!/usr/bin/env python3
"""
fix_skill_tiers.py — Batch-add 'tier' to all SKILL.md missing it.
Auto-assigns tier based on category + department heuristics.

Usage:
  python brain/shared-context/fix_skill_tiers.py           # dry-run
  python brain/shared-context/fix_skill_tiers.py --write   # apply patches
"""
import os
import re
import sys

AIOS_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
WRITE     = "--write" in sys.argv

# ── Tier assignment rules ──────────────────────────────────────────────
# Lower number = higher priority match

TIER_BY_CATEGORY = {
    # Tier 1 — Core system
    "mcp": 1, "specification": 1, "protocol": 1, "boot": 1,
    # Tier 2 — Active production tools
    "dev-tooling": 2, "ai-agent": 2, "analytics": 2, "monitoring": 2,
    "knowledge": 2, "database": 2, "security": 2, "design": 2,
    "ui-animation": 2, "workflow": 2, "notification": 2,
    # Tier 3 — Experimental / specialized
    "experimental": 3, "research": 3, "benchmark": 3,
    # Tier 4 — Domain reference only
    "reference": 4, "documentation": 4,
    # Tier 5 — Archived / deprecated
    "archive": 5, "deprecated": 5,
}

TIER_BY_DEPT = {
    # Tier 1 departments
    "registry_capability": 1, "monitoring_inspection": 1,
    # Tier 2
    "engineering": 2, "rd": 2, "security_grc": 2, "it_infra": 2,
    "operations": 2, "finance": 2, "monitoring": 2,
    # Tier 3
    "experimental": 3,
    # Tier 5
    "legacy": 5,
}

TIER_BY_STATUS = {
    "deprecated": 5,
    "archived": 5,
    "draft": 3,
    "experimental": 3,
}

TIER_BY_PATH = [
    # (path substring, tier)
    ("_archive",        5),
    ("legacy",          5),
    ("experimental",    3),
    ("workforce/agents", 2),
    ("workforce/subagents", 2),
    ("brain/skills",    2),
    ("tools/",          2),
    ("plugins/",        2),
]


def infer_tier(path: str, fm: dict) -> int:
    """Infer best tier for a SKILL.md based on frontmatter + path."""
    status = str(fm.get("status", "")).lower()
    if status in TIER_BY_STATUS:
        return TIER_BY_STATUS[status]

    category = str(fm.get("category", "")).lower().strip()
    if category in TIER_BY_CATEGORY:
        return TIER_BY_CATEGORY[category]

    dept_raw = fm.get("department", fm.get("dept", ""))
    depts = [d.strip().lower() for d in (dept_raw if isinstance(dept_raw, list) else str(dept_raw).split(","))]
    for d in depts:
        if d in TIER_BY_DEPT:
            return TIER_BY_DEPT[d]

    path_lower = path.lower().replace("\\", "/")
    for substr, t in TIER_BY_PATH:
        if substr in path_lower:
            return t

    return 2   # default: active production tier


def parse_frontmatter(text: str):
    """Return (fm_dict, has_tier)."""
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return {}, False
    fm = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, _, v = line.partition(':')
            fm[k.strip()] = v.strip()
    has_tier = "tier" in fm
    return fm, has_tier


def inject_tier(text: str, tier: int) -> str:
    """Insert 'tier: N' line after 'name:' in frontmatter."""
    # Try to insert after name: line
    def insert_after_name(m):
        block = m.group(1)
        lines = block.splitlines()
        out = []
        inserted = False
        for line in lines:
            out.append(line)
            if not inserted and line.startswith("name:"):
                out.append(f"tier: {tier}")
                inserted = True
        if not inserted:
            out.insert(0, f"tier: {tier}")
        return "---\n" + "\n".join(out) + "\n---"

    new_text = re.sub(r'^---\s*\n(.*?)\n---', insert_after_name, text, count=1, flags=re.DOTALL)
    return new_text


SCAN_DIRS = [
    ("plugins", 3),
    ("tools", 3),
    ("brain/skills", 4),
    ("workforce/agents", 3),
    ("workforce/subagents", 3),
]
EXCLUDE = {
    ".git", "__pycache__", "node_modules", "dist", "build",
    ".venv", "venv", "QUARANTINE", ".claude", ".gemini",
    ".codex", ".nullclaw", "coverage", "target", "vendor",
}


def main():
    fixed = 0
    skipped = 0
    errors = []

    for rel, max_depth in SCAN_DIRS:
        base = os.path.join(AIOS_ROOT, rel.replace("/", os.sep))
        if not os.path.isdir(base):
            continue

        def walk(dirpath, depth):
            nonlocal fixed, skipped
            if depth > max_depth:
                return
            try:
                entries = os.listdir(dirpath)
            except PermissionError:
                return

            if "SKILL.md" in entries:
                fpath = os.path.join(dirpath, "SKILL.md")
                relpath = os.path.relpath(fpath, AIOS_ROOT).replace("\\", "/")
                try:
                    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                    fm, has_tier = parse_frontmatter(content)
                    if not has_tier:
                        tier = infer_tier(relpath, fm)
                        if WRITE:
                            new_content = inject_tier(content, tier)
                            with open(fpath, "w", encoding="utf-8") as f:
                                f.write(new_content)
                            fixed += 1
                            if fixed <= 10 or fixed % 50 == 0:
                                print(f"  [{fixed:4d}] tier={tier}  {relpath}")
                        else:
                            fixed += 1
                            if fixed <= 5 or fixed % 100 == 0:
                                print(f"  [DRY {fixed:4d}] would set tier={tier}  {relpath}")
                    else:
                        skipped += 1
                except Exception as e:
                    errors.append((relpath, str(e)))

            for entry in entries:
                if entry in EXCLUDE or entry.startswith('.'):
                    continue
                full = os.path.join(dirpath, entry)
                if os.path.isdir(full):
                    walk(full, depth + 1)

        walk(base, 0)

    mode = "WRITTEN" if WRITE else "DRY-RUN (--write to apply)"
    print(f"\n{'='*50}")
    print(f"Mode: {mode}")
    print(f"Patched : {fixed}")
    print(f"Skipped (already had tier): {skipped}")
    print(f"Errors  : {len(errors)}")
    if errors:
        for p, e in errors[:5]:
            print(f"  ERR: {p} — {e}")
    if not WRITE and fixed > 0:
        print(f"\nRun with --write to apply {fixed} patches.")


if __name__ == "__main__":
    main()
