#!/usr/bin/env node
/**
 * Smart Bookmark Manager — MCP Server
 *
 * Exposes your bookmark data to Claude AI via Model Context Protocol.
 * Uses stdio transport (compatible with Claude Desktop).
 *
 * ─── Setup ──────────────────────────────────────────────────────────────────
 * 1. Export bookmarks from extension:
 *    Settings → Export as JSON → saves bookmarks_<date>.json
 *
 * 2. Place (or symlink) the exported file as: mcp/bookmarks.json
 *
 * 3. Add to Claude Desktop config:
 *    macOS:   ~/Library/Application Support/Claude/claude_desktop_config.json
 *    Windows: %APPDATA%\Claude\claude_desktop_config.json
 *
 *    {
 *      "mcpServers": {
 *        "bookmarks": {
 *          "command": "node",
 *          "args": ["/absolute/path/to/mcp/server.js"]
 *        }
 *      }
 *    }
 *
 * 4. Restart Claude Desktop — you'll see the bookmark tools available.
 *
 * ─── Available MCP Tools ────────────────────────────────────────────────────
 * • search_bookmarks   — full-text search across title + URL
 * • list_bookmarks     — list top-level or folder contents
 * • get_stats          — total count, folders, top domains
 * • find_duplicates    — detect duplicate URLs
 * ────────────────────────────────────────────────────────────────────────────
 */

import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createInterface } from 'node:readline';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_FILE = resolve(__dirname, 'bookmarks.json');

// ─── Load Bookmark Data ─────────────────────────────────────────────────────

function loadBookmarks() {
    if (!existsSync(DATA_FILE)) {
        return [];
    }
    try {
        return JSON.parse(readFileSync(DATA_FILE, 'utf8'));
    } catch (err) {
        process.stderr.write(`[MCP] Failed to load bookmarks.json: ${err.message}\n`);
        return [];
    }
}

/** Flatten tree to leaf bookmarks */
function flatten(nodes, acc = []) {
    for (const n of nodes) {
        if (n.url) acc.push(n);
        if (n.children?.length) flatten(n.children, acc);
    }
    return acc;
}

/** Normalize URL for dedup comparison */
function normalizeUrl(url) {
    try {
        const u = new URL(url);
        ['utm_source','utm_medium','utm_campaign','fbclid','gclid','ref'].forEach(p => u.searchParams.delete(p));
        u.hash = '';
        return `${u.protocol}//${u.host}${u.pathname.replace(/\/+$/, '')}${u.search}`.toLowerCase();
    } catch {
        return url.toLowerCase().trim();
    }
}

// ─── Tool Implementations ────────────────────────────────────────────────────

const tools = {
    /**
     * search_bookmarks — full-text search
     */
    search_bookmarks({ query, limit = 20 }) {
        if (!query?.trim()) return { results: [], count: 0 };
        const q = query.toLowerCase();
        const bookmarks = loadBookmarks();
        const flat = flatten(bookmarks);
        const results = flat
            .filter(b => b.title?.toLowerCase().includes(q) || b.url?.toLowerCase().includes(q))
            .slice(0, Math.min(limit, 50))
            .map(b => ({ id: b.id, title: b.title, url: b.url }));
        return { results, count: results.length, query };
    },

    /**
     * list_bookmarks — list top-level or folder contents
     */
    list_bookmarks({ folder_id, limit = 50 }) {
        const bookmarks = loadBookmarks();
        let nodes = bookmarks;

        if (folder_id) {
            // Find the folder
            const findFolder = (list) => {
                for (const n of list) {
                    if (n.id === folder_id) return n.children || [];
                    if (n.children?.length) {
                        const found = findFolder(n.children);
                        if (found) return found;
                    }
                }
                return null;
            };
            nodes = findFolder(bookmarks) ?? [];
        }

        const result = nodes.slice(0, limit).map(n => ({
            id: n.id,
            title: n.title,
            url: n.url || null,
            isFolder: !n.url,
            childCount: n.children?.length ?? 0,
        }));

        return { items: result, count: result.length, total: nodes.length };
    },

    /**
     * get_stats — bookmark statistics
     */
    get_stats() {
        const bookmarks = loadBookmarks();
        const flat = flatten(bookmarks);

        const domainMap = {};
        for (const b of flat) {
            try {
                const host = new URL(b.url).hostname.replace(/^www\./, '');
                domainMap[host] = (domainMap[host] || 0) + 1;
            } catch { /* skip invalid URLs */ }
        }

        const topDomains = Object.entries(domainMap)
            .sort(([, a], [, b]) => b - a)
            .slice(0, 10)
            .map(([domain, count]) => ({ domain, count }));

        const countFolders = (nodes) => nodes.reduce((sum, n) =>
            sum + (!n.url ? 1 : 0) + (n.children?.length ? countFolders(n.children) : 0), 0);

        return {
            total_bookmarks: flat.length,
            total_folders: countFolders(bookmarks),
            top_domains: topDomains,
        };
    },

    /**
     * find_duplicates — detect duplicate URLs
     */
    find_duplicates() {
        const bookmarks = loadBookmarks();
        const flat = flatten(bookmarks);
        const map = new Map();

        for (const b of flat) {
            const key = normalizeUrl(b.url);
            if (!map.has(key)) map.set(key, []);
            map.get(key).push({ id: b.id, title: b.title, url: b.url });
        }

        const groups = Array.from(map.values()).filter(g => g.length > 1);
        const total  = groups.reduce((s, g) => s + g.length - 1, 0);

        return {
            duplicate_groups: groups,
            total_duplicates: total,
            group_count: groups.length,
        };
    },
};

// ─── MCP Protocol (JSON-RPC 2.0 over stdio) ─────────────────────────────────

const SERVER_INFO = {
    name: 'smart-bookmark-manager',
    version: '1.2.0',
};

const CAPABILITIES = {
    tools: {},
};

const TOOL_DEFS = [
    {
        name: 'search_bookmarks',
        description: 'Search bookmarks by keyword across title and URL.',
        inputSchema: {
            type: 'object',
            properties: {
                query: { type: 'string', description: 'Search query' },
                limit: { type: 'number', description: 'Max results (default 20, max 50)' },
            },
            required: ['query'],
        },
    },
    {
        name: 'list_bookmarks',
        description: 'List bookmarks. Optionally pass folder_id to list contents of a specific folder.',
        inputSchema: {
            type: 'object',
            properties: {
                folder_id: { type: 'string', description: 'Folder ID to list (omit for top-level)' },
                limit:     { type: 'number', description: 'Max items (default 50)' },
            },
        },
    },
    {
        name: 'get_stats',
        description: 'Get bookmark statistics: total count, folder count, top domains.',
        inputSchema: { type: 'object', properties: {} },
    },
    {
        name: 'find_duplicates',
        description: 'Find bookmarks with duplicate URLs (after normalizing tracking params).',
        inputSchema: { type: 'object', properties: {} },
    },
];

function respond(id, result) {
    const msg = JSON.stringify({ jsonrpc: '2.0', id, result });
    process.stdout.write(msg + '\n');
}

function respondError(id, code, message) {
    const msg = JSON.stringify({ jsonrpc: '2.0', id, error: { code, message } });
    process.stdout.write(msg + '\n');
}

async function handleMessage(raw) {
    let msg;
    try {
        msg = JSON.parse(raw);
    } catch {
        respondError(null, -32700, 'Parse error');
        return;
    }

    const { id, method, params } = msg;

    try {
        switch (method) {
            case 'initialize':
                respond(id, { protocolVersion: '2024-11-05', capabilities: CAPABILITIES, serverInfo: SERVER_INFO });
                break;

            case 'initialized':
                break; // notification, no response needed

            case 'tools/list':
                respond(id, { tools: TOOL_DEFS });
                break;

            case 'tools/call': {
                const { name, arguments: args } = params || {};
                if (!tools[name]) {
                    respondError(id, -32601, `Unknown tool: ${name}`);
                    break;
                }
                const result = tools[name](args || {});
                respond(id, {
                    content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
                });
                break;
            }

            case 'ping':
                respond(id, {});
                break;

            default:
                respondError(id, -32601, `Method not found: ${method}`);
        }
    } catch (err) {
        process.stderr.write(`[MCP] Error handling ${method}: ${err.message}\n`);
        respondError(id, -32603, err.message);
    }
}

// ─── Entry Point ─────────────────────────────────────────────────────────────

process.stderr.write(`[MCP] Smart Bookmark Manager Server v${SERVER_INFO.version} ready\n`);
process.stderr.write(`[MCP] Data file: ${DATA_FILE}\n`);
process.stderr.write(existsSync(DATA_FILE)
    ? `[MCP] Loaded: ${flatten(loadBookmarks()).length} bookmarks\n`
    : `[MCP] WARNING: bookmarks.json not found — export from extension first!\n`);

const rl = createInterface({ input: process.stdin });
rl.on('line', line => {
    if (line.trim()) handleMessage(line.trim());
});
