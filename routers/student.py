"""
Student API Router
Handles student-specific endpoints for viewing and taking assessments
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any
from datetime import datetime
from database import get_db
from models import User
from models_k12 import K12Assessment, K12Question, K12Result
from security import get_current_user, require_role

router = APIRouter(prefix="/student", tags=["student"])


@router.get("/assessments")
def get_student_assessments(
    status_filter: str = "all",  # all, upcoming, active, completed
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    """
    Get assessments assigned to student's class and section
    """
    if not user.class_name or not user.section:
        raise HTTPException(
            status_code=400,
            detail="Student class and section not set. Please sync your profile."
        )

    # Base query
    query = db.query(K12Assessment).filter(
        K12Assessment.class_name == user.class_name,
        K12Assessment.section == user.section
    )

    now = datetime.now()

    # Apply filter
    if status_filter == "upcoming":
        query = query.filter(K12Assessment.start_time > now)
    elif status_filter == "active":
        query = query.filter(
            K12Assessment.start_time <= now,
            K12Assessment.end_time >= now
        )
    elif status_filter == "completed":
        query = query.filter(K12Assessment.end_time < now)

    assessments = query.order_by(K12Assessment.start_time.desc()).all()

    result = []
    for assessment in assessments:
        student_result = db.query(K12Result).filter(
            K12Result.assessment_id == assessment.id,
            K12Result.student_id == user.id
        ).first()

        question_count = db.query(K12Question).filter(
            K12Question.assessment_id == assessment.id
        ).count()

        if student_result:
            status_str = "submitted"
        elif now < assessment.start_time:
            status_str = "upcoming"
        elif now > assessment.end_time:
            status_str = "expired"
        else:
            status_str = "active"

        result.append({
            "id": assessment.id,
            "subject": assessment.subject,
            "chapter": assessment.chapter,
            "class_name": assessment.class_name,
            "section": assessment.section,
            "start_time": assessment.start_time.isoformat() if assessment.start_time else None,
            "end_time": assessment.end_time.isoformat() if assessment.end_time else None,
            "duration_minutes": assessment.duration_minutes,
            "question_count": question_count,
            "status": status_str,
            "submitted": student_result is not None,
            "score": student_result.score if student_result else None,
            "submitted_at": student_result.submitted_at.isoformat() if student_result and student_result.submitted_at else None
        })

    return result


@router.get("/assessments/{assessment_id}")
def get_assessment_details(
    assessment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    """Get assessment details with questions"""
    assessment = db.query(K12Assessment).filter(K12Assessment.id == assessment_id).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    if assessment.class_name != user.class_name or assessment.section != user.section:
        raise HTTPException(status_code=403, detail="Not eligible")

    result = db.query(K12Result).filter(
        K12Result.assessment_id == assessment_id,
        K12Result.student_id == user.id
    ).first()

    if result:
        raise HTTPException(status_code=400, detail="Already submitted")

    now = datetime.now()
    if now < assessment.start_time:
        raise HTTPException(status_code=400, detail="Not started yet")

    if now > assessment.end_time:
        raise HTTPException(status_code=400, detail="Assessment ended")

    questions = db.query(K12Question).filter(
        K12Question.assessment_id == assessment_id
    ).order_by(K12Question.id).all()

    return {
        "id": assessment.id,
        "subject": assessment.subject,
        "chapter": assessment.chapter,
        "start_time": assessment.start_time.isoformat(),
        "end_time": assessment.end_time.isoformat(),
        "duration_minutes": assessment.duration_minutes,
        "questions": [
            {
                "id": q.id,
                "question_text": q.question,
                "question_type": q.question_type,
                "options": q.options,
                "marks": q.marks
            }
            for q in questions
        ]
    }


@router.post("/assessments/{assessment_id}/submit")
def submit_assessment(
    assessment_id: int,
    submission: Dict[str, Any],
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    """Submit assessment answers"""
    assessment = db.query(K12Assessment).filter(K12Assessment.id == assessment_id).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    if assessment.class_name != user.class_name or assessment.section != user.section:
        raise HTTPException(status_code=403, detail="Not eligible")

    existing = db.query(K12Result).filter(
        K12Result.assessment_id == assessment_id,
        K12Result.student_id == user.id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already submitted")

    now = datetime.now()
    if now > assessment.end_time:
        raise HTTPException(status_code=400, detail="Assessment ended")

    answers = submission.get("answers", {})
    questions = db.query(K12Question).filter(
        K12Question.assessment_id == assessment_id
    ).all()

    total_marks = sum(q.marks for q in questions)
    scored_marks = 0

    for question in questions:
        student_answer = answers.get(str(question.id), "").strip()
        correct_answer = question.correct_answer.strip()

        if question.question_type in ["multiple_choice", "true_false", "fill_blank"]:
            if student_answer.lower() == correct_answer.lower():
                scored_marks += question.marks
        elif question.question_type == "multi_select":
            student_set = set(student_answer.split(",")) if student_answer else set()
            correct_set = set(correct_answer.split(","))
            if student_set == correct_set:
                scored_marks += question.marks

    score = (scored_marks / total_marks * 100) if total_marks > 0 else 0

    result = K12Result(
        assessment_id=assessment_id,
        student_id=user.id,
        answers=answers,
        score=score,
        submitted_at=datetime.now()
    )

    db.add(result)
    db.commit()

    return {
        "success": True,
        "score": round(score, 2),
        "scored_marks": scored_marks,
        "total_marks": total_marks,
        "message": f"Assessment submitted! Score: {scored_marks}/{total_marks} ({score:.1f}%)"
    }


@router.get("/results")
def get_student_results(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    """Get all student results"""
    results = db.query(K12Result).filter(
        K12Result.student_id == user.id
    ).order_by(K12Result.submitted_at.desc()).all()

    result_list = []
    for result in results:
        assessment = db.query(K12Assessment).filter(
            K12Assessment.id == result.assessment_id
        ).first()

        if assessment:
            result_list.append({
                "result_id": result.id,
                "assessment_id": assessment.id,
                "subject": assessment.subject,
                "chapter": assessment.chapter,
                "score": round(result.score, 2),
                "submitted_at": result.submitted_at.isoformat(),
                "class_name": assessment.class_name,
                "section": assessment.section
            })

    return result_list
