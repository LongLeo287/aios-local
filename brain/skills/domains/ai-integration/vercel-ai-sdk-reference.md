---
id: vercel_ai_sdk_reference
name: Vercel AI SDK Reference
version: 1.0.0
tier: 3
domain: ai-integration
cost_tier: standard
status: draft
author: AI OS (adapted from vercel/ai)
updated: 2026-03-14
source: https://github.com/vercel/ai
warning: UNVERIFIED — written from AI training data, not fetched from official docs. Verify before production use.
tags: [vercel, ai-sdk, llm, streaming, chat, openai, anthropic, google, typescript]
accessible_by:
  - Antigravity
  - Claude Code
  - Developer
exposed_functions:
  - name: get_provider_setup
    description: Return setup code for a specific AI provider
    input: provider name (openai, anthropic, google, etc.)
    output: setup + API call code
  - name: get_streaming_pattern
    description: Return streaming chat UI pattern
    input: framework (next.js, react, etc.)
    output: code pattern
  - name: get_tool_use_pattern
    description: Return AI tool/function calling pattern
    input: tool description
    output: code pattern with schema
load_on_boot: false
---

# Vercel AI SDK — AI OS Reference Skill

> Source: https://github.com/vercel/ai | `ai` npm package
> The TypeScript toolkit for building AI-powered products with React, Next.js, Svelte, Nuxt, and Node.

## Overview

- **Package**: `ai` + provider packages
- **Key Features**: Streaming, Tool Calls, Structured Output, Multi-modal, React hooks
- **Providers**: OpenAI, Anthropic, Google, Cohere, Mistral, Groq, Perplexity, and more

---

## Installation

```bash
npm install ai

# Provider packages (install as needed):
npm install @ai-sdk/openai      # OpenAI / Azure
npm install @ai-sdk/anthropic   # Claude
npm install @ai-sdk/google      # Gemini
npm install @ai-sdk/groq        # Groq (fast inference)
npm install @ai-sdk/mistral     # Mistral
npm install @ai-sdk/cohere      # Cohere
```

---

## Provider Setup

### OpenAI
```ts
import { openai } from '@ai-sdk/openai';

const model = openai('gpt-4o');
const mini  = openai('gpt-4o-mini');
const o1    = openai('o1-preview');
```

### Anthropic (Claude)
```ts
import { anthropic } from '@ai-sdk/anthropic';

const model = anthropic('claude-3-5-sonnet-20241022');
const haiku = anthropic('claude-3-5-haiku-20241022');
const opus  = anthropic('claude-3-opus-20240229');
```

### Google (Gemini)
```ts
import { google } from '@ai-sdk/google';

const model = google('gemini-2.0-flash-exp');
const pro   = google('gemini-1.5-pro');
```

---

## Core Functions

### generateText — Single completion
```ts
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

const { text, usage } = await generateText({
  model: openai('gpt-4o'),
  prompt: 'Explain quantum computing in simple terms.',
  system: 'You are a helpful assistant.',
  maxTokens: 500,
  temperature: 0.7,
});

console.log(text);
console.log(usage); // { promptTokens, completionTokens, totalTokens }
```

### streamText — Streaming completion
```ts
import { streamText } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';

const result = await streamText({
  model: anthropic('claude-3-5-sonnet-20241022'),
  prompt: 'Write a short story about AI.',
});

// Stream to response (Next.js Route Handler):
return result.toDataStreamResponse();

// Manual stream consumption:
for await (const delta of result.textStream) {
  process.stdout.write(delta);
}
```

### generateObject — Structured output
```ts
import { generateObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const { object } = await generateObject({
  model: openai('gpt-4o'),
  schema: z.object({
    title: z.string(),
    tags: z.array(z.string()),
    sentiment: z.enum(['positive', 'neutral', 'negative']),
    score: z.number().min(0).max(10),
  }),
  prompt: 'Analyze this product review: "Great quality, fast shipping!"',
});

console.log(object);
// { title: "...", tags: [...], sentiment: "positive", score: 8.5 }
```

---

## Chat Messages Format

```ts
import { generateText } from 'ai';

const { text } = await generateText({
  model: openai('gpt-4o'),
  messages: [
    { role: 'system',    content: 'You are a helpful assistant.' },
    { role: 'user',      content: 'What is the capital of France?' },
    { role: 'assistant', content: 'The capital of France is Paris.' },
    { role: 'user',      content: 'What is its population?' },
  ],
});
```

---

## Tool Calling (Function Calling)

```ts
import { generateText, tool } from 'ai';
import { z } from 'zod';

const { text, toolCalls } = await generateText({
  model: openai('gpt-4o'),
  prompt: 'What is the weather in San Francisco?',
  tools: {
    getWeather: tool({
      description: 'Get current weather for a location',
      parameters: z.object({
        location: z.string().describe('City name'),
        unit: z.enum(['celsius', 'fahrenheit']).default('celsius'),
      }),
      execute: async ({ location, unit }) => {
        // Call weather API...
        return { temperature: 22, condition: 'sunny', unit };
      },
    }),
  },
  maxSteps: 3,  // Allow multi-step tool use
});
```

---

## React Hooks (Next.js / React)

### useChat — Streaming chat UI
```tsx
'use client';
import { useChat } from 'ai/react';

export function Chat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat',   // Your API route
  });

  return (
    <div>
      {messages.map(m => (
        <div key={m.id} className={m.role === 'user' ? 'text-right' : 'text-left'}>
          <p>{m.content}</p>
        </div>
      ))}

      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} disabled={isLoading} />
        <button type="submit" disabled={isLoading}>Send</button>
      </form>
    </div>
  );
}
```

### API Route (Next.js App Router)
```ts
// app/api/chat/route.ts
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

export const runtime = 'edge'; // Optional: use Edge runtime

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = await streamText({
    model: openai('gpt-4o'),
    system: 'You are a helpful assistant.',
    messages,
  });

  return result.toDataStreamResponse();
}
```

### useCompletion — Single prompt completion
```tsx
import { useCompletion } from 'ai/react';

const { completion, input, handleInputChange, handleSubmit } = useCompletion({
  api: '/api/completion',
});
```

---

## Multi-modal (Vision)

```ts
const { text } = await generateText({
  model: openai('gpt-4o'),
  messages: [{
    role: 'user',
    content: [
      { type: 'text', text: 'Describe this image:' },
      { type: 'image', image: new URL('https://example.com/photo.jpg') },
      // Or base64:
      { type: 'image', image: Buffer.from(imageData), mimeType: 'image/jpeg' },
    ],
  }],
});
```

---

## Embeddings

```ts
import { embed, embedMany } from 'ai';
import { openai } from '@ai-sdk/openai';

// Single embedding
const { embedding } = await embed({
  model: openai.embedding('text-embedding-3-small'),
  value: 'The quick brown fox',
});

// Batch embeddings
const { embeddings } = await embedMany({
  model: openai.embedding('text-embedding-3-small'),
  values: ['First text', 'Second text', 'Third text'],
});
```

---

## Error Handling

```ts
import { generateText } from 'ai';
import { APICallError } from 'ai';

try {
  const { text } = await generateText({ model, prompt });
} catch (error) {
  if (APICallError.isInstance(error)) {
    console.error('API Error:', error.statusCode, error.message);
    // Retry logic here
  }
}
```

---

## Cost-Aware Model Selection

```ts
// Route to cheaper models for simple tasks
const selectModel = (taskComplexity: 'low' | 'medium' | 'high') => {
  switch (taskComplexity) {
    case 'low':    return openai('gpt-4o-mini');     // ~$0.15/1M tokens
    case 'medium': return openai('gpt-4o');           // ~$2.50/1M tokens
    case 'high':   return anthropic('claude-3-5-sonnet-20241022');
  }
};
```

---

## Resources

- **Docs**: https://sdk.vercel.ai/docs
- **GitHub**: https://github.com/vercel/ai
- **Examples**: https://sdk.vercel.ai/examples
- **Providers**: https://sdk.vercel.ai/providers
