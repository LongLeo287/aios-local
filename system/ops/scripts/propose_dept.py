#!/usr/bin/env python3
"""
propose_dept.py — AI OS Corp V3.1 Autonomous Department Proposal & Activation Engine
Path: system/ops/scripts/propose_dept.py

Antigravity scans org_chart → tìm gaps → tạo proposals → CEO approve → auto-execute.

Usage:
  python system/ops/scripts/propose_dept.py --scan          # Phân tích gaps hiện tại
  python system/ops/scripts/propose_dept.py --propose       # Tạo proposals cho CEO duyệt
  python system/ops/scripts/propose_dept.py --approve <id>  # CEO duyệt → auto-execute toàn bộ
  python system/ops/scripts/propose_dept.py --approve-all   # Duyệt tất cả PENDING proposals
  python system/ops/scripts/propose_dept.py --list          # Xem proposals hiện tại
"""

import json
import sys
import datetime
import subprocess
from pathlib import Path

try:
    from ruamel.yaml import YAML
    RUAMEL_OK = True
except ImportError:
    RUAMEL_OK = False

ROOT = Path(__file__).parent.parent.parent.parent  # system/ops/scripts -> AI OS root
PROPOSAL_DIR = ROOT / "brain" / "shared-context" / "corp" / "proposals"
DEPT_DIR     = ROOT / "brain" / "corp" / "departments"
ORG_CHART    = ROOT / "brain" / "corp" / "org_chart.yaml"
MEMORY_DEPTS = ROOT / "brain" / "corp" / "memory" / "departments"
BRIEFS_DIR   = ROOT / "brain" / "shared-context" / "corp" / "daily_briefs"
WORKFORCE    = ROOT / "ecosystem" / "workforce" / "agents"
AGENTS_MD    = ROOT / "brain" / "shared-context" / "AGENTS.md"
CREATE_AGENT = ROOT / "system" / "ops" / "scripts" / "create_agent.py"

def now():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat()

def today():
    return datetime.date.today().isoformat()

def pid():
    return f"DEPT-PROPOSAL-{today()}-{datetime.datetime.now().strftime('%H%M%S')}"


# ─── 21 DEPARTMENTS định nghĩa trong org_chart ───────────────────────────────
KNOWN_DEPTS = {
    "engineering":           {"head": "backend-architect-agent", "reports_to": "CTO"},
    "qa_testing":            {"head": "test-manager-agent",      "reports_to": "CTO"},
    "it_infra":              {"head": "it-manager-agent",        "reports_to": "CTO"},
    "marketing":             {"head": "growth-agent",            "reports_to": "CMO"},
    "support":               {"head": "channel-agent",           "reports_to": "CMO"},
    "content_review":        {"head": "editor-agent",            "reports_to": "CMO"},
    "operations":            {"head": "scrum-master-agent",      "reports_to": "COO"},
    "hr_people":             {"head": "hr-manager-agent",        "reports_to": "COO"},
    "security_grc":          {"head": "strix-agent",             "reports_to": "COO"},
    "finance":               {"head": "cost-manager-agent",      "reports_to": "CFO"},
    "strategy":              {"head": "product-manager-agent",   "reports_to": "CSO"},
    "legal":                 {"head": "legal-agent",             "reports_to": "CSO"},
    "rd":                    {"head": "rd-lead-agent",           "reports_to": "CSO"},
    "registry_capability":   {"head": "registry-manager-agent",  "reports_to": "CTO"},
    "asset_library":         {"head": "library-manager-agent",   "reports_to": "COO"},
    "od_learning":           {"head": "org-architect-agent",     "reports_to": "CSO"},
    "planning_pmo":          {"head": "pmo-agent",               "reports_to": "COO"},
    "monitoring_inspection": {"head": "monitor-chief-agent",     "reports_to": "COO"},
    "system_health":         {"head": "health-chief-agent",      "reports_to": "CTO"},
    "content_intake":        {"head": "intake-chief-agent",      "reports_to": "COO"},
    "client_reception":      {"head": "project-intake-agent",    "reports_to": "COO"},
}

REQUIRED_FILES = [
    "MANAGER_PROMPT.md",
    "WORKER_PROMPT.md",
    "rules.md",
]


def check_dept_files(dept_name: str) -> dict:
    """Check if a department has all required files."""
    dept_path = DEPT_DIR / dept_name
    results = {}
    for f in REQUIRED_FILES:
        results[f] = (dept_path / f).exists()
    results["memory"]      = (MEMORY_DEPTS / f"{dept_name}.md").exists()
    results["daily_brief"] = (BRIEFS_DIR / f"{dept_name}.md").exists()
    return results


def scan_gaps() -> list:
    """Scan all 21 departments, return list of gaps."""
    gaps = []
    for dept_name, info in KNOWN_DEPTS.items():
        status = check_dept_files(dept_name)
        missing = [f for f, exists in status.items() if not exists]
        if missing:
            gaps.append({
                "dept": dept_name,
                "head": info["head"],
                "reports_to": info["reports_to"],
                "missing_files": missing,
                "completeness": f"{len(status)-len(missing)}/{len(status)}",
            })
    return gaps


def cmd_scan():
    """Scan and display current department gaps."""
    print("\nAI OS Corp — Department Gap Analysis")
    print("=" * 50)
    gaps = scan_gaps()
    complete = [d for d in KNOWN_DEPTS if d not in [g["dept"] for g in gaps]]

    print(f"\nCOMPLETE ({len(complete)}/{len(KNOWN_DEPTS)}):")
    for d in complete:
        print(f"  [OK] {d}")

    print(f"\nINCOMPLETE ({len(gaps)}/{len(KNOWN_DEPTS)}):")
    for g in gaps:
        print(f"  [!!] {g['dept']} ({g['completeness']}) — missing: {', '.join(g['missing_files'])}")

    print(f"\nRun --propose to generate CEO proposals for all incomplete departments.\n")
    return gaps


def generate_manager_prompt(dept: str, head: str, reports_to: str) -> str:
    return f"""# Manager Prompt — {dept.replace('_', ' ').title()}
# Head: {head} | Reports to: {reports_to}
# AI OS Corp V3.1 | Created: {today()}

---

## Mission
Lead and coordinate the {dept.replace('_', ' ').title()} department.
Ensure all workers deliver on time, at quality, within governance.

## Team
- Head: {head} (reports to {reports_to})
- Workers: See brain/corp/org_chart.yaml → departments.{dept}.workers

## Boot Additions (run at session start)
1. Read this file
2. Check brain/shared-context/corp/daily_briefs/{dept}.md for pending items
3. Check brain/shared-context/blackboard.json for open tasks assigned to this dept

## Task Rules
- ALWAYS write receipt: system/telemetry/receipts/<task_id>.json after completing task
- ESCALATE to {reports_to} if: task blocked >1h, resource conflict, L3 event
- 2-Strike Rule: fail twice on same task -> set handoff_trigger: BLOCKED, report to Antigravity

## Workflow
1. Receive task from blackboard or CEO
2. Decompose into steps
3. Assign steps to workers (if applicable)
4. Monitor and synthesize worker outputs
5. Write daily brief to brain/shared-context/corp/daily_briefs/{dept}.md
6. Report completion/blockers back to supervisor

## Brief Format (daily output)
```
## {dept.upper()} BRIEF — {{DATE}}
STATUS: [ACTIVE|IDLE|BLOCKED]
TASKS COMPLETED: N
OPEN ITEMS: [list]
BLOCKERS: [list or NONE]
NEXT: [priority action]
```
"""


def generate_worker_prompt(dept: str, head: str) -> str:
    return f"""# Worker Prompt — {dept.replace('_', ' ').title()}
# Dept: {dept} | Manager: {head}
# AI OS Corp V3.1 | Created: {today()}

---

## Role Context
You are a specialist worker in the {dept.replace('_', ' ').title()} department.
You report to {head} and operate under AI OS governance.

## Skill Loading
Load from SKILL_REGISTRY.json the skills assigned to your agent ID before starting tasks.
Minimum: reasoning_engine + context_manager (always available).

## Task Ownership
- Take ownership of task when assigned
- Complete or escalate within SLA
- NEVER pass incomplete work without flagging

## Workflow Protocol
1. Receive task (from blackboard or {head})
2. Read required files/context
3. Execute with skill stack
4. Self-QA: does output meet spec?
5. Write receipt: system/telemetry/receipts/<task_id>.json
6. Report completion to {head}

## Receipt Format (after each task)
```json
{{
  "agent_id": "<your-agent-id>",
  "task_id": "<task_id>",
  "dept": "{dept}",
  "status": "COMPLETE|PARTIAL|BLOCKED",
  "output": "<summary>",
  "files_written": [],
  "timestamp": "<ISO8601>"
}}
```

## Escalation
- L1: Self-solve within 30 min
- L2: Ask {head} for guidance
- L3: Write ESCALATION_REPORT -> Antigravity
"""


def generate_rules(dept: str, reports_to: str) -> str:
    return f"""# Rules — {dept.replace('_', ' ').title()}
# Authority: Tier 2 | Reports to: {reports_to}
# AI OS Corp V3.1 | Created: {today()}

---

## Constraints
1. All outputs must follow report_formats.md
2. No external file writes outside designated paths
3. No autonomous agent creation without CEO approval
4. All tasks must generate a receipt before closing
5. Escalate L3 events immediately (do not buffer)

## Escalation Policy
- L1 (self): Agent resolves independently
- L2 (dept): Agent informs {dept} head, continues
- L3 (corp): Stop task. Write escalation. Alert Antigravity.
- CRITICAL: Any security/compliance event -> notify security_grc immediately

## Quality Gates
- All outputs self-reviewed before submission
- Dept head reviews before forwarding to supervisor
- See qa_rules.md for QA requirements

## Memory Policy
- Write to: brain/corp/memory/departments/{dept}.md (cycle entries)
- Format: MEMORY_SPEC.md Layer 3 schema
- Rotate after 10 entries (last 5 kept hot, rest to archive)
"""


def create_proposal(dept: str, info: dict, gaps: list) -> dict:
    """Create a proposal document for a department."""
    proposal_id = pid()
    proposal = {
        "id": proposal_id,
        "type": "DEPARTMENT_COMPLETION",
        "status": "PENDING_CEO",
        "dept": dept,
        "head_agent": info["head"],
        "reports_to": info["reports_to"],
        "missing_files": gaps,
        "proposed_actions": [
            f"Create brain/corp/departments/{dept}/MANAGER_PROMPT.md",
            f"Create brain/corp/departments/{dept}/WORKER_PROMPT.md",
            f"Create brain/corp/departments/{dept}/rules.md",
            f"Create brain/corp/memory/departments/{dept}.md",
            f"Create brain/shared-context/corp/daily_briefs/{dept}.md",
        ],
        "created_by": "Antigravity (propose_dept.py)",
        "created_at": now(),
        "ceo_approved": False,
        "approved_at": None,
    }
    return proposal


def save_proposal(proposal: dict) -> Path:
    """Save proposal to proposals directory."""
    PROPOSAL_DIR.mkdir(parents=True, exist_ok=True)
    path = PROPOSAL_DIR / f"PROPOSAL_{proposal['id']}.json"
    path.write_text(json.dumps(proposal, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def cmd_propose():
    """Generate proposals for all incomplete departments."""
    gaps = scan_gaps()
    if not gaps:
        print("\nAll departments are complete. No proposals needed.\n")
        return

    print(f"\nGenerating {len(gaps)} department completion proposals...\n")
    proposals = []
    for g in gaps:
        proposal = create_proposal(g["dept"], KNOWN_DEPTS[g["dept"]], g["missing_files"])
        path = save_proposal(proposal)
        proposals.append(proposal)
        print(f"  [+] Proposal created: {proposal['id']} — {g['dept']}")

    # Write summary proposal for CEO
    summary_path = PROPOSAL_DIR / f"DEPT_COMPLETION_SUMMARY_{today()}.md"
    lines = [
        f"# Department Completion Proposals — {today()}",
        f"Generated by: Antigravity (propose_dept.py)",
        f"Total: {len(gaps)} departments need completion\n",
        "---\n",
    ]
    for g in gaps:
        lines.append(f"## {g['dept'].replace('_',' ').title()}")
        lines.append(f"- Head: {g['head']}")
        lines.append(f"- Reports to: {g['reports_to']}")
        lines.append(f"- Completeness: {g['completeness']}")
        lines.append(f"- Missing: {', '.join(g['missing_files'])}")
        lines.append(f"- Proposal ID: DEPT-PROPOSAL-{today()}-* (see proposals/ folder)")
        lines.append("")

    lines += [
        "---",
        "## CEO Action Required",
        "",
        "To approve ALL proposals and auto-execute:",
        "```",
        "python system/ops/scripts/propose_dept.py --approve-all",
        "```",
        "",
        "To approve ONE proposal:",
        "```",
        "python system/ops/scripts/propose_dept.py --approve <dept-name>",
        "```",
    ]
    summary_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"\nSummary written: brain/shared-context/corp/proposals/DEPT_COMPLETION_SUMMARY_{today()}.md")
    print(f"\nTotal proposals: {len(proposals)}")
    print("\nCEO APPROVAL REQUIRED. Run --approve <dept> or --approve-all to execute.\n")


def execute_dept_activation(dept: str):
    """Auto-execute all file creation for a department."""
    info = KNOWN_DEPTS.get(dept)
    if not info:
        print(f"  [ERR] Unknown dept: {dept}")
        return False

    head = info["head"]
    reports_to = info["reports_to"]
    dept_path = DEPT_DIR / dept
    dept_path.mkdir(parents=True, exist_ok=True)

    created = []

    # MANAGER_PROMPT.md
    mp = dept_path / "MANAGER_PROMPT.md"
    if not mp.exists():
        mp.write_text(generate_manager_prompt(dept, head, reports_to), encoding="utf-8")
        created.append(f"brain/corp/departments/{dept}/MANAGER_PROMPT.md")

    # WORKER_PROMPT.md
    wp = dept_path / "WORKER_PROMPT.md"
    if not wp.exists():
        wp.write_text(generate_worker_prompt(dept, head), encoding="utf-8")
        created.append(f"brain/corp/departments/{dept}/WORKER_PROMPT.md")

    # rules.md
    rp = dept_path / "rules.md"
    if not rp.exists():
        rp.write_text(generate_rules(dept, reports_to), encoding="utf-8")
        created.append(f"brain/corp/departments/{dept}/rules.md")

    # Memory
    MEMORY_DEPTS.mkdir(parents=True, exist_ok=True)
    mem = MEMORY_DEPTS / f"{dept}.md"
    if not mem.exists():
        mem.write_text(
            f"# Dept Memory: {dept.replace('_',' ').title()}\n\n"
            f"## {today()} — Initialized\n"
            f"Head: {head}\nStatus: Active\nNote: Created by propose_dept.py auto-activation.\n",
            encoding="utf-8"
        )
        created.append(f"brain/corp/memory/departments/{dept}.md")

    # Daily brief channel
    BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    brief = BRIEFS_DIR / f"{dept}.md"
    if not brief.exists():
        brief.write_text(
            f"# Daily Brief: {dept.replace('_',' ').title()}\n\n"
            f"## {today()} — Activated\n"
            f"Department activated. Head: {head}. Ready for briefings.\n",
            encoding="utf-8"
        )
        created.append(f"brain/shared-context/corp/daily_briefs/{dept}.md")

    # Head agent scaffold (workforce folder)
    wf_agent = WORKFORCE / head
    wf_agent.mkdir(parents=True, exist_ok=True)
    skill_file = wf_agent / "SKILL.md"
    if not skill_file.exists():
        skill_file.write_text(
            f"---\nname: {head}\ndescription: Head of {dept.replace('_',' ').title()}\n"
            f"agents: [{head}]\ntier: tier2\nstatus: active\nadded: {today()}\n---\n\n"
            f"See: brain/corp/departments/{dept}/MANAGER_PROMPT.md\n",
            encoding="utf-8"
        )
        created.append(f"ecosystem/workforce/agents/{head}/SKILL.md")

    print(f"  [OK] {dept} — {len(created)} dept files created:")
    for f in created:
        print(f"       + {f}")

    if not created:
        print(f"  [--] {dept} — dept files already exist")

    # ── STEP 2: Smart routing — assign existing agent OR create new ──────────
    agent_md = ROOT / "brain" / "agents" / head / "AGENT.md"
    agent_exists = agent_md.exists()

    if agent_exists:
        # Agent đã có profile → cập nhật dept trong AGENT.md + org_chart
        print(f"\n  [=] Head agent '{head}' exists — assigning to '{dept}'...")

        # 2a. Update AGENT.md — đổi dept field
        try:
            content = agent_md.read_text(encoding="utf-8", errors="ignore")
            if f"Department: {dept}" not in content:
                # Replace dòng Department nếu có hoặc thêm vào header
                import re
                if re.search(r'# Department:.*', content):
                    content = re.sub(r'# Department:.*', f'# Department: {dept.title()}', content)
                elif re.search(r'\| \*\*Phòng ban\*\*.*\|', content):
                    content = re.sub(
                        r'(\| \*\*Phòng ban\*\*\s*\|).*?(\|)',
                        f'\\1 Dept ({dept.replace("_"," ").title()}) \\2',
                        content
                    )
                agent_md.write_text(content, encoding="utf-8")
                print(f"       [+] AGENT.md updated: Department → {dept}")
            else:
                print(f"       [=] AGENT.md already has dept={dept}")
        except Exception as e:
            print(f"       [WRN] Could not update AGENT.md: {e}")

        # 2b. Append to org_chart.yaml workers section (text append — safe)
        try:
            oc_text = ORG_CHART.read_text(encoding="utf-8", errors="ignore")
            if head not in oc_text:
                # Find the dept section and note agent needs manual registration
                print(f"       [!]  org_chart.yaml: '{head}' not yet listed under '{dept}'")
                print(f"       [!]  Manual step: Add to brain/corp/org_chart.yaml → departments.{dept}.workers")
            else:
                print(f"       [=] org_chart.yaml: '{head}' already registered")
        except Exception as e:
            print(f"       [WRN] Could not check org_chart.yaml: {e}")

        # 2c. Ghi assignment receipt
        assign_receipt_dir = ROOT / "system" / "telemetry" / "receipts" / "agent_assign"
        assign_receipt_dir.mkdir(parents=True, exist_ok=True)
        receipt = {
            "agent_id": head,
            "assigned_to_dept": dept,
            "assignment_type": "existing_agent_reused",
            "assigned_by": "propose_dept.py auto-activation",
            "assigned_at": now(),
            "agent_md_exists": True,
            "org_chart_note": "Verify agent is listed in org_chart.yaml workers",
        }
        (assign_receipt_dir / f"{head}_{dept}_{today()}.json").write_text(
            json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"       [+] Receipt: system/telemetry/receipts/agent_assign/{head}_{dept}_{today()}.json")

    else:
        # Chưa có → mở quy trình tạo agent mới
        print(f"\n  [>>] Head agent '{head}' NOT FOUND — triggering create_agent.py scaffold...")
        try:
            result = subprocess.run(
                ["python", str(CREATE_AGENT),
                 "--id", head,
                 "--dept", dept,
                 "--tier", "3",
                 "--head",
                 "--title", f"Head of {dept.replace('_', ' ').title()}"],
                capture_output=True, text=True, cwd=ROOT
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if line.strip():
                        print(f"       {line}")
            else:
                print(f"  [WRN] create_agent.py warning: {result.stderr[:200]}")
        except Exception as e:
            print(f"  [WRN] Could not run create_agent.py: {e}")

    return True


def cmd_approve(dept: str):
    """CEO approves a single department — auto-execute activation."""
    if dept not in KNOWN_DEPTS:
        print(f"\nUnknown department: '{dept}'")
        print(f"Valid departments: {', '.join(KNOWN_DEPTS.keys())}\n")
        return

    print(f"\nCEO APPROVED: Activating department '{dept}'...\n")
    success = execute_dept_activation(dept)

    if success:
        # Mark proposal as approved if exists
        for f in PROPOSAL_DIR.glob(f"PROPOSAL_DEPT-PROPOSAL-*{dept}*.json"):
            data = json.loads(f.read_text(encoding="utf-8"))
            data["status"] = "APPROVED"
            data["ceo_approved"] = True
            data["approved_at"] = now()
            f.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

        # Write activation receipt
        receipt_dir = ROOT / "system" / "telemetry" / "receipts" / "dept_activate"
        receipt_dir.mkdir(parents=True, exist_ok=True)
        receipt = {
            "dept": dept,
            "head": KNOWN_DEPTS[dept]["head"],
            "activated_by": "CEO approval via propose_dept.py",
            "activated_at": now(),
            "status": "ACTIVE",
        }
        (receipt_dir / f"{dept}_{today()}.json").write_text(
            json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"\n  Receipt written: system/telemetry/receipts/dept_activate/{dept}_{today()}.json")

        # ── STEP 3: Register into running system ─────────────────────────────
        print(f"\n  [>>] STEP 3: System Registration for '{dept}'...")
        register_dept_in_system(dept)

        print(f"\nDepartment '{dept}' is now ACTIVE and registered in system.\n")


def register_dept_in_system(dept: str):
    """
    Register new dept into all system files that drive runtime behavior.
    Called after dept + agent files are created and CEO has approved.

    Updates:
      1. AGENTS.md    — add agent entry so (other) agents know it exists at boot
      2. kpi_scoreboard.json  — add dept KPI slot so corp_cycle can track
      3. blackboard.json      — update total_depts count
      4. Print guidance for org_chart.yaml (YAML — manual)
    """
    info = KNOWN_DEPTS.get(dept, {})
    head = info.get("head", f"{dept}-head-agent")

    # 1. AGENTS.md — append entry block if not already present
    try:
        content = AGENTS_MD.read_text(encoding="utf-8", errors="ignore")
        if head not in content:
            entry = (
                f"\n\n### {head.replace('-', ' ').upper()}\n"
                f"**Role:** Head of {dept.replace('_', ' ').title()}\n"
                f"**Tier:** 2\n"
                f"**Department:** {dept}\n"
                f"**Reports to:** {info.get('reports_to', 'COO')}\n"
                f"**Key behaviors:**\n"
                f"- Lead {dept.replace('_',' ').title()} department\n"
                f"- Write daily brief to brain/shared-context/corp/daily_briefs/{dept}.md\n"
                f"- Escalate blockers to {info.get('reports_to', 'COO')}\n"
                f"- Created: {today()} via propose_dept.py\n"
                f"\n---"
            )
            AGENTS_MD.open("a", encoding="utf-8").write(entry)
            print(f"  [+] AGENTS.md: added entry for '{head}'")
        else:
            print(f"  [=] AGENTS.md: '{head}' already present")
    except Exception as e:
        print(f"  [WRN] AGENTS.md update failed: {e}")

    # 2. kpi_scoreboard.json — add dept slot
    KPI_FILE = ROOT / "brain" / "shared-context" / "corp" / "kpi_scoreboard.json"
    try:
        kpi = json.loads(KPI_FILE.read_text(encoding="utf-8", errors="ignore"))
        if dept not in kpi.get("departments", {}):
            kpi["departments"][dept] = {
                "head": head,
                "daily_target_score": 2,
                "completed_score": 0,
                "status": "idle",
                "metrics": {"tasks_completed": 0, "escalations": 0},
                "last_brief": None,
                "notes": f"Created {today()} via propose_dept.py"
            }
            # Update totals
            kpi["company_health"]["total_departments"] = len(kpi["departments"])
            kpi["_updated"] = now()
            KPI_FILE.write_text(json.dumps(kpi, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"  [+] kpi_scoreboard.json: added '{dept}' slot (total_departments={len(kpi['departments'])})")
        else:
            print(f"  [=] kpi_scoreboard.json: '{dept}' already has slot")
    except Exception as e:
        print(f"  [WRN] kpi_scoreboard.json update failed: {e}")

    # 3. blackboard.json — update system awareness
    BB_FILE = ROOT / "brain" / "shared-context" / "blackboard.json"
    try:
        bb = json.loads(BB_FILE.read_text(encoding="utf-8", errors="ignore"))
        corp_state = bb.get("corp_state", {})
        current = corp_state.get("total_depts", 0)
        if dept not in str(bb):  # rough check if dept is already mentioned
            corp_state["total_depts"] = max(current, len(KNOWN_DEPTS))
            corp_state[f"dept_{dept}_activated"] = today()
            bb["corp_state"] = corp_state
            bb["blackboard_updated_at"] = now()
            BB_FILE.write_text(json.dumps(bb, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"  [+] blackboard.json: corp_state.total_depts → {corp_state['total_depts']}")
        else:
            print(f"  [=] blackboard.json: dept already reflected")
    except Exception as e:
        print(f"  [WRN] blackboard.json update failed: {e}")

    # 4. org_chart.yaml — auto-update via ruamel.yaml (preserves comments)
    auto_update_org_chart(dept, head, info.get("reports_to", "COO"))


def auto_update_org_chart(dept: str, head: str, reports_to: str):
    """
    Auto-update org_chart.yaml to register new dept/agent.
    Uses ruamel.yaml to preserve all comments and formatting.

    - If dept exists: add agent to workers list if not already there
    - If dept is new: append full dept block at end of departments section
    """
    if not RUAMEL_OK:
        print(f"  [WRN] ruamel.yaml not installed — skipping org_chart auto-update")
        print(f"        Manual: Add '{head}' to brain/corp/org_chart.yaml → departments.{dept}")
        return

    try:
        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.default_flow_style = False
        yaml.width = 4096  # prevent line wrapping

        with open(ORG_CHART, "r", encoding="utf-8") as f:
            doc = yaml.load(f)

        depts = doc.get("departments", {})

        if dept in depts:
            # Dept exists → check/add head to workers
            dept_data = depts[dept]
            workers = dept_data.get("workers", [])

            # Check if agent already listed
            agent_ids = [w.get("agent", "") if isinstance(w, dict) else str(w) for w in workers]
            if head not in agent_ids and dept_data.get("head") != head:
                new_worker = {
                    "agent": head,
                    "role": f"Head of {dept.replace('_', ' ').title()} — added {today()}",
                }
                if workers is None:
                    dept_data["workers"] = [new_worker]
                else:
                    workers.append(new_worker)
                print(f"  [+] org_chart.yaml: added '{head}' to departments.{dept}.workers")
            else:
                print(f"  [=] org_chart.yaml: '{head}' already in '{dept}'")

        else:
            # New dept → append full block
            from ruamel.yaml.comments import CommentedMap, CommentedSeq
            new_dept = CommentedMap()
            new_dept["head"] = head
            new_dept["head_title"] = f"Head of {dept.replace('_', ' ').title()}"
            new_dept["reports_to"] = reports_to
            new_dept["prompt"] = f"brain/corp/departments/{dept}/MANAGER_PROMPT.md"
            new_dept["workers"] = CommentedSeq()
            new_dept["output_channel"] = f"shared-context/brain/corp/daily_briefs/{dept}.md"
            new_dept["qa_required"] = False
            new_dept["llm_tier"] = "economy"
            new_dept["memory"] = f"brain/corp/memory/departments/{dept}.md"
            new_dept.yaml_set_comment_before_after_key(
                "head", before=f"\n  # ── AUTO-CREATED: {dept.upper()} ({today()}) ─────────────────"
            )
            depts[dept] = new_dept
            print(f"  [+] org_chart.yaml: new dept block '{dept}' appended")

        doc["departments"] = depts

        with open(ORG_CHART, "w", encoding="utf-8") as f:
            yaml.dump(doc, f)

        print(f"  [+] org_chart.yaml saved (ruamel.yaml — comments preserved)")

    except Exception as e:
        print(f"  [WRN] org_chart.yaml auto-update failed: {e}")
        print(f"        Manual fallback: Add '{head}' to departments.{dept} in org_chart.yaml")



def cmd_approve_all():
    """CEO approves ALL pending department proposals — auto-execute all."""
    gaps = scan_gaps()
    if not gaps:
        print("\nAll departments already complete.\n")
        return

    print(f"\nCEO APPROVED ALL — Activating {len(gaps)} departments...\n")
    for g in gaps:
        print(f"--- {g['dept']} ---")
        execute_dept_activation(g["dept"])
        print()

    print(f"\nAll {len(gaps)} departments activated successfully.")
    print(f"Run --scan to verify.\n")


def cmd_list():
    """List all proposals."""
    PROPOSAL_DIR.mkdir(parents=True, exist_ok=True)
    proposals = list(PROPOSAL_DIR.glob("PROPOSAL_DEPT-*.json"))
    if not proposals:
        print("\nNo proposals found. Run --propose to generate.\n")
        return

    print(f"\nProposals ({len(proposals)}):")
    for p in sorted(proposals):
        data = json.loads(p.read_text(encoding="utf-8"))
        status = data.get("status", "UNKNOWN")
        dept   = data.get("dept", "?")
        print(f"  [{status:20}] {dept}")
    print()


# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    args = sys.argv[1:]

    if not args or "--help" in args:
        print("""
propose_dept.py — AI OS Corp Department Proposal & Activation Engine

Commands:
  --scan              Phân tích tất cả 21 phòng ban, tìm gaps
  --propose           Tạo proposals cho CEO duyệt
  --list              Xem proposals hiện tại
  --approve <dept>    CEO duyệt 1 phòng ban -> auto-execute
  --approve-all       CEO duyệt tất cả -> auto-execute hết

Flow:
  1. Antigravity chạy --propose (hoặc CEO gõ lệnh)
  2. CEO xem summary trong brain/shared-context/corp/proposals/
  3. CEO gõ: --approve <dept> hoặc --approve-all
  4. System tự tạo toàn bộ files + receipts
""")
        return

    if "--scan" in args:
        cmd_scan()
    elif "--propose" in args:
        cmd_propose()
    elif "--list" in args:
        cmd_list()
    elif "--approve-all" in args:
        cmd_approve_all()
    elif "--approve" in args:
        idx = args.index("--approve")
        dept = args[idx+1] if idx+1 < len(args) else ""
        if dept:
            cmd_approve(dept)
        else:
            print("Usage: --approve <dept-name>")
    else:
        print("Unknown command. Use --help.")
        sys.exit(1)


if __name__ == "__main__":
    main()
