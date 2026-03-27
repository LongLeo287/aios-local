---
name: llm_router
display_name: LLM Router — Cost-Optimized Model Selector
description: >
  Routes AI agent requests to the most cost-effective model based on task type,
  context size, and monthly budget. Implements fallback chains when primary
  models fail. Reads from llm/router.yaml and llm/config.yaml.
  Supports all 5 providers: Anthropic, OpenAI, GLM-5, Kimi K2.5, MiniMax.
version: 1.0.0
tier: 2
category: infrastructure
tags: [llm, routing, cost-optimization, multi-model, fallback, budget]
accessible_by:
  - all_agents
source: D:\Project\AI OS\llm\
exposed_functions:
  - name: route_request
    description: "Given task_type → returns optimal model + provider"
    params: [task_type, context_size_tokens, budget_usd]
  - name: estimate_cost
    description: "Estimate cost for a request before sending"
    params: [model, input_tokens, output_tokens]
  - name: get_cheapest_capable
    description: "Get cheapest model that can handle the task"
    params: [task_type, capabilities_required]
  - name: switch_provider
    description: "Override routing for a session"
    params: [task_type, preferred_model]
  - name: get_budget_status
    description: "Check remaining monthly budget"
corp_integration:
  dept: all
  trigger: "Before any LLM call — route through llm_router first"
  budget_flow: "Budget exhausted → auto-switch to economy tier"
load_on_boot: true
---

# LLM Router

## Purpose

Ensures every agent call uses the **cheapest model that can do the job well**.

## Routing Logic

```
1. Read task_type from request
2. Look up router.yaml → get primary/backup/economy models
3. Check provider circuit breaker (is this provider up?)
4. Check budget remaining
   - If > 90% used → force economy tier
5. Call primary model
   - On fail → fallback_chain.yaml
6. Log cost to telemetry/cost_log.json
```

## Cost Comparison (per 1K tokens, approx)

| Model | Input | Output | Best for |
|-------|-------|--------|---------|
| minimax-text | $0.0003 | $0.0009 | Bulk economy |
| claude-haiku | $0.00025 | $0.00125 | Quick Q&A |
| gpt-4o-mini | $0.00015 | $0.0006 | General economy |
| glm-5 | $0.0014 | $0.0014 | Coding + long ctx |
| kimi-k2.5 | $0.0014 | $0.0014 | Vision + agents |
| claude-sonnet | $0.003 | $0.015 | Premium coding |
| claude-opus | $0.018 | $0.09 | Complex reasoning |

## Dept Defaults

- Engineering/QA → claude-3.7 → glm-5 → gpt-4o-mini
- Marketing/Support → claude-haiku → minimax-text
- Strategy → claude-opus → gpt-4o
- Operations → gpt-4o-mini → claude-haiku
