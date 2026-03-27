import os
import yaml

ROOT_DIR = os.environ.get("AOS_ROOT", ".")
DEPT_DIR = os.path.join(ROOT_DIR, "brain", "corp", "departments")
SKILL_DIR = os.path.join(ROOT_DIR, "ecosystem", "skills")
PLUGIN_DIR = os.path.join(ROOT_DIR, "ecosystem", "plugins")
SUBAGENT_DIR = os.path.join(ROOT_DIR, "ecosystem", "subagents")

DEPT_KEYWORDS_WEAPONS = {
    "engineering": ["vercel", "git", "repo", "db", "sql", "port", "dev", "tech", "context7", "spec", "architect"],
    "qa_testing": ["shield", "security", "leak", "test", "vet"],
    "marketing": ["social", "seo", "ads", "market"],
    "hr_people": ["agentune", "profile", "review"],
    "operations": ["manager", "sync", "daemon", "mq", "continuous"],
    "registry_capability": ["search", "knowledge", "doc", "registry", "framework-standards"],
    "monitoring_inspection": ["monitor", "health", "alert"],
    "content_intake": ["fetch", "notebook", "ingest", "web"],
    "strategy": ["context", "learn", "retro"]
}

def guess_dept_for_weapon(weapon_name):
    lower_name = weapon_name.lower()
    for dept, keywords in DEPT_KEYWORDS_WEAPONS.items():
        if any(kw in lower_name for kw in keywords):
            return dept
    return "engineering" # Default for technical stuff

def main():
    if not os.path.exists(DEPT_DIR): return

    # Gather unlinked skills
    skills = []
    if os.path.exists(SKILL_DIR):
        skills = [s for s in os.listdir(SKILL_DIR) if os.path.isdir(os.path.join(SKILL_DIR, s))]

    plugins = []
    if os.path.exists(PLUGIN_DIR):
        plugins = [p for p in os.listdir(PLUGIN_DIR) if os.path.isdir(os.path.join(PLUGIN_DIR, p))]

    subagents = []
    if os.path.exists(SUBAGENT_DIR):
        subagents = [sa for sa in os.listdir(SUBAGENT_DIR) if os.path.isdir(os.path.join(SUBAGENT_DIR, sa))]

    # Build mapping
    distributions = {d: {"skills": [], "plugins": [], "subagents": []} for d in os.listdir(DEPT_DIR) if d.endswith(".yaml")}

    for s in skills:
        dept = f"{guess_dept_for_weapon(s)}.yaml"
        if dept in distributions: distributions[dept]["skills"].append(s)

    for p in plugins:
        dept = f"{guess_dept_for_weapon(p)}.yaml"
        if dept in distributions: distributions[dept]["plugins"].append(p)

    for sa in subagents:
        dept = f"{guess_dept_for_weapon(sa)}.yaml"
        if dept in distributions: distributions[dept]["subagents"].append(sa)

    # Write to files
    updated = 0
    for dept_file, data in distributions.items():
        if not data["skills"] and not data["plugins"] and not data["subagents"]:
            continue

        filepath = os.path.join(DEPT_DIR, dept_file)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                dept_data = yaml.safe_load(f)

            if "department" in dept_data:
                # Nested
                if "tools_and_capabilities" not in dept_data:
                    dept_data["tools_and_capabilities"] = {"skills": [], "plugins": [], "subagents": []}

                # Make sure lists exist
                if "skills" not in dept_data["tools_and_capabilities"]: dept_data["tools_and_capabilities"]["skills"] = []
                if "plugins" not in dept_data["tools_and_capabilities"]: dept_data["tools_and_capabilities"]["plugins"] = []
                if "subagents" not in dept_data["tools_and_capabilities"]: dept_data["tools_and_capabilities"]["subagents"] = []

                # Append new unique
                existing_s = set(dept_data["tools_and_capabilities"]["skills"])
                existing_p = set(dept_data["tools_and_capabilities"]["plugins"])
                existing_sa = set(dept_data["tools_and_capabilities"].get("subagents", []))

                dept_data["tools_and_capabilities"]["skills"].extend([i for i in data["skills"] if i not in existing_s])
                dept_data["tools_and_capabilities"]["plugins"].extend([i for i in data["plugins"] if i not in existing_p])
                dept_data["tools_and_capabilities"]["subagents"].extend([i for i in data["subagents"] if i not in existing_sa])
            else:
                # Flat old format
                if "tools_available" not in dept_data: dept_data["tools_available"] = []
                existing_t = set(dept_data["tools_available"])
                dept_data["tools_available"].extend([i for i in data["skills"] + data["plugins"] + data["subagents"] if i not in existing_t])

            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(dept_data, f, sort_keys=False, allow_unicode=True)
            updated += 1
            print(f"Equipped {dept_file}: +{len(data['skills'])} skills, +{len(data['plugins'])} plugins, +{len(data['subagents'])} subagents")
        except Exception as e:
            print(f"Error on {dept_file}: {e}")

    print(f"Successfully modified {updated} departments.")

if __name__ == "__main__":
    main()

