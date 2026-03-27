import os
import sys
import time
import shutil
import argparse
from pathlib import Path

# AI OS Path Mapping
AOS_ROOT = Path(os.environ.get("AOS_ROOT", os.environ.get("AOS_ROOT", ".")))
USER_PROFILE = Path(os.environ.get("USERPROFILE", "C:\\Users\\Default"))
GEMINI_CACHE = USER_PROFILE / ".gemini"

# Sanitation Targets
TARGET_DIRS = [
    AOS_ROOT / "system" / "security" / "QUARANTINE",
    AOS_ROOT / "storage" / "vault" / "DATA",
    GEMINI_CACHE
]
REPO_DIR = AOS_ROOT / "brain" / "knowledge" / "repos"
STRAY_DIR = AOS_ROOT / "storage" / "vault" / "DATA" / "stray_files"

TARGET_EXTS = {".log", ".md", ".txt", ".doc", ".docx", ".pdf"}
NOW = time.time()

# Core system files that should never be moved from root
PROTECTED_ROOT_FILES = {
    "GEMINI.md", "CLAUDE.md", "README.md", "requirements.txt",
    ".gitignore", "err.txt", "dashboard.ps1", ".mcp.json",
    ".claudeignore", ".clauderules"
}

def safely_delete_file(path: Path, dry_run: bool) -> bool:
    try:
        if not dry_run:
            path.unlink(missing_ok=True)
        return True
    except Exception as e:
        print(f"[!] Lá»—i xÃ³a file {path.name}: {e}")
        return False

def safely_move_file(src: Path, dest_dir: Path, dry_run: bool) -> bool:
    try:
        if not dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)
            # Avoid overwriting if same name exists
            dest_path = dest_dir / src.name
            if dest_path.exists():
                dest_path = dest_dir / f"{src.stem}_{int(time.time())}{src.suffix}"
            shutil.move(str(src), str(dest_path))
        return True
    except Exception as e:
        print(f"[!] Lá»—i di chuyá»ƒn file {src.name}: {e}")
        return False

def sweep_root_scatter(dry_run: bool, stale_days: int = 3) -> int:
    """QuÃ©t cÃ¡c file rÃ¡c náº±m ráº£i rÃ¡c ngoÃ i thÆ° má»¥c gá»‘c vÃ  Ä‘áº©y vÃ o khu cÃ¡ch ly stray_files"""
    moved_count = 0
    print(f"\n[+] Äang quÃ©t dá»n file Ä‘i láº¡c (Stray Files) táº¡i Root (CÅ© hÆ¡n {stale_days} ngÃ y)...")
    stale_seconds = stale_days * 24 * 3600

    # Chá»‰ quÃ©t cáº¥p 1 (root directory)
    for child in AOS_ROOT.iterdir():
        if child.is_file():
            # If it's a python script, doc, or log, and NOT a protected core file
            if child.name not in PROTECTED_ROOT_FILES and child.suffix.lower() in {".py", ".md", ".txt", ".json", ".log"}:
                try:
                    mtime = child.stat().st_mtime
                    age = NOW - mtime
                    if age > stale_seconds:
                        if safely_move_file(child, STRAY_DIR, dry_run):
                            print(f"   [>] ÄÃ£ dá»i file Ä‘i láº¡c: {child.name} -> storage/vault/DATA/stray_files/")
                            moved_count += 1
                except Exception:
                    pass

    label = "[DRY-RUN] Sáº½ Dá»n" if dry_run else "[ÄÃƒ Dá»ŒN]"
    print(f"{label}: {moved_count} file rÃ¡c ngoÃ i root.")
    return moved_count

def sweep_stale_artifacts(dry_run: bool, stale_days: int) -> int:
    deleted_count = 0
    reclaimed_bytes = 0
    stale_seconds = stale_days * 24 * 3600

    print(f"\n[+] Äang quÃ©t tá»‡p rÃ¡c (CÅ© hÆ¡n {stale_days} ngÃ y)...")

    # Bá»• sung stray_files vÃ o danh sÃ¡ch dá»n dáº¹p cáº·n bÃ£
    all_targets = TARGET_DIRS + [STRAY_DIR]

    for target in all_targets:
        if not target.exists():
            continue

        for root, dirs, files in os.walk(target):
            curr_dir = Path(root)
            for file in files:
                fpath = curr_dir / file
                # Náº¿u file náº±m trong stray_files, má»i file Ä‘á»u bá»‹ xÃ³a báº¥t cháº¥p Ä‘uÃ´i
                # CÃ²n á»Ÿ cÃ¡c folder khÃ¡c, chá»‰ xÃ³a cÃ¡c file sinh ra nhÆ° .log, .md...
                if target == STRAY_DIR or fpath.suffix.lower() in TARGET_EXTS:
                    try:
                        mtime = fpath.stat().st_mtime
                        age = NOW - mtime
                        if age > stale_seconds:
                            size = fpath.stat().st_size
                            if safely_delete_file(fpath, dry_run):
                                print(f"   [x] XÃ³a rÃ¡c: {fpath.name}")
                                deleted_count += 1
                                reclaimed_bytes += size
                    except Exception:
                        pass

    label = "[DRY-RUN] Sáº½ XÃ³a" if dry_run else "[ÄÃƒ XÃ“A]"
    print(f"{label}: {deleted_count} files | Tiáº¿t kiá»‡m: {reclaimed_bytes/(1024*1024):.2f} MB")
    return reclaimed_bytes

def sweep_empty_repos(dry_run: bool) -> int:
    print("\n[+] Äang quÃ©t Repository má»“ cÃ´i (Empty Clones)...")
    if not REPO_DIR.exists():
        return 0

    found_count = 0
    for child in REPO_DIR.iterdir():
        if child.is_dir():
            is_empty = not any(child.iterdir())
            has_git = (child / ".git").exists()

            if is_empty or not has_git:
                found_count += 1
                # [!] CEO Request: Do not auto-delete yet.
                print(f"   [!] PhÃ¡t hiá»‡n repo lá»—i/trá»‘ng: {child.name} (Chá» CEO xá»­ lÃ½, khÃ´ng auto-delete)")

    print(f"Tá»”NG: {found_count} Repositories rá»—ng phÃ¡t hiá»‡n.")
    return found_count

def purge_obsolete_directories(dry_run: bool) -> int:
    obsolete_targets = [
        AOS_ROOT / ".openclaw",
        AOS_ROOT / ".kiro",
        AOS_ROOT / ".cursorrules"
    ]
    purged_count = 0
    print("\n[+] Äang quÃ©t tiÃªu há»§y cÃ¡c thÆ° má»¥c/file di tÃ­ch (Obsolete Tiers)...")
    for target in obsolete_targets:
        if target.exists():
            try:
                if target.is_dir():
                    if not dry_run:
                        shutil.rmtree(target, ignore_errors=True)
                else:
                    safely_delete_file(target, dry_run)
                print(f"   [!] ÄÃ£ tiÃªu há»§y tá»­ huyá»‡t di tÃ­ch: {target.name}")
                purged_count += 1
            except Exception:
                pass
    return purged_count

def run_deep_cleaner():
    parser = argparse.ArgumentParser(description="AI OS Facility Sanitation Script")
    parser.add_argument("--auto-delete", action="store_true", help="Execute destructive deletion (Default is Dry-Run)")
    parser.add_argument("--stale-days", type=int, default=14, help="Number of days before an artifact is considered stale (Default: 14)")
    args = parser.parse_args()

    dry_run = not args.auto_delete
    print("="*60)
    print(f" AI OS DEEP CLEANER (Khá»Ÿi Ä‘á»™ng bá»Ÿi Dept 22 Facility Agent)")
    print(f" Cháº¿ Ä‘á»™: {'DRY-RUN (QuÃ©t an toÃ n)' if dry_run else 'AUTO-DELETE (Há»§y diá»‡t)'}")
    print("="*60)

    # 1. HÃºt cÃ¡c file Ä‘i láº¡c á»Ÿ root
    sweep_root_scatter(dry_run)

    # 1.5. TiÃªu há»§y di tÃ­ch cá»• Ä‘áº¡i (OpenClaw, Kiro...)
    purge_obsolete_directories(dry_run)

    # 2. XÃ³a cÃ¡c tá»‡p giÃ  cá»—i
    total_reclaimed = sweep_stale_artifacts(dry_run, args.stale_days)

    # 3. QuÃ©t thÃ´ng bÃ¡o repo rá»—ng (chÆ°a xÃ³a)
    sweep_empty_repos(dry_run)

    print("\n" + "="*60)
    print(f" HOÃ€N Táº¤T Dá»ŒN Dáº¸P Há»† THá»NG.")
    if not dry_run:
        print(f" Thu há»“i thÃ nh cÃ´ng bá»™ nhá»›: {total_reclaimed/(1024*1024):.2f} MB")
    print("="*60)

if __name__ == "__main__":
    run_deep_cleaner()

