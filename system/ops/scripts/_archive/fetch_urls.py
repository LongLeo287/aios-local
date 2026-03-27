import urllib.request
import sys
import re

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            # Extract basic text
            text = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL)
            text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            print(f"--- CONTENT FOR {url} ---\n{text[:2500]}\n")
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")

if __name__ == '__main__':
    for url in sys.argv[1:]:
        fetch(url)
