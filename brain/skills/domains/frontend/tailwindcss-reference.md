---
id: tailwindcss_reference
name: Tailwind CSS Reference
version: 1.0.0
tier: 3
domain: frontend
cost_tier: economy
status: active
author: AI OS (adapted from tailwindlabs/tailwindcss)
updated: 2026-03-14
source: https://github.com/tailwindlabs/tailwindcss
tags: [tailwind, css, utility-first, responsive, dark-mode, frontend]
accessible_by:
  - Antigravity
  - Claude Code
  - Developer
exposed_functions:
  - name: get_utility_classes
    description: Return Tailwind utility classes for a styling need
    input: styling description (e.g. "center a div with padding")
    output: Tailwind class string
  - name: get_config_pattern
    description: Return tailwind.config.js pattern
    input: customization need
    output: config snippet
load_on_boot: false
---

# Tailwind CSS — AI OS Reference Skill

> Source: https://tailwindlabs.com | v4 (latest) | v3 (stable)

## Core Philosophy

Utility-first CSS framework. Style directly in markup — no CSS files needed.

```html
<!-- Before Tailwind -->
<div class="chat-notification">...</div>

<!-- With Tailwind -->
<div class="flex items-center p-4 rounded-lg shadow-md bg-white dark:bg-gray-800">
```

---

## Installation

### v4 (Latest)
```bash
npm install tailwindcss @tailwindcss/vite   # Vite
npm install tailwindcss @tailwindcss/forms  # Forms plugin
```

```css
/* globals.css */
@import "tailwindcss";
```

### v3 (Stable — most projects)
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

```js
// tailwind.config.js
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: { extend: {} },
  plugins: [],
}
```

---

## Core Utility Categories

### Layout
```
container          → max-w-screen-xl mx-auto
block / inline-block / hidden / invisible
flex / inline-flex / grid / inline-grid

# Flexbox
flex-row / flex-col / flex-wrap
items-start / items-center / items-end / items-stretch
justify-start / justify-center / justify-end / justify-between / justify-around
gap-{n}  (gap-2 = 0.5rem, gap-4 = 1rem, gap-8 = 2rem)
grow / shrink / flex-1 / flex-none

# Grid
grid-cols-{n}      → grid-cols-3
grid-rows-{n}
col-span-{n}       → col-span-2
gap-{n}

# Positioning
relative / absolute / fixed / sticky / static
top-{n} / bottom-{n} / left-{n} / right-{n} / inset-{n}
z-{n}              → z-10, z-50, z-[100]
```

### Spacing (Margin & Padding)
```
# Padding
p-{n}     → all sides
px-{n}    → horizontal (left + right)
py-{n}    → vertical (top + bottom)
pt-{n} pb-{n} pl-{n} pr-{n}

# Margin
m-{n} mx-{n} my-{n} mt-{n} mb-{n} ml-{n} mr-{n}
mx-auto   → center block element
-m-{n}    → negative margin

# Scale: 0=0, 1=0.25rem, 2=0.5rem, 4=1rem, 8=2rem, 16=4rem
# Arbitrary: p-[13px]
```

### Sizing
```
w-{n}       → width (w-full, w-1/2, w-screen, w-[200px])
h-{n}       → height (h-full, h-screen, h-svh, h-[500px])
min-w-{n} / max-w-{n}
min-h-{n} / max-h-{n}
size-{n}    → width + height together (v3.4+)
aspect-square / aspect-video / aspect-[4/3]
```

### Typography
```
# Font Family
font-sans / font-serif / font-mono

# Font Size
text-xs(12) / text-sm(14) / text-base(16) / text-lg(18)
text-xl(20) / text-2xl(24) / text-3xl(30) / text-4xl(36)
text-5xl / text-6xl / text-7xl / text-8xl / text-9xl

# Font Weight
font-thin / font-light / font-normal / font-medium
font-semibold / font-bold / font-extrabold / font-black

# Line Height
leading-none / leading-tight / leading-snug
leading-normal / leading-relaxed / leading-loose

# Text Alignment
text-left / text-center / text-right / text-justify

# Text Transform
uppercase / lowercase / capitalize / normal-case

# Text Color
text-{color}-{shade}  → text-gray-900, text-blue-600, text-white

# Text Decoration
underline / line-through / no-underline
decoration-{color}    → decoration-blue-500

# Letter Spacing
tracking-tight / tracking-normal / tracking-wide / tracking-wider

# Line Clamp
line-clamp-{n}        → truncate to N lines
truncate              → single line with ellipsis
```

### Colors
```
# Color system: {color}-{shade}
# Shades: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950

# Text
text-slate-900   text-gray-500   text-zinc-400
text-red-500     text-orange-400 text-amber-300
text-yellow-400  text-lime-500   text-green-600
text-emerald-500 text-teal-400   text-cyan-500
text-sky-500     text-blue-600   text-indigo-500
text-violet-600  text-purple-500 text-fuchsia-500
text-pink-500    text-rose-500

# Background (same palette with bg- prefix)
bg-white / bg-black / bg-transparent
bg-blue-600

# Border (same with border- prefix)
border-gray-200

# Opacity modifier
text-blue-500/75   → 75% opacity
bg-black/50        → 50% opacity
```

### Borders
```
border             → 1px border
border-{n}         → border-2, border-4
border-{side}      → border-t, border-b, border-l, border-r
border-{color}     → border-gray-200, border-blue-500
border-transparent

rounded            → 0.25rem
rounded-sm / rounded-md / rounded-lg / rounded-xl
rounded-2xl / rounded-3xl / rounded-full

outline-none / ring-{n} / ring-{color}
ring-2 ring-blue-500 ring-offset-2  → Focus ring pattern
```

### Shadows
```
shadow-sm / shadow / shadow-md / shadow-lg
shadow-xl / shadow-2xl / shadow-inner / shadow-none
shadow-{color}/50  → Colored shadow
```

### Backgrounds
```
bg-{color}
bg-gradient-to-{direction}  → bg-gradient-to-r, bg-gradient-to-br
from-{color} to-{color} via-{color}    → Gradient stops
bg-cover / bg-contain / bg-center
```

---

## Responsive Design

Breakpoints (mobile-first):

| Prefix | Min Width | Device |
|--------|-----------|--------|
| (none) | 0 | Mobile |
| `sm:` | 640px | Small |
| `md:` | 768px | Tablet |
| `lg:` | 1024px | Desktop |
| `xl:` | 1280px | Large |
| `2xl:` | 1536px | Extra large |

```html
<div class="w-full md:w-1/2 lg:w-1/3">
  <!-- Full width on mobile, half on tablet, 1/3 on desktop -->
</div>
```

---

## Dark Mode

```js
// tailwind.config.js
module.exports = {
  darkMode: 'class',  // or 'media'
}
```

```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
```

---

## State Variants

```html
<!-- Hover / Focus / Active -->
hover:bg-blue-600
focus:ring-2 focus:ring-blue-500 focus:outline-none
active:scale-95

<!-- Group hover (parent controls child) -->
<div class="group">
  <span class="group-hover:text-blue-500">Changes on parent hover</span>
</div>

<!-- Peer (sibling state) -->
<input class="peer" type="checkbox" />
<label class="peer-checked:text-blue-500">Checked!</label>

<!-- Disabled / Required / Invalid (form states) -->
disabled:opacity-50 disabled:cursor-not-allowed
invalid:border-red-500
required:*

<!-- First / Last / Odd / Even -->
first:mt-0 last:mb-0
odd:bg-gray-50 even:bg-white
```

---

## Animations

```
# Built-in
animate-spin       → Loading spinner
animate-ping       → Ping ripple (notification badge)
animate-pulse      → Skeleton loading
animate-bounce     → Bounce
animate-none

# Custom (tailwind.config.js)
module.exports = {
  theme: {
    extend: {
      animation: {
        'slide-in': 'slideIn 0.3s ease-out',
      },
      keyframes: {
        slideIn: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
};
```

---

## Common Patterns

### Centered Card
```html
<div class="min-h-screen flex items-center justify-center bg-gray-50">
  <div class="w-full max-w-md bg-white rounded-xl shadow-lg p-8">
    <!-- Content -->
  </div>
</div>
```

### Sidebar Layout
```html
<div class="flex h-screen">
  <aside class="w-64 flex-shrink-0 bg-gray-900 text-white">Sidebar</aside>
  <main class="flex-1 overflow-auto p-6">Content</main>
</div>
```

### Responsive Grid
```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
  <div class="bg-white rounded-lg shadow p-4">Card</div>
</div>
```

### Sticky Header
```html
<header class="sticky top-0 z-50 bg-white/80 backdrop-blur border-b">
  <!-- Nav -->
</header>
```

### Gradient Button
```html
<button class="bg-gradient-to-r from-blue-600 to-purple-600 text-white
               px-6 py-3 rounded-lg font-semibold
               hover:from-blue-700 hover:to-purple-700
               transition-all duration-200
               shadow-lg shadow-blue-500/25">
  Get Started
</button>
```

### Glassmorphism Card
```html
<div class="bg-white/10 backdrop-blur-md border border-white/20
            rounded-2xl shadow-xl p-6 text-white">
  <!-- Content -->
</div>
```

---

## Tailwind Config Customization

```js
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50:  '#eff6ff',
          500: '#3b82f6',
          900: '#1e3a8a',
        },
      },
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem',
      },
      screens: {
        '3xl': '1920px',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
};
```

---

## Important Plugins

| Plugin | Install | Purpose |
|--------|---------|---------|
| `@tailwindcss/forms` | `npm i -D @tailwindcss/forms` | Better default form styles |
| `@tailwindcss/typography` | `npm i -D @tailwindcss/typography` | `prose` class for rich text |
| `@tailwindcss/aspect-ratio` | `npm i -D @tailwindcss/aspect-ratio` | `aspect-w-16 aspect-h-9` |
| `tailwindcss-animate` | `npm i -D tailwindcss-animate` | shadcn/ui animations |

---

## Resources

- **Docs**: https://tailwindcss.com/docs
- **UI Components**: https://tailwindui.com
- **Playground**: https://play.tailwindcss.com
- **Cheat Sheet**: https://nerdcave.com/tailwind-cheat-sheet
