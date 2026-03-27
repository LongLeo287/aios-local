#!/usr/bin/env node
/**
 * AI OS Corp Data MCP Server
 * Cho Claude Code đọc/ghi KPI, escalations, proposals
 */
const { Server } = require("@modelcontextprotocol/sdk/server/index.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const { ListToolsRequestSchema, CallToolRequestSchema } = require("@modelcontextprotocol/sdk/types.js");
const fs = require("fs");
const path = require("path");

const CORP_DIR = process.env.CORP_DIR || "D:/Project/AI OS/shared-context/corp";
const AOS_ROOT = process.env.AOS_ROOT || "D:/Project/AI OS";

const server = new Server(
  { name: "corp-data", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "get_kpi_board",
      description: "Lấy KPI scoreboard của tất cả phòng ban",
      inputSchema: { type: "object", properties: { dept: { type: "string" } } }
    },
    {
      name: "update_kpi",
      description: "Cập nhật KPI cho một phòng ban",
      inputSchema: {
        type: "object",
        properties: {
          dept: { type: "string" },
          metric: { type: "string" },
          value: { type: "number" }
        },
        required: ["dept", "metric", "value"]
      }
    },
    {
      name: "list_escalations",
      description: "Xem danh sách escalations hiện tại",
      inputSchema: { type: "object", properties: {} }
    },
    {
      name: "add_escalation",
      description: "Tạo escalation mới",
      inputSchema: {
        type: "object",
        properties: {
          dept: { type: "string" },
          level: { type: "string", enum: ["L1", "L2", "L3"] },
          issue: { type: "string" }
        },
        required: ["dept", "level", "issue"]
      }
    },
    {
      name: "get_proposals",
      description: "Liệt kê proposals từ Strategy dept",
      inputSchema: { type: "object", properties: {} }
    },
    {
      name: "get_mission",
      description: "Đọc mission và mục tiêu công ty",
      inputSchema: { type: "object", properties: {} }
    },
    {
      name: "get_org_chart",
      description: "Xem sơ đồ tổ chức corp",
      inputSchema: { type: "object", properties: {} }
    }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  const ts = new Date().toISOString();

  try {
    if (name === "get_kpi_board") {
      const kpiPath = path.join(CORP_DIR, "kpi_scoreboard.json");
      if (!fs.existsSync(kpiPath)) return { content: [{ type: "text", text: "KPI scoreboard not found" }] };
      const data = JSON.parse(fs.readFileSync(kpiPath, "utf-8"));
      if (args.dept) {
        const deptData = data[args.dept] || data.departments?.[args.dept];
        return { content: [{ type: "text", text: JSON.stringify(deptData, null, 2) }] };
      }
      return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
    }

    if (name === "update_kpi") {
      const kpiPath = path.join(CORP_DIR, "kpi_scoreboard.json");
      const data = fs.existsSync(kpiPath) ? JSON.parse(fs.readFileSync(kpiPath, "utf-8")) : {};
      if (!data.departments) data.departments = {};
      if (!data.departments[args.dept]) data.departments[args.dept] = {};
      data.departments[args.dept][args.metric] = { value: args.value, updated: ts };
      data.last_updated = ts;
      fs.writeFileSync(kpiPath, JSON.stringify(data, null, 2));
      return { content: [{ type: "text", text: `✅ KPI updated: ${args.dept}.${args.metric} = ${args.value}` }] };
    }

    if (name === "list_escalations") {
      const escPath = path.join(CORP_DIR, "escalations.md");
      const content = fs.existsSync(escPath) ? fs.readFileSync(escPath, "utf-8") : "No escalations";
      return { content: [{ type: "text", text: content }] };
    }

    if (name === "add_escalation") {
      const escPath = path.join(CORP_DIR, "escalations.md");
      const existing = fs.existsSync(escPath) ? fs.readFileSync(escPath, "utf-8") : "# Escalations\n\n";
      const entry = `\n## [${ts}] ${args.level} — ${args.dept}\n${args.issue}\n_Status: OPEN_\n`;
      fs.writeFileSync(escPath, existing + entry);
      return { content: [{ type: "text", text: `✅ Escalation ${args.level} added for ${args.dept}` }] };
    }

    if (name === "get_proposals") {
      const propDir = path.join(CORP_DIR, "proposals");
      if (!fs.existsSync(propDir)) return { content: [{ type: "text", text: "No proposals directory" }] };
      const files = fs.readdirSync(propDir).filter(f => f.endsWith(".md") && f !== "README.md");
      return { content: [{ type: "text", text: `${files.length} proposals:\n${files.join("\n")}` }] };
    }

    if (name === "get_mission") {
      const mPath = path.join(CORP_DIR, "mission.md");
      const content = fs.existsSync(mPath) ? fs.readFileSync(mPath, "utf-8") : "Mission file not found";
      return { content: [{ type: "text", text: content }] };
    }

    if (name === "get_org_chart") {
      const orgPath = path.join(AOS_ROOT, "corp", "org_chart.yaml");
      const content = fs.existsSync(orgPath) ? fs.readFileSync(orgPath, "utf-8") : "Org chart not found";
      return { content: [{ type: "text", text: content }] };
    }

    return { content: [{ type: "text", text: `Unknown tool: ${name}` }] };
  } catch (err) {
    return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
  }
});

async function main() {
  if (process.argv.includes("--test")) {
    console.log("✅ corp-data MCP server OK — CORP_DIR:", CORP_DIR);
    process.exit(0);
  }
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("corp-data MCP server running on stdio");
}

main().catch(console.error);
