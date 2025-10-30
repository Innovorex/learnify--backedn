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

    # relationship (1-to-many with TeachingMaterial)
    teaching_materials = relationship("TeachingMaterial", back_populates="teacher")

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
