import subprocess
import argparse
import sys
import os

def check_gcloud_installed():
    try:
        subprocess.run(["gcloud", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("LỖI: gcloud CLI chưa được cài đặt hoặc không nằm trong PATH.")
        print("Vui lòng cài đặt tại: https://cloud.google.com/sdk/docs/install")
        sys.exit(1)

def deploy_to_cloud_run(service_name, region):
    print(f"=== Đang triển khai (Deploy) mã nguồn hiện tại lên Cloud Run ===")
    print(f"Service: {service_name}")
    print(f"Region : {region}")
    print(f"Source : {os.getcwd()}")
    print("---------------------------------------------------------------")

    # GCP Command for source-based deployment
    cmd = [
        "gcloud", "run", "deploy", service_name,
        "--source", ".",
        "--region", region,
        "--allow-unauthenticated"  # Defaulting to allow public access for ease of use
    ]

    print(f"Executing: {' '.join(cmd)}")

    try:
        # Run process and stream output
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(line, end="")

        process.wait()
        if process.returncode == 0:
            print("\n=== TRIỂN KHAI THÀNH CÔNG! ===")
        else:
            print(f"\n[LỖI] Lệnh deploy thất bại với mã lỗi {process.returncode}")
            sys.exit(process.returncode)

    except Exception as e:
        print(f"\n[EXCEPTION] Có lỗi xảy ra trong Python Script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Triển khai source code local lên Google Cloud Run.")
    parser.add_argument("--service", required=True, help="Tên dịch vụ Cloud Run")
    parser.add_argument("--region", required=True, help="Khu vực GCP (ví dụ: us-central1, asia-southeast1)")

    args = parser.parse_args()

    check_gcloud_installed()
    deploy_to_cloud_run(args.service, args.region)
