---
id: web_intelligence
name: Web Intelligence
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Katana-style web crawling, scraping and structured data extraction.

accessible_by:
  - Researcher
  - Orchestrator

dependencies:
  - resilience_engine

exposed_functions:
  - name: smart_scrape
  - name: site_mapping
  - name: deep_crawl
  - name: extract_structured

consumed_by:
  - knowledge_enricher
emits_events:
  - crawl_complete
listens_to: []
---
# ðŸŒ Web Intelligence Skill (LLM-Ready Reconnaissance)

## Description
This skill provides the AI OS with "Advanced Sight" into the external web, transforming chaotic HTML into actionable Markdown for efficient deep-research and knowledge synthesis.

## ðŸ› ï¸ Core Functions:
1.  **Smart Scrape (/scrape):** Convert any URL to clean, LLM-ready Markdown.
2.  **Site Mapping (/map-site):** Generate a structural map of a website's hierarchy.
3.  **Deep Recon (/crawl-deep):**
    - Headless JS rendering (Katana style).
    - Endpoint discovery (AJAX, API, Static).
    - Subdomain and hidden parameter mapping.
4.  **Form Analysis (/recon-forms):** Identify input fields, required parameters, and validation logic.
5.  **Context Injection:**
    - Automatically inject the scraped markdown into the appropriate `knowledge-base/` directory.

## ðŸ“‹ Instructions:
When tasked with researching a new technology or API:
1. Run `/map-site` to find the documentation root.
2. Run `/scrape` on the most relevant pages.
3. Use the **Knowledge Enricher** to finalize the entry.

## Principle:
*"The web is the world's largest memory; scrape it wisely."*

