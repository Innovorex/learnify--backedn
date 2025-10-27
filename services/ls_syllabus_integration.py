"""
LS Syllabus Integration Service
Connects Learnify-Teach to LS database for authentic syllabus data
"""

import asyncpg
from typing import Dict, List, Optional
import json


class LSSyllabusService:
    """
    Service to fetch syllabus data from LS (Learning System) database
    """

    def __init__(self):
        self.ls_db_url = "postgresql://postgres:postgres@localhost:5432/learnify_syllabus"
        self.connection_pool = None

    async def init_pool(self):
        """Initialize connection pool to LS database"""
        if not self.connection_pool:
            try:
                self.connection_pool = await asyncpg.create_pool(
                    self.ls_db_url,
                    min_size=1,
                    max_size=10
                )
                print("[LS_INTEGRATION] Connected to LS syllabus database")
            except Exception as e:
                print(f"[LS_INTEGRATION ERROR] Cannot connect to LS database: {e}")
                print("[LS_INTEGRATION] Will use fallback curriculum data")

    async def get_syllabus_topics(
        self,
        board: str,
        class_name: str,
        subject: str,
        academic_year: str = "2024-25"
    ) -> List[Dict]:
        """
        Fetch complete syllabus topics from LS database

        Returns:
        [
            {
                "unit_name": "Force and Laws of Motion",
                "chapter_name": "Newton's Laws",
                "topic_name": "First Law of Motion",
                "learning_outcomes": [...],
                "key_concepts": [...],
                "subtopics": [...],
                "difficulty_level": "medium",
                "weightage": 15
            },
            ...
        ]
        """

        await self.init_pool()

        if not self.connection_pool:
            return await self._get_fallback_topics(board, class_name, subject)

        try:
            async with self.connection_pool.acquire() as conn:
                # Query syllabus_master to get syllabus_id
                syllabus_query = """
                    SELECT id FROM syllabus_master
                    WHERE board = $1
                    AND class_name = $2
                    AND subject = $3
                    AND academic_year = $4
                    AND is_active = true
                    LIMIT 1
                """

                syllabus_row = await conn.fetchrow(
                    syllabus_query,
                    board, class_name, subject, academic_year
                )

                if not syllabus_row:
                    print(f"[LS_INTEGRATION] No syllabus found for {board} {class_name} {subject}")
                    return await self._get_fallback_topics(board, class_name, subject)

                syllabus_id = syllabus_row['id']

                # Query syllabus_topics for all topics
                topics_query = """
                    SELECT
                        unit_number,
                        unit_name,
                        chapter_number,
                        chapter_name,
                        topic_name,
                        subtopics,
                        learning_outcomes,
                        key_concepts,
                        content_details,
                        difficulty_level,
                        weightage,
                        sequence_order
                    FROM syllabus_topics
                    WHERE syllabus_id = $1
                    ORDER BY sequence_order, unit_number, chapter_number
                """

                topics_rows = await conn.fetch(topics_query, syllabus_id)

                # Convert to dict format
                topics = []
                for row in topics_rows:
                    topics.append({
                        "unit_number": row['unit_number'],
                        "unit_name": row['unit_name'],
                        "chapter_number": row['chapter_number'],
                        "chapter_name": row['chapter_name'],
                        "topic_name": row['topic_name'],
                        "subtopics": list(row['subtopics']) if row['subtopics'] else [],
                        "learning_outcomes": list(row['learning_outcomes']) if row['learning_outcomes'] else [],
                        "key_concepts": list(row['key_concepts']) if row['key_concepts'] else [],
                        "content_details": row['content_details'],
                        "difficulty_level": row['difficulty_level'],
                        "weightage": row['weightage']
                    })

                print(f"[LS_INTEGRATION] Fetched {len(topics)} topics from LS database")
                return topics

        except Exception as e:
            print(f"[LS_INTEGRATION ERROR] Database query failed: {e}")
            return await self._get_fallback_topics(board, class_name, subject)

    async def get_topic_details(
        self,
        board: str,
        class_name: str,
        subject: str,
        unit_name: str,
        topic_name: str
    ) -> Optional[Dict]:
        """
        Get detailed information for a specific topic

        Returns detailed topic with:
        - Core concepts
        - Learning outcomes
        - Subtopics
        - Prerequisites
        """

        topics = await self.get_syllabus_topics(board, class_name, subject)

        for topic in topics:
            if topic['unit_name'] == unit_name and topic['topic_name'] == topic_name:
                return topic

        return None

    async def get_units_summary(
        self,
        board: str,
        class_name: str,
        subject: str
    ) -> List[Dict]:
        """
        Get summary of all units with topic counts

        Returns:
        [
            {
                "unit_name": "Number Systems",
                "unit_number": 1,
                "topic_count": 5,
                "total_weightage": 15,
                "topics": ["Real Numbers", "Rational Numbers", ...]
            },
            ...
        ]
        """

        all_topics = await self.get_syllabus_topics(board, class_name, subject)

        # Group by units
        units = {}
        for topic in all_topics:
            unit_name = topic['unit_name']
            if unit_name not in units:
                units[unit_name] = {
                    "unit_name": unit_name,
                    "unit_number": topic['unit_number'],
                    "topics": [],
                    "total_weightage": 0
                }

            units[unit_name]['topics'].append(topic['topic_name'])
            units[unit_name]['total_weightage'] += (topic['weightage'] or 0)

        # Convert to list
        units_list = []
        for unit_data in units.values():
            unit_data['topic_count'] = len(unit_data['topics'])
            units_list.append(unit_data)

        # Sort by unit number
        units_list.sort(key=lambda x: x['unit_number'])

        return units_list

    async def _get_fallback_topics(
        self,
        board: str,
        class_name: str,
        subject: str
    ) -> List[Dict]:
        """
        Fallback to curriculum_data.py when LS database unavailable
        """

        try:
            from services.curriculum_data import curriculum_service

            # Use existing curriculum service
            curriculum = curriculum_service.get_curriculum(
                board=board,
                grade=class_name,
                subject=subject
            )

            if not curriculum or 'units' not in curriculum:
                return []

            # Convert curriculum format to topics format
            topics = []
            sequence = 0

            for unit_name, unit_data in curriculum['units'].items():
                unit_topics = unit_data.get('topics', [])

                for topic_name in unit_topics:
                    topics.append({
                        "unit_name": unit_name,
                        "topic_name": topic_name,
                        "learning_outcomes": unit_data.get('learning_outcomes', []),
                        "key_concepts": [],  # Not available in fallback
                        "subtopics": [],
                        "difficulty_level": "medium",
                        "weightage": unit_data.get('weightage', 10),
                        "sequence_order": sequence
                    })
                    sequence += 1

            print(f"[LS_INTEGRATION] Using fallback curriculum: {len(topics)} topics")
            return topics

        except Exception as e:
            print(f"[LS_INTEGRATION ERROR] Fallback also failed: {e}")
            return []

    async def close(self):
        """Close database connection pool"""
        if self.connection_pool:
            await self.connection_pool.close()


# Global instance
ls_syllabus_service = LSSyllabusService()
