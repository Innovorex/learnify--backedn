"""
Comprehensive Endpoint Testing
Tests ALL growth plan endpoints with detailed status reporting
"""
import requests
import json
from database import SessionLocal
from models import User, GrowthPlan, GrowthPlanAction
from security import create_access_token

BASE_URL = "http://localhost:8000"

def get_teacher_token():
    """Get JWT token for existing teacher"""
    db = SessionLocal()
    try:
        teacher = db.query(User).filter_by(role="teacher").first()
        if not teacher:
            print("❌ No teacher found in database")
            return None, None

        token = create_access_token({
            "user_id": teacher.id,
            "email": teacher.email,
            "name": teacher.name,
            "role": teacher.role.value
        })
        print(f"✅ Got token for teacher: {teacher.name} ({teacher.email}, ID: {teacher.id})")
        return token, teacher.id
    finally:
        db.close()

def check_growth_plan_exists(teacher_id):
    """Check if teacher has any growth plans"""
    db = SessionLocal()
    try:
        plan_count = db.query(GrowthPlan).filter_by(teacher_id=teacher_id).count()
        active_plan = db.query(GrowthPlan).filter_by(teacher_id=teacher_id, is_active=True).first()

        print(f"\n📊 Growth Plan Status for Teacher ID {teacher_id}:")
        print(f"   Total plans: {plan_count}")
        print(f"   Active plan: {'Yes' if active_plan else 'No'}")

        if active_plan:
            actions = db.query(GrowthPlanAction).filter_by(growth_plan_id=active_plan.id).count()
            print(f"   Actions in active plan: {actions}")
            return True, active_plan.id

        return False, None
    finally:
        db.close()

def test_endpoint(method, endpoint, token, data=None, description="", expect_404=False):
    """Test an API endpoint with detailed reporting"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=10)

        status = response.status_code

        # Determine success
        if expect_404 and status == 404:
            result = "✅ WORKING (Expected 404)"
        elif status == 200:
            result = "✅ WORKING"
        elif status == 404:
            result = "⚠️  404 Not Found (No data)"
        elif status == 500:
            result = "❌ FAILED (500 Error)"
        else:
            result = f"⚠️  Status {status}"

        print(f"\n{'='*70}")
        print(f"🔍 {description}")
        print(f"{'='*70}")
        print(f"Endpoint: {method} {endpoint}")
        print(f"Status:   {status}")
        print(f"Result:   {result}")

        if status == 200:
            try:
                result_data = response.json()
                # Show first 300 chars of response
                response_str = json.dumps(result_data, indent=2)
                print(f"Response Preview:\n{response_str[:300]}...")
                return True, result_data
            except:
                print(f"Response: {response.text[:300]}")
                return True, response.text
        else:
            print(f"Error: {response.text[:200]}")
            return False, None

    except requests.exceptions.Timeout:
        print(f"\n❌ TIMEOUT: Endpoint took too long to respond")
        return False, None
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False, None

def main():
    print("="*70)
    print("🚀 COMPREHENSIVE GROWTH PLAN ENDPOINT TEST")
    print("="*70)

    # Get authentication
    token, teacher_id = get_teacher_token()
    if not token:
        print("\n❌ Cannot proceed without authentication")
        return

    # Check if growth plans exist
    has_plan, plan_id = check_growth_plan_exists(teacher_id)

    print("\n" + "="*70)
    print("STARTING ENDPOINT TESTS")
    print("="*70)

    results = []

    # Test 1: Get Insights (Should always work)
    print("\n\n📋 TEST 1/9: Get Peer Insights")
    success, data = test_endpoint(
        "GET",
        "/api/growth-plan/insights?limit=3",
        token,
        description="Get 3 peer learning insights"
    )
    results.append(("Get Insights", success))

    # Test 2: Check Regeneration Trigger
    print("\n\n📋 TEST 2/9: Check Regeneration Trigger")
    success, data = test_endpoint(
        "GET",
        "/api/growth-plan/should-regenerate",
        token,
        description="Check if plan needs regeneration",
        expect_404=not has_plan
    )
    results.append(("Check Regeneration", success))

    # Test 3: Get Current Plan
    print("\n\n📋 TEST 3/9: Get Current Growth Plan")
    success, data = test_endpoint(
        "GET",
        "/api/growth-plan/current",
        token,
        description="Get active growth plan",
        expect_404=not has_plan
    )
    results.append(("Get Current Plan", success))

    # Test 4: Get Actions
    print("\n\n📋 TEST 4/9: Get Actions")
    success, data = test_endpoint(
        "GET",
        "/api/growth-plan/actions",
        token,
        description="Get all growth plan actions"
    )
    results.append(("Get Actions", success))

    # Test 5: Get Progress
    print("\n\n📋 TEST 5/9: Get Progress Summary")
    success, data = test_endpoint(
        "GET",
        "/api/growth-plan/progress",
        token,
        description="Get progress statistics"
    )
    results.append(("Get Progress", success))

    # Test 6: Mark Insight Helpful
    print("\n\n📋 TEST 6/9: Mark Insight as Helpful")
    success, data = test_endpoint(
        "POST",
        "/api/growth-plan/insights/1/helpful",
        token,
        description="Upvote an insight"
    )
    results.append(("Mark Helpful", success))

    # Test 7: Start Action (only if plan exists)
    if has_plan:
        print("\n\n📋 TEST 7/9: Start Action")
        # Get first action ID
        db = SessionLocal()
        action = db.query(GrowthPlanAction).filter_by(growth_plan_id=plan_id).first()
        db.close()

        if action:
            success, data = test_endpoint(
                "POST",
                f"/api/growth-plan/actions/{action.id}/start",
                token,
                description="Mark action as in-progress"
            )
            results.append(("Start Action", success))
        else:
            print("\n\n📋 TEST 7/9: Start Action")
            print("⏭️  SKIPPED - No actions found")
            results.append(("Start Action", None))
    else:
        print("\n\n📋 TEST 7/9: Start Action")
        print("⏭️  SKIPPED - No growth plan exists")
        results.append(("Start Action", None))

    # Test 8: Complete Action (only if plan exists)
    if has_plan:
        print("\n\n📋 TEST 8/9: Complete Action")
        db = SessionLocal()
        action = db.query(GrowthPlanAction).filter_by(growth_plan_id=plan_id).first()
        db.close()

        if action:
            success, data = test_endpoint(
                "POST",
                f"/api/growth-plan/actions/{action.id}/complete",
                token,
                data={"notes": "Test completion", "evidence_urls": []},
                description="Mark action as completed"
            )
            results.append(("Complete Action", success))
        else:
            print("\n\n📋 TEST 8/9: Complete Action")
            print("⏭️  SKIPPED - No actions found")
            results.append(("Complete Action", None))
    else:
        print("\n\n📋 TEST 8/9: Complete Action")
        print("⏭️  SKIPPED - No growth plan exists")
        results.append(("Complete Action", None))

    # Test 9: Generate Plan (SKIPPED to save API credits)
    print("\n\n📋 TEST 9/9: Generate Growth Plan")
    print("⏭️  SKIPPED - Requires API credits")
    print("To test, uncomment the code below:")
    print("# success, data = test_endpoint(")
    print("#     'POST', '/api/growth-plan/generate',")
    print("#     token, data={'focus_areas': []},")
    print("#     description='Generate AI-powered plan'")
    print("# )")
    results.append(("Generate Plan", None))

    # Summary Report
    print("\n\n" + "="*70)
    print("📊 FINAL TEST RESULTS SUMMARY")
    print("="*70)

    working = sum(1 for _, status in results if status == True)
    failed = sum(1 for _, status in results if status == False)
    skipped = sum(1 for _, status in results if status is None)
    total = len(results)

    print(f"\n✅ Working:  {working}/{total}")
    print(f"❌ Failed:   {failed}/{total}")
    print(f"⏭️  Skipped:  {skipped}/{total}")

    print(f"\n{'Endpoint':<25} {'Status':<15}")
    print("-" * 40)
    for name, status in results:
        if status == True:
            status_str = "✅ Working"
        elif status == False:
            status_str = "❌ Failed"
        else:
            status_str = "⏭️  Skipped"
        print(f"{name:<25} {status_str:<15}")

    print("\n" + "="*70)

    if failed == 0:
        print("🎉 ALL TESTABLE ENDPOINTS ARE WORKING!")
    else:
        print(f"⚠️  {failed} endpoint(s) need attention")

    print("="*70)

    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    if not has_plan:
        print("   • No growth plan exists for this teacher")
        print("   • Generate a plan to test action tracking endpoints")
        print("   • Use: POST /api/growth-plan/generate")

    if working >= 5:
        print("   • Core functionality is working")
        print("   • Ready for frontend integration")

    print("\n")

if __name__ == "__main__":
    main()
