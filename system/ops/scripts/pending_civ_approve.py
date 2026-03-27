"""
pending_civ_approve.py — Approve batch PENDING repos sau khi CEO review CIV report
Đọc CIV report mới nhất → lấy APPROVE list → thêm vào ACTIVE_REPOS.md → kích hoạt pipeline

Chạy: python system/ops/scripts/pending_civ_approve.py [--auto-approve] [--report <path>]
  --auto-approve  : Tự động approve tất cả APPROVE list (CEO đã review report rồi)
"""
import os, re, sys
from pathlib import Path
from datetime import datetime

_AOS_ROOT = os.getenv("AOS_ROOT") or str(Path(__file__).resolve().parents[3])
ACTIVE_FILE  = Path(_AOS_ROOT) / "storage" / "vault" / "DATA" / "ACTIVE_REPOS.md"
REPORT_DIR   = Path(_AOS_ROOT) / "system" / "security" / "QUARANTINE" / "logs"

AUTO_APPROVE = "--auto-approve" in sys.argv

def get_latest_report() -> Path | None:
    reports = sorted(REPORT_DIR.glob("CIV_PENDING_REPORT_*.md"), reverse=True)
    return reports[0] if reports else None

def parse_approve_list(report: Path) -> list[dict]:
    content = report.read_text(encoding="utf-8", errors="ignore")
    # Extract APPROVE section
    approve_section = re.search(r'## ✅ APPROVE LIST.*?(?=## 🔍|## ❌|$)', content, re.DOTALL)
    if not approve_section: return []
    rows = re.findall(r'\|\s*\d+\s*\|\s*\[([^\]]+)\]\((https://[^\)]+)\)\s*\|\s*([^\|]+)\s*\|', approve_section.group())
    return [{"name": r[0], "url": r[1].strip(), "domain": r[2].strip()} for r in rows]

def get_active_urls() -> set:
    if not ACTIVE_FILE.exists(): return set()
    return set(re.findall(r'https://github\.com/[\w\-\.]+/[\w\-\.]+',
                          ACTIVE_FILE.read_text(encoding="utf-8", errors="ignore")))

def append_to_active(repos: list[dict]):
    """Thêm repos đã approve vào ACTIVE_REPOS.md"""
    ts = datetime.now().strftime("%Y-%m-%d")
    ACTIVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not ACTIVE_FILE.exists():
        ACTIVE_FILE.write_text(f"# ⭐ ACTIVE REPOS — AI OS Corp ({ts})\n\n")

    existing = get_active_urls()
    new_repos = [r for r in repos if r["url"] not in existing]

    if not new_repos:
        print("[OK] Tất cả repos đã có trong ACTIVE_REPOS.md")
        return 0

    with open(ACTIVE_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n## BATCH APPROVED — {ts} (auto via CIV classifier)\n\n")
        for r in new_repos:
            f.write(f"### {r['name']}\n")
            f.write(f"🔗 {r['url']}\n")
            f.write(f"- **Domain:** {r['domain']}\n")
            f.write(f"- **Status:** ✅ APPROVED (CIV batch)\n")
            f.write(f"- **CIV:** Passed keyword classifier — RULE-CIV-02\n\n")
    return len(new_repos)

def main():
    print(f"\n{'='*65}")
    print(f"  PENDING CIV APPROVE")
    print(f"  {'AUTO-APPROVE mode' if AUTO_APPROVE else 'Interactive mode'}")
    print(f"{'='*65}\n")

    report = get_latest_report()
    if not report:
        print("[ERROR] Không tìm thấy CIV report. Chạy pending_civ_classifier.py trước!")
        return

    print(f"Using report: {report.name}")
    approve_list = parse_approve_list(report)
    print(f"APPROVE list: {len(approve_list)} repos\n")

    if not approve_list:
        print("[WARN] Không có repos nào trong APPROVE list")
        return

    # Sample top 10 để CEO xem
    print("Sample repos sẽ được APPROVE:")
    for r in approve_list[:10]:
        print(f"  [{r['domain']}] {r['name']} — {r['url']}")
    if len(approve_list) > 10:
        print(f"  ... và {len(approve_list)-10} repos nữa\n")

    if not AUTO_APPROVE:
        confirm = input(f"\nApprove {len(approve_list)} repos vào ACTIVE_REPOS.md? [y/N]: ")
        if confirm.lower() != 'y':
            print("Huỷ. CEO chưa approve.")
            return

    # Thêm vào ACTIVE_REPOS.md
    added = append_to_active(approve_list)
    print(f"\n✅ Đã thêm {added} repos mới vào ACTIVE_REPOS.md")
    print(f"\nBước tiếp theo — Clone & Ingest:")
    print(f"  python system/ops/scripts/active_repos_pipeline.py")

if __name__ == "__main__":
    main()
