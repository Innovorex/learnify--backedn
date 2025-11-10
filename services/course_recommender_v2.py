"""
Course Recommender V2 - Real Course Recommendations
====================================================
Replaces AI hallucination with verified course matching
Uses CourseMatcher to find real CPD courses
"""

import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

from typing import List, Dict, Any
from sqlalchemy.orm import Session

from models import User, TeacherProfile
from services.performance_analyzer import PerformanceAnalyzer
from services.course_matcher import CourseMatcher


async def generate_course_recommendations(db: Session, teacher_id: int) -> List[Dict[str, Any]]:
    """
    Generate REAL course recommendations based on teacher performance

    Key Changes from V1:
    - No AI hallucination
    - Uses verified courses from database
    - Direct course URLs (not generic platform links)
    - Matching engine scores courses based on relevance

    Args:
        db: Database session
        teacher_id: Teacher's user ID

    Returns:
        List of course recommendation dictionaries
    """

    print(f"\n{'='*80}")
    print(f"GENERATING REAL COURSE RECOMMENDATIONS (V2)")
    print(f"Teacher ID: {teacher_id}")
    print(f"{'='*80}")

    # Get teacher profile
    teacher = db.query(User).filter(User.id == teacher_id).first()
    if not teacher:
        print("❌ Teacher not found")
        return []

    profile = db.query(TeacherProfile).filter(TeacherProfile.user_id == teacher_id).first()
    if not profile:
        print("❌ Teacher profile not found")
        return []

    print(f"\nTeacher: {teacher.name}")
    print(f"Email: {teacher.email}")
    print(f"Subjects: {profile.subjects_teaching}")
    print(f"Grades: {profile.grades_teaching}")
    print(f"Board: {profile.board}")

    # Use Performance Analyzer to identify weak areas
    analyzer = PerformanceAnalyzer(db, teacher_id)
    priority_areas = analyzer.get_priority_areas(max_areas=3)

    if not priority_areas:
        print("\n⚠️  No performance data available - cannot generate recommendations")
        return []

    print(f"\n📊 Priority Areas Identified: {len(priority_areas)}")
    for module_name, trend_data in priority_areas:
        print(f"   • {module_name}")
        print(f"     Score: {trend_data['current_score']}%")
        print(f"     Trend: {trend_data['trend']}")
        print(f"     Priority: {trend_data['priority']}")
        print(f"     Difficulty: {trend_data['recommended_difficulty']}")

    # Format weak areas for course matcher
    weak_areas_formatted = []
    for module_name, trend_data in priority_areas:
        weak_areas_formatted.append({
            "name": module_name,
            "current_score": trend_data["current_score"],
            "decline_percent": abs(trend_data.get("change_percentage", 0)),
            "trend": trend_data["trend"],
            "priority": trend_data["priority"],
            "recommended_difficulty": trend_data["recommended_difficulty"]
        })

    # Use Course Matcher to find real courses
    print(f"\n🔍 Searching for matching courses...")
    matcher = CourseMatcher(db)

    recommendations = matcher.create_recommendations(
        teacher_id=teacher_id,
        weak_areas=weak_areas_formatted,
        max_per_area=2
    )

    # Format recommendations for API response
    result = matcher.get_teacher_recommendations(teacher_id)

    print(f"\n✅ Successfully generated {len(result)} recommendations")

    return result


async def get_teacher_recommendations(db: Session, teacher_id: int) -> List[Dict[str, Any]]:
    """
    Get existing course recommendations for a teacher

    Args:
        db: Database session
        teacher_id: Teacher's user ID

    Returns:
        List of course recommendation dictionaries
    """

    matcher = CourseMatcher(db)
    recommendations = matcher.get_teacher_recommendations(teacher_id)

    return recommendations
