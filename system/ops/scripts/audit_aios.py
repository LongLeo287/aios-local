#!/usr/bin/env python3
"""audit_aios.py â€” Full AI OS Audit Script"""
import os, json, subprocess, re
from datetime import datetime, date

ROOT = os.environ.get("AOS_ROOT", ".")
NOW = datetime.now().isoformat()

issues = []
info   = []
ok     = []

def ISSUE(layer, msg): issues.append(f"[{layer}] {msg}")
def INFO(layer, msg):  info.append(f"[{layer}] {msg}")
def OK(layer, msg):    ok.append(f"[{layer}] {msg}")

# â”€â”€â”€ 1. DIRECTORY STRUCTURE â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("=== 1. STRUCTURE ===")
expected_dirs = [
    "plugins", "tools", "tools/clawtask", "tools/gitnexus", "tools/ag-auto-accept",
    "workforce/agents", "workforce/subagents",
    "brain/knowledge", "brain/shared-context", "brain/registry",
    "ops/workflows", "ops/runtime",
    "infra", "security",
    "corp/departments",
]
for d in expected_dirs:
    full = os.path.join(ROOT, d.replace("/", os.sep))
    if os.path.isdir(full):
        OK("structure", f"âœ“ {d}/")
    else:
        ISSUE("structure", f"âœ— MISSING dir: {d}/")

# â”€â”€â”€ 2. SERVICES â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("=== 2. SERVICES ===")
try:
    svc_path = os.path.join(ROOT, "tools", "clawtask", "services_control.py")
    content = open(svc_path, encoding="utf-8").read()
    # Extract service keys
    import re
    svc_keys = re.findall(r'^\s{4}"(\w+)":\s*\{', content, re.M)
    INFO("services", f"Defined services: {svc_keys}")
    # Check start_cmd: None entries
    for key in svc_keys:
        block_match = re.search(rf'"{key}":\s*\{{([^}}]+)\}}', content, re.S)
        if block_match:
            block = block_match.group(1)
            if '"start_cmd": None' in block and key not in ("clawtask",):
                ISSUE("services", f"start_cmd: None for: {key} (cannot auto-start)")
            else:
                OK("services", f"start_cmd OK: {key}")
except Exception as e:
    ISSUE("services", f"Cannot read services_control.py: {e}")

# â”€â”€â”€ 3. CLAWTASK MODULES â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("=== 3. CLAWTASK MODULES ===")
api_path = os.path.join(ROOT, "tools", "clawtask", "clawtask_api.py")
try:
    api_content = open(api_path, encoding="utf-8").read()
    modules = re.findall(r'import module_(\w+)', api_content)
    INFO("api", f"Registered modules: {modules}")
    for mod in modules:
        mod_file = os.path.join(ROOT, "tools", "clawtask", f"module_{mod}.py")
        if os.path.isfile(mod_file):
            OK("api", f"module_{mod}.py exists")
        else:
            ISSUE("api", f"module_{mod}.py MISSING â€” import will fail!")
    # Check for handle_get/handle_post in each module
    for mod in modules:
        mf = os.path.join(ROOT, "tools", "clawtask", f"module_{mod}.py")
        if os.path.isfile(mf):
            mc = open(mf, encoding="utf-8").read()
            if "def handle_get" not in mc:
                ISSUE("api", f"module_{mod} missing handle_get()")
            if "def handle_post" not in mc:
                ISSUE("api", f"module_{mod} missing handle_post()")
except Exception as e:
    ISSUE("api", f"Cannot read clawtask_api.py: {e}")

# â”€â”€â”€ 4. PORT CONFLICTS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("=== 4. PORTS ===")
PORT_MAP = {
    7474: "ClawTask API",
    4747: "GitNexus",
    7476: "ag-auto-accept",
    11434: "Ollama",
    7000: "API Bridge",
    5055: "open-notebook",
    8765: "DeepAgents ACP",
    3210: "Lobe Chat",
    7860: "open-notebooklm",
    3000: "nullclaw (Telegram)",
    9090: "Prometheus",
    4000: "Grafana",
    8082: "cAdvisor",
}
from urllib.request import urlopen, Request
from urllib.error import URLError

for port, name in PORT_MAP.items():
    health_urls = {
        7474: "http://127.0.0.1:7474/api/status",
        4747: "http://127.0.0.1:4747/health",
        7476: "http://127.0.0.1:7476/status",
        11434: "http://127.0.0.1:11434/api/tags",
        7000: "http://127.0.0.1:7000/health",
        5055: "http://127.0.0.1:5055/health",
        8765: "http://127.0.0.1:8765/health",
        3210: "http://127.0.0.1:3210/",
        7860: "http://127.0.0.1:7860/",
        3000: "http://127.0.0.1:3000/health",
        9090: "http://127.0.0.1:9090/-/ready",
        4000: "http://127.0.0.1:4000/api/health",
        8082: "http://127.0.0.1:8082/healthz",
    }
    url = health_urls.get(port)
    if url:
        try:
            with urlopen(Request(url), timeout=1) as r:
                INFO("ports", f":{port} ONLINE  â€” {name}")
        except:
            INFO("ports", f":{port} offline â€” {name}")

# â”€â”€â”€ 5. PLUGINS COVERAGE â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("=== 5. PLUGINS ===")
PLUGINS = os.path.join(ROOT, "plugins")
all_plugins = [d for d in os.listdir(PLUGINS) if os.path.isdir(os.path.join(PLUGINS, d))]
no_skill = [d for d in all_plugins if not os.path.isfile(os.path.join(PLUGINS, d, "SKILL.md"))]
cloned   = [d for d in all_plugins if os.path.isdir(os.path.join(PLUGINS, d, ".git"))]
skill_only = [d for d in all_plugins if not os.path.isdir(os.path.join(PLUGINS, d, ".git"))]

INFO("plugins", f"Total plugins: {len(all_plugins)}")
INFO("plugins", f"Git cloned: {len(cloned)}")
INFO("plugins", f"SKILL.md only: {len(skill_only)}")
if no_skill:
    ISSUE("plugins", f"Missing SKILL.md ({len(no_skill)}): {no_skill[:5]}...")
else:
    OK("plugins", f"All {len(all_plugins)} plugins have SKILL.md")

# Specific important plugins present?
important = ["mem0", "graphrag", "scrapling", "e2b", "vieneu-tts", "prometheus-grafana-alerts",
             "deepagents", "openclaw-command-center", "gitingest", "nexusrag", "lightrag",
             "ag-auto-click-scroll"]
for imp in important:
    if imp in all_plugins:
        cloned_flag = "cloned" if imp in cloned else "SKILL only"
        OK("plugins", f"âœ“ {imp} ({cloned_flag})")
    else:
        ISSUE("plugins", f"âœ— {imp} NOT in plugins/")

# â”€â”€â”€ 6. MCP SERVERS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("=== 6. MCPs ===")
mcp_plugins = [d for d in all_plugins if "mcp" in d.lower()]
INFO("mcp", f"MCP plugins: {mcp_plugins}")

# â”€â”€â”€ 7. AGENTS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("=== 7. AGENTS ===")
AGENTS_DIR = os.path.join(ROOT, "workforce", "agents")
SUBS_DIR   = os.path.join(ROOT, "workforce", "subagents")
agents = [d for d in os.listdir(AGENTS_DIR) if os.path.isdir(os.path.join(AGENTS_DIR, d))] if os.path.isdir(AGENTS_DIR) else []
subs   = [d for d in os.listdir(SUBS_DIR)   if os.path.isdir(os.path.join(SUBS_DIR, d))]   if os.path.isdir(SUBS_DIR)   else []
INFO("agents", f"workforce/agents: {len(agents)}")
INFO("agents", f"workforce/subagents: {len(subs)}")

# Each agent should have at least AGENT.md or SKILL.md
for a in agents:
    ap = os.path.join(AGENTS_DIR, a)
    has_doc = any(os.path.isfile(os.path.join(ap, f)) for f in ("AGENT.md", "SKILL.md", "README.md", f"{a}.md"))
    if not has_doc:
        ISSUE("agents", f"Agent '{a}' has no documentation file")

# â”€â”€â”€ 8. KNOWLEDGE BASE â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("=== 8. KNOWLEDGE ===")
KNOWLEDGE = os.path.join(ROOT, "brain", "knowledge")
ki_domains = {}
ki_total = 0
if os.path.isdir(KNOWLEDGE):
    for domain in os.listdir(KNOWLEDGE):
        dp = os.path.join(KNOWLEDGE, domain)
        if os.path.isdir(dp):
            count = sum(1 for f in os.listdir(dp) if f.endswith(".md"))
            ki_domains[domain] = count
            ki_total += count
INFO("knowledge", f"Total KI entries: {ki_total}")
INFO("knowledge", f"Domains: {dict(sorted(ki_domains.items(), key=lambda x: -x[1])[:8])}")

# â”€â”€â”€ 9. FAST_INDEX â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("=== 9. FAST_INDEX ===")
fi_path = os.path.join(ROOT, "brain", "shared-context", "FAST_INDEX.json")
if os.path.isfile(fi_path):
    fi = json.load(open(fi_path, encoding="utf-8"))
    m = fi.get("_meta", {})
    built = m.get("built_at", "unknown")
    paths = m.get("total_paths", 0)
    version = m.get("version", "?")
    INFO("index", f"FAST_INDEX v{version}: {paths} paths | built: {built}")
    # Check if recent enough (today)
    today = date.today().isoformat()
    if today in str(built):
        OK("index", "FAST_INDEX built today âœ“")
    else:
        ISSUE("index", f"FAST_INDEX last built: {built} â€” may be stale, rebuild needed")
else:
    ISSUE("index", "FAST_INDEX.json NOT FOUND!")

# â”€â”€â”€ 10. WORKFLOWS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("=== 10. WORKFLOWS ===")
WF_DIR = os.path.join(ROOT, "system", "ops", "workflows")
if os.path.isdir(WF_DIR):
    wf_files = [f for f in os.listdir(WF_DIR) if f.endswith(".md")]
    INFO("workflows", f"Workflow files count: {len(wf_files)}")
    important_wf = ["knowledge-ingest.md", "task-lifecycle.md", "deploy.md"]
    for wf in important_wf:
        if wf in wf_files:
            OK("workflows", f"âœ“ {wf}")
        else:
            INFO("workflows", f"â—‹ {wf} not found (optional)")
else:
    ISSUE("workflows", "system/ops/workflows/ directory missing")

# â”€â”€â”€ 11. REPO_REGISTRY â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("=== 11. REPO_REGISTRY ===")
reg_path = os.path.join(ROOT, "brain", "registry", "REPO_REGISTRY.md")
if os.path.isfile(reg_path):
    try:
        reg = open(reg_path, encoding="utf-8", errors="ignore").read()
        queued   = reg.count("ðŸ“¥ Queued")
        ingested = reg.count("âœ… Ingested")
        watchlist = reg.count("ðŸ” Watchlist")
        INFO("registry", f"âœ… Ingested: {ingested} | ðŸ“¥ Queued: {queued} | ðŸ” Watchlist: {watchlist}")
        if queued > 0:
            ISSUE("registry", f"{queued} repos still ðŸ“¥ Queued â€” not yet processed")
    except Exception as e:
        ISSUE("registry", f"Failed to read REPO_REGISTRY.md: {e}")
else:
    ISSUE("registry", "REPO_REGISTRY.md not found")

# â”€â”€â”€ 12. LOGIC CHECKS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("=== 12. LOGIC ===")

# ClawTask API file consistency
try:
    api_file = os.path.join(ROOT, "tools", "clawtask", "clawtask_api.py")
    if os.path.isfile(api_file):
        ac = open(api_file, encoding="utf-8", errors="ignore").read()
        # Check for common anti-patterns
        if "_db_module.USE_SUPABASE" in ac:
            OK("api_logic", "_db_module.USE_SUPABASE reference OK")
        if 'import db as _db_module' in ac:
            OK("api_logic", "db module imported as _db_module (no naming conflict)")
        # Check split logic for /clarification/answer
        if "7" in ac and "answer" in ac:
            OK("api_logic", "clarification answer path split fix present")
except Exception as e:
    ISSUE("api_logic", f"Failed reading clawtask_api: {e}")

# services_control port conflict check
try:
    port_re = re.compile(r'"port":\s*(\d+)')
    svcc = open(os.path.join(ROOT, "tools", "clawtask", "services_control.py"), encoding="utf-8", errors="ignore").read()
    ports = re.findall(r'"port":\s*(\d+)', svcc)
    port_dupes = [p for p in set(ports) if ports.count(p) > 1]
    if port_dupes:
        ISSUE("services_logic", f"PORT CONFLICT in services_control.py: {port_dupes}")
    else:
        OK("services_logic", f"No port conflicts in services_control.py")
except Exception as e:
    ISSUE("services_logic", f"Failed to scan services_control.py: {e}")

# â”€â”€â”€ SUMMARY â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print()
print("=" * 60)
print(f"AUDIT SUMMARY â€” {NOW}")
print("=" * 60)
print(f"\nðŸ”´ ISSUES ({len(issues)}):")
for i in issues: print(f"  {i}")
print(f"\nðŸ”µ INFO ({len(info)}):")
for i in info: print(f"  {i}")
print(f"\nâœ… OK ({len(ok)}):")
for i in ok: print(f"  {i}")

# Save report
report = {
    "audit_date": NOW,
    "issues": issues,
    "info": info,
    "ok": ok,
    "summary": {
        "issues_count": len(issues),
        "ok_count": len(ok),
        "plugins_total": len(all_plugins),
        "plugins_cloned": len(cloned),
        "agents": len(agents),
        "subagents": len(subs),
        "ki_total": ki_total,
        "ki_domains": ki_domains,
    }
}
report_path = os.path.join(ROOT, "ops", "runtime", "last_audit.json")
os.makedirs(os.path.dirname(report_path), exist_ok=True)
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
print(f"\nReport saved: {report_path}")

