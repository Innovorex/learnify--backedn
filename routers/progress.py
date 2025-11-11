"""
Progress Analytics API Router
Handles comprehensive teacher performance analytics across all dimensions:
- CPD Assessment Performance (MCQ, Submission, Outcome)
- Career Progression (B.Ed/M.Ed tracking)
- Student Impact (K-12 teaching effectiveness)
- Teaching Materials & AI Tutor Usage
- Engagement & Activity Patterns
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc, case, text
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel

from database import get_db
from models import User
from security import require_role

router = APIRouter(prefix="/progress", tags=["progress-analytics"])


# ============================================================================
# Response Models
# ============================================================================

class ScoreBreakdown(BaseModel):
    cpd_score: float
    career_score: float
    student_impact_score: float
    engagement_score: float
    materials_score: float
    overall_score: float
    rating: str  # Excellent, Very Good, Good, Satisfactory, Needs Improvement

class OverviewResponse(BaseModel):
    teacher_id: int
    teacher_name: str
    scores: ScoreBreakdown
    calculated_at: datetime

    # Quick stats
    modules_assessed: Optional[int] = 0
    career_progress_pct: Optional[float] = 0.0
    students_assessed: Optional[int] = 0
    active_days_this_month: Optional[int] = 0
    materials_count: Optional[int] = 0

class CPDAnalytics(BaseModel):
    cpd_score: float
    rating: str

    # Assessment type breakdown
    mcq_avg: Optional[float] = 0.0
    submission_avg: Optional[float] = 0.0
    outcome_avg: Optional[float] = 0.0

    # Activity metrics
    modules_assessed: int
    total_assessments: int
    last_assessment_date: Optional[datetime] = None

    # Performance trend (last 6 months)
    monthly_performance: List[Dict[str, Any]] = []

    # Strengths and areas for improvement
    strongest_area: str
    weakest_area: str

class CareerAnalytics(BaseModel):
    career_score: float
    rating: str

    # Current enrollment
    enrolled_course: Optional[str] = None
    course_type: Optional[str] = None  # B.Ed, M.Ed
    enrollment_status: Optional[str] = None

    # Progress metrics
    total_modules: int
    completed_modules: int
    in_progress_modules: int
    progress_percentage: float

    # Exam performance
    avg_exam_score: Optional[float] = 0.0
    exams_passed: int
    exams_failed: int

    # Timeline
    enrollment_date: Optional[datetime] = None
    estimated_completion_date: Optional[datetime] = None
    days_since_enrollment: Optional[int] = 0

class StudentImpactAnalytics(BaseModel):
    student_impact_score: float
    rating: str

    # Assessment creation
    assessments_created: int
    assessments_this_month: int

    # Student reach
    students_assessed: int
    unique_classes: int

    # Performance metrics
    avg_student_score: Optional[float] = 0.0
    participation_rate: Optional[float] = 0.0

    # Class-wise breakdown
    class_performance: List[Dict[str, Any]] = []

    # Subject-wise breakdown
    subject_performance: List[Dict[str, Any]] = []

    # Recent assessments
    recent_assessments: List[Dict[str, Any]] = []

class MaterialsAnalytics(BaseModel):
    materials_score: float
    rating: str

    # Materials metrics
    materials_count: int
    materials_this_month: int
    materials_by_subject: List[Dict[str, Any]] = []
    materials_by_grade: List[Dict[str, Any]] = []

    # AI Tutor usage
    ai_tutor_sessions: int
    ai_tutor_this_month: int
    avg_session_duration: Optional[float] = 0.0

    # Recent materials
    recent_materials: List[Dict[str, Any]] = []

class EngagementAnalytics(BaseModel):
    engagement_score: float
    rating: str

    # Activity metrics
    active_days_this_month: int
    total_days_in_month: int
    activity_rate: float

    # Action counts
    actions_completed: int
    avg_actions_per_day: float

    # Activity breakdown
    cpd_activities: int
    career_activities: int
    student_activities: int
    material_activities: int

    # Streak and patterns
    current_streak: int
    longest_streak: int
    most_active_day: Optional[str] = None
    most_active_hour: Optional[int] = None

    # Daily activity heatmap (last 30 days)
    daily_activity: List[Dict[str, Any]] = []


# ============================================================================
# Helper Functions
# ============================================================================

def get_score_rating(score: float) -> str:
    """Convert numeric score to rating band"""
    if score >= 90:
        return "Excellent"
    elif score >= 80:
        return "Very Good"
    elif score >= 70:
        return "Good"
    elif score >= 60:
        return "Satisfactory"
    else:
        return "Needs Improvement"


def get_teacher_current_scores(teacher_id: int, db: Session) -> Dict[str, Any]:
    """
    Get current scores from materialized view
    """
    query = text("""
        SELECT
            teacher_id, teacher_name, email,
            cpd_score, career_score, student_impact_score,
            engagement_score, materials_score, overall_score,
            modules_assessed, completed_modules, total_modules,
            assessments_created, students_assessed, active_days,
            materials_count, calculated_at
        FROM teacher_current_scores
        WHERE teacher_id = :teacher_id
    """)

    result = db.execute(query, {"teacher_id": teacher_id}).fetchone()

    if not result:
        # Return zeros if no data
        return {
            "teacher_id": teacher_id,
            "teacher_name": "",
            "email": "",
            "cpd_score": 0.0,
            "career_score": 0.0,
            "student_impact_score": 0.0,
            "engagement_score": 0.0,
            "materials_score": 0.0,
            "overall_score": 0.0,
            "modules_assessed": 0,
            "completed_modules": 0,
            "total_modules": 0,
            "assessments_created": 0,
            "students_assessed": 0,
            "active_days": 0,
            "materials_count": 0,
            "calculated_at": datetime.now()
        }

    return {
        "teacher_id": result[0],
        "teacher_name": result[1],
        "email": result[2],
        "cpd_score": float(result[3] or 0),
        "career_score": float(result[4] or 0),
        "student_impact_score": float(result[5] or 0),
        "engagement_score": float(result[6] or 0),
        "materials_score": float(result[7] or 0),
        "overall_score": float(result[8] or 0),
        "modules_assessed": int(result[9] or 0),
        "completed_modules": int(result[10] or 0),
        "total_modules": int(result[11] or 0),
        "assessments_created": int(result[12] or 0),
        "students_assessed": int(result[13] or 0),
        "active_days": int(result[14] or 0),
        "materials_count": int(result[15] or 0),
        "calculated_at": result[16] if result[16] else datetime.now()
    }


# ============================================================================
# ENDPOINT 1: Overview - Overall Score + Components
# ============================================================================
@router.get("/overview", response_model=OverviewResponse)
async def get_progress_overview(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Get comprehensive overview of teacher's progress across all dimensions
    Returns overall score and breakdown of 5 components
    """
    scores_data = get_teacher_current_scores(user.id, db)

    # Calculate career progress percentage
    career_progress_pct = 0.0
    if scores_data["total_modules"] and scores_data["total_modules"] > 0:
        career_progress_pct = round(
            (scores_data["completed_modules"] / scores_data["total_modules"]) * 100,
            1
        )

    return OverviewResponse(
        teacher_id=scores_data["teacher_id"],
        teacher_name=scores_data["teacher_name"] or user.name,
        scores=ScoreBreakdown(
            cpd_score=scores_data["cpd_score"],
            career_score=scores_data["career_score"],
            student_impact_score=scores_data["student_impact_score"],
            engagement_score=scores_data["engagement_score"],
            materials_score=scores_data["materials_score"],
            overall_score=scores_data["overall_score"],
            rating=get_score_rating(scores_data["overall_score"])
        ),
        calculated_at=scores_data["calculated_at"],
        modules_assessed=scores_data["modules_assessed"],
        career_progress_pct=career_progress_pct,
        students_assessed=scores_data["students_assessed"],
        active_days_this_month=scores_data["active_days"],
        materials_count=scores_data["materials_count"]
    )


# ============================================================================
# ENDPOINT 2: CPD Analytics - Detailed Assessment Performance
# ============================================================================
@router.get("/cpd", response_model=CPDAnalytics)
async def get_cpd_analytics(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Get detailed CPD (Continuous Professional Development) performance analytics
    Includes assessment type breakdown, trends, and strengths/weaknesses
    """
    scores_data = get_teacher_current_scores(user.id, db)

    # Get detailed CPD metrics
    cpd_query = text("""
        SELECT
            AVG(CASE WHEN m.assessment_type = 'mcq' THEN p.score END) as mcq_avg,
            AVG(CASE WHEN m.assessment_type = 'submission' THEN p.score END) as submission_avg,
            AVG(CASE WHEN m.assessment_type = 'outcome' THEN p.score END) as outcome_avg,
            COUNT(DISTINCT m.id) as modules_assessed,
            COUNT(*) as total_assessments,
            MAX(p.created_at) as last_assessment_date
        FROM performance p
        JOIN modules m ON p.module_id = m.id
        WHERE p.teacher_id = :teacher_id
        AND p.created_at >= NOW() - INTERVAL '6 months'
    """)

    cpd_result = db.execute(cpd_query, {"teacher_id": user.id}).fetchone()

    mcq_avg = float(cpd_result[0] or 0)
    submission_avg = float(cpd_result[1] or 0)
    outcome_avg = float(cpd_result[2] or 0)
    modules_assessed = int(cpd_result[3] or 0)
    total_assessments = int(cpd_result[4] or 0)
    last_assessment_date = cpd_result[5]

    # Get monthly performance trend (last 6 months)
    trend_query = text("""
        SELECT
            TO_CHAR(p.created_at, 'YYYY-MM') as month,
            AVG(p.score) as avg_score,
            COUNT(*) as assessment_count
        FROM performance p
        WHERE p.teacher_id = :teacher_id
        AND p.created_at >= NOW() - INTERVAL '6 months'
        GROUP BY TO_CHAR(p.created_at, 'YYYY-MM')
        ORDER BY month
    """)

    trend_results = db.execute(trend_query, {"teacher_id": user.id}).fetchall()
    monthly_performance = [
        {
            "month": row[0],
            "avg_score": round(float(row[1] or 0), 1),
            "assessment_count": int(row[2] or 0)
        }
        for row in trend_results
    ]

    # Determine strengths and weaknesses
    scores_map = {
        "MCQ Assessments": mcq_avg,
        "Submission-based": submission_avg,
        "Outcome-based": outcome_avg
    }

    strongest_area = max(scores_map, key=scores_map.get) if any(scores_map.values()) else "N/A"
    weakest_area = min(scores_map, key=scores_map.get) if any(scores_map.values()) else "N/A"

    return CPDAnalytics(
        cpd_score=scores_data["cpd_score"],
        rating=get_score_rating(scores_data["cpd_score"]),
        mcq_avg=round(mcq_avg, 1),
        submission_avg=round(submission_avg, 1),
        outcome_avg=round(outcome_avg, 1),
        modules_assessed=modules_assessed,
        total_assessments=total_assessments,
        last_assessment_date=last_assessment_date,
        monthly_performance=monthly_performance,
        strongest_area=strongest_area,
        weakest_area=weakest_area
    )


# ============================================================================
# ENDPOINT 3: Career Analytics - Progression Tracking
# ============================================================================
@router.get("/career", response_model=CareerAnalytics)
async def get_career_analytics(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Get detailed career progression analytics (B.Ed/M.Ed tracking)
    Includes module progress, exam performance, and timeline
    """
    scores_data = get_teacher_current_scores(user.id, db)

    # Get detailed career progression data
    career_query = text("""
        SELECT
            cc.course_name,
            cc.course_type,
            tce.status as enrollment_status,
            cc.total_modules,
            COUNT(CASE WHEN mp.passed = TRUE THEN 1 END) as completed_modules,
            COUNT(CASE WHEN mp.status = 'in_progress' THEN 1 END) as in_progress_modules,
            AVG(CASE WHEN mp.passed = TRUE THEN mp.exam_score END) as avg_exam_score,
            COUNT(CASE WHEN mp.passed = TRUE THEN 1 END) as exams_passed,
            COUNT(CASE WHEN mp.passed = FALSE THEN 1 END) as exams_failed,
            tce.created_at as enrollment_date,
            EXTRACT(DAY FROM NOW() - tce.created_at) as days_since_enrollment
        FROM teacher_career_enrollments tce
        JOIN career_courses cc ON tce.course_id = cc.id
        LEFT JOIN module_progress mp ON tce.id = mp.enrollment_id
        WHERE tce.teacher_id = :teacher_id
        AND tce.status IN ('in_progress', 'completed')
        GROUP BY cc.course_name, cc.course_type, tce.status, cc.total_modules, tce.created_at
        ORDER BY tce.created_at DESC
        LIMIT 1
    """)

    career_result = db.execute(career_query, {"teacher_id": user.id}).fetchone()

    if career_result:
        course_name = career_result[0]
        course_type = career_result[1]
        enrollment_status = career_result[2]
        total_modules = int(career_result[3] or 0)
        completed_modules = int(career_result[4] or 0)
        in_progress_modules = int(career_result[5] or 0)
        avg_exam_score = float(career_result[6] or 0)
        exams_passed = int(career_result[7] or 0)
        exams_failed = int(career_result[8] or 0)
        enrollment_date = career_result[9]
        days_since_enrollment = int(career_result[10] or 0)

        progress_percentage = round((completed_modules / total_modules * 100), 1) if total_modules > 0 else 0.0

        # Estimate completion date (assume 1 module per week)
        remaining_modules = total_modules - completed_modules
        estimated_completion_date = datetime.now() + timedelta(weeks=remaining_modules) if remaining_modules > 0 else None
    else:
        course_name = None
        course_type = None
        enrollment_status = None
        total_modules = 0
        completed_modules = 0
        in_progress_modules = 0
        avg_exam_score = 0.0
        exams_passed = 0
        exams_failed = 0
        enrollment_date = None
        days_since_enrollment = 0
        progress_percentage = 0.0
        estimated_completion_date = None

    return CareerAnalytics(
        career_score=scores_data["career_score"],
        rating=get_score_rating(scores_data["career_score"]),
        enrolled_course=course_name,
        course_type=course_type,
        enrollment_status=enrollment_status,
        total_modules=total_modules,
        completed_modules=completed_modules,
        in_progress_modules=in_progress_modules,
        progress_percentage=progress_percentage,
        avg_exam_score=round(avg_exam_score, 1),
        exams_passed=exams_passed,
        exams_failed=exams_failed,
        enrollment_date=enrollment_date,
        estimated_completion_date=estimated_completion_date,
        days_since_enrollment=days_since_enrollment
    )


# ============================================================================
# ENDPOINT 4: Student Impact Analytics - K-12 Teaching Effectiveness
# ============================================================================
@router.get("/students", response_model=StudentImpactAnalytics)
async def get_student_impact_analytics(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Get detailed student impact analytics
    Includes assessment creation, student reach, and performance metrics
    """
    scores_data = get_teacher_current_scores(user.id, db)

    # Get assessment and student metrics
    student_query = text("""
        SELECT
            COUNT(DISTINCT ka.id) as assessments_created,
            COUNT(DISTINCT CASE WHEN ka.created_at >= DATE_TRUNC('month', NOW()) THEN ka.id END) as assessments_this_month,
            COUNT(DISTINCT kr.student_id) as students_assessed,
            COUNT(DISTINCT CONCAT(ka.class_name, '-', ka.section)) as unique_classes,
            AVG(CASE WHEN (SELECT COUNT(*) FROM k12_questions WHERE assessment_id = ka.id) > 0
                THEN kr.score * 100.0 / (SELECT COUNT(*) FROM k12_questions WHERE assessment_id = ka.id)
                ELSE 0 END) as avg_student_score
        FROM k12_assessments ka
        LEFT JOIN k12_results kr ON ka.id = kr.assessment_id
        WHERE ka.teacher_id = :teacher_id
        AND ka.created_at >= DATE_TRUNC('month', NOW()) - INTERVAL '6 months'
    """)

    student_result = db.execute(student_query, {"teacher_id": user.id}).fetchone()

    assessments_created = int(student_result[0] or 0)
    assessments_this_month = int(student_result[1] or 0)
    students_assessed = int(student_result[2] or 0)
    unique_classes = int(student_result[3] or 0)
    avg_student_score = float(student_result[4] or 0)

    # Get class-wise performance
    class_query = text("""
        SELECT
            CONCAT(ka.class_name, '-', ka.section) as class_section,
            COUNT(DISTINCT ka.id) as assessments,
            COUNT(DISTINCT kr.student_id) as students,
            AVG(CASE WHEN (SELECT COUNT(*) FROM k12_questions WHERE assessment_id = ka.id) > 0
                THEN kr.score * 100.0 / (SELECT COUNT(*) FROM k12_questions WHERE assessment_id = ka.id)
                ELSE 0 END) as avg_score
        FROM k12_assessments ka
        LEFT JOIN k12_results kr ON ka.id = kr.assessment_id
        WHERE ka.teacher_id = :teacher_id
        AND ka.created_at >= DATE_TRUNC('month', NOW())
        GROUP BY CONCAT(ka.class_name, '-', ka.section)
        ORDER BY avg_score DESC
    """)

    class_results = db.execute(class_query, {"teacher_id": user.id}).fetchall()
    class_performance = [
        {
            "class": row[0],
            "assessments": int(row[1] or 0),
            "students": int(row[2] or 0),
            "avg_score": round(float(row[3] or 0), 1)
        }
        for row in class_results
    ]

    # Get subject-wise performance
    subject_query = text("""
        SELECT
            ka.subject,
            COUNT(DISTINCT ka.id) as assessments,
            AVG(CASE WHEN (SELECT COUNT(*) FROM k12_questions WHERE assessment_id = ka.id) > 0
                THEN kr.score * 100.0 / (SELECT COUNT(*) FROM k12_questions WHERE assessment_id = ka.id)
                ELSE 0 END) as avg_score
        FROM k12_assessments ka
        LEFT JOIN k12_results kr ON ka.id = kr.assessment_id
        WHERE ka.teacher_id = :teacher_id
        AND ka.created_at >= DATE_TRUNC('month', NOW())
        GROUP BY ka.subject
        ORDER BY avg_score DESC
    """)

    subject_results = db.execute(subject_query, {"teacher_id": user.id}).fetchall()
    subject_performance = [
        {
            "subject": row[0],
            "assessments": int(row[1] or 0),
            "avg_score": round(float(row[2] or 0), 1)
        }
        for row in subject_results
    ]

    # Get recent assessments
    recent_query = text("""
        SELECT
            ka.chapter,
            ka.subject,
            CONCAT(ka.class_name, '-', ka.section) as class_section,
            ka.created_at,
            COUNT(DISTINCT kr.student_id) as students_attempted
        FROM k12_assessments ka
        LEFT JOIN k12_results kr ON ka.id = kr.assessment_id
        WHERE ka.teacher_id = :teacher_id
        GROUP BY ka.id, ka.chapter, ka.subject, ka.class_name, ka.section, ka.created_at
        ORDER BY ka.created_at DESC
        LIMIT 5
    """)

    recent_results = db.execute(recent_query, {"teacher_id": user.id}).fetchall()
    recent_assessments = [
        {
            "chapter": row[0],
            "subject": row[1],
            "class": row[2],
            "created_at": row[3].isoformat() if row[3] else None,
            "students_attempted": int(row[4] or 0)
        }
        for row in recent_results
    ]

    # Calculate participation rate
    participation_rate = 0.0
    if unique_classes > 0:
        participation_rate = round((students_assessed / (unique_classes * 30)) * 100, 1)  # Assume 30 students per class

    return StudentImpactAnalytics(
        student_impact_score=scores_data["student_impact_score"],
        rating=get_score_rating(scores_data["student_impact_score"]),
        assessments_created=assessments_created,
        assessments_this_month=assessments_this_month,
        students_assessed=students_assessed,
        unique_classes=unique_classes,
        avg_student_score=round(avg_student_score, 1),
        participation_rate=participation_rate,
        class_performance=class_performance,
        subject_performance=subject_performance,
        recent_assessments=recent_assessments
    )


# ============================================================================
# ENDPOINT 5: Materials Analytics - Teaching Resources & AI Tutor
# ============================================================================
@router.get("/materials", response_model=MaterialsAnalytics)
async def get_materials_analytics(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Get detailed teaching materials and AI tutor usage analytics
    """
    scores_data = get_teacher_current_scores(user.id, db)

    # Get materials metrics
    materials_query = text("""
        SELECT
            COUNT(*) as materials_count,
            COUNT(CASE WHEN created_at >= DATE_TRUNC('month', NOW()) THEN 1 END) as materials_this_month
        FROM teaching_materials
        WHERE teacher_id = :teacher_id
        AND created_at >= DATE_TRUNC('month', NOW()) - INTERVAL '6 months'
    """)

    materials_result = db.execute(materials_query, {"teacher_id": user.id}).fetchone()
    materials_count = int(materials_result[0] or 0)
    materials_this_month = int(materials_result[1] or 0)

    # Get materials by subject
    subject_query = text("""
        SELECT
            subject,
            COUNT(*) as count
        FROM teaching_materials
        WHERE teacher_id = :teacher_id
        AND created_at >= DATE_TRUNC('month', NOW())
        GROUP BY subject
        ORDER BY count DESC
    """)

    subject_results = db.execute(subject_query, {"teacher_id": user.id}).fetchall()
    materials_by_subject = [
        {"subject": row[0], "count": int(row[1] or 0)}
        for row in subject_results
    ]

    # Get materials by grade
    grade_query = text("""
        SELECT
            grade_level,
            COUNT(*) as count
        FROM teaching_materials
        WHERE teacher_id = :teacher_id
        AND created_at >= DATE_TRUNC('month', NOW())
        GROUP BY grade_level
        ORDER BY grade_level
    """)

    grade_results = db.execute(grade_query, {"teacher_id": user.id}).fetchall()
    materials_by_grade = [
        {"grade": row[0], "count": int(row[1] or 0)}
        for row in grade_results
    ]

    # Get AI Tutor usage
    ai_tutor_query = text("""
        SELECT
            COUNT(*) as session_count,
            COUNT(CASE WHEN created_at >= DATE_TRUNC('month', NOW()) THEN 1 END) as sessions_this_month,
            AVG(EXTRACT(EPOCH FROM (last_activity - created_at))/60) as avg_duration_minutes
        FROM ai_tutor_sessions
        WHERE teacher_id = :teacher_id
        AND created_at >= DATE_TRUNC('month', NOW()) - INTERVAL '6 months'
    """)

    ai_tutor_result = db.execute(ai_tutor_query, {"teacher_id": user.id}).fetchone()
    ai_tutor_sessions = int(ai_tutor_result[0] or 0)
    ai_tutor_this_month = int(ai_tutor_result[1] or 0)
    avg_session_duration = float(ai_tutor_result[2] or 0)

    # Get recent materials
    recent_query = text("""
        SELECT
            title,
            subject,
            grade_level,
            created_at
        FROM teaching_materials
        WHERE teacher_id = :teacher_id
        ORDER BY created_at DESC
        LIMIT 5
    """)

    recent_results = db.execute(recent_query, {"teacher_id": user.id}).fetchall()
    recent_materials = [
        {
            "name": row[0],
            "subject": row[1],
            "grade": row[2],
            "created_at": row[3].isoformat() if row[3] else None
        }
        for row in recent_results
    ]

    return MaterialsAnalytics(
        materials_score=scores_data["materials_score"],
        rating=get_score_rating(scores_data["materials_score"]),
        materials_count=materials_count,
        materials_this_month=materials_this_month,
        materials_by_subject=materials_by_subject,
        materials_by_grade=materials_by_grade,
        ai_tutor_sessions=ai_tutor_sessions,
        ai_tutor_this_month=ai_tutor_this_month,
        avg_session_duration=round(avg_session_duration, 1),
        recent_materials=recent_materials
    )


# ============================================================================
# ENDPOINT 6: Engagement Analytics - Activity Patterns
# ============================================================================
@router.get("/engagement", response_model=EngagementAnalytics)
async def get_engagement_analytics(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Get detailed engagement and activity pattern analytics
    Includes streaks, activity breakdown, and heatmap data
    """
    scores_data = get_teacher_current_scores(user.id, db)

    # Get engagement metrics from performance table
    engagement_query = text("""
        SELECT
            COUNT(DISTINCT DATE(created_at)) as active_days,
            COUNT(*) as actions_completed,
            EXTRACT(DAY FROM (DATE_TRUNC('month', NOW()) + INTERVAL '1 month' - INTERVAL '1 day')) as total_days
        FROM performance
        WHERE teacher_id = :teacher_id
        AND created_at >= DATE_TRUNC('month', NOW())
    """)

    engagement_result = db.execute(engagement_query, {"teacher_id": user.id}).fetchone()
    active_days = int(engagement_result[0] or 0)
    actions_completed = int(engagement_result[1] or 0)
    total_days = int(engagement_result[2] or 30)

    activity_rate = round((active_days / total_days * 100), 1)
    avg_actions_per_day = round((actions_completed / active_days), 1) if active_days > 0 else 0.0

    # Get activity breakdown by type
    # CPD activities
    cpd_count_query = text("""
        SELECT COUNT(*) FROM performance
        WHERE teacher_id = :teacher_id
        AND created_at >= DATE_TRUNC('month', NOW())
    """)
    cpd_activities = db.execute(cpd_count_query, {"teacher_id": user.id}).scalar() or 0

    # Career activities (module progress)
    career_count_query = text("""
        SELECT COUNT(*) FROM module_progress mp
        JOIN teacher_career_enrollments tce ON mp.enrollment_id = tce.id
        WHERE tce.teacher_id = :teacher_id
        AND (mp.completed_at >= DATE_TRUNC('month', NOW()) OR mp.started_at >= DATE_TRUNC('month', NOW()))
    """)
    career_activities = db.execute(career_count_query, {"teacher_id": user.id}).scalar() or 0

    # Student activities (assessments)
    student_count_query = text("""
        SELECT COUNT(*) FROM k12_assessments
        WHERE teacher_id = :teacher_id
        AND created_at >= DATE_TRUNC('month', NOW())
    """)
    student_activities = db.execute(student_count_query, {"teacher_id": user.id}).scalar() or 0

    # Material activities
    material_count_query = text("""
        SELECT COUNT(*) FROM teaching_materials
        WHERE teacher_id = :teacher_id
        AND created_at >= DATE_TRUNC('month', NOW())
    """)
    material_activities = db.execute(material_count_query, {"teacher_id": user.id}).scalar() or 0

    # Calculate streaks
    streak_query = text("""
        WITH daily_activity AS (
            SELECT DISTINCT DATE(created_at) as activity_date
            FROM performance
            WHERE teacher_id = :teacher_id
            AND created_at >= NOW() - INTERVAL '90 days'
            ORDER BY activity_date DESC
        ),
        streak_groups AS (
            SELECT
                activity_date,
                activity_date - (ROW_NUMBER() OVER (ORDER BY activity_date))::INTEGER * INTERVAL '1 day' as streak_group
            FROM daily_activity
        )
        SELECT
            COUNT(*) as streak_length,
            MIN(activity_date) as streak_start
        FROM streak_groups
        GROUP BY streak_group
        ORDER BY streak_length DESC
        LIMIT 1
    """)

    streak_result = db.execute(streak_query, {"teacher_id": user.id}).fetchone()
    longest_streak = int(streak_result[0] or 0) if streak_result else 0

    # Current streak (consecutive days from today)
    current_streak_query = text("""
        WITH RECURSIVE dates AS (
            SELECT CURRENT_DATE::date as check_date
            UNION ALL
            SELECT (check_date - INTERVAL '1 day')::date
            FROM dates
            WHERE (check_date - INTERVAL '1 day')::date >= (CURRENT_DATE - INTERVAL '30 days')::date
        ),
        daily_activity AS (
            SELECT DISTINCT DATE(created_at) as activity_date
            FROM performance
            WHERE teacher_id = :teacher_id
            AND created_at >= CURRENT_DATE - INTERVAL '30 days'
        )
        SELECT COUNT(*)
        FROM dates d
        JOIN daily_activity da ON d.check_date = da.activity_date
        WHERE d.check_date <= CURRENT_DATE
    """)

    current_streak = db.execute(current_streak_query, {"teacher_id": user.id}).scalar() or 0

    # Get most active day and hour
    day_query = text("""
        SELECT TO_CHAR(created_at, 'Day') as day_name, COUNT(*) as activity_count
        FROM performance
        WHERE teacher_id = :teacher_id
        AND created_at >= DATE_TRUNC('month', NOW())
        GROUP BY TO_CHAR(created_at, 'Day')
        ORDER BY activity_count DESC
        LIMIT 1
    """)

    day_result = db.execute(day_query, {"teacher_id": user.id}).fetchone()
    most_active_day = day_result[0].strip() if day_result else None

    hour_query = text("""
        SELECT EXTRACT(HOUR FROM created_at) as hour, COUNT(*) as activity_count
        FROM performance
        WHERE teacher_id = :teacher_id
        AND created_at >= DATE_TRUNC('month', NOW())
        GROUP BY EXTRACT(HOUR FROM created_at)
        ORDER BY activity_count DESC
        LIMIT 1
    """)

    hour_result = db.execute(hour_query, {"teacher_id": user.id}).fetchone()
    most_active_hour = int(hour_result[0]) if hour_result else None

    # Get daily activity heatmap (last 30 days)
    heatmap_query = text("""
        SELECT
            DATE(created_at) as date,
            COUNT(*) as activity_count
        FROM performance
        WHERE teacher_id = :teacher_id
        AND created_at >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY DATE(created_at)
        ORDER BY date
    """)

    heatmap_results = db.execute(heatmap_query, {"teacher_id": user.id}).fetchall()
    daily_activity = [
        {
            "date": row[0].isoformat(),
            "count": int(row[1] or 0)
        }
        for row in heatmap_results
    ]

    return EngagementAnalytics(
        engagement_score=scores_data["engagement_score"],
        rating=get_score_rating(scores_data["engagement_score"]),
        active_days_this_month=active_days,
        total_days_in_month=total_days,
        activity_rate=activity_rate,
        actions_completed=actions_completed,
        avg_actions_per_day=avg_actions_per_day,
        cpd_activities=cpd_activities,
        career_activities=career_activities,
        student_activities=student_activities,
        material_activities=material_activities,
        current_streak=current_streak,
        longest_streak=longest_streak,
        most_active_day=most_active_day,
        most_active_hour=most_active_hour,
        daily_activity=daily_activity
    )


# ============================================================================
# ENDPOINT 7: Refresh Materialized View (Admin/Scheduled)
# ============================================================================
@router.post("/refresh-scores")
async def refresh_teacher_scores(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))  # Can be changed to admin only
):
    """
    Manually refresh the teacher_current_scores materialized view
    This endpoint can be called periodically (e.g., daily cron job)
    """
    try:
        db.execute(text("SELECT refresh_teacher_scores()"))
        db.commit()
        return {
            "success": True,
            "message": "Teacher scores refreshed successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to refresh scores: {str(e)}"
        )
