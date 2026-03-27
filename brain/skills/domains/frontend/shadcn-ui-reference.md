---
id: shadcn_ui_reference
name: shadcn/ui Reference
version: 1.0.0
tier: 3
domain: frontend
cost_tier: standard
status: active
author: AI OS (adapted from shadcn-ui/ui)
updated: 2026-03-14
source: https://github.com/shadcn-ui/ui
tags: [shadcn, react, tailwind, radix-ui, typescript, components, copy-paste]
accessible_by:
  - Antigravity
  - Claude Code
  - Developer
exposed_functions:
  - name: add_component
    description: CLI command to add a shadcn component to project
    input: component name
    output: CLI command string
  - name: get_component_pattern
    description: Return usage pattern for a shadcn component
    input: component name
    output: code pattern
  - name: get_theming_guide
    description: Return CSS variable theming configuration
    input: theme preference
    output: CSS variables + tailwind config
load_on_boot: false
---

# shadcn/ui — AI OS Reference Skill

> Source: https://github.com/shadcn-ui/ui (Open Source, Open Code)
> "A set of beautifully designed components you can customize, extend, and build on."

## Core Philosophy

shadcn/ui is **NOT a component library** — it's a collection of reusable components you **copy into your project**.

- **No dependency lock-in**: Components live in your `components/ui/` folder
- **Full ownership**: Edit, extend, rename anything
- **Built on**: Radix UI (accessibility) + Tailwind CSS (styling)
- **Stack**: React + TypeScript + Tailwind CSS + Radix UI

---

## Installation

### New Project
```bash
npx shadcn@latest init
```

Prompts: style (Default/New York), base color, CSS variables

### Add to Existing (Next.js)
```bash
npx shadcn@latest init
```

### Add Individual Components
```bash
npx shadcn@latest add button
npx shadcn@latest add dialog
npx shadcn@latest add form
npx shadcn@latest add table
npx shadcn@latest add card
npx shadcn@latest add input
npx shadcn@latest add select
npx shadcn@latest add sheet   # Sidebar panel
npx shadcn@latest add toast
npx shadcn@latest add calendar
npx shadcn@latest add chart   # Built on Recharts
npx shadcn@latest add sidebar # Full sidebar layout
npx shadcn@latest add data-table # Advanced table
```

---

## Component Catalog

### Layout
| Component | Add Command | Use Case |
|-----------|-------------|----------|
| `Separator` | `add separator` | Divider |
| `Resizable` | `add resizable` | Resizable panels |
| `Sidebar` | `add sidebar` | App sidebar layout (v2) |
| `ScrollArea` | `add scroll-area` | Custom scrollbar container |
| `AspectRatio` | `add aspect-ratio` | Maintain aspect ratio |

### Forms & Input
| Component | Add Command | Notes |
|-----------|-------------|-------|
| `Form` | `add form` | React Hook Form + Zod integration |
| `Input` | `add input` | Text input |
| `Textarea` | `add textarea` | Multi-line input |
| `Select` | `add select` | Dropdown (Radix) |
| `Checkbox` | `add checkbox` | Boolean toggle |
| `RadioGroup` | `add radio-group` | Single choice |
| `Switch` | `add switch` | Toggle |
| `Slider` | `add slider` | Range input |
| `DatePicker` | `add date-picker` | Built on Calendar + Popover |
| `InputOTP` | `add input-otp` | OTP/PIN input |

### Overlay
| Component | Add Command | Use Case |
|-----------|-------------|----------|
| `Dialog` | `add dialog` | Modal dialog |
| `Sheet` | `add sheet` | Slide-in panel (mobile-friendly) |
| `Drawer` | `add drawer` | Bottom drawer |
| `AlertDialog` | `add alert-dialog` | Confirmation dialog |
| `Popover` | `add popover` | Floating content |
| `Tooltip` | `add tooltip` | Hover tooltip |
| `HoverCard` | `add hover-card` | Rich hover card |
| `ContextMenu` | `add context-menu` | Right-click menu |
| `DropdownMenu` | `add dropdown-menu` | Dropdown actions |
| `Menubar` | `add menubar` | App menu bar |
| `Command` | `add command` | Command palette (⌘K) |

### Navigation
| Component | Add Command | Use Case |
|-----------|-------------|----------|
| `Tabs` | `add tabs` | Tab switching |
| `NavigationMenu` | `add navigation-menu` | Mega menu |
| `Breadcrumb` | `add breadcrumb` | Hierarchy indicator |
| `Pagination` | `add pagination` | Page navigation |

### Data Display
| Component | Add Command | Use Case |
|-----------|-------------|----------|
| `Table` | `add table` | Basic HTML table |
| `DataTable` | `add data-table` | TanStack Table integration |
| `Card` | `add card` | Content card |
| `Badge` | `add badge` | Status label |
| `Avatar` | `add avatar` | User image |
| `Progress` | `add progress` | Progress bar |
| `Skeleton` | `add skeleton` | Loading placeholder |
| `Accordion` | `add accordion` | Collapsible sections |
| `Collapsible` | `add collapsible` | Primitive collapse |
| `Carousel` | `add carousel` | Embla-based slider |
| `Chart` | `add chart` | Recharts wrapper |
| `Calendar` | `add calendar` | Date picker calendar |

### Feedback
| Component | Add Command | Use Case |
|-----------|-------------|----------|
| `Alert` | `add alert` | Inline message |
| `Toast` | `add toast` | Temporary notification (Sonner) |
| `Sonner` | `add sonner` | Modern toast provider |

### Typography / General
| Component | Add Command |
|-----------|-------------|
| `Button` | `add button` |
| `Label` | `add label` |
| `Toggle` | `add toggle` |
| `ToggleGroup` | `add toggle-group` |

---

## Theming (CSS Variables)

```css
/* globals.css */
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 240 10% 3.9%;
    --card: 0 0% 100%;
    --card-foreground: 240 10% 3.9%;
    --primary: 240 5.9% 10%;
    --primary-foreground: 0 0% 98%;
    --secondary: 240 4.8% 95.9%;
    --secondary-foreground: 240 5.9% 10%;
    --muted: 240 4.8% 95.9%;
    --muted-foreground: 240 3.8% 46.1%;
    --accent: 240 4.8% 95.9%;
    --accent-foreground: 240 5.9% 10%;
    --destructive: 0 84.2% 60.2%;
    --border: 240 5.9% 90%;
    --input: 240 5.9% 90%;
    --ring: 240 10% 3.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 240 10% 3.9%;
    --foreground: 0 0% 98%;
    --primary: 0 0% 98%;
    /* ... */
  }
}
```

### Custom Brand Color
```bash
# Generate theme at https://ui.shadcn.com/themes
# Copy CSS variables into globals.css
```

---

## Key Usage Patterns

### Form with Zod Validation (Most Common Pattern)
```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

const schema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(8, "Min 8 characters"),
});

export function LoginForm() {
  const form = useForm<z.infer<typeof schema>>({
    resolver: zodResolver(schema),
    defaultValues: { email: "", password: "" },
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit((data) => console.log(data))}>
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl><Input {...field} /></FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  );
}
```

### DataTable (TanStack Table)
```tsx
import { DataTable } from "@/components/ui/data-table";
import type { ColumnDef } from "@tanstack/react-table";

const columns: ColumnDef<User>[] = [
  { accessorKey: "name", header: "Name" },
  { accessorKey: "email", header: "Email" },
  {
    id: "actions",
    cell: ({ row }) => <DropdownMenu>...</DropdownMenu>,
  },
];

<DataTable columns={columns} data={users} />
```

### Command Palette
```tsx
import { CommandDialog, CommandInput, CommandList, CommandItem } from "@/components/ui/command";

<CommandDialog open={open} onOpenChange={setOpen}>
  <CommandInput placeholder="Type a command..." />
  <CommandList>
    <CommandItem onSelect={() => router.push("/dashboard")}>Dashboard</CommandItem>
  </CommandList>
</CommandDialog>
```

---

## Project Structure After Init

```
components/
└── ui/              # ← shadcn components live here (owned by you)
    ├── button.tsx
    ├── dialog.tsx
    ├── form.tsx
    └── ...
lib/
└── utils.ts         # cn() utility (clsx + tailwind-merge)
```

### The `cn()` Utility
```ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Usage:
<div className={cn("base-class", condition && "conditional-class", props.className)} />
```

---

## Frameworks Supported

- Next.js (App Router + Pages Router)
- Vite
- Remix
- Astro
- Laravel (via React)

---

## Resources

- **Docs**: https://ui.shadcn.com/docs
- **Components**: https://ui.shadcn.com/docs/components
- **Themes**: https://ui.shadcn.com/themes
- **Blocks**: https://ui.shadcn.com/blocks (Full page templates)
- **GitHub**: https://github.com/shadcn-ui/ui
