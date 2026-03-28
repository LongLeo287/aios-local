#!/usr/bin/env python3
"""
ops/scripts/repo_resolver.py — Auto-detect which large repos a project needs
Given: project description (text) or task brief
Output: clone commands + which repos to fetch

Usage:
  python ops/scripts/repo_resolver.py "Build analytics dashboard with charts"
  python ops/scripts/repo_resolver.py --dept engineering
  python ops/scripts/repo_resolver.py --file brain/shared-context/corp/proposals/PROP_xyz.md

Integration:
  - aos.py project init <name> → calls repo_resolver
  - brief_writer.py → calls repo_resolver per dept
  - Telegram: /project <description> → resolve + show clone commands
"""
import sys
import re
import json
import argparse
from pathlib import Path
from datetime import datetime

ROOT    = Path(__file__).parent.parent.parent
CATALOG = ROOT / "brain" / "knowledge" / "notes" / "LARGE_REPOS_CATALOG.md"
TARGET  = ROOT / "plugins" / "github-repos"

# ─── Repo Definitions ────────────────────────────────────────────────────────
LARGE_REPOS = [
    {
        "name": "next.js",
        "url": "https://github.com/vercel/next.js.git",
        "tags": ["FRONTEND", "WEB", "REACT", "SSR", "DASHBOARD", "UI", "APP"],
        "keywords": ["web app", "frontend", "dashboard", "ui", "next", "react", "ssr", "portal", "website", "landing"],
        "dept": ["engineering", "product", "design"],
        "desc": "React framework — dùng khi build web UI/dashboard",
        "size": "~1.2GB",
    },
    {
        "name": "excalidraw",
        "url": "https://github.com/excalidraw/excalidraw.git",
        "tags": ["UI-TOOL", "DIAGRAM", "WHITEBOARD", "DESIGN"],
        "keywords": ["diagram", "whiteboard", "architecture", "draw", "sketch", "wireframe", "board"],
        "dept": ["design", "rd", "product"],
        "desc": "Whiteboard/diagram tool — dùng khi cần vẽ system architecture",
        "size": "~500MB",
    },
    {
        "name": "posthog",
        "url": "https://github.com/posthog/posthog.git",
        "tags": ["ANALYTICS", "TRACKING", "METRICS", "FUNNEL"],
        "keywords": ["analytics", "tracking", "metrics", "funnel", "events", "user behavior", "retention"],
        "dept": ["analytics", "ops", "product"],
        "desc": "Self-hosted analytics pipeline",
        "size": "~800MB",
    },
    {
        "name": "plotly.js",
        "url": "https://github.com/plotly/plotly.js.git",
        "tags": ["VISUALIZATION", "CHARTS", "GRAPHS", "DATA"],
        "keywords": ["chart", "graph", "visualization", "plot", "data viz", "hud", "kpi", "dashboard charts"],
        "dept": ["data", "analytics", "engineering"],
        "desc": "JavaScript charting library — charts cho HUD/dashboard",
        "size": "~400MB",
    },
    {
        "name": "trivy",
        "url": "https://github.com/aquasecurity/trivy.git",
        "tags": ["SECURITY", "SCAN", "VULNERABILITY", "CONTAINER"],
        "keywords": ["security", "scan", "vulnerability", "cve", "audit", "secret", "container", "docker", "civ"],
        "dept": ["security", "devops", "civ"],
        "desc": "Security scanner — CIV pipeline deep scan",
        "size": "~600MB",
    },
    {
        "name": "developer-roadmap",
        "url": "https://github.com/kamranahmedse/developer-roadmap.git",
        "tags": ["KNOWLEDGE", "TRAINING", "ROADMAP", "SKILL"],
        "keywords": ["training", "roadmap", "skill", "onboard", "learning", "curriculum", "developer", "agent training"],
        "dept": ["training", "hr", "rd"],
        "desc": "Developer roadmaps — onboard, skill gap, training plan",
        "size": "~300MB",
    },
    {
        "name": "openai-cookbook",
        "url": "https://github.com/openai/openai-cookbook.git",
        "tags": ["AI-PATTERNS", "LLM", "RAG", "PROMPTING", "FINE-TUNE"],
        "keywords": ["llm", "ai", "rag", "prompt", "fine-tune", "embedding", "openai", "pattern", "research"],
        "dept": ["rd", "engineering", "ai-research"],
        "desc": "LLM patterns, RAG, prompting examples",
        "size": "~500MB",
    },
    {
        "name": "anime",
        "url": "https://github.com/juliangarnier/anime.git",
        "tags": ["ANIMATION", "UI", "FRONTEND"],
        "keywords": ["animation", "transition", "motion", "animated", "animate", "effect"],
        "dept": ["design", "frontend", "product"],
        "desc": "JS animation library — HUD animations, UI effects",
        "size": "~200MB",
    },
    {
        "name": "agents-course",
        "url": "https://github.com/huggingface/agents-course.git",
        "tags": ["AI-EDUCATION", "TRAINING", "AGENT", "LLM"],
        "keywords": ["agent training", "huggingface", "course", "curriculum", "ai education", "autonomous agent"],
        "dept": ["training", "rd"],
        "desc": "HuggingFace agents curriculum — train new agents",
        "size": "~2GB ⚠️",
    },
    {
        "name": "public-apis",
        "url": "https://github.com/public-apis/public-apis.git",
        "tags": ["INTEGRATION", "API", "EXTERNAL"],
        "keywords": ["api", "integration", "external", "third-party", "webhook", "connect", "service"],
        "dept": ["rd", "integration", "engineering"],
        "desc": "Directory of free public APIs — find integration targets",
        "size": "~100MB",
    },
    {
        "name": "gitignore",
        "url": "https://github.com/github/gitignore.git",
        "tags": ["TEMPLATE", "DEVOPS", "REPO-SETUP"],
        "keywords": ["gitignore", "template", "repo setup", "new project", "init"],
        "dept": ["devops", "engineering"],
        "desc": "GitHub gitignore templates — any new repo",
        "size": "~50MB",
    },
]

# ─── Dept → default repos ─────────────────────────────────────────────────────
DEPT_DEFAULTS = {
    "engineering":    ["next.js", "plotly.js", "openai-cookbook"],
    "design":         ["excalidraw", "anime", "next.js"],
    "rd":             ["openai-cookbook", "agents-course", "public-apis"],
    "security":       ["trivy"],
    "analytics":      ["posthog", "plotly.js"],
    "data":           ["plotly.js", "public-apis"],
    "training":       ["agents-course", "developer-roadmap"],
    "devops":         ["trivy", "gitignore"],
    "product":        ["next.js", "excalidraw", "posthog"],
    "integration":    ["public-apis"],
    "civ":            ["trivy"],
    "content_intake": ["trivy", "public-apis"],
}

def resolve_by_text(text: str) -> list:
    """Match text to relevant repos by keywords."""
    text_lower = text.lower()
    matches = []
    for repo in LARGE_REPOS:
        score = sum(1 for kw in repo["keywords"] if kw in text_lower)
        if score > 0:
            matches.append((score, repo))
    matches.sort(key=lambda x: -x[0])
    return [r for _, r in matches]

def resolve_by_dept(dept: str) -> list:
    """Match dept to default repos."""
    dept_lower = dept.lower().replace("-", "_").replace(" ", "_")
    defaults = DEPT_DEFAULTS.get(dept_lower, [])
    return [r for r in LARGE_REPOS if r["name"] in defaults]

def already_cloned(repo_name: str) -> bool:
    target = TARGET / repo_name
    return (target / ".git").exists()

def print_clone_cmd(repo: dict, checked: bool = True):
    status = "✅ CLONED" if already_cloned(repo["name"]) else f"📥 CLONE ({repo['size']})"
    print(f"\n  {status}: {repo['name']} — {repo['desc']}")
    if not already_cloned(repo["name"]):
        dest = TARGET / repo["name"]
        print(f"  └─ git clone --depth 1 {repo['url']} \"{dest}\"")

def main():
    parser = argparse.ArgumentParser(description="Resolve which large repos a project needs")
    parser.add_argument("text", nargs="*", help="Project description")
    parser.add_argument("--dept", help="Department name")
    parser.add_argument("--file", help="Read project description from file")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--clone", action="store_true", help="Auto-clone resolved repos")
    args = parser.parse_args()

    text = " ".join(args.text) if args.text else ""
    if args.file:
        fp = Path(args.file)
        try:
            try:
                text += " " + fp.read_text(encoding="utf-8", errors="ignore")[:2000]
            except Exception:
                pass
        except (FileNotFoundError, OSError) as e:
            print(f"[WARN] Khong doc duoc file '{args.file}': {e}")

    matches = []
    if args.dept:
        matches = resolve_by_dept(args.dept)
        print(f"🏢 Dept [{args.dept}] → {len(matches)} repos recommended")
    elif text:
        matches = resolve_by_text(text)
        print(f"🔍 Query: \"{text[:80]}\"")
        print(f"📦 {len(matches)} repos matched")
    else:
        matches = LARGE_REPOS
        print(f"📋 All large repos ({len(matches)}):")

    if not matches:
        print("  No matching repos found.")
        return

    if args.json:
        out = [{"name": r["name"], "url": r["url"], "cloned": already_cloned(r["name"]),
                "tags": r["tags"], "desc": r["desc"]} for r in matches]
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    print("─" * 60)
    clone_needed = []
    for repo in matches:
        print_clone_cmd(repo)
        if not already_cloned(repo["name"]):
            clone_needed.append(repo)

    if args.clone and clone_needed:
        import subprocess
        print(f"\n🚀 Auto-cloning {len(clone_needed)} repos...")
        for repo in clone_needed:
            dest = TARGET / repo["name"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            r = subprocess.run(
                ["git", "clone", "--depth", "1", "--quiet", repo["url"], str(dest)],
                capture_output=True, text=True, timeout=120
            )
            if r.returncode == 0:
                print(f"  ✅ {repo['name']}")
            else:
                print(f"  ❌ {repo['name']}: {r.stderr.strip()[:80]}")

    if clone_needed:
        print(f"\n💡 Run with --clone to auto-download {len(clone_needed)} repo(s)")

if __name__ == "__main__":
    main()
