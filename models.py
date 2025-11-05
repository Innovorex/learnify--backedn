# models.py
from sqlalchemy import Column, Integer, String, Enum, DateTime, func, ForeignKey, Text, Boolean, Float
from sqlalchemy.orm import relationship
from database import Base
import enum

# ---------- ROLE ENUM ----------
class Role(str, enum.Enum):
    teacher = "teacher"
    admin = "admin"
    student = "student"

# ---------- USER TABLE ----------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.teacher)

    # Student-specific fields (nullable, only for students)
    class_name = Column(String(10), nullable=True)
    section = Column(String(5), nullable=True)

    created_at = Column(DateTime, server_default=func.now())

    # relationship (1-to-1 with TeacherProfile)
    profile = relationship("TeacherProfile", back_populates="user", uselist=False)

# ---------- TEACHER PROFILE TABLE ----------
class TeacherProfile(Base):
    __tablename__ = "teacher_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    education = Column(String(255), nullable=False)
    grades_teaching = Column(String(100), nullable=False)   # e.g., "Grade 6, Grade 7"
    subjects_teaching = Column(String(100), nullable=False) # e.g., "Math, Science"
    experience_years = Column(Integer, nullable=False)
    board = Column(String(50), nullable=False)
    state = Column(String(50), nullable=True, default="Telangana")  # State for curriculum fetching

    user = relationship("User", back_populates="profile")

# ---------- SYLLABUS CACHE TABLE ----------
class SyllabusCache(Base):
    __tablename__ = "syllabus_cache"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(String(50), nullable=False, index=True)
    board = Column(String(50), nullable=False, index=True)
    grade = Column(String(10), nullable=False, index=True)
    subject = Column(String(100), nullable=False, index=True)

    syllabus_data = Column(Text, nullable=False)  # JSON string
    fetched_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

# models.py (add after TeacherProfile)

class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    assessment_type = Column(String(20), nullable=False, default="mcq")
    # values: "mcq", "submission", "outcome"
    category = Column(String(20), nullable=False, default="knowledge")
    # values: "knowledge" (mcq tests), "portfolio" (submissions), "outcomes" (student impact)

    # Timer and cooldown settings (for knowledge assessments)
    time_limit_minutes = Column(Integer, nullable=True, default=30)
    cooldown_hours = Column(Integer, nullable=True, default=24)
    max_attempts_per_month = Column(Integer, nullable=True, default=3)
# models.py (Phase 4 additions)
from sqlalchemy import Text, Boolean, Float, DateTime
from sqlalchemy.sql import func

# Store generated questions per (teacher,module) set
class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), index=True, nullable=False)

    question = Column(Text, nullable=False)
    options_json = Column(Text, nullable=False)        # JSON list of options
    correct_answer = Column(String(10), nullable=True) # e.g., "A" or text
    created_at = Column(DateTime, server_default=func.now())

# Store answers submitted by teacher
class AssessmentResponse(Base):
    __tablename__ = "assessment_responses"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), index=True, nullable=False)
    question_id = Column(Integer, ForeignKey("assessment_questions.id", ondelete="CASCADE"), nullable=False)

    selected_answer = Column(String(10), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

# Evidence uploads (certificates/CPD logs)
class TeacherSubmission(Base):
    __tablename__ = "teacher_submissions"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), index=True, nullable=False)

    file_path = Column(String, nullable=True)      # saved path
    notes = Column(Text, nullable=True)
    extracted_text = Column(Text, nullable=True)   # AI OCR/extraction (optional)
    ai_suggested_score = Column(Integer, nullable=True)
    admin_validated_score = Column(Integer, nullable=True)
    status = Column(String(20), nullable=False, default="pending")  # pending/approved/rejected
    created_at = Column(DateTime, server_default=func.now())

# Final per-module performance summary
class Performance(Base):
    __tablename__ = "performance"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), index=True, nullable=False)

    score = Column(Float, nullable=False)      # 0-100
    rating = Column(String(20), nullable=False)  # Excellent/Good/Needs Improvement etc.
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

# models.py (Phase 5)
class GrowthPlan(Base):
    __tablename__ = "growth_plans"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    content = Column(Text, nullable=False)  # markdown/JSON text from AI
    created_at = Column(DateTime, server_default=func.now())

    # Enhanced fields
    generated_context = Column(Text, nullable=True)  # JSON string of context used
    plan_version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True, index=True)
    expires_at = Column(DateTime, nullable=True)

    # Relationships
    actions = relationship("GrowthPlanAction", back_populates="growth_plan", cascade="all, delete-orphan")

# models.py (Phase 6 addition)
class PerformanceHistory(Base):
    __tablename__ = "performance_history"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), index=True, nullable=False)

    score = Column(Float, nullable=False)
    rating = Column(String(20), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

# ============================================================================
# CAREER PROGRESSION MODELS - B.Ed/M.Ed Course Management
# ============================================================================

# 1. Career Courses (B.Ed, M.Ed degree programs)
class CareerCourse(Base):
    __tablename__ = "career_courses"

    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String(255), nullable=False)  # "B.Ed Mathematics"
    course_type = Column(String(50), nullable=False)   # "B.Ed", "M.Ed", "D.El.Ed"
    subject = Column(String(100), nullable=False)      # "Mathematics", "Science"
    university = Column(String(100), nullable=False)   # "IGNOU", "NIOS"
    duration_months = Column(Integer, nullable=False)  # 24 months
    description = Column(Text, nullable=True)
    total_modules = Column(Integer, nullable=False)    # 8 modules
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    modules = relationship("CourseModule", back_populates="course", cascade="all, delete-orphan")
    enrollments = relationship("TeacherCareerEnrollment", back_populates="course")

# 2. Course Modules (modules within a career course)
class CourseModule(Base):
    __tablename__ = "course_modules"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("career_courses.id", ondelete="CASCADE"), index=True, nullable=False)
    module_number = Column(Integer, nullable=False)    # 1, 2, 3...8
    module_name = Column(String(255), nullable=False)  # "Childhood and Growing Up"
    description = Column(Text, nullable=True)
    duration_weeks = Column(Integer, nullable=True)    # 4 weeks
    exam_required = Column(Boolean, default=True)
    passing_score = Column(Integer, default=60)        # 60% to pass
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    course = relationship("CareerCourse", back_populates="modules")
    topics = relationship("ModuleTopic", back_populates="module", cascade="all, delete-orphan")
    progress_records = relationship("ModuleProgress", back_populates="module")
    exam_questions = relationship("ModuleExamQuestion", back_populates="module", cascade="all, delete-orphan")

# 3. Module Topics (study content: notes + videos)
class ModuleTopic(Base):
    __tablename__ = "module_topics"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("course_modules.id", ondelete="CASCADE"), index=True, nullable=False)
    topic_number = Column(Integer, nullable=False)     # 1, 2, 3...
    topic_name = Column(String(255), nullable=False)   # "Introduction to Child Development"
    content_text = Column(Text, nullable=True)         # Study notes
    video_url = Column(String(500), nullable=True)     # YouTube embed URL
    video_duration = Column(String(20), nullable=True) # "18:45"
    additional_resources = Column(Text, nullable=True) # JSON string
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    module = relationship("CourseModule", back_populates="topics")
    progress_records = relationship("TopicProgress", back_populates="topic")

# 4. Teacher Career Enrollments (track enrollments in courses)
class TeacherCareerEnrollment(Base):
    __tablename__ = "teacher_career_enrollments"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    course_id = Column(Integer, ForeignKey("career_courses.id", ondelete="CASCADE"), index=True, nullable=False)
    enrollment_date = Column(DateTime, server_default=func.now())
    status = Column(String(50), default="in_progress")  # 'in_progress', 'completed', 'dropped'
    current_module_id = Column(Integer, ForeignKey("course_modules.id"), nullable=True)
    completion_date = Column(DateTime, nullable=True)
    overall_score = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    course = relationship("CareerCourse", back_populates="enrollments")
    module_progress = relationship("ModuleProgress", back_populates="enrollment", cascade="all, delete-orphan")
    topic_progress = relationship("TopicProgress", back_populates="enrollment", cascade="all, delete-orphan")
    certificate = relationship("CourseCertificate", back_populates="enrollment", uselist=False)

# 5. Module Progress (track progress per module)
class ModuleProgress(Base):
    __tablename__ = "module_progress"

    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("teacher_career_enrollments.id", ondelete="CASCADE"), index=True, nullable=False)
    module_id = Column(Integer, ForeignKey("course_modules.id", ondelete="CASCADE"), index=True, nullable=False)
    status = Column(String(50), default="not_started")  # 'not_started', 'in_progress', 'completed'
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    exam_score = Column(Float, nullable=True)
    exam_attempts = Column(Integer, default=0)
    passed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    enrollment = relationship("TeacherCareerEnrollment", back_populates="module_progress")
    module = relationship("CourseModule", back_populates="progress_records")
    exam_responses = relationship("ModuleExamResponse", back_populates="module_progress")

# 6. Topic Progress (track which topics completed)
class TopicProgress(Base):
    __tablename__ = "topic_progress"

    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("teacher_career_enrollments.id", ondelete="CASCADE"), index=True, nullable=False)
    topic_id = Column(Integer, ForeignKey("module_topics.id", ondelete="CASCADE"), index=True, nullable=False)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    enrollment = relationship("TeacherCareerEnrollment", back_populates="topic_progress")
    topic = relationship("ModuleTopic", back_populates="progress_records")

# 7. Module Exam Questions (AI-generated exam questions)
class ModuleExamQuestion(Base):
    __tablename__ = "module_exam_questions"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("course_modules.id", ondelete="CASCADE"), index=True, nullable=False)
    question = Column(Text, nullable=False)
    options_json = Column(Text, nullable=False)         # JSON array
    correct_answer = Column(String(10), nullable=False) # "A", "B", "C", "D"
    difficulty = Column(String(20), default="medium")   # "easy", "medium", "hard"
    topic_reference = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    module = relationship("CourseModule", back_populates="exam_questions")
    responses = relationship("ModuleExamResponse", back_populates="question")

# 8. Module Exam Responses (teacher's answers)
class ModuleExamResponse(Base):
    __tablename__ = "module_exam_responses"

    id = Column(Integer, primary_key=True, index=True)
    module_progress_id = Column(Integer, ForeignKey("module_progress.id", ondelete="CASCADE"), index=True, nullable=False)
    question_id = Column(Integer, ForeignKey("module_exam_questions.id", ondelete="CASCADE"), index=True, nullable=False)
    selected_answer = Column(String(10), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    exam_attempt = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    module_progress = relationship("ModuleProgress", back_populates="exam_responses")
    question = relationship("ModuleExamQuestion", back_populates="responses")

# 9. Course Certificates (issued certificates)
class CourseCertificate(Base):
    __tablename__ = "course_certificates"

    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("teacher_career_enrollments.id", ondelete="CASCADE"), unique=True, nullable=False)
    certificate_number = Column(String(50), unique=True, nullable=False)
    issued_date = Column(DateTime, server_default=func.now())
    pdf_path = Column(String(500), nullable=True)
    verification_code = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    enrollment = relationship("TeacherCareerEnrollment", back_populates="certificate")


# ============================================================================
# GROWTH PLAN ENHANCEMENT MODELS
# ============================================================================

class GrowthPlanAction(Base):
    """Individual actionable items within a growth plan"""
    __tablename__ = "growth_plan_actions"

    id = Column(Integer, primary_key=True, index=True)
    growth_plan_id = Column(Integer, ForeignKey("growth_plans.id", ondelete="CASCADE"), nullable=False, index=True)

    # Action Classification
    action_type = Column(String(50), nullable=False, index=True)
    # Values: 'retake_cpd_module', 'enroll_cpd_course', 'complete_career_module',
    #         'use_ai_tutor', 'upload_material', 'create_k12_assessment'

    # Action Details
    action_title = Column(String(255), nullable=False)
    action_description = Column(Text, nullable=True)
    priority = Column(String(20), default="medium", index=True)  # 'high', 'medium', 'low'
    target_date = Column(DateTime, nullable=True)
    estimated_time_minutes = Column(Integer, nullable=True)

    # Target Resource Links
    target_cpd_module_id = Column(Integer, ForeignKey("modules.id", ondelete="SET NULL"), nullable=True)
    target_cpd_course_id = Column(Integer, nullable=True)
    target_career_module_id = Column(Integer, ForeignKey("course_modules.id", ondelete="SET NULL"), nullable=True)
    external_url = Column(String(500), nullable=True)

    # Progress Tracking
    status = Column(String(20), default="pending", index=True)  # 'pending', 'in_progress', 'completed', 'skipped'
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    time_spent_minutes = Column(Integer, nullable=True)

    # Reflection & Evidence
    completion_notes = Column(Text, nullable=True)
    evidence_urls = Column(Text, nullable=True)  # JSON string array

    # Ordering
    display_order = Column(Integer, default=0)

    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    growth_plan = relationship("GrowthPlan", back_populates="actions")
    cpd_module = relationship("Module", foreign_keys=[target_cpd_module_id])
    career_module = relationship("CourseModule", foreign_keys=[target_career_module_id])


class GrowthPlanInsight(Base):
    """Community-shared success strategies (anonymized)"""
    __tablename__ = "growth_plan_insights"

    id = Column(Integer, primary_key=True, index=True)

    # Insight Classification
    strategy_type = Column(String(50), nullable=False, index=True)
    # Values: 'cpd_improvement', 'career_completion', 'ai_tutor_usage',
    #         'material_creation', 'assessment_design'

    # Challenge-Solution-Outcome Framework
    challenge = Column(String(255), nullable=False)
    solution = Column(Text, nullable=False)
    outcome = Column(Text, nullable=False)
    context_tags = Column(Text, nullable=True)  # JSON string array

    # Engagement Metrics
    view_count = Column(Integer, default=0)
    helpful_count = Column(Integer, default=0)
    not_helpful_count = Column(Integer, default=0)
    try_count = Column(Integer, default=0)

    # Quality Control
    is_verified = Column(Boolean, default=False, index=True)
    is_featured = Column(Boolean, default=False, index=True)
    verified_by_admin_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    verified_at = Column(DateTime, nullable=True)

    # Privacy (no teacher_id for anonymity)
    contributed_by = Column(String(100), nullable=True)

    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class GrowthPlanRegeneration(Base):
    """Track when and why growth plans were regenerated"""
    __tablename__ = "growth_plan_regenerations"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    old_growth_plan_id = Column(Integer, ForeignKey("growth_plans.id", ondelete="SET NULL"), nullable=True)
    new_growth_plan_id = Column(Integer, ForeignKey("growth_plans.id", ondelete="CASCADE"), nullable=False)

    trigger_reason = Column(String(100), nullable=False, index=True)
    # 'time_based', 'all_actions_completed', 'new_assessment',
    # 'score_change', 'career_enrollment', 'manual'

    trigger_metadata = Column(Text, nullable=True)  # JSON string

    created_at = Column(DateTime, server_default=func.now())


class TeacherGrowthPreferences(Base):
    """Store user preferences for growth plan customization"""
    __tablename__ = "teacher_growth_preferences"

    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    # Learning Preferences
    preferred_timeline = Column(String(20), default="30day")  # '2week', '30day', '90day'
    daily_time_commitment = Column(Integer, default=30)  # minutes per day
    learning_style_preferences = Column(Text, nullable=True)  # JSON string

    # Notification Settings
    reminder_frequency = Column(String(20), default="daily")  # 'none', 'daily', 'weekly'
    reminder_time = Column(String(10), default="09:00")
    weekends_included = Column(Boolean, default=False)
    email_notifications = Column(Boolean, default=True)

    # Focus Areas
    custom_focus_areas = Column(Text, nullable=True)  # JSON string array

    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


# ============================================================================
# NCERT TEXTBOOK CONTENT EXTRACTION MODELS
# ============================================================================

class NCERTTextbookContent(Base):
    """Main textbook content extracted from NCERT PDFs"""
    __tablename__ = "ncert_textbook_content"

    id = Column(Integer, primary_key=True, index=True)

    # Linking to syllabus
    board = Column(String(50), nullable=False, default="CBSE", index=True)
    grade = Column(Integer, nullable=False, index=True)
    subject = Column(String(100), nullable=False, index=True)
    chapter_number = Column(Integer, nullable=True)
    chapter_name = Column(String(200), nullable=False, index=True)
    section_name = Column(String(200), nullable=True)
    topic_name = Column(String(200), nullable=True, index=True)

    # Content details
    content_type = Column(String(50), nullable=False, index=True)
    # Values: 'explanation', 'definition', 'theorem', 'activity', 'note', 'summary'

    content_text = Column(Text, nullable=False)  # Extracted text (markdown formatted)
    content_html = Column(Text, nullable=True)   # HTML formatted version

    # Metadata flags
    has_formulas = Column(Boolean, default=False)
    has_images = Column(Boolean, default=False)
    has_tables = Column(Boolean, default=False)

    # Source tracking
    page_start = Column(Integer, nullable=True)
    page_end = Column(Integer, nullable=True)
    extraction_method = Column(String(50), nullable=False)
    # Values: 'pdf_extract', 'ocr', 'manual'

    # Quality assurance
    is_reviewed = Column(Boolean, default=False)
    reviewed_by = Column(String(100), nullable=True)
    quality_score = Column(Float, nullable=True)  # 0-100

    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    images = relationship("NCERTImage", back_populates="content", cascade="all, delete-orphan")
    examples = relationship("NCERTExample", back_populates="content")


class NCERTExample(Base):
    """Solved examples extracted from NCERT textbooks"""
    __tablename__ = "ncert_examples"

    id = Column(Integer, primary_key=True, index=True)

    # Linking
    content_id = Column(Integer, ForeignKey("ncert_textbook_content.id", ondelete="CASCADE"), nullable=True, index=True)
    grade = Column(Integer, nullable=False, index=True)
    subject = Column(String(100), nullable=False, index=True)
    chapter_name = Column(String(200), nullable=False, index=True)

    # Example details
    example_number = Column(String(20), nullable=True)  # "Example 1", "Example 2.1"
    example_title = Column(String(200), nullable=True)

    # Content (verbatim from textbook)
    problem_statement = Column(Text, nullable=False)
    solution_text = Column(Text, nullable=False)
    solution_steps = Column(Text, nullable=True)  # JSON array of step-by-step solution

    # Metadata
    has_diagrams = Column(Boolean, default=False)
    difficulty_level = Column(String(20), nullable=True)  # 'easy', 'medium', 'hard'
    page_number = Column(Integer, nullable=True)

    # Quality assurance
    is_reviewed = Column(Boolean, default=False)

    # Metadata
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    content = relationship("NCERTTextbookContent", back_populates="examples")


class NCERTExercise(Base):
    """Exercise questions extracted from NCERT textbooks"""
    __tablename__ = "ncert_exercises"

    id = Column(Integer, primary_key=True, index=True)

    # Linking
    grade = Column(Integer, nullable=False, index=True)
    subject = Column(String(100), nullable=False, index=True)
    chapter_name = Column(String(200), nullable=False, index=True)

    # Exercise details
    exercise_number = Column(String(20), nullable=True)  # "Exercise 1.1", "Exercise 2.3"
    question_number = Column(String(20), nullable=False)  # "1", "2(a)", "3(ii)"

    # Question content (exact from textbook)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=True)
    # Values: 'mcq', 'short_answer', 'long_answer', 'numerical', 'proof'

    # Answer (if provided in textbook)
    answer_text = Column(Text, nullable=True)
    hints = Column(Text, nullable=True)

    # Metadata
    has_diagrams = Column(Boolean, default=False)
    difficulty_level = Column(String(20), nullable=True)
    page_number = Column(Integer, nullable=True)

    # Quality assurance
    is_reviewed = Column(Boolean, default=False)

    # Metadata
    created_at = Column(DateTime, server_default=func.now())


class NCERTImage(Base):
    """Images, diagrams, and figures extracted from NCERT textbooks"""
    __tablename__ = "ncert_images"

    id = Column(Integer, primary_key=True, index=True)

    # Linking
    content_id = Column(Integer, ForeignKey("ncert_textbook_content.id", ondelete="SET NULL"), nullable=True, index=True)
    grade = Column(Integer, nullable=False, index=True)
    subject = Column(String(100), nullable=False, index=True)
    chapter_name = Column(String(200), nullable=False)

    # Image details
    image_type = Column(String(50), nullable=False)
    # Values: 'diagram', 'graph', 'photo', 'illustration', 'table'

    figure_number = Column(String(20), nullable=True)  # "Figure 1.1"
    caption = Column(Text, nullable=True)

    # File storage
    file_path = Column(String(500), nullable=False)  # Local storage path
    file_format = Column(String(20), nullable=True)  # 'png', 'jpg', 'svg'
    file_size_kb = Column(Integer, nullable=True)

    # Image metadata
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    page_number = Column(Integer, nullable=True)

    # Quality assurance
    is_reviewed = Column(Boolean, default=False)
    alt_text = Column(Text, nullable=True)  # Accessibility description

    # Metadata
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    content = relationship("NCERTTextbookContent", back_populates="images")


class NCERTActivity(Base):
    """Activity boxes and 'Try This' sections from NCERT textbooks"""
    __tablename__ = "ncert_activities"

    id = Column(Integer, primary_key=True, index=True)

    # Linking
    grade = Column(Integer, nullable=False, index=True)
    subject = Column(String(100), nullable=False, index=True)
    chapter_name = Column(String(200), nullable=False, index=True)

    # Activity details
    activity_type = Column(String(50), nullable=False)
    # Values: 'activity', 'think_discuss', 'do_you_know', 'try_this', 'project'

    activity_title = Column(String(200), nullable=True)
    activity_text = Column(Text, nullable=False)

    # Instructions and objectives
    instructions = Column(Text, nullable=True)
    learning_objective = Column(Text, nullable=True)
    materials_needed = Column(Text, nullable=True)  # JSON array

    # Metadata
    page_number = Column(Integer, nullable=True)
    estimated_time_minutes = Column(Integer, nullable=True)

    # Quality assurance
    is_reviewed = Column(Boolean, default=False)

    # Metadata
    created_at = Column(DateTime, server_default=func.now())


class NCERTPDFSource(Base):
    """Track NCERT PDF sources and extraction status"""
    __tablename__ = "ncert_pdf_sources"

    id = Column(Integer, primary_key=True, index=True)

    # Source identification
    grade = Column(Integer, nullable=False, index=True)
    subject = Column(String(100), nullable=False, index=True)
    book_name = Column(String(200), nullable=False)

    # PDF details
    pdf_url = Column(String(500), nullable=False)  # NCERT official URL
    local_path = Column(String(500), nullable=True)  # Downloaded location
    file_size_mb = Column(Float, nullable=True)
    total_pages = Column(Integer, nullable=True)

    # Extraction status
    extraction_status = Column(String(50), default="pending", index=True)
    # Values: 'pending', 'downloading', 'downloaded', 'extracting', 'completed', 'failed'

    extraction_started_at = Column(DateTime, nullable=True)
    extraction_completed_at = Column(DateTime, nullable=True)

    # Statistics
    total_content_items = Column(Integer, default=0)
    total_examples = Column(Integer, default=0)
    total_exercises = Column(Integer, default=0)
    total_images = Column(Integer, default=0)
    total_activities = Column(Integer, default=0)

    # Error tracking
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)

    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
