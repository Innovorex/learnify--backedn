"""
Service for managing syllabus cache and retrieval
"""
import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import SyllabusCache
from services.syllabus_agent import syllabus_agent


class SyllabusService:
    """Manages syllabus caching and retrieval"""

    @staticmethod
    def get_difficulty_level(experience_years: int) -> str:
        """
        Determine question difficulty based on teacher experience

        Args:
            experience_years: Years of teaching experience

        Returns:
            'easy', 'medium', or 'hard'
        """
        if experience_years <= 2:
            return 'easy'
        elif experience_years <= 7:
            return 'medium'
        else:
            return 'hard'

    @staticmethod
    async def get_syllabus(
        db: Session,
        state: str,
        board: str,
        grade: str,
        subject: str,
        force_refresh: bool = False
    ) -> dict:
        """
        Get syllabus from cache or fetch using AI agent

        Args:
            db: Database session
            state: State name
            board: Board name
            grade: Grade/Class
            subject: Subject name
            force_refresh: Force re-fetch even if cached

        Returns:
            Syllabus data dictionary
        """
        # Normalize inputs
        state = state.strip()
        board = board.strip()
        grade = str(grade).strip()
        subject = subject.strip()

        # Check cache first (unless force refresh)
        if not force_refresh:
            cached = db.query(SyllabusCache).filter(
                SyllabusCache.state == state,
                SyllabusCache.board == board,
                SyllabusCache.grade == grade,
                SyllabusCache.subject == subject
            ).first()

            # If cached and less than 30 days old, use it
            if cached:
                age = datetime.utcnow() - cached.fetched_at
                if age < timedelta(days=30):
                    print(f"[CACHE HIT] Using cached syllabus for {state}/{board}/{grade}/{subject}")
                    return json.loads(cached.syllabus_data)

        # Cache miss or expired - fetch using AI agent
        print(f"[CACHE MISS] Fetching syllabus using AI agent...")
        syllabus_data = await syllabus_agent.fetch_syllabus(state, board, grade, subject)

        # Save to cache
        try:
            cached = db.query(SyllabusCache).filter(
                SyllabusCache.state == state,
                SyllabusCache.board == board,
                SyllabusCache.grade == grade,
                SyllabusCache.subject == subject
            ).first()

            syllabus_json = json.dumps(syllabus_data, ensure_ascii=False)

            if cached:
                # Update existing
                cached.syllabus_data = syllabus_json
                cached.updated_at = datetime.utcnow()
            else:
                # Create new
                new_cache = SyllabusCache(
                    state=state,
                    board=board,
                    grade=grade,
                    subject=subject,
                    syllabus_data=syllabus_json
                )
                db.add(new_cache)

            db.commit()
            print(f"[CACHE SAVED] Syllabus cached for {state}/{board}/{grade}/{subject}")

        except Exception as e:
            print(f"[CACHE ERROR] Failed to save to cache: {e}")
            db.rollback()

        return syllabus_data


# Global service instance
syllabus_service = SyllabusService()
