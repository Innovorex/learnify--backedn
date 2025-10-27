import os
import httpx
from dotenv import load_dotenv

# ✅ Load environment file
load_dotenv(dotenv_path="/home/hub_ai/teacher/backend/.env")

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("❌ Missing OPENROUTER_API_KEY. Add it to your .env file or export it.")

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

data = {
    "model": "google/gemma-7b-it:free",
    "messages": [{"role": "user", "content": "Hello! Please confirm this model is working."}],
}

try:
    print("🔄 Sending request to OpenRouter...")
    r = httpx.post(url, headers=headers, json=data, timeout=60)
    print(f"✅ Status Code: {r.status_code}")
    print("🧾 Response Text:", r.text[:500])
except Exception as e:
    print("❌ Error:", e)
