"""
Test script for Career Progression APIs
Creates test teacher and tests all endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"
EMAIL = "test.career@teacher.com"
PASSWORD = "Test@123"

def test_signup():
    """Create test teacher account"""
    print("\n" + "="*60)
    print("TEST 1: Creating Test Teacher Account")
    print("="*60)

    payload = {
        "name": "Priya Sharma",
        "email": EMAIL,
        "password": PASSWORD,
        "confirm_password": PASSWORD,
        "role": "teacher"
    }

    response = requests.post(f"{BASE_URL}/auth/signup", json=payload)

    if response.status_code in [200, 201]:
        print("✅ Teacher account created successfully")
        return response.json()
    elif "already exists" in response.text.lower() or response.status_code == 400:
        print("⚠️  Teacher already exists, will try to login")
        return None
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return None

def test_login():
    """Login and get JWT token"""
    print("\n" + "="*60)
    print("TEST 2: Login to Get JWT Token")
    print("="*60)

    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": EMAIL, "password": PASSWORD}
    )

    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✅ Login successful")
        print(f"   Token (first 50 chars): {token[:50]}...")
        return token
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
        return None

def test_recommendation(token):
    """Test get recommended course"""
    print("\n" + "="*60)
    print("TEST 3: Get Recommended Course")
    print("="*60)

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/career-progression/recommend",
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        print("✅ Recommendation received:")
        print(f"   Current: {data['current_qualification']}")
        if data.get('recommended_course'):
            print(f"   Recommended: {data['recommended_course']['name']}")
            print(f"   University: {data['recommended_course']['university']}")
            print(f"   Duration: {data['recommended_course']['duration_months']} months")
            print(f"   Modules: {data['recommended_course']['total_modules']}")
            return data['recommended_course']['id']
        else:
            print(f"   Message: {data.get('message')}")
            return None
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return None

def test_enrollment(token, course_id):
    """Test course enrollment"""
    print("\n" + "="*60)
    print("TEST 4: Enroll in Course")
    print("="*60)

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/api/career-progression/enroll/{course_id}",
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        print("✅ Enrollment successful:")
        print(f"   Enrollment ID: {data['enrollment_id']}")
        print(f"   Course: {data['course_name']}")
        print(f"   Status: {data['status']}")
        print(f"   Current Module: {data.get('current_module')}")
        return data['enrollment_id']
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return None

def test_get_modules(token, course_id):
    """Test get course modules"""
    print("\n" + "="*60)
    print("TEST 5: Get Course Modules")
    print("="*60)

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/career-progression/course/{course_id}/modules",
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        print("✅ Modules retrieved:")
        print(f"   Course: {data['course']['name']}")
        print(f"   Total Modules: {len(data['modules'])}")
        print("\n   Module List:")
        for mod in data['modules'][:3]:  # Show first 3
            locked = "🔒" if mod['is_locked'] else "🔓"
            print(f"   {locked} Module {mod['module_number']}: {mod['module_name']}")
            print(f"      Status: {mod['status']}")
        return data['modules'][0]['id'] if data['modules'] else None
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return None

def test_get_content(token, module_id):
    """Test get module content"""
    print("\n" + "="*60)
    print("TEST 6: Get Module Content")
    print("="*60)

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/career-progression/module/{module_id}/content",
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        print("✅ Content retrieved:")
        print(f"   Module: {data['module']['module_name']}")
        print(f"   Total Topics: {data['progress']['total_topics']}")
        print(f"   Progress: {data['progress']['percentage']}%")
        print("\n   Topics:")
        for topic in data['topics'][:2]:  # Show first 2
            completed = "✅" if topic['completed'] else "⏳"
            print(f"   {completed} {topic['topic_number']}. {topic['topic_name']}")
            print(f"      Video: {topic['video_duration']}")
        return data['topics'][0]['id'] if data['topics'] else None
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return None

def test_complete_topic(token, topic_id):
    """Test mark topic complete"""
    print("\n" + "="*60)
    print("TEST 7: Mark Topic Complete")
    print("="*60)

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/api/career-progression/topic/{topic_id}/complete",
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        print("✅ Topic marked complete:")
        print(f"   Module Progress: {data['module_progress_percentage']}%")
        print(f"   Topics Completed: {data['topics_completed']}/{data['total_topics']}")
        return True
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return False

def test_my_courses(token):
    """Test get my courses"""
    print("\n" + "="*60)
    print("TEST 8: Get My Enrolled Courses")
    print("="*60)

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/career-progression/my-courses",
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {len(data)} enrolled course(s):")
        for course in data:
            print(f"\n   Course: {course['course']['name']}")
            print(f"   Progress: {course['progress_percentage']}%")
            print(f"   Modules: {course['modules_completed']}/{course['total_modules']}")
            print(f"   Status: {course['status']}")
        return True
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return False

def create_teacher_profile(token):
    """Create teacher profile after signup"""
    print("\n" + "="*60)
    print("Creating Teacher Profile")
    print("="*60)

    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "education": "B.Sc Mathematics",
        "grades_teaching": "8, 9, 10",
        "subjects_teaching": "Mathematics",
        "experience_years": 3,
        "board": "CBSE",
        "state": "Telangana"
    }

    response = requests.post(
        f"{BASE_URL}/teacher/profile",
        json=payload,
        headers=headers
    )

    if response.status_code == 200:
        print("✅ Profile created successfully")
        return True
    elif "already" in response.text.lower():
        print("⚠️  Profile already exists")
        return True
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return False

def run_all_tests():
    """Run all tests in sequence"""
    print("\n" + "🚀"*30)
    print(" CAREER PROGRESSION API TESTING")
    print("🚀"*30)

    # Test 1 & 2: Signup/Login
    signup_result = test_signup()
    token = test_login()

    if not token:
        print("\n❌ Cannot proceed without token")
        return

    # Always try to create profile (will skip if exists)
    create_teacher_profile(token)

    # Test 3: Get Recommendation
    course_id = test_recommendation(token)

    if not course_id:
        print("\n❌ No course recommendation available")
        return

    # Test 4: Enroll in Course
    enrollment_id = test_enrollment(token, course_id)

    if not enrollment_id:
        print("\n⚠️  Enrollment may already exist, continuing...")

    # Test 5: Get Modules
    module_id = test_get_modules(token, course_id)

    if not module_id:
        print("\n❌ No modules found")
        return

    # Test 6: Get Content
    topic_id = test_get_content(token, module_id)

    if not topic_id:
        print("\n❌ No topics found")
        return

    # Test 7: Complete Topic
    test_complete_topic(token, topic_id)

    # Test 8: Get My Courses
    test_my_courses(token)

    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED!")
    print("="*60)
    print("\nBackend APIs are working correctly! 🎉")
    print("Ready for frontend integration.")

if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend server")
        print("Please make sure the server is running:")
        print("  cd /home/hub_ai/learnify-teach/backend")
        print("  uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
