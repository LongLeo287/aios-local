#!/usr/bin/env node
/**
 * AI OS Workspace MCP Server
 * Cho Claude Code / Cursor truy cập toàn bộ AI OS workspace
 * Tools: list_dir, read_file, search_skills, read_blackboard, read_registry
 */
const { Server } = require("@modelcontextprotocol/sdk/server/index.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const { ListToolsRequestSchema, CallToolRequestSchema } = require("@modelcontextprotocol/sdk/types.js");
const fs = require("fs");
const path = require("path");

const AOS_ROOT = process.env.AOS_ROOT || "D:/Project/AI OS";

const server = new Server(
  { name: "aos-workspace", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// === TOOLS ===
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "list_dir",
      description: "Liệt kê nội dung thư mục trong AI OS workspace",
      inputSchema: {
        type: "object",
        properties: {
          path: { type: "string", description: "Đường dẫn tương đối từ AI OS root" }
        },
        required: ["path"]
      }
    },
    {
      name: "read_file",
      description: "Đọc nội dung file trong AI OS workspace",
      inputSchema: {
        type: "object",
        properties: {
          path: { type: "string", description: "Đường dẫn tương đối từ AI OS root" }
        },
        required: ["path"]
      }
    },
    {
      name: "search_skills",
      description: "Tìm kiếm skills theo tên, category hoặc tag",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string" },
          category: { type: "string" },
          tier: { type: "number" }
        }
      }
    },
    {
      name: "read_blackboard",
      description: "Đọc bảng thông tin chung (blackboard) của AI OS",
      inputSchema: { type: "object", properties: {} }
    },
    {
      name: "read_context",
      description: "Đọc file AI_OS_CONTEXT.md — universal context cho tất cả AI",
      inputSchema: { type: "object", properties: {} }
    },
    {
      name: "list_plugins",
      description: "Liệt kê tất cả plugins và trạng thái SKILL.md",
      inputSchema: { type: "object", properties: {} }
    }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === "list_dir") {
      const fullPath = path.join(AOS_ROOT, args.path);
      if (!fs.existsSync(fullPath)) return { content: [{ type: "text", text: `Not found: ${args.path}` }] };
      const entries = fs.readdirSync(fullPath, { withFileTypes: true });
      const result = entries.map(e => `${e.isDirectory() ? "[DIR]" : "[FILE]"} ${e.name}`).join("\n");
      return { content: [{ type: "text", text: result }] };
    }

    if (name === "read_file") {
      const fullPath = path.join(AOS_ROOT, args.path);
      if (!fs.existsSync(fullPath)) return { content: [{ type: "text", text: `Not found: ${args.path}` }] };
      const content = fs.readFileSync(fullPath, "utf-8");
      return { content: [{ type: "text", text: content }] };
    }

    if (name === "search_skills") {
      const skillsDir = path.join(AOS_ROOT, "skills");
      const results = [];
      if (fs.existsSync(skillsDir)) {
        const dirs = fs.readdirSync(skillsDir, { withFileTypes: true })
          .filter(e => e.isDirectory());
        for (const dir of dirs) {
          const skillMd = path.join(skillsDir, dir.name, "SKILL.md");
          if (fs.existsSync(skillMd)) {
            const content = fs.readFileSync(skillMd, "utf-8");
            const queryMatch = !args.query || content.toLowerCase().includes(args.query.toLowerCase());
            const catMatch = !args.category || content.toLowerCase().includes(args.category.toLowerCase());
            if (queryMatch && catMatch) results.push(dir.name);
          }
        }
      }
      return { content: [{ type: "text", text: `Found ${results.length} skills:\n${results.join("\n")}` }] };
    }

    if (name === "read_blackboard") {
      const bbPath = path.join(AOS_ROOT, "shared-context", "blackboard.json");
      const content = fs.existsSync(bbPath) ? fs.readFileSync(bbPath, "utf-8") : "{}";
      return { content: [{ type: "text", text: content }] };
    }

    if (name === "read_context") {
      const ctxPath = path.join(AOS_ROOT, "shared-context", "AI_OS_CONTEXT.md");
      const content = fs.existsSync(ctxPath) ? fs.readFileSync(ctxPath, "utf-8") : "Context file not found";
      return { content: [{ type: "text", text: content }] };
    }

    if (name === "list_plugins") {
      const pluginsDir = path.join(AOS_ROOT, "plugins");
      const dirs = fs.readdirSync(pluginsDir, { withFileTypes: true }).filter(e => e.isDirectory());
      const results = dirs.map(d => {
        const hasSkill = fs.existsSync(path.join(pluginsDir, d.name, "SKILL.md"));
        return `${hasSkill ? "✅" : "❌"} ${d.name}`;
      });
      return { content: [{ type: "text", text: `${dirs.length} plugins:\n${results.join("\n")}` }] };
    }

    return { content: [{ type: "text", text: `Unknown tool: ${name}` }] };
  } catch (err) {
    return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
  }
});

async function main() {
  if (process.argv.includes("--test")) {
    console.log("✅ aos-workspace MCP server OK — AOS_ROOT:", AOS_ROOT);
    process.exit(0);
  }
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("aos-workspace MCP server running on stdio");
}

main().catch(console.error);
