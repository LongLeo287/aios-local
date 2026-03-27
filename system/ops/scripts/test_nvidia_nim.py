import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# Fallback in case not in .env
NVK = os.getenv("NVIDIA_API_KEY_2", "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")
NVU = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")

client = OpenAI(
  base_url=NVU,
  api_key=NVK
)

models = [
    {"name": "Llama 3.1 405B Instruct", "id": "meta/llama-3.1-405b-instruct", "temp": 0.2, "top_p": 0.7, "prompt": "Solve: What is the meaning of life, universe, and everything in 2 words?"},
    {"name": "Llama 3.3 70B Instruct", "id": "meta/llama-3.3-70b-instruct", "temp": 0.2, "top_p": 0.7, "prompt": "Explain Quantum computing in 1 simple sentence."},
    {"name": "Mixtral 8x22B Instruct", "id": "mistralai/mixtral-8x22b-instruct-v0.1", "temp": 0.7, "top_p": 0.9, "prompt": "Write a haiku about AI OS."},
    {"name": "Gemma 2 27B IT", "id": "google/gemma-2-27b-it", "temp": 0.4, "top_p": 0.8, "prompt": "Translate 'Hello' to French, Spanish, and German."},
    {"name": "Mamba Codestral 7B", "id": "mistralai/mamba-codestral-7b-v0.1", "temp": 0.5, "top_p": 1, "prompt": "def fibonacci(n):"},
    {"name": "Phi 3 Medium 128K", "id": "microsoft/phi-3-medium-128k-instruct", "temp": 0.2, "top_p": 0.7, "prompt": "Solve: if 2x = 10, what is x?"}
]

print("=========================================")
print("🧪 NVIDIA NIM API INTEGRATION TESTER")
print("=========================================")

for m in models:
    print(f"\n[Testing Model] {m['name']} ({m['id']})")
    print(f"Prompt: {m['prompt']}")
    print("-" * 40)

    try:
        completion = client.chat.completions.create(
            model=m['id'],
            messages=[{"role":"user","content":m['prompt']}],
            temperature=m['temp'],
            top_p=m['top_p'],
            max_tokens=150,
            stream=True
        )

        for chunk in completion:
            if hasattr(chunk, 'choices') and chunk.choices and chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="")
        print("\n")
    except Exception as e:
        print(f"\n💥 ERROR testing {m['id']}: {e}\n")
    print("=" * 40)

print("\n✅ All NVIDIA models tested!")
