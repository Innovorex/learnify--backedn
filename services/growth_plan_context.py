"""
Comprehensive context collection for holistic growth plan generation
Aggregates data from ALL platform features
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from models import (
    User, TeacherProfile, Performance, Module,
    TeacherCareerEnrollment, CourseModule, ModuleProgress
)
from models_materials import TeachingMaterial
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json


class GrowthPlanContextCollector:
    """Collect comprehensive teacher context for AI growth plan generation"""

    def __init__(self, db: Session):
        self.db = db

    async def collect_full_context(self, teacher_id: int) -> Dict:
        """
        Aggregate ALL teacher data across platform
        Returns comprehensive context dictionary for AI prompt
        """
        context = {
            "teacher_profile": await self._get_teacher_profile(teacher_id),
            "cpd_performance": await self._get_cpd_performance(teacher_id),
            "career_progression": await self._get_career_status(teacher_id),
            "cpd_courses": await self._get_cpd_courses_activity(teacher_id),
            "ai_tutor": await self._get_ai_tutor_usage(teacher_id),
            "materials": await self._get_materials_activity(teacher_id),
            "k12_activity": await self._get_k12_teaching_activity(teacher_id),
            "improvement_trends": await self._get_improvement_trends(teacher_id),
            "platform_engagement": await self._get_engagement_metrics(teacher_id)
        }
        return context

    async def _get_teacher_profile(self, teacher_id: int) -> Dict:
        """Basic teacher profile information"""
        profile = self.db.query(TeacherProfile).filter_by(user_id=teacher_id).first()
        user = self.db.query(User).filter_by(id=teacher_id).first()

        if not profile or not user:
            return {}

        return {
            "name": user.name,
            "education": profile.education,
            "grades_teaching": profile.grades_teaching,
            "subjects_teaching": profile.subjects_teaching,
            "experience_years": profile.experience_years,
            "board": profile.board,
            "state": profile.state or "Telangana"
        }

    async def _get_cpd_performance(self, teacher_id: int) -> Dict:
        """CPD assessment performance data"""
        from services.analysis import collect_teacher_module_scores

        module_scores, type_avgs, overall = collect_teacher_module_scores(self.db, teacher_id)

        # Identify weak areas
        module_scores_sorted = sorted(module_scores, key=lambda m: m["score"])
        weak_modules = [m for m in module_scores_sorted[:3]]
        strong_modules = [m for m in module_scores_sorted[-3:]] if len(module_scores_sorted) >= 3 else []

        # Assessment type breakdown
        weak_types = sorted(type_avgs.items(), key=lambda kv: kv[1])[:2]

        return {
            "overall_score": overall,
            "module_scores": module_scores,
            "weak_modules": weak_modules,
            "strong_modules": strong_modules,
            "type_averages": type_avgs,
            "weak_assessment_types": [{"type": t, "avg": a} for t, a in weak_types]
        }

    async def _get_career_status(self, teacher_id: int) -> Dict:
        """Career progression enrollment and progress"""
        enrollments = self.db.query(TeacherCareerEnrollment).filter_by(
            teacher_id=teacher_id
        ).all()

        if not enrollments:
            return {
                "enrolled": False,
                "current_courses": [],
                "completion_rate": 0
            }

        career_data = []
        for enroll in enrollments:
            # Get module progress
            module_progress = self.db.query(ModuleProgress).filter_by(
                enrollment_id=enroll.id
            ).all()

            completed_modules = len([mp for mp in module_progress if mp.status == "completed"])
            total_modules = len(module_progress)

            pending_exams = [
                {
                    "module_id": mp.module_id,
                    "module_name": mp.module.module_name if mp.module else "Unknown",
                    "progress": (completed_modules / total_modules * 100) if total_modules > 0 else 0
                }
                for mp in module_progress if mp.status != "completed"
            ]

            career_data.append({
                "course_id": enroll.course_id,
                "course_name": enroll.course.course_name if enroll.course else "Unknown",
                "status": enroll.status,
                "modules_completed": completed_modules,
                "total_modules": total_modules,
                "completion_percentage": (completed_modules / total_modules * 100) if total_modules > 0 else 0,
                "pending_exams": pending_exams,
                "enrollment_date": enroll.enrollment_date.isoformat() if enroll.enrollment_date else None
            })

        return {
            "enrolled": True,
            "current_courses": career_data,
            "total_enrollments": len(enrollments),
            "completion_rate": sum(c["completion_percentage"] for c in career_data) / len(career_data) if career_data else 0
        }

    async def _get_cpd_courses_activity(self, teacher_id: int) -> Dict:
        """CPD course recommendations and enrollments"""
        # Placeholder - can be enhanced when CPD courses feature is implemented
        return {
            "enrolled_courses": [],
            "completed_courses": 0,
            "in_progress_courses": 0,
            "recommended_courses": []
        }

    async def _get_ai_tutor_usage(self, teacher_id: int) -> Dict:
        """AI Tutor session history and patterns"""
        # Placeholder - query ai_tutor_sessions table if exists
        return {
            "total_sessions": 0,
            "topics_explored": [],
            "avg_session_length_minutes": 0,
            "last_session_date": None,
            "frequently_asked_topics": []
        }

    async def _get_materials_activity(self, teacher_id: int) -> Dict:
        """Teaching materials upload activity"""
        materials = self.db.query(TeachingMaterial).filter_by(
            teacher_id=teacher_id
        ).all()

        subjects_covered = list(set(m.subject for m in materials if hasattr(m, 'subject') and m.subject))
        grades_covered = list(set(m.grade for m in materials if hasattr(m, 'grade') and m.grade))

        last_upload = max((m.uploaded_at for m in materials if hasattr(m, 'uploaded_at')), default=None)

        return {
            "total_uploaded": len(materials),
            "subjects_covered": subjects_covered,
            "grades_covered": grades_covered,
            "last_upload_date": last_upload.isoformat() if last_upload else None
        }

    async def _get_k12_teaching_activity(self, teacher_id: int) -> Dict:
        """K-12 assessment creation and student interaction"""
        # Placeholder - depends on your k12 models
        return {
            "assessments_created": 0,
            "students_assessed": 0,
            "active_in_last_30_days": False
        }

    async def _get_improvement_trends(self, teacher_id: int) -> Dict:
        """Historical performance trends"""
        from models import PerformanceHistory

        # Get last 90 days of performance history
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)
        history = self.db.query(PerformanceHistory).filter(
            PerformanceHistory.teacher_id == teacher_id,
            PerformanceHistory.created_at >= ninety_days_ago
        ).order_by(PerformanceHistory.created_at.asc()).all()

        if not history or len(history) < 2:
            return {
                "trend": "insufficient_data",
                "improvement_velocity": 0,
                "stagnant_modules": [],
                "recent_scores": []
            }

        # Calculate trend
        scores = [float(h.score) for h in history]

        # Simple linear trend
        first_half_avg = sum(scores[:len(scores)//2]) / (len(scores)//2)
        second_half_avg = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)

        if second_half_avg > first_half_avg + 5:
            trend = "improving"
        elif second_half_avg < first_half_avg - 5:
            trend = "declining"
        else:
            trend = "stable"

        velocity = ((second_half_avg - first_half_avg) / 90) * 30  # Per month

        return {
            "trend": trend,
            "improvement_velocity": round(velocity, 2),
            "stagnant_modules": [],  # TODO: Identify modules with no improvement
            "recent_scores": scores[-10:] if len(scores) > 10 else scores
        }

    async def _get_engagement_metrics(self, teacher_id: int) -> Dict:
        """Platform engagement statistics"""
        # Placeholder for engagement tracking
        return {
            "days_active_last_30": 0,
            "features_used": [],
            "avg_session_length_minutes": 0
        }
