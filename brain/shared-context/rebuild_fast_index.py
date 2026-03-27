#!/usr/bin/env python3
"""
rebuild_fast_index.py — Full FAST_INDEX rebuild from scratch
Smart crawler: targets known dirs, limits depth, skips node_modules/.git/.
Run:
  python brain/shared-context/rebuild_fast_index.py
  python brain/shared-context/rebuild_fast_index.py --dry-run
"""
import json
import os
import re
import sys
import shutil
from datetime import datetime

AIOS_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUTPUT    = os.path.join(AIOS_ROOT, "brain", "shared-context", "FAST_INDEX.json")
DRY_RUN   = "--dry-run" in sys.argv

# Top-level dirs to crawl (depth-limited per dir)
SCAN_DIRS = [
    ("plugins",          3),   # plugins/<name>/SKILL.md
    ("tools",            3),   # tools/<name>/SKILL.md
    ("brain/skills",     4),   # brain/skills/<name>/SKILL.md
    ("workforce/agents", 3),   # workforce/agents/<name>/SKILL.md
    ("workforce/subagents", 3),
    ("corp/departments", 3),
    ("infra",            3),
    ("security",         3),
    ("ops",              3),
]

EXCLUDE_DIRS = {
    ".git", ".github", "__pycache__", "node_modules", "dist", "build",
    ".venv", "venv", ".pixi", ".cargo", ".cache", ".nyc_output",
    "QUARANTINE", ".claude", ".gemini", ".codex", ".nullclaw", ".9router",
    "coverage", ".pytest_cache", "target", "vendor",
}

def parse_frontmatter(text: str) -> dict:
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, _, v = line.partition(':')
            k = k.strip()
            v = v.strip()
            if v.startswith('[') and v.endswith(']'):
                v = [x.strip().strip("'\"") for x in v[1:-1].split(',') if x.strip()]
            fm[k] = v
    return fm

def crawl_dir(base_dir: str, max_depth: int) -> list[dict]:
    """Walk base_dir up to max_depth, finding SKILL.md files."""
    results = []
    if not os.path.isdir(base_dir):
        return results

    def _walk(dirpath: str, depth: int):
        if depth > max_depth:
            return
        try:
            entries = sorted(os.listdir(dirpath))
        except PermissionError:
            return

        if "SKILL.md" in entries:
            fpath = os.path.join(dirpath, "SKILL.md")
            rel   = os.path.relpath(fpath, AIOS_ROOT).replace("\\", "/")
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                fm = parse_frontmatter(content)
                if not fm.get("description"):
                    m2 = re.search(r'^#+\s+.+\n+(.+)', content, re.MULTILINE)
                    if m2:
                        fm["description"] = m2.group(1).strip()[:120]
                results.append({"path": rel, "fm": fm})
            except Exception as e:
                results.append({"path": rel, "fm": {}, "error": str(e)})

        for entry in entries:
            if entry in EXCLUDE_DIRS or entry.startswith('.'):
                continue
            full = os.path.join(dirpath, entry)
            if os.path.isdir(full):
                _walk(full, depth + 1)

    _walk(base_dir, 0)
    return results


def build_index(skills: list[dict]) -> dict:
    fi = {
        "_meta": {
            "version": "2.0",
            "built": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "total_paths": len(skills),
            "builder": "rebuild_fast_index.py",
            "note": "Auto-rebuilt from SKILL.md frontmatter — do not edit manually",
        },
        "tier1_boot": {},
        "domain": {},
        "keyword": {},
        "agent": {},
        "paths": {},
    }

    seen_kw = set()

    for s in skills:
        path = s["path"]
        fm   = s["fm"]
        name = str(fm.get("name", ""))
        dept_raw = fm.get("department", fm.get("dept", ""))
        dept = dept_raw[0] if isinstance(dept_raw, list) else str(dept_raw)
        dept = dept.strip().split(",")[0].strip()
        tier_raw = fm.get("tier", 5)
        try:
            tier = int(tier_raw)
        except Exception:
            tier = 5
        category = str(fm.get("category", "general")).strip()
        desc     = str(fm.get("description", ""))[:120]
        tags     = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]

        # Slug
        parts = path.replace("\\", "/").split("/")
        slug = parts[-2] if len(parts) >= 2 else "unknown"
        slug = re.sub(r'[^a-z0-9_]', '_', slug.lower()).strip('_')

        # paths
        fi["paths"][slug] = path

        # tier1_boot
        if tier == 1:
            fi["tier1_boot"][slug] = {"path": path, "name": name, "dept": dept, "desc": desc}

        # domain
        if category:
            if category not in fi["domain"] or tier < fi["domain"][category].get("tier", 99):
                fi["domain"][category] = {"path": path, "tier": tier, "dept": dept}

        # keywords from tags + name tokens
        kw_tokens = list(tags)
        kw_tokens += [t.lower() for t in re.split(r'[\s\-_/]', name) if len(t) > 2]
        for kw in kw_tokens:
            kw = re.sub(r'[^a-z0-9_]', '_', kw.lower()).strip('_')
            if kw and len(kw) > 2 and kw not in fi["keyword"]:
                fi["keyword"][kw] = {"path": path, "tier": tier, "dept": dept, "desc": desc}

        # agent
        if any(x in path for x in ["workforce/", "subagents/"]):
            agent_id = parts[-2] if len(parts) >= 2 else slug
            fi["agent"][agent_id] = {"path": path, "dept": dept, "name": name}

    return fi


def main():
    print(f"AIOS root: {AIOS_ROOT}")
    all_skills = []

    for rel_dir, max_depth in SCAN_DIRS:
        base = os.path.join(AIOS_ROOT, rel_dir.replace("/", os.sep))
        found = crawl_dir(base, max_depth)
        print(f"  {rel_dir:30s} → {len(found)} SKILL.md")
        all_skills.extend(found)

    # Deduplicate by path
    seen = set()
    unique = []
    for s in all_skills:
        if s["path"] not in seen:
            seen.add(s["path"])
            unique.append(s)

    print(f"\nTotal unique SKILL.md: {len(unique)}")

    tiers = {}
    for s in unique:
        t = str(s["fm"].get("tier", "?"))
        tiers[t] = tiers.get(t, 0) + 1
    print(f"Tier dist: {dict(sorted(tiers.items()))}")

    fi = build_index(unique)
    fi["_meta"]["total_paths"] = len(unique)

    print(f"\nFAST_INDEX built:")
    print(f"  paths    : {len(fi['paths'])}")
    print(f"  tier1    : {len(fi['tier1_boot'])}")
    print(f"  domains  : {len(fi['domain'])}")
    print(f"  keywords : {len(fi['keyword'])}")
    print(f"  agents   : {len(fi['agent'])}")

    if DRY_RUN:
        print("\n[dry-run] Not writing. Remove --dry-run to save.")
        return fi

    # Backup
    if os.path.exists(OUTPUT):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        bk = OUTPUT.replace(".json", f"_bk_{ts}.json")
        shutil.copy2(OUTPUT, bk)
        print(f"Backup: {os.path.basename(bk)}")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(fi, f, ensure_ascii=False, separators=(",", ":"))

    kb = os.path.getsize(OUTPUT) / 1024
    print(f"\n✅ FAST_INDEX v2.0 written ({kb:.1f} KB)")
    print(f"   {OUTPUT}")


if __name__ == "__main__":
    main()
