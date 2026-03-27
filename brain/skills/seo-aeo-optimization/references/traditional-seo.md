# Traditional SEO — Deep Reference

## TABLE OF CONTENTS
1. [Technical SEO Checklists](#technical-seo)
2. [Core Web Vitals](#core-web-vitals)
3. [On-Page Deep Dive](#on-page)
4. [Content Strategy](#content)
5. [Local SEO](#local)
6. [Link Building Tactics](#links)
7. [Google Search Console Workflow](#gsc)
8. [Algorithm Updates Cheat Sheet](#algorithms)

---

## 1. TECHNICAL SEO CHECKLISTS {#technical-seo}

### Crawlability
- [ ] robots.txt exists and is valid (`/robots.txt`)
- [ ] Sitemap submitted to Google Search Console and Bing Webmaster
- [ ] Sitemap.xml is dynamic/auto-updating for large sites
- [ ] Crawl budget not wasted on paginated, filtered, or session-ID URLs
- [ ] No orphan pages (every page reachable within 3 clicks from homepage)
- [ ] No redirect chains longer than 2 hops
- [ ] Canonical tags correct (self-referencing on all canonical pages)
- [ ] Noindex audit: paginated pages, thin content, filtered URLs, thank-you pages, admin pages should be noindexed
- [ ] Hreflang implemented if multilingual (x-default + all language variants)
- [ ] JavaScript: key content in HTML source (not JS-rendered only)

### Site Architecture
- [ ] Flat architecture (most pages ≤3 clicks from homepage)
- [ ] URL structure: `/category/subcategory/page-name/` (logical hierarchy)
- [ ] Consistent internal linking (pillar → cluster → pillar)
- [ ] Breadcrumbs on all non-homepage pages
- [ ] Pagination: `rel="next"` / `rel="prev"` OR paginated content on single URL with lazy load
- [ ] 404 page is custom and links to key sections

### Security & Infrastructure
- [ ] HTTPS on all pages (no mixed content warnings)
- [ ] SSL certificate valid and auto-renewing
- [ ] www vs. non-www canonical redirect in place
- [ ] HTTP → HTTPS redirect (301) on all pages
- [ ] CDN in place for assets
- [ ] Server location matches primary target audience (or CDN covers it)

---

## 2. CORE WEB VITALS {#core-web-vitals}

### LCP — Largest Contentful Paint (Target: <2.5 seconds)
**What it measures:** How fast the largest visible element loads (hero image, H1, video)

**Fixes:**
- Preload hero images: `<link rel="preload" as="image" href="hero.jpg">`
- Convert images to WebP/AVIF format
- Use a CDN for images
- Eliminate render-blocking resources (move CSS inline for critical path, defer non-critical JS)
- Upgrade hosting or use edge delivery

### INP — Interaction to Next Paint (Target: <200ms)
**What it measures:** How fast the page responds to user interactions

**Fixes:**
- Break up long JavaScript tasks (>50ms) into smaller chunks
- Use `requestIdleCallback` for non-critical JS
- Avoid large DOM sizes (>1,400 elements)
- Minimize third-party scripts

### CLS — Cumulative Layout Shift (Target: <0.1)
**What it measures:** How much content moves unexpectedly during page load

**Fixes:**
- Set explicit width/height attributes on all images and videos
- Reserve space for ads and embeds
- Avoid inserting content above existing content after load
- Use `font-display: optional` or preload fonts

### Measurement Tools
- Google Search Console → Core Web Vitals report (field data)
- PageSpeed Insights (lab + field data)
- web.dev/measure (Lighthouse)
- Chrome DevTools → Performance tab
- CrUX Dashboard (Google Data Studio)

---

## 3. ON-PAGE DEEP DIVE {#on-page}

### Title Tag Formula
```
Primary Keyword | Secondary Keyword | Brand Name
OR
[Action] [Primary Keyword]: [Benefit/Hook] | Brand
```
- Hard limit: 60 characters (580px rendering width)
- Put most important keyword near the front
- Don't keyword-stuff; write for CTR first

### Meta Description Formula
```
[Address the query intent]. [Unique value proposition]. [CTA] → [Brand].
```
- 150–160 characters (can go up to 300 for mobile)
- Include target keyword (appears bolded in SERP)
- Every page needs a unique meta description

### Header Hierarchy
```
H1 — One per page. Contains primary keyword. Matches page intent.
 └─ H2 — Major sections. Include semantic/related keywords.
     └─ H3 — Subsections. Support H2 topic.
         └─ H4 — Further breakdown (rarely needed)
```

### Content Optimization Process
1. **SERP analysis**: Search target keyword, analyze top 10 results
   - What content types rank? (guides, listicles, tools, product pages)
   - Average word count of top 3
   - Common headings and topics covered
   - Questions in "People Also Ask"
2. **Semantic keyword research**: Use LSIGraph, Clearscope, Surfer SEO, or NLP tools
3. **Content brief**: Outline headings, target word count, keywords to include, questions to answer
4. **Write**: Answer the primary query in first 100 words; expand with depth and supporting info
5. **Optimize**: Add LSI keywords, improve readability (Flesch score), add media

### Readability Standards
- Flesch Reading Ease: 60–70 for general audience, 50–60 for professional
- Sentences: avg 15–20 words
- Paragraphs: 3–5 sentences max
- Use subheadings every 300 words
- Use bold for key terms and callouts
- Include images/media every 500 words

---

## 4. CONTENT STRATEGY {#content}

### E-E-A-T Signals (Experience, Expertise, Authoritativeness, Trustworthiness)

**Experience:**
- First-hand case studies ("We ran this test and found...")
- Original data from your customer base
- Behind-the-scenes content
- Dated content with documented history

**Expertise:**
- Author bio with credentials, certifications, years of experience
- Inline citations to primary research
- Deep coverage of subtopics (not surface-level)
- FAQ sections addressing expert-level questions

**Authoritativeness:**
- Backlinks from high-DA domains in your niche
- Mentions in industry press
- Guest posts on respected platforms
- Speaking engagements, podcasts cited on page

**Trustworthiness:**
- Privacy policy, terms of service, contact page easily accessible
- SSL certificate
- Review widgets (Google, Trustpilot, G2)
- No misleading claims; source all statistics

### Content Calendar Framework
```
Monthly cadence per pillar:
- 1 Pillar page update/refresh
- 2 Cluster articles (long-form, 1,500+ words)
- 2 Supporting posts (targeted, 800–1,200 words)
- 1 Data/research piece (quarterly)
```

### Content Refresh Process
1. Pull GSC data: find pages dropping in rank over 90 days
2. Check current SERP: has content type changed?
3. Identify gaps vs. current top-rankers
4. Update: add missing sections, refresh outdated stats, improve internal links
5. Update publish date ONLY if substantial changes made

---

## 5. LOCAL SEO {#local}

### Google Business Profile Optimization
- [ ] Claimed and verified
- [ ] Business name matches NAP exactly
- [ ] Primary category is specific (not just "Business")
- [ ] All secondary categories filled in
- [ ] Hours accurate (including holidays)
- [ ] Photos: exterior, interior, team, products (min 10)
- [ ] Posts: weekly or biweekly updates
- [ ] Q&A section: seed with common questions + answers
- [ ] Respond to ALL reviews (positive and negative)

### NAP Consistency
Name, Address, Phone must be identical across:
- Website (footer + contact page)
- Google Business Profile
- Bing Places
- Apple Maps
- Yelp, Foursquare
- Industry directories
- Social profiles

### Local Citation Building
Priority citation sites by category:
- **General**: Yelp, BBB, Foursquare, YellowPages, Manta
- **Industry-specific**: Find via Whitespark or BrightLocal citation finder
- **Chamber of commerce**: City/region business directory

### Local Content Strategy
- Landing pages per city/service area: `/[service]/[city]/`
- Local events, news, case studies featuring local clients
- FAQ pages addressing local intent queries

---

## 6. LINK BUILDING TACTICS {#links}

### Tier 1: Editorial (Highest Value)
- **Digital PR**: Create original research, surveys, data studies → pitch to journalists
- **HARO/Connectively**: Respond to journalist source requests daily
- **Reactive PR**: Comment on trending news with expert quotes
- **Podcast appearances**: Get mentioned in episode show notes

### Tier 2: Relationship-Based
- **Guest posting**: Pitch unique data-driven articles to DA40+ sites in niche
- **Expert roundups**: Contribute expert quotes to compilation articles
- **Resource page outreach**: Find `/resources` or `/links` pages; pitch inclusion
- **Broken link building**: Find broken links on competitor sites; offer your page as replacement

### Tier 3: Content-Driven
- **Skyscraper technique**: Outperform top-linked content; outreach to those who linked to inferior version
- **Link reclamation**: Find unlinked mentions of your brand → request link addition
- **Scholarship pages**: Create scholarship page; submit to university `.edu` pages

### Link Quality Assessment
Good links:
- Relevant domain (same or adjacent industry)
- DA/DR 30+
- Real traffic (check Ahrefs/SimilarWeb)
- Contextual placement (within body content, not footer/sidebar)
- Followed (not `rel="nofollow"` or `rel="sponsored"`)

Avoid / disavow:
- PBN links (private blog networks)
- Link farms
- Irrelevant niche sites
- Links from penalized domains

---

## 7. GOOGLE SEARCH CONSOLE WORKFLOW {#gsc}

### Monthly Review Checklist
1. **Coverage report**: Fix all "Error" pages; review "Excluded" for legitimacy
2. **Core Web Vitals**: Fix all "Poor" URLs; improve "Needs Improvement"
3. **Performance → Queries**: Find high-impression / low-CTR queries (CTR <3%) → improve title/meta
4. **Performance → Pages**: Find declining pages → schedule for content refresh
5. **Manual Actions**: Verify none exist
6. **Links**: Review top linked pages; identify link gaps

### Quick Wins via GSC
- **High impression, low CTR (<2%)**: Rewrite title tag to be more compelling
- **Position 5–15, high volume**: Content needs optimization to break into top 5
- **Queries with no dedicated page**: Create new content targeting that query
- **Mobile usability errors**: Fix responsive design issues flagged

---

## 8. ALGORITHM UPDATES CHEAT SHEET {#algorithms}

| Update | Core Focus | Winning Strategy |
|--------|-----------|-----------------|
| Helpful Content | Originality, human-first | Write for users, not search engines |
| E-E-A-T Updates | Trust & expertise | Author credentials, original research |
| Core Updates | Overall quality | Comprehensive E-E-A-T improvements |
| Page Experience | Core Web Vitals | LCP/INP/CLS optimization |
| Product Reviews | Depth & originality | Test products; show real experience |
| Spam Updates | Link spam, thin content | Audit links; remove thin pages |
| Local Search | Proximity, relevance | GBP optimization, local citations |

**When hit by a core update:**
1. Don't make panic changes — wait 2 weeks for full rollout
2. Audit affected pages vs. winners: what do winners have that you don't?
3. Focus on E-E-A-T improvements
4. Content refresh + internal link improvement
5. Recovery often comes in the next core update (3–6 months)
