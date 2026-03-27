import os
import subprocess
import sys

# MA TRáº¬N Ká»ŠCH Báº¢N KIá»‚M KÃŠ (Ontology Auditor Suite)
# ÄÆ°á»£c cháº¡y bá»Ÿi SRE-Agent hoáº·c Há»‡ thá»‘ng Daemon hÃ ng tuáº§n.

ROOT_DIR = os.environ.get("AOS_ROOT", ".")
SCRIPT_DIR = os.path.join(ROOT_DIR, "system", "ops", "scripts")

scripts_to_run = [
    "deep_scan_unlinked.py",    # Check xem cÃ³ RÃ¡c khÃ´ng
    "tag_workflows.py",         # ÄÃ³ng dáº¥u náº¿u phÃ¡t hiá»‡n workflow má»“ cÃ´i
    "distribute_weapons.py",    # Ráº£i vÅ© khÃ­ má»“ cÃ´i vá» cÃ¡c kho phÃ²ng ban
    "org_mapper.py"             # Render láº¡i nguyÃªn SÆ¡ Ä‘á»“ Nháº­n thá»©c 3D
]

def main():
    print("====================================")
    print("ðŸš€ ONGOLOGY AUDITOR SUITE STARTED")
    print("====================================")

    for script in scripts_to_run:
        script_path = os.path.join(SCRIPT_DIR, script)
        if not os.path.exists(script_path):
            print(f"[ERROR] Missing {script_path}. Skipping.")
            continue

        print(f"\n---> RUNNING: {script}")
        try:
            result = subprocess.run([sys.executable, script_path], cwd=ROOT_DIR, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(f"[STDERR] {result.stderr}")
        except Exception as e:
            print(f"[CRITICAL] Error running {script}: {e}")

    print("\n====================================")
    print("âœ… ONTOLOGY AUDITOR FINISHED. System Integrity Restored & Fully Remapped.")
    print("====================================")

if __name__ == "__main__":
    main()

