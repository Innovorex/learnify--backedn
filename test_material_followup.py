"""
Test Material-Based Follow-Up Questions
========================================
Tests the AI Tutor's ability to:
1. Understand complete uploaded material
2. Answer follow-up questions about the material
3. Maintain conversation history
"""

import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

import asyncio
import requests
import json

BASE_URL = "http://localhost:8000"

# Test credentials
TEACHER_EMAIL = "siva@gmail.com"
TEACHER_PASSWORD = "siva@123"


def login():
    """Login as teacher and get token"""
    print("\n🔐 Logging in as teacher...")

    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": TEACHER_EMAIL,
            "password": TEACHER_PASSWORD
        }
    )

    if response.status_code == 200:
        data = response.json()
        token = data['access_token']
        user_id = data['user']['id']
        print(f"✅ Logged in successfully! User ID: {user_id}")
        return token, user_id
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
        return None, None


def test_cbse_topic_with_followup(token):
    """Test CBSE topic (Real Numbers) with follow-up questions"""

    print("\n" + "="*80)
    print("TEST 1: CBSE Topic (Real Numbers) - Full Understanding")
    print("="*80)

    # Start session with Real Numbers topic
    print("\n📚 Starting AI Tutor session with topic: Real Numbers (CBSE Class 10 Maths)...")

    response = requests.post(
        f"{BASE_URL}/api/ai-tutor/start-session",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "topic_name": "Real Numbers",
            "subject": "Mathematics",
            "grade": "10",
            "board": "CBSE",
            "state": "Telangana",
            "use_uploaded_material": False
        }
    )

    if response.status_code != 200:
        print(f"❌ Failed to start session: {response.status_code}")
        print(response.text)
        return

    session_data = response.json()
    session_id = session_data['session_id']
    initial_response = session_data['initial_message']

    print(f"\n✅ Session started! Session ID: {session_id}")
    print(f"\n📝 Initial Response (first 500 chars):")
    print("-" * 80)
    print(initial_response[:500])
    print("-" * 80)

    # Follow-up question 1: Specific concept
    print("\n\n❓ Follow-up Question 1: What is Euclid's Division Lemma?")
    print("-" * 80)

    response1 = requests.post(
        f"{BASE_URL}/api/ai-tutor/chat",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "session_id": session_id,
            "message": "What is Euclid's Division Lemma?",
            "subject": "Mathematics",
            "grade": "10"
        }
    )

    if response1.status_code == 200:
        answer1 = response1.json()['response']
        print(f"✅ Answer 1 (first 400 chars):")
        print(answer1[:400])
    else:
        print(f"❌ Failed: {response1.status_code}")
        print(response1.text)
        return

    # Follow-up question 2: Related concept
    print("\n\n❓ Follow-up Question 2: How is it used to find HCF?")
    print("-" * 80)

    response2 = requests.post(
        f"{BASE_URL}/api/ai-tutor/chat",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "session_id": session_id,
            "message": "How is it used to find HCF?",
            "subject": "Mathematics",
            "grade": "10"
        }
    )

    if response2.status_code == 200:
        answer2 = response2.json()['response']
        print(f"✅ Answer 2 (first 400 chars):")
        print(answer2[:400])
    else:
        print(f"❌ Failed: {response2.status_code}")
        print(response2.text)
        return

    # Follow-up question 3: Different topic in same chapter
    print("\n\n❓ Follow-up Question 3: What about irrational numbers?")
    print("-" * 80)

    response3 = requests.post(
        f"{BASE_URL}/api/ai-tutor/chat",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "session_id": session_id,
            "message": "What about irrational numbers? How are they defined?",
            "subject": "Mathematics",
            "grade": "10"
        }
    )

    if response3.status_code == 200:
        answer3 = response3.json()['response']
        print(f"✅ Answer 3 (first 400 chars):")
        print(answer3[:400])
    else:
        print(f"❌ Failed: {response3.status_code}")
        print(response3.text)

    print("\n" + "="*80)
    print("✅ TEST 1 COMPLETE: CBSE topic with follow-up questions")
    print("="*80)


def test_uploaded_material_with_followup(token):
    """Test uploaded material with follow-up questions"""

    print("\n" + "="*80)
    print("TEST 2: Uploaded Material - Full Understanding")
    print("="*80)

    # Check if any materials are uploaded
    print("\n📄 Checking uploaded materials...")

    response = requests.get(
        f"{BASE_URL}/api/teaching-materials/",
        headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code != 200:
        print(f"❌ Failed to fetch materials: {response.status_code}")
        return

    materials = response.json()

    if not materials:
        print("⚠️ No materials uploaded. Skipping uploaded material test.")
        print("   Upload a material first using the frontend, then run this test again.")
        return

    # Use the first material
    material = materials[0]
    material_id = material['id']
    material_name = material['title']

    print(f"✅ Found material: {material_name} (ID: {material_id})")

    # Start session with uploaded material
    print(f"\n📚 Starting AI Tutor session with uploaded material...")

    response = requests.post(
        f"{BASE_URL}/api/ai-tutor/start-session",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "topic_name": material_name,
            "subject": "Mathematics",  # Adjust as needed
            "grade": "10",
            "board": "CBSE",
            "state": "Telangana",
            "use_uploaded_material": True,
            "material_id": material_id
        }
    )

    if response.status_code != 200:
        print(f"❌ Failed to start session: {response.status_code}")
        print(response.text)
        return

    session_data = response.json()
    session_id = session_data['session_id']
    initial_response = session_data['initial_message']

    print(f"\n✅ Session started! Session ID: {session_id}")
    print(f"\n📝 Initial Response (first 500 chars):")
    print("-" * 80)
    print(initial_response[:500])
    print("-" * 80)

    # Follow-up question 1: General question
    print("\n\n❓ Follow-up Question 1: What are the main topics covered in this material?")
    print("-" * 80)

    response1 = requests.post(
        f"{BASE_URL}/api/ai-tutor/chat",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "session_id": session_id,
            "message": "What are the main topics covered in this material?",
            "subject": "Mathematics",
            "grade": "10"
        }
    )

    if response1.status_code == 200:
        answer1 = response1.json()['response']
        print(f"✅ Answer 1 (first 400 chars):")
        print(answer1[:400])
    else:
        print(f"❌ Failed: {response1.status_code}")
        print(response1.text)
        return

    # Follow-up question 2: Specific detail
    print("\n\n❓ Follow-up Question 2: Can you explain the first concept in detail?")
    print("-" * 80)

    response2 = requests.post(
        f"{BASE_URL}/api/ai-tutor/chat",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "session_id": session_id,
            "message": "Can you explain the first concept mentioned in the material in detail?",
            "subject": "Mathematics",
            "grade": "10"
        }
    )

    if response2.status_code == 200:
        answer2 = response2.json()['response']
        print(f"✅ Answer 2 (first 400 chars):")
        print(answer2[:400])
    else:
        print(f"❌ Failed: {response2.status_code}")
        print(response2.text)

    print("\n" + "="*80)
    print("✅ TEST 2 COMPLETE: Uploaded material with follow-up questions")
    print("="*80)


def main():
    """Run all tests"""

    print("\n" + "="*80)
    print("🧪 TESTING: Material-Based Follow-Up Questions")
    print("="*80)
    print("\nThis test verifies:")
    print("1. AI Tutor loads COMPLETE material content")
    print("2. Can answer ANY follow-up question about the material")
    print("3. Maintains conversation history")
    print("4. References specific content when answering")

    # Login
    token, user_id = login()
    if not token:
        print("\n❌ Test failed: Could not login")
        return

    # Test 1: CBSE topic with follow-up
    test_cbse_topic_with_followup(token)

    # Test 2: Uploaded material with follow-up
    test_uploaded_material_with_followup(token)

    print("\n" + "="*80)
    print("🎉 ALL TESTS COMPLETE")
    print("="*80)
    print("\n✅ If you see answers that reference the material/textbook,")
    print("   the implementation is working correctly!")
    print("\n❌ If you see generic answers or 'I don't have information',")
    print("   there may be an issue with material loading.")


if __name__ == "__main__":
    main()
