import os
import json
import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
VAULT_DATA_DIR = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA')

# Danh sách 10 Repository được Approve (Priority 1 & 2)
APPROVED_REPOS = [
    {"repo": "upstash/context7", "type": "TOOL", "domain": "mcp, llm, docs", "priority": "P1", "notes": "MCP server cung cấp doc realtime. Rule GEMINI.md"},
    {"repo": "aquasecurity/trivy", "type": "TOOL", "domain": "security, devops, cve", "priority": "P1", "notes": "Vulnerability scanner cho container, code. Tích hợp strix-scan."},
    {"repo": "VoltAgent/awesome-agent-skills", "type": "TOOL", "domain": "skills, agent", "priority": "P1", "notes": "700+ skills (Firecrawl, Stripe, Gemini) tương thích Antigravity"},
    {"repo": "hoavdc/CodexKit", "type": "REFERENCE", "domain": "skills, framework", "priority": "P2", "notes": "Framework 5 layers, 4C Quality gate. Template cho system skills."},
    {"repo": "affaan-m/everything-claude-code", "type": "REFERENCE", "domain": "agent, skills", "priority": "P2", "notes": "Cherry pick AgentShield và Continuous Learning v2."},
    {"repo": "HoangNguyen0403/agent-skills-standard", "type": "TOOL", "domain": "skills", "priority": "P2", "notes": "Framework skills (NextJS, Supabase, FastAPI)"},
    {"repo": "Lum1104/Understand-Anything", "type": "RESEARCH", "domain": "knowledge, graph", "priority": "P2", "notes": "Codebase knowledge graph skill cho Antigravity"},
    {"repo": "BloopAI/vibe-kanban", "type": "TOOL", "domain": "productivity, pm", "priority": "P2", "notes": "AI-native Kanban 10X output. Đối chiếu với hệ thống task hiện tại."},
    {"repo": "tqdat410/agentune", "type": "TOOL", "domain": "mcp, music", "priority": "P2", "notes": "MCP Music player cho ambient sound coder."},
    {"repo": "tody-agent/codymaster", "type": "REFERENCE", "domain": "skills, ui", "priority": "P2", "notes": "Cherry-pick 34 skills (Zero-Doc generator, Visual Dashboard)."}
]

def main():
    os.makedirs(VAULT_DATA_DIR, exist_ok=True)
    print(f"[{datetime.datetime.now().isoformat()}] STARTING BULK INTAKE TO VAULT...")

    count = 0
    for idx, item in enumerate(APPROVED_REPOS):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + f"{idx:02d}"
        ki_id = f"KI-{timestamp}"

        ticket = {
            "id": ki_id,
            "source_type": "repo",
            "source": f"https://github.com/{item['repo']}",
            "submitted_by": "antigravity-bulk-intake",
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "PENDING_CLASSIFICATION",
            "metadata_hints": {
                "knowledge_type": item["type"],
                "suggested_domains": item["domain"].split(", "),
                "priority": item["priority"],
                "ceo_notes": item["notes"]
            }
        }

        filename = f"{ki_id}_{item['repo'].replace('/', '_')}.json"
        filepath = os.path.join(VAULT_DATA_DIR, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(ticket, f, indent=4, ensure_ascii=False)

        print(f"  [+] Dropped into Vault: {filename}")
        count += 1

    print(f"\n[SUCCESS] Dropped {count} Repo Intake Tickets into {VAULT_DATA_DIR}.")
    print("Daemon 'auto_evolution_engine' should now detect these and trigger knowledge-ingest.md -> agent-auto-create.md")

if __name__ == "__main__":
    main()
