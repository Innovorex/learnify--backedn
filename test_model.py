import os
import httpx
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
model = os.getenv("OPENROUTER_MODEL")

print(f"Testing model: {model}")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

data = {
    "model": model,
    "messages": [{"role": "user", "content": "Generate a simple math question for grade 5."}],
    "temperature": 0.3,
}

try:
    with httpx.Client(timeout=60) as client:
        r = client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text[:500]}")
except Exception as e:
    print(f"Error: {e}")
