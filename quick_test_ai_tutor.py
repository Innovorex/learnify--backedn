"""Quick AI Tutor Test - Check CBSE content and follow-up"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Login
print("🔐 Logging in...")
resp = requests.post(f"{BASE_URL}/auth/login", json={"email":"siva@gmail.com","password":"siva@123"})
token = resp.json()['access_token']
print(f"✅ Token obtained\n")

# Start session with CBSE topic
print("📚 Starting AI Tutor with 'Real Numbers' (CBSE Class 10)...")
resp = requests.post(
    f"{BASE_URL}/api/ai-tutor/start-session",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "topic_name": "Real Numbers",
        "subject": "Mathematics",
        "grade": "10",
        "board": "CBSE",
        "state": "Telangana",
        "use_uploaded_material": False
    },
    timeout=60
)

if resp.status_code != 200:
    print(f"❌ Error: {resp.status_code} - {resp.text}")
    exit(1)

data = resp.json()
session_id = data['session_id']
print(f"\n✅ Session {session_id} created!")
print(f"\n📝 Initial Response ({len(data['initial_message'])} chars):")
print("="*80)
print(data['initial_message'][:600])
print("="*80)

# Check if CBSE content was used
if "textbook" in data['initial_message'].lower() or "ncert" in data['initial_message'].lower():
    print("\n✅ GOOD: Response mentions textbook/NCERT content")
else:
    print("\n⚠️  WARNING: Response doesn't explicitly mention textbook content")

# Follow-up question 1
print("\n\n❓ Follow-up Question: 'What is Euclid's Division Lemma?'")
resp2 = requests.post(
    f"{BASE_URL}/api/ai-tutor/chat",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "session_id": session_id,
        "message": "What is Euclid's Division Lemma?",
        "subject": "Mathematics",
        "grade": "10"
    },
    timeout=60
)

if resp2.status_code != 200:
    print(f"❌ Error: {resp2.status_code} - {resp2.text}")
else:
    answer = resp2.json()['response']
    print(f"\n💬 Answer ({len(answer)} chars):")
    print("="*80)
    print(answer[:800])
    print("="*80)

    # Check quality
    if "a = bq + r" in answer or "dividend" in answer.lower():
        print("\n✅ EXCELLENT: Answer contains specific formula/terminology from CBSE textbook")
    else:
        print("\n⚠️  Answer may be generic")

# Follow-up question 2
print("\n\n❓ Follow-up Question 2: 'How is it used to find HCF?'")
resp3 = requests.post(
    f"{BASE_URL}/api/ai-tutor/chat",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "session_id": session_id,
        "message": "How is it used to find HCF?",
        "subject": "Mathematics",
        "grade": "10"
    },
    timeout=60
)

if resp3.status_code != 200:
    print(f"❌ Error: {resp3.status_code} - {resp3.text}")
else:
    answer = resp3.json()['response']
    print(f"\n💬 Answer ({len(answer)} chars):")
    print("="*80)
    print(answer[:800])
    print("="*80)

print("\n" + "="*80)
print("🎉 TEST COMPLETE")
print("="*80)
