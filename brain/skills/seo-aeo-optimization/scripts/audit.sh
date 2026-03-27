#!/bin/bash
# ============================================================
# SEO + AEO Live Audit Script
# Usage: bash audit.sh https://yourdomain.com [/page-path]
# ============================================================

DOMAIN="${1:-}"
PAGE_PATH="${2:-/}"

if [ -z "$DOMAIN" ]; then
  echo "Usage: bash audit.sh https://yourdomain.com [/page-path]"
  exit 1
fi

case "$DOMAIN" in
  http://*|https://*) ;;
  *) echo "Error: domain must start with http:// or https://"; exit 1 ;;
esac

BASE="${DOMAIN%/}"
# Cleanup temp files on exit, interrupt, or termination
TMPFILE=""
ROBOTS_TMPFILE=""
PSI_TMPFILE=""
trap 'rm -f "$TMPFILE" "$ROBOTS_TMPFILE" "$PSI_TMPFILE"' EXIT INT TERM
# Extract origin (scheme + host only) for robots.txt, llms.txt, sitemap
# e.g. https://site.com/blog → https://site.com
ORIGIN=$(python3 -c "
import urllib.parse, sys
p = urllib.parse.urlparse(sys.argv[1])
netloc = p.netloc.split('@')[-1]  # strip any credentials
if not netloc:
    print('INVALID')
else:
    print(f'{p.scheme}://{netloc}')
" "$BASE")

if [ "$ORIGIN" = "INVALID" ] || [ -z "$ORIGIN" ]; then
  echo "Error: could not parse a valid host from '$DOMAIN'"
  exit 1
fi
# Ensure PAGE_PATH starts with /
case "$PAGE_PATH" in
  /*) ;;
  *) PAGE_PATH="/$PAGE_PATH" ;;
esac
PAGE="${BASE}${PAGE_PATH}"

echo "========================================"
echo " SEO + AEO AUDIT: $PAGE"
echo " $(date)"
echo "========================================"


# ── 1. ROBOTS.TXT ──────────────────────────
echo ""
echo "[ ROBOTS.TXT ]"
ROBOTS=$(curl -s --max-time 10 "$ORIGIN/robots.txt")

if [ -z "$ROBOTS" ]; then
  echo "  ❌ robots.txt not found or unreachable"
else
  echo "  ✓ robots.txt found"
  echo ""
  echo "  AI Crawler Access:"

  ROBOTS_TMPFILE=$(mktemp /tmp/robots_XXXXXX.txt)
  printf '%s' "$ROBOTS" > "$ROBOTS_TMPFILE"

  python3 - "$ROBOTS_TMPFILE" << 'PYEOF'
import sys, re

def is_bot_blocked(lines, bot_name):
    """
    Parse robots.txt. Specific bot rules take precedence over wildcard.
    Returns True=blocked, False=mentioned+allowed, None=not mentioned.
    """
    blocks = []
    current = []
    for line in lines:
        s = line.strip()
        if not s or s.startswith('#'):
            if current:
                blocks.append(current)
                current = []
        else:
            current.append(s)
    if current:
        blocks.append(current)

    specific_result = None
    wildcard_result = None

    for block in blocks:
        agents    = [l for l in block if l.lower().startswith('user-agent:')]
        disallows = [l for l in block if l.lower().startswith('disallow:')]
        bot_in_block      = any(bot_name.lower() in a.lower() for a in agents)
        wildcard_in_block = any(re.search(r'user-agent:\s*\*', a, re.IGNORECASE) for a in agents)

        if bot_in_block:
            blocked = any(
                re.sub(r'^disallow:\s*', '', d, flags=re.IGNORECASE).strip() in ('/', '/*')
                for d in disallows
            )
            specific_result = True if blocked else False
        elif wildcard_in_block:
            blocked = any(
                re.sub(r'^disallow:\s*', '', d, flags=re.IGNORECASE).strip() in ('/', '/*')
                for d in disallows
            )
            wildcard_result = True if blocked else False

    # Specific rule wins over wildcard; None = not mentioned anywhere
    result = specific_result if specific_result is not None else wildcard_result

    return result  # True=blocked, False=allowed, None=not mentioned

with open(sys.argv[1], encoding='utf-8', errors='replace') as f:
    raw = f.read()

lines = raw.replace('\r\n', '\n').replace('\r', '\n').split('\n')

bots = ["GPTBot", "ClaudeBot", "PerplexityBot", "GoogleOther", "Bytespider", "CCBot", "anthropic-ai"]
for bot in bots:
    result = is_bot_blocked(lines, bot)
    if result is True:
        print(f"  \u274c {bot} \u2014 BLOCKED")
    elif result is False:
        print(f"  \u2713  {bot} \u2014 allowed")
    else:
        print(f"  \u26a0  {bot} \u2014 not mentioned (defaults to allowed)")
PYEOF

  rm -f "$ROBOTS_TMPFILE"
fi


# ── 2. LLMS.TXT ────────────────────────────
echo ""
echo "[ LLMS.TXT ]"

LLMS_STATUS=$(curl -o /dev/null -s -w "%{http_code}" --max-time 10 "$ORIGIN/llms.txt")
if [ "$LLMS_STATUS" = "200" ]; then
  LLMS_SIZE=$(curl -s --max-time 10 "$ORIGIN/llms.txt" | wc -c)
  echo "  ✓ llms.txt found (HTTP 200, ~${LLMS_SIZE} bytes)"
else
  echo "  ❌ llms.txt missing (HTTP $LLMS_STATUS)"
  echo "     → HIGH PRIORITY: create at $ORIGIN/llms.txt"
  echo "     → Run: python3 scripts/generate_llms_txt.py"
fi

LLMS_FULL_STATUS=$(curl -o /dev/null -s -w "%{http_code}" --max-time 10 "$ORIGIN/llms-full.txt")
if [ "$LLMS_FULL_STATUS" = "200" ]; then
  echo "  ✓ llms-full.txt found"
else
  echo "  ⚠  llms-full.txt missing (recommended for full content indexing)"
fi


# ── 3. SITEMAP ─────────────────────────────
echo ""
echo "[ SITEMAP ]"

SITEMAP_STATUS=$(curl -o /dev/null -s -w "%{http_code}" --max-time 10 "$ORIGIN/sitemap.xml")
if [ "$SITEMAP_STATUS" = "200" ]; then
  SITEMAP_CONTENT=$(curl -s --max-time 10 "$ORIGIN/sitemap.xml")
  SITEMAP_URLS=$(echo "$SITEMAP_CONTENT" | grep -c "<url>" || true)
  SITEMAP_SUBS=$(echo "$SITEMAP_CONTENT" | grep -c "<sitemap>" || true)
  if [ "$SITEMAP_URLS" -gt 0 ]; then
    echo "  ✓ sitemap.xml found (~$SITEMAP_URLS URLs)"
  elif [ "$SITEMAP_SUBS" -gt 0 ]; then
    echo "  ✓ sitemap.xml found (sitemap index with ~$SITEMAP_SUBS sub-sitemaps)"
  else
    echo "  ✓ sitemap.xml found (~0 URLs — verify content is valid XML)"
  fi
else
  SITEMAP_LOCATION=$(echo "$ROBOTS" | grep -i "^Sitemap:" | head -1 | awk '{print $2}' | tr -d '\r')
  if [ -n "$SITEMAP_LOCATION" ]; then
    echo "  ✓ Sitemap declared in robots.txt: $SITEMAP_LOCATION"
  else
    echo "  ❌ sitemap.xml not found — submit to Google Search Console and Bing Webmaster Tools"
  fi
fi


# ── 4. FETCH PAGE HTML ─────────────────────
echo ""
echo "[ PAGE ANALYSIS: $PAGE ]"

HTML=$(curl -s --max-time 15 -A "Mozilla/5.0 (compatible; SEOAuditBot/1.0)" "$PAGE")

if [ -z "$HTML" ]; then
  echo "  ❌ Could not fetch page — check URL and server availability"
else

  # Write HTML to temp file — avoids ALL quoting issues in Python calls
  TMPFILE=$(mktemp /tmp/seo_audit_XXXXXX.html)
  printf '%s' "$HTML" > "$TMPFILE"

  # ── Title tag
  TITLE=$(python3 - "$TMPFILE" << 'PYEOF'
import sys, re
from html import unescape
with open(sys.argv[1], encoding='utf-8', errors='replace') as f:
    html = f.read()
# Strip HTML comments and script/style blocks before extracting title
clean_html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
clean_html = re.sub(r'<(script|style)[^>]*>.*?</(script|style)>', '', clean_html, flags=re.DOTALL|re.IGNORECASE)
m = re.search(r'<title[^>]*>(.*?)</title>', clean_html, re.IGNORECASE | re.DOTALL)
result = unescape(re.sub(r'<[^>]+>', '', m.group(1)).strip()) if m else 'NOT FOUND'
print(result)
PYEOF
)

  TITLE_LEN=${#TITLE}
  if [ "$TITLE" = "NOT FOUND" ] || [ "$TITLE_LEN" -eq 0 ]; then
    echo "  ❌ No <title> tag found — add one immediately"
  elif [ "$TITLE_LEN" -gt 60 ]; then
    echo "  Title ($TITLE_LEN chars): $TITLE"
    echo "  ⚠  Title too long — may be truncated in SERPs (keep under 60 chars)"
  else
    echo "  Title ($TITLE_LEN chars): $TITLE"
    echo "  ✓  Title length OK"
  fi

  # ── Meta description
  META=$(python3 - "$TMPFILE" << 'PYEOF'
import sys, re
from html import unescape
with open(sys.argv[1], encoding='utf-8', errors='replace') as f:
    html = f.read()
html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
html = re.sub(r'<(script|style)[^>]*>.*?</(script|style)>', '', html, flags=re.DOTALL|re.IGNORECASE)
m = re.search(
    r'<meta[^>]*name=["\']description["\'][^>]*content=(["\'])(.*?)\1',
    html, re.IGNORECASE | re.DOTALL
)
if not m:
    m = re.search(
        r'<meta[^>]*content=(["\'])(.*?)\1[^>]*name=["\']description["\']',
        html, re.IGNORECASE | re.DOTALL
    )
    print(unescape(m.group(2).strip()[:300]) if m else 'NOT FOUND')
else:
    print(unescape(m.group(2).strip()[:300]))
PYEOF
)

  META_LEN=${#META}
  if [ "$META" = "NOT FOUND" ] || [ "$META_LEN" -eq 0 ]; then
    echo "  Meta description: ❌ NOT FOUND — add a meta description to every page"
  elif [ "$META_LEN" -gt 160 ]; then
    echo "  Meta description ($META_LEN chars): ⚠  Too long (aim for 150-160 chars)"
    echo "  Preview: ${META:0:100}..."
  else
    echo "  Meta description ($META_LEN chars): ✓ OK"
    if [ "$META_LEN" -gt 100 ]; then
      echo "  Preview: ${META:0:100}..."
    else
      echo "  Preview: $META"
    fi
  fi

  # ── H1 tags
  H1_RESULT=$(python3 - "$TMPFILE" << 'PYEOF'
import sys, re
from html import unescape
with open(sys.argv[1], encoding='utf-8', errors='replace') as f:
    html = f.read()
html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
html = re.sub(r'<(script|style)[^>]*>.*?</(script|style)>', '', html, flags=re.DOTALL|re.IGNORECASE)
h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
clean = [unescape(re.sub(r'<[^>]+>', '', h).strip()) for h in h1s]
clean = [c for c in clean if c]  # remove empty/whitespace-only entries
if not clean:
    print('STATUS:NONE')
elif len(clean) == 1:
    print(f'STATUS:OK|{clean[0][:80]}')
else:
    text = ' | '.join(c[:40] for c in clean[:3])
    print(f'STATUS:MULTI|{len(clean)}|{text}')
PYEOF
)

  if [ -z "$H1_RESULT" ] || echo "$H1_RESULT" | grep -q "^STATUS:NONE$"; then
    echo "  H1: ❌ No H1 tag found — add one with your primary keyword"
  elif echo "$H1_RESULT" | grep -q "^STATUS:MULTI|"; then
    COUNT=$(echo "$H1_RESULT" | cut -d'|' -f2)
    TEXT=$(echo "$H1_RESULT" | cut -d'|' -f3-)
    echo "  H1: ⚠  $COUNT H1 tags found (should be exactly 1): $TEXT"
  else
    TEXT=$(echo "$H1_RESULT" | cut -d'|' -f2-)
    echo "  H1: ✓  $TEXT"
  fi

  # ── Schema markup
  echo ""
  echo "  Schema Markup:"
  python3 - "$TMPFILE" << 'PYEOF'
import sys, re, json
with open(sys.argv[1], encoding='utf-8', errors='replace') as f:
    html = f.read()
html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
schemas = re.findall(
    r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>',
    html, re.DOTALL | re.IGNORECASE
)
if not schemas:
    print('  ❌ NO SCHEMA FOUND')
    print('     Priority additions: Organization, FAQPage, Article')
else:
    found_types = []
    for i, s in enumerate(schemas):
        try:
            p = json.loads(s.strip())
            # ld+json can be an array — wrap in list and process each item
            items = p if isinstance(p, list) else [p]
            for p in items:
                if not isinstance(p, dict):
                    continue
                schema_type = p.get('@type', 'unknown')
                if isinstance(schema_type, list):
                    # @type can be a list e.g. ["Product", "ItemPage"] — filter None
                    clean_types = [str(t) for t in schema_type if t is not None]
                    found_types.extend(t.lower() for t in clean_types)
                    schema_type = ', '.join(clean_types)
                elif schema_type == 'unknown' and '@graph' in p:
                    graph = p['@graph']
                    if not isinstance(graph, list):
                        graph = [graph] if isinstance(graph, dict) else []
                    raw_types = [item.get('@type', '?') if isinstance(item, dict) else '?' for item in graph]
                    # Each @type in @graph may itself be a list or null — flatten safely
                    flat = []
                    for t in raw_types:
                        if isinstance(t, list):
                            flat.extend(str(x) for x in t if x is not None)
                        elif t is not None:
                            flat.append(str(t))
                        else:
                            flat.append('?')
                    schema_type = '@graph [' + ', '.join(flat) + ']'
                    found_types.extend(t.lower() for t in flat if t != '?')
                elif not isinstance(schema_type, str):
                    # @type is some other non-string type (int, dict, etc.) — coerce safely
                    schema_type = str(schema_type)
                else:
                    found_types.append(schema_type.lower())
                print(f'  ✓  Schema {i+1}: @type = {schema_type}')
        except json.JSONDecodeError as e:
            print(f'  ❌ Schema {i+1}: INVALID JSON — {e}')
        except Exception as e:
            print(f'  ❌ Schema {i+1}: ERROR — {e}')
    all_types = ' '.join(found_types)
    if 'faqpage' not in all_types:
        print('  ⚠  Missing FAQPage — high AEO impact, add Q&A section + schema')
    if 'organization' not in all_types and 'localbusiness' not in all_types:
        print('  ⚠  Missing Organization schema — add to homepage for entity recognition')
    if 'article' not in all_types and 'newsarticle' not in all_types:
        print('  ⚠  Missing Article schema — add to blog/guide pages for E-E-A-T')
PYEOF

  # ── SSR vs CSR detection
  echo ""
  CSR_SIGNALS=$(grep -cE "window\.__NEXT_DATA__|__nuxt__|ng-version|data-reactroot|__REACT_QUERY__" "$TMPFILE" 2>/dev/null)
  CSR_SIGNALS=${CSR_SIGNALS:-0}
  if [ "$CSR_SIGNALS" -gt 0 ]; then
    echo "  ⚠  CSR/SPA framework detected"
    echo "     → Verify key content is in HTML source (AI crawlers may not run JavaScript)"
    echo "     → Implement SSR or pre-rendering for critical pages"
  else
    echo "  ✓  No CSR signals detected (content likely server-rendered)"
  fi

  # ── HTTPS
  if echo "$PAGE" | grep -q "^https://"; then
    echo "  ✓  HTTPS enabled"
  else
    echo "  ❌ HTTP only — HTTPS is required for Google ranking and user trust"
  fi

  # ── Word count estimate
  WORD_COUNT=$(python3 - "$TMPFILE" << 'PYEOF'
import sys, re
with open(sys.argv[1], encoding='utf-8', errors='replace') as f:
    html = f.read()
# Strip tags and scripts/styles
text = re.sub(r'<(script|style)[^>]*>.*?</(script|style)>', ' ', html, flags=re.DOTALL|re.IGNORECASE)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text).strip()
print(len(text.split()))
PYEOF
)
  echo "  Estimated word count: ~${WORD_COUNT:-?} words"

  rm -f "$TMPFILE"
fi


# ── 5. PERFORMANCE ─────────────────────────
echo ""
echo "[ PERFORMANCE ]"

ENCODED_URL=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$PAGE")
PSI_URL="https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=${ENCODED_URL}&strategy=mobile"
PSI_RESPONSE=$(curl -s --max-time 20 "$PSI_URL" 2>/dev/null)

PSI_TMPFILE=$(mktemp /tmp/psi_XXXXXX.json)
echo "$PSI_RESPONSE" > "$PSI_TMPFILE"

PSI_RESULT=$(python3 - "$PSI_TMPFILE" << 'PYEOF'
import sys, json
with open(sys.argv[1], encoding='utf-8', errors='replace') as f:
    try:
        d = json.load(f)
    except Exception:
        print('  UNAVAILABLE')
        sys.exit()
try:
    cats = d['lighthouseResult']['categories']
    audits = d['lighthouseResult']['audits']
    score = int(cats['performance']['score'] * 100)
    lcp = audits['largest-contentful-paint']['displayValue']
    cls = audits['cumulative-layout-shift']['displayValue']
    inp = audits.get('interaction-to-next-paint', audits.get('max-potential-fid', {})).get('displayValue', 'N/A')
    status = '✓' if score >= 90 else ('⚠ ' if score >= 50 else '❌')
    print(f'  {status} Mobile Score: {score}/100  |  LCP: {lcp}  |  CLS: {cls}  |  INP: {inp}')
    if score < 50:
        print('  ❌ Poor performance — AI crawlers may time out, rankings will suffer')
    elif score < 90:
        print('  ⚠  Needs improvement — target LCP <2.5s, CLS <0.1, INP <200ms')
    else:
        print('  ✓  Good Core Web Vitals')
except Exception:
    print('  UNAVAILABLE')
PYEOF
)

rm -f "$PSI_TMPFILE"

if echo "$PSI_RESULT" | grep -q "UNAVAILABLE"; then
  echo "  ⚠  PageSpeed API not available in this environment"
  echo "     → Check manually: https://pagespeed.web.dev/?url=${ENCODED_URL}"
else
  echo "$PSI_RESULT"
fi


# ── 6. SUMMARY ─────────────────────────────
echo ""
echo "========================================"
echo " AUDIT COMPLETE"
echo "========================================"
echo ""
echo "  Next steps:"
echo "  1. Fix all ❌ CRITICAL items first (crawlability, HTTPS, title, H1)"
echo "  2. Address ⚠  WARNING items within 1-2 weeks (schema, llms.txt, speed)"
echo "  3. Generate llms.txt → run: python3 scripts/generate_llms_txt.py"
echo "  4. Test AI visibility manually:"
echo "       ChatGPT   → 'What is [your brand]?'"
echo "       Perplexity → '[your brand] [core topic]'"
echo "       Gemini    → 'Best [your service] for [use case]'"
echo ""
echo "  Reference guides:"
echo "    Traditional SEO  → references/traditional-seo.md"
echo "    AI/AEO playbook  → references/ai-seo-aeo.md"
echo "    Schema templates → references/schema-markup.md"
echo "========================================"
