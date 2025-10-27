# routers/courses.py - CPD Course Recommendation API
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from database import get_db
from models import User
from models_cpd import CPDCourse, TeacherCourseRecommendation, TeacherCourseProgress
from security import require_role
from services.course_recommender import generate_course_recommendations, get_teacher_recommendations

router = APIRouter(prefix="/courses", tags=["courses"])

@router.post("/recommendations/generate")
async def generate_recommendations(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """Generate AI-powered course recommendations based on teacher performance"""
    try:
        recommendations = await generate_course_recommendations(db, user.id)
        return {
            "success": True,
            "message": f"Generated {len(recommendations)} course recommendations",
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        )

@router.get("/recommendations")
async def get_recommendations(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """Get existing course recommendations for the current teacher"""
    try:
        recommendations = await get_teacher_recommendations(db, user.id)
        return {
            "success": True,
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch recommendations: {str(e)}"
        )

@router.post("/recommendations/{course_id}/enroll")
async def enroll_in_course(
    course_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """Mark a recommended course as enrolled"""
    # Find the recommendation
    recommendation = db.query(TeacherCourseRecommendation).filter_by(
        teacher_id=user.id,
        course_id=course_id,
        status="recommended"
    ).first()

    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )

    # Update recommendation status
    recommendation.status = "enrolled"

    # Create or update progress tracking
    progress = db.query(TeacherCourseProgress).filter_by(
        teacher_id=user.id,
        course_id=course_id
    ).first()

    if not progress:
        progress = TeacherCourseProgress(
            teacher_id=user.id,
            course_id=course_id,
            progress_percentage=0.0
        )
        db.add(progress)

    db.commit()

    return {
        "success": True,
        "message": "Successfully enrolled in course"
    }

@router.post("/recommendations/{course_id}/dismiss")
async def dismiss_recommendation(
    course_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """Dismiss a course recommendation"""
    recommendation = db.query(TeacherCourseRecommendation).filter_by(
        teacher_id=user.id,
        course_id=course_id,
        status="recommended"
    ).first()

    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )

    recommendation.status = "dismissed"
    db.commit()

    return {
        "success": True,
        "message": "Recommendation dismissed"
    }

@router.get("/progress")
async def get_course_progress(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """Get teacher's progress in enrolled courses"""
    progress_records = db.query(TeacherCourseProgress, CPDCourse).join(CPDCourse).filter(
        TeacherCourseProgress.teacher_id == user.id
    ).all()

    result = []
    for progress, course in progress_records:
        result.append({
            "course": {
                "id": course.id,
                "title": course.title,
                "platform": course.platform,
                "duration_hours": course.duration_hours
            },
            "progress": {
                "percentage": progress.progress_percentage,
                "time_spent_hours": progress.time_spent_hours,
                "completed": progress.completed,
                "last_accessed": progress.last_accessed.isoformat() if progress.last_accessed else None,
                "certificate_earned": progress.certificate_earned
            }
        })

    return {
        "success": True,
        "enrolled_courses": result
    }

@router.get("/catalog")
async def get_course_catalog(
    category: str = None,
    platform: str = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """Get available CPD courses catalog with optional filtering"""
    query = db.query(CPDCourse).filter_by(is_active=True)

    if category:
        query = query.filter(CPDCourse.category.ilike(f"%{category}%"))

    if platform:
        query = query.filter(CPDCourse.platform.ilike(f"%{platform}%"))

    courses = query.all()

    result = []
    for course in courses:
        result.append({
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "category": course.category,
            "subcategory": course.subcategory,
            "duration_hours": course.duration_hours,
            "difficulty_level": course.difficulty_level,
            "platform": course.platform,
            "provider": course.provider,
            "certificate_available": course.certificate_available,
            "url": course.url
        })

    return {
        "success": True,
        "courses": result,
        "total": len(result)
    }

# Admin endpoints for managing courses
@router.post("/admin/courses")
async def create_course(
    course_data: dict,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin"))
):
    """Admin: Create a new CPD course"""
    course = CPDCourse(**course_data)
    db.add(course)
    db.commit()
    db.refresh(course)

    return {
        "success": True,
        "message": "Course created successfully",
        "course_id": course.id
    }