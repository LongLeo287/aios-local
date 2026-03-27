---
id: prisma_orm_reference
name: Prisma ORM Reference
version: 1.0.0
tier: 3
domain: databases
cost_tier: standard
status: draft
author: AI OS (adapted from prisma/prisma docs)
updated: 2026-03-14
source: https://github.com/prisma/prisma
warning: UNVERIFIED — written from AI training data, not fetched from official docs. Verify before production use.
tags: [prisma, orm, database, postgresql, mysql, sqlite, typescript, migrations]
accessible_by:
  - Antigravity
  - Claude Code
  - Developer
exposed_functions:
  - name: get_schema_pattern
    description: Return Prisma schema pattern for a data model
    input: model description
    output: schema definition
  - name: get_query_pattern
    description: Return Prisma client query for a use case
    input: query description (find, create, update, etc.)
    output: Prisma client code
  - name: get_migration_command
    description: Return migration CLI commands
    input: migration scenario
    output: CLI commands
load_on_boot: false
---

# Prisma ORM — AI OS Reference Skill

> Source: https://github.com/prisma/prisma | https://www.prisma.io
> Type-safe database client for TypeScript and Node.js

## Overview

- **What**: ORM with auto-generated type-safe client from schema
- **Databases**: PostgreSQL, MySQL, SQLite, MongoDB, CockroachDB, SQL Server
- **Main Features**: Schema definition, Migrations, Type-safe queries, Prisma Studio

---

## Installation

```bash
npm install prisma @prisma/client
npx prisma init              # Creates prisma/schema.prisma + .env
```

---

## Schema Definition

```prisma
// prisma/schema.prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"      // or "mysql", "sqlite", "mongodb"
  url      = env("DATABASE_URL")
}

// === MODELS ===

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  role      Role     @default(USER)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  // Relations
  posts     Post[]
  profile   Profile?

  @@map("users")  // Table name override
}

model Profile {
  id     String @id @default(cuid())
  bio    String?
  avatar String?

  userId String @unique
  user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)
}

model Post {
  id          String   @id @default(cuid())
  title       String
  content     String?
  published   Boolean  @default(false)
  viewCount   Int      @default(0)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  authorId    String
  author      User     @relation(fields: [authorId], references: [id])

  tags        Tag[]    @relation("PostToTag")
  categories  Category[]

  @@index([authorId])
  @@index([createdAt])
}

model Tag {
  id    String @id @default(cuid())
  name  String @unique
  posts Post[] @relation("PostToTag")
}

model Category {
  id    Int    @id @default(autoincrement())
  name  String @unique
  posts Post[]
}

// === ENUMS ===

enum Role {
  USER
  ADMIN
  MODERATOR
}
```

### Field Types

| Prisma Type | TypeScript Type | DB Type (PG) |
|-------------|-----------------|--------------|
| `String` | `string` | `text` |
| `Int` | `number` | `integer` |
| `Float` | `number` | `double precision` |
| `BigInt` | `bigint` | `bigint` |
| `Boolean` | `boolean` | `boolean` |
| `DateTime` | `Date` | `timestamp` |
| `Json` | `Prisma.JsonValue` | `jsonb` |
| `Bytes` | `Buffer` | `bytea` |
| `Decimal` | `Prisma.Decimal` | `decimal` |

### Common Attributes

```prisma
@id                         → Primary key
@unique                     → Unique constraint
@default(value)             → Default value
@default(now())             → Current timestamp
@default(autoincrement())   → Auto-increment INT
@default(cuid())            → CUID string ID
@default(uuid())            → UUID string ID
@updatedAt                  → Auto-update timestamp
@map("column_name")         → Column name override
@@map("table_name")         → Table name override
@@index([field1, field2])   → Composite index
@@unique([field1, field2])  → Composite unique
```

---

## Migrations

```bash
# Create + apply migration (development)
npx prisma migrate dev --name add_user_table

# Apply migrations (production)
npx prisma migrate deploy

# Reset database (development only — DESTROYS DATA)
npx prisma migrate reset

# View migration status
npx prisma migrate status

# Generate client after schema change
npx prisma generate

# Open Prisma Studio (visual DB browser)
npx prisma studio
```

---

## Prisma Client Queries

### Setup
```ts
import { PrismaClient } from '@prisma/client';

// Singleton pattern (important for Next.js)
const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  log: ['query'],  // Optional: log all queries
});

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}
```

### CREATE

```ts
// Create one
const user = await prisma.user.create({
  data: {
    email: 'user@example.com',
    name: 'Alice',
    profile: {
      create: {              // Nested create
        bio: 'Developer',
      },
    },
  },
  include: { profile: true },  // Return with profile
});

// Create many
await prisma.user.createMany({
  data: [
    { email: 'a@example.com', name: 'Alice' },
    { email: 'b@example.com', name: 'Bob' },
  ],
  skipDuplicates: true,
});
```

### READ

```ts
// Find unique
const user = await prisma.user.findUnique({
  where: { email: 'user@example.com' },
  include: {
    posts: { where: { published: true }, orderBy: { createdAt: 'desc' } },
    profile: true,
  },
});

// Find first matching
const post = await prisma.post.findFirst({
  where: {
    published: true,
    author: { role: 'ADMIN' },
  },
  orderBy: { createdAt: 'desc' },
});

// Find many
const posts = await prisma.post.findMany({
  where: {
    published: true,
    title: { contains: 'prisma', mode: 'insensitive' },
    createdAt: { gte: new Date('2024-01-01') },
  },
  select: {           // Select specific fields
    id: true,
    title: true,
    author: { select: { name: true, email: true } },
  },
  orderBy: [
    { createdAt: 'desc' },
    { title: 'asc' },
  ],
  take: 10,           // LIMIT
  skip: 20,           // OFFSET
});

// Count
const total = await prisma.post.count({
  where: { published: true },
});

// Aggregate
const stats = await prisma.post.aggregate({
  where: { published: true },
  _count: { id: true },
  _avg: { viewCount: true },
  _max: { viewCount: true },
});
```

### UPDATE

```ts
// Update one
const user = await prisma.user.update({
  where: { id: 'user-id' },
  data: {
    name: 'Updated Name',
    role: 'ADMIN',
    posts: {
      connect: { id: 'post-id' },     // Add relation
      disconnect: { id: 'old-id' },   // Remove relation
    },
  },
});

// Upsert (create or update)
const user = await prisma.user.upsert({
  where: { email: 'user@example.com' },
  update: { name: 'Updated' },
  create: { email: 'user@example.com', name: 'New User' },
});

// Update many
await prisma.post.updateMany({
  where: { published: false, createdAt: { lt: new Date('2023-01-01') } },
  data: { published: true },
});

// Increment / Decrement
await prisma.post.update({
  where: { id: 'post-id' },
  data: { viewCount: { increment: 1 } },
});
```

### DELETE

```ts
// Delete one
await prisma.user.delete({ where: { id: 'user-id' } });

// Delete many
await prisma.post.deleteMany({
  where: { createdAt: { lt: new Date('2020-01-01') } },
});
```

---

## Filtering Operators

```ts
where: {
  // String
  name: { equals: 'Alice' }
  name: { contains: 'ali', mode: 'insensitive' }
  email: { startsWith: 'admin@' }
  email: { endsWith: '@company.com' }

  // Numbers / Dates
  age: { gt: 18 }         // >
  age: { gte: 18 }        // >=
  age: { lt: 65 }         // <
  age: { lte: 65 }        // <=
  age: { not: 0 }
  createdAt: { gte: new Date('2024-01-01'), lt: new Date('2025-01-01') }

  // Arrays
  id: { in: ['id1', 'id2', 'id3'] }
  id: { notIn: ['id-x'] }

  // Null check
  name: null              // IS NULL
  name: { not: null }     // IS NOT NULL

  // Relations
  posts: { some: { published: true } }   // Has at least one published post
  posts: { every: { published: true } }  // All posts published
  posts: { none: { published: false } }  // No unpublished posts

  // Logical
  AND: [{ published: true }, { viewCount: { gt: 100 } }]
  OR:  [{ role: 'ADMIN' }, { role: 'MODERATOR' }]
  NOT: { deleted: true }
}
```

---

## Transactions

```ts
// Sequential transaction
const [user, post] = await prisma.$transaction([
  prisma.user.create({ data: { email: 'x@x.com' } }),
  prisma.post.create({ data: { title: 'Hello', authorId: 'id' } }),
]);

// Interactive transaction (with rollback on error)
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data: { email: 'x@x.com' } });
  const post = await tx.post.create({
    data: { title: 'Hello', authorId: user.id },
  });
  return { user, post };
});
```

---

## Raw Queries

```ts
// When Prisma queries are not enough
const result = await prisma.$queryRaw`
  SELECT * FROM "users"
  WHERE email ILIKE ${`%${search}%`}
  LIMIT ${limit}
`;

await prisma.$executeRaw`
  UPDATE "posts" SET view_count = view_count + 1
  WHERE id = ${postId}
`;
```

---

## Common Patterns

### Pagination (Cursor-based — preferred for large datasets)
```ts
const posts = await prisma.post.findMany({
  take: pageSize,
  skip: cursor ? 1 : 0,
  cursor: cursor ? { id: cursor } : undefined,
  orderBy: { createdAt: 'desc' },
});

const nextCursor = posts.length === pageSize ? posts[posts.length - 1].id : null;
```

### Soft Delete
```prisma
model Post {
  id        String   @id @default(cuid())
  deletedAt DateTime?   // null = not deleted

  @@index([deletedAt])
}
```

```ts
// Soft delete
await prisma.post.update({
  where: { id },
  data: { deletedAt: new Date() },
});

// Query only non-deleted
const posts = await prisma.post.findMany({
  where: { deletedAt: null },
});
```

---

## Resources

- **Docs**: https://www.prisma.io/docs
- **Schema Reference**: https://www.prisma.io/docs/reference/api-reference/prisma-schema-reference
- **Client API**: https://www.prisma.io/docs/reference/api-reference/prisma-client-reference
- **GitHub**: https://github.com/prisma/prisma
- **Prisma Accelerate** (connection pooling): https://www.prisma.io/data-platform/accelerate
