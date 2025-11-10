"""
Smart Course Recommender (No Database Scraping!)
=================================================
Generates real course links directly from platforms
Uses SmartCourseLinkGenerator to create intelligent deep links

KEY FEATURES:
- Performance-driven: Different performance → Different courses
- Real links: Direct to actual platform search results
- Zero maintenance: No course database to manage
- Always current: Uses platform's live catalog
"""

import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

import re
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from models import User, TeacherProfile
from services.performance_analyzer import PerformanceAnalyzer
from services.smart_course_link_generator import SmartCourseLinkGenerator


async def generate_course_recommendations(db: Session, teacher_id: int) -> List[Dict[str, Any]]:
    """
    Generate REAL course recommendations with direct platform links

    Flow:
    1. Analyze teacher performance → Identify weak areas
    2. For each weak area → Generate smart platform search links
    3. Return courses with real URLs that work

    Args:
        db: Database session
        teacher_id: Teacher's user ID

    Returns:
        List of course recommendation dictionaries
    """

    print(f"\n{'='*80}")
    print(f"🔗 SMART COURSE RECOMMENDATION SYSTEM")
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

    print(f"\n👤 Teacher: {teacher.name}")
    print(f"📧 Email: {teacher.email}")
    print(f"📚 Subjects: {profile.subjects_teaching}")
    print(f"🎓 Grades: {profile.grades_teaching}")
    print(f"📋 Board: {profile.board}")
    print(f"📍 State: {profile.state}")

    # Use Performance Analyzer to identify weak areas
    analyzer = PerformanceAnalyzer(db, teacher_id)
    priority_areas = analyzer.get_priority_areas(max_areas=3)

    if not priority_areas:
        print("\n⚠️  No performance data available - generating general recommendations")
        return _generate_general_recommendations(profile)

    print(f"\n📊 Priority Areas Identified: {len(priority_areas)}")
    for module_name, trend_data in priority_areas:
        print(f"   • {module_name}")
        print(f"     Current Score: {trend_data['current_score']}%")
        print(f"     Trend: {trend_data['trend']}")
        print(f"     Change: {trend_data.get('change_percentage', 0):+.1f}%")
        print(f"     Priority: {trend_data['priority']}")
        print(f"     Recommended Difficulty: {trend_data['recommended_difficulty']}")

    # Extract teacher details
    primary_subject = profile.subjects_teaching.split(',')[0].strip() if profile.subjects_teaching else 'General'
    primary_grade = profile.grades_teaching.split(',')[0].strip() if profile.grades_teaching else '6-10'

    # Extract numeric grade from "Grade 9" → "9"
    grade_match = re.search(r'\d+', primary_grade)
    grade_num = grade_match.group() if grade_match else '9'

    board = profile.board or 'CBSE'
    state = profile.state or 'Telangana'

    # Initialize smart link generator
    link_generator = SmartCourseLinkGenerator()

    # Generate smart links for each weak area
    all_recommendations = []

    for module_name, trend_data in priority_areas[:3]:  # Top 3 priorities
        difficulty = trend_data.get('recommended_difficulty', 'intermediate')

        print(f"\n🔍 Generating smart links for: {module_name}")

        # Generate course links for this weak area
        course_links = link_generator.generate_course_links(
            weak_area=module_name,
            subject=primary_subject,
            grade=grade_num,
            board=board,
            state=state,
            difficulty=difficulty
        )

        # Enhance each course with performance context
        for course in course_links:
            # Build performance-specific reasoning
            decline_pct = abs(trend_data.get('change_percentage', 0))
            current_score = trend_data['current_score']
            trend = trend_data['trend']

            # Performance message
            if trend == 'declined':
                performance_msg = f"⚠️ Your {module_name} score declined by {decline_pct:.0f}% in recent assessments. "
            elif trend == 'stagnant':
                performance_msg = f"📊 Your {module_name} performance has been stagnant at {current_score:.0f}%. "
            else:
                performance_msg = f"📈 While improving, your {module_name} score of {current_score:.0f}% needs strengthening. "

            # Action message based on current score
            if current_score < 40:
                action_msg = "This course will help you build foundational knowledge in this area."
            elif current_score < 60:
                action_msg = "This course addresses key concepts to strengthen your understanding."
            elif current_score < 75:
                action_msg = "This course will help you achieve mastery in this topic."
            else:
                action_msg = "This course will help you maintain and enhance your expertise."

            # Combine with original reasoning
            course['recommendation']['reasoning'] = (
                performance_msg + action_msg + " " +
                course['recommendation']['reasoning']
            )

            # Update priority based on performance
            course['recommendation']['priority'] = trend_data['priority']

            # Add improvement areas
            course['recommendation']['improvement_areas'] = [module_name]

            all_recommendations.append(course)

    # Deduplicate by platform (keep highest scoring per platform)
    print(f"\n🔄 Deduplicating recommendations...")
    unique_recommendations = _deduplicate_by_platform(all_recommendations)

    print(f"\n{'='*80}")
    print(f"✅ Generated {len(unique_recommendations)} unique course recommendations")
    print(f"{'='*80}")

    for i, rec in enumerate(unique_recommendations[:4], 1):
        print(f"\n{i}. {rec['platform']}: {rec['title'][:60]}...")
        print(f"   Priority: {rec['recommendation']['priority']}")
        print(f"   Score: {rec['recommendation']['score']}%")
        print(f"   URL: {rec['url'][:80]}...")

    return unique_recommendations[:4]  # Return top 4


def _deduplicate_by_platform(recommendations: List[Dict]) -> List[Dict]:
    """
    Keep one course per platform (highest scoring)
    """
    platform_map = {}

    for rec in recommendations:
        platform = rec['platform']
        score = rec['recommendation']['score']

        if platform not in platform_map or score > platform_map[platform]['recommendation']['score']:
            platform_map[platform] = rec

    # Sort by score
    unique = list(platform_map.values())
    unique.sort(key=lambda x: x['recommendation']['score'], reverse=True)

    return unique


def _generate_general_recommendations(profile: TeacherProfile) -> List[Dict[str, Any]]:
    """
    Generate general recommendations when no performance data available
    (For new teachers who haven't taken assessments yet)
    """

    print("\n💡 Generating general recommendations (no performance data yet)")

    link_generator = SmartCourseLinkGenerator()

    subject = profile.subjects_teaching.split(',')[0].strip() if profile.subjects_teaching else 'General Teaching'
    grade = profile.grades_teaching.split(',')[0].strip() if profile.grades_teaching else '6-10'

    # Extract numeric grade
    grade_match = re.search(r'\d+', grade)
    grade_num = grade_match.group() if grade_match else '6-10'

    # Generate general links for the subject
    recommendations = link_generator.generate_course_links(
        weak_area=f"{subject} Teaching Methods",
        subject=subject,
        grade=grade_num,
        board=profile.board or 'CBSE',
        state=profile.state or 'Telangana',
        difficulty='intermediate'
    )

    # Update reasoning for general recommendations
    for rec in recommendations:
        rec['recommendation']['reasoning'] = (
            f"📚 Welcome to Learnify! Since you're teaching {subject} for Grade {grade_num}, "
            f"these courses will help you strengthen your teaching skills. "
            f"Complete assessments to get personalized recommendations based on your performance. "
            + rec['recommendation']['reasoning']
        )
        rec['recommendation']['priority'] = 'medium'

    return recommendations[:4]


async def get_teacher_recommendations(db: Session, teacher_id: int) -> List[Dict[str, Any]]:
    """
    Get course recommendations for a teacher

    Note: With smart link generation, we always generate fresh recommendations
    based on current performance data (no caching)
    """

    return await generate_course_recommendations(db, teacher_id)
