"""
pending_civ_classifier.py — Batch CIV Pre-Analysis cho PENDING_REPOS.md
RULE-CIV-02: PENDING → CIV Analysis → APPROVE/REJECT → ACTIVE_REPOS.md → clone

Script này KHÔNG clone repo. Chỉ phân tích URL/metadata để CEO có báo cáo duyệt.
Pipeline đúng: URL analyze → verdict → CEO review → approve → đưa vào ACTIVE_REPOS.md

Chạy: python system/ops/scripts/pending_civ_classifier.py
"""
import os, re, sys
from pathlib import Path
from datetime import datetime

_AOS_ROOT = os.getenv("AOS_ROOT") or str(Path(__file__).resolve().parents[3])
PENDING_FILE  = Path(_AOS_ROOT) / "storage" / "vault" / "DATA" / "PENDING_REPOS.md"
ACTIVE_FILE   = Path(_AOS_ROOT) / "storage" / "vault" / "DATA" / "ACTIVE_REPOS.md"
REPORT_DIR    = Path(_AOS_ROOT) / "system" / "security" / "QUARANTINE" / "logs"
REPORT_FILE   = REPORT_DIR / f"CIV_PENDING_REPORT_{datetime.now().strftime('%Y%m%d_%H%M')}.md"

# Domain classification rules (keyword-based, no LLM needed)
DOMAIN_RULES = {
    "AI/LLM": ["llm", "gpt", "claude", "gemini", "ollama", "langchain", "agent", "openai",
                "huggingface", "transformers", "embedding", "rag", "vector", "ai-", "-ai",
                "notebook", "ml-", "deep-", "neural", "diffusion", "stablediffusion"],
    "DevTools": ["vscode", "vim", "neovim", "editor", "linter", "formatter", "cli",
                 "terminal", "shell", "zsh", "bash", "git", "docker", "kubernetes", "k8s"],
    "Frontend": ["react", "vue", "angular", "next", "nuxt", "svelte", "tailwind", "ui",
                 "animation", "css", "html", "frontend", "web-", "-web"],
    "Backend/API": ["fastapi", "flask", "django", "express", "rails", "spring", "api",
                    "backend", "server", "rest", "graphql", "grpc"],
    "Data/Analytics": ["pandas", "numpy", "spark", "etl", "pipeline", "analytics",
                       "dashboard", "visualization", "chart", "graph", "sql", "postgres"],
    "Security": ["security", "pentest", "vulnerability", "exploit", "scanner", "firewall",
                 "crypto", "auth", "jwt", "oauth", "cert"],
    "Automation": ["n8n", "zapier", "workflow", "automation", "cron", "scheduler",
                   "bot", "scraper", "crawler", "rpa"],
    "Reference/Awesome": ["awesome-", "roadmap", "public-api", "gitignore", "cheatsheet",
                          "learn", "tutorial", "course", "resource"],
}

# Strix patterns — tự động reject
REJECT_PATTERNS = ["xpfarm", "hexhog", "prompt_leak", "jailbreak", "bypass-",
                   "crack-", "hack-tools", "malware", "keylogger", "stealer"]

# Domain relevance cho AI OS Corp
RELEVANT_DOMAINS = {"AI/LLM", "DevTools", "Automation", "Security", "Data/Analytics"}
REVIEW_DOMAINS   = {"Backend/API", "Frontend", "Reference/Awesome"}

def classify_repo(url: str) -> dict:
    name = url.rstrip("/").split("/")[-1].lower()
    owner = url.split("/")[-2].lower() if url.count("/") >= 3 else ""

    # Strix pre-check
    for pat in REJECT_PATTERNS:
        if pat in name or pat in owner:
            return {"url": url, "name": name, "domain": "BLOCKED", "verdict": "REJECT",
                    "reason": f"Pattern nguy hiểm: {pat}"}

    # Domain classification
    domain = "Uncategorized"
    for d, keywords in DOMAIN_RULES.items():
        if any(k in name or k in owner for k in keywords):
            domain = d
            break

    # Verdict
    if domain == "Uncategorized":
        verdict = "REVIEW"
        reason = "Không phân loại được — cần CEO xem tay"
    elif domain in RELEVANT_DOMAINS:
        verdict = "APPROVE"
        reason = f"Domain '{domain}' phù hợp AI OS Corp"
    elif domain in REVIEW_DOMAINS:
        verdict = "REVIEW"
        reason = f"Domain '{domain}' cần CEO xem xét"
    else:
        verdict = "REVIEW"
        reason = "BLOCKED domain"

    return {"url": url, "name": name, "domain": domain, "verdict": verdict, "reason": reason}

def get_active_urls() -> set:
    if not ACTIVE_FILE.exists(): return set()
    content = ACTIVE_FILE.read_text(encoding="utf-8", errors="ignore")
    return set(re.findall(r'https://github\.com/[\w\-\.]+/[\w\-\.]+', content))

def get_pending_urls() -> list:
    content = PENDING_FILE.read_text(encoding="utf-8", errors="ignore")
    urls = re.findall(r'https://github\.com/[\w\-\.]+/[\w\-\.]+', content)
    seen, unique = set(), []
    for u in urls:
        if u not in seen: seen.add(u); unique.append(u)
    return unique

def main():
    print(f"\n{'='*65}")
    print(f"  PENDING CIV PRE-CLASSIFIER v1.0")
    print(f"  RULE-CIV-02: Phân tích trước khi cấp phép clone")
    print(f"{'='*65}\n")

    pending_urls = get_pending_urls()
    active_urls  = get_active_urls()

    # Filter: bỏ những cái đã ACTIVE
    to_classify = [u for u in pending_urls if u not in active_urls]
    print(f"PENDING: {len(pending_urls)} | Đã ACTIVE: {len(pending_urls)-len(to_classify)} | Cần phân tích: {len(to_classify)}\n")

    results = {"APPROVE": [], "REVIEW": [], "REJECT": []}
    for url in to_classify:
        r = classify_repo(url)
        results[r["verdict"]].append(r)

    # Write CIV report
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# CIV PENDING BATCH REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"> **RULE-CIV-02**: Báo cáo này cần CEO/intake-chief REVIEW & APPROVE trước khi repo được clone\n\n")
        f.write(f"## Summary\n")
        f.write(f"- Total analyzed: {len(to_classify)}\n")
        f.write(f"- ✅ APPROVE (phù hợp, sẵn sàng duyệt): **{len(results['APPROVE'])}**\n")
        f.write(f"- 🔍 REVIEW (cần CEO xem tay): **{len(results['REVIEW'])}**\n")
        f.write(f"- ❌ REJECT (loại bỏ): **{len(results['REJECT'])}**\n\n")
        f.write(f"## ✅ APPROVE LIST — ({len(results['APPROVE'])} repos)\n\n")
        f.write(f"> CEO: Duyệt những cái này sẽ được chuyển vào ACTIVE_REPOS.md tự động\n\n")
        f.write(f"| # | Repo | Domain | Lý do |\n|---|------|--------|-------|\n")
        for i, r in enumerate(results["APPROVE"], 1):
            f.write(f"| {i} | [{r['name']}]({r['url']}) | {r['domain']} | {r['reason']} |\n")
        f.write(f"\n## 🔍 REVIEW LIST — ({len(results['REVIEW'])} repos, CEO xem tay)\n\n")
        f.write(f"| # | Repo | Domain | Lý do |\n|---|------|--------|-------|\n")
        for i, r in enumerate(results["REVIEW"], 1):
            f.write(f"| {i} | [{r['name']}]({r['url']}) | {r['domain']} | {r['reason']} |\n")
        f.write(f"\n## ❌ REJECT LIST — ({len(results['REJECT'])} repos)\n\n")
        for r in results["REJECT"]:
            f.write(f"- {r['url']} — {r['reason']}\n")

    print(f"✅ APPROVE : {len(results['APPROVE'])} repos")
    print(f"🔍 REVIEW  : {len(results['REVIEW'])} repos")
    print(f"❌ REJECT  : {len(results['REJECT'])} repos")
    print(f"\n📄 CIV Report: {REPORT_FILE}")
    print(f"\nBước tiếp theo — CEO review report và approve:")
    print(f"  python system/ops/scripts/pending_civ_approve.py --auto-approve")

if __name__ == "__main__":
    main()
