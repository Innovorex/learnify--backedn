"""
Course Matcher Engine
=====================
Intelligently matches teacher needs to real CPD courses
Replaces AI hallucination with verified course recommendations
"""

import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
import json
import re

from models import RealCPDCourse, CPDCourseRecommendation, User, TeacherProfile, ModuleProgress
from database import SessionLocal


class CourseMatcher:
    """Matches teacher needs to real CPD courses"""

    def __init__(self, db: Session):
        self.db = db

    def find_matching_courses(self,
                             weak_areas: List[str],
                             teacher_profile: Dict,
                             difficulty: str = "intermediate",
                             max_courses: int = 5) -> List[Tuple[RealCPDCourse, float]]:
        """
        Find real CPD courses that match teacher's weak areas

        Args:
            weak_areas: List of weak topics/modules (e.g., ["Algebra", "Fractions"])
            teacher_profile: Teacher's profile data (subjects, grades, board)
            difficulty: Recommended difficulty level
            max_courses: Maximum courses to return

        Returns:
            List of (course, match_score) tuples
        """

        # Extract teacher context
        subjects_teaching = teacher_profile.get("subjects_teaching", "")
        grades_teaching = teacher_profile.get("grades_teaching", "")
        board = teacher_profile.get("board", "")

        # Parse subjects and grades
        teacher_subjects = [s.strip() for s in subjects_teaching.split(",")]
        teacher_grades = [g.strip() for g in grades_teaching.split(",")]

        # Build search keywords from weak areas
        search_keywords = []
        for area in weak_areas:
            # Extract meaningful words (4+ chars)
            words = re.findall(r'\b\w{4,}\b', area.lower())
            search_keywords.extend(words)

        print(f"\n🔍 Searching for courses:")
        print(f"   Weak areas: {weak_areas}")
        print(f"   Keywords: {search_keywords}")
        print(f"   Subjects: {teacher_subjects}")
        print(f"   Grades: {teacher_grades}")
        print(f"   Difficulty: {difficulty}")

        # Query database for matching courses
        query = self.db.query(RealCPDCourse).filter(
            RealCPDCourse.is_active == True
        )

        # Apply difficulty filter
        if difficulty:
            query = query.filter(RealCPDCourse.difficulty_level == difficulty)

        # Get all active courses
        all_courses = query.all()

        print(f"   Found {len(all_courses)} active courses in database")

        # Score each course
        scored_courses = []

        for course in all_courses:
            score = self._calculate_match_score(
                course,
                search_keywords,
                teacher_subjects,
                teacher_grades,
                weak_areas
            )

            if score > 0:
                scored_courses.append((course, score))

        # Sort by score (descending)
        scored_courses.sort(key=lambda x: x[1], reverse=True)

        # Return top N
        top_courses = scored_courses[:max_courses]

        print(f"   ✅ Found {len(top_courses)} matching courses")
        for course, score in top_courses:
            print(f"      {score:.1f}% - {course.title[:60]}")

        return top_courses

    def _calculate_match_score(self,
                               course: RealCPDCourse,
                               search_keywords: List[str],
                               teacher_subjects: List[str],
                               teacher_grades: List[str],
                               weak_areas: List[str]) -> float:
        """
        Calculate match score (0-100) between course and teacher needs

        Scoring criteria:
        - Keyword match in title/description: 40 points
        - Subject match: 30 points
        - Grade level match: 20 points
        - Category relevance: 10 points
        """

        score = 0.0

        # 1. Keyword matching (40 points max)
        course_text = f"{course.title} {course.description or ''} {course.keywords or ''}".lower()

        keyword_matches = 0
        for keyword in search_keywords:
            if keyword in course_text:
                keyword_matches += 1

        if len(search_keywords) > 0:
            keyword_score = (keyword_matches / len(search_keywords)) * 40
            score += keyword_score

        # 2. Subject matching (30 points max)
        course_subjects = course.subjects or ""
        course_subjects_list = [s.strip().lower() for s in course_subjects.split(",")]

        subject_matches = 0
        for teacher_subj in teacher_subjects:
            teacher_subj_lower = teacher_subj.lower()
            for course_subj in course_subjects_list:
                if teacher_subj_lower in course_subj or course_subj in teacher_subj_lower:
                    subject_matches += 1
                    break

        # Special handling for "All Subjects" courses
        if "all subjects" in course_subjects.lower() or course_subjects == "":
            subject_matches = max(1, subject_matches)

        if len(teacher_subjects) > 0:
            subject_score = (subject_matches / len(teacher_subjects)) * 30
            score += subject_score

        # 3. Grade level matching (20 points max)
        course_grades = course.grades or ""

        if not course_grades or "all" in course_grades.lower():
            # Course applies to all grades
            score += 15
        else:
            course_grades_list = [g.strip() for g in course_grades.split(",")]

            grade_matches = 0
            for teacher_grade in teacher_grades:
                # Extract numeric grade (e.g., "Grade 6" -> "6")
                teacher_grade_num = re.search(r'\d+', teacher_grade)
                if teacher_grade_num:
                    teacher_grade_num = teacher_grade_num.group()

                    if teacher_grade_num in course_grades_list:
                        grade_matches += 1

            if len(teacher_grades) > 0:
                grade_score = (grade_matches / len(teacher_grades)) * 20
                score += grade_score

        # 4. Category relevance (10 points max)
        relevant_categories = [
            "Subject Knowledge",
            "Subject Pedagogy",
            "Assessment",
            "Professional Development"
        ]

        category = course.category or ""
        if any(cat.lower() in category.lower() for cat in relevant_categories):
            score += 10
        elif category:
            score += 5

        return round(score, 2)

    def create_recommendations(self,
                              teacher_id: int,
                              weak_areas: List[Dict],
                              max_per_area: int = 2) -> List[CPDCourseRecommendation]:
        """
        Create personalized course recommendations for a teacher

        Args:
            teacher_id: Teacher's user ID
            weak_areas: List of weak area dicts with 'name', 'decline_percent', etc.
            max_per_area: Maximum courses to recommend per weak area

        Returns:
            List of CPDCourseRecommendation objects
        """

        print(f"\n{'='*80}")
        print(f"CREATING COURSE RECOMMENDATIONS FOR TEACHER {teacher_id}")
        print(f"{'='*80}")

        # Get teacher profile
        teacher = self.db.query(User).filter(User.id == teacher_id).first()
        if not teacher or not teacher.profile:
            print("❌ Teacher or profile not found")
            return []

        profile = teacher.profile
        teacher_profile = {
            "subjects_teaching": profile.subjects_teaching,
            "grades_teaching": profile.grades_teaching,
            "board": profile.board,
            "state": profile.state
        }

        print(f"Teacher: {teacher.name}")
        print(f"Subjects: {profile.subjects_teaching}")
        print(f"Grades: {profile.grades_teaching}")
        print(f"Board: {profile.board}")

        # Clear existing pending recommendations
        self.db.query(CPDCourseRecommendation).filter(
            CPDCourseRecommendation.teacher_id == teacher_id,
            CPDCourseRecommendation.status == "pending"
        ).delete()
        self.db.commit()

        all_recommendations = []

        # Process each weak area
        for weak_area in weak_areas:
            area_name = weak_area.get("name", "")
            decline_percent = weak_area.get("decline_percent", 0)
            current_score = weak_area.get("current_score", 0)
            difficulty = weak_area.get("recommended_difficulty", "intermediate")

            print(f"\n📉 Weak Area: {area_name}")
            print(f"   Decline: {decline_percent}% | Score: {current_score}% | Difficulty: {difficulty}")

            # Find matching courses
            matching_courses = self.find_matching_courses(
                weak_areas=[area_name],
                teacher_profile=teacher_profile,
                difficulty=difficulty,
                max_courses=max_per_area
            )

            # Create recommendations
            for course, match_score in matching_courses:
                # Determine priority
                if decline_percent > 30 or current_score < 40:
                    priority = "urgent"
                elif decline_percent > 15 or current_score < 60:
                    priority = "high"
                else:
                    priority = "medium"

                # Build recommendation reason
                reason = self._build_recommendation_reason(
                    area_name,
                    decline_percent,
                    current_score
                )

                # Create recommendation
                recommendation = CPDCourseRecommendation(
                    teacher_id=teacher_id,
                    course_id=course.id,
                    recommendation_reason=reason,
                    priority=priority,
                    match_score=match_score,
                    improvement_areas=json.dumps([area_name]),
                    status="pending"
                )

                self.db.add(recommendation)
                all_recommendations.append(recommendation)

                print(f"   ✅ Recommended: {course.title[:60]}")
                print(f"      Match: {match_score:.1f}% | Priority: {priority}")

        # Commit all recommendations
        self.db.commit()

        print(f"\n{'='*80}")
        print(f"✅ Created {len(all_recommendations)} course recommendations")
        print(f"{'='*80}\n")

        return all_recommendations

    def _build_recommendation_reason(self,
                                    area_name: str,
                                    decline_percent: float,
                                    current_score: float) -> str:
        """Build human-readable recommendation reason"""

        if decline_percent > 0:
            reason = f"Your {area_name} score declined by {abs(decline_percent):.0f}% in recent assessments. "
        else:
            reason = f"Your {area_name} performance needs improvement (current: {current_score:.0f}%). "

        if current_score < 40:
            reason += "This course will help you build foundational knowledge."
        elif current_score < 60:
            reason += "This course addresses key concepts to strengthen your understanding."
        else:
            reason += "This course will help you maintain and enhance your expertise."

        return reason

    def get_teacher_recommendations(self, teacher_id: int) -> List[Dict]:
        """
        Get all active recommendations for a teacher

        Returns:
            List of recommendation dictionaries with course details
        """

        recommendations = self.db.query(CPDCourseRecommendation).filter(
            CPDCourseRecommendation.teacher_id == teacher_id,
            CPDCourseRecommendation.status == "pending"
        ).order_by(
            CPDCourseRecommendation.priority.desc(),
            CPDCourseRecommendation.match_score.desc()
        ).all()

        result = []
        for rec in recommendations:
            course = rec.course

            result.append({
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "category": course.category,
                "duration_hours": course.duration_hours,
                "platform": course.platform,
                "url": course.course_url,
                "certificate_available": course.certificate_available,
                "recommendation": {
                    "score": rec.match_score,
                    "priority": rec.priority,
                    "reasoning": rec.recommendation_reason,
                    "improvement_areas": json.loads(rec.improvement_areas) if rec.improvement_areas else []
                }
            })

        return result


def test_matcher():
    """Test the course matcher"""

    db = SessionLocal()
    matcher = CourseMatcher(db)

    # Simulate teacher profile
    teacher_profile = {
        "subjects_teaching": "Mathematics, Science",
        "grades_teaching": "Grade 6, Grade 7, Grade 8",
        "board": "CBSE",
        "state": "Telangana"
    }

    # Simulate weak areas
    weak_areas = ["Algebra", "Fractions"]

    # Find matching courses
    courses = matcher.find_matching_courses(
        weak_areas=weak_areas,
        teacher_profile=teacher_profile,
        difficulty="intermediate",
        max_courses=5
    )

    print(f"\n{'='*80}")
    print(f"TEST RESULTS")
    print(f"{'='*80}")
    print(f"Found {len(courses)} matching courses:\n")

    for course, score in courses:
        print(f"{score:.1f}% - {course.title}")
        print(f"        Platform: {course.platform}")
        print(f"        URL: {course.course_url}")
        print()

    db.close()


if __name__ == "__main__":
    test_matcher()
