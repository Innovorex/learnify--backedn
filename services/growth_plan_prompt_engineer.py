"""
Advanced prompt engineering for growth plan generation
Transforms comprehensive context into structured AI prompts
"""
from typing import Dict, List
import json


class GrowthPlanPromptEngineer:
    """Engineer optimized prompts for growth plan AI generation"""

    def __init__(self, model_name: str = "wizardlm-2-8x22b"):
        self.model_name = model_name
        self.max_tokens = 4000

    def build_holistic_prompt(self, context: Dict, focus_areas: List[str] = None) -> str:
        """
        Build comprehensive prompt using full teacher context
        Uses Chain-of-Thought prompting for better results
        """

        profile = context.get("teacher_profile", {})
        cpd = context.get("cpd_performance", {})
        career = context.get("career_progression", {})
        trends = context.get("improvement_trends", {})

        # Extract key insights
        weak_modules = [m["module_name"] for m in cpd.get("weak_modules", [])[:3]]
        strong_modules = [m["module_name"] for m in cpd.get("strong_modules", [])[:3]]

        if focus_areas:
            weak_modules = focus_areas + weak_modules

        prompt = f"""You are an expert Indian education consultant and instructional coach with 20+ years of experience in teacher professional development. You specialize in creating personalized, actionable growth plans.

TEACHER PROFILE ANALYSIS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: {profile.get('name', 'Teacher')}
Education: {profile.get('education', 'N/A')}
Teaching: {profile.get('grades_teaching', 'N/A')} | {profile.get('subjects_teaching', 'N/A')}
Experience: {profile.get('experience_years', 0)} years
Board: {profile.get('board', 'N/A')}
State: {profile.get('state', 'N/A')}

CURRENT PERFORMANCE ASSESSMENT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall CPD Score: {cpd.get('overall_score', 0):.1f}/100
Performance Trend: {trends.get('trend', 'unknown').upper()}
Monthly Improvement Rate: {trends.get('improvement_velocity', 0):+.1f} points/month

Strengths (Strong Modules):
{self._format_list(strong_modules)}

Areas Needing Attention (Weak Modules):
{self._format_list(weak_modules)}

Weak Assessment Types:
{self._format_assessment_types(cpd.get('weak_assessment_types', []))}

CAREER PROGRESSION STATUS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{self._format_career_status(career)}

PLATFORM ENGAGEMENT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{self._format_engagement(context)}

TASK:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Create a comprehensive, actionable 30-day professional growth plan following this EXACT structure:

## Executive Summary
2-3 sentences summarizing current status, key challenges, and primary improvement goals.

## Priority Focus Areas (Top 3)
For each area:
- **Area Name**: Brief description
- **Current Status**: Specific score/metric
- **Target Goal**: Specific, measurable target
- **Why This Matters**: Impact on teaching effectiveness

## Week 1: Assessment & Foundation (Days 1-7)
### Goals:
- [3 specific, measurable goals]

### Daily Action Items:
- **Day 1**: [Specific actionable task with deliverable]
- **Day 2**: [Specific actionable task with deliverable]
- **Day 3-7**: [Continue with specific daily tasks]

## Week 2: Skill Development (Days 8-14)
### Goals:
- [3 specific goals focused on {weak_modules[0] if weak_modules else 'teaching skills'}]

### Daily Action Items:
- **Day 8-14**: [Seven specific skill-building tasks]

## Week 3: Implementation & Practice (Days 15-21)
### Goals:
- [3 goals for applying new strategies]

### Daily Action Items:
- **Day 15-21**: [Seven implementation tasks]

## Week 4: Evaluation & Mastery (Days 22-30)
### Goals:
- [3 goals for assessment and refinement]

### Daily Action Items:
- **Day 22-30**: [Nine evaluation and consolidation tasks]

## Recommended Free Resources
Provide 5 specific, actionable resources:
1. **[Resource Name]** - [Platform] - [Link/Access Method]
   - What it covers: [Specific topics]
   - Time commitment: [Duration]
   - Best for: [Which weak area it addresses]

## {profile.get('board', 'CBSE')} Board Specific Strategies
3 board-specific strategies for {profile.get('grades_teaching', 'Grade 6-8')} {profile.get('subjects_teaching', 'teaching')}

## Success Metrics & Tracking
Define 3 specific, measurable outcomes:
1. **[Metric Name]**: Baseline → Target | How to measure
2. **[Metric Name]**: Baseline → Target | How to measure
3. **[Metric Name]**: Baseline → Target | How to measure

IMPORTANT GUIDELINES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Every action item must be SPECIFIC and ACTIONABLE (avoid vague advice)
✓ Prioritize addressing: {', '.join(weak_modules[:2]) if weak_modules else 'general teaching skills'}
✓ Reference {profile.get('board', 'CBSE')} curriculum explicitly
✓ Include time estimates for tasks (e.g., "30 minutes")
✓ Provide concrete examples for {profile.get('subjects_teaching', 'subjects')}
✓ Balance professional development with practical classroom application
✓ Consider teacher's {profile.get('experience_years', 0)} years of experience level
✓ Use Indian context and NCERT/DIKSHA/SWAYAM resources

Generate the plan now:"""

        return prompt

    def _format_list(self, items: List[str]) -> str:
        """Format list items with bullets"""
        if not items:
            return "• None identified"
        return "\n".join(f"• {item}" for item in items)

    def _format_assessment_types(self, types: List[Dict]) -> str:
        """Format assessment type performance"""
        if not types:
            return "• All assessment types performing well"
        return "\n".join(f"• {t['type'].upper()}: {t['avg']:.1f}% average" for t in types)

    def _format_career_status(self, career: Dict) -> str:
        """Format career progression information"""
        if not career.get("enrolled"):
            return "Not currently enrolled in any career advancement program (B.Ed/M.Ed)"

        courses = career.get("current_courses", [])
        if not courses:
            return "Enrolled but no active courses"

        lines = []
        for course in courses:
            lines.append(f"• {course['course_name']}: {course['completion_percentage']:.0f}% complete ({course['modules_completed']}/{course['total_modules']} modules)")
            if course['pending_exams']:
                lines.append(f"  → Pending: {len(course['pending_exams'])} module exams")

        return "\n".join(lines)

    def _format_engagement(self, context: Dict) -> str:
        """Format platform engagement summary"""
        materials = context.get("materials", {})
        ai_tutor = context.get("ai_tutor", {})

        lines = []
        lines.append(f"• Teaching Materials Uploaded: {materials.get('total_uploaded', 0)}")
        lines.append(f"• AI Tutor Sessions: {ai_tutor.get('total_sessions', 0)}")

        return "\n".join(lines)
