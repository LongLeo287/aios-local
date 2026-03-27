import os
import yaml

DEPT_DIR = r"<AI_OS_ROOT>\brain\corp\departments"
AGENT_DIR = r"<AI_OS_ROOT>\brain\agents"

# Base mappings for department keywords to guess agent attribution
DEPT_KEYWORDS = {
    "engineering": ["backend", "frontend", "devops", "sre", "software-", "database", "netops", "sysadmin", "it-manager"],
    "qa_testing": ["qa", "tester", "superpowers-agent", "strix", "pentest", "security-engineer", "security-auditor"],
    "marketing": ["market", "growth", "seo", "social", "ads", "affiliate", "content-agent"],
    "hr_people": ["hr", "payroll", "recruiter", "trainer", "curriculum"],
    "finance": ["budget", "invoice", "cost-manager", "finance"],
    "operations": ["ops", "scrum", "pmo", "project", "execution", "asset"],
    "legal": ["legal", "contract", "compliance", "gdpr", "ip-agent"],
    "registry_capability": ["registry", "knowledge", "archivist", "library", "doc-parser"],
    "strategy": ["product", "roadmap", "cognitive", "data", "report", "analyst", "evaluator"],
    "support": ["support", "faq", "customer", "reception", "incident", "feedback", "intake-greeter", "client"],
    "monitoring_inspection": ["monitor", "health", "alert", "log", "port-checker"],
    "rd": ["rd", "experiment", "research", "innovate", "ai-ml"],
    "content_intake": ["intake-", "repo-fetcher", "ingest", "web-crawler"],
    "content_review": ["review", "content-validator", "formatter", "classifier"]
}

def guess_dept_for_agent(agent_name):
    lower_name = agent_name.lower()
    for dept, keywords in DEPT_KEYWORDS.items():
        if any(kw in lower_name for kw in keywords):
            return dept
    return "legacy" # Default if unfound

def main():
    if not os.path.exists(DEPT_DIR) or not os.path.exists(AGENT_DIR):
        print("Missing directories!")
        return

    # 1. Get all departments (folders)
    departments = [d for d in os.listdir(DEPT_DIR) if os.path.isdir(os.path.join(DEPT_DIR, d))]

    # 2. Get all agents
    agents = []
    for root, dirs, files in os.walk(AGENT_DIR):
        for f in files:
            if f.endswith(".md"):
                agents.append(f.replace(".md", ""))

    print(f"Found {len(departments)} departments and {len(agents)} agents.")

    # 3. Map agents
    dept_to_agents = {d: [] for d in departments}

    for agent in agents:
        dept = guess_dept_for_agent(agent)
        if dept not in dept_to_agents:
            dept = "legacy"
        dept_to_agents[dept].append(agent)

    # 4. Generate YAMLs
    created = 0
    updated = 0

    for dept in departments:
        yaml_path = os.path.join(DEPT_DIR, f"{dept}.yaml")

        # Base structure
        data = {
            "department": {
                "id": dept,
                "name": dept.upper().replace("_", " "),
                "active": True
            },
            "leadership": {
                "manager": f"{dept}-lead-agent",
                "reports_to": "ceo-agent"
            },
            "workforce": [
                {
                    "agent_id": agent,
                    "role": f"Worker for {dept}",
                    "access_level": "standard",
                    "status": "active"
                } for agent in dept_to_agents[dept]
            ],
            "kpi_targets": f"brain/corp/kpi_targets.yaml#{dept}",
            "tools_and_capabilities": {
                "skills": ["neural_navigator", "sequential-thinking"],
                "plugins": []
            },
            "outputs": [
                {
                    "artifact": f"{dept}_reports",
                    "consumer": "strategy"
                }
            ]
        }

        # If exists, we just update workforce, otherwise create
        if os.path.exists(yaml_path):
            with open(yaml_path, 'r', encoding='utf-8') as f:
                try:
                    existing = yaml.safe_load(f)
                    if existing and "workforce" in existing:
                        # Append new ones, avoid duplicate
                        existing_agents = [w.get("agent_id") for w in existing.get("workforce", [])]
                        for a in dept_to_agents[dept]:
                            if a not in existing_agents:
                                existing["workforce"].append({
                                    "agent_id": a,
                                    "role": "Auto-mapped worker",
                                    "access_level": "standard",
                                    "status": "active"
                                })
                        data = existing
                        updated += 1
                except:
                    pass
        else:
            created += 1

        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, sort_keys=False, allow_unicode=True)

    print(f"Successfully generated {created} new YAMLs and updated {updated} existing ones.")

if __name__ == "__main__":
    main()
