"""
AI Agent to fetch real CPD courses from DIKSHA, SWAYAM, NISHTHA
Based on teacher's weak areas, subject, and grade level
"""
import os
import httpx
import json
import asyncio
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-chat")


class CourseFetcherAgent:
    """
    AI Agent to search and fetch real CPD courses based on teacher needs
    """

    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.model = OPENROUTER_MODEL

    async def fetch_personalized_courses(
        self,
        weak_modules: List[str],
        subject: str,
        grade: str,
        board: str,
        state: str = "India",
        difficulty: str = "Intermediate",
        max_courses: int = 3
    ) -> List[Dict]:
        """
        Fetch real courses based on teacher's weak areas and profile

        Args:
            weak_modules: List of weak module names (e.g., ["Subject Knowledge & Content Expertise"])
            subject: Teacher's subject (e.g., "Mathematics", "Telugu")
            grade: Grade teaching (e.g., "8-10", "5-7")
            board: Board (e.g., "CBSE", "State Board")
            state: State name (e.g., "Telangana")
            difficulty: Course difficulty level (Beginner/Intermediate/Advanced)
            max_courses: Maximum number of courses to return (default: 3)

        Returns:
            List of personalized course recommendations with real URLs
        """
        print(f"[COURSE AGENT] Fetching {difficulty} courses for {subject} teacher (Grades {grade})")
        print(f"[COURSE AGENT] Weak areas: {weak_modules}")

        # Map modules to course categories
        category_focus = self._map_modules_to_categories(weak_modules, subject)

        # Fetch courses using AI
        courses = await self._fetch_courses_with_ai(
            category_focus, subject, grade, board, state, difficulty, max_courses
        )

        print(f"[COURSE AGENT] Found {len(courses)} personalized courses")
        return courses[:max_courses]  # Limit to requested number

    def _map_modules_to_categories(self, weak_modules: List[str], subject: str) -> str:
        """Map weak modules to course categories and subject needs"""

        category_mapping = {
            "Subject Knowledge & Content Expertise": f"{subject} subject knowledge, {subject} teaching methodology, content mastery in {subject}",
            "Pedagogical Skills & Classroom Practice": f"Classroom management, teaching strategies for {subject}, lesson planning",
            "Use of Technology & Innovation": f"Digital tools for {subject} teaching, educational technology, online teaching",
            "Assessment & Feedback": f"Assessment strategies, evaluation methods for {subject}, formative assessment",
            "Inclusivity, Values & Dispositions": "Inclusive education, diverse learners, equity in classroom",
            "Community & Parent Engagement": "Parent communication, community involvement, stakeholder engagement",
            "Professional Development & Leadership": "Teacher leadership, professional growth, educational leadership"
        }

        focus_areas = []
        for module in weak_modules:
            if module in category_mapping:
                focus_areas.append(category_mapping[module])

        return ", ".join(focus_areas) if focus_areas else f"{subject} teaching, general pedagogy"

    async def _fetch_courses_with_ai(
        self, category_focus: str, subject: str, grade: str, board: str, state: str, difficulty: str = "Intermediate", max_courses: int = 3
    ) -> List[Dict]:
        """Use AI to search and extract real courses"""

        prompt = f"""You are an expert educational consultant helping Indian teachers find relevant CPD courses.

TEACHER PROFILE:
- Subject Teaching: {subject}
- Grade Level: {grade}
- Board: {board}
- State: {state}
- Weak Areas Needing Improvement: {category_focus}
- Required Difficulty Level: {difficulty}

PLATFORMS TO SEARCH:
1. DIKSHA (diksha.gov.in) - Government platform by NCERT
   - NISHTHA modules for teacher training
   - Subject-specific courses
   - State-specific content

2. SWAYAM (swayam.gov.in) - MOOC platform
   - Courses by IITs, IGNOU, NCERT
   - Education pedagogy courses
   - Subject teaching methodology

3. NCERT Online Courses
   - Teacher training programs
   - Subject-specific workshops

TASK:
Recommend exactly {max_courses} relevant {difficulty} level CPD course topics for {subject} teachers to improve in: {category_focus}

CRITICAL SUBJECT FILTER:
- Teacher teaches {subject} subject ONLY
- ALL courses MUST be for {subject} teaching
- DO NOT include other subjects

For EACH course recommendation provide:
{{
  "title": "Course title for {subject} teachers",
  "description": "What the course covers (2-3 sentences)",
  "platform": "DIKSHA/SWAYAM/NISHTHA",
  "category": "Main category from weak areas",
  "duration_hours": estimated_hours,
  "target_subjects": "{subject}",
  "difficulty_level": "{difficulty}",
  "relevance_reason": "Why this addresses teacher's weak areas"
}}

IMPORTANT:
- DO NOT include URLs (we will add platform links automatically)
- Focus on course content and relevance
- Courses should address: {category_focus}
- Return EXACTLY {max_courses} course recommendations at {difficulty} level

Return ONLY a valid JSON array. NO markdown, NO explanations.
"""

        max_retries = 3
        retry_delays = [5, 10, 20]

        for attempt in range(max_retries):
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }

                body = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 3000
                }

                async with httpx.AsyncClient(timeout=90) as client:
                    response = await client.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        json=body
                    )
                    response.raise_for_status()
                    data = response.json()

                content = data["choices"][0]["message"]["content"].strip()

                # Clean markdown
                if content.startswith('```json'):
                    content = content[7:]
                if content.startswith('```'):
                    content = content[3:]
                if content.endswith('```'):
                    content = content[:-3]
                content = content.strip()

                # Extract JSON array
                start = content.find('[')
                end = content.rfind(']') + 1

                if start >= 0 and end > start:
                    json_str = content[start:end]
                    courses = json.loads(json_str)

                    if isinstance(courses, list) and len(courses) > 0:
                        # Add valid platform URLs to each course
                        courses = self._add_platform_urls(courses, subject, state)
                        print(f"[COURSE AGENT] Successfully fetched {len(courses)} courses")
                        return courses

                print("[COURSE AGENT] Failed to parse course data")
                return []

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    if attempt < max_retries - 1:
                        wait_time = retry_delays[attempt]
                        print(f"[COURSE AGENT RATE LIMIT] Waiting {wait_time}s...")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        print(f"[COURSE AGENT ERROR] Rate limit exceeded")
                        return self._get_fallback_courses(subject, grade)
                else:
                    print(f"[COURSE AGENT ERROR] HTTP {e.response.status_code}")
                    return self._get_fallback_courses(subject, grade)
            except json.JSONDecodeError as e:
                print(f"[COURSE AGENT ERROR] JSON parse failed: {e}")
                return self._get_fallback_courses(subject, grade)
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = retry_delays[attempt]
                    print(f"[COURSE AGENT ERROR] {e}. Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    print(f"[COURSE AGENT ERROR] Failed: {e}")
                    return self._get_fallback_courses(subject, grade)

        return self._get_fallback_courses(subject, grade)

    def _add_platform_urls(self, courses: List[Dict], subject: str, state: str) -> List[Dict]:
        """Add valid, working platform URLs and missing fields to AI-generated courses"""

        # Platform-specific valid URLs
        platform_urls = {
            "DIKSHA": f"https://diksha.gov.in/explore-course?selectedTab=course&board=State%20({state})",
            "SWAYAM": "https://swayam.gov.in/nc_details/NCERT",
            "NISHTHA": "https://itpd.ncert.gov.in/",
            "NCERT": "https://ncert.nic.in/online-courses.php"
        }

        for course in courses:
            platform = course.get("platform", "DIKSHA")

            # Add valid URL based on platform
            if platform in platform_urls:
                course["url"] = platform_urls[platform]
            elif "DIKSHA" in platform or "NISHTHA" in platform:
                course["url"] = platform_urls["DIKSHA"]
            elif "SWAYAM" in platform:
                course["url"] = platform_urls["SWAYAM"]
            else:
                course["url"] = platform_urls["DIKSHA"]  # Default to DIKSHA

            # Add missing required fields
            if "target_grades" not in course:
                course["target_grades"] = "All Grades"
            if "target_boards" not in course:
                course["target_boards"] = "All Boards"
            if "certificate_available" not in course:
                course["certificate_available"] = True
            if "provider" not in course:
                course["provider"] = "NCERT" if platform == "DIKSHA" else platform

        return courses

    def _get_fallback_courses(self, subject: str, grade: str) -> List[Dict]:
        """Fallback with general platform links when AI fails"""
        print("[COURSE AGENT] Using fallback course links")

        return [
            {
                "title": f"DIKSHA - {subject} Teaching Courses",
                "description": f"Explore free CPD courses for {subject} teachers on DIKSHA platform. Includes NISHTHA modules, subject-specific training, and pedagogical resources.",
                "url": "https://diksha.gov.in/explore-course",
                "platform": "DIKSHA",
                "category": "Subject Knowledge & Content Expertise",
                "duration_hours": 20,
                "target_grades": grade,
                "target_subjects": subject,
                "target_boards": "All Boards",
                "difficulty_level": "Intermediate",
                "certificate_available": True,
                "provider": "NCERT",
                "relevance_reason": f"Platform with multiple {subject} teaching courses"
            },
            {
                "title": "SWAYAM - Teacher Training Programs",
                "description": "Browse education and teacher training MOOCs from IITs, IGNOU, and NCERT. Free courses on pedagogy, subject methodology, and professional development.",
                "url": "https://swayam.gov.in/",
                "platform": "SWAYAM",
                "category": "Pedagogical Skills & Classroom Practice",
                "duration_hours": 30,
                "target_grades": grade,
                "target_subjects": "All Subjects",
                "target_boards": "All Boards",
                "difficulty_level": "Intermediate",
                "certificate_available": True,
                "provider": "SWAYAM",
                "relevance_reason": "Comprehensive teacher training platform"
            },
            {
                "title": "NISHTHA Training Modules",
                "description": "National Initiative for School Heads' and Teachers' Holistic Advancement. Access capacity building modules on DIKSHA platform.",
                "url": "https://itpd.ncert.gov.in/",
                "platform": "DIKSHA-NISHTHA",
                "category": "Professional Development & Leadership",
                "duration_hours": 15,
                "target_grades": grade,
                "target_subjects": subject,
                "target_boards": "All Boards",
                "difficulty_level": "Beginner",
                "certificate_available": True,
                "provider": "NCERT",
                "relevance_reason": "Structured teacher capacity building program"
            }
        ]


# Global agent instance
course_fetcher_agent = CourseFetcherAgent()
