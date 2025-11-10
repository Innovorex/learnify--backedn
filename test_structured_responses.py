"""
Test Structured AI Tutor Responses
===================================
Tests the new ContentFormatter implementation for structured responses
across different subjects.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def login():
    """Login as teacher"""
    print("\n🔐 Logging in...")
    resp = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "siva@gmail.com", "password": "siva@123"}
    )
    token = resp.json()['access_token']
    print(f"✅ Logged in")
    return token


def test_mathematics_structured(token):
    """Test Mathematics topic with structured formatting"""
    print("\n" + "="*80)
    print("TEST 1: Mathematics - Real Numbers (CBSE Class 10)")
    print("="*80)

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
        timeout=120
    )

    if resp.status_code != 200:
        print(f"❌ Failed: {resp.status_code} - {resp.text}")
        return None

    data = resp.json()
    response = data['initial_message']

    print(f"\n✅ Session {data['session_id']} created")
    print(f"\n📝 Response ({len(response)} chars):")
    print("="*80)
    print(response)
    print("="*80)

    # Check for structured elements
    checks = {
        "Has 'Introduction' section": "Introduction" in response or "introduction" in response,
        "Has bullet points (•)": "•" in response,
        "Has 'Teaching Tips'": "Teaching Tips" in response or "teaching tips" in response.lower(),
        "Has formulas": "=" in response and ("HCF" in response or "LCM" in response or "bq" in response),
        "Has examples": "Example" in response or "example" in response,
        "Mentions CBSE/NCERT": "textbook" in response.lower() or "ncert" in response.lower()
    }

    print("\n✅ Quality Checks:")
    for check, result in checks.items():
        status = "✓" if result else "✗"
        print(f"  {status} {check}")

    return data['session_id']


def test_science_structured(token):
    """Test Science topic with structured formatting"""
    print("\n" + "="*80)
    print("TEST 2: Science - Chemical Reactions (CBSE Class 10)")
    print("="*80)

    resp = requests.post(
        f"{BASE_URL}/api/ai-tutor/start-session",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "topic_name": "Chemical Reactions and Equations",
            "subject": "Science",
            "grade": "10",
            "board": "CBSE",
            "state": "Telangana",
            "use_uploaded_material": False
        },
        timeout=120
    )

    if resp.status_code != 200:
        print(f"❌ Failed: {resp.status_code} - {resp.text}")
        return None

    data = resp.json()
    response = data['initial_message']

    print(f"\n✅ Session {data['session_id']} created")
    print(f"\n📝 Response ({len(response)} chars):")
    print("="*80)
    print(response[:1500])  # First 1500 chars
    print("\n... [truncated] ...\n")
    print("="*80)

    # Check for structured elements
    checks = {
        "Has 'Introduction' section": "Introduction" in response,
        "Has bullet points (•)": "•" in response,
        "Has 'Teaching Tips'": "Teaching Tips" in response,
        "Has chemical equations": "→" in response or "->" in response,
        "Has 'Activity' or 'Experiment'": "Activity" in response or "Experiment" in response,
        "Has 'Observation'": "Observation" in response or "observation" in response
    }

    print("\n✅ Quality Checks:")
    for check, result in checks.items():
        status = "✓" if result else "✗"
        print(f"  {status} {check}")

    return data['session_id']


def test_followup_performance(token, session_id):
    """Test follow-up question performance (should be fast!)"""
    print("\n" + "="*80)
    print("TEST 3: Follow-up Question Performance")
    print("="*80)

    import time

    print(f"\n❓ Follow-up: 'What is Euclid's Division Lemma?'")

    start_time = time.time()

    resp = requests.post(
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

    end_time = time.time()
    duration = end_time - start_time

    if resp.status_code != 200:
        print(f"❌ Failed: {resp.status_code} - {resp.text}")
        return

    answer = resp.json()['response']

    print(f"\n⏱️  Response time: {duration:.2f} seconds")
    print(f"\n💬 Answer ({len(answer)} chars):")
    print("="*80)
    print(answer[:800])
    print("="*80)

    if duration < 20:
        print(f"\n✅ EXCELLENT: Response time under 20 seconds!")
    elif duration < 40:
        print(f"\n✓ GOOD: Response time acceptable")
    else:
        print(f"\n⚠️  SLOW: Response took too long")

    # Check answer quality
    has_formula = "a = bq + r" in answer or "dividend" in answer.lower() or "divisor" in answer.lower()
    print(f"\n{'✓' if has_formula else '✗'} Answer contains specific formula/terminology")


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("🧪 TESTING: Structured AI Tutor Responses")
    print("="*80)

    token = login()

    # Test 1: Mathematics
    math_session = test_mathematics_structured(token)

    # Test 2: Science
    science_session = test_science_structured(token)

    # Test 3: Follow-up performance
    if math_session:
        test_followup_performance(token, math_session)

    print("\n" + "="*80)
    print("🎉 TESTS COMPLETE")
    print("="*80)
    print("\nExpected outcomes:")
    print("✓ Responses should be structured with Introduction, sections, Teaching Tips")
    print("✓ Should use bullet points (•) for clarity")
    print("✓ Math should have formulas and examples")
    print("✓ Science should have reactions, activities, observations")
    print("✓ Follow-up questions should respond in <20 seconds")


if __name__ == "__main__":
    main()
