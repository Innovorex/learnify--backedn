"""
Career Progression Detection Service
Analyzes teacher's education qualification and recommends appropriate next course
"""

from typing import Optional, Dict
from sqlalchemy.orm import Session
from models import TeacherProfile, CareerCourse

def detect_recommended_course(
    education: str,
    subject: str,
    db: Session
) -> Optional[Dict]:
    """
    Detect recommended career course based on teacher's education

    Args:
        education: Teacher's current education (e.g., "B.Sc Mathematics")
        subject: Teaching subject (e.g., "Mathematics")
        db: Database session

    Returns:
        Dictionary with recommendation details or None if already qualified
    """

    # Normalize inputs
    education_lower = education.lower().strip()
    subject_clean = subject.split(',')[0].strip() if ',' in subject else subject.strip()

    # Determine course type needed
    course_type_needed = None
    next_after = None
    reason = ""

    if "m.ed" in education_lower or "m ed" in education_lower or "med" in education_lower:
        # Already has M.Ed - highest qualification
        return {
            "current_qualification": education,
            "recommended_course": None,
            "next_after": None,
            "reason": "You have already completed M.Ed - the highest teaching qualification.",
            "message": "No further degree courses required. Focus on continuous professional development."
        }

    elif "b.ed" in education_lower or "b ed" in education_lower or "bed" in education_lower:
        # Has B.Ed → Recommend M.Ed
        course_type_needed = "M.Ed"
        next_after = None
        reason = "Advance your career with Master of Education (M.Ed) for leadership roles and higher positions"

    elif "m.sc" in education_lower or "m sc" in education_lower or "msc" in education_lower:
        # Has M.Sc → Need B.Ed first, then M.Ed
        course_type_needed = "B.Ed"
        next_after = "M.Ed"
        reason = "B.Ed is required for professional teaching certification. After B.Ed, you can pursue M.Ed"

    elif "b.sc" in education_lower or "b sc" in education_lower or "bsc" in education_lower:
        # Has B.Sc → Need B.Ed, then M.Ed
        course_type_needed = "B.Ed"
        next_after = "M.Ed"
        reason = "B.Ed is essential for professional teaching certification and career advancement"

    elif "b.a" in education_lower or "ba" in education_lower:
        # Has B.A → Need B.Ed
        course_type_needed = "B.Ed"
        next_after = "M.Ed"
        reason = "B.Ed will provide you with professional teaching certification"

    elif "m.a" in education_lower or "ma" in education_lower:
        # Has M.A → Need B.Ed
        course_type_needed = "B.Ed"
        next_after = "M.Ed"
        reason = "B.Ed is required for teaching certification at secondary level"

    else:
        # Other qualifications → Recommend B.Ed as default
        course_type_needed = "B.Ed"
        next_after = "M.Ed"
        reason = "B.Ed provides professional teaching qualification and opens career opportunities"

    # Find the recommended course in database
    recommended_course = db.query(CareerCourse).filter(
        CareerCourse.course_type == course_type_needed,
        CareerCourse.subject == subject_clean,
        CareerCourse.is_active == True
    ).first()

    if not recommended_course:
        # Try without subject filter (generic course)
        recommended_course = db.query(CareerCourse).filter(
            CareerCourse.course_type == course_type_needed,
            CareerCourse.is_active == True
        ).first()

    if not recommended_course:
        return {
            "current_qualification": education,
            "recommended_course": None,
            "next_after": next_after,
            "reason": reason,
            "message": f"{course_type_needed} course for {subject_clean} is not available yet. Coming soon!"
        }

    return {
        "current_qualification": education,
        "recommended_course": {
            "id": recommended_course.id,
            "name": recommended_course.course_name,
            "type": recommended_course.course_type,
            "subject": recommended_course.subject,
            "university": recommended_course.university,
            "duration_months": recommended_course.duration_months,
            "total_modules": recommended_course.total_modules,
            "description": recommended_course.description
        },
        "next_after": next_after,
        "reason": reason
    }


def get_course_benefits(course_type: str) -> list:
    """
    Get benefits of completing a specific course type

    Args:
        course_type: "B.Ed" or "M.Ed"

    Returns:
        List of benefit strings
    """
    benefits = {
        "B.Ed": [
            "₹8,000-15,000 monthly salary increase",
            "Eligible for TGT (Trained Graduate Teacher) positions",
            "Professional teaching certification (NCTE approved)",
            "Better job security and career stability",
            "Qualify for government teaching jobs",
            "Enhanced pedagogical skills and classroom management"
        ],
        "M.Ed": [
            "₹15,000-25,000 monthly salary increase",
            "Eligible for PGT (Post Graduate Teacher) and leadership roles",
            "Qualify for principal and administrative positions",
            "Research and academic career opportunities",
            "Teacher educator roles in B.Ed colleges",
            "Educational policy and curriculum development roles"
        ]
    }

    return benefits.get(course_type, [])


def check_enrollment_eligibility(
    teacher_id: int,
    course_id: int,
    db: Session
) -> tuple[bool, str]:
    """
    Check if teacher is eligible to enroll in a course

    Args:
        teacher_id: Teacher's user ID
        course_id: Course ID
        db: Database session

    Returns:
        Tuple of (is_eligible, message)
    """
    from models import TeacherCareerEnrollment

    # Check if already enrolled
    existing_enrollment = db.query(TeacherCareerEnrollment).filter(
        TeacherCareerEnrollment.teacher_id == teacher_id,
        TeacherCareerEnrollment.course_id == course_id
    ).first()

    if existing_enrollment:
        if existing_enrollment.status == "completed":
            return False, "You have already completed this course"
        elif existing_enrollment.status == "in_progress":
            return False, "You are already enrolled in this course"
        elif existing_enrollment.status == "dropped":
            return True, "You can re-enroll in this course"

    return True, "Eligible to enroll"
