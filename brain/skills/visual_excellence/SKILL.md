---
id: visual_excellence
name: Visual Excellence
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Cinematic UI generation and Apple-style premium visual storytelling.

accessible_by:
  - Designer
  - UX

dependencies: []

exposed_functions:
  - name: ui_audit
  - name: style_guide_enforcement
  - name: cinematic_layout
  - name: generate_palette

consumed_by:
  - accessibility_grounding
emits_events: []
listens_to: []
---
# âœ¨ Visual Excellence Skill (Cinematic UI)

## Description
This skill ensures all AI OS products (Dashboard, Popup, Reports) achieve a "WOW" effect through cinematic, scroll-driven storytelling and high-impact visual design.

## ðŸ› ï¸ Core Functions:
1.  **Cinematic Storytelling:**
    - Use `<Scene>` and `<ScrollTransform>` components for smooth, Apple-style transitions.
    - Implement `TextReveal` for high-impact briefing documents.
2.  **Performance-First Motion:**
    - Keep animation logic lightweight (<1KB core).
    - Prioritize CSS Scroll Timeline for GPU-accelerated performance.
3.  **Visual Hierarchy:**
    - Use 3D perspectives and parallax to guide the user's attention to key insights.

## ðŸ“‹ Instructions:
- When building the Dashboard, ensure every interaction feels fluid and "premium."
- Respect `prefers-reduced-motion` settings.
- Use scaffolding for "Case Study" or "Product Launch" styles when generating final project reports.

## Principle:
*"Design is not just what it looks like; it's how it moves."*

