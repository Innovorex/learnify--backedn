#!/usr/bin/env python3
"""
DIKSHA Course Scraper
=====================
Scrapes CPD courses from DIKSHA platform (diksha.gov.in)

DIKSHA API endpoints:
- Search: https://diksha.gov.in/api/course/v1/search
- Course Details: https://diksha.gov.in/api/course/v1/read/{courseId}
"""

import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime
import time
import re

from database import SessionLocal
from models import RealCPDCourse


class DIKSHAScraper:
    """Scrapes CPD courses from DIKSHA platform"""

    def __init__(self):
        self.base_url = "https://diksha.gov.in"
        self.api_url = f"{self.base_url}/api"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

    def search_courses(self,
                       query: str = "",
                       subject: Optional[str] = None,
                       board: Optional[str] = None,
                       limit: int = 100) -> List[Dict]:
        """
        Search for CPD courses on DIKSHA

        Args:
            query: Search keywords
            subject: Subject filter (Mathematics, Science, etc.)
            board: Board filter (CBSE, State boards)
            limit: Maximum courses to fetch

        Returns:
            List of course dictionaries
        """

        search_url = f"{self.api_url}/course/v1/search"

        # Build search request
        request_body = {
            "request": {
                "filters": {
                    "primaryCategory": ["Course"],
                    "status": ["Live"],
                    "contentType": ["Course"]
                },
                "limit": limit,
                "offset": 0,
                "query": query or "",
                "sort_by": {"createdOn": "desc"}
            }
        }

        # Add filters
        if subject:
            request_body["request"]["filters"]["subject"] = [subject]

        if board:
            request_body["request"]["filters"]["board"] = [board]

        try:
            print(f"🔍 Searching DIKSHA courses: query='{query}', subject={subject}, board={board}")
            response = self.session.post(search_url, json=request_body, timeout=30)

            if response.status_code == 200:
                data = response.json()
                courses = data.get("result", {}).get("content", [])
                print(f"   ✅ Found {len(courses)} courses")
                return courses
            else:
                print(f"   ❌ Search failed: {response.status_code}")
                return []

        except Exception as e:
            print(f"   ❌ Error searching DIKSHA: {e}")
            return []

    def get_course_details(self, course_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific course

        Args:
            course_id: DIKSHA course identifier

        Returns:
            Course details dictionary or None
        """

        details_url = f"{self.api_url}/course/v1/read/{course_id}"

        try:
            response = self.session.get(details_url, timeout=15)

            if response.status_code == 200:
                data = response.json()
                return data.get("result", {}).get("content", {})
            else:
                print(f"   ⚠️  Failed to get details for {course_id}")
                return None

        except Exception as e:
            print(f"   ⚠️  Error fetching details for {course_id}: {e}")
            return None

    def parse_course(self, course_data: Dict) -> Dict:
        """
        Parse DIKSHA course data into our standard format

        Args:
            course_data: Raw course data from DIKSHA API

        Returns:
            Standardized course dictionary
        """

        # Extract basic info
        course_id = course_data.get("identifier", "")
        title = course_data.get("name", "Unknown Course")
        description = course_data.get("description", "")

        # Course URL
        course_url = f"{self.base_url}/learn/course/{course_id}"

        # Extract metadata
        subjects = course_data.get("subject", [])
        if isinstance(subjects, list):
            subjects = ",".join(subjects)
        else:
            subjects = str(subjects) if subjects else ""

        grades = course_data.get("gradeLevel", [])
        if isinstance(grades, list):
            grades = ",".join(grades)
        else:
            grades = str(grades) if grades else ""

        # Category
        category = course_data.get("contentType", "")
        if not category:
            category = "Professional Development"

        # Duration (convert minutes to hours)
        duration_mins = course_data.get("duration", 0)
        duration_hours = max(1, int(duration_mins / 60)) if duration_mins else None

        # Language
        language = course_data.get("language", ["English"])
        if isinstance(language, list):
            language = language[0] if language else "English"

        # Certificate
        certificate_available = course_data.get("certifyingAgency", "") != ""

        # Provider
        provider = course_data.get("createdBy", "DIKSHA")
        if not provider or provider == "":
            provider = "DIKSHA"

        # Keywords
        keywords = []

        # Extract from title
        title_words = re.findall(r'\b\w{4,}\b', title.lower())
        keywords.extend(title_words[:10])

        # Extract from description
        if description:
            desc_words = re.findall(r'\b\w{4,}\b', description.lower())
            keywords.extend(desc_words[:15])

        # Add subject/grade keywords
        if subjects:
            keywords.extend(subjects.lower().split(','))

        # Remove duplicates and create JSON
        keywords = list(set(keywords))
        keywords_json = json.dumps(keywords)

        # Search vector (for text search)
        search_vector = f"{title} {description} {' '.join(keywords)}"

        # Rating and enrollments
        rating = course_data.get("averageRating", None)
        total_enrollments = course_data.get("enrollmentCount", None)

        return {
            "course_id_external": f"DIKSHA_{course_id}",
            "platform": "DIKSHA",
            "title": title,
            "description": description or f"DIKSHA course on {subjects}",
            "course_url": course_url,
            "category": category,
            "subjects": subjects,
            "grades": grades,
            "difficulty_level": self._infer_difficulty(title, description),
            "duration_hours": duration_hours,
            "language": language,
            "certificate_available": certificate_available,
            "target_roles": "Primary Teacher,Secondary Teacher,High School Teacher",
            "rating": rating,
            "total_enrollments": total_enrollments,
            "keywords": keywords_json,
            "provider": provider,
            "search_vector": search_vector,
            "is_active": True
        }

    def _infer_difficulty(self, title: str, description: str) -> str:
        """Infer difficulty level from title/description"""

        text = f"{title} {description}".lower()

        if any(word in text for word in ['beginner', 'basic', 'introduction', 'foundational']):
            return 'beginner'
        elif any(word in text for word in ['advanced', 'expert', 'mastery', 'specialized']):
            return 'advanced'
        else:
            return 'intermediate'

    def save_to_database(self, courses: List[Dict]) -> int:
        """
        Save scraped courses to database

        Args:
            courses: List of standardized course dictionaries

        Returns:
            Number of courses saved
        """

        db = SessionLocal()
        saved_count = 0

        for course in courses:
            try:
                # Check if already exists
                existing = db.query(RealCPDCourse).filter(
                    RealCPDCourse.course_id_external == course["course_id_external"]
                ).first()

                if existing:
                    # Update existing course
                    for key, value in course.items():
                        setattr(existing, key, value)
                    existing.last_verified_at = datetime.now()
                    print(f"   🔄 Updated: {course['title'][:60]}")
                else:
                    # Create new course
                    new_course = RealCPDCourse(**course)
                    db.add(new_course)
                    print(f"   ✅ Added: {course['title'][:60]}")

                db.commit()
                saved_count += 1

            except Exception as e:
                print(f"   ❌ Error saving course: {e}")
                db.rollback()
                continue

        db.close()
        return saved_count

    def scrape_all_cpd_courses(self, max_courses: int = 500) -> int:
        """
        Scrape all relevant CPD courses from DIKSHA

        Args:
            max_courses: Maximum number of courses to scrape

        Returns:
            Total courses saved
        """

        print("=" * 80)
        print("DIKSHA COURSE SCRAPER")
        print("=" * 80)

        all_courses = []

        # Search queries for teacher professional development
        search_queries = [
            "teacher training",
            "professional development",
            "pedagogy",
            "classroom management",
            "assessment",
            "NISHTHA",
            "CPD",
            "subject knowledge"
        ]

        # Subjects to target
        subjects = [
            "Mathematics",
            "Science",
            "English",
            "Hindi",
            "Social Science",
            "EVS"
        ]

        print(f"\n📚 Starting DIKSHA scraping...")
        print(f"   Max courses: {max_courses}")

        # Search by queries
        for query in search_queries:
            if len(all_courses) >= max_courses:
                break

            courses = self.search_courses(query=query, limit=50)

            for course in courses:
                parsed = self.parse_course(course)

                # Check for duplicates
                if not any(c["course_id_external"] == parsed["course_id_external"] for c in all_courses):
                    all_courses.append(parsed)

                if len(all_courses) >= max_courses:
                    break

            time.sleep(1)  # Rate limiting

        # Search by subjects
        for subject in subjects:
            if len(all_courses) >= max_courses:
                break

            courses = self.search_courses(query="teacher", subject=subject, limit=30)

            for course in courses:
                parsed = self.parse_course(course)

                if not any(c["course_id_external"] == parsed["course_id_external"] for c in all_courses):
                    all_courses.append(parsed)

                if len(all_courses) >= max_courses:
                    break

            time.sleep(1)

        print(f"\n📊 Scraped {len(all_courses)} unique courses")

        # Save to database
        print(f"\n💾 Saving to database...")
        saved = self.save_to_database(all_courses)

        print(f"\n{'='*80}")
        print(f"✅ DIKSHA Scraping Complete")
        print(f"   Total scraped: {len(all_courses)}")
        print(f"   Successfully saved: {saved}")
        print(f"{'='*80}")

        return saved


def main():
    """Run DIKSHA scraper"""
    scraper = DIKSHAScraper()
    scraper.scrape_all_cpd_courses(max_courses=500)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
