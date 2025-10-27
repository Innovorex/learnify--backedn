# services/course_recommender.py - AI-Powered Course Recommendation Engine
import os
import json
import httpx
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from models import User, TeacherProfile, Performance, Module
from models_cpd import CPDCourse, TeacherCourseRecommendation
from services.course_fetcher_agent import course_fetcher_agent
from services.performance_analyzer import PerformanceAnalyzer

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-chat")

async def generate_course_recommendations(db: Session, teacher_id: int) -> List[Dict[str, Any]]:
    """
    SMART AI-powered course recommendations based on performance trends
    - Analyzes performance trends (improved/stagnant/declined)
    - Recommends ONLY 2-3 most relevant courses
    - Adapts difficulty based on current performance
    - Provides personalized reasoning for each recommendation
    """
    print(f"[SMART-REC] Generating intelligent recommendations for teacher ID: {teacher_id}")

    # Get teacher profile
    teacher = db.query(User).filter_by(id=teacher_id).first()
    if not teacher:
        print(f"[ERROR] Teacher not found for ID: {teacher_id}")
        return []

    profile = db.query(TeacherProfile).filter_by(user_id=teacher_id).first()
    if not profile:
        print(f"[ERROR] Teacher profile not found for user: {teacher.name}")
        return []

    # Check if teacher has any performance data
    performances = db.query(Performance).filter(Performance.teacher_id == teacher_id).count()
    if performances == 0:
        print("[INFO] No performance data yet, using general recommendations")
        return await _generate_fallback_recommendations(db, teacher_id, profile, None)

    # Use Performance Analyzer to identify priority areas
    analyzer = PerformanceAnalyzer(db, teacher_id)
    priority_areas = analyzer.get_priority_areas(max_areas=3)  # Top 3 priorities

    print(f"[SMART-REC] Identified {len(priority_areas)} priority areas for {teacher.name}")
    for module_name, trend_data in priority_areas:
        print(f"  - {module_name}: {trend_data['current_score']}% ({trend_data['trend']}, {trend_data['priority']} priority)")

    # Extract teacher details
    primary_subject = profile.subjects_teaching.split(',')[0].strip() if profile.subjects_teaching else 'General'
    primary_grade = profile.grades_teaching.split(',')[0].strip() if profile.grades_teaching else '1-12'
    board = profile.board or 'CBSE'
    state = getattr(profile, 'state', 'Telangana')

    # Get platforms already used (for diversity)
    used_platforms = _get_used_platforms(db, teacher_id)

    # Generate recommendations for each priority area (limit to 2-3 total)
    all_recommendations = []
    platforms_used = set(used_platforms)

    for idx, (module_name, trend_data) in enumerate(priority_areas[:3]):  # Max 3 courses
        # Determine preferred platform (alternate for diversity)
        preferred_platform = _select_diverse_platform(platforms_used)
        platforms_used.add(preferred_platform)

        print(f"[SMART-REC] Fetching {trend_data['recommended_difficulty']} course for {module_name} ({trend_data['trend']})")

        # Fetch course using AI agent
        fetched_courses = await course_fetcher_agent.fetch_personalized_courses(
            weak_modules=[module_name],
            subject=primary_subject,
            grade=primary_grade,
            board=board,
            state=state,
            difficulty=trend_data['recommended_difficulty'],  # Pass difficulty to AI
            max_courses=1  # Only 1 course per priority area
        )

        if fetched_courses:
            # Add performance trend context to the course
            course = fetched_courses[0]
            course["performance_context"] = {
                "current_score": trend_data["current_score"],
                "trend": trend_data["trend"],
                "change_percentage": trend_data["change_percentage"],
                "priority": trend_data["priority"]
            }
            course["relevance_reason"] = analyzer.get_focus_message(module_name, trend_data)
            all_recommendations.append(course)

    if not all_recommendations:
        print("[WARNING] Course fetcher failed, using fallback")
        return await _generate_fallback_recommendations(db, teacher_id, profile, None)

    # Save recommendations to database
    saved_recommendations = await _save_smart_recommendations(db, teacher_id, all_recommendations)

    print(f"[SUCCESS] Generated {len(saved_recommendations)} smart recommendations")
    return saved_recommendations

def _get_used_platforms(db: Session, teacher_id: int) -> List[str]:
    """Get platforms teacher has already enrolled in (for diversity)"""
    from models_cpd import TeacherCourseProgress

    enrolled = db.query(CPDCourse.platform).join(TeacherCourseProgress).filter(
        TeacherCourseProgress.teacher_id == teacher_id
    ).distinct().all()

    return [platform[0] for platform in enrolled]

def _select_diverse_platform(used_platforms: set) -> str:
    """Select a platform for diversity (rotate through platforms)"""
    all_platforms = ["DIKSHA", "SWAYAM", "NISHTHA"]

    # Find platforms not yet used
    unused = [p for p in all_platforms if p not in used_platforms]

    if unused:
        return unused[0]  # Return first unused platform
    else:
        # All platforms used, cycle through
        return all_platforms[len(used_platforms) % len(all_platforms)]

async def _save_smart_recommendations(db: Session, teacher_id: int, recommendations: List[Dict]) -> List[Dict[str, Any]]:
    """Save smart recommendations with performance context"""
    saved_recommendations = []

    for course_data in recommendations:
        # Check if course exists
        existing_course = db.query(CPDCourse).filter_by(url=course_data["url"]).first()

        if not existing_course:
            # Create new course
            course = CPDCourse(
                title=course_data["title"],
                description=course_data["description"],
                url=course_data["url"],
                platform=course_data["platform"],
                category=course_data.get("category", "General"),
                subcategory=course_data.get("category", "General"),
                duration_hours=course_data.get("duration_hours", 20),
                difficulty_level=course_data.get("difficulty_level", "Intermediate"),
                target_grades=course_data.get("target_grades", "All"),
                target_subjects=course_data.get("target_subjects", "All"),
                target_boards=course_data.get("target_boards", "All"),
                provider=course_data.get("provider", "NCERT"),
                certificate_available=course_data.get("certificate_available", True),
                is_active=True
            )
            db.add(course)
            db.flush()
            course_id = course.id
        else:
            course_id = existing_course.id
            course = existing_course

        # Create recommendation with performance context
        perf_context = course_data.get("performance_context", {})
        existing_rec = db.query(TeacherCourseRecommendation).filter_by(
            teacher_id=teacher_id,
            course_id=course_id,
            status="recommended"
        ).first()

        if not existing_rec:
            # Map priority to recommendation score
            priority_scores = {"urgent": 95, "high": 85, "medium": 75, "low": 65}
            score = priority_scores.get(perf_context.get("priority", "medium"), 75)

            recommendation = TeacherCourseRecommendation(
                teacher_id=teacher_id,
                course_id=course_id,
                recommendation_score=score,
                ai_reasoning=course_data.get("relevance_reason", "Recommended based on your performance"),
                priority=perf_context.get("priority", "medium"),
                improvement_area=course_data.get("category", "Professional Development")
            )
            db.add(recommendation)

        # Format for response
        saved_recommendations.append({
            "id": course_id,
            "title": course.title,
            "description": course.description,
            "category": course.category,
            "duration_hours": course.duration_hours,
            "platform": course.platform,
            "difficulty_level": course.difficulty_level,
            "url": course.url,
            "certificate_available": course.certificate_available,
            "recommendation": {
                "score": priority_scores.get(perf_context.get("priority", "medium"), 75),
                "priority": perf_context.get("priority", "medium"),
                "reasoning": course_data.get("relevance_reason", "Recommended based on your performance"),
                "improvement_areas": [course_data.get("category", "Professional Development")],
                "performance_trend": perf_context.get("trend", "new"),
                "current_score": perf_context.get("current_score", 0),
                "change_percentage": perf_context.get("change_percentage", 0)
            }
        })

    db.commit()
    return saved_recommendations

def _prepare_teacher_context(teacher: User, profile: TeacherProfile, performances: List) -> Dict[str, Any]:
    """Prepare teacher data for AI analysis"""

    # Calculate performance summary
    weak_areas = []
    strong_areas = []
    performance_details = {}

    for perf, module in performances:
        performance_details[module.name] = {
            "score": perf.score,
            "rating": perf.rating
        }

        if perf.score < 60:
            weak_areas.append(module.name)
        elif perf.score >= 80:
            strong_areas.append(module.name)

    return {
        "teacher_name": teacher.name,
        "education": profile.education,
        "experience_years": profile.experience_years,
        "grades_teaching": profile.grades_teaching,
        "subjects_teaching": profile.subjects_teaching,
        "board": profile.board,
        "performance_summary": {
            "weak_areas": weak_areas,
            "strong_areas": strong_areas,
            "detailed_scores": performance_details
        }
    }

def _prepare_course_data(courses: List[CPDCourse], profile: TeacherProfile) -> List[Dict[str, Any]]:
    """Filter and prepare relevant courses for AI consideration"""
    relevant_courses = []

    for course in courses:
        # Filter courses relevant to teacher's context
        is_relevant = True

        # Check grade relevance - make more flexible
        if course.target_grades:
            teacher_grades = profile.grades_teaching.lower()
            course_grades = course.target_grades.lower()
            # Accept if there's any overlap OR if course is general (contains "all" or "general")
            if not (any(grade in teacher_grades for grade in course_grades.split(",")) or
                    "all" in course_grades or "general" in course_grades):
                is_relevant = False

        # Check subject relevance - make more flexible
        if course.target_subjects and is_relevant:
            teacher_subjects = profile.subjects_teaching.lower()
            course_subjects = course.target_subjects.lower()
            # Accept if there's overlap OR if course is general/cross-curricular
            if not (any(subject.strip() in teacher_subjects for subject in course_subjects.split(",")) or
                    "all" in course_subjects or "general" in course_subjects or "cross-curricular" in course_subjects):
                is_relevant = False

        # Check board relevance - make more flexible
        if course.target_boards and is_relevant:
            # Accept if board matches OR if course supports multiple boards
            if not (profile.board.lower() in course.target_boards.lower() or
                    "all" in course.target_boards.lower() or "multi" in course.target_boards.lower()):
                is_relevant = False

        if is_relevant:
            relevant_courses.append({
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "category": course.category,
                "subcategory": course.subcategory,
                "duration_hours": course.duration_hours,
                "difficulty_level": course.difficulty_level,
                "platform": course.platform,
                "url": course.url,
                "certificate_available": course.certificate_available
            })

    return relevant_courses

async def _get_ai_recommendations(teacher_context: Dict[str, Any], courses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Use AI to generate personalized course recommendations"""

    prompt = f"""
You are an expert educational consultant specializing in teacher professional development. Analyze the teacher's performance and recommend the most suitable CPD courses.

TEACHER PROFILE:
- Name: {teacher_context['teacher_name']}
- Education: {teacher_context['education']}
- Experience: {teacher_context['experience_years']} years
- Teaching: {teacher_context['grades_teaching']} grades, {teacher_context['subjects_teaching']} subjects
- Board: {teacher_context['board']}

PERFORMANCE ANALYSIS:
- Weak Areas: {teacher_context['performance_summary']['weak_areas']}
- Strong Areas: {teacher_context['performance_summary']['strong_areas']}
- Detailed Scores: {teacher_context['performance_summary']['detailed_scores']}

AVAILABLE CPD COURSES:
{json.dumps(courses, indent=2)}

TASK: Recommend the TOP 3-5 most relevant courses based on:
1. Teacher's weak performance areas (prioritize improvement needs)
2. Teaching context (grades, subjects, board)
3. Course relevance and quality
4. Progressive skill development

For each recommendation, provide:
1. Course ID (from the available courses)
2. Priority (High/Medium/Low)
3. Recommendation score (0-100)
4. Detailed reasoning explaining why this course is recommended
5. Expected impact on teacher's weak areas

Return ONLY a JSON array in this format:
[
  {{
    "course_id": 1,
    "priority": "High",
    "recommendation_score": 95,
    "reasoning": "This course directly addresses your weak area in...",
    "improvement_areas": ["Pedagogical Skills", "Technology Integration"]
  }}
]
"""

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": OPENROUTER_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1500,
                    "temperature": 0.7
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"].strip()

                # Extract JSON from response
                if content.startswith("```json"):
                    content = content[7:-3].strip()
                elif content.startswith("```"):
                    content = content[3:-3].strip()

                recommendations = json.loads(content)
                return recommendations
            else:
                print(f"AI API error: {response.status_code} - {response.text}")
                return []

    except Exception as e:
        print(f"Error generating AI recommendations: {e}")
        return []

def _save_recommendations(db: Session, teacher_id: int, ai_recommendations: List[Dict[str, Any]], available_courses: List[CPDCourse]) -> List[Dict[str, Any]]:
    """Save AI recommendations to database and return formatted response"""

    # Create course lookup
    course_lookup = {course.id: course for course in available_courses}

    saved_recommendations = []

    for rec in ai_recommendations:
        course_id = rec.get("course_id")
        if course_id not in course_lookup:
            continue

        course = course_lookup[course_id]

        # Check if recommendation already exists
        existing = db.query(TeacherCourseRecommendation).filter_by(
            teacher_id=teacher_id,
            course_id=course_id,
            status="recommended"
        ).first()

        if not existing:
            # Create new recommendation
            recommendation = TeacherCourseRecommendation(
                teacher_id=teacher_id,
                course_id=course_id,
                recommendation_score=rec.get("recommendation_score", 0),
                ai_reasoning=rec.get("reasoning", ""),
                priority=rec.get("priority", "medium").lower(),
                improvement_area=", ".join(rec.get("improvement_areas", []))
            )
            db.add(recommendation)

        # Format for response
        saved_recommendations.append({
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "category": course.category,
            "duration_hours": course.duration_hours,
            "platform": course.platform,
            "url": course.url,
            "certificate_available": course.certificate_available,
            "recommendation": {
                "score": rec.get("recommendation_score", 0),
                "priority": rec.get("priority", "medium"),
                "reasoning": rec.get("reasoning", ""),
                "improvement_areas": rec.get("improvement_areas", [])
            }
        })

    db.commit()
    return saved_recommendations

async def get_teacher_recommendations(db: Session, teacher_id: int) -> List[Dict[str, Any]]:
    """Get existing recommendations for a teacher"""

    recommendations = db.query(TeacherCourseRecommendation, CPDCourse).join(CPDCourse).filter(
        TeacherCourseRecommendation.teacher_id == teacher_id,
        TeacherCourseRecommendation.status == "recommended"
    ).order_by(TeacherCourseRecommendation.recommendation_score.desc()).all()

    result = []
    for rec, course in recommendations:
        result.append({
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "category": course.category,
            "duration_hours": course.duration_hours,
            "platform": course.platform,
            "url": course.url,
            "certificate_available": course.certificate_available,
            "recommendation": {
                "score": rec.recommendation_score,
                "priority": rec.priority,
                "reasoning": rec.ai_reasoning,
                "improvement_areas": rec.improvement_area.split(", ") if rec.improvement_area else []
            }
        })

    return result

async def _generate_fallback_recommendations(db: Session, teacher_id: int, profile: TeacherProfile, performances: List = None) -> List[Dict[str, Any]]:
    """
    Generate fallback recommendations when AI is unavailable or no performance data exists
    """
    available_courses = db.query(CPDCourse).filter_by(is_active=True).all()

    if not available_courses:
        return []

    recommendations = []
    weak_areas = []

    # Analyze performance if available
    if performances:
        for perf, module in performances:
            if perf.score < 60:
                weak_areas.append(module.name.lower())

    # Score courses based on relevance
    for course in available_courses:
        score = 50  # Base score
        priority = "medium"
        reasoning = f"Recommended based on your teaching profile: {profile.grades_teaching} grades, {profile.subjects_teaching} subjects"
        improvement_areas = []

        # Boost score for relevant categories
        if weak_areas:
            for weak_area in weak_areas:
                if any(keyword in course.category.lower() for keyword in ["pedagog", "classroom", "teaching"]):
                    score += 20
                    priority = "high"
                    reasoning = f"This course addresses areas where you can improve based on assessment performance."
                    improvement_areas.append("Pedagogical Skills")
                    break

        # Check subject relevance
        if course.target_subjects:
            teacher_subjects = profile.subjects_teaching.lower()
            course_subjects = course.target_subjects.lower()
            if any(subject.strip() in teacher_subjects for subject in course_subjects.split(",")):
                score += 15
                improvement_areas.append("Subject Knowledge")

        # Check grade relevance
        if course.target_grades:
            teacher_grades = profile.grades_teaching.lower()
            course_grades = course.target_grades.lower()
            if any(grade in teacher_grades for grade in course_grades.split(",")):
                score += 10
                improvement_areas.append("Grade-specific Teaching")

        # Technology courses get medium priority
        if "technology" in course.category.lower() or "digital" in course.category.lower():
            score += 10
            priority = "medium"
            improvement_areas.append("Technology Integration")

        if score >= 60:
            recommendations.append({
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "category": course.category,
                "duration_hours": course.duration_hours,
                "platform": course.platform,
                "url": course.url,
                "certificate_available": course.certificate_available,
                "recommendation": {
                    "score": min(score, 100),
                    "priority": priority,
                    "reasoning": reasoning,
                    "improvement_areas": improvement_areas or ["Professional Development"]
                }
            })

    # Sort by score and return top 3
    recommendations.sort(key=lambda x: x["recommendation"]["score"], reverse=True)
    top_recommendations = recommendations[:3]

    # Save to database
    for rec in top_recommendations:
        existing = db.query(TeacherCourseRecommendation).filter_by(
            teacher_id=teacher_id,
            course_id=rec["id"],
            status="recommended"
        ).first()

        if not existing:
            recommendation = TeacherCourseRecommendation(
                teacher_id=teacher_id,
                course_id=rec["id"],
                recommendation_score=rec["recommendation"]["score"],
                ai_reasoning=rec["recommendation"]["reasoning"],
                priority=rec["recommendation"]["priority"],
                improvement_area=", ".join(rec["recommendation"]["improvement_areas"])
            )
            db.add(recommendation)

    db.commit()
    return top_recommendations

async def _save_fetched_courses(db: Session, teacher_id: int, fetched_courses: List[Dict]) -> List[Dict[str, Any]]:
    """
    Save courses fetched by AI Agent to database and create recommendations
    """
    saved_recommendations = []

    for course_data in fetched_courses:
        # Check if course already exists in database by URL
        existing_course = db.query(CPDCourse).filter_by(url=course_data["url"]).first()

        if not existing_course:
            # Create new course
            course = CPDCourse(
                title=course_data["title"],
                description=course_data["description"],
                url=course_data["url"],
                platform=course_data["platform"],
                category=course_data.get("category", "General"),
                subcategory=course_data.get("category", "General"),
                duration_hours=course_data.get("duration_hours", 20),
                difficulty_level=course_data.get("difficulty_level", "Intermediate"),
                target_grades=course_data.get("target_grades", "All"),
                target_subjects=course_data.get("target_subjects", "All"),
                target_boards=course_data.get("target_boards", "All"),
                provider=course_data.get("provider", "Unknown"),
                certificate_available=course_data.get("certificate_available", True),
                is_active=True
            )
            db.add(course)
            db.flush()  # Get the course ID
            course_id = course.id
        else:
            course_id = existing_course.id
            course = existing_course

        # Create recommendation
        existing_rec = db.query(TeacherCourseRecommendation).filter_by(
            teacher_id=teacher_id,
            course_id=course_id,
            status="recommended"
        ).first()

        if not existing_rec:
            recommendation = TeacherCourseRecommendation(
                teacher_id=teacher_id,
                course_id=course_id,
                recommendation_score=90,  # High score for personalized recommendations
                ai_reasoning=course_data.get("relevance_reason", "Matches your teaching profile and weak areas"),
                priority="high",
                improvement_area=course_data.get("category", "Professional Development")
            )
            db.add(recommendation)

        # Format for response
        saved_recommendations.append({
            "id": course_id,
            "title": course.title,
            "description": course.description,
            "category": course.category,
            "duration_hours": course.duration_hours,
            "platform": course.platform,
            "url": course.url,
            "certificate_available": course.certificate_available,
            "recommendation": {
                "score": 90,
                "priority": "high",
                "reasoning": course_data.get("relevance_reason", "Matches your teaching profile and weak areas"),
                "improvement_areas": [course_data.get("category", "Professional Development")]
            }
        })

    db.commit()
    return saved_recommendations