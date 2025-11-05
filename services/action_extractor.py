"""
Action Extractor Service
Parses growth plan content and extracts actionable items
Maps actions to platform resources (modules, courses, etc.)
"""
from sqlalchemy.orm import Session
from typing import Dict, List
import re
from datetime import datetime, timedelta


class ActionExtractor:
    """Extract and structure actionable items from growth plan text"""

    def __init__(self, db: Session):
        self.db = db

    async def extract_actions(self, growth_plan_content: str, context: Dict, growth_plan_id: int) -> List[Dict]:
        """
        Parse growth plan and extract structured actions
        Returns list of action dictionaries ready for database insertion
        """
        actions = []

        # Extract from CPD performance context
        cpd_actions = await self._extract_cpd_retake_actions(context)
        actions.extend(cpd_actions)

        # Extract from career progression context
        career_actions = await self._extract_career_actions(context)
        actions.extend(career_actions)

        # Extract from AI Tutor suggestions
        ai_tutor_actions = await self._extract_ai_tutor_actions(context, growth_plan_content)
        actions.extend(ai_tutor_actions)

        # Extract material creation actions
        material_actions = await self._extract_material_actions(context, growth_plan_content)
        actions.extend(material_actions)

        # Extract CPD course enrollments from text
        cpd_course_actions = await self._extract_cpd_course_actions(growth_plan_content)
        actions.extend(cpd_course_actions)

        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        actions.sort(key=lambda x: priority_order.get(x.get("priority", "medium"), 1))

        # Add display order
        for idx, action in enumerate(actions):
            action["display_order"] = idx

        return actions

    async def _extract_cpd_retake_actions(self, context: Dict) -> List[Dict]:
        """Extract actions for retaking weak CPD modules"""
        actions = []
        cpd = context.get("cpd_performance", {})
        weak_modules = cpd.get("weak_modules", [])

        for module in weak_modules[:3]:  # Top 3 weak modules
            if module["score"] < 70:  # Below good performance
                priority = "high" if module["score"] < 50 else "medium"

                actions.append({
                    "action_type": "retake_cpd_module",
                    "action_title": f"Retake: {module['module_name']}",
                    "action_description": f"Current score: {module['score']:.0f}%. Target: 80%+. Focus on improving your understanding in this area.",
                    "priority": priority,
                    "target_cpd_module_id": module["module_id"],
                    "target_date": datetime.utcnow() + timedelta(days=14),
                    "estimated_time_minutes": 60
                })

        return actions

    async def _extract_career_actions(self, context: Dict) -> List[Dict]:
        """Extract actions from career progression status"""
        actions = []
        career = context.get("career_progression", {})

        if not career.get("enrolled"):
            return actions

        for course in career.get("current_courses", []):
            pending_exams = course.get("pending_exams", [])

            for exam in pending_exams[:2]:  # Top 2 pending exams
                actions.append({
                    "action_type": "complete_career_module",
                    "action_title": f"Complete: {exam['module_name']} Exam",
                    "action_description": f"Progress: {exam['progress']:.0f}%. Complete module materials and take the exam.",
                    "priority": "high",
                    "target_career_module_id": exam["module_id"],
                    "target_date": datetime.utcnow() + timedelta(days=21),
                    "estimated_time_minutes": 120
                })

        return actions

    async def _extract_ai_tutor_actions(self, context: Dict, content: str) -> List[Dict]:
        """Extract AI Tutor usage recommendations"""
        actions = []
        cpd = context.get("cpd_performance", {})
        weak_modules = cpd.get("weak_modules", [])

        # If AI Tutor is mentioned in content or weak areas exist
        if weak_modules and (len(weak_modules) > 0):
            # Suggest AI Tutor for weakest area
            weakest = weak_modules[0] if weak_modules else {}

            if weakest:
                actions.append({
                    "action_type": "use_ai_tutor",
                    "action_title": f"Explore: {weakest['module_name']} with AI Tutor",
                    "action_description": "Get personalized guidance and clarifications on challenging topics using our AI Tutor.",
                    "priority": "medium",
                    "target_date": datetime.utcnow() + timedelta(days=7),
                    "estimated_time_minutes": 30
                })

        return actions

    async def _extract_material_actions(self, context: Dict, content: str) -> List[Dict]:
        """Extract material creation/upload actions"""
        actions = []
        materials = context.get("materials", {})
        profile = context.get("teacher_profile", {})

        # If low material uploads, suggest creating materials
        if materials.get("total_uploaded", 0) < 3:
            subjects = profile.get("subjects_teaching", "your subject")

            actions.append({
                "action_type": "upload_material",
                "action_title": f"Upload Teaching Materials for {subjects}",
                "action_description": "Share your lesson plans, worksheets, or resources to help yourself and the teaching community.",
                "priority": "low",
                "target_date": datetime.utcnow() + timedelta(days=30),
                "estimated_time_minutes": 45
            })

        return actions

    async def _extract_cpd_course_actions(self, content: str) -> List[Dict]:
        """Extract CPD course enrollment actions from text"""
        actions = []

        # Look for common patterns of course recommendations
        # Pattern: "enroll in", "take course", "complete training", followed by course name
        patterns = [
            r'enroll\s+in\s+([A-Z][A-Za-z\s:&-]+(?:course|training|program))',
            r'complete\s+(?:the\s+)?([A-Z][A-Za-z\s:&-]+(?:course|training))',
            r'take\s+(?:the\s+)?([A-Z][A-Za-z\s:&-]+(?:course|training))'
        ]

        found_courses = set()
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            found_courses.update(matches)

        # Create actions for unique courses found
        for course_name in list(found_courses)[:3]:  # Limit to 3
            # Check if it's a DIKSHA/SWAYAM/NCERT resource
            platform = "DIKSHA" if "diksha" in content.lower() else \
                      "SWAYAM" if "swayam" in content.lower() else \
                      "NCERT" if "ncert" in content.lower() else "Online Platform"

            actions.append({
                "action_type": "enroll_cpd_course",
                "action_title": f"Enroll: {course_name.strip()}",
                "action_description": f"Free professional development course available on {platform}.",
                "priority": "medium",
                "external_url": f"https://diksha.gov.in/",  # Default to DIKSHA
                "target_date": datetime.utcnow() + timedelta(days=10),
                "estimated_time_minutes": 180
            })

        return actions
