"""
quarantine_batch_ingest.py — Batch ingest 13 repos từ QUARANTINE vào brain/knowledge/repos/
Pipeline: Security Check → Copy → Cleanup QUARANTINE

Chạy: python system/ops/scripts/quarantine_batch_ingest.py [--dry-run]
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# Dynamic root
_AOS_ROOT = os.getenv("AOS_ROOT") or str(Path(__file__).resolve().parents[3])
QUARANTINE_ROOT = Path(_AOS_ROOT) / "system" / "security" / "QUARANTINE"
BRAIN_PROCESSED = Path(_AOS_ROOT) / "brain" / "knowledge" / "processed_repos"
REJECTED_DIR = QUARANTINE_ROOT / "rejected"
LOG_FILE = QUARANTINE_ROOT / "logs" / "intake_log.md"

SKIP_DIRS = {"logs", "rejected", "incoming", "vetted", "pending_review", "approved"}
DRY_RUN = "--dry-run" in sys.argv

# Known bad patterns (simplified Strix check)
BAD_PATTERNS = ["xpfarm", "hexhog", "wifi-card", "leak", "prompt_leaks", "ransomware", "malware"]

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def strix_scan(repo_path: Path) -> tuple[bool, str]:
    """Security check: kiểm tra tên và nội dung cơ bản"""
    name = repo_path.name.lower()
    for bad in BAD_PATTERNS:
        if bad in name:
            return False, f"BLOCKED: tên repo chứa pattern nguy hiểm ({bad})"
    # Kiểm tra có README không (repo hợp lệ)
    has_readme = any((repo_path / f).exists() for f in ["README.md", "readme.md", "README.txt"])
    if not has_readme and not any(repo_path.glob("*.py")) and not any(repo_path.glob("*.js")):
        return False, "WARN: Repo không có README và không có source code rõ ràng"
    return True, "PASS"

def extract_and_cleanup(repo_path: Path, dry_run: bool = False) -> bool:
    """Nén repo thành file tri thức và xóa khỏi QUARANTINE"""
    dest_file = BRAIN_PROCESSED / f"{repo_path.name}_knowledge.md"

    if dest_file.exists():
        log(f"  [SKIP] {repo_path.name} → Đã được nén tại {dest_file.name}")
        if not dry_run: shutil.rmtree(repo_path, ignore_errors=True)
        return True

    if dry_run:
        log(f"  [DRY] WOULD EXTRACT {repo_path.name} → {dest_file.name} AND CLEANUP")
        return True

    extractor_script = Path(_AOS_ROOT) / "system" / "ops" / "scripts" / "knowledge_extractor.py"
    log(f"  [EXTRACT] Đang nén repo thành file Knowledge...")

    result = subprocess.run(
        [sys.executable, str(extractor_script), "--dir", str(repo_path), "--cleanup"],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        log(f"  [ERROR] Lỗi khi nén repo: {result.stderr[:200]}")
        return False

    log(f"  [INGEST] Đã nén thành {dest_file.name} và dọn sạch QUARANTINE.")
    return True

def write_log(entry: str):
    """Ghi log vào intake_log.md"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

def main():
    print(f"\n{'='*60}")
    print(f"  QUARANTINE BATCH INGEST {'(DRY RUN)' if DRY_RUN else '(LIVE)'}")
    print(f"  Root: {_AOS_ROOT}")
    print(f"{'='*60}\n")

    repos = sorted([p for p in QUARANTINE_ROOT.iterdir()
                    if p.is_dir() and p.name not in SKIP_DIRS])

    if not repos:
        log("Không có repo nào trong QUARANTINE để xử lý.")
        return

    log(f"Tìm thấy {len(repos)} repos cần xử lý:\n")

    results = {"ingested": [], "rejected": [], "skipped": []}

    for repo in repos:
        print(f"\n--- [{repo.name}] ---")

        # STEP 1: Security Scan
        log(f"  [STRIX] Đang quét bảo mật...")
        ok, reason = strix_scan(repo)
        log(f"  [STRIX] {reason}")

        if not ok:
            log(f"  [REJECT] {repo.name} → QUARANTINE/rejected/")
            if not DRY_RUN:
                REJECTED_DIR.mkdir(parents=True, exist_ok=True)
                shutil.move(str(repo), str(REJECTED_DIR / repo.name))
            results["rejected"].append(repo.name)
            write_log(f"| {datetime.now().strftime('%Y-%m-%d %H:%M')} | {repo.name} | REJECTED | {reason} |")
            continue

        # STEP 2: Trích xuất và dọn dẹp
        log(f"  [INGEST] Đóng gói vào brain/knowledge/processed_repos/...")
        success = extract_and_cleanup(repo, dry_run=DRY_RUN)

        if success:
            results["ingested"].append(repo.name)
            write_log(f"| {datetime.now().strftime('%Y-%m-%d %H:%M')} | {repo.name} | INGESTED_AS_KNOWLEDGE | Batch extract from QUARANTINE |")

    # SUMMARY
    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"  Ingested : {len(results['ingested'])} repos")
    print(f"  Rejected : {len(results['rejected'])} repos")
    print(f"  Skipped  : {len(results['skipped'])} repos")
    print(f"{'='*60}\n")

    if results["ingested"]:
        print("✅ Ingested:")
        for r in results["ingested"]: print(f"   └─ {r}")
    if results["rejected"]:
        print("❌ Rejected (moved to QUARANTINE/rejected/):")
        for r in results["rejected"]: print(f"   └─ {r}")

if __name__ == "__main__":
    main()
