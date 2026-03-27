# AI OS — Secrets Registry
# ============================================================
# Danh sách TẤT CẢ secrets trong project AI OS Corp.
# FILE NÀY: chỉ chứa KEY NAMES, KHÔNG chứa values.
# Values thực được lưu tại: <AI_OS_ROOT>/tools/clawtask/.env
# ============================================================
# Maintained by: Security GRC Dept (strix-agent)
# Last updated: 2026-03-22

---

## 📋 Principle

> Một nguồn sự thật duy nhất cho tất cả secrets: **`tools/clawtask/.env`** (AI OS root)
> Sub-tools (nullclaw, plugins...) có `.env` riêng chỉ chứa vars cần thiết.
> **KHÔNG BAO GIỜ** hardcode values vào source files — dùng `$env:VAR_NAME`.

---

## 🔑 Secret Inventory

### Category: AI / LLM Providers

| Key Name | Provider | Status | Rotation |
|----------|----------|--------|---------|
| `ANTHROPIC_API_KEY` | Anthropic Claude | ✅ Active | Rotate nếu compromise |
| `OPENAI_API_KEY` | OpenAI GPT | 🔵 Optional | — |
| `GOOGLE_AI_API_KEY` | Google Gemini | 🔵 Optional | — |
| `GROQ_API_KEY` | Groq | 🔵 Optional | — |
| `OPENROUTER_API_KEY` | OpenRouter | ✅ Active | — |
| `NINE_ROUTER_API_KEY` | 9Router AI_OS | ✅ Active | — |

### Category: GitHub / Source Control

| Key Name | Provider | Status | Rotation |
|----------|----------|--------|---------|
| `GITHUB_TOKEN` | GitHub PAT | ✅ Active | Expires per setting |

### Category: Database

| Key Name | Provider | Status | Rotation |
|----------|----------|--------|---------|
| `SUPABASE_URL` | Supabase | ✅ Active | Never (URL) |
| `SUPABASE_ANON_KEY` | Supabase | ✅ Active | Rotate if needed |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase | 🔵 Optional | ⚠️ Rotate if exposed |
| `DATABASE_URL` | Postgres | 🔵 Optional | — |

### Category: Communication / Notifications

| Key Name | Provider | Status | Rotation |
|----------|----------|--------|---------|
| `TELEGRAM_BOT_TOKEN` | Telegram (@aios_corp_bot) | ✅ Active | Revoke via @BotFather |
| `TELEGRAM_CHAT_ID` | Telegram (@LongLeo) | ✅ Active | Not rotatable |
| `SLACK_BOT_TOKEN` | Slack | 🔵 Optional | — |
| `DISCORD_WEBHOOK_URL` | Discord | 🔵 Optional | — |

### Category: Cloud / Deployment

| Key Name | Provider | Status | Rotation |
|----------|----------|--------|---------|
| `VERCEL_TOKEN` | Vercel | 🔵 Optional | — |
| `AWS_ACCESS_KEY_ID` | AWS | 🔵 Optional | Rotate every 90 days |
| `AWS_SECRET_ACCESS_KEY` | AWS | 🔵 Optional | Rotate every 90 days |
| `GCP_SERVICE_ACCOUNT_KEY` | GCP | 🔵 Optional | — |

### Category: Payments / Other

| Key Name | Provider | Status | Rotation |
|----------|----------|--------|---------|
| `STRIPE_SECRET_KEY` | Stripe | 🔵 Optional | — |
| `SENDGRID_API_KEY` | SendGrid | 🔵 Optional | — |
| `RESEND_API_KEY` | Resend | 🔵 Optional | — |

---

## 📁 Secret File Locations

| File | Purpose | Protected |
|------|---------|-----------|
| `tools/clawtask/.env` | **MASTER** — AI provider + Supabase + Telegram | ✅ .gitignore |
| `REMOTE/claws/nullclaw/.env` | Telegram only (nullclaw runtime) | ✅ .gitignore |

**KHÔNG bao giờ:** commit `.env`, `secrets/`, `*.key` lên git.

---

## 🚨 Nếu bị Compromise

1. Xác định key bị lộ từ bảng trên
2. Revoke ngay trên portal của provider
3. Generate key mới
4. Update `tools/clawtask/.env`
5. Restart các services liên quan
6. Write incident report vào `security/incidents/`

---

## Quản lý Rotation

| Key | Rotation Policy |
|-----|----------------|
| GitHub PAT | Check expiry in GitHub Settings |
| Anthropic | Rotate nếu suspicious activity |
| Supabase anon | Rotate qua Supabase Dashboard |
| Telegram token | `/revoke` tại @BotFather |
| AWS keys | Rotate mỗi 90 ngày |

---

*Security GRC Dept — strix-agent | Maintained with Strix v2.0*
