import os
import yaml
from datetime import datetime

DEPT_DIR = r"<AI_OS_ROOT>\brain\corp\departments"
REGISTRY_DIR = r"<AI_OS_ROOT>\system\registry"
OUT_YAML = os.path.join(REGISTRY_DIR, "ORG_GRAPH.yaml")
OUT_TXT = os.path.join(REGISTRY_DIR, "ORG_GRAPH_NARRATIVE.txt")

def process_department(filepath):
    """Parses a department YAML file and extracts graph edges/narrative."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

    if not data:
        return None

    # Support nested format (from new generator)
    if "department" in data:
        dept_id = data["department"].get("id", "unknown")
        display_name = data["department"].get("name", dept_id)
        head_agent = data.get("leadership", {}).get("manager", "none")
        reports_to = data.get("leadership", {}).get("reports_to", "none")
        workers = data.get("workforce", [])
        tools = data.get("tools_and_capabilities", {}).get("skills", []) + data.get("tools_and_capabilities", {}).get("plugins", [])
        kpi_ref = data.get("kpi_targets", "none")
    else:
        # Fallback to old flat format
        if 'id' not in data: return None
        dept_id = data.get('id', 'unknown')
        display_name = data.get('display_name', dept_id)
        head_agent = data.get('head_agent', 'none')
        reports_to = data.get('reports_to', 'none')
        workers = data.get('workers', [])
        tools = data.get('tools_available', [])
        kpi_ref = data.get('kpi_ref', 'none')

    # Edge extraction
    edges = []
    if head_agent != 'none':
        edges.append({"source": head_agent, "relation": "MANAGES", "target": dept_id})
    if reports_to != 'none':
        edges.append({"source": dept_id, "relation": "REPORTS_TO", "target": reports_to})

    narrative_lines = []
    narrative_lines.append(f"### DEPARTMENT: {display_name} (ID: {dept_id})")
    narrative_lines.append(f"- **Leadership**: The {display_name} department is managed by '{head_agent}' and reports to '{reports_to}'.")

    worker_narrative = []
    for w in workers:
        if isinstance(w, dict) and 'id' in w:
            wid = w['id']
            specialty = w.get('specialty', 'general task execution')
            edges.append({"source": wid, "relation": "WORKS_IN", "target": dept_id})
            worker_narrative.append(f"'{wid}' (specializes in {specialty})")

    if worker_narrative:
        narrative_lines.append(f"- **Workforce / Agents**: It employs the following agents: {', '.join(worker_narrative)}.")
    else:
        narrative_lines.append(f"- **Workforce / Agents**: No dedicated workers defined yet.")

    if tools:
        for t in tools:
            if isinstance(t, str):
                edges.append({"source": dept_id, "relation": "HAS_ACCESS_TO", "target": t})
        narrative_lines.append(f"- **Tools & Capabilities**: The department has access to the following tools/plugins/skills: {', '.join(map(str, tools))}.")

    if kpi_ref != 'none':
        edges.append({"source": dept_id, "relation": "TRACKS_KPI", "target": kpi_ref})
        narrative_lines.append(f"- **KPI & Monitoring**: It performance is measured by KPI reference '{kpi_ref}'.")

    # Collaboration
    collab = data.get('collaboration', {})
    provides_to = collab.get('provides_to', [])
    for c in provides_to:
        target_dept = c.get('dept')
        typ = c.get('type', 'outputs')
        if target_dept:
            edges.append({"source": dept_id, "relation": "PROVIDES_OUTPUT_TO", "target": target_dept, "payload": typ})
            narrative_lines.append(f"- **Collaboration**: Provides {typ} to department '{target_dept}'.")

    receives_from = collab.get('receives_from', [])
    for c in receives_from:
        target_dept = c.get('dept')
        typ = c.get('type', 'inputs')
        if target_dept:
            edges.append({"source": dept_id, "relation": "RECEIVES_INPUT_FROM", "target": target_dept, "payload": typ})

    narrative_lines.append("")

    return {
        "id": dept_id,
        "name": display_name,
        "edges": edges,
        "narrative": "\n".join(narrative_lines)
    }

WORKFLOW_DIR = r"<AI_OS_ROOT>\system\ops\workflows"
AUTOMATION_REGISTRY = r"<AI_OS_ROOT>\system\automations\AUTOMATION_REGISTRY.yaml"

def process_automations(master_graph, narratives):
    if not os.path.exists(AUTOMATION_REGISTRY):
        return
    try:
        with open(AUTOMATION_REGISTRY, 'r', encoding='utf-8') as f:
            auto_data = yaml.safe_load(f)

        automations = auto_data.get("automations", {})
        for auto_id, details in automations.items():
            master_graph["nodes"].append({"id": auto_id, "type": "AUTOMATION", "name": details.get("description", auto_id)})

            # Find department of owner
            owner_agent = str(details.get("owner", "")).lower()
            dept_owner = "operations" # default
            for n in master_graph["nodes"]:
                if n["type"] == "DEPARTMENT" and n["id"] in owner_agent:
                    dept_owner = n["id"]
                    break

            master_graph["edges"].append({"source": dept_owner, "relation": "OWNS_AUTOMATION", "target": auto_id})
            narratives.append(f"### AUTOMATION: {auto_id}\n- **Type**: {details.get('type')}\n- **Status**: {details.get('status')}\n- **Owner**: Administered by '{owner_agent}' (Mapped to Dept: {dept_owner}).\n- **Description**: {details.get('description')}\n")
    except Exception as e:
        print(f"Error parsing automations: {e}")

def process_workflows(master_graph, narratives):
    if not os.path.exists(WORKFLOW_DIR):
        return

    for wf in os.listdir(WORKFLOW_DIR):
        if not wf.endswith(".md"):
            continue

        filepath = os.path.join(WORKFLOW_DIR, wf)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception:
            continue

        dept_owner = None
        for line in lines[:20]:  # Scan top 20 lines for metadata
            if line.startswith("# Department:"):
                dept_str = line.lower()
                for node in master_graph["nodes"]:
                    if node["type"] == "DEPARTMENT" and node["id"] in dept_str:
                        dept_owner = node["id"]
                        break

        if dept_owner:
            master_graph["nodes"].append({"id": wf, "type": "WORKFLOW", "name": wf})
            master_graph["edges"].append({"source": dept_owner, "relation": "OWNS_PROCESS", "target": wf})
            narratives.append(f"### WORKFLOW: {wf}\n- **Process Ownership**: This workflow is owned and executed by department '{dept_owner}'.\n")

def main():
    if not os.path.exists(REGISTRY_DIR):
        os.makedirs(REGISTRY_DIR)

    dept_files = [f for f in os.listdir(DEPT_DIR) if f.endswith(".yaml")]

    master_graph = {
        "meta": {
            "title": "AI OS Organizational Ontology Graph",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_departments": 0,
            "total_edges": 0
        },
        "nodes": [],
        "edges": []
    }

    narratives = [
        "==================================================",
        "🏢 KNOWLEDGE GRAPH NARRATIVE: ORGANIZATION",
        "==================================================",
        "This document describes the relational mapping between departments, agents, tools, processes, and automations inside AI OS.",
        ""
    ]

    for df in dept_files:
        filepath = os.path.join(DEPT_DIR, df)
        dept_data = process_department(filepath)

        if dept_data:
            master_graph["nodes"].append({"id": dept_data["id"], "type": "DEPARTMENT", "name": dept_data["name"]})
            master_graph["edges"].extend(dept_data["edges"])
            narratives.append(dept_data["narrative"])

    # HÀM QUÉT WORKFLOW & AUTOMATIONS
    process_workflows(master_graph, narratives)
    process_automations(master_graph, narratives)

    # Compile stats
    master_graph["meta"]["total_departments"] = len([n for n in master_graph["nodes"] if n["type"] == "DEPARTMENT"])
    master_graph["meta"]["total_edges"] = len(master_graph["edges"])

    with open(OUT_YAML, "w", encoding="utf-8") as f:
        yaml.dump(master_graph, f, sort_keys=False, allow_unicode=True)

    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(narratives))

    print(f"[SUCCESS] Org Graph mapped {master_graph['meta']['total_departments']} Depts, Workflow/Auto nodes, and {len(master_graph['edges'])} Links.")
    print(f"[OUTPUT] -> {OUT_YAML}")
    print(f"[OUTPUT] -> {OUT_TXT}")

if __name__ == "__main__":
    main()
