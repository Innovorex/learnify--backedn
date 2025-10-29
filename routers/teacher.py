# routers/teacher.py
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
from models import TeacherProfile, User
from models_k12 import K12Assessment, K12Question, K12Result
from schemas import TeacherProfileIn, TeacherProfileOut
from security import get_current_user, require_role

# AI Services for K-12 Assessment
from services.ai_question_generator import generate_questions
from services.syllabus_service import get_syllabus_service

router = APIRouter(prefix="/teacher", tags=["teacher"])

@router.post("/profile", response_model=TeacherProfileOut, status_code=201)
def create_profile(payload: TeacherProfileIn,
                   db: Session = Depends(get_db),
                   user: User = Depends(require_role("teacher"))):
    # Check if profile already exists
    exists = db.query(TeacherProfile).filter(TeacherProfile.user_id == user.id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Profile already exists")

    profile = TeacherProfile(
        user_id=user.id,
        education=payload.education,
        grades_teaching=payload.grades_teaching,
        subjects_teaching=payload.subjects_teaching,
        experience_years=payload.experience_years,
        board=payload.board,
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/profile/me", response_model=TeacherProfileOut)
def get_my_profile(db: Session = Depends(get_db),
                   user: User = Depends(require_role("teacher"))):
    profile = db.query(TeacherProfile).filter(TeacherProfile.user_id == user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


# ============================================================================
# K-12 ASSESSMENT ENDPOINTS (Student Assessment System)
# ============================================================================

@router.post("/k12/create-assessment")
def create_k12_assessment(
    teacher_id: int,
    class_name: str,
    section: str,
    subject: str,
    chapter: str,
    start_time: datetime,
    end_time: datetime,
    duration_minutes: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a K-12 assessment for students"""

    # Verify teacher exists
    teacher = db.query(User).filter(User.id == teacher_id, User.role == "teacher").first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    # Convert timezone-aware datetime to naive datetime
    start_time_naive = start_time.replace(tzinfo=None) if start_time.tzinfo else start_time
    end_time_naive = end_time.replace(tzinfo=None) if end_time.tzinfo else end_time

    # Create assessment
    new_assessment = K12Assessment(
        teacher_id=teacher_id,
        class_name=class_name,
        section=section,
        subject=subject,
        chapter=chapter,
        start_time=start_time_naive,
        end_time=end_time_naive,
        duration_minutes=duration_minutes
    )

    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)

    # Generate questions in background (if AI service is available)
    background_tasks.add_task(
        generate_and_store_k12_questions,
        new_assessment.id,
        class_name,
        subject,
        chapter,
        db
    )

    return {
        "id": new_assessment.id,
        "message": "Assessment created successfully",
        "assessment": new_assessment
    }


@router.get("/k12/my-assessments/{teacher_id}")
def get_teacher_k12_assessments(teacher_id: int, db: Session = Depends(get_db)):
    """Get all K-12 assessments created by a teacher"""

    # Sort by start_time descending (latest first)
    assessments = db.query(K12Assessment).filter(
        K12Assessment.teacher_id == teacher_id
    ).order_by(K12Assessment.start_time.desc()).all()

    return assessments


@router.get("/k12/assessment/{assessment_id}/questions")
def get_k12_assessment_questions(assessment_id: int, db: Session = Depends(get_db)):
    """Get all questions for a K-12 assessment (teacher view with correct answers)"""

    assessment = db.query(K12Assessment).filter(K12Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    questions = db.query(K12Question).filter(K12Question.assessment_id == assessment_id).all()

    return [
        {
            "id": q.id,
            "question": q.question,
            "options": q.options,
            "correct_answer": q.correct_answer,
            "difficulty": q.difficulty
        } for q in questions
    ]


@router.get("/k12/results/{assessment_id}")
def get_k12_assessment_results(assessment_id: int, db: Session = Depends(get_db)):
    """Get results for a specific K-12 assessment"""

    results = db.query(K12Result).filter(K12Result.assessment_id == assessment_id).all()
    if not results:
        return {
            "assessment_id": assessment_id,
            "total_students": 0,
            "average_score": 0,
            "top_scorer": None,
            "results": []
        }

    total_students = len(results)
    avg_score = sum(r.score for r in results) / total_students
    top_result = max(results, key=lambda r: r.score)
    top_student = db.query(User).filter(User.id == top_result.student_id).first()

    return {
        "assessment_id": assessment_id,
        "average_score": round(avg_score, 2),
        "total_students": total_students,
        "top_scorer": top_student.name if top_student else None,
        "results": [
            {
                "student_id": r.student_id,
                "student_name": db.query(User).filter(User.id == r.student_id).first().name,
                "score": r.score,
                "submitted_at": r.submitted_at
            } for r in results
        ]
    }


@router.get("/k12/summary/{teacher_id}")
def get_teacher_k12_summary(teacher_id: int, db: Session = Depends(get_db)):
    """Get summary of all K-12 assessments for a teacher"""

    assessments = db.query(K12Assessment).filter(K12Assessment.teacher_id == teacher_id).all()
    summary = []

    for a in assessments:
        results = db.query(K12Result).filter(K12Result.assessment_id == a.id).all()
        if not results:
            continue
        avg = sum(r.score for r in results) / len(results)
        top = max(r.score for r in results)
        summary.append({
            "assessment_id": a.id,
            "subject": a.subject,
            "chapter": a.chapter,
            "class_name": a.class_name,
            "section": a.section,
            "average_score": round(avg, 2),
            "top_score": top,
            "total_submissions": len(results)
        })

    return summary


# Helper function for background question generation
def generate_and_store_k12_questions(assessment_id: int, class_name: str, subject: str, chapter: str, db: Session):
    """
    Generate K-12 questions using AI with REAL CBSE syllabus content
    Fetches syllabus from database and generates contextual MCQs
    """
    try:
        print(f"🔄 Generating questions for: Class {class_name} - {subject} - {chapter}")

        # Get syllabus content from database
        syllabus_service = get_syllabus_service(db)
        syllabus_content = syllabus_service.get_syllabus_content(
            class_name=class_name,
            subject=subject,
            chapter=chapter
        )

        # Generate 10 questions using AI with syllabus content
        ai_questions = generate_questions(
            board="CBSE",
            class_name=class_name,
            subject=subject,
            chapter=chapter,
            num_questions=10,
            syllabus_content=syllabus_content  # Real CBSE content!
        )

        # Store questions in database
        for q_data in ai_questions:
            question = K12Question(
                assessment_id=assessment_id,
                question=q_data["question"],
                options=q_data["options"],
                correct_answer=q_data["correct_answer"],
                difficulty=q_data.get("difficulty", "medium")
            )
            db.add(question)

        db.commit()

        if syllabus_content:
            print(f"✅ Generated {len(ai_questions)} AI questions with REAL syllabus content for assessment {assessment_id}")
        else:
            print(f"⚠️ Generated {len(ai_questions)} sample questions (no syllabus content found) for assessment {assessment_id}")

    except Exception as e:
        print(f"❌ Error generating questions: {e}")
        db.rollback()
