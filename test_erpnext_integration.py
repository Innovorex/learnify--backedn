"""
Test ERPNext Integration End-to-End
"""

import asyncio
from services.erpnext_client import get_erpnext_client
from services.erpnext_sync_service import get_sync_service
from database import SessionLocal

async def test_authentication():
    """Test ERPNext authentication"""
    print("\n" + "="*60)
    print("TEST 1: ERPNext Authentication")
    print("="*60)

    client = get_erpnext_client()

    # Test with Administrator credentials
    print("\n→ Testing authentication with Administrator...")
    result = await client.authenticate_user("Administrator", "Innovorex@1")

    if result["success"]:
        print("✅ Authentication successful!")
        print(f"   User: {result.get('user')}")
        print(f"   Role: {result.get('role')}")
        print(f"   Email: {result.get('email')}")
        print(f"   Token: {result.get('token')[:50]}...")
    else:
        print(f"❌ Authentication failed: {result.get('error')}")

    return result["success"]


async def test_fetch_teacher_data():
    """Test fetching complete teacher data"""
    print("\n" + "="*60)
    print("TEST 2: Fetch Teacher Data")
    print("="*60)

    client = get_erpnext_client()

    # Use test teacher email
    teacher_email = "siva.bhogela@school.edu"
    print(f"\n→ Fetching complete data for {teacher_email}...")

    result = await client.sync_teacher_complete(teacher_email)

    if result["success"]:
        print("✅ Data fetched successfully!")
        print(f"\n📧 User Email: {result['user'].get('name')}")
        print(f"👤 Employee Name: {result['employee'].get('employee_name')}")
        print(f"🎓 Designation: {result['employee'].get('designation')}")
        print(f"🏢 Company: {result['employee'].get('company')}")
        print(f"👨‍🏫 Instructor: {result['instructor'].get('name')}")
        print(f"📚 Board: {result['board']}")
        print(f"📖 Subjects: {', '.join(result['subjects'])}")
        print(f"🏫 Classes: {len(result['classes'])} class(es)")

        for cls in result['classes']:
            print(f"   - {cls.get('name')} ({cls.get('program')})")

    else:
        print(f"❌ Failed to fetch data: {result.get('error')}")

    return result["success"]


async def test_sync_to_database():
    """Test syncing teacher data to local database"""
    print("\n" + "="*60)
    print("TEST 3: Sync to Local Database")
    print("="*60)

    db = SessionLocal()

    try:
        sync_service = get_sync_service(db)
        teacher_email = "siva.bhogela@school.edu"

        print(f"\n→ Syncing {teacher_email} to local database...")

        result = await sync_service.sync_teacher(teacher_email)

        if result["success"]:
            print("✅ Sync successful!")
            print(f"\n👤 User ID: {result['user'].id}")
            print(f"📧 Email: {result['user'].email}")
            print(f"📛 Name: {result['user'].name}")
            print(f"👔 Role: {result['user'].role.value}")
            print(f"🔄 Synced: {result['user'].erpnext_synced}")
            print(f"📚 Board: {result['board']}")
            print(f"🏫 Classes synced: {len(result['classes'])}")

            # Query database to verify
            from models import User
            user = db.query(User).filter(User.email == teacher_email).first()

            if user:
                print(f"\n✅ Verified in database:")
                print(f"   - User exists: {user.name}")
                print(f"   - Last sync: {user.erpnext_last_sync}")

                # Check teacher profile
                from models import TeacherProfile
                profile = db.query(TeacherProfile).filter(TeacherProfile.user_id == user.id).first()

                if profile:
                    print(f"   - Teacher profile exists")
                    print(f"   - Board: {profile.board}")
                    print(f"   - Grades: {profile.grades_teaching}")
                    print(f"   - Subjects: {profile.subjects_teaching}")
                else:
                    print("   ⚠️  Teacher profile NOT found")

        else:
            print(f"❌ Sync failed: {result.get('error')}")

        return result["success"]

    finally:
        db.close()


async def test_connection():
    """Test ERPNext API connection"""
    print("\n" + "="*60)
    print("TEST 0: API Connection Check")
    print("="*60)

    client = get_erpnext_client()

    print("\n→ Testing connection to ERPNext API...")

    result = await client.test_connection()

    if result["success"]:
        print("✅ Connection successful!")
        print(f"   Status: {result.get('message')}")
    else:
        print(f"❌ Connection failed: {result.get('error')}")

    return result["success"]


async def run_all_tests():
    """Run all tests in sequence"""
    print("\n")
    print("🚀 ERPNext Integration Test Suite")
    print("="*60)

    results = {}

    # Test 0: Connection
    results["connection"] = await test_connection()

    if not results["connection"]:
        print("\n❌ Connection failed. Stopping tests.")
        return

    # Test 1: Authentication
    results["authentication"] = await test_authentication()

    # Test 2: Fetch teacher data
    results["fetch_data"] = await test_fetch_teacher_data()

    # Test 3: Sync to database
    results["sync_database"] = await test_sync_to_database()

    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name.replace('_', ' ').title()}")

    all_passed = all(results.values())

    print("\n" + "="*60)
    if all_passed:
        print("🎉 All tests PASSED!")
    else:
        print("⚠️  Some tests FAILED")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
