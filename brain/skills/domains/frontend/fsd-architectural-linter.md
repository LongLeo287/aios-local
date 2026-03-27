---
name: fsd_architectural_linter
display_name: Feature-Sliced Design Architectural Linter
description: >
  Enforces Feature-Sliced Design (FSD) boundaries in frontend projects.
  Prevents horizontal feature imports, ensures proper layer isolation
  (app/pages/widgets/features/entities/shared), and rejects boundary violations.
version: 1.0.0
author: LongLeo (adapted for AI OS)
tier: 3
category: code-quality
domain: frontend
tags: [fsd, architecture, linter, frontend, react, vue, angular, boundaries]
cost_tier: economy
accessible_by:
  - QA
  - Claude Code
dependencies: []
load_on_boot: false
promoted_from: D:\GA\Workspaces\LongLeo\.claude\skills\
---

# Feature-Sliced Design Architectural Linter

## When to Use
Load for ANY frontend project that uses FSD architecture.
Works with React, Vue, Angular — framework agnostic.

## FSD Layer Hierarchy (strict — lower cannot import higher)

```
app/         ← global config, providers, routing
pages/       ← page compositions
widgets/     ← independent UI blocks
features/    ← user interactions, business logic
entities/    ← business entities (models, api, ui)
shared/      ← reusable utilities, UI kit, constants
```

## Valid Import Rules

```
app      → can import: all layers
pages    → can import: widgets, features, entities, shared
widgets  → can import: features, entities, shared
features → can import: entities, shared
entities → can import: shared only
shared   → NO imports from other layers
```

## Violation Patterns to Reject

```typescript
// VIOLATION: feature importing from another feature
// src/features/cart/ui.tsx
import { useAuth } from '../auth/model'; // ❌ Cross-feature import

// CORRECT: use shared or entities
import { useAuth } from '@/entities/session'; // ✅

// VIOLATION: entity importing from feature
// src/entities/product/api.ts
import { useCart } from '@/features/cart'; // ❌

// VIOLATION: shared importing from entities
// src/shared/ui/Button.tsx
import { UserType } from '@/entities/user'; // ❌
```

## QA Review Checklist

When QA role runs this skill, check these in `src/`:
- [ ] No `features/*` importing from another `features/*`
- [ ] No `entities/*` importing from `features/*` or above
- [ ] No `shared/*` importing from any other layer
- [ ] All cross-cutting logic goes through `shared/`
- [ ] Page components only compose, do not contain business logic

## Auto-Lint Command (if eslint-plugin-fsd installed)

```bash
npx eslint src/ --rule '{"@feature-sliced/layers-slices": "error"}'
```
