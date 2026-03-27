---
id: accessibility_grounding
name: Accessibility Grounding
version: 1.1.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: WCAG compliance and Accessibility Tree parsing for efficient web control.

accessible_by:
  - QA
  - UX

dependencies:
  - visual_excellence

exposed_functions:
  - name: wcag_check
  - name: screen_reader_simulation
  - name: parse_accessibility_tree

consumed_by: []
emits_events: []
listens_to: []
---
# â™¿ Accessibility Grounding Skill (Efficient Web Control)

This skill optimizes web interaction by using Accessibility Tree parsing instead of raw HTML, inspired by the `PinchTab` protocol.

## ðŸ› ï¸ Core Functions:
1.  **Token Efficiency:**
    - Convert complex web pages into streamlined Accessibility Trees.
    - Reduce context usage from 10k+ tokens to <800 tokens per page.
2.  **Stable Referencing:**
    - Assign stable ID references (e.g., `e1`, `e2`) to interactive elements to prevent "flaky selector" errors.
3.  **Human-like Orchestration:**
    - Simulate realistic user behavior (Cubic Bezier mouse movements, keystroke jitter).
    - Manage multi-instance Chrome profiles for persistent sessions.

## ðŸ“‹ Instructions:
- Always prioritize the Accessibility Tree view when browsing for data.
- Use `humanClick` and `humanType` for high-fidelity browser automation.

## Principle:
*"See only what matters. Act with human precision."*

