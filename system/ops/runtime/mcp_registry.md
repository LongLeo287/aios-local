# MCP Registry - AI OS Corp

Registry of all Model Context Protocol (MCP) servers running in the AI OS ecosystem.

## Active MCP Servers

### 1. GitNexus
- **Command**: `npx -y gitnexus@latest mcp`
- **Type**: stdio
- **Purpose**: Git repository analysis and code knowledge graph

### 2. Notebook Agent
- **Command**: `python tools/mcp/notebook_mcp_server.py`
- **Type**: stdio
- **Description**: AI OS Notebook Agent — extract, analyze, save knowledge from PDF/URL/text

### 3. MiniMax MCP
- **Command**: `uvx minimax-mcp`
- **Type**: stdio
- **Description**: MiniMax AI API — TTS, ASR, image generation, video generation, voice clone
- **Environment**:
  - `MINIMAX_API_KEY`
  - `MINIMAX_MCP_BASE_PATH`

### 4. MiniMax MCP JS
- **Command**: `node plugins/MiniMax-MCP-JS/build/index.js`
- **Type**: stdio
- **Description**: MiniMax AI API JS — image gen, video gen, TTS, voice clone (JS runtime)

### 5. NotebookLM MCP
- **Command**: `node plugins/notebooklm-mcp/dist/index.js`
- **Type**: stdio
- **Description**: NotebookLM MCP — AI note analysis and research synthesis

### 6. Claude Memory
- **Command**: `bun plugins/claude-mem/plugin/scripts/worker-service.cjs start`
- **Type**: stdio
- **Description**: Claude persistent memory — cross-session context storage

### 7. Scrapling MCP
- **Command**: `scrapling mcp`
- **Type**: stdio
- **Description**: Scrapling web scraper — 6 tools: get/fetch/stealthy, bypass Cloudflare

## Status
- **Total Servers**: 7
- **Last Updated**: 2026-03-24
- **All servers operational**: Yes