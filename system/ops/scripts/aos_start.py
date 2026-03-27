#!/usr/bin/env python3
"""
AOS START — AI OS Cognitive Boot Protocol v1.0
Owner: Antigravity | Based on GEMINI.md SECTION 2 Boot Sequence

Đây là quy trình KHỞI ĐỘNG NHẬN THỨC, KHÔNG start bất kỳ server/port nào.
Thực hiện 9 bước bắt buộc như trong GEMINI.md:
  STEP 1  → Read GEMINI.md (entry point)
  STEP 2  → Load Identity & Core Values          [brain/shared-context/SOUL.md]
  STEP 3  → Load Governance & Rules              [brain/shared-context/GOVERNANCE.md]
  STEP 4  → Load Agent Roster & Roles            [brain/shared-context/AGENTS.md]
  STEP 5  → Load Strategy & 40 Pillars           [brain/shared-context/THESIS.md]
  STEP 6  → Load Output Format Guide             [brain/shared-context/report_formats.md]
  STEP 7  → Check Blackboard (active tasks)       [brain/shared-context/blackboard.json]
  STEP 8  → Load Skill Registry                  [brain/shared-context/SKILL_REGISTRY.json]
  STEP 9  → Begin work — Print boot summary

Usage:
  python system/ops/scripts/aos_start.py
  OR via launcher: aos start
"""

import os, json, datetime, sys, subprocess

# Màu ANSI
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
GRAY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))

BOOT_FILES = [
    # (step, label, relative_path, required)
    (1, "GEMINI.md              (Entry Point)",      "GEMINI.md",                                          True),
    (2, "SOUL.md                (Identity)",         "brain/shared-context/SOUL.md",                       True),
    (3, "GOVERNANCE.md          (Rules)",            "brain/shared-context/GOVERNANCE.md",                 True),
    (4, "AGENTS.md              (Roster)",           "brain/shared-context/AGENTS.md",                     True),
    (5, "THESIS.md              (Strategy)",         "brain/shared-context/THESIS.md",                     False),
    (6, "report_formats.md      (Output Format)",    "brain/shared-context/report_formats.md",             False),
    (7, "event_bus.db           (Task Pub/Sub)",     "brain/shared-context/event_bus.db",                  True),
    (8, "SKILL_REGISTRY.json    (Skill Registry)",   "ecosystem/skills/SKILL_REGISTRY.json",           False),
]

def banner():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{CYAN}{BOLD}{'='*60}{RESET}")
    print(f"{CYAN}{BOLD}  AI OS CORP — COGNITIVE BOOT PROTOCOL{RESET}")
    print(f"{CYAN}{BOLD}  Antigravity | Boot v1.0 | {now}{RESET}")
    print(f"{CYAN}{BOLD}{'='*60}{RESET}\n")

def check_file(step, label, rel_path, required):
    full_path = os.path.join(ROOT, rel_path)
    exists = os.path.exists(full_path)

    if exists:
        size = os.path.getsize(full_path)
        size_label = f"{size//1024}KB" if size > 1024 else f"{size}B"

        status = f"{GREEN}✓{RESET}"
        if full_path.endswith('.json'):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    json.load(f)
            except Exception as e:
                status = f"{RED}SYNTAX ERROR{RESET}"
                print(f"  {RED}[STEP {step:02d}] ✗  {label:<42} {RED}(JSON Parse Error: {e}){RESET}")
                return False, full_path

        print(f"  {GREEN}[STEP {step:02d}] {status}{RESET}  {label:<42} {GRAY}({size_label}){RESET}")
        return True, full_path
    else:
        marker = f"{RED}[MISSING]{RESET}" if required else f"{YELLOW}[SKIP]{RESET}"
        print(f"  {marker} [STEP {step:02d}]  {label}")
        return False, None

def check_event_bus():
    """Đọc SQLite Event Bus xem có bao nhiêu Task Pending"""
    try:
        sys.path.append(ROOT)
        from system.ops.scripts.agent_bus import AgentBus
        bus = AgentBus()
        cnt = bus.get_pending_count()

        print(f"\n  {CYAN}── EVENT BUS (PUB/SUB) ────────────────────────────{RESET}")
        print(f"  {BOLD}📡 Tín Hiệu Nhiệm Vụ:{RESET} {YELLOW}{cnt} PENDING TASKS{RESET} đang vỗ biên")

        bus.cursor.execute("SELECT id, topic, status, picked_by FROM events WHERE status='PENDING' ORDER BY id ASC LIMIT 5")
        rows = bus.cursor.fetchall()
        if rows:
            for r in rows:
                print(f"     • [{r[1]:<10}] ID:{r[0]:03d} - Chưa có Agent tiếp nhận")
            if cnt > 5:
                print(f"     {GRAY}... và {cnt-5} tín hiệu khác{RESET}")
        else:
            print(f"  {GREEN}✓ Đội hình Agent đang rảnh rỗi. Event Bus trống.{RESET}")

    except Exception as e:
        print(f"  {YELLOW}[WARN] Không đọc được Event Bus: {e}{RESET}")

def read_skill_registry(path):
    """Đọc SKILL_REGISTRY.json và báo số skills active"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            reg = json.load(f)

        entries = reg.get('skills', [])
        active = [e for e in entries if str(e.get('status')).lower() == 'active']
        count  = reg.get('count', len(entries))

        print(f"\n  {CYAN}── SKILL REGISTRY ─────────────────────────────────{RESET}")
        print(f"  {BOLD}🎛️  Skills registered:{RESET} {count} total | {GREEN}{len(active)} active{RESET}")

        # Show by domain
        domains = {}
        for e in active:
            d = e.get('domain', 'unknown')
            domains[d] = domains.get(d, 0) + 1
        for dom, cnt in sorted(domains.items()):
            print(f"     {dom:<15} {cnt} skills")

    except Exception as e:
        print(f"  {YELLOW}[WARN] Không đọc được SKILL_REGISTRY: {e}{RESET}")

def check_environment():
    print(f"\n  {CYAN}── SYSTEM ENVIRONMENT ───────────────────────────────{RESET}")
    # Python
    py_ver = sys.version.split()[0]
    print(f"  {BOLD}🐍 Python:{RESET} {py_ver}")
    # Git
    try:
        branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, stderr=subprocess.DEVNULL).decode().strip()
        print(f"  {BOLD}🌿 Git Branch:{RESET} {branch}")
    except:
        print(f"  {BOLD}🌿 Git Branch:{RESET} {YELLOW}Not a git repo / git missing{RESET}")

    # MASTER.env
    env_path = os.path.join(ROOT, "system/ops/secrets/MASTER.env")
    if os.path.exists(env_path):
        size = os.path.getsize(env_path)
        print(f"  {BOLD}🔐 MASTER.env:{RESET} {GREEN}Loaded ({size} bytes){RESET}")
    else:
        print(f"  {BOLD}🔐 MASTER.env:{RESET} {RED}MISSING! LLM Agents sẽ lỗi.{RESET}")

def check_knowledge_pulse():
    print(f"\n  {CYAN}── KNOWLEDGE PULSE ────────────────────────────────{RESET}")
    active_path = os.path.join(ROOT, "storage/vault/DATA/ACTIVE_REPOS.md")
    pending_path = os.path.join(ROOT, "storage/vault/DATA/PENDING_REPOS.md")

    def count_links(p):
        if not os.path.exists(p): return 0
        with open(p, 'r', encoding='utf-8') as f:
            return sum(1 for line in f if line.strip().startswith("- [") and "](http" in line)

    active_cnt = count_links(active_path)
    pending_cnt = count_links(pending_path)

    print(f"  {BOLD}📚 Repositories:{RESET} {GREEN}{active_cnt} Active{RESET} | {YELLOW}{pending_cnt} Pending{RESET} in System Vault")

def check_memory_core():
    print(f"\n  {CYAN}── LONG-TERM MEMORY (LTM) ─────────────────────────{RESET}")
    try:
        sys.path.append(ROOT)
        from system.ops.scripts.memory_daemon import MemoryCore
        core = MemoryCore()
        memories = core.get_all()
        count = len(memories) if memories else 0
        print(f"  {BOLD}🧠 Cortex Status:{RESET} {GREEN}ONLINE & READY{RESET}")
        print(f"  {BOLD}📚 Total Memories:{RESET} {count} Neural Nodes mapped in Qdrant Local")
    except Exception as e:
        print(f"  {BOLD}🧠 Cortex Status:{RESET} {YELLOW}OFFLINE / SYNCING ({e}){RESET}")

def check_automations():
    print(f"\n  {CYAN}── AUTOMATIONS & DAEMONS ──────────────────────────{RESET}")
    auto_path = os.path.join(ROOT, "system/automations/AUTOMATION_REGISTRY.yaml")
    if not os.path.exists(auto_path):
        print(f"  {YELLOW}Registry missing.{RESET}")
        return

    try:
        import yaml
        with open(auto_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        automations = data.get('automations', {})
        active = [a for a in automations.values() if a.get('status') == 'active']
        print(f"  {BOLD}⚙️  Running:{RESET} {GREEN}{len(active)} active daemons{RESET} / {len(automations)} total")
        for a in active[:3]:
            # The dictionary might not have 'name', so we just print its description or something,
            # or if it has a 'path' we can use that. Actually let's assume 'path' is safe
            path_show = str(a.get('path', 'Unknown'))[:40]
            print(f"     • {path_show}...")
        if len(active) > 3:
            print(f"     {GRAY}... and {len(active)-3} more{RESET}")
    except ImportError:
        print(f"  {YELLOW}[WARN] PyYAML not installed. Tự cài: pip install pyyaml{RESET}")
    except Exception as e:
        print(f"  {RED}Error reading yaml: {e}{RESET}")


def boot_summary(results):
    ok      = sum(1 for ok, _ in results if ok)
    total   = len(results)
    missing = [(step, label) for (step, label, _, req), (ok, _) in zip(BOOT_FILES, results) if not ok and req]

    print(f"\n{CYAN}{'='*60}{RESET}")
    print(f"  Boot result: {GREEN if not missing else RED}{ok}/{total}{RESET} files loaded")

    if missing:
        print(f"\n  {RED}⚠ MISSING REQUIRED FILES:{RESET}")
        for step, label in missing:
            print(f"    STEP {step:02d}: {label}")
        print(f"\n  {YELLOW}Boot INCOMPLETE — Resolve missing files trước khi làm việc.{RESET}")
    else:
        print(f"\n  {GREEN}{BOLD}☀ HỆ THỐNG ĐÃ SẴN SÀNG CHO CA LÀM VIỆC MỚI.{RESET}")
        print(f"\n  {BOLD}CÁC LỆNH TIẾP THEO:{RESET}")
        print(f"  {GRAY}  aos corp start   → Corp daily cycle{RESET}")
        print(f"  {GRAY}  aos hud          → Xem HUD dashboard{RESET}")
        print(f"  {GRAY}  aos ingest <url> → Nạp URL mới{RESET}")

    print(f"{CYAN}{'='*60}{RESET}\n")

if __name__ == "__main__":
    banner()

    # Run Diagnostics First
    check_environment()
    check_knowledge_pulse()
    check_memory_core()
    check_automations()

    print(f"\n  {BOLD}── BOOT SEQUENCE ───────────────────────────────────{RESET}")
    results = []
    bb_path   = None
    sk_path   = None

    for step, label, rel, required in BOOT_FILES:
        ok, path = check_file(step, label, rel, required)
        results.append((ok, path))
        if step == 7 and ok:
            bb_path = path
        if step == 8 and ok:
            sk_path = path

    # Step 7: Event Bus detail
    if bb_path:
        check_event_bus()

    # Step 8: Skill Registry detail
    if sk_path:
        read_skill_registry(sk_path)

    # Step 9: Summary
    boot_summary(results)
