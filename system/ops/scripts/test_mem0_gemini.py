import os
import sys
import warnings
warnings.filterwarnings("ignore")

from mem0 import Memory

ENV_PATH = r"<AI_OS_ROOT>\system\ops\secrets\MASTER.env"

def load_env():
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line:
                    key, val = line.strip().split('=', 1)
                    os.environ[key] = val

load_env()
# Lấy fallback nếu environment vars ko khớp chuẩn
gemini_key = os.environ.get('GOOGLE_AI_API_KEY', '')
if not gemini_key:
    gemini_key = os.environ.get('GEMINI_API_KEY', '')
gemini_key = gemini_key.strip('"').strip("'")
os.environ['GEMINI_API_KEY'] = gemini_key

config = {
    "llm": {
        "provider": "gemini",
        "config": {
            "model": "gemini-2.5-flash",
            "api_key": gemini_key,
            "temperature": 0.2
        }
    },
    "embedder": {
        "provider": "huggingface",
        "config": {
            "model": "sentence-transformers/all-MiniLM-L6-v2"
        }
    }
}

print("Initializing mem0 Memory...")
try:
    m = Memory.from_config(config_dict=config)
    print("Memory initialized successfully with Gemini.")

    print("Adding a memory...")
    result = m.add("Tôi là Chủ tịch AI OS Corp, rất thích mô hình Agile và Cloud Run.", user_id="CEO")
    print(f"Add result: {result}")

    print("Searching memory for 'Sếp thích gì?'...")
    search_res = m.search("Chủ tịch thích gì?", user_id="CEO")
    print(f"Search Result: {search_res}")

except Exception as e:
    print(f"Failed with {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
