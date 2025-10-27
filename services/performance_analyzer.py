"""
Performance Trend Analyzer
Analyzes teacher performance trends to provide intelligent course recommendations
"""
from typing import Dict, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc
from models import Performance, PerformanceHistory, Module


class PerformanceAnalyzer:
    """Analyzes teacher performance trends over time"""

    def __init__(self, db: Session, teacher_id: int):
        self.db = db
        self.teacher_id = teacher_id

    def analyze_trends(self) -> Dict[str, Dict]:
        """
        Analyze performance trends for all modules

        Returns:
            {
                "module_name": {
                    "current_score": 45,
                    "previous_score": 60,
                    "trend": "declined",  # declined/stagnant/improved
                    "change_percentage": -15,
                    "priority": "urgent",  # urgent/high/medium/low
                    "recommended_difficulty": "beginner"  # beginner/intermediate/advanced
                }
            }
        """
        # Get current performance for all modules
        current_performances = self.db.query(Performance, Module).join(Module).filter(
            Performance.teacher_id == self.teacher_id
        ).all()

        trends = {}

        for perf, module in current_performances:
            # Get last 3 historical records for this module
            history = self.db.query(PerformanceHistory).filter(
                PerformanceHistory.teacher_id == self.teacher_id,
                PerformanceHistory.module_id == module.id
            ).order_by(desc(PerformanceHistory.created_at)).limit(3).all()

            current_score = perf.score

            # Calculate trend
            if len(history) >= 2:
                # Compare current with previous
                previous_score = history[1].score  # Second most recent (history[0] is current)
                change = current_score - previous_score
                change_percentage = (change / previous_score * 100) if previous_score > 0 else 0

                # Determine trend
                if change_percentage < -5:
                    trend = "declined"
                elif change_percentage > 5:
                    trend = "improved"
                else:
                    trend = "stagnant"
            else:
                # No history, use current score to determine need
                previous_score = current_score
                change_percentage = 0
                trend = "new"

            # Determine priority based on score and trend
            priority = self._determine_priority(current_score, trend)

            # Determine recommended difficulty level
            recommended_difficulty = self._determine_difficulty(current_score, trend)

            trends[module.name] = {
                "module_id": module.id,
                "current_score": current_score,
                "previous_score": previous_score,
                "trend": trend,
                "change_percentage": round(change_percentage, 1),
                "priority": priority,
                "recommended_difficulty": recommended_difficulty,
                "rating": perf.rating
            }

        return trends

    def _determine_priority(self, score: float, trend: str) -> str:
        """Determine recommendation priority based on score and trend"""

        # Declining scores are always urgent
        if trend == "declined":
            if score < 50:
                return "urgent"  # Declining AND low score
            else:
                return "high"    # Declining but still acceptable

        # Low scores need attention
        if score < 50:
            return "urgent"
        elif score < 60:
            return "high"

        # Stagnant weak areas
        if trend == "stagnant" and score < 70:
            return "high"

        # Improving areas - encourage growth
        if trend == "improved":
            return "medium"

        # Strong areas
        if score >= 80:
            return "low"

        return "medium"

    def _determine_difficulty(self, score: float, trend: str) -> str:
        """Determine appropriate course difficulty level"""

        # Declining scores need foundational refresh
        if trend == "declined":
            if score < 50:
                return "Beginner"
            else:
                return "Intermediate"

        # Score-based difficulty
        if score < 50:
            return "Beginner"
        elif score < 70:
            return "Intermediate"
        else:
            return "Advanced"

    def get_priority_areas(self, max_areas: int = 3) -> List[Tuple[str, Dict]]:
        """
        Get top priority areas for course recommendations

        Args:
            max_areas: Maximum number of areas to return (default: 3)

        Returns:
            List of (module_name, trend_data) sorted by priority
        """
        trends = self.analyze_trends()

        # Priority order: urgent > high > medium > low
        priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}

        # Sort by priority, then by current score (lower first)
        sorted_areas = sorted(
            trends.items(),
            key=lambda x: (priority_order.get(x[1]["priority"], 4), x[1]["current_score"])
        )

        return sorted_areas[:max_areas]

    def get_focus_message(self, module_name: str, trend_data: Dict) -> str:
        """Generate a personalized message explaining why this course is recommended"""

        score = trend_data["current_score"]
        trend = trend_data["trend"]
        change = trend_data["change_percentage"]

        if trend == "declined":
            return f"⚠️ Your {module_name} score declined by {abs(change):.0f}% - this course addresses foundational concepts to help you recover"

        elif trend == "stagnant" and score < 60:
            return f"→ Your {module_name} score has been stagnant at {score:.0f}% - try a different teaching approach with this course"

        elif trend == "improved":
            return f"✅ Great progress! You improved {change:.0f}% in {module_name} - this advanced course builds on your success"

        elif score < 50:
            return f"🎯 {module_name} needs immediate attention (current: {score:.0f}%) - this beginner course covers the essentials"

        elif score < 70:
            return f"📈 Strengthen your {module_name} skills (current: {score:.0f}%) - this course targets your specific gaps"

        else:
            return f"🌟 You're doing well in {module_name} ({score:.0f}%) - this advanced course helps you excel further"

    def has_enrolled_recently(self, course_id: int) -> bool:
        """Check if teacher enrolled in a course recently"""
        from models_cpd import TeacherCourseProgress

        progress = self.db.query(TeacherCourseProgress).filter(
            TeacherCourseProgress.teacher_id == self.teacher_id,
            TeacherCourseProgress.course_id == course_id
        ).first()

        return progress is not None
