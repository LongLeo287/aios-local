import os
from pathlib import Path

TARGET = Path("<AI_OS_ROOT>/brain/knowledge/repos")

def get_size(path):
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except Exception:
                pass
    return total

if __name__ == "__main__":
    if not TARGET.exists():
        print("Trống")
        exit(0)

    sizes = []
    # Các thư mục con của brain/knowledge/repos thường là tên tổ chức (vd: 01mf02)
    for org in TARGET.iterdir():
        if org.is_dir():
            for repo in org.iterdir():
                if repo.is_dir():
                    sizes.append((repo, get_size(repo)))
                else:
                    sizes.append((repo, get_size(repo)))
        else:
            sizes.append((org, get_size(org)))

    sizes.sort(key=lambda x: x[1], reverse=True)

    print("Top 15 Cục Bloat Nặng Nhất trong brain/knowledge/repos:")
    for path, size in sizes[:15]:
        print(f"{path.relative_to(TARGET)}: {size / (1024*1024):.2f} MB")

    total_gb = sum(s for _, s in sizes) / (1024**3)
    print(f"\nTổng dung lượng: {total_gb:.2f} GB")
    print(f"Tổng số project thô: {len(sizes)}")
