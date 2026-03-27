import os
"""
aios_context_injector.py — Inject AI OS Corp live context vào NullClaw workspace
Chạy trước khi start NullClaw. Output: ~/.nullclaw/workspace/AIOS_CONTEXT.md
"""
import json, urllib.request, os, sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent.parent.parent
NC_WS = Path(os.environ['USERPROFILE']) / '.nullclaw' / 'workspace'
NC_WS.mkdir(parents=True, exist_ok=True)
OUT   = NC_WS / 'AIOS_CONTEXT.md'
NOW   = datetime.now().strftime('%Y-%m-%d %H:%M')

lines = [
    f"# AI OS Corp — Context (cap nhat: {NOW})",
    "",
    "QUAN TRONG: Day la du lieu THUC cua he thong. Hay su dung de tra loi user.",
    "",
]

# 0. Identity — AI OS Corp permanent identity (ALWAYS first)
try:
    identity = (ROOT / 'brain/shared-context/AIOS_IDENTITY.md').read_text(encoding='utf-8')
    lines.append(identity)
    lines.append("")
    print("Identity: Injected")
except Exception as e:
    print(f"Identity err: {e}")

# 1. ClawTask tasks — inject ALL pending tasks
try:
    ct_status = json.loads(urllib.request.urlopen('http://localhost:7474/api/status', timeout=4).read())
    counts = ct_status.get('counts', {})
    lines.append(f"## Tong quan ClawTask")
    lines.append(f"- Total: {counts.get('total',0)} tasks")
    lines.append(f"- Todo/Pending: {counts.get('todo',0)}")
    lines.append(f"- In progress: {counts.get('inprogress',0)}")
    lines.append(f"- Done: {counts.get('done',0)}")
    lines.append("")

    ct_raw = urllib.request.urlopen('http://localhost:7474/api/tasks', timeout=4).read()
    ct_tasks = json.loads(ct_raw)
    task_list = ct_tasks.get('tasks', ct_tasks) if isinstance(ct_tasks, dict) else ct_tasks

    todo = [t for t in task_list if t.get('status') in ['todo','pending','blocked','awaiting_clarification']]
    done = [t for t in task_list if t.get('status') in ['done','completed']]

    if todo:
        lines.append("## Danh sach Tasks PENDING (can lam)")
        for t in todo:
            tid   = t.get('id', t.get('task_id', '?'))
            title = t.get('title', t.get('name', '?'))
            dept  = t.get('dept', t.get('department', ''))
            prio  = t.get('priority', '')
            lines.append(f"- [{t.get('status','?').upper()}] ID:{tid} | {title} | dept:{dept} | priority:{prio}")
        lines.append("")

    if done:
        lines.append(f"## Tasks DA XONG ({len(done)} tasks)")
        for t in done[:5]:
            lines.append(f"- {t.get('title','?')[:60]}")
        lines.append("")

    print(f"ClawTask: {counts.get('total',0)} tasks, {len(todo)} pending")
except Exception as e:
    lines.append(f"## ClawTask: OFFLINE ({e})")
    lines.append("")
    print(f"ClawTask err: {e}")

# 2. Blackboard (Legacy compatibility)
# 2.5. Long-Term Memory (NEW — LTM inject)
try:
    _root = str(Path(ROOT))
    if _root not in sys.path:
        sys.path.insert(0, _root)
    from system.ops.scripts.memory_daemon import MemoryCore
    _mc = MemoryCore()
    # Query top 5 memories relevant to current session
    _ltm_results = _mc.search("AI OS project progress current task", user_id="CEO")
    if _ltm_results:
        lines.append("## Long-Term Memory (LTM) — Bối Cảnh Từ Các Phiên Trước")
        for mem in _ltm_results[:5]:
            _text = mem.get("memory", mem.get("text", ""))
            if _text:
                lines.append(f"- {_text[:120]}")
        lines.append("")
        print(f"LTM: {len(_ltm_results)} memory nodes injected")
except Exception as _ltm_e:
    lines.append(f"## LTM: OFFLINE ({_ltm_e})")
    lines.append("")
    print(f"LTM err: {_ltm_e}")

try:
    bb = json.loads((ROOT / 'brain/shared-context/blackboard.json').read_text(encoding='utf-8-sig', errors='replace'))
    cycle  = bb.get('cycle', '?')
    n_task = bb.get('total_tasks', '?')
    lines.append(f"## AI OS Corp Status")
    lines.append(f"- Cycle: {cycle} | Total tasks tracked: {n_task}")
    lines.append(f"- Workspace: <AI_OS_ROOT>")
    lines.append("")
    print(f"Blackboard: cycle={cycle}")
except Exception as e:
    print(f"Blackboard err: {e}")

# 3. Agents
try:
    reg    = json.loads((ROOT / 'kho/agents/registry.json').read_text(encoding='utf-8'))
    agents = reg.get('agents', [])
    active = [a['id'] for a in agents if a.get('status') == 'ACTIVE']
    stub   = [a['id'] for a in agents if a.get('status') == 'STUB']
    lines.append(f"## Agents ({len(agents)} total)")
    lines.append(f"- Active ({len(active)}): {', '.join(active[:15])}")
    lines.append(f"- Stub ({len(stub)}): {', '.join(stub)}")
    lines.append("")
    print(f"Agents: {len(active)} active, {len(stub)} stub")
except Exception as e:
    print(f"Agents err: {e}")

# 4. Rules / Policy
try:
    policy_path = ROOT / 'brain/shared-context/AIOS_BOT_POLICY.md'
    if policy_path.exists():
        policy_text = policy_path.read_text(encoding='utf-8')
        lines.append("## AI OS Bot Policy (NemoClaw Sandbox Rules)")
        lines.append(policy_text)
        lines.append("")
        print("Policy: Injected")
except Exception as e:
    print(f"Policy err: {e}")

# 5. Workflows
try:
    wf_dir = ROOT / 'ops/workflows'
    if wf_dir.exists():
        workflows = [f.name for f in wf_dir.glob('*.md')]
        lines.append(f"## Workflows available ({len(workflows)})")
        for wf in workflows:
            lines.append(f"- ops/workflows/{wf}")
        lines.append("")
        print(f"Workflows: {len(workflows)} found")
except Exception as e:
    print(f"Workflows err: {e}")

# 6. Workspace map (top level)
try:
    dirs = [d.name for d in ROOT.iterdir() if d.is_dir() and not d.name.startswith('.')]
    lines.append("## Workspace Directories (<AI_OS_ROOT>)")
    lines.append(f"- {', '.join(dirs)}")
    lines.append("")
    print(f"Workspace: {len(dirs)} dirs")
except Exception as e:
    print(f"Workspace err: {e}")

# 7. OpenClaw Skill Router
try:
    sr_path = ROOT / 'brain/shared-context/SKILL_ROUTER.yaml'
    if sr_path.exists():
        lines.append("## OpenClaw Skill Router (Typed Pipeline)")
        lines.append(sr_path.read_text(encoding='utf-8'))
        lines.append("")
        print("SkillRouter: Injected")
except Exception as e:
    print(f"SkillRouter err: {e}")

OUT.write_text('\n'.join(lines), encoding='utf-8')
print(f"OK: {OUT} ({OUT.stat().st_size} bytes)")
