#!/usr/bin/env python3
"""
llms.txt Generator — SEO/AEO Skill
Claude Code will run this interactively or call generate() directly.

Usage:
  python3 generate_llms_txt.py                    # interactive mode
  python3 generate_llms_txt.py --json config.json # from JSON config
"""

import json
import sys
import os
from datetime import datetime

def generate(config: dict) -> tuple[str, str]:
    """
    Generate llms.txt and llms-full.txt content from config dict.

    Config keys:
      brand_name        str   — Company/brand name
      brand_description str   — One paragraph description
      base_url          str   — https://yourdomain.com
      pages             list  — Each: {"title": str, "url": str, "description": str, "category": str, "full_content": str (optional)}

    Returns: (llms_txt_content, llms_full_txt_content)
    """

    for key in ("brand_name", "brand_description"):
        if key not in config:
            raise ValueError(f"config missing required key '{key}'")
    brand = str(config["brand_name"]).replace('\n', ' ').replace('\r', ' ').strip()
    desc = str(config["brand_description"]).replace('\n', ' ').replace('\r', ' ').strip()
    if not brand:
        raise ValueError("brand_name cannot be empty")
    if not desc:
        raise ValueError("brand_description cannot be empty")
    if "base_url" not in config:
        raise ValueError("config missing required key 'base_url'")
    base = str(config["base_url"]).rstrip("/")
    # Validate base_url has a real netloc (catches 'https://', 'https:', etc.)
    try:
        import urllib.parse as _up
        _p = _up.urlparse(base)
        if not _p.netloc:
            raise ValueError(f"base_url '{base}' has no valid host")
    except Exception as e:
        raise ValueError(f"base_url is invalid: {e}")

    pages = config.get("pages", [])
    if not isinstance(pages, list):
        pages = []

    # Category order for llms.txt
    category_order = [
        "Core Documentation",
        "How-To Guides",
        "Definitions & Glossary",
        "Research & Data",
        "Products & Services",
        "Case Studies",
        "Blog & Insights",
        "About & Authority",
        "Contact",
    ]

    # Group pages by category — skip non-dict entries
    categorized = {}
    for page in pages:
        if not isinstance(page, dict):
            continue
        cat = page.get("category") or "Blog & Insights"
        if cat not in categorized:
            categorized[cat] = []
        categorized[cat].append(page)

    def make_url(base, raw_url):
        """Ensure URL is absolute and well-formed."""
        if not raw_url:
            return base + "/"
        raw_url = str(raw_url)
        if raw_url.startswith("http://") or raw_url.startswith("https://"):
            url = raw_url
        else:
            if not raw_url.startswith("/"):
                raw_url = "/" + raw_url
            url = base + raw_url
        # Encode bare parens in URLs so markdown links don't break
        return url.replace("(", "%28").replace(")", "%29")

    def safe_title(t):
        """Escape ] in titles so markdown link syntax isn't broken."""
        return str(t).replace("]", "\\]")

    # ── llms.txt ──────────────────────────────────────────────────
    lines = [f"# {brand}", ""]
    lines.append(f"> {desc}")
    lines.append("")

    for cat in category_order:
        if cat not in categorized:
            continue
        lines.append(f"## {cat}")
        for page in categorized[cat]:
            url = make_url(base, page.get("url", "/"))
            title = safe_title(page.get("title", "Untitled") or "Untitled")
            description = page.get("description", "") or ""
            lines.append(f"- [{title}]({url}): {description}")
        lines.append("")

    # Add uncategorized
    known_cats = set(category_order)
    for cat, cat_pages in categorized.items():
        if cat not in known_cats:
            lines.append(f"## {cat}")
            for page in cat_pages:
                url = make_url(base, page.get("url", "/"))
                title = safe_title(page.get("title", "Untitled") or "Untitled")
                description = page.get("description", "") or ""
                lines.append(f"- [{title}]({url}): {description}")
            lines.append("")

    llms_txt = "\n".join(lines)

    # ── llms-full.txt ─────────────────────────────────────────────
    full_lines = [f"# {brand} — Full Content Index", ""]
    full_lines.append(f"> {desc}")
    full_lines.append("")
    full_lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d')}*")
    full_lines.append("")
    full_lines.append("---")
    full_lines.append("")

    for cat in category_order:
        if cat not in categorized:
            continue
        full_lines.append(f"## {cat}")
        full_lines.append("")
        for page in categorized[cat]:
            url = make_url(base, page.get("url", "/"))
            title = safe_title(page.get("title", "Untitled") or "Untitled")
            description = page.get("description", "") or ""
            full_lines.append(f"### [{title}]({url})")
            full_lines.append(f"*{description}*")
            full_lines.append("")
            fc = page.get("full_content")
            if isinstance(fc, str) and fc.strip():
                full_lines.append(fc)
            else:
                full_lines.append(f"[Full content available at: {url}]")
            full_lines.append("")
            full_lines.append("---")
            full_lines.append("")

    # Also include uncategorized pages in llms-full.txt
    known_cats = set(category_order)
    for cat, cat_pages in categorized.items():
        if cat not in known_cats:
            full_lines.append(f"## {cat}")
            full_lines.append("")
            for page in cat_pages:
                url = make_url(base, page.get("url", "/"))
                title = safe_title(page.get("title", "Untitled") or "Untitled")
                description = page.get("description", "") or ""
                full_lines.append(f"### [{title}]({url})")
                full_lines.append(f"*{description}*")
                full_lines.append("")
                fc = page.get("full_content")
                if isinstance(fc, str) and fc.strip():
                    full_lines.append(fc)
                else:
                    full_lines.append(f"[Full content available at: {url}]")
                full_lines.append("")
                full_lines.append("---")
                full_lines.append("")

    llms_full_txt = "\n".join(full_lines)

    return llms_txt, llms_full_txt


def interactive():
    print("=" * 50)
    print("  llms.txt Generator — SEO/AEO Skill")
    print("=" * 50)
    print()

    try:
        config = {}

        config["brand_name"] = input("Brand/company name: ").strip()
        if not config["brand_name"]:
            print("Error: brand name cannot be empty")
            sys.exit(1)
        config["base_url"] = input("Base URL (e.g. https://yourdomain.com): ").strip().rstrip("/")
        if not (config["base_url"].startswith("http://") or config["base_url"].startswith("https://")):
            print("Error: base URL must start with http:// or https://")
            sys.exit(1)
        from urllib.parse import urlparse as _urlparse
        if not _urlparse(config["base_url"]).netloc:
            print("Error: base URL has no valid host (e.g. https://yourdomain.com)")
            sys.exit(1)
        config["brand_description"] = input(
            "One-sentence description (what you do + who you serve):\n> "
        ).strip()
        if not config["brand_description"]:
            print("Error: brand description cannot be empty")
            sys.exit(1)

        print("\nNow add your pages. Press Enter with no title to finish.\n")

        categories = [
            "Core Documentation",
            "How-To Guides",
            "Definitions & Glossary",
            "Research & Data",
            "Products & Services",
            "About & Authority",
            "Blog & Insights",
            "Contact",
        ]

        pages = []
        while True:
            title = input("Page title (or press Enter to finish): ").strip()
            if not title:
                break
            url = input("  URL path (e.g. /about or full URL): ").strip()
            description = input("  One-line description: ").strip()

            print("  Category options:")
            for i, cat in enumerate(categories, 1):
                print(f"    {i}. {cat}")
            cat_choice = input("  Choose category (1–8) or type custom: ").strip()

            try:
                cat_idx = int(cat_choice) - 1
                category = categories[cat_idx] if 0 <= cat_idx < len(categories) else cat_choice
            except ValueError:
                category = cat_choice

            pages.append({
                "title": title,
                "url": url,
                "description": description,
                "category": category,
            })
            print(f"  ✓ Added: {title}\n")

        config["pages"] = pages

    except EOFError:
        print("\nError: input ended unexpectedly. Use --json mode for non-interactive use:")
        print("  python3 generate_llms_txt.py --json config.json")
        sys.exit(1)

    # Generate
    try:
        llms_txt, llms_full_txt = generate(config)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Save files
    output_dir = os.getcwd()

    llms_path = os.path.join(output_dir, "llms.txt")
    llms_full_path = os.path.join(output_dir, "llms-full.txt")
    config_path = os.path.join(output_dir, "llms-config.json")
    try:
        with open(llms_path, "w") as f:
            f.write(llms_txt)
        print(f"\n✓ Saved: {llms_path}")

        with open(llms_full_path, "w") as f:
            f.write(llms_full_txt)
        print(f"✓ Saved: {llms_full_path}")

        # Save config for reuse
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        print(f"✓ Config saved: {config_path} (reuse with --json flag)")
    except OSError as e:
        print(f"\nError: could not write output files — {e}")
        print(f"Try running from a directory where you have write permission.")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("  DEPLOYMENT INSTRUCTIONS")
    print("=" * 50)
    base = config["base_url"].rstrip("/")
    print(f"""
1. Upload llms.txt to: {base}/llms.txt
2. Upload llms-full.txt to: {base}/llms-full.txt
3. Verify access:
   curl -I {base}/llms.txt
   (should return HTTP 200)

4. Register at: https://llmstxt.org/
5. Test AI visibility:
   - Search "{config['brand_name']}" in Perplexity
   - Ask "What does {config['brand_name']} do?" in ChatGPT
   - Repeat monthly to track improvements
""")

    return llms_txt, llms_full_txt


def from_json(json_path: str):
    if not os.path.exists(json_path):
        print(f"Error: config file not found: {json_path}")
        sys.exit(1)
    try:
        with open(json_path, encoding='utf-8', errors='replace') as f:
            config = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"Error: invalid or unreadable JSON in {json_path}: {e}")
        sys.exit(1)
    if not isinstance(config, dict):
        print(f"Error: config file must contain a JSON object, not {type(config).__name__}")
        sys.exit(1)
    for key in ("brand_name", "brand_description", "base_url"):
        if key not in config:
            print(f"Error: missing required key '{key}' in config file")
            sys.exit(1)
        if not str(config[key]).strip() if config[key] is not None else True:
            print(f"Error: '{key}' cannot be empty or null in config file")
            sys.exit(1)
    try:
        llms_txt, llms_full_txt = generate(config)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    try:
        with open("llms.txt", "w") as f:
            f.write(llms_txt)
        with open("llms-full.txt", "w") as f:
            f.write(llms_full_txt)
    except OSError as e:
        print(f"Error: could not write output files — {e}")
        sys.exit(1)
    print("✓ Generated llms.txt")
    print("✓ Generated llms-full.txt")
    return llms_txt, llms_full_txt


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        if len(sys.argv) < 3:
            print("Error: --json requires a config file path")
            print("Usage: python3 generate_llms_txt.py --json config.json")
            sys.exit(1)
        from_json(sys.argv[2])
    else:
        interactive()
