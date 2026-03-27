---
name: framework-standards
description: High-density coding standards and best practices for major frameworks. Auto-apply when writing code for Next.js, NestJS, FastAPI, Supabase, React, Vue, or other covered frameworks.
---

# Framework Standards — Agent Skills Standard

## What it Does
Cherry-picked from `HoangNguyen0403/agent-skills-standard` (VN developer, 135 releases)
Provides framework-specific best practices that agents apply automatically when coding.

## Covered Frameworks

### Next.js (App Router)
```
✅ Use Server Components by default — Client Components only when needed
✅ Data fetching in Server Components with async/await
✅ Use next/image for images, next/font for fonts
✅ API routes in app/api/[route]/route.ts
✅ Middleware in middleware.ts at root (not in /app)
✅ Use server actions for mutations (not API routes for simple forms)
✅ Environment vars: NEXT_PUBLIC_* for client, server-only for secrets
```

### NestJS
```
✅ Module-per-feature structure
✅ DTOs with class-validator for request validation
✅ Guards for auth, Interceptors for logging/transform
✅ Repository pattern for database access
✅ ConfigModule for environment config
✅ Exception filters at global level
```

### FastAPI (Python)
```
✅ Pydantic models for request/response validation
✅ Async endpoints (async def) for I/O-bound
✅ Dependency injection for DB sessions, auth
✅ APIRouter per domain
✅ Use HTTPException with status_code
✅ Background tasks for non-blocking ops
```

### Supabase
```
✅ Use Row Level Security (RLS) — always enable
✅ Server-side client (createServerClient) for SSR/API
✅ Client-side (createBrowserClient) for UI only
✅ Never expose service_role key to client
✅ Use Supabase Auth helpers for session management
✅ Real-time subscriptions for live data
```

### React
```
✅ Functional components + hooks only
✅ useState for local state, useContext for shared
✅ useMemo/useCallback only when profiler confirms need
✅ Custom hooks for reusable logic (use* prefix)
✅ Error boundaries for resilient UI
```

### Vue 3
```
✅ Composition API (not Options API)
✅ <script setup> syntax
✅ Pinia for state management
✅ defineProps/defineEmits for component contracts
```

## Auto-Apply Rule
When writing code for any covered framework, AUTOMATICALLY apply these standards without waiting for user to ask.

Use with context7 to get real-time docs:
```bash
npx ctx7 docs /vercel/next.js "server components data fetching"
npx ctx7 docs /tiangolo/fastapi "dependency injection database"
```

## Notes
- Source: github.com/HoangNguyen0403/agent-skills-standard | VN developer | 135 releases
- Owner: Dept 1 (Engineering) — apply globally on coding tasks
- Updates: follow repo releases for new framework additions
