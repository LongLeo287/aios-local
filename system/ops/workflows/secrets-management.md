# Department: operations
---
description: HÆ°á»›ng dáº«n quáº£n lÃ½ táº­p trung API keys, tokens, vÃ  secrets trong AI OS Corp
---

# Secrets Management SOP

## NguyÃªn táº¯c cá»‘t lÃµi

| Rule | Detail |
|------|--------|
| **1 nguá»“n** | Táº¥t cáº£ secrets trong `<AI_OS_ROOT>\.env` (root master) |
| **KhÃ´ng commit** | `.env` luÃ´n bá»‹ gitignore, khÃ´ng bao giá» push lÃªn git |
| **KhÃ´ng hardcode** | KhÃ´ng paste key vÃ o code, markdown, hay comment |
| **Rotate** | Xoay vÃ²ng keys theo lá»‹ch (xem SECRETS_REGISTRY.md) |
| **Least privilege** | Chá»‰ cáº¥p quyá»n tá»‘i thiá»ƒu cáº§n thiáº¿t cho má»—i key |

---

## Cáº¥u trÃºc Files

```
<AI_OS_ROOT>\
â”œâ”€â”€ .env                    â† MASTER secrets (gitignored âœ…)
â”œâ”€â”€ .env.example            â† Template an toÃ n (cÃ³ thá»ƒ commit)
â”œâ”€â”€ secrets\
â”‚   â”œâ”€â”€ .gitignore          â† Cháº·n toÃ n folder
â”‚   â”œâ”€â”€ SECRETS_REGISTRY.md â† Inventory keys (khÃ´ng cÃ³ values)
â”‚   â””â”€â”€ .env.master.example â† Template master Ä‘áº§y Ä‘á»§
â””â”€â”€ tools\clawtask\
    â””â”€â”€ .env                â† Sub-env (chá»‰ vars cáº§n cho clawtask, gitignored âœ…)
```

---

## Quy trÃ¬nh Onboarding (setup láº§n Ä‘áº§u)

### BÆ°á»›c 1: Copy template
```powershell
copy "<AI_OS_ROOT>\secrets\.env.master.example" "<AI_OS_ROOT>\.env"
```

### BÆ°á»›c 2: Äiá»n values
Má»Ÿ `<AI_OS_ROOT>\.env` vÃ  Ä‘iá»n giÃ¡ trá»‹ thá»±c cho tá»«ng key.

### BÆ°á»›c 3: Setup sub-tool .env
```powershell
# ClawTask cáº§n subset nhá»
copy template vÃ o tools\clawtask\.env
# Chá»‰ Ä‘iá»n: SUPABASE_URL, SUPABASE_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
```

### BÆ°á»›c 4: Verify gitignore
```powershell
git status   # .env KHÃ”NG Ä‘Æ°á»£c xuáº¥t hiá»‡n trong danh sÃ¡ch
git check-ignore -v .env  # Pháº£i tráº£ vá» ".gitignore:.env"
```

---

## ThÃªm Secret Má»›i

1. **ThÃªm vÃ o `<AI_OS_ROOT>\.env`** (giÃ¡ trá»‹ thá»±c)
2. **ThÃªm vÃ o `secrets\.env.master.example`** (placeholder)
3. **ÄÄƒng kÃ½ vÃ o `secrets\SECRETS_REGISTRY.md`** (key name + metadata)
4. Load trong code qua `os.environ.get("KEY_NAME")`

---

## Rotate Secret

1. **Revoke key cÅ©** trÃªn portal cá»§a provider
2. **Generate key má»›i**
3. **Update** `<AI_OS_ROOT>\.env`
4. **Restart** services dÃ¹ng key Ä‘Ã³ (Docker: `docker compose restart`)
5. **Ghi nháº­t kÃ½** vÃ o SECRETS_REGISTRY.md (update date)

---

## Náº¿u Key bá»‹ Lá»™ (Emergency)

```
KHáº¨N Cáº¤P: Revoke ngay trÃªn provider portal!
```

1. ðŸ”´ **Revoke ngay** â€” khÃ´ng chá»
2. Generate key replacement
3. Update `.env` + restart services
4. Verify khÃ´ng cÃ²n reference trong code: `grep -r "old_key_prefix" d:\Project`
5. Audit log xem ai/cÃ¡i gÃ¬ Ä‘Ã£ access

---

## Tools & Commands há»¯u Ã­ch

```powershell
# Kiá»ƒm tra file cÃ³ bá»‹ commit khÃ´ng
git ls-files .env

# Xem secrets Ä‘ang Ä‘Æ°á»£c load khÃ´ng
python -c "import os; print(os.environ.get('ANTHROPIC_API_KEY','NOT SET')[:10])"

# Check gitnore
git check-ignore -v tools\clawtask\.env

# Test Telegram bot sau khi config
curl http://localhost:7474/api/telegram/test
```

---

## Provider Dashboards

| Provider | Revoke Location |
|----------|----------------|
| Anthropic | console.anthropic.com â†’ API Keys |
| OpenAI | platform.openai.com â†’ API Keys |
| GitHub | github.com/settings/tokens |
| Supabase | Project â†’ Settings â†’ API |
| Telegram | Telegram â†’ @BotFather â†’ /revoke |
| Google | console.cloud.google.com â†’ Credentials |

---

*Security GRC Dept | SOP-SEC-001 | Created Cycle 5 (2026-03-20)*

