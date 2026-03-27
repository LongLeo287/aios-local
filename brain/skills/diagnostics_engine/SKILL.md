---
id: diagnostics_engine
name: Diagnostics Engine
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Full system health audit and project quality scoring (React Doctor style).

accessible_by:
  - Architect
  - Chief of Staff

dependencies:
  - performance_profiler

exposed_functions:
  - name: health_audit
  - name: project_scoring
  - name: generate_diagnostic_report

consumed_by: []
emits_events:
  - health_report_ready
listens_to: []
---
# ðŸ¥ Diagnostics Engine Skill (Project Health Audit)

This skill provides the AI OS with "Clinical Diagnostics" â€” the ability to audit any part of the project for health, performance, and compliance.

## ðŸ› ï¸ Core Functions:
1.  **Health Audit (/audit):**
    - Perform a multi-pass scan of the current directory.
    - Check for: Lint errors, broken links, missing JSDoc, rule violations (from `.agents/rules/`), and context drift.
    - Generate a `health_report.md` with a **Project Health Score (0-100)**.
2.  **Diagnostics Dashboard (/doctor):**
    - A summary of the most critical "Health Bottlenecks" (Inspired by React Doctor).
    - Provide "Auto-Fix" proposals for P1 issues.
3.  **Adherence Tracking:**
    - Monitor how well Agent actions align with the 13 Pillars of the AI OS.

## ðŸ“‹ Instructions:
Before ending a session or starting a major refactor:
1. Run `/audit` on the relevant scope.
2. If Score < 80, trigger the [Self-Correction](/resilience-fix).
3. Update the **Task Receipt** with the Health Score.

## Principle:
*"A healthy codebase is a thinking codebase."*

