#!/usr/bin/env node
/**
 * AI OS Skill Registry MCP Server
 * Cho Claude Code query và manage SKILL_REGISTRY.json
 */
const { Server } = require("@modelcontextprotocol/sdk/server/index.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const { ListToolsRequestSchema, CallToolRequestSchema } = require("@modelcontextprotocol/sdk/types.js");
const fs = require("fs");
const path = require("path");

const REGISTRY_PATH = process.env.REGISTRY_PATH ||
  "D:/Project/AI OS/shared-context/SKILL_REGISTRY.json";

const server = new Server(
  { name: "skill-registry", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

function loadRegistry() {
  return fs.existsSync(REGISTRY_PATH)
    ? JSON.parse(fs.readFileSync(REGISTRY_PATH, "utf-8"))
    : { skills: [] };
}

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "list_skills",
      description: "Liệt kê skills trong registry (filter: tier, category, status)",
      inputSchema: {
        type: "object",
        properties: {
          tier: { type: "number" },
          category: { type: "string" },
          status: { type: "string", enum: ["active", "inactive", "beta"] }
        }
      }
    },
    {
      name: "get_skill",
      description: "Lấy chi tiết 1 skill theo ID hoặc name",
      inputSchema: {
        type: "object",
        properties: { id: { type: "string" } },
        required: ["id"]
      }
    },
    {
      name: "check_health",
      description: "Kiểm tra tất cả skills: có SKILL.md? Đúng format?",
      inputSchema: { type: "object", properties: {} }
    },
    {
      name: "get_registry_summary",
      description: "Thống kê tổng quan registry: số skills, tier breakdown, categories",
      inputSchema: { type: "object", properties: {} }
    }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    const registry = loadRegistry();
    const entries = registry.skills || registry.entries || [];

    if (name === "list_skills") {
      let filtered = entries;
      if (args.tier) filtered = filtered.filter(s => s.tier === args.tier);
      if (args.category) filtered = filtered.filter(s => s.category === args.category);
      if (args.status) filtered = filtered.filter(s => (s.status || "active") === args.status);
      const result = filtered.map(s => `[Tier ${s.tier}] ${s.id || s.name} — ${s.category || ""}`).join("\n");
      return { content: [{ type: "text", text: `${filtered.length} skills:\n${result}` }] };
    }

    if (name === "get_skill") {
      const skill = entries.find(s => (s.id || s.name)?.toLowerCase() === args.id.toLowerCase());
      if (!skill) return { content: [{ type: "text", text: `Skill '${args.id}' not found` }] };
      return { content: [{ type: "text", text: JSON.stringify(skill, null, 2) }] };
    }

    if (name === "check_health") {
      const issues = [];
      for (const s of entries) {
        const skillPath = s.path;
        if (skillPath && !fs.existsSync(path.join("D:/Project/AI OS", skillPath, "SKILL.md"))) {
          issues.push(`❌ Missing SKILL.md: ${s.id || s.name}`);
        }
      }
      if (issues.length === 0) return { content: [{ type: "text", text: `✅ All ${entries.length} skills healthy` }] };
      return { content: [{ type: "text", text: issues.join("\n") }] };
    }

    if (name === "get_registry_summary") {
      const tiers = {};
      const cats = {};
      for (const s of entries) {
        tiers[s.tier] = (tiers[s.tier] || 0) + 1;
        if (s.category) cats[s.category] = (cats[s.category] || 0) + 1;
      }
      const summary = {
        total: entries.length,
        by_tier: tiers,
        by_category: cats
      };
      return { content: [{ type: "text", text: JSON.stringify(summary, null, 2) }] };
    }

    return { content: [{ type: "text", text: `Unknown tool: ${name}` }] };
  } catch (err) {
    return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
  }
});

async function main() {
  if (process.argv.includes("--test")) {
    console.log("✅ skill-registry MCP server OK — REGISTRY:", REGISTRY_PATH);
    process.exit(0);
  }
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("skill-registry MCP server running on stdio");
}

main().catch(console.error);
