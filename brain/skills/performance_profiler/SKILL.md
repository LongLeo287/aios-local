---
id: performance_profiler
name: Performance Profiler
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Latency auditing, resource tracking and performance bottleneck detection.

accessible_by:
  - Dev
  - QA

dependencies: []

exposed_functions:
  - name: audit_latency
  - name: track_resources
  - name: generate_profile_report

consumed_by:
  - diagnostics_engine
emits_events:
  - profile_ready
listens_to: []
---
# â±ï¸ Performance Profiler Skill (Agent Observability)

This skill enables continuous profiling of the Digital Workforce, identifying bottlenecks in execution and resource usage.

## Capabilities:
1. **Session Auditing:** Count tool calls, file reads, and character counts per session.
2. **Context Monitoring:** Alert when the context window is >70% full, recommending a `/compact` or state preservation.
3. **Bottleneck Identification:** Document steps that take >3 retries or multiple tool failures.

## ðŸ“‹ Instructions:
Every 5-10 tool calls, or at the end of a session:
1. Generate a **Session Profile Snapshot** in `.agents/telemetry/profiles/`.
2. Format the snapshot as a "Logic Flame Graph" (Indented list showing nested tool calls and durations).
3. If a specific skill (e.g., `Reasoning Engine`) is consuming too much time without output, flag it for "Refactoring" in `memory/long-term/`.

## Principle:
*"Measurement is the first step toward optimization."*

