import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, Module, TeacherProfile, AssessmentQuestion, AssessmentResponse, Performance
from schemas import GenerateAssessmentOut, MCQQuestion, SubmitAnswersIn, ScoreOut, AnswerReview
from security import require_role
from services.openrouter import generate_mcqs

router = APIRouter(prefix="/assessment", tags=["assessment"])


@router.post("/generate/{module_id}", response_model=GenerateAssessmentOut)
async def generate_assessment(
    module_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher")),
):
    module = db.query(Module).filter_by(id=module_id).first()
    if not module:
        raise HTTPException(404, "Module not found")
    if module.assessment_type != "mcq":
        raise HTTPException(400, "This module is not MCQ-based")

    profile = db.query(TeacherProfile).filter_by(user_id=user.id).first()
    if not profile:
        raise HTTPException(400, "Complete teacher profile first")

    profile_data = {
        "education": profile.education,
        "grades_teaching": profile.grades_teaching,
        "subjects_teaching": profile.subjects_teaching,
        "experience_years": profile.experience_years,
    }

    board = getattr(profile, "board", "General")
    state = getattr(profile, "state", "Telangana")

    # MODULE 1: Enhanced Question Generation with Bloom's Taxonomy
    if module_id == 1 or module.name == "Subject Knowledge & Content Expertise":
        print(f"[ENHANCED MODULE 1] Using Bloom's taxonomy generator for syllabus-aligned HARD questions")
        print(f"[TEACHER] Grades: {profile.grades_teaching}, Subjects: {profile.subjects_teaching}, Board: {board}")

        from services.enhanced_module1_generator import generate_enhanced_module1_questions

        questions = await generate_enhanced_module1_questions(
            teacher_profile=profile_data,
            board=board,
            state=state,
            n_questions=8
        )

    else:
        # Other modules: Use existing generator
        print(f"[AI AGENT] Generating 8 mixed difficulty questions in 1 API call: State={state}, Board={board}")

        questions = await generate_mcqs(
            profile_data,
            module.name,
            board,
            n_questions=8,
            state=state,
            difficulty="mixed",  # Generate mix of medium and hard questions
            db_session=db,
        )

    # ✅ Safe fallback handling for NoneType
    if questions is None:
        print("[ERROR] Question generation returned None!")
        questions = []
    print(f"[DEBUG] Generated total questions: {len(questions)}")

    if not questions:
        raise HTTPException(500, "Failed to generate questions from AI agent.")

    # Save questions to database
    saved = []
    try:
        for q in questions:
            options = q.get("options") or []
            norm_opts = []
            for opt in options:
                norm_opts.append(opt.split(")", 1)[-1].strip() if ")" in opt[:3] else opt)

            aq = AssessmentQuestion(
                teacher_id=user.id,
                module_id=module_id,
                question=q.get("question", ""),
                options_json=json.dumps(norm_opts, ensure_ascii=False),
                correct_answer=q.get("correct_answer"),
            )
            db.add(aq)
            saved.append(aq)
        db.commit()
        for s in saved:
            db.refresh(s)
        print(f"[DEBUG] Successfully saved {len(saved)} questions to database")

    except Exception as e:
        print(f"[ERROR] Failed to save questions: {type(e).__name__}: {e}")
        raise HTTPException(500, f"Failed to save questions: {str(e)}")

    # Prepare response (don’t send correct answers to frontend)
    out_questions = []
    for s in saved:
        out_questions.append({
            "id": s.id,
            "question": s.question,
            "options": json.loads(s.options_json),
            "correct_answer": None
        })

    return GenerateAssessmentOut(
        module_id=module_id,
        module_name=module.name,
        questions=out_questions
    )


@router.post("/submit/{module_id}", response_model=ScoreOut)
def submit_answers(
    module_id: int,
    payload: SubmitAnswersIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher")),
):
    module = db.query(Module).filter_by(id=module_id).first()
    if not module:
        raise HTTPException(404, "Module not found")
    if module.assessment_type != "mcq":
        raise HTTPException(400, "This module is not MCQ-based")

    qids = [a.question_id for a in payload.answers]
    qmap = {
        q.id: q
        for q in db.query(AssessmentQuestion)
        .filter(
            AssessmentQuestion.id.in_(qids),
            AssessmentQuestion.teacher_id == user.id,
            AssessmentQuestion.module_id == module_id,
        )
        .all()
    }

    if len(qmap) != len(qids):
        raise HTTPException(400, "Invalid question ids")

    correct = 0
    total = len(payload.answers)
    review_data = []

    for ans in payload.answers:
        q = qmap.get(ans.question_id)
        is_correct = (str(ans.selected_answer).strip().upper()
                      == (q.correct_answer or "").strip().upper())
        if is_correct:
            correct += 1

        review_data.append(
            AnswerReview(
                question=q.question,
                options=json.loads(q.options_json),
                user_answer=str(ans.selected_answer).upper(),
                correct_answer=q.correct_answer or "",
                is_correct=is_correct,
            )
        )

        ar = AssessmentResponse(
            teacher_id=user.id,
            module_id=module_id,
            question_id=q.id,
            selected_answer=str(ans.selected_answer).upper(),
            is_correct=is_correct,
        )
        db.add(ar)

    db.commit()

    score_percent = round((correct / total) * 100.0, 2) if total else 0.0
    rating = "Excellent" if score_percent >= 85 else "Good" if score_percent >= 60 else "Needs Improvement"

    # Upsert performance
    perf = db.query(Performance).filter_by(teacher_id=user.id, module_id=module_id).first()
    if not perf:
        perf = Performance(
            teacher_id=user.id,
            module_id=module_id,
            score=score_percent,
            rating=rating,
            details=f"MCQ auto-score: {correct}/{total}",
        )
        db.add(perf)
    else:
        perf.score = score_percent
        perf.rating = rating
        perf.details = f"MCQ auto-score: {correct}/{total}"

    db.commit()

    # Log performance history for timeline tracking
    from services.tracking import log_performance_history
    log_performance_history(db, user.id, module_id, score_percent, rating)

    return ScoreOut(
        total_questions=total,
        correct=correct,
        score_percent=score_percent,
        review=review_data,
    )
