import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import fs from "fs/promises";
import path from "path";

/**
 * MCP Server for Smart Bookmark Manager
 * Allows AI Agents (like Claude Desktop) to query your bookmarks.
 * Phase 9 Enhancement: Advanced context retrieval.
 */

// We look for bookmarks.json in the current directory, or via ENV, or in standard OS downloads
const BOOKMARKS_PATH = process.env.BOOKMARKS_JSON_PATH || path.resolve(process.cwd(), "bookmarks.json");

const server = new Server(
  {
    name: "smart-bookmark-manager",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

/**
 * Helper to load and flatten bookmarks
 */
async function getFlatBookmarks() {
  try {
    const content = await fs.readFile(BOOKMARKS_PATH, "utf-8");
    const tree = JSON.parse(content);
    
    const flat = [];
    const flatten = (nodes) => {
      for (const node of nodes) {
        if (node.url) {
          flat.push({
            id: node.id,
            title: node.title,
            url: node.url,
            tags: node.tags || []
          });
        }
        if (node.children) flatten(node.children);
      }
    };
    
    flatten(tree);
    return flat;
  } catch (error) {
    throw new Error(`Failed to read bookmarks.json at ${BOOKMARKS_PATH}. Make sure to export it from the extension first.`);
  }
}

/**
 * List available tools
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "search_bookmarks",
        description: "Search for bookmarks by title or URL keyword",
        inputSchema: {
          type: "object",
          properties: {
            query: { type: "string", description: "Search keyword" },
          },
          required: ["query"],
        },
      },
      {
        name: "get_bookmarks_by_tag",
        description: "Filter bookmarks by an AI-generated tag",
        inputSchema: {
          type: "object",
          properties: {
            tag: { type: "string", description: "Tag name (e.g. Development, Design, News)" },
          },
          required: ["tag"],
        },
      },
      {
        name: "get_recent_bookmarks",
        description: "Get the most recently added bookmarks to understand current context",
        inputSchema: {
          type: "object",
          properties: {
            limit: { type: "number", description: "Number of recent bookmarks to fetch (default: 10)" },
          },
        },
      },
    ],
  };
});

/**
 * Handle tool calls
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const bookmarks = await getFlatBookmarks();

  switch (request.params.name) {
    case "search_bookmarks": {
      const query = request.params.arguments.query.toLowerCase();
      const results = bookmarks.filter(
        (b) => b.title.toLowerCase().includes(query) || b.url.toLowerCase().includes(query)
      );
      return {
        content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
      };
    }

    case "get_bookmarks_by_tag": {
      const tag = request.params.arguments.tag.toLowerCase();
      const results = bookmarks.filter((b) => 
        b.tags && b.tags.some(t => t.toLowerCase() === tag)
      );
      return {
        content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
      };
    }

    case "get_recent_bookmarks": {
      const limit = request.params.arguments.limit || 10;
      // Assuming higher ID means more recent in Chrome's internal DB, 
      // or we just return the end of the flat array.
      // Often bookmarks are appended.
      const results = bookmarks.slice(-limit).reverse();
      return {
        content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
      };
    }

    default:
      throw new Error("Unknown tool");
  }
});

/**
 * Start the server
 */
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Smart Bookmark Manager MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
