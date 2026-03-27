---
name: UI-UX Skills
description: Container namespace for all UI/UX skill collections in AI OS. Currently hosts ui-ux-pro-max sub-collection. Provides design system references, component patterns, and interaction design skills.
department: engineering, rd
tier: 2
category: design
status: active
tags: [ui, ux, design, frontend, components, interaction]
---

# UI-UX Skills

**Repo:** `brain/skills/ui-ux`
**Type:** Skill namespace / container
**Department:** Engineering / R&D
**Tier:** 2

## What it is

Namespace container for all UI/UX related skill collections. Currently houses:

### Sub-collections
| Dir | Contents |
|-----|---------|
| `ui-ux-pro-max/` | Pro-grade UX skills: data + scripts for systematic UI analysis |

## Usage

All UI/UX skills in this namespace are accessible via:
- ClawTask Knowledge Browser → ui-ux files
- `FAST_INDEX.json` category: `design`
- Agent skill query: `GET /api/aios/skills?category=design`

## AI OS Integration
- **Owner dept:** Engineering + R&D joint
- **ClawTask:** Skills & Plugins panel → UI/UX category
- **Used by:** Frontend agent, UI-UX pro-max analysis scripts
