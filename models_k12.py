# models_k12.py - K-12 Student Assessment Models
"""
These models support the K-12 student assessment system where:
- Teachers create assessments for students
- Students take exams and submit answers
- Results are stored and visible to teachers
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Text
from database import Base
from datetime import datetime

class K12Assessment(Base):
    """
    Assessments created by teachers for K-12 students
    Different from CPD assessments (for teacher professional development)
    """
    __tablename__ = "k12_assessments"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Target students (by class and section)
    class_name = Column(String(10), nullable=False, index=True)
    section = Column(String(5), nullable=False, index=True)

    # Assessment details
    subject = Column(String(100), nullable=False)
    chapter = Column(String(200), nullable=False)
    language = Column(String(20), nullable=False, default="English")  # "English" or "Hindi"
    board = Column(String(50), nullable=True, default="CBSE")  # CBSE, TELANGANA, ICSE, etc.

    # Timing
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)


class K12Question(Base):
    """
    Question bank for K-12 assessments
    Supports multiple question types: MCQ, True/False, Short Answer, Fill Blank, Multi-Select, Ordering
    """
    __tablename__ = "k12_questions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("k12_assessments.id", ondelete="CASCADE"), nullable=False, index=True)

    # Question content
    question = Column(Text, nullable=False)

    # Question type - CRITICAL NEW FIELD
    question_type = Column(String(30), nullable=False, default="multiple_choice", index=True)
    # Values: 'multiple_choice', 'multi_select', 'true_false', 'short_answer', 'fill_blank', 'ordering'

    # Type-specific data (flexible JSON structure)
    question_data = Column(JSON, nullable=False)
    # Structure varies by type:
    # MCQ: {"options": {"A": "...", "B": "..."}, "correct_answer": "A"}
    # Multi-select: {"options": {"A": "...", "B": "..."}, "correct_answers": ["A", "C"]}
    # True/False: {"correct_answer": true}
    # Short answer: {"sample_answer": "...", "max_words": 50}
    # Fill blank: {"correct_answers": ["answer1", "answer2"]}
    # Ordering: {"items": ["A", "B", "C"], "correct_order": [2, 0, 1]}

    # Legacy fields (for backward compatibility with MCQ)
    options = Column(JSON, nullable=True)  # Deprecated: Use question_data instead
    correct_answer = Column(String(5), nullable=True)  # Deprecated: Use question_data instead

    # Question metadata
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    marks = Column(Integer, default=1)
    explanation = Column(Text, nullable=True)  # Step-by-step solution

    # NCERT reference (general chapter/topic, NO example numbers)
    ncert_grade = Column(Integer, nullable=True, index=True)
    ncert_subject = Column(String(100), nullable=True, index=True)
    ncert_chapter = Column(String(200), nullable=True, index=True)
    ncert_topic = Column(String(200), nullable=True)  # General topic name

    # Educational metadata
    concept_tested = Column(String(200), nullable=True)  # "Physical vs Chemical Change"
    blooms_level = Column(String(20), nullable=True)  # remember, understand, apply, analyze, evaluate, create
    cognitive_skill = Column(String(50), nullable=True)  # problem_solving, critical_thinking, recall

    created_at = Column(DateTime, default=datetime.utcnow)


class K12Result(Base):
    """
    Student exam results
    Stores answers and calculated scores
    """
    __tablename__ = "k12_results"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    assessment_id = Column(Integer, ForeignKey("k12_assessments.id", ondelete="CASCADE"), nullable=False, index=True)

    answers = Column(JSON)
    score = Column(Integer, default=0)
    submitted_at = Column(DateTime, default=datetime.utcnow)
