# AI Integration — Knowledge Base

## Description
Technical documentation outlining the integration of Claude AI into the Smart Bookmark Manager, covering model selection, privacy, security, and the MCP bridge.

Smart Bookmark Manager integrates Claude AI for 3 core features:
1. Auto-tagging/classification (Phase 2)
2. Semantic search via embeddings (Phase 2)
3. Natural language bookmark queries (Phase 4)

## Model Selection

| Use Case | Model | Why |
|----------|-------|-----|
| Bookmark classification | claude-haiku-4-5-20251001 | Fast, cost-efficient, sufficient |
| Semantic search | text-embedding (future) | Vector similarity |
| Complex queries | claude-sonnet-4-6 | Higher quality results |

## Claude Haiku Integration

```js
// src/services/ai.service.js
import Anthropic from '@anthropic-ai/sdk';

class AIService {
  constructor(apiKey) {
    this.client = new Anthropic({ apiKey });
    this.model = 'claude-haiku-4-5-20251001';
  }

  async classifyBookmark({ title, url }) {
    // Extract domain only (privacy)
    const domain = new URL(url).hostname;

    const response = await this.client.messages.create({
      model: this.model,
      max_tokens: 200,
      messages: [{
        role: 'user',
        content: `Classify bookmark:
Title: ${title}
Domain: ${domain}

JSON response:
{"category":"Technology","tags":["js","tutorial"],"confidence":0.9,"suggested_folder":"Dev"}`
      }]
    });

    return JSON.parse(response.content[0].text);
  }

  async classifyBatch(bookmarks) {
    // 10 per batch for cost efficiency
    const batches = [];
    for (let i = 0; i < bookmarks.length; i += 10) {
      batches.push(bookmarks.slice(i, i + 10));
    }

    const results = [];
    for (const batch of batches) {
      const batchResults = await this.classifyBookmark(batch);
      results.push(...batchResults);
    }
    return results;
  }
}
```

## Privacy Guidelines

### What to Send to AI
```
✅ OK: Bookmark title
✅ OK: Domain name (hostname only)
✅ OK: Page category hints (from URL structure)
❌ NEVER: Full URL path (may contain tokens, IDs)
❌ NEVER: URL query params (may contain personal data)
❌ NEVER: Page content
❌ NEVER: User's name or personal info
```

### Implementation Example
```js
// Safe: only send sanitized data
const safeData = {
  title: bookmark.title,
  domain: new URL(bookmark.url).hostname,
  // NOT: bookmark.url (may have private tokens in path)
};
```

## Consent Flow

```
First AI feature use:
1. Show consent dialog with explanation:
   "Smart Bookmark Manager wants to use Claude AI to classify your bookmarks.
    We will send only bookmark titles and domain names (never full URLs).
    Do you want to enable AI features?"

2. User accepts → save consent flag → proceed
3. User declines → use rule-based fallback → no API calls

Consent stored: chrome.storage.local['bm_ai_consent']
Revoke anytime in settings.
```

## Cost Management

```js
const COST_PER_TOKEN = 0.000001; // Haiku: $1 per 1M tokens
const TOKENS_PER_BOOKMARK = 20;  // Rough estimate

function estimateCost(bookmarkCount) {
  const calls = Math.ceil(bookmarkCount / 10);
  const tokens = calls * 200; // in + out
  return (tokens * COST_PER_TOKEN).toFixed(4);
}

// Example:
// 100 bookmarks → ~10 calls → ~2000 tokens → $0.002
// 1000 bookmarks → ~100 calls → ~20000 tokens → $0.02
```

## Caching Strategy

```js
// Cache in chrome.storage.local
const CACHE_KEY = 'bm_ai_tags';
const CACHE_TTL = 30 * 24 * 60 * 60 * 1000; // 30 days

async function getCached(bookmarkId) {
  const cache = await chrome.storage.local.get(CACHE_KEY);
  const entry = cache[CACHE_KEY]?.[bookmarkId];
  if (!entry) return null;
  if (Date.now() - entry.timestamp > CACHE_TTL) return null; // expired
  return entry.data;
}

async function setCache(bookmarkId, data) {
  const cache = await chrome.storage.local.get(CACHE_KEY) || {};
  cache[CACHE_KEY] = {
    ...cache[CACHE_KEY],
    [bookmarkId]: { data, timestamp: Date.now() }
  };
  await chrome.storage.local.set(cache);
}
```

## Rule-Based Fallback (No API)

Works offline, no cost, reasonable accuracy (~70%):

```js
const DOMAIN_RULES = {
  'github.com': { category: 'Development', tags: ['code'] },
  'stackoverflow.com': { category: 'Development', tags: ['qa'] },
  'youtube.com': { category: 'Entertainment', tags: ['video'] },
  'medium.com': { category: 'Learning', tags: ['article'] },
  'twitter.com': { category: 'Social', tags: ['social'] },
  'x.com': { category: 'Social', tags: ['social'] },
  'linkedin.com': { category: 'Business', tags: ['professional'] },
  'amazon.com': { category: 'Shopping', tags: ['ecommerce'] },
  'figma.com': { category: 'Design', tags: ['design'] },
  'notion.so': { category: 'Tools', tags: ['productivity'] },
  'docs.google.com': { category: 'Tools', tags: ['docs'] },
  'reddit.com': { category: 'Social', tags: ['community'] },
  'news.ycombinator.com': { category: 'Technology', tags: ['tech', 'news'] },
};
```

## MCP Integration (Phase 4)

Claude Code / Claude Desktop can access bookmarks via MCP:
```
Claude: "Find all bookmarks about JavaScript"
→ MCP tool: search_bookmarks("javascript")
→ Returns: [{ title, url, category, tags }]

Claude: "Organize bookmarks into suitable folders"
→ MCP tool: organize_with_ai({ dryRun: true })
→ Returns: proposed folder structure
```
