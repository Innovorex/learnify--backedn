# services/tracking.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import PerformanceHistory, Performance, Module, User, TeacherProfile
from datetime import datetime

def log_performance_history(db: Session, teacher_id: int, module_id: int, score: float, rating: str):
    """Log a performance snapshot to history for timeline tracking"""
    hist = PerformanceHistory(teacher_id=teacher_id, module_id=module_id, score=score, rating=rating)
    db.add(hist)
    db.commit()

def get_teacher_progress(db: Session, teacher_id: int):
    """Return chronological timeline per module for a teacher"""
    rows = (db.query(PerformanceHistory, Module)
              .join(Module, PerformanceHistory.module_id == Module.id)
              .filter(PerformanceHistory.teacher_id == teacher_id)
              .order_by(PerformanceHistory.created_at.asc())
              .all())

    timeline = []
    for ph, mod in rows:
        timeline.append({
            "module_id": mod.id,
            "module_name": mod.name,
            "assessment_type": mod.assessment_type,
            "score": ph.score,
            "rating": ph.rating,
            "date": ph.created_at.isoformat(),
            "timestamp": ph.created_at.timestamp()
        })
    return timeline

def get_teacher_module_trend(db: Session, teacher_id: int, module_id: int):
    """Get score trend for a specific teacher and module"""
    history = (db.query(PerformanceHistory)
              .filter(PerformanceHistory.teacher_id == teacher_id,
                     PerformanceHistory.module_id == module_id)
              .order_by(PerformanceHistory.created_at.asc())
              .all())

    return [{
        "score": h.score,
        "rating": h.rating,
        "date": h.created_at.isoformat(),
        "timestamp": h.created_at.timestamp()
    } for h in history]

def get_admin_overview(db: Session):
    """High-level report: avg per module, distribution of ratings, compliance stats"""
    modules = db.query(Module).all()
    module_stats = []

    for mod in modules:
        # Average score for this module
        avg = db.query(func.avg(Performance.score)).filter(Performance.module_id == mod.id).scalar() or 0.0

        # Count of teachers who completed this module
        completed = db.query(func.count(Performance.id)).filter(Performance.module_id == mod.id).scalar() or 0

        # Rating distribution for this module
        ratings = db.query(Performance.rating, func.count(Performance.id)).filter(Performance.module_id == mod.id).group_by(Performance.rating).all()
        rating_dist = {r: c for r, c in ratings}

        module_stats.append({
            "module_id": mod.id,
            "module_name": mod.name,
            "assessment_type": mod.assessment_type,
            "avg_score": round(float(avg), 2),
            "completed_count": completed,
            "rating_distribution": rating_dist
        })

    # Overall rating distribution across all modules
    overall_ratings = db.query(Performance.rating, func.count(Performance.id)).group_by(Performance.rating).all()
    overall_rating_dist = {r: c for r, c in overall_ratings}

    # Board-wise performance
    board_stats = get_board_wise_stats(db)

    # NEP 2020 compliance metrics
    nep_compliance = get_nep_compliance_stats(db)

    return {
        "module_statistics": module_stats,
        "overall_rating_distribution": overall_rating_dist,
        "board_wise_performance": board_stats,
        "nep_2020_compliance": nep_compliance,
        "total_teachers": db.query(func.count(User.id)).filter(User.role == "teacher").scalar() or 0,
        "total_assessments": db.query(func.count(Performance.id)).scalar() or 0
    }

def get_board_wise_stats(db: Session):
    """Get performance statistics grouped by educational board"""
    # Join Performance -> User -> TeacherProfile to get board info
    board_stats = (db.query(TeacherProfile.board,
                           func.avg(Performance.score).label('avg_score'),
                           func.count(Performance.id).label('assessment_count'))
                  .join(User, TeacherProfile.user_id == User.id)
                  .join(Performance, Performance.teacher_id == User.id)
                  .group_by(TeacherProfile.board)
                  .all())

    return [{
        "board": board,
        "avg_score": round(float(avg_score or 0), 2),
        "assessment_count": assessment_count
    } for board, avg_score, assessment_count in board_stats]

def get_nep_compliance_stats(db: Session):
    """Calculate NEP 2020 compliance metrics"""
    total_teachers = db.query(func.count(User.id)).filter(User.role == "teacher").scalar() or 0

    # Teachers who completed at least one assessment
    active_teachers = db.query(func.count(func.distinct(Performance.teacher_id))).scalar() or 0

    # Module completion rates
    modules = db.query(Module).all()
    module_completion = []
    for mod in modules:
        completed = db.query(func.count(Performance.id)).filter(Performance.module_id == mod.id).scalar() or 0
        completion_rate = (completed / total_teachers * 100) if total_teachers > 0 else 0
        module_completion.append({
            "module_name": mod.name,
            "completion_count": completed,
            "completion_rate": round(completion_rate, 2)
        })

    # Overall compliance score (teachers with all modules completed)
    teachers_with_all_modules = 0
    if modules:
        required_modules = len(modules)
        for teacher_id in db.query(User.id).filter(User.role == "teacher").all():
            completed_modules = db.query(func.count(Performance.id)).filter(Performance.teacher_id == teacher_id[0]).scalar() or 0
            if completed_modules >= required_modules:
                teachers_with_all_modules += 1

    overall_compliance = (teachers_with_all_modules / total_teachers * 100) if total_teachers > 0 else 0

    return {
        "total_teachers": total_teachers,
        "active_teachers": active_teachers,
        "participation_rate": round((active_teachers / total_teachers * 100), 2) if total_teachers > 0 else 0,
        "module_completion_rates": module_completion,
        "overall_compliance_rate": round(overall_compliance, 2),
        "teachers_fully_compliant": teachers_with_all_modules
    }

def get_export_data(db: Session, report_type: str = "overview"):
    """Get data formatted for CSV/Excel export"""
    if report_type == "overview":
        overview = get_admin_overview(db)
        return {
            "module_stats": overview["module_statistics"],
            "rating_distribution": overview["overall_rating_distribution"],
            "board_performance": overview["board_wise_performance"],
            "compliance": overview["nep_2020_compliance"]
        }
    elif report_type == "detailed":
        # Detailed teacher-wise report
        teachers = (db.query(User, TeacherProfile)
                   .join(TeacherProfile, User.id == TeacherProfile.user_id)
                   .filter(User.role == "teacher")
                   .all())

        detailed_data = []
        for user, profile in teachers:
            performances = db.query(Performance, Module).join(Module, Performance.module_id == Module.id).filter(Performance.teacher_id == user.id).all()

            for perf, module in performances:
                detailed_data.append({
                    "teacher_id": user.id,
                    "teacher_name": user.name,
                    "teacher_email": user.email,
                    "education": profile.education,
                    "grades_teaching": profile.grades_teaching,
                    "subjects_teaching": profile.subjects_teaching,
                    "experience_years": profile.experience_years,
                    "board": profile.board,
                    "module_name": module.name,
                    "assessment_type": module.assessment_type,
                    "score": perf.score,
                    "rating": perf.rating,
                    "completed_date": perf.created_at.isoformat()
                })

        return {"detailed_records": detailed_data}

    return {}