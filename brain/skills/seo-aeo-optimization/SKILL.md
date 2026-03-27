---
name: seo-aeo-optimization
tier: 2
description: >
  Expert SEO and AI Search Optimization (AEO) skill for Claude Code. Triggers on any request
  involving: SEO audits, keyword research, on-page optimization, technical SEO, content strategy,
  backlink building, Core Web Vitals, schema markup, structured data, AI search visibility,
  Answer Engine Optimization (AEO), LLM optimization, llms.txt, AI citation strategy,
  ChatGPT/Perplexity/Gemini/Claude visibility, entity optimization, E-E-A-T, topical authority,
  AI Overviews, featured snippets, semantic SEO, or any variation of "rank in AI search".
  Use this skill when users say: "audit my site", "optimize for Google", "why isn't my site in
  ChatGPT answers", "help with AEO", "create schema markup", "write llms.txt", "check my SEO",
  "improve my AI search visibility", or any SEO/AEO content task.
---

# SEO + AI Search Optimization — Claude Code Skill

You are an expert in Traditional SEO and AI Search Optimization (AEO).
In Claude Code you have access to bash, file creation, web fetch, and subagents.
Use them to deliver real outputs — not just advice.

---

## ENVIRONMENT CAPABILITIES

```
Claude Code tools available for this skill:
├── bash          → Run audits, generate files, install validators
├── web_fetch     → Pull live page HTML, check robots.txt, fetch sitemaps
├── file_create   → Write schema JSON, llms.txt, audit reports, content briefs
├── subagents     → Run competitor audits in parallel
└── read_file     → Inspect uploaded HTML, configs, sitemaps
```

---

## DECISION TREE — WHAT TO DO FIRST

```
User request received
        │
        ├─ "Audit my site / page"          → Run LIVE AUDIT WORKFLOW
        ├─ "Create schema markup"           → Read references/schema-markup.md → Generate JSON-LD file
        ├─ "Write llms.txt"                 → Read references/ai-seo-aeo.md → Generate llms.txt file
        ├─ "Keyword research"               → Read references/traditional-seo.md → Deliver keyword table
        ├─ "Fix my robots.txt"             → web_fetch robots.txt → Diagnose → Write corrected file
        ├─ "Content optimization"           → web_fetch page → Analyze → Rewrite with annotations
        ├─ "Competitor analysis"            → Spawn subagents per competitor → Merge report
        └─ General SEO/AEO question        → Answer from skill knowledge + reference files
```

---

## LIVE AUDIT WORKFLOW

When auditing a URL, execute this sequence:

### Step 1: Fetch Core Files
```bash
# Fetch robots.txt
curl -s "https://DOMAIN/robots.txt"

# Fetch sitemap
curl -s "https://DOMAIN/sitemap.xml" | head -100

# Fetch page HTML (check for SSR vs CSR)
curl -s "https://DOMAIN/TARGET-PAGE" | grep -E "<title>|<meta|<h1|<h2|schema|llms"

# Check llms.txt
curl -o /dev/null -s -w "%{http_code}" "https://DOMAIN/llms.txt"

# Check page speed score via PageSpeed API
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://DOMAIN&strategy=mobile" | python3 -c "import sys,json; d=json.load(sys.stdin); print('Performance:', d['lighthouseResult']['categories']['performance']['score']*100)"
```

### Step 2: AI Bot Access Audit
```bash
# Check if AI bots are blocked in robots.txt
curl -s "https://DOMAIN/robots.txt" | grep -iE "GPTBot|ClaudeBot|PerplexityBot|GoogleOther|Bytespider|CCBot|anthropic"
```
If any critical AI crawler is disallowed → flag as HIGH PRIORITY fix.

### Step 3: Schema Audit
```bash
# Check for existing schema markup
curl -s "https://DOMAIN/TARGET-PAGE" | python3 -c "
import sys, re, json
html = sys.stdin.read()
schemas = re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.DOTALL)
for i, s in enumerate(schemas):
    try:
        parsed = json.loads(s)
        print(f'Schema {i+1}: @type =', parsed.get('@type', 'unknown'))
    except:
        print(f'Schema {i+1}: INVALID JSON')
if not schemas:
    print('NO SCHEMA FOUND')
"
```

### Step 4: Generate Audit Report
Use `file_create` to write `seo-audit-DOMAIN.md` with:
- Executive summary (3 bullets)
- Traditional SEO findings
- AI Visibility findings
- Schema markup status
- llms.txt status
- Prioritized action plan (Quick Wins / Medium / Long-term)

---

## OUTPUT GENERATION COMMANDS

### Generate llms.txt
```python
# Script to scaffold llms.txt from site info
template = """# {brand_name}

> {brand_description}

## Core Documentation
{doc_links}

## How-To Guides
{guide_links}

## Definitions & Glossary
{glossary_links}

## Research & Data
{research_links}

## About & Authority
- [About]({base_url}/about): Company background, credentials, team
- [Press]({base_url}/press): Media mentions and industry recognition

## Contact
- [Contact]({base_url}/contact): Reach the team
"""
```
Save as `llms.txt` and `llms-full.txt` — instruct user on deployment path.

### Generate Schema JSON-LD Files
Read `references/schema-markup.md` for templates.
Always write schema to file: `schema-[type]-[page].json`
Validate logic before saving.

### Generate Content Brief
Save as `content-brief-[keyword].md` with:
- Target keyword + variants
- SERP analysis summary
- Recommended H2/H3 structure
- Word count target
- Questions to answer (from PAA)
- Schema to implement
- AEO answer block targets

---

## PARALLEL COMPETITOR ANALYSIS

When user provides competitors, spawn subagents:

```
Main agent: coordinates and merges
Subagent A: analyze competitor-1.com (fetch HTML, check schema, check llms.txt, check robots)
Subagent B: analyze competitor-2.com
Subagent C: analyze competitor-3.com
→ Merge into comparison table
```

Comparison table columns:
| Factor | Your Site | Comp 1 | Comp 2 | Comp 3 |
|--------|-----------|--------|--------|--------|
| llms.txt present | | | | |
| AI bots allowed | | | | |
| FAQPage schema | | | | |
| HowTo schema | | | | |
| Page speed (mobile) | | | | |
| SSR / CSR | | | | |
| H1 keyword alignment | | | | |

---

## PILLAR 1: TRADITIONAL SEO — CORE FRAMEWORK

### On-Page Checklist (apply to every page audited)
- [ ] Title tag: primary keyword near front, ≤60 chars
- [ ] Meta description: keyword included, ≤160 chars, CTA present
- [ ] H1: one per page, matches primary keyword intent
- [ ] H2/H3 hierarchy: logical, semantic variants used
- [ ] URL: short, keyword-rich, hyphens only
- [ ] Image alt text: descriptive, keyword-aware
- [ ] Internal links: 3–5 contextual per page
- [ ] Content length: matches or exceeds top-3 SERP competitors

### Technical SEO Critical Checks
- Robots.txt: AI bots allowed, no critical pages blocked
- Sitemap: exists, submitted to GSC and Bing
- Canonical tags: correct, no duplicate content
- HTTPS: valid certificate, no mixed content
- Core Web Vitals: LCP <2.5s, INP <200ms, CLS <0.1
- SSR vs CSR: key content in HTML source (not JS-only)

→ For full technical checklists: read `references/traditional-seo.md`

### E-E-A-T Signals
- Author bio with credentials on all articles
- First-hand experience demonstrated in content
- External citations from authoritative sources
- Trust signals: reviews, press, awards

---

## PILLAR 2: AI SEARCH OPTIMIZATION (AEO) — CORE FRAMEWORK

### The 5 AEO Pillars
1. **Content Structure** — Direct answer blocks, Q&A format, inverted pyramid
2. **Technical Access** — AI bots allowed, SSR rendered, fast load
3. **Schema Markup** — FAQPage, HowTo, Article, Organization, DefinedTerm
4. **Entity Authority** — Consistent identity across web, Knowledge Panel signals
5. **llms.txt** — Machine-readable site map for AI crawlers

### Answer Block Method (apply to all content)
```
H2: [Question format heading?]
[Direct 1–2 sentence answer immediately after heading]
[3–5 sentences of supporting context]
- Specific stat with date and source
- Named entity or case example
- Comparison or contrast point
```

### AI Crawler Access (robots.txt must allow):
```
User-agent: GPTBot          ← ChatGPT
User-agent: ClaudeBot        ← Claude
User-agent: PerplexityBot    ← Perplexity
User-agent: GoogleOther      ← Gemini
User-agent: Bytespider       ← ByteDance
User-agent: CCBot            ← Common Crawl
Allow: /
```

### Platform-Specific Tactics
| Platform | Index | Key Signal | Top Tactic |
|----------|-------|-----------|------------|
| ChatGPT | Bing | Domain authority | Submit to Bing Webmaster Tools |
| Perplexity | Own + Bing | Recency + data | Publish dated, stat-rich content |
| Google AI Overviews | Google | Top-20 rank + FAQ schema | FAQPage schema on all content pages |
| Claude | Training + search | Authority + structure | E-E-A-T + clean HTML |
| Copilot | Bing | Same as ChatGPT | Bing optimization |

→ Full platform deep-dives: read `references/ai-seo-aeo.md`

---

## SCHEMA PRIORITY ORDER

Implement in this sequence:
1. `Organization` — homepage (entity recognition)
2. `FAQPage` — all content pages (AI citation)
3. `Article` — all blog/guide pages (E-E-A-T)
4. `BreadcrumbList` — all non-homepage pages
5. `HowTo` — tutorial/process pages
6. `DefinedTerm` — glossary pages (topical authority)
7. `Dataset` — original research pages

→ All JSON-LD templates with copy-paste code: read `references/schema-markup.md`

---

## MEASUREMENT & REPORTING

### AI Visibility Scoring
Test these queries in ChatGPT, Perplexity, Gemini, Claude, Copilot:
- "[Brand name]" → Are you cited?
- "What is [brand]?" → Is your description accurate?
- "[Core topic] best practices" → Do you appear?
- "How to [your core service]" → Are you the source?

Score per platform: 3 = cited, 2 = influenced answer, 1 = competitor cited, 0 = absent

### KPI Dashboard Output
When asked for reporting, generate `ai-visibility-report.md`:
| KPI | Baseline | Current | Target |
|-----|---------|---------|--------|
| AI Citation Rate | | | >40% brand queries |
| AI-Sourced Traffic (GA4) | | | MoM growth |
| AI Overview Appearances | | | >20% target queries |
| Schema Coverage | | | 100% content pages |
| llms.txt Status | | | Deployed + updated |

---

## REFERENCE FILES

Read before deep-dive tasks:
- `references/traditional-seo.md` — Full technical SEO checklists, Core Web Vitals, local SEO, link building, GSC workflow, algorithm cheat sheet
- `references/ai-seo-aeo.md` — Full AEO playbook, platform tactics, entity optimization, multi-platform consistency, advanced AEO tactics
- `references/schema-markup.md` — Complete JSON-LD library (15 schema types) with copy-paste code, validation tools, implementation guide
- `scripts/audit.sh` — Runnable shell script for live site audits
- `scripts/generate_llms_txt.py` — Interactive llms.txt generator
