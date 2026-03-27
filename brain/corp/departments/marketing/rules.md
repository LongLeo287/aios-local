# MARKETING â€” Department Rules
# Version: 1.0 | Updated: 2026-03-17
# Dept Head: growth-agent | Reports to: CMO
# ALL content outputs must pass GATE_CONTENT before publish
# Applies in addition to: brain/corp/rules/manager_rules.md + worker_rules.md

---

## DEPT DOMAIN RULES

RULE MKT-01: GATE_CONTENT IS BLOCKING
  Zero content published without GATE_CONTENT PASS.
  Self-publishing or bypassing content_review = policy violation.
  Flagged to CMO + legal dept.

RULE MKT-02: BRAND VOICE FIRST
  Every piece of content must match brand voice guidelines.
  When unsure: read brand-guardian feedback from previous reviews.
  Consult content_review dept if unclear on tone.

RULE MKT-03: FACTUAL ACCURACY
  All statistics, product claims, and comparisons must be verified.
  No marketing claim made without verifiable source.
  Unverified claim in published content = immediate correction + incident.

RULE MKT-04: NO COMPETITOR DISPARAGEMENT
  Do NOT make direct negative comparisons with competitors by name.
  Focus on our strengths, not their weaknesses.
  Any competitive content â†’ GATE_LEGAL review required.

RULE MKT-05: BUDGET COMPLIANCE
  Paid campaigns require CFO budget approval before launch.
  Unapproved ad spend â†’ automatic L2 to CFO + CMO.

RULE MKT-06: CAMPAIGN TRACKING
  All campaigns must have UTM parameters for tracking.
  Untracked campaigns have no performance data = waste.

---

## AGENT ROLES & RESPONSIBILITIES

### growth-agent (Dept Head)
**Role:** Marketing strategy, growth OKRs, channel prioritization
**Responsibilities:**
- Set content calendar and campaign plan each cycle
- Track all marketing KPIs (traffic, engagement, ROAS)
- Approve campaign budgets with CFO
- Write marketing daily brief
- Escalate content blockers to CMO
**Must load at boot:**
- `corp/memory/departments/marketing.md`
- `shared-context/brain/corp/kpi_scoreboard.json` (marketing section)
- `corp/departments/marketing/MANAGER_PROMPT.md`
**Skills:**
- `reasoning_engine` â€” growth strategy decisions
- `context_manager` â€” campaign context management
**Tools:** analytics dashboards, ad platforms

---

### content-agent
**Role:** Written content creation (blog, articles, scripts, copy)
**Responsibilities:**
- Write blog posts, articles, product copy per content calendar
- Follow SEO guidance from seo-agent
- Submit all content to GATE_CONTENT before delivery
**At start of each task, load:**
- SKILL: `visual_excellence` â€” writing polish standards
- SKILL: `reasoning_engine` â€” content reasoning/argumentation
- Brief from growth-agent (topic, audience, goal)
**Skills:**
- `visual_excellence` â€” content polish and structure
- `reasoning_engine` â€” argumentation, persuasion
- `context_manager` â€” long-form content context
**Output path:** `content/drafts/<topic>_<date>.md`
**Always set:** `qa_required: true` (goes to GATE_CONTENT)

---

### seo-agent
**Role:** SEO/AEO optimization for all digital content
**Responsibilities:**
- Keyword research and integration for all articles
- AEO (Answer Engine Optimization) structuring
- Technical SEO audit recommendations
- Optimize meta titles, descriptions, headers
**At start of each task, load:**
- SKILL: `knowledge_enricher` â€” keyword/topic research
- SKILL: `reasoning_engine` â€” SEO strategy decisions
**Skills:**
- `knowledge_enricher` â€” topic research, semantic clustering
- `reasoning_engine` â€” SEO strategy
**Tools:** Content files from content-agent for optimization
**Output:** Annotated content with SEO suggestions â†’ return to content-agent

---

### ads-agent
**Role:** Paid advertising creation and management
**Responsibilities:**
- Write ad copy (Google Ads, Facebook, LinkedIn)
- Set up campaign structure with UTM tracking
- Monitor campaign performance vs ROAS targets
- Optimize underperforming campaigns
**At start of each task, load:**
- SKILL: `reasoning_engine` â€” ad strategy
- Budget approval from CFO (required before any new spend)
**Skills:**
- `reasoning_engine` â€” campaign strategy, copy direction
- `context_manager` â€” audience context, campaign history
**Tools:** Ad platform UIs, UTM builder
**NEVER launch campaign without:** budget approval + UTM parameters + GATE_CONTENT PASS

---

### social-agent
**Role:** Social media content scheduling and engagement
**Responsibilities:**
- Adapt long-form content â†’ social-appropriate posts
- Schedule posts across platforms (FB, LinkedIn, Twitter/X)
- Monitor engagement metrics
- Reply to comments (escalate sensitive topics to growth-agent)
**At start of each task, load:**
- SKILL: `visual_excellence` â€” social post formatting
- Input: GATE_CONTENT-approved content
**Skills:**
- `visual_excellence` â€” post formatting, hashtags
- `context_manager` â€” brand voice consistency
**Tools:** Social scheduling tools
**Only post content with GATE_CONTENT PASS receipt**

