---
id: antd_reference
name: Ant Design Reference
version: 1.0.0
tier: 3
domain: frontend
cost_tier: standard
status: active
author: AI OS (adapted from ant-design/ant-design)
updated: 2026-03-14
source: https://github.com/ant-design/ant-design
tags: [antd, react, typescript, ui-library, design-system, components, enterprise]
accessible_by:
  - Antigravity
  - Claude Code
  - Developer
exposed_functions:
  - name: get_component_api
    description: Return props/API for a specific Ant Design component
    input: component name (string)
    output: API table with props, types, defaults
  - name: get_design_tokens
    description: Return design token variables for theming
    input: token category (color, size, typography, etc.)
    output: token list with values
  - name: get_usage_pattern
    description: Return correct usage pattern for a component
    input: component name + use case
    output: code pattern + best practices
load_on_boot: false
---

# Ant Design (antd) — AI OS Reference Skill

> Source: https://github.com/ant-design/ant-design (97K ⭐ | TypeScript | React)
> Adapted: CLAUDE.md + component catalog — NOT the source code (251MB, too large to clone)

## Overview

Ant Design is an enterprise-class UI design language and React UI library.

- **Package**: `antd` (npm)
- **Stack**: TypeScript + React + CSS-in-JS (`@ant-design/cssinjs`)
- **Features**: Design Token theming, dark mode, RTL, SSR, i18n (150+ languages)
- **Components**: 84+ components across categories

---

## Project Structure (Reference)

```
components/
├── component-name/
│   ├── ComponentName.tsx      # Main component
│   ├── demo/                  # Demo code (*.tsx + *.md)
│   ├── style/                 # CSS-in-JS (index.ts / token.ts)
│   ├── __tests__/             # Unit tests
│   ├── index.en-US.md         # English docs
│   ├── index.zh-CN.md         # Chinese docs
│   └── index.tsx              # Export entry
├── _util/                     # Shared utilities
├── theme/                     # Theme system
└── locale/                    # i18n text (zh_CN.ts, en_US.ts, ...)
```

---

## Component Catalog (84+ Components)

### General
| Component | Import | Use Case |
|-----------|--------|----------|
| `Button` | `import { Button } from 'antd'` | Actions — primary, default, dashed, text, link |
| `Icon` | `import { Icon } from '@ant-design/icons'` | 1000+ icons |
| `Typography` | `import { Typography } from 'antd'` | Text, Title, Paragraph, Link |
| `Flex` | `import { Flex } from 'antd'` | Flexbox layout container |

### Layout
| Component | Use Case |
|-----------|----------|
| `Layout` | Header, Sider, Content, Footer scaffold |
| `Grid` | 24-column responsive grid (Row + Col) |
| `Space` | Inline spacing between elements |
| `Divider` | Horizontal/vertical separator |
| `Splitter` | Resizable panel split |

### Navigation
| Component | Use Case |
|-----------|----------|
| `Breadcrumb` | Hierarchical location indicator |
| `Menu` | Sidebar or top navigation |
| `Pagination` | Page navigation |
| `Steps` | Multi-step wizard progress |
| `Tabs` | Tab panel switching |
| `Anchor` | Page anchor links |
| `BackTop` | Scroll-to-top button |

### Data Entry (Forms)
| Component | Use Case |
|-----------|----------|
| `Form` | Form wrapper with validation |
| `Input` | Text input (Input, Input.TextArea, Input.Search, Input.Password) |
| `InputNumber` | Numeric input with step |
| `Select` | Dropdown selector |
| `TreeSelect` | Hierarchical selector |
| `Cascader` | Multi-level selector |
| `DatePicker` | Date/time selection |
| `TimePicker` | Time-only selection |
| `Checkbox` | Boolean toggle (single or group) |
| `Radio` | Single choice from group |
| `Switch` | Boolean toggle |
| `Slider` | Range/value slider |
| `Rate` | Star rating |
| `Upload` | File upload (drag & drop) |
| `ColorPicker` | Color selector |
| `Mentions` | @mention text input |
| `AutoComplete` | Autocomplete input |
| `Transfer` | Dual-list selection |

### Data Display
| Component | Use Case |
|-----------|----------|
| `Table` | Data table with sort, filter, pagination |
| `List` | Simple or complex list |
| `Tree` | Hierarchical tree structure |
| `Card` | Content container card |
| `Carousel` | Slideshow / image carousel |
| `Collapse` | Accordion panels |
| `Descriptions` | Key-value data display |
| `Empty` | Empty state placeholder |
| `Image` | Image with preview |
| `Avatar` | User avatar (image/text/icon) |
| `Badge` | Count badge / status indicator |
| `Calendar` | Month/year calendar view |
| `Statistic` | Key metric display |
| `Tag` | Labeling / categorizing |
| `Timeline` | Chronological event list |
| `Tooltip` | Hover info popup |
| `Popover` | Richer hover popup |
| `Tour` | Feature walkthrough overlay |
| `QRCode` | QR code generator |
| `Segmented` | Segmented control selector |
| `Watermark` | Document watermark |

### Feedback
| Component | Use Case |
|-----------|----------|
| `Alert` | Inline status message |
| `Message` | Transient top notification |
| `Notification` | Corner pop-up notification |
| `Modal` | Dialog overlay |
| `Drawer` | Slide-in panel |
| `Popconfirm` | Inline confirm dialog |
| `Progress` | Progress bar / circle |
| `Result` | Success/error/warning full-page |
| `Skeleton` | Loading placeholder |
| `Spin` | Loading spinner |

### Other
| Component | Use Case |
|-----------|----------|
| `Affix` | Sticky positioning |
| `App` | Message/notification context provider |
| `ConfigProvider` | Global config (theme, locale, size) |
| `FloatButton` | Floating action button |

---

## Design Token System

Ant Design v5 uses a Design Token system for theming. Override via `ConfigProvider`:

```tsx
import { ConfigProvider } from 'antd';

<ConfigProvider
  theme={{
    token: {
      // === Color Palette ===
      colorPrimary: '#1677ff',        // Brand primary
      colorSuccess: '#52c41a',
      colorWarning: '#faad14',
      colorError: '#ff4d4f',
      colorInfo: '#1677ff',
      colorLink: '#1677ff',

      // === Layout ===
      borderRadius: 6,               // Global border radius
      wireframe: false,              // Wireframe mode

      // === Typography ===
      fontFamily: '-apple-system, BlinkMacSystemFont, ...',
      fontSize: 14,
      lineHeight: 1.5714,

      // === Size ===
      sizeUnit: 4,                   // Base unit (px)
      sizeStep: 4,
      controlHeight: 32,             // Default form control height
    },
    components: {
      // Component-level token overrides
      Button: {
        borderRadius: 4,
        primaryColor: '#ffffff',
      },
      Table: {
        headerBg: '#fafafa',
      },
    },
  }}
>
  <App />
</ConfigProvider>
```

### Dark Mode
```tsx
import { ConfigProvider, theme } from 'antd';
const { darkAlgorithm } = theme;

<ConfigProvider theme={{ algorithm: darkAlgorithm }}>
  <App />
</ConfigProvider>
```

### Compact Mode
```tsx
import { ConfigProvider, theme } from 'antd';
const { compactAlgorithm } = theme;

<ConfigProvider theme={{ algorithm: compactAlgorithm }}>
  <App />
</ConfigProvider>
```

---

## API Table Format (How Ant Design Documents APIs)

Standard format for component props documentation:

| Property | Description | Type | Default | Version |
|----------|-------------|------|---------|---------|
| `disabled` | Whether disabled | `boolean` | `false` | - |
| `type` | Button type | `primary \| default \| dashed \| text \| link` | `default` | - |
| `size` | Button size | `large \| middle \| small` | `middle` | - |
| `loading` | Show loading state | `boolean \| { delay: number }` | `false` | - |
| `onClick` | Click handler | `(event: MouseEvent) => void` | - | - |

Rules:
- String defaults use backtick, boolean/number direct, no default = `-`
- Props sorted alphabetically
- New props must declare version number

---

## Common Usage Patterns

### Form with Validation
```tsx
import { Form, Input, Button } from 'antd';

const MyForm = () => {
  const [form] = Form.useForm();

  const onFinish = (values: any) => {
    console.log('Success:', values);
  };

  return (
    <Form form={form} layout="vertical" onFinish={onFinish}>
      <Form.Item
        name="email"
        label="Email"
        rules={[
          { required: true, message: 'Required' },
          { type: 'email', message: 'Invalid email' },
        ]}
      >
        <Input />
      </Form.Item>
      <Button type="primary" htmlType="submit">Submit</Button>
    </Form>
  );
};
```

### Table with Pagination
```tsx
import { Table } from 'antd';
import type { TableProps } from 'antd';

const columns: TableProps['columns'] = [
  { title: 'Name', dataIndex: 'name', key: 'name', sorter: true },
  { title: 'Age', dataIndex: 'age', key: 'age' },
  { title: 'Action', key: 'action', render: (_, record) => (
    <Button onClick={() => console.log(record)}>Edit</Button>
  )},
];

<Table
  columns={columns}
  dataSource={data}
  rowKey="id"
  pagination={{ pageSize: 10 }}
  loading={loading}
/>
```

### Modal Dialog
```tsx
import { Modal, Button } from 'antd';

const [open, setOpen] = useState(false);

<>
  <Button onClick={() => setOpen(true)}>Open</Button>
  <Modal
    title="Title"
    open={open}
    onOk={() => setOpen(false)}
    onCancel={() => setOpen(false)}
    okText="Confirm"
    cancelText="Cancel"
  >
    <p>Content here</p>
  </Modal>
</>
```

### Message / Notification
```tsx
import { App } from 'antd'; // Recommended: use App context

const { message, notification } = App.useApp();

// Transient message
message.success('Saved!');
message.error('Failed!');

// Notification (persists until closed)
notification.open({
  message: 'Title',
  description: 'Description',
  type: 'success',
  placement: 'topRight',
});
```

---

## Installation & Setup

```bash
npm install antd
# or
pnpm add antd
```

### Next.js Setup
```tsx
// app/layout.tsx
import { AntdRegistry } from '@ant-design/nextjs-registry';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <AntdRegistry>
          {children}
        </AntdRegistry>
      </body>
    </html>
  );
}
```

---

## Internationalization

```tsx
import { ConfigProvider } from 'antd';
import enUS from 'antd/locale/en_US';
import viVN from 'antd/locale/vi_VN';
import zhCN from 'antd/locale/zh_CN';

<ConfigProvider locale={viVN}>
  <App />
</ConfigProvider>
```

Supported: 150+ locales in `node_modules/antd/locale/`

---

## Key Rules When Using antd (from official CLAUDE.md)

1. **CSS-in-JS**: Always use `ConfigProvider` for theme, not CSS overrides
2. **App Context**: Use `App.useApp()` for message/modal/notification — not static methods
3. **Form**: Always use `Form.useForm()` hook, not ref
4. **TypeScript**: Import types from antd directly: `import type { TableProps } from 'antd'`
5. **Icons**: Install `@ant-design/icons` separately — not included in `antd`
6. **SSR**: Use `@ant-design/nextjs-registry` for Next.js SSR compatibility
7. **Tree Shaking**: Import directly — `import { Button } from 'antd'` (auto tree-shaken in v5)

---

## Resources

- **Docs**: https://ant.design/components/overview
- **GitHub**: https://github.com/ant-design/ant-design
- **Design Resources**: https://ant.design/docs/resources
- **Changelog**: https://ant.design/changelog
- **Figma**: https://ant.design/docs/resources (Ant Design Figma Kit)
