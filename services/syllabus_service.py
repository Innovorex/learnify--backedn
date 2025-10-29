"""
Enhanced CBSE Syllabus Service for K-12 Assessment
==================================================
Retrieves syllabus content from database for AI question generation.
Simplified version focused on content retrieval (no PDF fetching).
"""

from typing import Optional, Dict
from sqlalchemy.orm import Session
from models_syllabus import SyllabusMaster, SyllabusContent, SyllabusTopics


class SyllabusService:
    """
    Service for retrieving syllabus content for question generation
    """

    def __init__(self, db: Session):
        self.db = db

    def get_syllabus_content(self, class_name: str, subject: str, chapter: str) -> Optional[str]:
        """
        Get syllabus content for a specific chapter.
        This is used by the AI question generator.
        
        Args:
            class_name: Class (e.g., '9', '10')
            subject: Subject name (e.g., 'Mathematics')
            chapter: Chapter name (e.g., 'Real Numbers')
            
        Returns:
            Full syllabus content as string, or None if not found
        """
        # First try syllabus_content table (most specific)
        content = self.db.query(SyllabusContent).filter(
            SyllabusContent.class_name == class_name,
            SyllabusContent.subject.ilike(subject),
            SyllabusContent.chapter.ilike(chapter)
        ).first()

        if content:
            print(f"✅ Found specific content for {chapter}")
            return content.full_content

        # Fallback to syllabus_master (broader content)
        syllabus = self.db.query(SyllabusMaster).filter(
            SyllabusMaster.class_name == class_name,
            SyllabusMaster.subject.ilike(subject),
            SyllabusMaster.is_active == True
        ).first()

        if syllabus and syllabus.content_extracted:
            print(f"✅ Using master syllabus content for {subject}")
            # Try to find chapter-specific section in the full content
            content_text = syllabus.content_extracted
            
            # Simple heuristic: look for chapter name in content
            if chapter.lower() in content_text.lower():
                # Extract relevant section (simplified)
                return content_text
            
            return content_text

        print(f"⚠️ No syllabus content found for Class {class_name} - {subject} - {chapter}")
        return None

    def get_topics_for_subject(self, class_name: str, subject: str) -> list:
        """
        Get all available chapters/topics for a subject
        
        Returns:
            List of chapter names
        """
        syllabus = self.db.query(SyllabusMaster).filter(
            SyllabusMaster.class_name == class_name,
            SyllabusMaster.subject.ilike(subject),
            SyllabusMaster.is_active == True
        ).first()

        if not syllabus:
            return []

        topics = self.db.query(SyllabusTopics).filter(
            SyllabusTopics.syllabus_id == syllabus.id,
            SyllabusTopics.is_chapter == True
        ).order_by(SyllabusTopics.sequence_order).all()

        return [topic.chapter_name for topic in topics]

    def get_chapter_details(self, class_name: str, subject: str, chapter: str) -> Optional[Dict]:
        """
        Get detailed information about a chapter
        """
        syllabus = self.db.query(SyllabusMaster).filter(
            SyllabusMaster.class_name == class_name,
            SyllabusMaster.subject.ilike(subject),
            SyllabusMaster.is_active == True
        ).first()

        if not syllabus:
            return None

        topic = self.db.query(SyllabusTopics).filter(
            SyllabusTopics.syllabus_id == syllabus.id,
            SyllabusTopics.chapter_name.ilike(chapter),
            SyllabusTopics.is_chapter == True
        ).first()

        if not topic:
            return None

        return {
            "chapter_name": topic.chapter_name,
            "unit_name": topic.unit_name,
            "chapter_number": topic.chapter_number,
            "subtopics": topic.subtopics or [],
            "learning_outcomes": topic.learning_outcomes or [],
            "key_concepts": topic.key_concepts or [],
            "weightage": topic.weightage,
            "difficulty_level": topic.difficulty_level
        }


def get_syllabus_service(db: Session) -> SyllabusService:
    """Factory function to create syllabus service"""
    return SyllabusService(db)
