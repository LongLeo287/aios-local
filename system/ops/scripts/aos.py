#!/usr/bin/env python3
"""
aos.py — AI OS Corp Cycle CLI v2.0
Triggers corp-daily-cycle.md phases from terminal.

Usage:
  python ops/aos.py corp start           # Phase 0+1: Boot + CEO Brief
  python ops/aos.py corp dispatch <dept> # Phase 2-3: Dispatch tasks
  python ops/aos.py corp retro           # Phase 5-7: Synthesis + Retro + HUD
  python ops/aos.py status               # Show cycle status
  python ops/aos.py brief                # Show CEO daily brief (Phase 1)
  python ops/aos.py proposals            # List pending CEO proposals
  python ops/aos.py proposals approve <id>  # Approve a proposal
  python ops/aos.py dispatch <dept>      # Dispatch tasks to a department
  python ops/aos.py hud update
  python ops/aos.py intake <url>       # CIV pipeline: classify + ticket + receipt           # Run update_hud.ps1
  python ops/aos.py rebuild-index        # Rebuild FAST_INDEX from scratch

Shortcuts: aos = python ops/aos.py  (add alias to your shell profile)
"""
import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

ROOT     = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
BB_PATH  = os.path.join(ROOT, "brain", "shared-context", "blackboard.json")
KPI_PATH = os.path.join(ROOT, "brain", "shared-context", "corp", "kpi_scoreboard.json")
PROP_DIR = os.path.join(ROOT, "brain", "shared-context", "corp", "proposals")
BRIEF_DIR= os.path.join(ROOT, "brain", "shared-context", "corp", "daily_briefs")
HUD_PS1  = os.path.join(ROOT, "system", "ops", "scripts", "update_hud.ps1")

CYAN  = "\033[96m"
GREEN = "\033[92m"
YELLOW= "\033[93m"
RED   = "\033[91m"
BOLD  = "\033[1m"
RESET = "\033[0m"

def load_json(path, default=None):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return default or {}

def save_json(path, data):
    import time, os
    lock_path = str(path) + ".lock"
    for _ in range(50):
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            break
        except FileExistsError:
            time.sleep(0.05)
    try:
        tmp_path = str(path) + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        os.replace(tmp_path, path)
    finally:
        if os.path.exists(lock_path):
            try: os.remove(lock_path)
            except: pass

def _now():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

# ─── Corp Cycle ─────────────────────────────────────────────────────────────

def cmd_corp_start():
    """Phase 0+1: Boot + CEO Brief — sets cycle RUNNING."""
    bb = load_json(BB_PATH)
    status = bb.get("corp_cycle_status", "IDLE")
    cycle = bb.get("corp_cycle_number", 0)
    if status == "RUNNING":
        print(f"{YELLOW}Cycle {cycle} already RUNNING. Use 'aos status' to check.{RESET}")
        return
    cycle += 1
    bb["corp_cycle_number"] = cycle
    bb["corp_cycle_status"] = "RUNNING"
    bb["corp_cycle_date"] = datetime.now().strftime("%Y-%m-%d")
    save_json(BB_PATH, bb)
    print(f"{GREEN}\u2705 AOS CORP START — Cycle {cycle} RUNNING{RESET}")
    # Phase 0: core file check
    checks = [BB_PATH, KPI_PATH,
              os.path.join(ROOT,"GEMINI.md"),
              os.path.join(ROOT,"brain","shared-context","SKILL_REGISTRY.json"),
              os.path.join(ROOT,"hud","HUD.md")]
    ok = sum(1 for f in checks if os.path.exists(f))
    print(f"  Phase 0: Core files {ok}/{len(checks)} OK")
    cmd_brief()

def cmd_corp_dispatch(dept="all"):
    """Phase 2-3: Dispatch tasks to dept(s) via MQ."""
    mq_dir = os.path.join(ROOT, "subagents", "mq")
    os.makedirs(mq_dir, exist_ok=True)
    bb = load_json(BB_PATH)
    bb["last_dispatch"] = _now()
    bb["dispatch_signal"] = f"DISPATCH_{dept.upper()}"
    save_json(BB_PATH, bb)
    task_file = os.path.join(mq_dir, f"{dept}_tasks.md")
    entry = f"\n## Dispatch {_now()}\n- [ ] CEO dispatch — dept: {dept}\n"
    with open(task_file, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"{GREEN}✅ Dispatch — dept: {dept} — task written to subagents/mq/{dept}_tasks.md{RESET}")

def cmd_corp_retro():
    """Phase 5-7: Synthesis + Retro + HUD update."""
    bb = load_json(BB_PATH)
    cycle = bb.get("corp_cycle_number", "?")
    today = datetime.now().strftime("%Y-%m-%d")
    retro_dir = os.path.join(ROOT, "brain", "shared-context", "corp", "daily_briefs")
    os.makedirs(retro_dir, exist_ok=True)
    retro_file = os.path.join(retro_dir, f"RETRO_{today}.md")
    with open(retro_file, "w", encoding="utf-8") as f:
        f.write(f"# RETRO — Cycle {cycle} — {today}\n")
        f.write(f"Generated: {_now()}\n\n")
        f.write(f"## Actions\n{bb.get('last_actions_this_cycle', 'None recorded')}\n")
        f.write(f"## Open Items: {len(bb.get('open_items', []))}\n")
    bb["corp_cycle_status"] = "IDLE"
    bb["last_retro"] = _now()
    save_json(BB_PATH, bb)
    print(f"{GREEN}✅ RETRO_{today}.md written — Cycle {cycle} COMPLETE{RESET}")

    # ── Tích hợp Auto-Dream (TECH-01) ──
    reflector = os.path.join(ROOT, "system", "ops", "scripts", "cognitive_reflector.py")
    if os.path.exists(reflector):
        print(f"{CYAN}Kích hoạt giấc ngủ Auto-Dream (REM Sleep)...{RESET}")
        subprocess.run([sys.executable, reflector], check=False)

    cmd_hud_update()

def cmd_hud_update():
    """Update HUD via update_hud.ps1."""
    if os.path.exists(HUD_PS1):
        print(f"{CYAN}Updating HUD...{RESET}")
        try:
            subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-NoProfile", "-File", HUD_PS1], check=True)
            print(f"{GREEN}✅ HUD updated{RESET}")
        except subprocess.CalledProcessError as e:
            print(f"{RED}❌ HUD update failed: {e}{RESET}")
    else:
        print(f"{YELLOW}HUD script not found: {HUD_PS1}{RESET}")

def cmd_proposals_approve(prop_id=""):
    """Approve a proposal by index or name."""
    if not os.path.isdir(PROP_DIR):
        print("No proposals dir."); return
    props = sorted(f for f in os.listdir(PROP_DIR) if f.startswith("PROP_") and f.endswith(".md"))
    target = None
    if prop_id.isdigit():
        idx = int(prop_id) - 1
        target = props[idx] if 0 <= idx < len(props) else None
    else:
        matches = [p for p in props if prop_id.lower() in p.lower()]
        target = matches[0] if matches else None
    if not target:
        print(f"{RED}Proposal '{prop_id}' not found.{RESET}"); return
    fpath = os.path.join(PROP_DIR, target)
    with open(fpath, "a", encoding="utf-8") as f:
        f.write(f"\n\n## CEO DECISION\n- Status: APPROVED\n- Date: {_now()}\n- Notes: Approved via `aos proposals approve`\n")
    print(f"{GREEN}✅ APPROVED: {target}{RESET}")


def cmd_status():
    """Show current corp cycle status."""
    bb  = load_json(BB_PATH)
    kpi = load_json(KPI_PATH, {})

    status = bb.get("corp_cycle_status", "UNKNOWN")
    color  = GREEN if status == "IDLE" else YELLOW if status == "RUNNING" else RED

    print(f"\n{BOLD}╔══ AI OS Corp Status ══════════════════════╗{RESET}")
    print(f"  Cycle status : {color}{status}{RESET}")
    print(f"  Cycles done  : {bb.get('cycles_complete', 0)}")
    print(f"  Last cycle   : {bb.get('last_cycle_date', 'N/A')}")
    print(f"  Last Phase 7 : {bb.get('last_phase7', 'N/A')[:19]}")
    print(f"  Skill cov.   : {kpi.get('metrics', {}).get('skill_coverage', 'N/A')}")
    print(f"  FAST_INDEX   : {kpi.get('metrics', {}).get('fast_index_paths', 'N/A')} paths")
    print(f"  ClawTask     : {kpi.get('metrics', {}).get('clawtask_views', 'N/A')} views")

    props = bb.get("pending_proposals", [])
    if props:
        print(f"\n  {YELLOW}Pending proposals ({len(props)}):{RESET}")
        for p in props:
            print(f"    • {p}")

    print(f"{BOLD}╚═══════════════════════════════════════════╝{RESET}\n")


def cmd_retro():
    """Run Phase 7 — Reflect + Propose."""
    script = os.path.join(ROOT, "system", "ops", "scripts", "phase7_retro.py")
    if os.path.exists(script):
        print(f"{CYAN}Running Phase 7 (Reflect + Propose)...{RESET}")
        subprocess.run([sys.executable, script], check=True)
    else:
        print(f"{RED}Error: ops/phase7_retro.py not found{RESET}")
        sys.exit(1)


def cmd_proposals():
    """List pending CEO proposals."""
    if not os.path.isdir(PROP_DIR):
        print("No proposals dir found.")
        return
    files = sorted(f for f in os.listdir(PROP_DIR) if f.startswith("PROP_") and f.endswith(".md"))
    if not files:
        print("No proposals found.")
        return
    print(f"\n{BOLD}CEO Proposals ({len(files)}){RESET}")
    for fname in files:
        fpath = os.path.join(PROP_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        title = next((l.lstrip("# ") for l in lines if l.startswith("# ")), fname)
        priority = next((l.split("|")[1].strip() for l in lines if "Priority" in l), "?")
        print(f"  {YELLOW}•{RESET} {title}")
        print(f"    File: {fname}   Priority: {priority}")
    print()


def cmd_brief():
    """Show CEO daily brief summary."""
    if not os.path.isdir(BRIEF_DIR):
        print("No daily briefs found.")
        return
    briefs = sorted(os.listdir(BRIEF_DIR), reverse=True)
    print(f"\n{BOLD}Daily Briefs ({len(briefs)} total){RESET}")
    for b in briefs[:10]:
        print(f"  • {b}")
    if len(briefs) > 10:
        print(f"  ... and {len(briefs) - 10} more")
    print()


def cmd_dispatch(dept: str):
    """Dispatch tasks to a department (Phase 3 stub)."""
    print(f"{CYAN}Dispatching to department: {dept}{RESET}")
    # Stub — in full impl would write to subagents/mq/<dept>_tasks.md
    mq_dir = os.path.join(ROOT, "subagents", "mq")
    os.makedirs(mq_dir, exist_ok=True)
    task_file = os.path.join(mq_dir, f"{dept}_tasks.md")
    entry = f"\n## Dispatch {datetime.now().isoformat()[:19]}\n- [ ] Manual dispatch from `aos dispatch {dept}`\n"
    with open(task_file, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"{GREEN}Task written to: subagents/mq/{dept}_tasks.md{RESET}")


def cmd_rebuild_index():
    """Rebuild FAST_INDEX from scratch."""
    script = os.path.join(ROOT, "brain", "shared-context", "rebuild_fast_index.py")
    if os.path.exists(script):
        print(f"{CYAN}Rebuilding FAST_INDEX...{RESET}")
        subprocess.run([sys.executable, script], check=True)
    else:
        print(f"{RED}Error: brain/shared-context/rebuild_fast_index.py not found{RESET}")
        sys.exit(1)


COMMANDS = {
    "status":         cmd_status,
    "retro":          cmd_retro,
    "proposals":      cmd_proposals,
    "brief":          cmd_brief,
    "rebuild-index":  cmd_rebuild_index,
    "hud":            cmd_hud_update,
}


def main():
    args = sys.argv[1:]
    if not args:
        print(f"{BOLD}aos — AI OS Corp CLI v2.0{RESET}")
        print("Usage: python ops/aos.py <command> [args]")
        print("\nCommands:")
        print("  corp start            Boot + CEO Brief (Phase 0-1)")
        print("  corp dispatch [dept]  Dispatch tasks (Phase 2-3)")
        print("  corp retro            Synthesis + Retro + HUD (Phase 5-7)")
        print("  hud update            Update HUD dashboard")
        print("  proposals             List pending proposals")
        print("  proposals approve <id> Approve a proposal")
        for cmd, fn in COMMANDS.items():
            doc = fn.__doc__ or ""
            if cmd not in ("hud",):
                print(f"  {cmd:<16} {doc.strip()}")
        return

    cmd  = args[0].lower()
    sub  = args[1].lower() if len(args) > 1 else ""
    rest = args[2:]

    if cmd == "corp":
        if sub == "start":          cmd_corp_start()
        elif sub == "dispatch":     cmd_corp_dispatch(rest[0] if rest else "all")
        elif sub == "retro":        cmd_corp_retro()
        else: print(f"{RED}Unknown corp sub-command: {sub}{RESET}")
    elif cmd == "dispatch":
        cmd_corp_dispatch(sub or "engineering")
    elif cmd == "hud" and sub == "update":
        cmd_hud_update()
    elif cmd == "proposals" and sub == "approve":
        cmd_proposals_approve(rest[0] if rest else "")
    elif cmd == "project":
        cmd_project(args[1:])
    elif cmd == "intake":
        cmd_intake(args[1:])
    elif cmd in COMMANDS:
        COMMANDS[cmd]()
    else:
        print(f"{RED}Unknown command: {cmd}{RESET}")
        sys.exit(1)


# ─── C1: Intake Command ────────────────────────────────────────────────────────

def cmd_intake(args):
    """C1: CEO paste link/text → CIV pipeline auto-classify + receipt"""
    import sys
    _scripts = os.path.join(ROOT, "system", "ops", "scripts")
    source = " ".join(args) if args else ""
    if not source:
        print(f"{RED}Usage: aos intake <url_or_text>{RESET}")
        return

    print(f"{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}CIV INTAKE PIPELINE{RESET}")
    print(f"  Source: {source}")
    print(f"{CYAN}{'='*60}{RESET}")

    # Step 1: Classify
    print(f"\n{YELLOW}[Step 1] Classifying...{RESET}")
    r = subprocess.run(
        [sys.executable, os.path.join(_scripts, "civ_classifier.py"), source],
        capture_output=True, text=True, cwd=ROOT
    )
    import json as _json
    try:
        cls = _json.loads(r.stdout)
        print(f"  Type: {GREEN}{cls['type']}{RESET} ({cls['confidence']})")
        print(f"  Route: {cls['route']}")
        print(f"  Agent: {cls['agent']}")
    except Exception:
        cls = {"type": "REPO", "route": "brain/knowledge/notes/", "agent": "content-analyst-agent", "label": source}
        print(f"  {YELLOW}(classifier error — defaulting to REPO){RESET}")

    # Step 2: Determine ticket ID
    from datetime import datetime as _dt
    date = _dt.now().strftime("%Y-%m-%d")
    ticket = f"CIV-{date}-AUTO"
    print(f"\n{YELLOW}[Step 2] Ticket: {ticket}{RESET}")

    # Step 3: Write to QUARANTINE staging
    staging_dir = os.path.join(ROOT, "security", "QUARANTINE", "incoming", cls["type"])
    os.makedirs(staging_dir, exist_ok=True)
    ticket_file = os.path.join(staging_dir, f"{ticket}.txt")
    with open(ticket_file, "w", encoding="utf-8") as f:
        f.write(f"Source: {source}\nType: {cls['type']}\nAgent: {cls['agent']}\nRoute: {cls['route']}\nDate: {date}\n")
    print(f"  Staged: {ticket_file.replace(ROOT, '').lstrip(os.sep)}")

    # Step 4: Generate receipt + Telegram
    print(f"\n{YELLOW}[Step 3] Generating receipt...{RESET}")
    title = source.split("/")[-1].split("?")[0][:40]
    subprocess.run([
        sys.executable, os.path.join(_scripts, "civ_receipt.py"),
        "--ticket", ticket, "--source", source,
        "--type", cls["type"], "--verdict", "PENDING",
        "--route", cls["route"], "--value", "MED",
        "--title", title,
    ], cwd=ROOT)

    print(f"\n{GREEN}CIV Intake submitted. Ticket: {ticket}{RESET}")
    print(f"  Next: Antigravity analyzes + writes KI note to brain/knowledge/notes/")

if __name__ == "__main__":
    main()


# ─── Project Init with Repo-on-Demand ──────────────────────────────────────────

def cmd_project(args):
    """Project init — detect needed repos, show clone commands, optionally auto-clone"""
    import subprocess as _sp
    if not args:
        print(f"{RED}Usage: aos project init <name> [--dept <dept>] [--clone]{RESET}")
        print("  Example: aos project init hud-dashboard --dept engineering --clone")
        return
    sub  = args[0] if args else "init"
    rest = args[1:] if len(args) > 1 else []

    if sub == "init" or sub not in ("init", "list"):
        # parse name + dept + clone flag
        name  = rest[0] if rest else sub
        dept  = ""
        auto_clone = False
        for i, a in enumerate(rest):
            if a == "--dept" and i+1 < len(rest): dept = rest[i+1]
            if a == "--clone": auto_clone = True

        print(f"{CYAN}{'='*60}{RESET}")
        print(f"{BOLD}PROJECT INIT: {name}{RESET}")
        if dept: print(f"  Dept: {dept}")
        print(f"{CYAN}{'='*60}{RESET}")

        resolver = os.path.join(ROOT, "system", "ops", "scripts", "repo_resolver.py")
        cmd = [sys.executable, resolver]
        if dept:
            cmd += ["--dept", dept]
        else:
            cmd += [name]
        if auto_clone:
            cmd += ["--clone"]

        r = _sp.run(cmd, cwd=ROOT)
        print(f"\n{GREEN}Project workspace ready. Repos above cloned/available.{RESET}")
        print(f"  Catalog: brain/knowledge/notes/LARGE_REPOS_CATALOG.md")
        print(f"  Workflow: ops/workflows/repo-on-demand.md")
