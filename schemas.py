# schemas.py
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

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
