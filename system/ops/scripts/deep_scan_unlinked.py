import os
import yaml
import json

ROOT_DIR = os.environ.get("AOS_ROOT", ".")
DEPT_DIR = os.path.join(ROOT_DIR, "brain", "corp", "departments")

AGENT_DIR = os.path.join(ROOT_DIR, "brain", "agents")
WORKFLOW_DIR = os.path.join(ROOT_DIR, "system", "ops", "workflows")
SKILL_DIR = os.path.join(ROOT_DIR, "ecosystem", "skills")
PLUGIN_DIR = os.path.join(ROOT_DIR, "ecosystem", "plugins")
SUBAGENT_DIR = os.path.join(ROOT_DIR, "ecosystem", "subagents")

def load_all_depts():
    depts = []
    if not os.path.exists(DEPT_DIR): return depts
    for f in os.listdir(DEPT_DIR):
        if f.endswith(".yaml"):
            try:
                with open(os.path.join(DEPT_DIR, f), 'r', encoding='utf-8') as yml:
                    d = yaml.safe_load(yml)
                    if d: depts.append(d)
            except:
                pass
    return depts

def find_unmapped(depts):
    # 1. Gather mapped items from depts
    mapped_agents = set()
    mapped_skills = set()
    mapped_plugins = set()

    for d in depts:
        # nested structure
        if "department" in d:
            w = d.get("workforce", [])
            tc = d.get("tools_and_capabilities", {})
            mapped_agents.update([x.get("agent_id", "") for x in w if isinstance(x, dict)])
            mapped_skills.update(tc.get("skills", []))
            mapped_plugins.update(tc.get("plugins", []))
            # Also head agent
            head = d.get("leadership", {}).get("manager", "")
            if head: mapped_agents.add(head)

    # Normalize
    mapped_agents = {a.lower().replace(".md", "") for a in mapped_agents}
    mapped_skills = {s.lower() for s in mapped_skills}
    mapped_plugins = {p.lower() for p in mapped_plugins}

    # 1. Unlinked Agents
    unlinked_agents = []
    if os.path.exists(AGENT_DIR):
        for f in os.listdir(AGENT_DIR):
            if f.endswith(".md"):
                aname = f.replace(".md", "").lower()
                if aname not in mapped_agents:
                    unlinked_agents.append(f)

    # 2. Unlinked Workflows
    unlinked_workflows = []
    if os.path.exists(WORKFLOW_DIR):
        for f in os.listdir(WORKFLOW_DIR):
            if f.endswith(".md"):
                try:
                    with open(os.path.join(WORKFLOW_DIR, f), "r", encoding="utf-8") as wf:
                        content = wf.read(1000)
                        if "# Department:" not in content:
                            unlinked_workflows.append(f)
                except:
                    pass

    # 3. Unlinked Skills (Folders in ecosystem/skills that aren't mapped in depts)
    unlinked_skills = []
    if os.path.exists(SKILL_DIR):
        for s in os.listdir(SKILL_DIR):
            s_path = os.path.join(SKILL_DIR, s)
            if os.path.isdir(s_path) and s.lower() not in mapped_skills:
                unlinked_skills.append(s)

    # 4. Unlinked Plugins / MCPs
    unlinked_plugins = []
    if os.path.exists(PLUGIN_DIR):
        for p in os.listdir(PLUGIN_DIR):
            if os.path.isdir(os.path.join(PLUGIN_DIR, p)) and p.lower() not in mapped_plugins:
                unlinked_plugins.append(p)

    # 5. Subagents (Are they mapped in depts? Probably not)
    unlinked_subagents = []
    if os.path.exists(SUBAGENT_DIR):
        for sa in os.listdir(SUBAGENT_DIR):
            if os.path.isdir(os.path.join(SUBAGENT_DIR, sa)):
                unlinked_subagents.append(sa)

    print("====================================")
    print("DEEP SCAN & RECONCILIATION REPORT")
    print("====================================")
    print(f"Total Agents Unlinked: {len(unlinked_agents)}")
    if unlinked_agents: print(" -> " + ", ".join(unlinked_agents[:10]) + ("..." if len(unlinked_agents) > 10 else ""))

    print(f"\nTotal Workflows Unlinked: {len(unlinked_workflows)}")
    if unlinked_workflows: print(" -> " + ", ".join(unlinked_workflows))

    print(f"\nTotal Skills Unlinked (Not granted to any Dept): {len(unlinked_skills)}")
    if unlinked_skills: print(" -> " + ", ".join(unlinked_skills))

    print(f"\nTotal Plugins/MCPs Unlinked (Not granted to any Dept): {len(unlinked_plugins)}")
    if unlinked_plugins: print(" -> " + ", ".join(unlinked_plugins))

    print(f"\nTotal Subagents Unlinked (Not owned by any Dept): {len(unlinked_subagents)}")
    if unlinked_subagents: print(" -> " + ", ".join(unlinked_subagents))

if __name__ == "__main__":
    depts = load_all_depts()
    find_unmapped(depts)

