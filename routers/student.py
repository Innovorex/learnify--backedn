# routers/student.py - K-12 Student Assessment APIs
"""
Student endpoints for K-12 assessment system:
- View available assessments for their class/section
- Take exams within the time window
- Submit answers and get scores
- View past results
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from database import get_db
from models_k12 import K12Assessment, K12Question, K12Result

# IST timezone (UTC + 5:30)
IST = timezone(timedelta(hours=5, minutes=30))

router = APIRouter(prefix="/student", tags=["student"])

def get_ist_now():
    """Get current time in IST as naive datetime"""
    return datetime.now(IST).replace(tzinfo=None)


@router.get("/assessments/{class_name}/{section}")
def get_assessments(class_name: str, section: str, db: Session = Depends(get_db)):
    """Get all upcoming assessments for a student's class and section"""
    now = get_ist_now()

    print(f"🔍 Fetching assessments for Class: '{class_name}', Section: '{section}'")

    # Get all active assessments that haven't ended yet
    data = db.query(K12Assessment).filter(
        K12Assessment.class_name == class_name,
        K12Assessment.section == section,
        K12Assessment.end_time > now
    ).all()

    print(f"✅ Found {len(data)} active assessments for '{class_name}'-'{section}'")

    return data


@router.get("/assessment/{assessment_id}/questions")
def get_questions(assessment_id: int, db: Session = Depends(get_db)):
    """Get questions for a specific assessment (only if exam is currently active)"""
    assessment = db.query(K12Assessment).filter(K12Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    # Get current time in IST (naive datetime)
    now = get_ist_now()

    # Ensure assessment times are naive datetimes
    start_time = assessment.start_time.replace(tzinfo=None) if assessment.start_time.tzinfo else assessment.start_time
    end_time = assessment.end_time.replace(tzinfo=None) if assessment.end_time.tzinfo else assessment.end_time

    print(f"🕐 Current IST time: {now}")
    print(f"📝 Assessment ID {assessment_id}: {start_time} to {end_time} IST")

    # Check if exam is currently active
    if now < start_time or now > end_time:
        raise HTTPException(
            status_code=403,
            detail=f"Exam not active. Available from {start_time.strftime('%Y-%m-%d %H:%M')} to {end_time.strftime('%Y-%m-%d %H:%M')} IST"
        )

    # Fetch questions (don't send correct answers to frontend)
    questions = db.query(K12Question).filter(K12Question.assessment_id == assessment_id).all()

    question_list = []
    for q in questions:
        # Build response without correct answers
        question_response = {
            "id": q.id,
            "question": q.question,
            "question_type": q.question_type,
            "marks": q.marks
        }

        # Add question data based on type, removing correct answers
        if q.question_type == 'multiple_choice' or q.question_type == 'multi_select':
            # Send options but NOT correct_answer/correct_answers
            if q.question_data and 'options' in q.question_data:
                question_response['options'] = q.question_data['options']
            elif q.options:
                question_response['options'] = q.options
        elif q.question_type == 'true_false':
            # No data needed, just the question
            pass
        elif q.question_type == 'short_answer':
            # Send max_words if available
            if q.question_data and 'max_words' in q.question_data:
                question_response['max_words'] = q.question_data['max_words']
        elif q.question_type == 'fill_blank':
            # No hints, just the question with blanks
            pass
        elif q.question_type == 'ordering':
            # Send items to be ordered
            if q.question_data and 'items' in q.question_data:
                question_response['items'] = q.question_data['items']

        question_list.append(question_response)

    # Calculate remaining time based on exam duration (not window end time)
    # Students get the full duration_minutes when they start the exam
    time_remaining_seconds = assessment.duration_minutes * 60

    # Return questions with assessment metadata
    return {
        "assessment": {
            "id": assessment.id,
            "subject": assessment.subject,
            "chapter": assessment.chapter,
            "duration_minutes": assessment.duration_minutes,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "time_remaining_seconds": time_remaining_seconds
        },
        "questions": question_list
    }


@router.post("/submit-exam")
def submit_exam(req: dict, db: Session = Depends(get_db)):
    """Submit exam answers and calculate score"""
    student_id = req["student_id"]
    assessment_id = req["assessment_id"]
    answers = req["answers"]

    # Check if already submitted
    existing = db.query(K12Result).filter(
        K12Result.student_id == student_id,
        K12Result.assessment_id == assessment_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="You have already submitted this exam")

    # Fetch all questions for this assessment
    questions = db.query(K12Question).filter(K12Question.assessment_id == assessment_id).all()
    if not questions:
        raise HTTPException(status_code=404, detail="Questions not found")

    score = 0
    total = len(questions)

    # Evaluate answers
    for q in questions:
        selected = answers.get(str(q.id)) or answers.get(q.id)
        if selected and selected == q.correct_answer:
            score += 1

    # Save result
    result = K12Result(
        student_id=student_id,
        assessment_id=assessment_id,
        answers=answers,
        score=score
    )
    db.add(result)
    db.commit()

    return {"message": "Exam submitted successfully", "score": score, "total": total}


@router.get("/assessments-with-status/{student_id}/{class_name}/{section}")
def get_assessments_with_status(student_id: int, class_name: str, section: str, db: Session = Depends(get_db)):
    """Get all assessments with completion status for a student"""
    now = get_ist_now()

    print(f"🔍 Fetching assessments with status for Student ID: {student_id}, Class: '{class_name}', Section: '{section}'")

    # Get all assessments for this class/section, sorted by start_time descending
    assessments = db.query(K12Assessment).filter(
        K12Assessment.class_name == class_name,
        K12Assessment.section == section
    ).order_by(K12Assessment.start_time.desc()).all()

    print(f"📚 Found {len(assessments)} total assessments for '{class_name}'-'{section}'")

    output = []
    for a in assessments:
        # Check if student has submitted this assessment
        result = db.query(K12Result).filter(
            K12Result.student_id == student_id,
            K12Result.assessment_id == a.id
        ).first()

        # Make times timezone-aware for comparison if needed
        start_time = a.start_time.replace(tzinfo=None) if a.start_time.tzinfo else a.start_time
        end_time = a.end_time.replace(tzinfo=None) if a.end_time.tzinfo else a.end_time

        # Determine status
        if result:
            status = "completed"
            score = result.score
            total_questions = db.query(K12Question).filter(K12Question.assessment_id == a.id).count()
            submitted_at = result.submitted_at
        elif now < start_time:
            status = "scheduled"
            score = None
            total_questions = None
            submitted_at = None
        elif now >= start_time and now <= end_time:
            status = "available"
            score = None
            total_questions = None
            submitted_at = None
        else:  # now > end_time
            status = "missed"
            score = None
            total_questions = None
            submitted_at = None

        output.append({
            "id": a.id,
            "subject": a.subject,
            "chapter": a.chapter,
            "start_time": a.start_time,
            "end_time": a.end_time,
            "duration_minutes": a.duration_minutes,
            "status": status,
            "score": score,
            "total_questions": total_questions,
            "submitted_at": submitted_at
        })

    print(f"✅ Returning {len(output)} assessments with status")
    return output


@router.get("/my-results/{student_id}")
def get_student_results(student_id: int, db: Session = Depends(get_db)):
    """Get all past exam results for a student"""
    results = db.query(K12Result).filter(K12Result.student_id == student_id).all()
    output = []

    for r in results:
        a = db.query(K12Assessment).filter(K12Assessment.id == r.assessment_id).first()
        if not a:
            continue
        total_questions = db.query(K12Question).filter(K12Question.assessment_id == a.id).count()
        output.append({
            "assessment_id": a.id,
            "subject": a.subject,
            "chapter": a.chapter,
            "score": r.score,
            "total": total_questions,
            "submitted_at": r.submitted_at
        })
    return output
