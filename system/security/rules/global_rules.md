# Global Agent Rules

## Description
Universal governance rules applying to all agents within the workspace, mandating directory boundaries, tool usage constraints, and hybrid sourcing protocols.

## 1. Zero-Touch Project Policy
- The agent must **never** modify the `extension/` directory unless explicitly instructed by the user.
- All experiments, scratchpads, and temporary scripts must be written to `.agents/worktree/`.

## 2. Capability On-Demand (Hybrid Sourcing)
- Before attempting complex operations (like data extraction, advanced UI design, or RAG), the agent must consult `.agents/docs/github_capabilities_registry.md` and `.agents/docs/external_skill_libraries.md`.
- Ensure you load the correct skill plugin (e.g., `LightRAG`, `ui-ux-pro-max`, `langextract`) dynamically.

## 3. Tool Usage Constraints
- Prefer local `.agents/skills/` scripts over writing new ad-hoc implementations.
- If a workflow exists in `.agents/workflows/`, follow its standard operating procedure step-by-step.

## 4. MCP Server Ecosystem
- All external context integrations (Databases, File Systems, Web Search) must route through the defined `.agents/mcp/` config. Do not assume direct API access if an MCP server is configured for the task.
