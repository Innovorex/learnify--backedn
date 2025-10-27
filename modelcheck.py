import requests

api_key = "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"
model = "meta-llama/llama-3.3-8b-instruct:free"

print("🔑 Testing API key:", api_key[:15] + "...")
print("🧠 Model:", model)

headers = {
    "Authorization": f"Bearer {api_key}",
    "HTTP-Referer": "https://openrouter.ai/",
    "X-Title": "Key Check Script"
}

data = {
    "model": model,
    "messages": [
        {"role": "system", "content": "Health check"},
        {"role": "user", "content": "Say hi if you’re working."}
    ]
}

response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                         headers=headers, json=data)

print("\n🔢 Status code:", response.status_code)
print("🧾 Response text:", response.text)
