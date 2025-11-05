# schemas.py
from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from datetime import datetime

# Role enum (string-based for easy serialization)
class RoleEnum(str, Enum):
    teacher = "teacher"
    admin = "admin"
    student = "student"

# ---------- INPUT SCHEMAS ----------

class SignupIn(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6)
    confirm_password: str = Field(min_length=6)
    role: RoleEnum = RoleEnum.teacher   # default to teacher

    # Student-specific fields (required if role is student)
    class_name: str | None = None
    section: str | None = None


class LoginIn(BaseModel):
    email: EmailStr
    password: str

class ModuleIn(BaseModel):
    name: str
    description: str | None = None
    assessment_type: str

# ---------- OUTPUT SCHEMAS ----------

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum   # auto converts Enum -> string for API response

    # Student-specific fields
    class_name: str | None = None
    section: str | None = None

    class Config:
        from_attributes = True  # SQLAlchemy -> Pydantic conversion
# schemas.py (add below UserOut)

class TeacherProfileIn(BaseModel):
    education: str
    grades_teaching: str
    subjects_teaching: str
    experience_years: int
    board: str 


class TeacherProfileOut(BaseModel):
    id: int
    user_id: int
    education: str
    grades_teaching: str
    subjects_teaching: str
    experience_years: int
    board: str 

    class Config:
        from_attributes = True
# schemas.py (add at bottom)

class ModuleOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    assessment_type: str
    category: str = "knowledge"  # knowledge, portfolio, outcomes
    time_limit_minutes: int | None = 30
    cooldown_hours: int | None = 24
    max_attempts_per_month: int | None = 3

    class Config:
        from_attributes = True
# schemas.py (Phase 4 additions)
from typing import List, Optional

# ---------- MCQ generation / answering ----------

class MCQQuestion(BaseModel):
    id: Optional[int] = None  # Include database ID
    question: str
    options: List[str]
    correct_answer: Optional[str] = None  # keep in API response for admin-only if needed

class GenerateAssessmentOut(BaseModel):
    module_id: int
    module_name: str
    questions: List[MCQQuestion]

class SubmitAnswerIn(BaseModel):
    question_id: int
    selected_answer: str  # e.g., "A"

class SubmitAnswersIn(BaseModel):
    answers: List[SubmitAnswerIn]

class EnhancedSubmitAnswersIn(BaseModel):
    """Enhanced submission with session tracking"""
    session_id: int
    answers: List[SubmitAnswerIn]

class AnswerReview(BaseModel):
    question: str
    options: List[str]
    user_answer: str
    correct_answer: str
    is_correct: bool

class ScoreOut(BaseModel):
    total_questions: int
    correct: int
    score_percent: float
    review: List[AnswerReview]

# ---------- Submissions (CPD / certificates) ----------

class SubmissionCreateOut(BaseModel):
    submission_id: int
    status: str
    ai_suggested_score: int | None = None

class SubmissionValidateIn(BaseModel):
    status: str  # approved/rejected
    admin_validated_score: int

# ---------- Outcomes (placeholder) ----------

class OutcomeIn(BaseModel):
    metric_name: str
    value: float  # e.g., avg improvement percentage

class OutcomeIngestIn(BaseModel):
    entries: List[OutcomeIn]

# schemas.py (Phase 5)
from typing import Dict

class ModuleScore(BaseModel):
    module_id: int
    module_name: str
    assessment_type: str
    score: float
    rating: str

class BenchmarkOut(BaseModel):
    teacher_percentile: float
    cohort_size: int
    cohort_definition: dict  # {"board": "CBSE", "subjects": "...", "grades": "..."}

class PerformanceSummaryOut(BaseModel):
    overall_score: float
    overall_rating: str
    weighted_breakdown: Dict[str, float]  # {"mcq": 78.5, "submission": 65.0, "outcome": 72.0}
    module_scores: list[ModuleScore]
    benchmark: BenchmarkOut

class GrowthPlanIn(BaseModel):
    # optionally let admin force a regeneration with custom focus
    focus_areas: list[str] | None = None

class GrowthPlanOut(BaseModel):
    content: str  # markdown text
    id: int | None = None
    created_at: str | None = None
    expires_at: str | None = None
    actions: list | None = None
    context_summary: dict | None = None

    class Config:
        from_attributes = True


# ============================================================================
# GROWTH PLAN ENHANCEMENT SCHEMAS
# ============================================================================

class ActionOut(BaseModel):
    """Output schema for growth plan action"""
    id: int
    growth_plan_id: int
    action_type: str
    action_title: str
    action_description: str | None = None
    priority: str
    target_date: str | None = None
    estimated_time_minutes: int | None = None
    target_cpd_module_id: int | None = None
    target_cpd_course_id: int | None = None
    target_career_module_id: int | None = None
    external_url: str | None = None
    status: str
    started_at: str | None = None
    completed_at: str | None = None
    time_spent_minutes: int | None = None
    completion_notes: str | None = None
    display_order: int
    created_at: str | None = None

    class Config:
        from_attributes = True


class ActionUpdateRequest(BaseModel):
    """Request to update action status"""
    status: str | None = None
    notes: str | None = None


class ActionCompleteRequest(BaseModel):
    """Request to mark action as completed"""
    notes: str | None = None
    evidence_urls: list[str] | None = None


class GrowthPlanGenerateRequest(BaseModel):
    """Request to generate new growth plan"""
    focus_areas: list[str] | None = None


class RegenerationTriggerOut(BaseModel):
    """Output for regeneration trigger check"""
    should_regenerate: bool
    reason: str | None = None
    urgency: str | None = None


class InsightOut(BaseModel):
    """Output schema for peer insights"""
    id: int
    strategy_type: str
    challenge: str
    solution: str
    outcome: str
    context_tags: list[str] | None = None
    view_count: int
    helpful_count: int
    not_helpful_count: int
    try_count: int
    is_verified: bool
    is_featured: bool
    contributed_by: str | None = None
    created_at: str | None = None

    class Config:
        from_attributes = True


class InsightCreateRequest(BaseModel):
    """Request to create new insight"""
    strategy_type: str
    challenge: str
    solution: str
    outcome: str
    context_tags: list[str] | None = None


class PreferencesOut(BaseModel):
    """Output schema for growth preferences"""
    teacher_id: int
    preferred_timeline: str
    daily_time_commitment: int
    learning_style_preferences: dict | None = None
    reminder_frequency: str
    reminder_time: str
    weekends_included: bool
    email_notifications: bool
    custom_focus_areas: list[str] | None = None

    class Config:
        from_attributes = True


class PreferencesUpdateRequest(BaseModel):
    """Request to update growth preferences"""
    preferred_timeline: str | None = None
    daily_time_commitment: int | None = None
    learning_style_preferences: dict | None = None
    reminder_frequency: str | None = None
    reminder_time: str | None = None
    weekends_included: bool | None = None
    email_notifications: bool | None = None
    custom_focus_areas: list[str] | None = None

# ========== Knowledge Assessment Attempt Tracking Schemas ==========

class QuestionFeedback(BaseModel):
    """Detailed feedback for a single question"""
    question_id: int
    question_text: str
    your_answer: str
    correct_answer: str
    is_correct: bool
    explanation: str  # AI-generated explanation
    topic: str | None = None

class EnhancedAssessmentResult(BaseModel):
    """Enhanced result with attempt tracking and feedback"""
    score_percentage: float
    correct_count: int
    total_questions: int
    time_taken_seconds: int
    attempt_number: int
    improvement: float | None = None  # vs previous attempt
    feedback: List[QuestionFeedback]
    weak_topics: List[str]
    next_attempt_available: datetime | None = None
    attempts_used_this_month: int
    max_attempts_per_month: int

class EligibilityCheck(BaseModel):
    """Check if teacher can attempt assessment"""
    eligible: bool
    reason: str | None = None
    hours_remaining: float | None = None
    days_until_reset: int | None = None
    attempts_used_this_month: int
    max_attempts_per_month: int

class SessionStart(BaseModel):
    """Session info when starting assessment"""
    session_id: int
    attempt_number: int
    started_at: datetime
    expires_at: datetime
    time_limit_minutes: int
    
class EnhancedModuleWithAttempts(ModuleOut):
    """Module with attempt tracking data"""
    attempts_used_this_month: int = 0
    total_attempts: int = 0
    best_score: float | None = None
    latest_score: float | None = None
    next_attempt_available: datetime | None = None
    can_attempt: bool = True
    improvement_rate: float | None = None
