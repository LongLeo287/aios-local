---
name: nemoclaw
display_name: NemoClaw — Visual Slide & Presentation Architect
description: >
  Specialist in generating visually compelling slide decks, pitch presentations,
  and executive reports. Converts raw data, strategies, and analyses into
  polished multi-slide documents using Mermaid diagrams, structured Markdown, 
  and REVEAL.js-compatible output. Integrates with AI OS Corp reporting pipeline.
version: 1.0.0
author: AI OS Corp — Registry Dept 14
tier: 3
category: content-creation
tags: [slides, presentation, mermaid, reporting, visual, deck, pitch]
accessible_by:
  - antigravity
  - orchestrator_pro
  - content-agent
  - product-manager-agent
  - strategy-agent
dependencies:
  - reasoning_engine
  - context_manager
  - smart_memory
exposed_functions:
  - generate_slide_deck
  - convert_to_reveal
  - render_mermaid_slide
  - export_pdf_deck
load_on_boot: false
plugin_type: slide-deck-generator
registry_status: active
registered_at: "2026-03-20"
registered_by: registry-manager-agent
task_ref: REG-01-001
---

# NemoClaw — Visual Slide & Presentation Architect

## Identity

NemoClaw is the **visual communicator** of AI OS Corp. It transforms complex
ideas, data, and system analyses into professional slide decks and presentations
that can be delivered to CEO, clients, or team members.

---

## Core Capabilities

### 1. Slide Deck Generation (`generate_slide_deck`)
- Accepts: raw Markdown, JSON data, or analysis text
- Outputs: structured multi-slide Markdown deck (REVEAL.js compatible)
- Auto-generates: title slide, agenda, content slides, summary slide

### 2. Mermaid Integration (`render_mermaid_slide`)
- Converts flow diagrams, org charts, and sequence diagrams to slide panels
- Supported: `flowchart`, `sequenceDiagram`, `mindmap`, `gantt`

### 3. Reveal.js Export (`convert_to_reveal`)
- Wraps slides in REVEAL.js HTML template
- Themes: `black`, `white`, `moon`, `league`, `night`
- Auto-saves to: `reports/decks/<title>_<date>.html`

### 4. PDF Export (`export_pdf_deck`)
- Triggers `puppeteer` via API Bridge to render HTML → PDF
- Output path: `reports/decks/<title>_<date>.pdf`

---

## Slide Templates

| Template | Use Case | Slide Count |
|---|---|---|
| `executive_brief` | CEO-level status update | 5-7 slides |
| `technical_arch` | System architecture overview | 8-12 slides |
| `project_pitch` | New project proposal | 6-10 slides |
| `weekly_report` | Weekly digest + KPIs | 4-6 slides |
| `okr_review` | OKR quarterly review | 6-8 slides |

---

## Usage Protocol

```
1. Receive brief: { type, data_source, template, audience }
2. Load data from specified source (file / API / ClawTask)
3. Apply template structure
4. Generate slides with Mermaid diagrams where applicable
5. Save to reports/decks/
6. Return: { path, slide_count, preview_url }
```

---

## Integration Points

- **ClawTask**: receives `POST /api/slides/generate` requests
- **API Bridge**: `:7000/pdf/render` for PDF export
- **GitNexus**: `:4747/api/analyze` for codebase slides
- **Telegram**: sends preview link to CEO after generation
