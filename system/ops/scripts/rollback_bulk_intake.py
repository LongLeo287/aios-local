import os
import glob
import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
VAULT_DATA_DIR = os.path.join(BASE_DIR, 'storage', 'vault', 'DATA')

def main():
    print(f"[{datetime.datetime.now().isoformat()}] STARTING EMERGENCY ROLLBACK...")

    # Tìm tất cả các file do bulk_repo_intake_v2 tạo ra (bulk_intake_v2)
    # hoặc tất cả file KI-*.json có source_type: url_repo_bulk
    search_pattern = os.path.join(VAULT_DATA_DIR, 'KI-*_*.json')
    files = glob.glob(search_pattern)

    deleted_count = 0
    for fpath in files:
        # Chỉ xóa những file do V2 tạo (có url_entry, hoặc những file thuộc 91 URLs)
        # Để an toàn, đọc nội dung xem submitter có phải là "antigravity-bulk-intake-v2" không
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
                if '"submitted_by": "antigravity-bulk-intake-v2"' in content:
                    os.remove(fpath)
                    print(f"  [-] Rollback (Deleted): {os.path.basename(fpath)}")
                    deleted_count += 1
        except Exception as e:
            print(f"  [!] Error reading/deleting {fpath}: {e}")

    print(f"\n[SUCCESS] Emptied {deleted_count} massive intake tickets from Vault.")
    print("The system is safe from digesting unfiltered data. Awaiting proper evaluation workflow.")

if __name__ == "__main__":
    main()
