#!/usr/bin/env python3
"""
ops/scripts/dept_health.py — B4: Dept Health Dashboard Generator
Reads per-dept briefs + task_backlog → generates hud/DEPT_HEALTH.md + updates KPI

Usage:
  python ops/scripts/dept_health.py        # Generate health dashboard
  python ops/scripts/dept_health.py --hud  # Also update HUD.md
"""
import json
import sys
from pathlib import Path
from datetime import datetime, date

ROOT    = Path(__file__).parent.parent.parent
DEPTS   = ROOT / "corp" / "departments"
BACKLOG = ROOT / "brain" / "shared-context" / "corp" / "task_backlog.json"
SLA_CFG = ROOT / "brain" / "shared-context" / "corp" / "dept_sla_config.json"
HUD_DIR = ROOT / "hud"
BB      = ROOT / "brain" / "shared-context" / "blackboard.json"

today = date.today().isoformat()

def get_dept_health(dept_name: str, sla: dict) -> dict:
    dept_dir  = DEPTS / dept_name
    brief_today = dept_dir / "briefs" / f"BRIEF_{today}.md"
    last_brief  = None

    if dept_dir.exists():
        briefs = sorted((dept_dir / "briefs").glob("BRIEF_*.md")) if (dept_dir / "briefs").exists() else []
        if briefs:
            last_brief = briefs[-1].stem.replace("BRIEF_", "")

    # Load backlog tasks
    backlog = {}
    try:
        backlog = json.loads(BACKLOG.read_text(encoding="utf-8"))
    except Exception:
        pass
    tasks = backlog.get(dept_name, [])
    open_tasks = [t for t in tasks if isinstance(t, dict) and t.get("status") != "DONE"]
    done_tasks = [t for t in tasks if isinstance(t, dict) and t.get("status") == "DONE"]

    dept_sla = sla.get(dept_name, sla.get("defaults", {}))
    brief_freq = dept_sla.get("brief_freq", 1)
    priority   = dept_sla.get("priority", "MED")

    # Health score
    score = 100
    has_brief_today = brief_today.exists()
    if not has_brief_today:
        score -= 30
    if len(open_tasks) > 5:
        score -= 10
    if not last_brief:
        score -= 20

    status = "🟢" if score >= 80 else "🟡" if score >= 50 else "🔴"
    return {
        "dept": dept_name,
        "status": status,
        "score": score,
        "brief_today": "✅" if has_brief_today else "❌",
        "last_brief": last_brief or "never",
        "open_tasks": len(open_tasks),
        "done_tasks": len(done_tasks),
        "priority": priority,
    }

def main():
    sla = {}
    try:
        sla = json.loads(SLA_CFG.read_text(encoding="utf-8"))
        sla_depts = sla.get("departments", {})
        sla_defaults = sla.get("defaults", {})
    except Exception:
        sla_depts = {}
        sla_defaults = {}

    all_sla = {**sla_depts}

    # Get all depts
    dept_names = sorted(d.name for d in DEPTS.iterdir() if d.is_dir()) if DEPTS.exists() else []
    if not dept_names:
        print("[WARN] No dept directories found")
        return

    results = []
    for dept in dept_names:
        health = get_dept_health(dept, all_sla)
        results.append(health)

    # Sort by score asc (worst first)
    results_sorted = sorted(results, key=lambda x: x["score"])

    # Generate DEPT_HEALTH.md
    bb = {}
    try:
        bb = json.loads(BB.read_text(encoding="utf-8"))
    except Exception:
        pass
    cycle = bb.get("corp_cycle_number", "?")

    on_track  = sum(1 for r in results if r["score"] >= 80)
    lagging   = sum(1 for r in results if r["score"] < 80)

    lines = [
        f"# 🏢 Dept Health Dashboard — Cycle {cycle} — {today}",
        f"*{on_track}/21 on-track | {lagging} lagging | Generated: {datetime.now().strftime('%H:%M:%S')}*",
        "",
        f"| Dept | Status | Score | Brief Today | Last Brief | Open Tasks | Priority |",
        f"|------|--------|-------|-------------|------------|-----------|---------|",
    ]
    for r in results_sorted:
        lines.append(
            f"| {r['dept']} | {r['status']} | {r['score']} | {r['brief_today']} | {r['last_brief']} | {r['open_tasks']} | {r['priority']} |"
        )

    lag_depts = [r["dept"] for r in results if r["score"] < 80]
    if lag_depts:
        lines += ["", f"## ⚠️ Lagging Depts ({len(lag_depts)})", ""]
        for d in lag_depts:
            lines.append(f"- `{d}` — submit brief or check task_backlog.json")

    lines += [
        "", "---",
        f"*Run: `python ops/scripts/dept_health.py` | Update: post-session auto-trigger*"
    ]

    out = HUD_DIR / "DEPT_HEALTH.md"
    HUD_DIR.mkdir(exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ DEPT_HEALTH.md — {on_track}/21 on-track, {lagging} lagging")

    # Update blackboard
    try:
        bb["dept_health_updated"] = today
        bb["depts_on_track"] = on_track
        BB.write_text(json.dumps(bb, indent=4, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass

if __name__ == "__main__":
    main()
