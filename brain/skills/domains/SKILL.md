---
name: Domain Skills Library
description: Multi-domain skill reference collection covering ai-integration, databases, finance, frontend, google-workspace, and POS systems. Each domain contains reference docs, best practices, and agent skill blueprints.
department: engineering, rd, finance, operations
tier: 2
category: knowledge
status: active
tags: [domains, reference, ai, database, frontend, finance, google, pos]
---

# Domain Skills Library

**Repo:** `brain/skills/domains`
**Type:** Knowledge base / skill blueprints
**Department:** Cross-functional (Engineering, Finance, Ops)
**Tier:** 2 — reference and blueprint ready

## What it is

A structured library of domain-specific skill references across 6 business/technical domains. Each domain directory contains reference documents, best-practice guides, and agent skill blueprints.

## Domains

### `ai-integration/`
| File | Content |
|------|---------|
| `agentic-architectures-reference.md` | Multi-agent architectures, orchestration patterns |
| `vercel-ai-sdk-reference.md` | Vercel AI SDK integration for Next.js |

### `databases/`
| File | Content |
|------|---------|
| `prisma-orm-reference.md` | Prisma ORM with TypeScript, migrations |
| `supabase-postgres-best-practices.md` | Supabase performance, RLS, indexing |
| `supabase-agent-skills/` | Supabase agent skill sub-collection |

### `finance/`
| File | Content |
|------|---------|
| `cost-manager-skill.md` | AI cost optimization, budget firewall |
| `edge-compute-patterns.md` | Edge computing cost efficiency |

### `frontend/`
| File | Content |
|------|---------|
| `antd-reference.md` | Ant Design component reference |
| `fsd-architectural-linter.md` | Feature-Sliced Design linter |
| `hitl-gateway-enforcer.md` | Human-in-the-loop gateway patterns |
| `shadcn-ui-reference.md` | shadcn/ui component library reference |

### `google-workspace/`
| File | Content |
|------|---------|
| `gas-skill.md` | Google Apps Script skill blueprint |
| `sheets-performance-optimization.md` | Google Sheets optimization |
| `sheets-skill.md` | Sheets agent skill |

### `pos/`
| File | Content |
|------|---------|
| `pos-event-sourcing-auditor.md` | POS system event sourcing + audit trail |

## AI OS Integration
- **Used by:** All dept agents for domain-specific guidance
- **Knowledge Browser:** Accessible via ClawTask Knowledge Browser panel
- **FAST_INDEX:** Each domain's key docs indexed in FAST_INDEX.json
- **Agent query:** `GET /api/brain/knowledge/read?file=<filename>`
