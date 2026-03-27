---
name: cost_manager_skill
display_name: AI Cost & Model Routing Manager
description: >
  Universal skill for managing AI inference costs in agent systems.
  Covers model routing strategies (fast/standard/premium tiers),
  token estimation, cost tracking, and budget policies.
  Applicable to any project using LLM APIs.
version: 1.0.0
author: LongLeo/cfo-agent (adapted concept for AI OS — values removed)
tier: 3
category: governance
domain: finance
tags: [cost, model-routing, tokens, budget, llm, optimization]
cost_tier: economy
accessible_by:
  - Antigravity
  - Claude Code
dependencies:
  - context_manager
load_on_boot: false
promoted_from: D:\GA\Workspaces\LongLeo\.ai-core\governance\
---

# AI Cost & Model Routing Manager

## When to Use
Load when a project has significant AI inference costs and needs:
- Controlled model selection per task type
- Token budget enforcement
- Cost reporting across sessions

## Model Routing Strategy (70/20/10)

```
70% → Fast/Economy model   (simple, repetitive tasks)
20% → Standard model       (reasoning, code review)
10% → Premium model        (critical decisions, complex code)
```

### Task Classification

| Task Type | Recommended Tier | Examples |
|-----------|-----------------|---------|
| Data lookup, formatting | Economy | Registry queries, JSON transforms |
| Code generation, review | Standard | DEVELOPER/QA roles |
| Architecture decisions | Premium | Plan approval, BLOCKED resolution |
| User-facing reports | Standard | Phase 6 Mermaid report |

## Token Estimation Formula

```
Rough estimate before calling LLM:
  input_tokens  ≈ (input_chars / 4)
  output_tokens ≈ expected_output_chars / 4
  total_cost_usd = (input_tokens * input_price) + (output_tokens * output_price)

For Claude Sonnet 3.5:
  input: $3/1M tokens
  output: $15/1M tokens
```

## Budget Policy Template (Customize Per Project)

```json
{
  "daily_limit_usd": 5.00,
  "session_limit_usd": 2.00,
  "step_limit_tokens": 8000,
  "alert_threshold_pct": 80,
  "on_exceed": "WARN | BLOCK | ESCALATE"
}
```

## Cost Receipt Format (Add to telemetry/receipts/)

```json
{
  "receipt_type": "COST",
  "task_id": "...",
  "step_id": "...",
  "model_used": "claude-sonnet-3-5",
  "tier": "standard",
  "input_tokens": 1250,
  "output_tokens": 480,
  "estimated_cost_usd": 0.0111,
  "timestamp": "..."
}
```
