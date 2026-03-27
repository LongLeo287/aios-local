# KHO LLM — Index
# Registry: kho/llm/registry.json
# Config: infra/llm/router.yaml + fallback_chain.yaml
# Rule: RULE-VERSION-01 (no @latest)

## PROVIDERS (7)
- ollama_local       :11434  LIVE (gemma2:2b + nomic-embed-text)
- anthropic_claude   cloud   CONFIGURED (primary for Claude Code)
- google_gemini      cloud   ACTIVE (via Antigravity)
- openai             cloud   CONFIGURED (fallback)
- minimax            cloud   CONFIGURED
- kimi               cloud   CONFIGURED
- glm5               cloud   CONFIGURED

OFFLINE_MODE=false | LOCAL_FIRST=true
