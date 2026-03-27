import os
import re
from datetime import datetime

YAML_PATH = r"<AI_OS_ROOT>\system\registry\SYSTEM_INDEX.yaml"
NARRATIVE_PATH = r"<AI_OS_ROOT>\system\registry\SYSTEM_INDEX_NARRATIVE.txt"

def build_narrative_for_lightrag():
    if not os.path.exists(YAML_PATH):
        print(f"Error: {YAML_PATH} not found.")
        return

    with open(YAML_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Simple regex parser to avoid strictly requiring PyYAML
    blocks = content.split("- id: ")
    if len(blocks) < 2:
        print("No entities found.")
        return

    narrative_lines = []
    narrative_lines.append("TITLE: AI OS MASTER KNOWLEDGE GRAPH NARRATIVE")
    narrative_lines.append(f"DATE: {datetime.now().strftime('%Y-%m-%d')}")
    narrative_lines.append("DESCRIPTION: This document describes the exact architecture and entities operating within the AI OS. It defines what systems live in the Local Core vs Remote Ecosystem.")
    narrative_lines.append("---")

    entity_count = 0

    for block in blocks[1:]:
        # Extract fields using simple string ops
        lines = block.split('\n')
        e_id = lines[0].strip().strip("'")

        e_name = "Unknown"
        e_path = "Unknown"
        e_cat = "Unknown"
        e_type = "Unknown"

        for line in lines:
            if "name: " in line:
                e_name = line.split("name: ")[1].strip().strip("'")
            elif "path: " in line:
                e_path = line.split("path: ")[1].strip().strip("'")
            elif "category: " in line:
                e_cat = line.split("category: ")[1].strip().strip("'")
            elif "type: " in line:
                e_type = line.split("type: ")[1].strip().strip("'")

        # Generate semantic sentences for Graph Extraction
        narrative = f"The entity '{e_name}' (ID: {e_id}) is a {e_type} component located at '{e_path}'. It belongs to the {e_cat} architectural branch of the AI OS. "

        if e_cat == "LOCAL_CORE":
            narrative += f"Because '{e_name}' is in LOCAL_CORE, it is an isolated backend system, agent, or logic core that operates securely inside the main AI OS engine."
        elif e_cat == "REMOTE_ECOSYSTEM":
            narrative += f"Because '{e_name}' is in REMOTE_ECOSYSTEM, it is a user interface, dashboard, application, or gateway that operates securely outside the main core."

        narrative_lines.append(narrative)
        entity_count += 1

    with open(NARRATIVE_PATH, "w", encoding="utf-8") as f:
        f.write("\n\n".join(narrative_lines))

    print(f"[DONE] Translated {entity_count} entities into LightRAG narrative format.")
    print(f"Narrative saved to: {NARRATIVE_PATH}")
    print("\nNext step: Run LightRAG.insert() on this file to map the Knowledge Graph!")

if __name__ == "__main__":
    build_narrative_for_lightrag()
