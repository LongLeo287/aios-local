#!/usr/bin/env python3
"""Update FAST_INDEX.json and SKILL_REGISTRY.json with 12 newly processed repos."""
import json
import os
from datetime import datetime

AIOS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
fi_path = os.path.join(AIOS, "brain", "shared-context", "FAST_INDEX.json")
sr_path = os.path.join(AIOS, "brain", "shared-context", "SKILL_REGISTRY.json")

# ── FAST_INDEX ──────────────────────────────────────────────────────
with open(fi_path, "r", encoding="utf-8") as f:
    fi = json.load(f)

fi.setdefault("keyword", {}).update({
    "lenis":          {"path": "plugins/lenis/SKILL.md",           "tier": 2, "dept": "engineering",          "desc": "Smooth scroll animation library"},
    "opensandbox":    {"path": "plugins/OpenSandbox/SKILL.md",     "tier": 2, "dept": "engineering",          "desc": "Isolated code sandbox CLI"},
    "sandbox":        {"path": "plugins/OpenSandbox/SKILL.md",     "tier": 2, "dept": "engineering",          "desc": "Isolated code sandbox CLI"},
    "mcp":            {"path": "tools/mcp/SKILL.md",               "tier": 1, "dept": "registry_capability", "desc": "Notebook MCP server"},
    "core_intel":     {"path": "tools/core_intel/SKILL.md",        "tier": 1, "dept": "monitoring",          "desc": "CIV metrics analytics"},
    "civ_metrics":    {"path": "tools/core_intel/SKILL.md",        "tier": 1, "dept": "monitoring",          "desc": "CIV score computation"},
    "gitnexus_web":   {"path": "tools/gitnexus-web/SKILL.md",      "tier": 2, "dept": "engineering",         "desc": "GitNexus browser UI"},
    "agentskills":    {"path": "brain/skills/agentskills-spec/SKILL.md", "tier": 1, "dept": "registry_capability", "desc": "Anthropic agentskills spec"},
    "cybersecurity":  {"path": "brain/skills/cybersecurity/SKILL.md", "tier": 2, "dept": "security_grc",     "desc": "Web security skills"},
    "domains":        {"path": "brain/skills/domains/SKILL.md",    "tier": 2, "dept": "engineering",          "desc": "Multi-domain skill library"},
    "ui_ux_pro":      {"path": "brain/skills/ui-ux-pro-max/SKILL.md", "tier": 2, "dept": "engineering",      "desc": "Advanced UI/UX skill scripts"},
    "vibe_coder":     {"path": "brain/skills/antigravity/SKILL.md","tier": 2, "dept": "rd",                  "desc": "Vibe coding skill"},
    "scroll":         {"path": "plugins/lenis/SKILL.md",           "tier": 2, "dept": "engineering",          "desc": "Smooth scroll animation"},
})

fi.setdefault("domain", {}).update({
    "scroll_animation":  {"path": "plugins/lenis/SKILL.md",        "tier": 2, "dept": "engineering"},
    "sandbox_execution": {"path": "plugins/OpenSandbox/SKILL.md",  "tier": 2, "dept": "engineering"},
    "mcp_protocol":      {"path": "tools/mcp/SKILL.md",            "tier": 1, "dept": "registry_capability"},
    "civ_analytics":     {"path": "tools/core_intel/SKILL.md",     "tier": 1, "dept": "monitoring"},
    "web_security":      {"path": "brain/skills/cybersecurity/SKILL.md", "tier": 2, "dept": "security_grc"},
    "domain_skills":     {"path": "brain/skills/domains/SKILL.md", "tier": 2, "dept": "engineering"},
    "ui_ux_advanced":    {"path": "brain/skills/ui-ux-pro-max/SKILL.md", "tier": 2, "dept": "engineering"},
})

# paths is a dict {name: path_string}
fi.setdefault("paths", {}).update({
    "lenis":             "plugins/lenis/SKILL.md",
    "opensandbox":       "plugins/OpenSandbox/SKILL.md",
    "_archive":          "plugins/_archive/SKILL.md",
    "notebook_mcp":      "tools/mcp/SKILL.md",
    "core_intel":        "tools/core_intel/SKILL.md",
    "gitnexus_web":      "tools/gitnexus-web/SKILL.md",
    "agentskills_spec":  "brain/skills/agentskills-spec/SKILL.md",
    "antigravity_sk":    "brain/skills/antigravity/SKILL.md",
    "cybersecurity":     "brain/skills/cybersecurity/SKILL.md",
    "domains":           "brain/skills/domains/SKILL.md",
    "experimental":      "brain/skills/experimental/SKILL.md",
    "ui_ux":             "brain/skills/ui-ux/SKILL.md",
    "ui_ux_pro_max":     "brain/skills/ui-ux-pro-max/SKILL.md",
})

fi["_meta"]["built"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
fi["_meta"]["total_paths"] = len(fi["paths"])
fi["_meta"]["version"] = "1.2"

with open(fi_path, "w", encoding="utf-8") as f:
    json.dump(fi, f, ensure_ascii=False, separators=(",", ":"))

total_kw = len(fi.get("keyword", {}))
total_p  = len(fi["paths"])
print(f"FAST_INDEX v1.2: {total_p} paths, {total_kw} keywords")

# ── SKILL_REGISTRY ──────────────────────────────────────────────────
with open(sr_path, "r", encoding="utf-8") as f:
    sr = json.load(f)

if isinstance(sr, dict):
    key = "skills" if "skills" in sr else "entries"
    entries = sr.get(key, [])
else:
    entries = sr
    key = None

existing = {e.get("id") or e.get("name") for e in entries}

new_entries = [
    {"id": "lenis",             "name": "Lenis Smooth Scroll",       "path": "plugins/lenis/SKILL.md",                    "tier": 2, "category": "ui-animation",   "dept": "engineering",          "status": "active"},
    {"id": "opensandbox",       "name": "OpenSandbox",               "path": "plugins/OpenSandbox/SKILL.md",              "tier": 2, "category": "dev-tooling",    "dept": "engineering",          "status": "active"},
    {"id": "notebook_mcp",      "name": "Notebook MCP Server",       "path": "tools/mcp/SKILL.md",                        "tier": 1, "category": "mcp",            "dept": "registry_capability",  "status": "active"},
    {"id": "core_intel",        "name": "Core Intel CIV Metrics",    "path": "tools/core_intel/SKILL.md",                 "tier": 1, "category": "analytics",      "dept": "monitoring",           "status": "active"},
    {"id": "gitnexus_web",      "name": "GitNexus Web UI",           "path": "tools/gitnexus-web/SKILL.md",               "tier": 2, "category": "dev-tooling",    "dept": "engineering",          "status": "active"},
    {"id": "agentskills_spec",  "name": "AgentSkills Specification", "path": "brain/skills/agentskills-spec/SKILL.md",    "tier": 1, "category": "specification",  "dept": "registry_capability",  "status": "active"},
    {"id": "antigravity_skills","name": "Antigravity Agent Skills",  "path": "brain/skills/antigravity/SKILL.md",         "tier": 2, "category": "ai-agent",       "dept": "rd",                   "status": "active"},
    {"id": "cybersecurity",     "name": "Cybersecurity Skills",      "path": "brain/skills/cybersecurity/SKILL.md",       "tier": 2, "category": "security",       "dept": "security_grc",         "status": "active"},
    {"id": "domain_skills",     "name": "Domain Skills Library",     "path": "brain/skills/domains/SKILL.md",             "tier": 2, "category": "knowledge",      "dept": "engineering",          "status": "active"},
    {"id": "experimental",      "name": "Experimental Skills",       "path": "brain/skills/experimental/SKILL.md",        "tier": 3, "category": "experimental",   "dept": "rd",                   "status": "draft"},
    {"id": "ui_ux_skills",      "name": "UI-UX Skills",              "path": "brain/skills/ui-ux/SKILL.md",               "tier": 2, "category": "design",         "dept": "engineering",          "status": "active"},
    {"id": "ui_ux_pro_max",     "name": "UI-UX Pro Max",             "path": "brain/skills/ui-ux-pro-max/SKILL.md",       "tier": 2, "category": "design",         "dept": "engineering",          "status": "active"},
    {"id": "archive_legacy",    "name": "Archive (Legacy)",          "path": "plugins/_archive/SKILL.md",                 "tier": 5, "category": "archive",        "dept": "legacy",               "status": "deprecated"},
]

added = 0
for e in new_entries:
    if e["id"] not in existing:
        entries.append(e)
        existing.add(e["id"])
        added += 1

if key:
    sr[key] = entries
    sr["count"] = len(entries)
    sr["updated"] = datetime.now().isoformat()
else:
    sr = entries

with open(sr_path, "w", encoding="utf-8") as f:
    json.dump(sr, f, ensure_ascii=False, indent=2)

print(f"SKILL_REGISTRY: +{added} new => {len(entries)} total")
print("DONE!")
