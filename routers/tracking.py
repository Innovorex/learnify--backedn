# routers/tracking.py
import csv
import io
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import get_db
from models import User
from security import require_role
from services.tracking import (
    get_teacher_progress,
    get_teacher_module_trend,
    get_admin_overview,
    get_export_data
)

router = APIRouter(prefix="/tracking", tags=["tracking"])

# ========== TEACHER ENDPOINTS ==========

@router.get("/teacher/me/progress")
def my_progress(db: Session = Depends(get_db), user: User = Depends(require_role("teacher"))):
    """Get teacher's progress timeline across all modules"""
    timeline = get_teacher_progress(db, user.id)
    return {
        "teacher_id": user.id,
        "teacher_name": user.name,
        "timeline": timeline,
        "total_assessments": len(timeline)
    }

@router.get("/teacher/me/module/{module_id}/trend")
def my_module_trend(module_id: int, db: Session = Depends(get_db), user: User = Depends(require_role("teacher"))):
    """Get score trend for a specific module"""
    trend = get_teacher_module_trend(db, user.id, module_id)
    return {
        "teacher_id": user.id,
        "module_id": module_id,
        "trend": trend,
        "attempts": len(trend)
    }

# ========== ADMIN ENDPOINTS ==========

@router.get("/admin/overview")
def admin_overview(db: Session = Depends(get_db), admin: User = Depends(require_role("admin"))):
    """Get comprehensive admin dashboard overview"""
    return get_admin_overview(db)

@router.get("/admin/teacher/{teacher_id}/progress")
def admin_teacher_progress(teacher_id: int,
                          db: Session = Depends(get_db),
                          admin: User = Depends(require_role("admin"))):
    """Get any teacher's progress timeline (admin view)"""
    timeline = get_teacher_progress(db, teacher_id)
    teacher = db.query(User).filter_by(id=teacher_id).first()
    teacher_name = teacher.name if teacher else f"Teacher {teacher_id}"

    return {
        "teacher_id": teacher_id,
        "teacher_name": teacher_name,
        "timeline": timeline,
        "total_assessments": len(timeline)
    }

# ========== EXPORT ENDPOINTS ==========

@router.get("/admin/export/csv")
def export_csv_overview(db: Session = Depends(get_db),
                       admin: User = Depends(require_role("admin"))):
    """Export overview report as CSV"""
    data = get_export_data(db, "overview")

    output = io.StringIO()
    writer = csv.writer(output)

    # Module Statistics
    writer.writerow(["=== MODULE STATISTICS ==="])
    writer.writerow(["Module Name", "Assessment Type", "Average Score", "Completed Count", "Excellent", "Good", "Needs Improvement"])

    for module in data["module_stats"]:
        ratings = module["rating_distribution"]
        writer.writerow([
            module["module_name"],
            module["assessment_type"],
            module["avg_score"],
            module["completed_count"],
            ratings.get("Excellent", 0),
            ratings.get("Good", 0),
            ratings.get("Needs Improvement", 0)
        ])

    # Board Performance
    writer.writerow([])
    writer.writerow(["=== BOARD-WISE PERFORMANCE ==="])
    writer.writerow(["Board", "Average Score", "Assessment Count"])

    for board in data["board_performance"]:
        writer.writerow([
            board["board"],
            board["avg_score"],
            board["assessment_count"]
        ])

    # NEP 2020 Compliance
    writer.writerow([])
    writer.writerow(["=== NEP 2020 COMPLIANCE ==="])
    writer.writerow(["Metric", "Value"])
    compliance = data["compliance"]
    writer.writerow(["Total Teachers", compliance["total_teachers"]])
    writer.writerow(["Active Teachers", compliance["active_teachers"]])
    writer.writerow(["Participation Rate %", compliance["participation_rate"]])
    writer.writerow(["Overall Compliance Rate %", compliance["overall_compliance_rate"]])
    writer.writerow(["Teachers Fully Compliant", compliance["teachers_fully_compliant"]])

    # Module Completion Rates
    writer.writerow([])
    writer.writerow(["=== MODULE COMPLETION RATES ==="])
    writer.writerow(["Module Name", "Completion Count", "Completion Rate %"])

    for module_comp in compliance["module_completion_rates"]:
        writer.writerow([
            module_comp["module_name"],
            module_comp["completion_count"],
            module_comp["completion_rate"]
        ])

    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=teacher_evaluation_overview.csv"}
    )

@router.get("/admin/export/detailed-csv")
def export_detailed_csv(db: Session = Depends(get_db),
                       admin: User = Depends(require_role("admin"))):
    """Export detailed teacher-wise report as CSV"""
    data = get_export_data(db, "detailed")

    output = io.StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow([
        "Teacher ID", "Teacher Name", "Email", "Education", "Grades Teaching",
        "Subjects Teaching", "Experience Years", "Board", "Module Name",
        "Assessment Type", "Score", "Rating", "Completed Date"
    ])

    # Data rows
    for record in data["detailed_records"]:
        writer.writerow([
            record["teacher_id"],
            record["teacher_name"],
            record["teacher_email"],
            record["education"],
            record["grades_teaching"],
            record["subjects_teaching"],
            record["experience_years"],
            record["board"],
            record["module_name"],
            record["assessment_type"],
            record["score"],
            record["rating"],
            record["completed_date"]
        ])

    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=teacher_evaluation_detailed.csv"}
    )

@router.get("/admin/export/module-csv/{module_id}")
def export_module_csv(module_id: int,
                     db: Session = Depends(get_db),
                     admin: User = Depends(require_role("admin"))):
    """Export performance data for a specific module"""
    from models import Performance, Module, User, TeacherProfile

    # Get module info
    module = db.query(Module).filter_by(id=module_id).first()
    if not module:
        return {"error": "Module not found"}

    # Get all performances for this module
    performances = (db.query(Performance, User, TeacherProfile)
                   .join(User, Performance.teacher_id == User.id)
                   .join(TeacherProfile, User.id == TeacherProfile.user_id)
                   .filter(Performance.module_id == module_id)
                   .all())

    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([f"Module: {module.name} ({module.assessment_type})"])
    writer.writerow([])
    writer.writerow([
        "Teacher ID", "Teacher Name", "Email", "Board", "Grades", "Subjects",
        "Experience", "Score", "Rating", "Completed Date"
    ])

    # Data
    for perf, user, profile in performances:
        writer.writerow([
            user.id,
            user.name,
            user.email,
            profile.board,
            profile.grades_teaching,
            profile.subjects_teaching,
            profile.experience_years,
            perf.score,
            perf.rating,
            perf.created_at.isoformat()
        ])

    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=module_{module_id}_{module.name.replace(' ', '_')}.csv"}
    )

# ========== ANALYTICS ENDPOINTS ==========

@router.get("/admin/analytics/trends")
def admin_analytics_trends(days: int = Query(30, description="Number of days to analyze"),
                          db: Session = Depends(get_db),
                          admin: User = Depends(require_role("admin"))):
    """Get trend analytics for the admin dashboard"""
    from datetime import datetime, timedelta
    from models import PerformanceHistory

    # Get performance history for the last N days
    cutoff_date = datetime.now() - timedelta(days=days)

    recent_history = (db.query(PerformanceHistory, User)
                     .join(User, PerformanceHistory.teacher_id == User.id)
                     .filter(PerformanceHistory.created_at >= cutoff_date)
                     .order_by(PerformanceHistory.created_at.asc())
                     .all())

    # Group by date for trend analysis
    daily_stats = {}
    for hist, user in recent_history:
        date_key = hist.created_at.date().isoformat()
        if date_key not in daily_stats:
            daily_stats[date_key] = {
                "date": date_key,
                "assessments_completed": 0,
                "avg_score": 0,
                "scores": []
            }
        daily_stats[date_key]["assessments_completed"] += 1
        daily_stats[date_key]["scores"].append(hist.score)

    # Calculate averages
    trend_data = []
    for date_key, stats in daily_stats.items():
        avg_score = sum(stats["scores"]) / len(stats["scores"]) if stats["scores"] else 0
        trend_data.append({
            "date": stats["date"],
            "assessments_completed": stats["assessments_completed"],
            "avg_score": round(avg_score, 2)
        })

    trend_data.sort(key=lambda x: x["date"])

    return {
        "period_days": days,
        "trend_data": trend_data,
        "total_assessments": sum(d["assessments_completed"] for d in trend_data),
        "period_avg_score": round(sum(d["avg_score"] for d in trend_data) / len(trend_data), 2) if trend_data else 0
    }