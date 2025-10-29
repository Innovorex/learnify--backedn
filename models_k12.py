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

    # Timing
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)


class K12Question(Base):
    """
    Question bank for K-12 assessments
    Multiple choice questions with 4 options (A, B, C, D)
    """
    __tablename__ = "k12_questions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("k12_assessments.id", ondelete="CASCADE"), nullable=False, index=True)

    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)
    correct_answer = Column(String(5), nullable=False)
    difficulty = Column(String(20), default="medium")

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
