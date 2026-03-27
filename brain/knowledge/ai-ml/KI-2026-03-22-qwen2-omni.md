---
id: KI-2026-03-22-qwen2-omni
source: https://github.com/QwenLM/Qwen2.5-Omni
type: RESEARCH
domain: ['ai-ml', 'llm', 'multimodal', 'tts', 'asr']
dept: rd
agents: ['llm_router', 'content_analyst']
created: 2026-03-22T22:37:16.443912
---

# Qwen2.5-Omni Multimodal LLM

> End-to-end multimodal LLM (text/image/audio/video → text+speech). Thinker-Talker architecture. Real-time streaming. TMRoPE position embedding. 7B-72B models.

**Source:** [https://github.com/QwenLM/Qwen2.5-Omni](https://github.com/QwenLM/Qwen2.5-Omni)  
**Type:** RESEARCH | **Dept:** rd  
**Relevant Agents:** llm_router, content_analyst

## AI OS Notes
Requires high-end GPU. Use via Aliyun Model Studio API for production. MiniMax API is current replacement for TTS. Track for future local multimodal model use.

## Install / Use
```
pip install transformers torch  # needs A100+ GPU
```

## Key Concepts
- Thinker-Talker architecture
- TMRoPE
- streaming audio output
- omni modality

## Cross-links
- SKILL.md: `plugins/22-qwen2-omni/SKILL.md`
- FAST_INDEX: keyword `qwen2.5-omni_multimo`
