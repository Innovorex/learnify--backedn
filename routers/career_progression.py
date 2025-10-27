"""
Career Progression API Router
Handles B.Ed/M.Ed course enrollments, progress tracking, exams, and certificates
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
import json

from database import get_db
from models import (
    User, TeacherProfile, CareerCourse, CourseModule, ModuleTopic,
    TeacherCareerEnrollment, ModuleProgress, TopicProgress,
    ModuleExamQuestion, ModuleExamResponse, CourseCertificate
)
from security import require_role
from services.career_detector import detect_recommended_course, check_enrollment_eligibility
from services.module_exam_generator import generate_module_exam_questions, get_exam_questions_for_module

router = APIRouter(prefix="/career-progression", tags=["career-progression"])


# ============================================================================
# Request/Response Models
# ============================================================================
class ExamAnswer(BaseModel):
    question_id: int
    selected_answer: str

class ExamSubmission(BaseModel):
    answers: List[ExamAnswer]


# ============================================================================
# ENDPOINT 1: Get Recommended Course
# ============================================================================
@router.get("/recommend")
async def get_recommended_course(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Detect teacher's qualification and recommend appropriate next course
    """
    # Get teacher profile
    profile = db.query(TeacherProfile).filter_by(user_id=user.id).first()
    if not profile:
        raise HTTPException(400, "Please complete your teacher profile first")

    # Detect recommended course
    recommendation = detect_recommended_course(
        education=profile.education,
        subject=profile.subjects_teaching,
        db=db
    )

    return recommendation


# ============================================================================
# ENDPOINT 2: Enroll in Course
# ============================================================================
@router.post("/enroll/{course_id}")
async def enroll_in_course(
    course_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Enroll teacher in a career course (B.Ed/M.Ed)
    """
    # Check if course exists
    course = db.query(CareerCourse).filter_by(id=course_id, is_active=True).first()
    if not course:
        raise HTTPException(404, "Course not found")

    # Check eligibility
    is_eligible, message = check_enrollment_eligibility(user.id, course_id, db)
    if not is_eligible:
        raise HTTPException(400, message)

    # Create enrollment
    enrollment = TeacherCareerEnrollment(
        teacher_id=user.id,
        course_id=course_id,
        status="in_progress"
    )
    db.add(enrollment)
    db.flush()

    # Get all modules for this course
    modules = db.query(CourseModule).filter_by(course_id=course_id).order_by(CourseModule.module_number).all()

    # Create ModuleProgress records for all modules
    for i, module in enumerate(modules):
        module_progress = ModuleProgress(
            enrollment_id=enrollment.id,
            module_id=module.id,
            status="in_progress" if i == 0 else "not_started"  # Unlock first module
        )
        db.add(module_progress)

    # Set current module to first module
    if modules:
        enrollment.current_module_id = modules[0].id

    db.commit()
    db.refresh(enrollment)

    return {
        "enrollment_id": enrollment.id,
        "course_name": course.course_name,
        "status": "enrolled",
        "message": "Successfully enrolled in course",
        "current_module": modules[0].module_name if modules else None
    }


# ============================================================================
# ENDPOINT 3: Get My Enrolled Courses
# ============================================================================
@router.get("/my-courses")
async def get_my_courses(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Get all courses the teacher is enrolled in with progress
    """
    enrollments = db.query(TeacherCareerEnrollment).filter_by(
        teacher_id=user.id
    ).all()

    result = []
    for enrollment in enrollments:
        course = enrollment.course

        # Count completed modules
        completed_modules = db.query(ModuleProgress).filter(
            ModuleProgress.enrollment_id == enrollment.id,
            ModuleProgress.status == "completed"
        ).count()

        total_modules = course.total_modules
        progress_percentage = round((completed_modules / total_modules) * 100, 1) if total_modules > 0 else 0

        # Get current module info
        current_module = None
        if enrollment.current_module_id:
            current_mod = db.query(CourseModule).filter_by(id=enrollment.current_module_id).first()
            if current_mod:
                current_module = {
                    "id": current_mod.id,
                    "module_number": current_mod.module_number,
                    "name": current_mod.module_name
                }

        result.append({
            "enrollment_id": enrollment.id,
            "course": {
                "id": course.id,
                "name": course.course_name,
                "type": course.course_type,
                "university": course.university,
                "duration_months": course.duration_months,
                "total_modules": course.total_modules
            },
            "status": enrollment.status,
            "progress_percentage": progress_percentage,
            "modules_completed": completed_modules,
            "total_modules": total_modules,
            "current_module": current_module,
            "enrollment_date": enrollment.enrollment_date.isoformat(),
            "completion_date": enrollment.completion_date.isoformat() if enrollment.completion_date else None
        })

    return result


# ============================================================================
# ENDPOINT 4: Get Course Modules with Progress
# ============================================================================
@router.get("/course/{course_id}/modules")
async def get_course_modules(
    course_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Get all modules for a course with teacher's progress
    """
    # Check if course exists
    course = db.query(CareerCourse).filter_by(id=course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")

    # Get teacher's enrollment
    enrollment = db.query(TeacherCareerEnrollment).filter_by(
        teacher_id=user.id,
        course_id=course_id
    ).first()

    if not enrollment:
        raise HTTPException(400, "You are not enrolled in this course")

    # Get all modules
    modules = db.query(CourseModule).filter_by(course_id=course_id).order_by(CourseModule.module_number).all()

    result_modules = []
    previous_completed = True

    for module in modules:
        # Get progress for this module
        progress = db.query(ModuleProgress).filter_by(
            enrollment_id=enrollment.id,
            module_id=module.id
        ).first()

        # Module is locked if previous module not completed
        is_locked = not previous_completed and progress.status != "completed"

        result_modules.append({
            "id": module.id,
            "module_number": module.module_number,
            "module_name": module.module_name,
            "description": module.description,
            "duration_weeks": module.duration_weeks,
            "passing_score": module.passing_score,
            "status": progress.status if progress else "not_started",
            "exam_score": progress.exam_score if progress else None,
            "exam_attempts": progress.exam_attempts if progress else 0,
            "passed": progress.passed if progress else False,
            "is_locked": is_locked,
            "started_at": progress.started_at.isoformat() if progress and progress.started_at else None,
            "completed_at": progress.completed_at.isoformat() if progress and progress.completed_at else None
        })

        # Update for next iteration
        if progress and progress.status == "completed":
            previous_completed = True
        else:
            previous_completed = False

    return {
        "course": {
            "id": course.id,
            "name": course.course_name,
            "university": course.university,
            "total_modules": course.total_modules,
            "enrollment_id": enrollment.id
        },
        "enrollment_status": enrollment.status,
        "modules": result_modules
    }


# ============================================================================
# ENDPOINT 5: Get Module Content (Topics, Notes, Videos)
# ============================================================================
@router.get("/module/{module_id}/content")
async def get_module_content(
    module_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Get all topics for a module with notes, videos, and progress
    """
    # Get module
    module = db.query(CourseModule).filter_by(id=module_id).first()
    if not module:
        raise HTTPException(404, "Module not found")

    # Get teacher's enrollment for this course
    enrollment = db.query(TeacherCareerEnrollment).filter_by(
        teacher_id=user.id,
        course_id=module.course_id
    ).first()

    if not enrollment:
        raise HTTPException(400, "You are not enrolled in this course")

    # Get all topics for this module
    topics = db.query(ModuleTopic).filter_by(module_id=module_id).order_by(ModuleTopic.topic_number).all()

    result_topics = []
    topics_completed = 0

    for topic in topics:
        # Check if topic is completed
        topic_progress = db.query(TopicProgress).filter_by(
            enrollment_id=enrollment.id,
            topic_id=topic.id
        ).first()

        is_completed = topic_progress.completed if topic_progress else False
        if is_completed:
            topics_completed += 1

        # Parse additional resources if present
        additional_resources = None
        if topic.additional_resources:
            try:
                additional_resources = json.loads(topic.additional_resources)
            except:
                additional_resources = None

        result_topics.append({
            "id": topic.id,
            "topic_number": topic.topic_number,
            "topic_name": topic.topic_name,
            "content_text": topic.content_text,
            "video_url": topic.video_url,
            "video_duration": topic.video_duration,
            "additional_resources": additional_resources,
            "completed": is_completed,
            "completed_at": topic_progress.completed_at.isoformat() if topic_progress and topic_progress.completed_at else None
        })

    total_topics = len(topics)
    progress_percentage = round((topics_completed / total_topics) * 100, 1) if total_topics > 0 else 0

    return {
        "module": {
            "id": module.id,
            "module_number": module.module_number,
            "module_name": module.module_name,
            "description": module.description,
            "duration_weeks": module.duration_weeks
        },
        "topics": result_topics,
        "progress": {
            "topics_completed": topics_completed,
            "total_topics": total_topics,
            "percentage": progress_percentage
        }
    }


# ============================================================================
# ENDPOINT 6: Mark Topic as Complete
# ============================================================================
@router.post("/topic/{topic_id}/complete")
async def mark_topic_complete(
    topic_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Mark a topic as completed by the teacher
    """
    # Get topic
    topic = db.query(ModuleTopic).filter_by(id=topic_id).first()
    if not topic:
        raise HTTPException(404, "Topic not found")

    # Get enrollment
    enrollment = db.query(TeacherCareerEnrollment).filter_by(
        teacher_id=user.id,
        course_id=topic.module.course_id
    ).first()

    if not enrollment:
        raise HTTPException(400, "You are not enrolled in this course")

    # Check if already completed
    topic_progress = db.query(TopicProgress).filter_by(
        enrollment_id=enrollment.id,
        topic_id=topic_id
    ).first()

    if topic_progress:
        if not topic_progress.completed:
            topic_progress.completed = True
            topic_progress.completed_at = datetime.utcnow()
    else:
        topic_progress = TopicProgress(
            enrollment_id=enrollment.id,
            topic_id=topic_id,
            completed=True,
            completed_at=datetime.utcnow()
        )
        db.add(topic_progress)

    db.commit()

    # Calculate module progress
    total_topics = db.query(ModuleTopic).filter_by(module_id=topic.module_id).count()
    completed_topics = db.query(TopicProgress).filter(
        TopicProgress.enrollment_id == enrollment.id,
        TopicProgress.topic_id.in_(
            db.query(ModuleTopic.id).filter_by(module_id=topic.module_id)
        ),
        TopicProgress.completed == True
    ).count()

    progress_percentage = round((completed_topics / total_topics) * 100, 1) if total_topics > 0 else 0

    # Update module progress status if needed
    module_progress = db.query(ModuleProgress).filter_by(
        enrollment_id=enrollment.id,
        module_id=topic.module_id
    ).first()

    if module_progress and module_progress.status == "not_started":
        module_progress.status = "in_progress"
        module_progress.started_at = datetime.utcnow()
        db.commit()

    return {
        "success": True,
        "topic_completed": True,
        "module_progress_percentage": progress_percentage,
        "topics_completed": completed_topics,
        "total_topics": total_topics
    }


# ============================================================================
# ENDPOINT 7: Start Module Exam
# ============================================================================
@router.post("/module/{module_id}/start-exam")
async def start_module_exam(
    module_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Generate and start exam for a module (25 questions)
    """
    # Get module
    module = db.query(CourseModule).filter_by(id=module_id).first()
    if not module:
        raise HTTPException(404, "Module not found")

    # Get enrollment
    enrollment = db.query(TeacherCareerEnrollment).filter_by(
        teacher_id=user.id,
        course_id=module.course_id
    ).first()

    if not enrollment:
        raise HTTPException(400, "You are not enrolled in this course")

    # Get module progress
    module_progress = db.query(ModuleProgress).filter_by(
        enrollment_id=enrollment.id,
        module_id=module_id
    ).first()

    if not module_progress:
        raise HTTPException(400, "Module progress not found")

    # Check if module is locked (previous module must be completed)
    previous_module = db.query(CourseModule).filter_by(
        course_id=module.course_id,
        module_number=module.module_number - 1
    ).first()

    if previous_module:
        previous_progress = db.query(ModuleProgress).filter_by(
            enrollment_id=enrollment.id,
            module_id=previous_module.id
        ).first()

        if not previous_progress or previous_progress.status != "completed" or not previous_progress.passed:
            raise HTTPException(400, "This module is locked. Complete previous module first.")

    # Generate or get existing exam questions (10 questions)
    questions = generate_module_exam_questions(module, db, n_questions=10, force_regenerate=False)

    if not questions:
        raise HTTPException(500, "Failed to generate exam questions")

    # Return only first 10 questions WITHOUT correct answers
    exam_questions = [
        {
            "id": q["id"],
            "question": q["question"],
            "options": q["options"]
        }
        for q in questions[:10]  # Take only first 10
    ]

    return exam_questions


# ============================================================================
# ENDPOINT 8: Submit Module Exam
# ============================================================================
@router.post("/module/{module_id}/submit-exam")
async def submit_module_exam(
    module_id: int,
    submission: ExamSubmission,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Submit exam answers and calculate score
    """
    # Get module
    module = db.query(CourseModule).filter_by(id=module_id).first()
    if not module:
        raise HTTPException(404, "Module not found")

    # Get enrollment
    enrollment = db.query(TeacherCareerEnrollment).filter_by(
        teacher_id=user.id,
        course_id=module.course_id
    ).first()

    if not enrollment:
        raise HTTPException(400, "You are not enrolled in this course")

    # Get module progress
    module_progress = db.query(ModuleProgress).filter_by(
        enrollment_id=enrollment.id,
        module_id=module_id
    ).first()

    if not module_progress:
        raise HTTPException(400, "Module progress not found")

    # Get questions with correct answers
    question_ids = [ans.question_id for ans in submission.answers]
    questions = db.query(ModuleExamQuestion).filter(
        ModuleExamQuestion.id.in_(question_ids)
    ).all()

    questions_map = {q.id: q for q in questions}

    # Calculate score
    correct_count = 0
    total_questions = len(submission.answers)
    detailed_review = []

    exam_attempt = module_progress.exam_attempts + 1

    for answer in submission.answers:
        question_id = answer.question_id
        selected_answer = str(answer.selected_answer).strip().upper()

        if question_id not in questions_map:
            continue

        question = questions_map[question_id]
        correct_answer = question.correct_answer.strip().upper()

        # Normalize answers (extract just letter)
        if selected_answer.startswith('('):
            selected_answer = selected_answer[1]
        if ')' in selected_answer:
            selected_answer = selected_answer.split(')')[0]
        selected_answer = selected_answer[0] if selected_answer else ""

        is_correct = selected_answer == correct_answer
        if is_correct:
            correct_count += 1

        # Save response
        response = ModuleExamResponse(
            module_progress_id=module_progress.id,
            question_id=question_id,
            selected_answer=selected_answer,
            is_correct=is_correct,
            exam_attempt=exam_attempt
        )
        db.add(response)

        detailed_review.append({
            "question": question.question,
            "options": json.loads(question.options_json),
            "selected_answer": selected_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })

    # Calculate final score
    score = round((correct_count / total_questions) * 100, 1) if total_questions > 0 else 0
    passed = score >= module.passing_score

    # Update module progress
    module_progress.exam_score = score
    module_progress.exam_attempts += 1
    module_progress.passed = passed

    if passed:
        module_progress.status = "completed"
        module_progress.completed_at = datetime.utcnow()

        # Unlock next module
        next_module = db.query(CourseModule).filter_by(
            course_id=module.course_id,
            module_number=module.module_number + 1
        ).first()

        if next_module:
            next_progress = db.query(ModuleProgress).filter_by(
                enrollment_id=enrollment.id,
                module_id=next_module.id
            ).first()
            if next_progress:
                next_progress.status = "in_progress"
                next_progress.started_at = datetime.utcnow()

            # Update current module
            enrollment.current_module_id = next_module.id
        else:
            # All modules completed - mark course as completed
            enrollment.status = "completed"
            enrollment.completion_date = datetime.utcnow()

            # Calculate overall score
            all_progress = db.query(ModuleProgress).filter_by(
                enrollment_id=enrollment.id
            ).all()
            total_score = sum(p.exam_score for p in all_progress if p.exam_score)
            enrollment.overall_score = total_score / len(all_progress) if all_progress else 0

    db.commit()

    return {
        "score": score,
        "percentage": score,  # Same as score for clarity
        "total": total_questions,
        "correct": correct_count,
        "passed": passed,
        "passing_score": module.passing_score,
        "exam_attempt": exam_attempt,
        "next_module_unlocked": passed and module.module_number < module.course.total_modules,
        "module_completed": passed,
        "course_completed": enrollment.status == "completed",
        "detailed_review": detailed_review
    }


# ============================================================================
# ENDPOINT 9: Get Exam Result
# ============================================================================
@router.get("/module/{module_id}/exam-result")
async def get_exam_result(
    module_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Get detailed exam results for a completed module
    """
    # Get module
    module = db.query(CourseModule).filter_by(id=module_id).first()
    if not module:
        raise HTTPException(404, "Module not found")

    # Get enrollment
    enrollment = db.query(TeacherCareerEnrollment).filter_by(
        teacher_id=user.id,
        course_id=module.course_id
    ).first()

    if not enrollment:
        raise HTTPException(400, "You are not enrolled in this course")

    # Get module progress
    module_progress = db.query(ModuleProgress).filter_by(
        enrollment_id=enrollment.id,
        module_id=module_id
    ).first()

    if not module_progress or not module_progress.exam_score:
        raise HTTPException(400, "No exam results found. Take the exam first.")

    # Get latest exam responses
    latest_attempt = module_progress.exam_attempts

    responses = db.query(ModuleExamResponse).filter_by(
        module_progress_id=module_progress.id,
        exam_attempt=latest_attempt
    ).all()

    detailed_review = []
    for response in responses:
        question = response.question
        detailed_review.append({
            "question": question.question,
            "options": json.loads(question.options_json),
            "selected_answer": response.selected_answer,
            "correct_answer": question.correct_answer,
            "is_correct": response.is_correct
        })

    return {
        "module_name": module.module_name,
        "score": module_progress.exam_score,
        "passed": module_progress.passed,
        "passing_score": module.passing_score,
        "exam_attempts": module_progress.exam_attempts,
        "completed_at": module_progress.completed_at.isoformat() if module_progress.completed_at else None,
        "detailed_review": detailed_review
    }


# ============================================================================
# ENDPOINT 10: Get Course Certificate
# ============================================================================
@router.get("/enrollment/{enrollment_id}/certificate")
async def get_course_certificate(
    enrollment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Get or generate course completion certificate
    """
    # Get enrollment
    enrollment = db.query(TeacherCareerEnrollment).filter_by(
        id=enrollment_id,
        teacher_id=user.id
    ).first()

    if not enrollment:
        raise HTTPException(404, "Enrollment not found")

    if enrollment.status != "completed":
        raise HTTPException(400, "Course not yet completed")

    # Check if certificate already exists
    certificate = db.query(CourseCertificate).filter_by(enrollment_id=enrollment_id).first()

    if not certificate:
        # Generate new certificate
        import secrets
        certificate_number = f"LT-{enrollment.course.course_type.upper()}-{datetime.now().year}-{secrets.token_hex(3).upper()}"
        verification_code = secrets.token_urlsafe(16)

        certificate = CourseCertificate(
            enrollment_id=enrollment_id,
            certificate_number=certificate_number,
            verification_code=verification_code,
            pdf_path=None  # TODO: Generate PDF
        )
        db.add(certificate)
        db.commit()
        db.refresh(certificate)

    return {
        "certificate_number": certificate.certificate_number,
        "course_name": enrollment.course.course_name,
        "teacher_name": user.name,
        "issued_date": certificate.issued_date.isoformat(),
        "completion_date": enrollment.completion_date.isoformat(),
        "overall_score": enrollment.overall_score,
        "verification_code": certificate.verification_code,
        "pdf_url": certificate.pdf_path if certificate.pdf_path else None
    }


# ============================================================================
# ENDPOINT 11: Update Teacher Education
# ============================================================================
@router.patch("/update-education")
async def update_teacher_education(
    enrollment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Update teacher's education field after course completion
    """
    # Get enrollment
    enrollment = db.query(TeacherCareerEnrollment).filter_by(
        id=enrollment_id,
        teacher_id=user.id
    ).first()

    if not enrollment:
        raise HTTPException(404, "Enrollment not found")

    if enrollment.status != "completed":
        raise HTTPException(400, "Course not yet completed")

    # Get teacher profile
    profile = db.query(TeacherProfile).filter_by(user_id=user.id).first()
    if not profile:
        raise HTTPException(400, "Teacher profile not found")

    old_education = profile.education
    new_education = f"{enrollment.course.course_type} {enrollment.course.subject}"

    # Update education
    profile.education = new_education
    db.commit()

    return {
        "success": True,
        "old_education": old_education,
        "new_education": new_education,
        "message": "Education qualification updated successfully"
    }
