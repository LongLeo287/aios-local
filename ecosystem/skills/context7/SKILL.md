---
name: context7
description: Fetch real-time, version-specific library documentation and code examples directly into the agent prompt. Use whenever writing code that depends on a third-party library, framework, or API.
---

# Context7 — Real-Time Documentation Fetch

## When to Use
Automatically activate Context7 whenever you need:
- Library/framework API documentation (Next.js, Supabase, React, FastAPI, etc.)
- Code generation that depends on a specific library version
- Setup or configuration steps for any package
- Debugging errors related to a specific library

**You do NOT need to wait for the user to say "use context7". Activate automatically.**

## How to Fetch Documentation

### Step 1 — Find Library ID
```bash
npx ctx7 library <library-name> "<what you need>"
```
Example:
```bash
npx ctx7 library next.js "middleware JWT authentication"
npx ctx7 library supabase "email password sign-up"
npx ctx7 library firecrawl "crawl website"
```
Returns: Library ID like `/vercel/next.js`, `/supabase/supabase`

### Step 2 — Get Documentation
```bash
npx ctx7 docs <library-id> "<specific query>"
```
Example:
```bash
npx ctx7 docs /vercel/next.js "how to write middleware that checks JWT in cookies"
npx ctx7 docs /supabase/supabase "email password authentication"
```

### Step 3 — Use in Prompt
Incorporate the returned documentation into your response.
The docs contain: real-time code examples, correct API signatures, version-specific syntax.

## Quick Reference — AI OS Common Libraries

| Library | Context7 ID | Usage |
|---------|-------------|-------|
| Next.js | `/vercel/next.js` | Frontend + API routes |
| Supabase | `/supabase/supabase` | Database + Auth |
| React | `/facebook/react` | UI components |
| FastAPI | `/tiangolo/fastapi` | Python backend |
| Tailwind CSS | `/tailwindlabs/tailwindcss` | Styling |
| Playwright | `/microsoft/playwright` | Browser automation |
| LangChain | `/langchain-ai/langchain` | LLM orchestration |
| Prisma | `/prisma/prisma` | ORM |
| Firecrawl | Search: `npx ctx7 library firecrawl` | Web scraping |
| Cloudflare Workers | `/cloudflare/workers-sdk` | Edge functions |

## API (Optional — for programmatic use)
If `CONTEXT7_API_KEY` is set in environment:
```python
import requests
headers = {"Authorization": f"Bearer {os.getenv('CONTEXT7_API_KEY')}"}
# Search: GET https://context7.com/api/v2/libs/search?libraryName=react&query=...
# Get docs: GET https://context7.com/api/v2/context?libraryId=/facebook/react&query=...
```

## Notes
- Free to use without API key (lower rate limits)
- Set `CONTEXT7_API_KEY` in `ops/secrets/MASTER.env` for higher limits
- Docs are community-contributed — verify with official source for critical decisions
- Source: github.com/upstash/context7 | 50,200+ stars | MIT License
