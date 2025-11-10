"""
NCERT Content Service
=====================
Retrieves NCERT textbook content from database and prepares it for question generation.

Key Features:
- Fetches chapter content from ncert_textbook_content table
- Cleans content (removes example numbers, page references)
- Extracts key concepts and definitions
- Returns structured data for AI question generation
"""

from typing import Optional, Dict, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import NCERTTextbookContent
import re


class NCERTContentService:
    """Service for retrieving and processing NCERT textbook content"""

    def __init__(self, db: Session):
        self.db = db

    def get_chapter_content(self, grade: int, subject: str, chapter_name: str) -> Optional[Dict]:
        """
        Get full NCERT textbook content for a specific chapter

        Args:
            grade: Integer (1-10)
            subject: String ("Mathematics", "Science", etc.)
            chapter_name: String ("Chemical Reactions and Equations", "Real Numbers", etc.)

        Returns:
            {
                "chapter_name": "Chemical Reactions and Equations",
                "chapter_number": 1,
                "raw_content": "Full chapter text...",
                "cleaned_content": "Content without example numbers",
                "key_concepts": ["Chemical change", "Physical change", ...],
                "definitions": {"Oxidation": "...", "Reduction": "..."},
                "total_length": 15000,
                "has_formulas": True,
                "has_images": True
            }

            None if content not found
        """

        # Query all content pieces for this chapter
        contents = self.db.query(NCERTTextbookContent).filter(
            NCERTTextbookContent.grade == grade,
            NCERTTextbookContent.subject.ilike(f"%{subject}%"),
            NCERTTextbookContent.chapter_name.ilike(f"%{chapter_name}%")
        ).all()

        if not contents:
            print(f"❌ No NCERT content found for Grade {grade}, {subject}, {chapter_name}")
            return None

        print(f"✅ Found {len(contents)} content pieces for {chapter_name}")

        # Combine all content pieces
        raw_content = "\n\n".join([c.content_text for c in contents])

        # Get chapter metadata
        first_content = contents[0]
        chapter_number = first_content.chapter_number
        has_formulas = any(c.has_formulas for c in contents)
        has_images = any(c.has_images for c in contents)

        # Clean content (remove example numbers)
        cleaned_content = self._clean_content(raw_content)

        # Extract key concepts
        key_concepts = self._extract_concepts(cleaned_content)

        # Extract definitions
        definitions = self._extract_definitions(cleaned_content)

        return {
            "chapter_name": first_content.chapter_name,
            "chapter_number": chapter_number,
            "raw_content": raw_content,
            "cleaned_content": cleaned_content,
            "key_concepts": key_concepts,
            "definitions": definitions,
            "total_length": len(cleaned_content),
            "has_formulas": has_formulas,
            "has_images": has_images
        }

    def _clean_content(self, text: str) -> str:
        """
        Remove example numbers, exercise references, and page numbers
        Keep the concepts but remove "Example 1.1", "Exercise 2.3" etc.

        This ensures questions are concept-based, not example-specific
        """

        # Remove patterns like "Example 1.1", "Example: 2.3"
        text = re.sub(r'Example\s*:?\s*\d+\.?\d*', '', text, flags=re.IGNORECASE)

        # Remove "Exercise 1.1", "EXERCISE 2.3"
        text = re.sub(r'Exercise\s*:?\s*\d+\.?\d*', '', text, flags=re.IGNORECASE)

        # Remove "Activity 1.2", "ACTIVITY 2.1"
        text = re.sub(r'Activity\s*:?\s*\d+\.?\d*', '', text, flags=re.IGNORECASE)

        # Remove "Question 1.1", "Q 2.3"
        text = re.sub(r'Question\s*:?\s*\d+\.?\d*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Q\.?\s*\d+\.?\d*', '', text)

        # Remove page references
        text = re.sub(r'Page\s+\d+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\[Page:\s*\d+\]', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\(Page\s+\d+\)', '', text, flags=re.IGNORECASE)

        # Remove "Fig. 1.1", "Figure 2.3"
        text = re.sub(r'Fig\.?\s*:?\s*\d+\.?\d*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Figure\s*:?\s*\d+\.?\d*', '', text, flags=re.IGNORECASE)

        # Clean up multiple spaces and newlines
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)

        return text.strip()

    def _extract_concepts(self, text: str) -> List[str]:
        """
        Extract key concepts/terminology from text

        Returns:
            ["Chemical change", "Physical change", "Oxidation", "Reduction"]
        """
        concepts = []

        # Pattern 1: Extract from section headings (all caps or title case)
        # Example: "CHEMICAL REACTIONS" or "Physical Changes"
        heading_pattern = r'\n([A-Z][A-Z\s]{3,30})\n'
        headings = re.findall(heading_pattern, text)
        concepts.extend([h.strip().title() for h in headings if len(h.strip()) > 3])

        # Pattern 2: Extract from definition patterns
        # Example: "Oxidation is...", "A chemical change is..."
        definition_pattern = r'([A-Z][a-z]+(?:\s+[a-z]+){0,2})\s+(?:is|are|means|refers to)'
        defined_terms = re.findall(definition_pattern, text)
        concepts.extend([term.strip() for term in defined_terms])

        # Pattern 3: Extract bold/emphasized terms (if markdown present)
        bold_pattern = r'\*\*([A-Za-z\s]{3,30})\*\*'
        bold_terms = re.findall(bold_pattern, text)
        concepts.extend([term.strip() for term in bold_terms])

        # Remove duplicates and limit to top 20
        unique_concepts = list(set(concepts))
        unique_concepts = [c for c in unique_concepts if 3 < len(c) < 50]

        return unique_concepts[:20]

    def _extract_definitions(self, text: str) -> Dict[str, str]:
        """
        Extract definitions from text

        Returns:
            {
                "Oxidation": "Addition of oxygen or removal of hydrogen",
                "Reduction": "Removal of oxygen or addition of hydrogen"
            }
        """
        definitions = {}

        # Pattern: "Term is definition." or "Term: definition"
        # Example: "Oxidation is the addition of oxygen."
        pattern1 = r'([A-Z][a-z]+)\s+is\s+([^.!?]+[.!?])'
        matches = re.findall(pattern1, text)
        for term, definition in matches[:10]:
            if len(term) > 2 and len(definition) < 200:
                definitions[term.strip()] = definition.strip()

        # Pattern: "Term: definition"
        pattern2 = r'([A-Z][a-z]+)\s*:\s*([^.!?\n]+[.!?])'
        matches = re.findall(pattern2, text)
        for term, definition in matches[:10]:
            if len(term) > 2 and len(definition) < 200:
                definitions[term.strip()] = definition.strip()

        return definitions

    def validate_chapter_exists(self, grade: int, subject: str, chapter_name: str) -> bool:
        """
        Check if chapter content exists in database

        Returns:
            True if content exists, False otherwise
        """
        count = self.db.query(NCERTTextbookContent).filter(
            NCERTTextbookContent.grade == grade,
            NCERTTextbookContent.subject.ilike(f"%{subject}%"),
            NCERTTextbookContent.chapter_name.ilike(f"%{chapter_name}%")
        ).count()

        return count > 0

    def get_available_chapters(self, grade: int, subject: str) -> List[Dict]:
        """
        Get list of available chapters for a subject

        Args:
            grade: 1-10
            subject: "Mathematics", "Science", etc.

        Returns:
            [
                {"chapter_number": 1, "chapter_name": "Real Numbers", "available": True, "content_pieces": 5},
                {"chapter_number": 2, "chapter_name": "Polynomials", "available": True, "content_pieces": 8},
                ...
            ]
        """

        # Query distinct chapters
        results = self.db.query(
            NCERTTextbookContent.chapter_number,
            NCERTTextbookContent.chapter_name,
            func.count(NCERTTextbookContent.id).label('content_pieces')
        ).filter(
            NCERTTextbookContent.grade == grade,
            NCERTTextbookContent.subject.ilike(f"%{subject}%")
        ).group_by(
            NCERTTextbookContent.chapter_number,
            NCERTTextbookContent.chapter_name
        ).order_by(
            NCERTTextbookContent.chapter_number
        ).all()

        chapters = []
        for row in results:
            chapters.append({
                "chapter_number": row.chapter_number or 0,
                "chapter_name": row.chapter_name,
                "available": True,
                "content_pieces": row.content_pieces
            })

        return chapters

    def get_topic_content(self, grade: int, subject: str, chapter_name: str, topic_name: str) -> Optional[str]:
        """
        Get content for a specific topic within a chapter

        Args:
            topic_name: "Euclid's Division Algorithm", "HCF and LCM", etc.

        Returns:
            Filtered content related to that topic only
        """

        # Query content with specific topic
        contents = self.db.query(NCERTTextbookContent).filter(
            NCERTTextbookContent.grade == grade,
            NCERTTextbookContent.subject.ilike(f"%{subject}%"),
            NCERTTextbookContent.chapter_name.ilike(f"%{chapter_name}%"),
            NCERTTextbookContent.topic_name.ilike(f"%{topic_name}%")
        ).all()

        if not contents:
            # If no specific topic found, return None (will use full chapter)
            return None

        # Combine topic-specific content
        topic_content = "\n\n".join([c.content_text for c in contents])

        return self._clean_content(topic_content)

    def get_content_summary(self, grade: int, subject: str) -> Dict:
        """
        Get summary of available content for a subject

        Returns:
            {
                "total_chapters": 15,
                "total_content_pieces": 245,
                "chapters": [...list of chapters...]
            }
        """

        chapters = self.get_available_chapters(grade, subject)
        total_pieces = sum(ch['content_pieces'] for ch in chapters)

        return {
            "grade": grade,
            "subject": subject,
            "total_chapters": len(chapters),
            "total_content_pieces": total_pieces,
            "chapters": chapters
        }


def get_ncert_service(db: Session) -> NCERTContentService:
    """Factory function to create NCERT service"""
    return NCERTContentService(db)
