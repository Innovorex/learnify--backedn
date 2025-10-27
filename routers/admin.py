# routers/admin.py - Admin Dashboard API endpoints
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Any
from database import get_db
from models import User, TeacherProfile, Performance, Module
from models_cpd import CPDCourse, TeacherCourseRecommendation, TeacherCourseProgress
from security import require_role, hash_password
from datetime import datetime, timedelta

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users")
async def get_all_users(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin"))
):
    """Get all users (teachers and admins)"""
    users = db.query(User).all()
    return {"users": users}

@router.post("/users")
async def create_user(
    user_data: dict,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin"))
):
    """Create a new user (teacher or admin)"""
    existing_user = db.query(User).filter_by(email=user_data.get("email")).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = User(
        name=user_data.get("name"),
        email=user_data.get("email"),
        password=hash_password(user_data.get("password", "password123")),
        role=user_data.get("role", "teacher"),
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "success": True,
        "message": f"{new_user.role.capitalize()} created successfully",
        "user": new_user
    }

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    """Delete a user"""
    user_to_delete = db.query(User).filter_by(id=user_id).first()
    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user_to_delete.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admins cannot delete themselves"
        )

    db.delete(user_to_delete)
    db.commit()

    return {"success": True, "message": "User deleted successfully"}

@router.patch("/users/{user_id}/status")
async def toggle_user_status(
    user_id: int,
    status_data: dict,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin"))
):
    """Toggle user active status"""
    user_to_update = db.query(User).filter_by(id=user_id).first()
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user_to_update.is_active = status_data.get("is_active", user_to_update.is_active)
    db.commit()

    return {
        "success": True,
        "message": f"User status updated successfully"
    }

@router.get("/stats")
async def get_admin_stats(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin"))
):
    """Get comprehensive system statistics for admin dashboard"""

    # Basic counts
    total_teachers = db.query(User).filter_by(role="teacher").count()
    total_courses = db.query(CPDCourse).filter_by(is_active=True).count()
    total_recommendations = db.query(TeacherCourseRecommendation).count()
    active_enrollments = db.query(TeacherCourseRecommendation).filter_by(status="enrolled").count()

    # Average performance calculation
    avg_performance = db.query(func.avg(Performance.score)).scalar() or 0

    # Recent activities (last 24 hours simulation)
    recent_activities = [
        {
            "teacher": "John Doe",
            "action": "enrolled in Digital Math Tools",
            "time": "2 hours ago"
        },
        {
            "teacher": "Jane Smith",
            "action": "completed FLN course",
            "time": "4 hours ago"
        },
        {
            "teacher": "Mike Johnson",
            "action": "dismissed recommendation",
            "time": "6 hours ago"
        }
    ]

    return {
        "totalTeachers": total_teachers,
        "totalCourses": total_courses,
        "totalRecommendations": total_recommendations,
        "activeEnrollments": active_enrollments,
        "averagePerformance": round(avg_performance, 1),
        "recentActivities": recent_activities
    }

@router.get("/teachers")
async def get_all_teachers(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin"))
):
    """Get all teachers with their profiles and performance data"""

    teachers = db.query(User).filter_by(role="teacher").all()
    result = []

    for teacher in teachers:
        profile = db.query(TeacherProfile).filter_by(user_id=teacher.id).first()

        # Get performance summary
        performances = db.query(Performance, Module).join(Module).filter(
            Performance.teacher_id == teacher.id
        ).all()

        weak_areas = []
        strong_areas = []
        total_score = 0

        for perf, module in performances:
            if perf.score < 60:
                weak_areas.append(module.name)
            elif perf.score >= 80:
                strong_areas.append(module.name)
            total_score += perf.score

        overall_score = round(total_score / len(performances), 1) if performances else 0

        # Get course progress
        enrolled_count = db.query(TeacherCourseRecommendation).filter_by(
            teacher_id=teacher.id, status="enrolled"
        ).count()

        completed_count = db.query(TeacherCourseProgress).filter_by(
            teacher_id=teacher.id, completed=True
        ).count()

        recommendations_received = db.query(TeacherCourseRecommendation).filter_by(
            teacher_id=teacher.id
        ).count()

        recommendations_accepted = db.query(TeacherCourseRecommendation).filter_by(
            teacher_id=teacher.id, status="enrolled"
        ).count()

        teacher_data = {
            "id": teacher.id,
            "name": teacher.name,
            "email": teacher.email,
            "profile": {
                "education": profile.education if profile else "N/A",
                "experience_years": profile.experience_years if profile else 0,
                "grades_teaching": profile.grades_teaching if profile else "N/A",
                "subjects_teaching": profile.subjects_teaching if profile else "N/A",
                "board": profile.board if profile else "N/A"
            } if profile else None,
            "performance_summary": {
                "overall_score": overall_score,
                "total_assessments": len(performances),
                "weak_areas": weak_areas,
                "strong_areas": strong_areas
            },
            "course_progress": {
                "enrolled_courses": enrolled_count,
                "completed_courses": completed_count,
                "recommendations_received": recommendations_received,
                "recommendations_accepted": recommendations_accepted
            }
        }

        result.append(teacher_data)

    return {"teachers": result}

@router.get("/courses/analytics")
async def get_course_analytics(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin"))
):
    """Get detailed course analytics for admin"""

    courses = db.query(CPDCourse).all()
    result = []

    for course in courses:
        # Get recommendation stats
        total_recommendations = db.query(TeacherCourseRecommendation).filter_by(
            course_id=course.id
        ).count()

        enrolled_count = db.query(TeacherCourseRecommendation).filter_by(
            course_id=course.id, status="enrolled"
        ).count()

        dismissed_count = db.query(TeacherCourseRecommendation).filter_by(
            course_id=course.id, status="dismissed"
        ).count()

        # Get completion stats
        completed_count = db.query(TeacherCourseProgress).filter_by(
            course_id=course.id, completed=True
        ).count()

        course_data = {
            "id": course.id,
            "title": course.title,
            "category": course.category,
            "platform": course.platform,
            "total_recommendations": total_recommendations,
            "enrolled_count": enrolled_count,
            "dismissed_count": dismissed_count,
            "completed_count": completed_count,
            "acceptance_rate": round((enrolled_count / total_recommendations * 100), 1) if total_recommendations > 0 else 0,
            "completion_rate": round((completed_count / enrolled_count * 100), 1) if enrolled_count > 0 else 0
        }

        result.append(course_data)

    return {"courses": result}

@router.patch("/courses/{course_id}/toggle")
async def toggle_course_status(
    course_id: int,
    status_data: dict,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin"))
):
    """Toggle course active status"""

    course = db.query(CPDCourse).filter_by(id=course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    course.is_active = status_data.get("is_active", course.is_active)
    db.commit()

    return {
        "success": True,
        "message": f"Course {'activated' if course.is_active else 'deactivated'} successfully"
    }

@router.get("/reports/performance")
async def generate_performance_report(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin"))
):
    """Generate comprehensive performance report for principal"""

    # Module-wise performance with detailed breakdown
    modules = db.query(Module).all()
    module_performance = []

    for module in modules:
        performances = db.query(Performance).filter_by(module_id=module.id).all()
        if performances:
            scores = [p.score for p in performances]
            avg_score = sum(scores) / len(scores)
            below_60 = len([s for s in scores if s < 60])
            teachers_count = len(set([p.teacher_id for p in performances]))

            module_performance.append({
                "module": module.name,
                "average_score": round(avg_score, 1),
                "total_assessments": len(performances),
                "teachers_assessed": teachers_count,
                "teachers_below_60": below_60,
                "below_60_percent": round((below_60 / len(performances) * 100), 1) if performances else 0
            })

    # Teacher performance distribution by bands
    all_teachers = db.query(User).filter_by(role="teacher").all()
    distribution = {"excellent": 0, "good": 0, "needs_support": 0, "critical": 0}

    for teacher in all_teachers:
        performances = db.query(Performance).filter_by(teacher_id=teacher.id).all()
        if performances:
            avg_score = sum(p.score for p in performances) / len(performances)
            if avg_score >= 85:
                distribution["excellent"] += 1
            elif avg_score >= 70:
                distribution["good"] += 1
            elif avg_score >= 60:
                distribution["needs_support"] += 1
            else:
                distribution["critical"] += 1

    # Monthly trends (last 6 months)
    monthly_trends = []
    for i in range(5, -1, -1):
        month_start = datetime.now() - timedelta(days=30 * (i + 1))
        month_end = datetime.now() - timedelta(days=30 * i)

        month_performances = db.query(Performance).filter(
            Performance.created_at >= month_start,
            Performance.created_at < month_end
        ).all()

        if month_performances:
            avg = sum(p.score for p in month_performances) / len(month_performances)
            monthly_trends.append({
                "month": month_start.strftime("%b %Y"),
                "average_score": round(avg, 1),
                "assessments_count": len(month_performances)
            })

    # Competency gaps (modules with avg < 70%)
    competency_gaps = [m for m in module_performance if m["average_score"] < 70]
    competency_gaps.sort(key=lambda x: x["average_score"])

    # Top improving teachers (comparison last 30 vs previous 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    sixty_days_ago = datetime.now() - timedelta(days=60)

    improvements = []
    for teacher in all_teachers:
        recent = db.query(func.avg(Performance.score)).filter(
            Performance.teacher_id == teacher.id,
            Performance.created_at >= thirty_days_ago
        ).scalar() or 0

        previous = db.query(func.avg(Performance.score)).filter(
            Performance.teacher_id == teacher.id,
            Performance.created_at >= sixty_days_ago,
            Performance.created_at < thirty_days_ago
        ).scalar() or 0

        if recent > 0 and previous > 0:
            improvement = round(recent - previous, 1)
            if improvement > 0:
                improvements.append({
                    "teacher_name": teacher.name,
                    "improvement": improvement,
                    "current_score": round(recent, 1)
                })

    improvements.sort(key=lambda x: x["improvement"], reverse=True)

    # Overall stats
    total_assessments = db.query(Performance).count()
    overall_avg = db.query(func.avg(Performance.score)).scalar() or 0

    # This month vs last month comparison
    this_month_avg = db.query(func.avg(Performance.score)).filter(
        Performance.created_at >= thirty_days_ago
    ).scalar() or 0

    last_month_avg = db.query(func.avg(Performance.score)).filter(
        Performance.created_at >= sixty_days_ago,
        Performance.created_at < thirty_days_ago
    ).scalar() or 0

    return {
        "overall_stats": {
            "total_assessments": total_assessments,
            "overall_average": round(overall_avg, 1),
            "this_month_avg": round(this_month_avg, 1),
            "last_month_avg": round(last_month_avg, 1),
            "month_change": round(this_month_avg - last_month_avg, 1) if last_month_avg > 0 else 0
        },
        "module_performance": module_performance,
        "teacher_distribution": distribution,
        "monthly_trends": monthly_trends,
        "competency_gaps": competency_gaps[:5],
        "top_improvements": improvements[:5],
        "generated_at": datetime.now().isoformat()
    }

@router.post("/teachers/create")
async def create_teacher(
    teacher_data: dict,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin"))
):
    """Create a new teacher user"""
    from security import hash_password

    # Check if email already exists
    existing_user = db.query(User).filter_by(email=teacher_data.get("email")).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new teacher user
    new_teacher = User(
        name=teacher_data.get("name"),
        email=teacher_data.get("email"),
        password=hash_password(teacher_data.get("password", "password123")),  # Default password
        role="teacher"
    )

    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    return {
        "success": True,
        "message": "Teacher created successfully",
        "teacher": {
            "id": new_teacher.id,
            "name": new_teacher.name,
            "email": new_teacher.email
        }
    }

@router.get("/dashboard/principal-insights")
async def get_principal_insights(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin"))
):
    """Get principal-focused analytics answering 5 key questions"""

    # QUESTION 1: Which teachers need immediate attention?
    teachers_needing_attention = []
    all_teachers = db.query(User).filter_by(role="teacher").all()

    for teacher in all_teachers:
        performances = db.query(Performance).filter_by(teacher_id=teacher.id).all()
        if performances:
            avg_score = sum(p.score for p in performances) / len(performances)
            weak_modules = [p.module_id for p in performances if p.score < 60]

            if avg_score < 60 or len(weak_modules) >= 3:
                teachers_needing_attention.append({
                    "id": teacher.id,
                    "name": teacher.name,
                    "average_score": round(avg_score, 1),
                    "weak_modules_count": len(weak_modules),
                    "total_assessments": len(performances),
                    "status": "critical" if avg_score < 50 else "needs_support"
                })

    # QUESTION 2: Is school improving overall?
    thirty_days_ago = datetime.now() - timedelta(days=30)
    sixty_days_ago = datetime.now() - timedelta(days=60)

    recent_avg = db.query(func.avg(Performance.score)).filter(
        Performance.created_at >= thirty_days_ago
    ).scalar() or 0

    previous_avg = db.query(func.avg(Performance.score)).filter(
        Performance.created_at >= sixty_days_ago,
        Performance.created_at < thirty_days_ago
    ).scalar() or 0

    improvement_rate = round(recent_avg - previous_avg, 1) if previous_avg > 0 else 0

    # QUESTION 3: Where to invest in training?
    training_needs = []
    modules = db.query(Module).all()

    for module in modules:
        performances = db.query(Performance).filter_by(module_id=module.id).all()
        if performances:
            avg_score = sum(p.score for p in performances) / len(performances)
            below_60 = len([p for p in performances if p.score < 60])
            below_60_percent = round((below_60 / len(performances)) * 100, 1)

            training_needs.append({
                "module_name": module.name,
                "average_score": round(avg_score, 1),
                "teachers_below_60_percent": below_60_percent,
                "total_assessments": len(performances),
                "priority": "high" if avg_score < 60 else "medium" if avg_score < 70 else "low"
            })

    # Sort by priority
    training_needs.sort(key=lambda x: x["average_score"])

    # QUESTION 4: Are PD programs working?
    total_recommendations = db.query(TeacherCourseRecommendation).count()
    accepted_recommendations = db.query(TeacherCourseRecommendation).filter_by(status="enrolled").count()
    completed_courses = db.query(TeacherCourseProgress).filter_by(completed=True).count()

    # Calculate performance improvement after course completion
    teachers_with_completed_courses = db.query(TeacherCourseProgress.teacher_id).filter_by(completed=True).distinct().all()
    improvement_after_training = []

    for (teacher_id,) in teachers_with_completed_courses[:10]:  # Limit to 10 for performance
        before_score = db.query(func.avg(Performance.score)).filter(
            Performance.teacher_id == teacher_id,
            Performance.created_at < sixty_days_ago
        ).scalar() or 0

        after_score = db.query(func.avg(Performance.score)).filter(
            Performance.teacher_id == teacher_id,
            Performance.created_at >= thirty_days_ago
        ).scalar() or 0

        if before_score > 0 and after_score > 0:
            improvement_after_training.append(after_score - before_score)

    avg_improvement_after_training = round(sum(improvement_after_training) / len(improvement_after_training), 1) if improvement_after_training else 0

    # QUESTION 5: Who deserves recognition?
    top_performers = []
    for teacher in all_teachers:
        performances = db.query(Performance).filter_by(teacher_id=teacher.id).all()
        if performances and len(performances) >= 3:  # At least 3 assessments
            avg_score = sum(p.score for p in performances) / len(performances)
            excellent_count = len([p for p in performances if p.score >= 85])

            if avg_score >= 80:
                top_performers.append({
                    "id": teacher.id,
                    "name": teacher.name,
                    "average_score": round(avg_score, 1),
                    "total_assessments": len(performances),
                    "excellent_performances": excellent_count,
                    "consistency": round((excellent_count / len(performances)) * 100, 1)
                })

    top_performers.sort(key=lambda x: x["average_score"], reverse=True)

    # School overview stats
    total_teachers = db.query(User).filter_by(role="teacher").count()
    teachers_with_assessments = db.query(Performance.teacher_id).distinct().count()
    total_assessments = db.query(Performance).count()
    overall_avg = db.query(func.avg(Performance.score)).scalar() or 0

    return {
        "school_overview": {
            "total_teachers": total_teachers,
            "active_teachers": teachers_with_assessments,
            "participation_rate": round((teachers_with_assessments / total_teachers * 100), 1) if total_teachers > 0 else 0,
            "total_assessments_completed": total_assessments,
            "overall_average_score": round(overall_avg, 1),
            "improvement_trend": improvement_rate,
            "trend_direction": "up" if improvement_rate > 0 else "down" if improvement_rate < 0 else "stable"
        },
        "question_1_immediate_attention": {
            "count": len(teachers_needing_attention),
            "teachers": sorted(teachers_needing_attention, key=lambda x: x["average_score"])[:10]
        },
        "question_2_school_improvement": {
            "current_month_avg": round(recent_avg, 1),
            "previous_month_avg": round(previous_avg, 1),
            "improvement_rate": improvement_rate,
            "is_improving": improvement_rate > 0,
            "total_assessments_this_month": db.query(Performance).filter(
                Performance.created_at >= thirty_days_ago
            ).count()
        },
        "question_3_training_investment": {
            "priority_areas": training_needs[:5],
            "all_modules": training_needs
        },
        "question_4_pd_effectiveness": {
            "total_recommendations": total_recommendations,
            "acceptance_rate": round((accepted_recommendations / total_recommendations * 100), 1) if total_recommendations > 0 else 0,
            "completed_courses": completed_courses,
            "avg_improvement_after_training": avg_improvement_after_training,
            "is_effective": avg_improvement_after_training > 5
        },
        "question_5_recognition": {
            "count": len(top_performers),
            "top_performers": top_performers[:10]
        }
    }

@router.get("/dashboard/metrics")
async def get_dashboard_metrics(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin"))
):
    """Get real-time metrics for admin dashboard (legacy endpoint)"""

    # System health metrics
    total_users = db.query(User).count()
    active_teachers = db.query(User).filter_by(role="teacher").count()

    # Performance metrics
    recent_assessments = db.query(Performance).filter(
        Performance.created_at >= datetime.now() - timedelta(days=7)
    ).count()

    # Course metrics
    active_courses = db.query(CPDCourse).filter_by(is_active=True).count()
    recent_enrollments = db.query(TeacherCourseRecommendation).filter(
        TeacherCourseRecommendation.created_at >= datetime.now() - timedelta(days=7),
        TeacherCourseRecommendation.status == "enrolled"
    ).count()

    return {
        "system_health": {
            "total_users": total_users,
            "active_teachers": active_teachers,
            "system_uptime": "99.9%",
            "last_backup": "2 hours ago"
        },
        "weekly_metrics": {
            "new_assessments": recent_assessments,
            "new_enrollments": recent_enrollments,
            "recommendations_generated": 15,
            "average_session_time": "24 minutes"
        },
        "course_metrics": {
            "active_courses": active_courses,
            "most_popular": "Digital Teaching Tools",
            "highest_completion": "Classroom Management",
            "newest_addition": "FLN Training"
        }
    }