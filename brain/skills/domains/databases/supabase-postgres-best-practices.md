---
name: supabase_postgres_best_practices
display_name: Supabase Postgres Best Practices
description: >
  Best practices for Supabase projects: schema design, RLS policies,
  Edge Functions, real-time subscriptions, and performance optimization.
  Applicable to any project using Supabase as backend.
version: 1.0.0
author: LongLeo/skills.sh (adapted for AI OS)
tier: 3
category: database
domain: databases
tags: [supabase, postgres, database, rls, edge-functions, backend]
cost_tier: economy
accessible_by:
  - Claude Code
  - Developer
  - QA
dependencies: []
load_on_boot: false
promoted_from: D:\GA\Workspaces\LongLeo\.claude\skills\
---

# Supabase Postgres Best Practices

## When to Use
Load when project uses Supabase as backend (auth, database, storage, functions).

## Schema Design

### Naming Conventions
```sql
-- Tables: snake_case plural
CREATE TABLE user_profiles (...);

-- Foreign keys: {table}_{column}
ALTER TABLE orders ADD COLUMN user_id UUID REFERENCES users(id);

-- Timestamps: always include
created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
```

### Row Level Security (RLS)
```sql
-- Always enable RLS on user-facing tables
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Users can only read their own data
CREATE POLICY "users_own_data" ON user_profiles
  FOR SELECT USING (auth.uid() = user_id);

-- Admins can read all
CREATE POLICY "admin_all" ON user_profiles
  FOR ALL USING (auth.jwt() ->> 'role' = 'admin');
```

### Edge Functions
```typescript
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )
  // ... handler logic
  return new Response(JSON.stringify({ data }), {
    headers: { 'Content-Type': 'application/json' }
  })
})
```

## Performance Checklist
- [ ] Add indexes on frequently filtered columns
- [ ] Use `select()` with specific columns (avoid `select *`)
- [ ] Enable connection pooling for serverless
- [ ] Use RPC for complex queries instead of multiple round-trips
