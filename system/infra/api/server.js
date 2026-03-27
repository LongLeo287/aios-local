/**
 * AI OS Universal REST API Bridge
 * Port 7000 — dùng cho ChatGPT, Gemini, AI Studio, và bất kỳ HTTP client nào
 * Antigravity và Claude Code dùng file system / MCP trực tiếp
 *
 * Start: node api/server.js
 */
const http = require("http");
const fs = require("fs");
const path = require("path");
const url = require("url");

const PORT = process.env.PORT || 7000;
// AOS_ROOT: resolve from __dirname (infra/api/) → ../../ = project root
const AOS_ROOT = process.env.AOS_ROOT || path.resolve(__dirname, "../../");
const BRAIN_CTX = path.join(AOS_ROOT, "brain/shared-context");
const CORP_DIR = path.join(BRAIN_CTX, "corp");
const REGISTRY_PATH = path.join(BRAIN_CTX, "SKILL_REGISTRY.json");

// CORS headers — cho phép call từ mọi nguồn (ChatGPT Actions, Gemini, v.v.)
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
  "Content-Type": "application/json"
};

function json(res, data, status = 200) {
  res.writeHead(status, CORS);
  res.end(JSON.stringify(data, null, 2));
}

function readJson(filePath) {
  return fs.existsSync(filePath) ? JSON.parse(fs.readFileSync(filePath, "utf-8")) : null;
}

function readText(filePath) {
  return fs.existsSync(filePath) ? fs.readFileSync(filePath, "utf-8") : null;
}

function parseBody(req) {
  return new Promise((resolve) => {
    let body = "";
    req.on("data", chunk => body += chunk);
    req.on("end", () => {
      try { resolve(JSON.parse(body)); } catch { resolve({}); }
    });
  });
}

const server = http.createServer(async (req, res) => {
  const { pathname, query } = url.parse(req.url, true);

  // CORS preflight
  if (req.method === "OPTIONS") {
    res.writeHead(204, CORS);
    res.end();
    return;
  }

  // === SKILLS ===
  if (pathname === "/api/skills" && req.method === "GET") {
    const registry = readJson(REGISTRY_PATH);
    if (!registry) return json(res, { error: "Registry not found" }, 404);
    let entries = registry.skills || registry.entries || [];
    if (query.tier) entries = entries.filter(s => String(s.tier) === query.tier);
    if (query.category) entries = entries.filter(s => s.category === query.category);
    if (query.status) entries = entries.filter(s => (s.status || "active") === query.status);
    return json(res, { count: entries.length, skills: entries });
  }

  if (pathname.startsWith("/api/skills/") && req.method === "GET") {
    const id = pathname.split("/api/skills/")[1];
    const registry = readJson(REGISTRY_PATH);
    const entries = registry?.skills || registry?.entries || [];
    const skill = entries.find(s => (s.id || s.name)?.toLowerCase() === id.toLowerCase());
    if (!skill) return json(res, { error: "Skill not found" }, 404);
    return json(res, skill);
  }

  // === CORP KPI ===
  if (pathname === "/api/corp/kpi" && req.method === "GET") {
    const kpi = readJson(path.join(CORP_DIR, "kpi_scoreboard.json"));
    if (!kpi) return json(res, { error: "KPI data not found" }, 404);
    if (query.dept) return json(res, kpi.departments?.[query.dept] || kpi[query.dept] || {});
    return json(res, kpi);
  }

  // === ESCALATIONS ===
  if (pathname === "/api/corp/escalations" && req.method === "GET") {
    const content = readText(path.join(CORP_DIR, "escalations.md"));
    return json(res, { content: content || "No escalations" });
  }

  if (pathname === "/api/corp/escalate" && req.method === "POST") {
    const body = await parseBody(req);
    const { dept, level, issue } = body;
    if (!dept || !level || !issue) return json(res, { error: "dept, level, issue required" }, 400);
    const escPath = path.join(CORP_DIR, "escalations.md");
    const existing = fs.existsSync(escPath) ? fs.readFileSync(escPath, "utf-8") : "# Escalations\n\n";
    const ts = new Date().toISOString();
    const entry = `\n## [${ts}] ${level} — ${dept}\n${issue}\n_Status: OPEN_\n`;
    fs.writeFileSync(escPath, existing + entry);
    return json(res, { ok: true, message: `Escalation ${level} added for ${dept}` });
  }

  // === PROPOSALS ===
  if (pathname === "/api/corp/proposals" && req.method === "GET") {
    const propDir = path.join(CORP_DIR, "proposals");
    if (!fs.existsSync(propDir)) return json(res, { proposals: [] });
    const files = fs.readdirSync(propDir).filter(f => f.endsWith(".md") && f !== "README.md");
    return json(res, { count: files.length, proposals: files });
  }

  // === CONTEXT FILES ===
  if (pathname.startsWith("/api/context/") && req.method === "GET") {
    const fileKey = pathname.split("/api/context/")[1];
    const allowed = {
      "blackboard": path.join(BRAIN_CTX, "blackboard.json"),
      "mission": path.join(CORP_DIR, "mission.md"),
      "context": path.join(BRAIN_CTX, "AI_OS_CONTEXT.md"),
      "agents": path.join(BRAIN_CTX, "AGENTS.md")
    };
    const filePath = allowed[fileKey];
    if (!filePath) return json(res, { error: "Unknown context file" }, 400);
    const content = readText(filePath);
    return json(res, { file: fileKey, content: content || "Not found" });
  }

  // === LLM ROUTER ===
  if (pathname === "/api/llm/route" && req.method === "GET") {
    const task = query.task || "qa";
    const routerPath = path.join(AOS_ROOT, "infra/llm/router.yaml");
    if (!fs.existsSync(routerPath)) return json(res, { error: "Router not configured" }, 404);
    // Simple parse: find the task block
    const content = fs.readFileSync(routerPath, "utf-8");
    const lines = content.split("\n");
    let inTask = false, result = {};
    for (const line of lines) {
      if (line.trim() === `${task}:`) { inTask = true; continue; }
      if (inTask && line.match(/^  \w/)) {
        const [k, v] = line.trim().split(": ");
        result[k] = v;
        if (Object.keys(result).length >= 4) break;
      }
      if (inTask && line.match(/^\w/)) break;
    }
    return json(res, { task, ...result });
  }

  // === PLUGINS ===
  if (pathname === "/api/plugins" && req.method === "GET") {
    const pluginsDir = path.join(AOS_ROOT, "plugins");
    if (!fs.existsSync(pluginsDir)) return json(res, { plugins: [] });
    const dirs = fs.readdirSync(pluginsDir, { withFileTypes: true })
      .filter(e => e.isDirectory())
      .map(e => ({
        name: e.name,
        hasSkill: fs.existsSync(path.join(pluginsDir, e.name, "SKILL.md"))
      }));
    return json(res, { count: dirs.length, plugins: dirs });
  }

  // === HEALTH CHECK ===
  if (pathname === "/health") {
    const ver = readJson(path.join(AOS_ROOT, "version.json"));
    return json(res, { status: "ok", version: ver?.version || "3.0.0", timestamp: new Date().toISOString() });
  }

  // 404
  json(res, { error: "Not found", path: pathname }, 404);
});

server.listen(PORT, () => {
  console.log(`\n🚀 AI OS REST API Bridge running at http://localhost:${PORT}`);
  console.log(`   GET  /api/skills          — skill list`);
  console.log(`   GET  /api/corp/kpi        — KPI board`);
  console.log(`   POST /api/corp/escalate   — add escalation`);
  console.log(`   GET  /api/context/context — AI_OS_CONTEXT.md`);
  console.log(`   GET  /api/llm/route?task= — LLM routing advice`);
  console.log(`   GET  /health              — health check\n`);
});

module.exports = server;
