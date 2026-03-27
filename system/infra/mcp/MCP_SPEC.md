# MCP Server Specification — Smart Bookmark Manager

## Overview
Smart Bookmark Manager exposes a Model Context Protocol (MCP) server
allowing AI tools to read and manage bookmarks.

## Server Identity

```json
{
  "name": "bookmark-manager",
  "version": "1.0.0",
  "description": "MCP server for Smart Bookmark Manager Chrome Extension"
}
```

## Resources

### bookmark://tree
Full bookmark tree structure.

### bookmark://folder/{id}
Bookmarks in specific folder.

### bookmark://search?q={query}
Search results for query.

## Tools

### create_bookmark
```json
{
  "name": "create_bookmark",
  "description": "Create a new bookmark",
  "inputSchema": {
    "type": "object",
    "properties": {
      "title": { "type": "string" },
      "url": { "type": "string" },
      "parentId": { "type": "string", "default": "1" }
    },
    "required": ["title", "url"]
  }
}
```

### search_bookmarks
```json
{
  "name": "search_bookmarks",
  "description": "Search through bookmarks",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": { "type": "string" }
    },
    "required": ["query"]
  }
}
```

### organize_with_ai
```json
{
  "name": "organize_with_ai",
  "description": "AI-powered bookmark organization",
  "inputSchema": {
    "type": "object",
    "properties": {
      "targetFolder": { "type": "string" },
      "dryRun": { "type": "boolean", "default": true }
    }
  }
}
```

## Implementation Plan
- Phase 3: Implement MCP server via native messaging or extension API
- Connect Claude Desktop / Claude Code to extension bookmarks
- Enable AI agents to manage bookmarks directly
