#!/usr/bin/env python3
"""
AI OS V3.1 — Central Workflow Orchestrator (FULL EDITION)
Path: system/ops/aios_orchestrator.py
Built: 2026-03-26 | Based on AGENTS.md v4.0

Coverage:
  - 21 Departments
  - C-Suite (CEO/CTO/CMO/COO/CFO/CLO/CSO)
  - 99 Agent definitions (Tier 1-3)
  - 38 Subagents (spawned on-demand)
  - Corp Mode (daily cycle 7-phase)
  - Blackboard → Route → Dispatch → HUD → Telegram
"""

import json
import os
import sys
import time
import datetime
import urllib.request
import warnings
warnings.filterwarnings("ignore")
from pathlib import Path

# ─── OPTIONAL: Memory & Event Bus (graceful degrade if not ready) ─────────────
try:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from system.ops.scripts.memory_daemon import MemoryCore as _MemoryCore
    from system.ops.scripts.agent_bus import AgentBus as _AgentBus
    _MEMORY_CORE = _MemoryCore()
    _AGENT_BUS   = _AgentBus()
    _LTM_ONLINE  = True
except Exception as _e:
    print(f"[!] Cảnh báo: LTM/AgentBus Offline do lỗi - {_e}")
    _LTM_ONLINE = False
    _MEMORY_CORE = None
    _AGENT_BUS   = None

# ─── CONFIG ─────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent.parent
BLACKBOARD     = ROOT / "brain" / "shared-context" / "blackboard.json"
SKILL_REGISTRY = ROOT / "ecosystem" / "skills" / "SKILL_REGISTRY.json"
AGENTS_ROSTER  = ROOT / "brain" / "shared-context" / "AGENTS.md"
STATUS_JSON    = ROOT / "system" / "hud" / "STATUS.json"
RECEIPTS_DIR   = ROOT / "system" / "telemetry" / "receipts"
ACT_STATUS     = ROOT / "brain" / "agents" / "activation_status.json"
AGENTS_DIR     = ROOT / "ecosystem" / "workforce" / "agents"
PLUGINS_DIR    = ROOT / "ecosystem" / "plugins"

# ─── ENV ──────────────────────────────────────────────────────────────────────
def _load_env():
    env, path = {}, ROOT / ".env"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("="); env[k.strip()] = v.strip().strip('"')
    return env
ENV = _load_env()

# ─── FULL AGENT ROUTING TABLE (AGENTS.md v4.0) ───────────────────────────────
#
# Format: domain_keyword → { agent, tier, dept, primary_skill, fallback_agent }
# Domain keywords match against task["domain"] field (case-insensitive substring)
#
ROUTING_TABLE = {

    # ── TIER 0: C-SUITE (Corp Mode) ──────────────────────────────────────────
    "ceo":           {"agent": "antigravity",              "tier": 0, "dept": "CEO",          "skill": "reasoning_engine",       "fallback": "orchestrator_pro"},
    "strategy":      {"agent": "product-manager-agent",   "tier": 0, "dept": "CSO/Strategy",  "skill": "proposal_engine",        "fallback": "orchestrator_pro"},
    "operations":    {"agent": "scrum-master-agent",      "tier": 0, "dept": "COO/Ops",       "skill": "orchestrator_pro",       "fallback": "pmo-agent"},
    "finance":       {"agent": "cost-manager-agent",      "tier": 0, "dept": "CFO/Finance",   "skill": "insight_engine",         "fallback": "data-agent"},
    "legal":         {"agent": "legal-agent",             "tier": 0, "dept": "CLO/Legal",     "skill": "reasoning_engine",       "fallback": "security-engineer-agent"},
    "architecture":  {"agent": "software-architect-agent","tier": 0, "dept": "CTO",           "skill": "reasoning_engine",       "fallback": "backend-architect-agent"},

    # ── TIER 1: CORE AGENTS ───────────────────────────────────────────────────
    "orchestration": {"agent": "orchestrator_pro",        "tier": 1, "dept": "System",        "skill": "orchestrator_pro",       "fallback": "antigravity"},
    "intake":        {"agent": "civ-agent",               "tier": 1, "dept": "Dept20/Intake", "skill": "context_manager",        "fallback": "knowledge_agent"},
    "security":      {"agent": "security-engineer-agent", "tier": 1, "dept": "Dept10/GRC",    "skill": "agent-shield",           "fallback": "strix-agent"},
    "strix":         {"agent": "strix-agent",             "tier": 1, "dept": "Dept10/GRC",    "skill": "trivy",                  "fallback": "security-engineer-agent"},
    "registry":      {"agent": "registry-manager-agent",  "tier": 1, "dept": "Dept4",         "skill": "knowledge_navigator",    "fallback": "knowledge_agent"},
    "pmo":           {"agent": "pmo-agent",               "tier": 1, "dept": "Dept6/PMO",     "skill": "orchestrator_pro",       "fallback": "scrum-master-agent"},
    "health":        {"agent": "sre-agent",               "tier": 1, "dept": "Dept7/SRE",     "skill": "shell_assistant",        "fallback": "devops-agent"},
    "monitoring":    {"agent": "sre-agent",               "tier": 1, "dept": "Dept7/SRE",     "skill": "shell_assistant",        "fallback": "devops-agent"},
    "qa":            {"agent": "test-manager-agent",      "tier": 1, "dept": "Dept9/QA",      "skill": "reasoning_engine",       "fallback": "security-engineer-agent"},
    "testing":       {"agent": "test-manager-agent",      "tier": 1, "dept": "Dept9/QA",      "skill": "reasoning_engine",       "fallback": "security-engineer-agent"},

    # ── TIER 2: TECHNICAL SPECIALISTS ────────────────────────────────────────
    "engineering":   {"agent": "backend-architect-agent", "tier": 2, "dept": "Dept1/Eng",     "skill": "reasoning_engine",       "fallback": "software-architect-agent"},
    "backend":       {"agent": "backend-architect-agent", "tier": 2, "dept": "Dept1/Eng",     "skill": "reasoning_engine",       "fallback": "software-architect-agent"},
    "api":           {"agent": "backend-architect-agent", "tier": 2, "dept": "Dept1/Eng",     "skill": "framework-standards",    "fallback": "software-architect-agent"},
    "database":      {"agent": "backend-architect-agent", "tier": 2, "dept": "Dept1/Eng",     "skill": "framework-standards",    "fallback": "data-agent"},
    "frontend":      {"agent": "frontend-agent",          "tier": 2, "dept": "Dept1/Eng",     "skill": "shell_assistant",        "fallback": "ui-ux-agent"},
    "ui":            {"agent": "ui-ux-agent",             "tier": 2, "dept": "Dept1/Eng",     "skill": "reasoning_engine",       "fallback": "frontend-agent"},
    "ux":            {"agent": "ui-ux-agent",             "tier": 2, "dept": "Dept1/Eng",     "skill": "reasoning_engine",       "fallback": "frontend-agent"},
    "design":        {"agent": "ui-ux-agent",             "tier": 2, "dept": "Dept1/Eng",     "skill": "reasoning_engine",       "fallback": "frontend-agent"},
    "mobile":        {"agent": "mobile-agent",            "tier": 2, "dept": "Dept1/Eng",     "skill": "shell_assistant",        "fallback": "frontend-agent"},
    "android":       {"agent": "mobile-agent",            "tier": 2, "dept": "Dept1/Eng",     "skill": "shell_assistant",        "fallback": "frontend-agent"},
    "ios":           {"agent": "mobile-agent",            "tier": 2, "dept": "Dept1/Eng",     "skill": "shell_assistant",        "fallback": "frontend-agent"},
    "ai":            {"agent": "ai-ml-agent",             "tier": 2, "dept": "Dept1/AI",      "skill": "reasoning_engine",       "fallback": "backend-architect-agent"},
    "ml":            {"agent": "ai-ml-agent",             "tier": 2, "dept": "Dept1/AI",      "skill": "reasoning_engine",       "fallback": "backend-architect-agent"},
    "llm":           {"agent": "ai-ml-agent",             "tier": 2, "dept": "Dept1/AI",      "skill": "reasoning_engine",       "fallback": "knowledge_agent"},
    "rag":           {"agent": "ai-ml-agent",             "tier": 2, "dept": "Dept1/AI",      "skill": "smart_memory",           "fallback": "knowledge_agent"},
    "devops":        {"agent": "devops-agent",            "tier": 2, "dept": "Dept1/DevOps",  "skill": "shell_assistant",        "fallback": "sre-agent"},
    "deploy":        {"agent": "devops-agent",            "tier": 2, "dept": "Dept1/DevOps",  "skill": "gcp_deploy_skill",       "fallback": "sre-agent"},
    "cloud":         {"agent": "devops-agent",            "tier": 2, "dept": "Dept1/DevOps",  "skill": "gcp_deploy_skill",       "fallback": "gcp_architect"},
    "gcp":           {"agent": "gcp_architect",           "tier": 2, "dept": "Dept1/Cloud",   "skill": "gcp_deploy_skill",       "fallback": "devops-agent"},
    "sre":           {"agent": "sre-agent",               "tier": 2, "dept": "Dept7/SRE",     "skill": "shell_assistant",        "fallback": "devops-agent"},
    "incident":      {"agent": "sre-agent",               "tier": 2, "dept": "Dept7/SRE",     "skill": "resilience_engine",      "fallback": "security-engineer-agent"},
    "web":           {"agent": "web-researcher",          "tier": 2, "dept": "Dept14/RD",     "skill": "web_intelligence",       "fallback": "knowledge_agent"},
    "research":      {"agent": "web-researcher",          "tier": 2, "dept": "Dept14/RD",     "skill": "web_intelligence",       "fallback": "knowledge_agent"},
    "scrape":        {"agent": "web-researcher",          "tier": 2, "dept": "Dept14/RD",     "skill": "web_intelligence",       "fallback": "knowledge_agent"},
    "rd":            {"agent": "rd-lead-agent",           "tier": 2, "dept": "Dept14/RD",     "skill": "reasoning_engine",       "fallback": "ai-ml-agent"},
    "game":          {"agent": "game-designer-agent",     "tier": 2, "dept": "Special",       "skill": "reasoning_engine",       "fallback": "software-architect-agent"},

    # ── TIER 2: KNOWLEDGE & MEMORY ────────────────────────────────────────────
    "knowledge":     {"agent": "knowledge_agent",         "tier": 2, "dept": "Dept14/KB",     "skill": "knowledge_navigator",    "fallback": "archivist"},
    "memory":        {"agent": "knowledge_agent",         "tier": 2, "dept": "Dept14/KB",     "skill": "smart_memory",           "fallback": "archivist"},
    "archive":       {"agent": "archivist",               "tier": 2, "dept": "Dept14/Archive","skill": "context_manager",        "fallback": "knowledge_agent"},
    "reflect":       {"agent": "cognitive_reflector",     "tier": 2, "dept": "System",        "skill": "reasoning_engine",       "fallback": "archivist"},
    "learning":      {"agent": "cognitive_reflector",     "tier": 2, "dept": "OD/Learning",   "skill": "reasoning_engine",       "fallback": "knowledge_agent"},
    "notebooklm":    {"agent": "notebooklm-agent",        "tier": 2, "dept": "Dept14/KB",     "skill": "knowledge_navigator",    "fallback": "knowledge_agent"},

    # ── TIER 2: BUSINESS ──────────────────────────────────────────────────────
    "marketing":     {"agent": "growth-agent",            "tier": 2, "dept": "Dept2/Mkt",     "skill": "web_intelligence",       "fallback": "content-agent"},
    "growth":        {"agent": "growth-agent",            "tier": 2, "dept": "Dept2/Mkt",     "skill": "web_intelligence",       "fallback": "content-agent"},
    "seo":           {"agent": "growth-agent",            "tier": 2, "dept": "Dept2/Mkt",     "skill": "web_intelligence",       "fallback": "content-agent"},
    "ads":           {"agent": "growth-agent",            "tier": 2, "dept": "Dept2/Mkt",     "skill": "web_intelligence",       "fallback": "content-agent"},
    "social":        {"agent": "content-agent",           "tier": 2, "dept": "Dept2/Mkt",     "skill": "channel_manager",        "fallback": "growth-agent"},
    "content":       {"agent": "content-agent",           "tier": 2, "dept": "Dept2/Content", "skill": "reasoning_engine",       "fallback": "growth-agent"},
    "youtube":       {"agent": "content-agent",           "tier": 2, "dept": "Dept2/Content", "skill": "reasoning_engine",       "fallback": "growth-agent"},
    "copywriting":   {"agent": "content-agent",           "tier": 2, "dept": "Dept2/Content", "skill": "reasoning_engine",       "fallback": "growth-agent"},
    "crm":           {"agent": "channel_agent",           "tier": 2, "dept": "Dept19/Support","skill": "channel_manager",        "fallback": "growth-agent"},
    "customer":      {"agent": "channel_agent",           "tier": 2, "dept": "Dept19/Support","skill": "channel_manager",        "fallback": "growth-agent"},
    "support":       {"agent": "channel_agent",           "tier": 2, "dept": "Dept19/Support","skill": "channel_manager",        "fallback": "aios_bot"},
    "product":       {"agent": "product-manager-agent",  "tier": 2, "dept": "Dept5/PM",      "skill": "reasoning_engine",       "fallback": "scrum-master-agent"},
    "roadmap":       {"agent": "product-manager-agent",  "tier": 2, "dept": "Dept5/PM",      "skill": "reasoning_engine",       "fallback": "scrum-master-agent"},
    "hr":            {"agent": "hr-manager-agent",        "tier": 2, "dept": "Dept16/HR",     "skill": "reasoning_engine",       "fallback": "orchestrator_pro"},
    "onboard":       {"agent": "hr-manager-agent",        "tier": 2, "dept": "Dept16/HR",     "skill": "reasoning_engine",       "fallback": "orchestrator_pro"},
    "data":          {"agent": "data-agent",              "tier": 2, "dept": "Dept15/Data",   "skill": "reasoning_engine",       "fallback": "knowledge_agent"},
    "analytics":     {"agent": "data-agent",              "tier": 2, "dept": "Dept15/Data",   "skill": "reasoning_engine",       "fallback": "knowledge_agent"},
    "kpi":           {"agent": "data-agent",              "tier": 2, "dept": "Dept15/Data",   "skill": "reasoning_engine",       "fallback": "cost-manager-agent"},
    "report":        {"agent": "data-agent",              "tier": 2, "dept": "Dept15/Data",   "skill": "reasoning_engine",       "fallback": "archivist"},

    # ── COMMS & NOTIFICATIONS ─────────────────────────────────────────────────
    "comms":         {"agent": "channel_agent",           "tier": 2, "dept": "Dept19/Comms",  "skill": "channel_manager",        "fallback": "aios_bot"},
    "notification":  {"agent": "channel_agent",           "tier": 2, "dept": "Dept19/Comms",  "skill": "channel_manager",        "fallback": "aios_bot"},
    "telegram":      {"agent": "aios_bot",                "tier": 1, "dept": "Gateway",       "skill": "channel_manager",        "fallback": "channel_agent"},
    "alert":         {"agent": "channel_agent",           "tier": 2, "dept": "Dept19/Comms",  "skill": "channel_manager",        "fallback": "sre-agent"},
    "scrum":         {"agent": "scrum-master-agent",      "tier": 2, "dept": "Dept6/PMO",     "skill": "orchestrator_pro",       "fallback": "pmo-agent"},
    "sprint":        {"agent": "scrum-master-agent",      "tier": 2, "dept": "Dept6/PMO",     "skill": "orchestrator_pro",       "fallback": "pmo-agent"},
    "shell":         {"agent": "devops-agent",            "tier": 2, "dept": "Dept1/DevOps",  "skill": "shell_assistant",        "fallback": "sre-agent"},
    "script":        {"agent": "devops-agent",            "tier": 2, "dept": "Dept1/DevOps",  "skill": "shell_assistant",        "fallback": "sre-agent"},
    "plugin":        {"agent": "registry-manager-agent",  "tier": 2, "dept": "Dept4",         "skill": "knowledge_navigator",    "fallback": "strix-agent"},
    "skill":         {"agent": "skill-creator-agent",     "tier": 2, "dept": "Dept4",         "skill": "knowledge_navigator",    "fallback": "registry-manager-agent"},
}

# ── DEPARTMENT MAP (21 Depts) ─────────────────────────────────────────────────
DEPARTMENTS = {
    "Dept1":  {"name": "Engineering",         "head": "software-architect-agent",  "members": ["backend-architect-agent","frontend-agent","ai-ml-agent","devops-agent","sre-agent","mobile-agent","ui-ux-agent","web-researcher"]},
    "Dept2":  {"name": "Marketing",           "head": "growth-agent",              "members": ["content-agent","channel_agent"]},
    "Dept4":  {"name": "Registry&Capability", "head": "registry-manager-agent",    "members": ["skill-creator-agent"]},
    "Dept5":  {"name": "Product/Strategy",    "head": "product-manager-agent",     "members": ["scrum-master-agent","pmo-agent"]},
    "Dept6":  {"name": "PMO",                 "head": "pmo-agent",                 "members": ["scrum-master-agent"]},
    "Dept7":  {"name": "SRE/Monitoring",      "head": "sre-agent",                 "members": ["devops-agent","nemoclaw","tinyclaw"]},
    "Dept9":  {"name": "QA/Testing",          "head": "test-manager-agent",        "members": ["security-engineer-agent"]},
    "Dept10": {"name": "Security/GRC",        "head": "security-engineer-agent",   "members": ["strix-agent","security_agent"]},
    "Dept14": {"name": "Knowledge/RD",        "head": "knowledge_agent",           "members": ["archivist","web-researcher","cognitive_reflector","rd-lead-agent","notebooklm-agent"]},
    "Dept15": {"name": "Data/Analytics",      "head": "data-agent",                "members": ["cost-manager-agent"]},
    "Dept16": {"name": "HR/People",           "head": "hr-manager-agent",          "members": []},
    "Dept19": {"name": "Support/Comms",       "head": "channel_agent",             "members": ["aios_bot"]},
    "Dept20": {"name": "Content Intake",      "head": "civ-agent",                 "members": ["content-analyst-agent"]},
    "Legal":  {"name": "Legal/Compliance",    "head": "legal-agent",               "members": []},
    "System": {"name": "System Core",         "head": "antigravity",               "members": ["orchestrator_pro","cognitive_reflector","archivist","aios_bot","gcp_architect"]},
}

# ─── HELPERS ────────────────────────────────────────────────────────────────
def now_iso(): return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat()
def now_ts(): return datetime.datetime.now().strftime("%H:%M:%S")

def load_json(path):
    try:
        with open(path, encoding="utf-8-sig") as f: return json.load(f)
    except: return {}

def save_json(path, data, indent=2):
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
            json.dump(data, f, indent=indent, ensure_ascii=False)
        os.replace(tmp_path, path)
    finally:
        if os.path.exists(lock_path):
            try: os.remove(lock_path)
            except: pass

def log(msg, level="INFO"):
    icon = {"INFO": "ℹ️", "OK": "✅", "WARN": "⚠️", "ERR": "❌", "ROUTE": "🔀", "DISPATCH": "📤"}.get(level, "•")
    print(f"[{now_ts()}] {icon} {msg}")

# ─── LTM + BUS HELPERS ────────────────────────────────────────────────────────
def _bus_publish(topic: str, payload: dict):
    """Publish task event to Agent Bus (silent fail if offline)"""
    if _AGENT_BUS:
        try:
            _AGENT_BUS.publish(topic, payload)
        except: pass

def _ltm_save(fact: str, agent_id: str = "orchestrator"):
    """Save fact to Long-Term Memory (silent fail if offline)"""
    if _MEMORY_CORE:
        try:
            _MEMORY_CORE.add_fact(fact, user_id="CEO", agent_id=agent_id)
        except: pass

# ─── ROUTING ENGINE ───────────────────────────────────────────────────────────
def route_task(task: dict) -> dict:
    """
    Route task to best agent based on domain keywords in ROUTING_TABLE.
    Checks: task['domain'] → task['type'] → task['title'] in order.
    Falls back to orchestrator_pro if no match.
    """
    search_fields = [
        task.get("domain", ""),
        task.get("type", ""),
        task.get("title", ""),
        task.get("description", ""),
    ]

    for field in search_fields:
        field_lower = field.lower()
        for keyword, route in ROUTING_TABLE.items():
            if keyword in field_lower:
                log(f"Matched keyword '{keyword}' → {route['agent']} (Tier {route['tier']}, {route['dept']})", "ROUTE")
                return route

    # Default fallback
    log("No domain match — defaulting to orchestrator_pro", "WARN")
    return ROUTING_TABLE["orchestration"]


def check_agent_active(agent_id: str, act_status: dict) -> bool:
    """Check if agent is ACTIVE or PLACEHOLDER via activation_status.json"""
    for tier_group in act_status.values():
        if isinstance(tier_group, dict) and agent_id in tier_group:
            return tier_group[agent_id].get("status") == "ACTIVE"
    return True  # assume active if not in registry


def dispatch_task(task: dict, route: dict, act_status: dict) -> dict:
    """Dispatch task to agent, fallback if PLACEHOLDER"""
    agent_id = route["agent"]

    # Use fallback if primary is PLACEHOLDER
    if not check_agent_active(agent_id, act_status):
        fallback = route.get("fallback", "orchestrator_pro")
        log(f"Agent {agent_id} is PLACEHOLDER → routing to fallback: {fallback}", "WARN")
        agent_id = fallback

    receipt = {
        "task_id":       task.get("task_id", f"T-{int(time.time())}"),
        "agent":         agent_id,
        "dept":          route["dept"],
        "tier":          route["tier"],
        "primary_skill": route["skill"],
        "status":        "DISPATCHED",
        "dispatched_at": now_iso(),
        "task_payload":  task,
    }

    # Write receipt to telemetry
    receipt_dir = RECEIPTS_DIR / agent_id
    receipt_dir.mkdir(parents=True, exist_ok=True)
    save_json(receipt_dir / f"{receipt['task_id']}.json", receipt)

    log(f"DISPATCHED {receipt['task_id']} → [{route['dept']}] {agent_id} | skill: {route['skill']}", "DISPATCH")
    return receipt


def update_hud() -> dict:
    """Update STATUS.json with live counts from filesystem"""
    status = load_json(STATUS_JSON)

    skill_count   = len([d for d in (ROOT/"ecosystem"/"skills").iterdir() if d.is_dir()])
    agent_count   = len([d for d in AGENTS_DIR.iterdir() if d.is_dir()]) if AGENTS_DIR.exists() else 0
    brain_agents  = len([f for f in (ROOT/"brain"/"agents").iterdir() if f.suffix == ".md"]) if (ROOT/"brain"/"agents").exists() else 0
    mcp_data      = load_json(ROOT / ".mcp.json")
    mcp_count     = len(mcp_data.get("mcpServers", {}))
    plugin_count  = len([d for d in PLUGINS_DIR.iterdir() if d.is_dir()]) if PLUGINS_DIR.exists() else 0
    route_count   = len(ROUTING_TABLE)
    dept_count    = len(DEPARTMENTS)

    status.update({
        "version":          "v3.1",
        "cycle":            11,
        "system":           "AI OS Corp",
        "updated":          now_iso(),
        "last_hud_update":  now_iso(),
        "skills":           skill_count,
        "agents":           agent_count,
        "brain_agent_profiles": brain_agents,
        "departments":      dept_count,
        "routing_rules":    route_count,
        "corp_cycle_status":"ACTIVE",
        "orchestrator":     "ONLINE",
        "v31_reconnect":    "COMPLETE",
        "kho": {
            **status.get("kho", {}),
            "skills":   {"total": skill_count,  "status": "OK"},
            "agents":   {"total": agent_count,  "status": "OK"},
            "mcp":      {"servers": mcp_count,  "status": "OK"},
            "plugins":  {"plugins": plugin_count,"status": "OK"},
        }
    })

    save_json(STATUS_JSON, status)
    log(f"HUD ✅ | skills={skill_count} | agents={agent_count}+{brain_agents}profiles | MCPs={mcp_count} | plugins={plugin_count} | routes={route_count} | depts={dept_count}", "OK")
    return status


def send_telegram_simple(msg: str) -> bool:
    """Fire-and-forget Telegram send (no deps)"""
    token = ENV.get("TELEGRAM_BOT_TOKEN", "")
    chat  = ENV.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat:
        log(f"Telegram skip (no credentials): {msg[:60]}", "WARN")
        return False
    try:
        payload = json.dumps({"chat_id": chat, "text": msg, "parse_mode": "Markdown"}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=payload, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=8): pass
        log("Telegram ✅ sent", "OK")
        return True
    except Exception as e:
        log(f"Telegram ❌ {e}", "ERR")
        return False


def run_cycle(verbose=True) -> dict:
    """Main orchestration cycle — 1 pass"""
    if verbose:
        print("=" * 65)
        print("  AI OS V3.1 ORCHESTRATOR — FULL EDITION")
        print(f"  Routing rules: {len(ROUTING_TABLE)} | Depts: {len(DEPARTMENTS)}")
        print("=" * 65)

    # 1. Update HUD
    status = update_hud()

    # 2. Load activation status
    act_status = load_json(ACT_STATUS)

    # 3. Read blackboard
    bb = load_json(BLACKBOARD)
    trigger = bb.get("handoff_trigger", "IDLE")
    log(f"Blackboard: trigger={trigger} | campaign={bb.get('active_campaign', 'none')}")

    # 4. Dispatch if READY
    result = {"status": "OK", "trigger": trigger, "hud": status}

    if trigger == "READY":
        task = bb.get("task_payload", {})
        route = route_task(task)
        receipt = dispatch_task(task, route, act_status)

        # Update blackboard
        bb["handoff_trigger"] = "IN_PROGRESS"
        bb["last_dispatch"] = receipt
        bb["blackboard_updated_at"] = now_iso()
        save_json(BLACKBOARD, bb)

        # [NEW] Dual-write: Publish to Event Bus
        _bus_publish(
            topic=route.get("dept", "SYSTEM"),
            payload={"task_id": receipt["task_id"], "agent": receipt["agent"], "skill": receipt["primary_skill"], "payload": task}
        )

        # [NEW] Save dispatch fact to LTM
        _ltm_save(
            f"Task {receipt['task_id']} dispatched to agent {receipt['agent']} (Dept: {receipt['dept']}, Skill: {receipt['primary_skill']})",
            agent_id="orchestrator"
        )

        send_telegram_simple(
            f"📤 *Task Dispatched*\n"
            f"→ Agent: `{receipt['agent']}`\n"
            f"→ Dept: `{receipt['dept']}` (Tier {receipt['tier']})\n"
            f"→ Skill: `{receipt['primary_skill']}`\n"
            f"→ Task: `{receipt['task_id']}`"
        )
        result["receipt"] = receipt

    elif trigger == "DONE":
        s = status
        send_telegram_simple(
            f"📊 *AI OS V3.1 — System Status*\n"
            f"• 🤖 Agents: `{s['agents']}` (+`{s['brain_agent_profiles']}` profiles)\n"
            f"• 🧠 Skills: `{s['skills']}`\n"
            f"• 🏢 Depts: `{s['departments']}`\n"
            f"• 🔀 Routes: `{s['routing_rules']}`\n"
            f"• 🔌 MCPs: `{s['kho']['mcp']['servers']}`\n"
            f"• 📦 Plugins: `{s['kho']['plugins']['plugins']}`\n"
            f"• ✅ Reconnect: `{s['v31_reconnect']}`"
        )
        log("System idle — status digest sent", "OK")

    if verbose:
        print("─" * 65)
        log("Orchestration cycle complete", "OK")

    return result


def list_routes():
    """Print full routing table for verification"""
    print(f"\n{'='*65}")
    print(f"  ROUTING TABLE — {len(ROUTING_TABLE)} rules | {len(DEPARTMENTS)} depts")
    print(f"{'='*65}")
    by_dept = {}
    for kw, r in ROUTING_TABLE.items():
        by_dept.setdefault(r['dept'], []).append((kw, r['agent'], r['tier']))
    for dept, entries in sorted(by_dept.items()):
        print(f"\n  [{dept}]")
        for kw, agent, tier in sorted(entries):
            print(f"    '{kw}' → {agent} (T{tier})")


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "once"

    if cmd == "once":
        result = run_cycle()
        print(json.dumps({"status": result["status"], "trigger": result["trigger"]}, indent=2))

    elif cmd == "routes":
        list_routes()

    elif cmd == "watch":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        log(f"Watch mode — polling every {interval}s | Ctrl+C to stop", "OK")
        while True:
            try:
                run_cycle(verbose=False)
            except KeyboardInterrupt:
                log("Orchestrator stopped", "WARN"); break
            except Exception as e:
                log(f"Cycle error: {e}", "ERR")
            time.sleep(interval)

    elif cmd == "route":
        # Test routing for a given domain
        domain = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "unknown"
        task = {"domain": domain, "task_id": "TEST-001", "title": domain}
        route = route_task(task)
        print(json.dumps(route, indent=2))

    else:
        print("Usage: python aios_orchestrator.py [once|routes|watch [sec]|route <domain>]")
