import os
import shutil
from datetime import datetime

LOCAL_INCOMING = r"<AI_OS_ROOT>\system\security\QUARANTINE\incoming\repos"
LOCAL_VETTED   = r"<AI_OS_ROOT>\system\security\QUARANTINE\vetted\repos"
REMOTE_INCOMING = r"<AI_OS_REMOTE_ROOT>\incoming_repos"
GITHUB_QUEUE   = r"<AI_OS_ROOT>\storage\vault\DATA\Github.txt"

# Keywords to detect Remote/UI stuff
REMOTE_KEYWORDS = [
    'ui', 'dashboard', 'web', 'frontend', 'app', 'next.js', 'react', 'tailwind',
    'css', 'html', 'viewer', 'visual', 'chart', 'plotly', 'excalidraw', 'animation',
    'cms', 'posthog', 'kanban', 'hub'
]

def classify_and_move():
    if not os.path.exists(LOCAL_INCOMING):
        print("No incoming repos found.")
        return

    folders = [f for f in os.listdir(LOCAL_INCOMING) if os.path.isdir(os.path.join(LOCAL_INCOMING, f))]

    remote_moved = []
    local_vetted = []

    for folder in folders:
        folder_lower = folder.lower()
        is_remote = any(k in folder_lower for k in REMOTE_KEYWORDS)

        src = os.path.join(LOCAL_INCOMING, folder)
        if is_remote:
            dst = os.path.join(REMOTE_INCOMING, folder)
            category = "REMOTE_ECOSYSTEM"
            remote_moved.append(folder)
        else:
            dst = os.path.join(LOCAL_VETTED, folder)
            category = "LOCAL_CORE"
            local_vetted.append(folder)

        # Move
        try:
            shutil.move(src, dst)
            print(f"Moved: {folder} -> {category}")
        except Exception as e:
            print(f"Error moving {folder}: {e}")

    # Generate Report
    report_path = r"<AI_OS_ROOT>\storage\vault\DATA\bulk_intake_report_v3.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 📊 C-SUITE DASHBOARD: BULK REPO INTAKE\n")
        f.write("> **System:** AI OS v3.3 Governance (Air-Gapped)\n")
        f.write(f"> **Date Executed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("```ascii\n")
        f.write("    [LOCAL CORE] <<-- AIR-GAP -->> [REMOTE ECOSYSTEM]\n")
        f.write("```\n\n")

        f.write("## 1. 🌍 REMOTE ECOSYSTEM (UI/Web/Dashboard)\n")
        f.write(f"Total: {len(remote_moved)} repos moved to AI OS REMOTE.\n")
        for r in sorted(remote_moved):
            f.write(f"- {r}\n")

        f.write("\n## 2. 🧠 LOCAL CORE (Agent/Backend/RAG)\n")
        f.write(f"Total: {len(local_vetted)} repos vetted and kept in AI OS Local.\n")
        for r in sorted(local_vetted):
            f.write(f"- {r}\n")

    print(f"\n[DONE] Processed {len(folders)} repos. Report saved to {report_path}")

    # Clear Github Queue
    if os.path.exists(GITHUB_QUEUE):
        open(GITHUB_QUEUE, 'w').close()
        print("[DONE] Github.txt queue cleared.")

if __name__ == "__main__":
    if not os.path.exists(REMOTE_INCOMING):
        os.makedirs(REMOTE_INCOMING)
    if not os.path.exists(LOCAL_VETTED):
        os.makedirs(LOCAL_VETTED)

    classify_and_move()
