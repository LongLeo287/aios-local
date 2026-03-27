"""
active_repos_pipeline.py — Ingest ACTIVE_REPOS.md qua đúng pipeline AI OS Corp
Pipeline: git clone --depth=1 → QUARANTINE/incoming/repos/ → Strix scan → brain/knowledge/repos/ → cleanup

Chạy: python system/ops/scripts/active_repos_pipeline.py [--dry-run]
"""
import os, sys, re, shutil, subprocess
from pathlib import Path
from datetime import datetime

_AOS_ROOT = os.getenv("AOS_ROOT") or str(Path(__file__).resolve().parents[3])
QUARANTINE_INCOMING = Path(_AOS_ROOT) / "system" / "security" / "QUARANTINE" / "incoming" / "repos"
QUARANTINE_REJECTED = Path(_AOS_ROOT) / "system" / "security" / "QUARANTINE" / "rejected"
BRAIN_PROCESSED     = Path(_AOS_ROOT) / "brain" / "knowledge" / "processed_repos"
ACTIVE_REPOS_FILE   = Path(_AOS_ROOT) / "storage" / "vault" / "DATA" / "ACTIVE_REPOS.md"
LOG_FILE            = Path(_AOS_ROOT) / "system" / "security" / "QUARANTINE" / "logs" / "intake_log.md"
PROGRESS_FILE       = Path(_AOS_ROOT) / "system" / "security" / "QUARANTINE" / "logs" / ".pipeline_progress.json"

DRY_RUN = "--dry-run" in sys.argv
BAD_PATTERNS = ["xpfarm", "hexhog", "malware", "ransomware", "prompt_leak"]

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def load_progress():
    import json
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {"done": [], "failed": []}

def save_progress(state):
    import json
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(state, indent=2))

def get_repo_urls(file_path):
    content = file_path.read_text(encoding="utf-8", errors="ignore")
    urls = re.findall(r'https://github\.com/[\w\-\.]+/[\w\-\.]+', content)
    seen, unique = set(), []
    for u in urls:
        if u not in seen: seen.add(u); unique.append(u)
    return unique

def strix_scan(repo_name: str, repo_path: Path) -> tuple[bool, str]:
    for bad in BAD_PATTERNS:
        if bad in repo_name.lower():
            return False, f"BLOCKED: pattern '{bad}' trong tên repo"
    has_code = (any(repo_path.rglob("*.py")) or any(repo_path.rglob("*.js"))
                or any(repo_path.rglob("*.ts")) or any(repo_path.rglob("*.md")))
    if not has_code:
        return False, "WARN: Repo trống, không có code hay docs"
    return True, "PASS"

def clone_repo(url: str, dest: Path, dry_run: bool = False) -> bool:
    if dest.exists():
        log(f"  [EXISTS] {dest.name} đã có sẵn trong incoming")
        return True
    if dry_run:
        log(f"  [DRY] WOULD clone {url}")
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(
            ["git", "clone", "--depth=1", "--quiet", url, str(dest)],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            log(f"  [ERROR] clone thất bại: {result.stderr[:100]}")
            shutil.rmtree(dest, ignore_errors=True)
            return False
    except subprocess.TimeoutExpired:
        log(f"  [TIMEOUT] clone mất quá 120s, bỏ qua repo {url}")
        shutil.rmtree(dest, ignore_errors=True)
        return False
    except Exception as e:
        log(f"  [ERROR] lỗi không mong muốn khi clone: {e}")
        shutil.rmtree(dest, ignore_errors=True)
        return False
    return True

def extract_and_cleanup(src: Path, dry_run: bool = False) -> bool:
    dest_file = BRAIN_PROCESSED / f"{src.name}_knowledge.md"
    if dest_file.exists():
        log(f"  [SKIP] {src.name} đã được chiết xuất tại {dest_file.name}")
        if not dry_run: shutil.rmtree(src, ignore_errors=True)
        return True

    if dry_run:
        log(f"  [DRY] WOULD extract {src.name} → {dest_file.name} and cleanup")
        return True

    extractor_script = Path(_AOS_ROOT) / "system" / "ops" / "scripts" / "knowledge_extractor.py"
    log(f"  [EXTRACT] Đang nén repo thành file Knowledge...")

    result = subprocess.run(
        [sys.executable, str(extractor_script), "--dir", str(src), "--cleanup"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )

    if result.returncode != 0:
        log(f"  [ERROR] Lỗi khi nén repo:\n{result.stderr}")
        return False

    log(f"  [INGEST] Đã lưu {dest_file.name} và xóa raw clone.")
    return True

def write_log(repo_name, url, status, reason):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"| {ts} | {repo_name} | {status} | {reason} | {url} |\n")

def main():
    print(f"\n{'='*65}")
    print(f"  ACTIVE REPOS PIPELINE {'(DRY RUN)' if DRY_RUN else '(LIVE)'}")
    print(f"  Root: {_AOS_ROOT}")
    print(f"{'='*65}\n")

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--file", type=str, default="")
    args, _ = parser.parse_known_args()

    target_file = Path(args.file) if args.file else ACTIVE_REPOS_FILE
    if not target_file.exists():
        log(f"Error: {target_file} không tồn tại!")
        return

    urls = get_repo_urls(target_file)
    state = load_progress()

    # Filter repos already done
    todo = [u for u in urls if u not in state["done"] and u not in state["failed"]]
    log(f"File: {target_file.name} | Tổng: {len(urls)} | Đã xong: {len(state['done'])} | Bỏ qua: {len(state['failed'])} | Cần xử lý: {len(todo)}")

    results = {"ingested": 0, "rejected": 0, "failed": 0, "skipped": 0}

    for i, url in enumerate(todo, 1):
        repo_name = url.rstrip("/").split("/")[-1]
        print(f"\n[{i}/{len(todo)}] {url}")

        # STEP 1: Clone vào QUARANTINE/incoming/repos/
        log("  [STEP 1] Strix pre-check tên repo...")
        for bad in BAD_PATTERNS:
            if bad in repo_name.lower():
                log(f"  [REJECT] Tên repo chứa pattern nguy hiểm")
                write_log(repo_name, url, "REJECTED", f"Bad pattern: {bad}")
                state["failed"].append(url)
                results["rejected"] += 1
                save_progress(state)
                continue

        incoming_path = QUARANTINE_INCOMING / repo_name
        log(f"  [STEP 2] git clone --depth=1 → QUARANTINE/incoming/repos/{repo_name}")
        ok = clone_repo(url, incoming_path, DRY_RUN)
        if not ok:
            log(f"  [FAIL] Không clone được — bỏ qua")
            state["failed"].append(url)
            results["failed"] += 1
            save_progress(state)
            continue

        # STEP 3: Strix scan trên code thực tế
        if not DRY_RUN and incoming_path.exists():
            log("  [STEP 3] Strix security scan...")
            ok, reason = strix_scan(repo_name, incoming_path)
            log(f"  [STRIX] {reason}")
            if not ok:
                QUARANTINE_REJECTED.mkdir(parents=True, exist_ok=True)
                shutil.move(str(incoming_path), str(QUARANTINE_REJECTED / repo_name))
                write_log(repo_name, url, "REJECTED", reason)
                state["failed"].append(url)
                results["rejected"] += 1
                save_progress(state)
                continue

        # STEP 4: Extract Knowledge → brain/knowledge/processed_repos/ + cleanup incoming
        log("  [STEP 4] Trích xuất Tri thức và dọn rác (Knowledge Extractor)...")
        if extract_and_cleanup(incoming_path, DRY_RUN):
            write_log(repo_name, url, "INGESTED_AS_KNOWLEDGE", "Nén thành .md và xóa raw clone")
            state["done"].append(url)
            results["ingested"] += 1
            save_progress(state)
            log(f"  [OK] {repo_name} ✅ DONE")

    print(f"\n{'='*65}")
    print(f"  SUMMARY")
    print(f"  Ingested : {results['ingested']}")
    print(f"  Rejected : {results['rejected']}")
    print(f"  Failed   : {results['failed']}")
    print(f"  Skipped  : {results['skipped']}")
    print(f"{'='*65}")
    if todo:
        print(f"\n✅ Progress saved → chạy lại nếu mạng đứt, tự tiếp tục từ chỗ dừng!")

if __name__ == "__main__":
    main()
