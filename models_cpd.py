# models_cpd.py - CPD Course Recommendation System Models
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class CPDCourse(Base):
    """CPD courses from various platforms like DIKSHA, SWAYAM, etc."""
    __tablename__ = "cpd_courses"

    id = Column(Integer, primary_key=True)
    external_id = Column(String(100), nullable=True)  # ID from external platform
    platform = Column(String(50), nullable=False)    # DIKSHA, SWAYAM, NCERT, etc.

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(500), nullable=False)

    # Course categorization
    category = Column(String(100), nullable=False)    # Subject Knowledge, Pedagogical Skills, etc.
    subcategory = Column(String(100), nullable=True)  # Specific area
    target_modules = Column(Text, nullable=True)      # JSON array of module IDs this course helps with

    # Course details
    duration_hours = Column(Integer, nullable=True)
    difficulty_level = Column(String(20), nullable=True)  # Beginner, Intermediate, Advanced
    language = Column(String(20), nullable=False, default="English")

    # Targeting criteria
    target_grades = Column(String(100), nullable=True)    # "1-5", "6-8", "9-12"
    target_subjects = Column(String(200), nullable=True)  # "Mathematics, Science"
    target_boards = Column(String(100), nullable=True)    # "CBSE, ICSE, State"

    # Metadata
    provider = Column(String(100), nullable=True)
    certificate_available = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class TeacherCourseRecommendation(Base):
    """AI-generated personalized course recommendations for teachers"""
    __tablename__ = "teacher_course_recommendations"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    course_id = Column(Integer, ForeignKey("cpd_courses.id", ondelete="CASCADE"), nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=True)

    # AI-generated recommendation details
    recommendation_score = Column(Float, nullable=False)  # 0-100, AI confidence score
    ai_reasoning = Column(Text, nullable=True)            # AI's explanation for recommendation
    priority = Column(String(20), nullable=False, default="medium")  # high, medium, low

    # Performance context
    based_on_score = Column(Float, nullable=True)        # Performance score that triggered this
    improvement_area = Column(String(100), nullable=True) # Specific skill area to improve

    # Teacher interaction
    status = Column(String(20), nullable=False, default="recommended")  # recommended, enrolled, completed, dismissed
    enrolled_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    dismissed_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, server_default=func.now())

class TeacherCourseProgress(Base):
    """Track teacher progress in recommended CPD courses"""
    __tablename__ = "teacher_course_progress"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    course_id = Column(Integer, ForeignKey("cpd_courses.id", ondelete="CASCADE"), nullable=False)

    # Progress tracking
    progress_percentage = Column(Float, default=0.0)
    time_spent_hours = Column(Float, default=0.0)
    last_accessed = Column(DateTime, nullable=True)

    # Completion
    completed = Column(Boolean, default=False)
    completion_date = Column(DateTime, nullable=True)
    certificate_earned = Column(Boolean, default=False)
    certificate_url = Column(String(500), nullable=True)

    # Feedback
    rating = Column(Integer, nullable=True)  # 1-5 stars
    feedback = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())