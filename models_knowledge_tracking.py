"""
Database models for Knowledge Assessment Attempt Tracking
Tracks attempts, limits, sessions, and performance summaries
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from database import Base

# Table 1: Individual Assessment Attempts
class TeacherAssessmentAttempt(Base):
    __tablename__ = "teacher_assessment_attempts"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False, index=True)

    attempt_number = Column(Integer, nullable=False)  # 1, 2, 3, etc.
    score_percentage = Column(Float, nullable=False)
    time_taken_seconds = Column(Integer, nullable=True)

    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Store questions and answers for feedback
    questions_json = Column(JSON, nullable=False)  # List of questions with correct answers
    answers_json = Column(JSON, nullable=False)     # User's answers

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('teacher_id', 'module_id', 'attempt_number', name='unique_teacher_module_attempt'),
    )


# Table 2: Monthly Attempt Limits (3 per month, 24h cooldown)
class TeacherAttemptLimit(Base):
    __tablename__ = "teacher_attempt_limits"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False, index=True)

    year_month = Column(String(7), nullable=False)  # Format: "2025-01"
    attempts_used = Column(Integer, default=0, nullable=False)
    max_attempts = Column(Integer, default=3, nullable=False)
    cooldown_hours = Column(Integer, default=24, nullable=False)

    last_attempt_at = Column(DateTime(timezone=True), nullable=True)
    next_attempt_available = Column(DateTime(timezone=True), nullable=True)  # last_attempt + cooldown_hours

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('teacher_id', 'module_id', 'year_month', name='unique_teacher_module_month'),
    )


# Table 3: Performance Summary (Denormalized for quick access)
class TeacherAssessmentSummary(Base):
    __tablename__ = "teacher_assessment_summary"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False, index=True)

    total_attempts = Column(Integer, default=0, nullable=False)
    best_score = Column(Float, default=0.0, nullable=False)
    latest_score = Column(Float, default=0.0, nullable=False)
    first_attempt_score = Column(Float, nullable=True)
    average_score = Column(Float, default=0.0, nullable=False)

    # Improvement rate: (latest - first) / first * 100
    improvement_rate = Column(Float, nullable=True)

    # Track weak topics for targeted improvement
    weak_topics = Column(JSON, nullable=True)  # ["topic1", "topic2"]

    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('teacher_id', 'module_id', name='unique_teacher_module_summary'),
    )


# Table 4: Active Assessment Sessions (for timer tracking)
class AssessmentSession(Base):
    __tablename__ = "assessment_sessions"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False, index=True)

    attempt_number = Column(Integer, nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=False)  # Set explicitly in code with UTC
    expires_at = Column(DateTime(timezone=True), nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)
    submitted_at = Column(DateTime(timezone=True), nullable=True)

    # Store generated questions for this session
    questions_json = Column(JSON, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
