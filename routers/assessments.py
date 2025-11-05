import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, Module, TeacherProfile, AssessmentQuestion, AssessmentResponse, Performance
from schemas import (
    GenerateAssessmentOut,
    MCQQuestion,
    SubmitAnswersIn,
    EnhancedSubmitAnswersIn,
    ScoreOut,
    AnswerReview,
    EnhancedAssessmentResult,
    QuestionFeedback
)
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
    """
    Legacy submission endpoint (no timer enforcement)
    For backward compatibility with old frontend code
    """
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


@router.post("/submit-enhanced/{module_id}", response_model=EnhancedAssessmentResult)
async def submit_answers_enhanced(
    module_id: int,
    payload: EnhancedSubmitAnswersIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher")),
):
    """
    Enhanced submission endpoint with timer enforcement and attempt tracking
    Phase 2: Implements auto-fail on timeout, session validation, attempt recording
    Phase 3: AI-generated feedback and weak topics analysis
    """
    from datetime import datetime, timezone
    from models_knowledge_tracking import (
        AssessmentSession,
        TeacherAssessmentAttempt,
        TeacherAttemptLimit,
        TeacherAssessmentSummary
    )

    # 1. Validate module exists
    module = db.query(Module).filter_by(id=module_id).first()
    if not module:
        raise HTTPException(404, "Module not found")
    if module.assessment_type != "mcq":
        raise HTTPException(400, "This module is not MCQ-based")

    # 2. Validate session exists and is active
    session = db.query(AssessmentSession).filter_by(
        id=payload.session_id,
        teacher_id=user.id,
        module_id=module_id,
        is_active=True
    ).first()

    if not session:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired session. Please start a new assessment."
        )

    # 3. Check if session has expired (TIMER ENFORCEMENT)
    now = datetime.now(timezone.utc)
    # Make expires_at timezone-aware if it isn't already
    expires_at_aware = session.expires_at.replace(tzinfo=timezone.utc) if session.expires_at.tzinfo is None else session.expires_at
    started_at_aware = session.started_at.replace(tzinfo=timezone.utc) if session.started_at.tzinfo is None else session.started_at
    session_expired = now > expires_at_aware

    # Calculate time taken
    time_taken_seconds = int((now - started_at_aware).total_seconds())

    # 4. Get questions from session
    questions_data = session.questions_json
    if not questions_data or not isinstance(questions_data, list):
        raise HTTPException(500, "Session questions data is invalid")

    # Build question map from session
    qmap = {}
    for q_data in questions_data:
        qmap[q_data['id']] = q_data

    # 5. Grade the assessment
    correct = 0
    total = len(payload.answers)
    feedback_list = []

    # If session expired, auto-fail (score = 0)
    if session_expired:
        print(f"[TIMER] Session {session.id} expired. Auto-failing attempt.")
        score_percentage = 0.0

        # Generate feedback showing all as incorrect due to timeout
        for ans in payload.answers:
            q_data = qmap.get(ans.question_id)
            if q_data:
                feedback_list.append(
                    QuestionFeedback(
                        question_id=q_data['id'],
                        question_text=q_data['question'],
                        your_answer=str(ans.selected_answer).upper(),
                        correct_answer=q_data['correct_answer'],
                        is_correct=False,
                        explanation="Time expired - submission not counted",
                        topic=None
                    )
                )
    else:
        # Normal grading
        user_answers_for_ai = []

        for ans in payload.answers:
            q_data = qmap.get(ans.question_id)
            if not q_data:
                raise HTTPException(400, f"Question ID {ans.question_id} not in session")

            is_correct = (
                str(ans.selected_answer).strip().upper()
                == str(q_data['correct_answer']).strip().upper()
            )

            if is_correct:
                correct += 1

            # Build feedback object (explanation to be filled by AI)
            feedback_list.append(
                QuestionFeedback(
                    question_id=q_data['id'],
                    question_text=q_data['question'],
                    your_answer=str(ans.selected_answer).upper(),
                    correct_answer=q_data['correct_answer'],
                    is_correct=is_correct,
                    explanation="",  # Will be filled by AI
                    topic=None  # Will be filled by AI
                )
            )

            # Collect data for AI feedback
            user_answers_for_ai.append({
                "question_id": q_data['id'],
                "selected_answer": str(ans.selected_answer).upper(),
                "is_correct": is_correct
            })

        score_percentage = round((correct / total) * 100.0, 2) if total else 0.0

        # PHASE 3: Generate AI feedback for all answers
        print("[PHASE 3] Generating AI feedback...")
        from services.ai_feedback_generator import (
            generate_feedback_for_answers,
            extract_subject_from_module
        )

        try:
            # Get teacher profile for context
            profile = db.query(TeacherProfile).filter_by(user_id=user.id).first()
            subject = extract_subject_from_module(module.name)

            # Generate AI feedback in parallel
            ai_feedback = await generate_feedback_for_answers(
                questions=questions_data,
                user_answers=user_answers_for_ai,
                subject=subject
            )

            # Merge AI feedback into feedback_list
            for i, ai_fb in enumerate(ai_feedback):
                if i < len(feedback_list):
                    feedback_list[i].explanation = ai_fb['explanation']
                    feedback_list[i].topic = ai_fb['topic']

            print(f"[PHASE 3] ✓ AI feedback generated for {len(ai_feedback)} questions")

        except Exception as e:
            print(f"[PHASE 3] ✗ AI feedback generation failed: {e}")
            # Continue without AI feedback - not critical

    # 6. Record attempt in teacher_assessment_attempts
    attempt = TeacherAssessmentAttempt(
        teacher_id=user.id,
        module_id=module_id,
        attempt_number=session.attempt_number,
        score_percentage=score_percentage,
        time_taken_seconds=time_taken_seconds,
        started_at=started_at_aware,
        completed_at=now,
        questions_json=questions_data,
        answers_json=[{"question_id": a.question_id, "selected_answer": a.selected_answer} for a in payload.answers]
    )
    db.add(attempt)

    # 7. Update attempt limits
    year_month = now.strftime("%Y-%m")
    limit_record = db.query(TeacherAttemptLimit).filter_by(
        teacher_id=user.id,
        module_id=module_id,
        year_month=year_month
    ).first()

    if limit_record:
        limit_record.attempts_used += 1
        limit_record.last_attempt_at = now
        # Calculate next attempt available (last_attempt + cooldown_hours)
        from datetime import timedelta
        cooldown_hours = module.cooldown_hours or 24
        limit_record.next_attempt_available = now + timedelta(hours=cooldown_hours)

    # 8. Update summary statistics
    summary = db.query(TeacherAssessmentSummary).filter_by(
        teacher_id=user.id,
        module_id=module_id
    ).first()

    improvement = None
    if summary:
        previous_score = summary.latest_score
        summary.total_attempts += 1
        summary.latest_score = score_percentage
        if score_percentage > summary.best_score:
            summary.best_score = score_percentage

        # Recalculate average (including current attempt)
        # Current attempt + existing attempts
        total_score = (summary.average_score * (summary.total_attempts - 1)) + score_percentage
        summary.average_score = total_score / summary.total_attempts if summary.total_attempts > 0 else score_percentage

        # Calculate improvement rate
        if summary.first_attempt_score and summary.first_attempt_score > 0:
            summary.improvement_rate = (
                (summary.latest_score - summary.first_attempt_score) / summary.first_attempt_score * 100
            )

        # Calculate improvement vs previous attempt
        if previous_score is not None:
            improvement = score_percentage - previous_score
    else:
        # First attempt - create summary
        summary = TeacherAssessmentSummary(
            teacher_id=user.id,
            module_id=module_id,
            total_attempts=1,
            best_score=score_percentage,
            latest_score=score_percentage,
            first_attempt_score=score_percentage,
            average_score=score_percentage,
            improvement_rate=0.0
        )
        db.add(summary)

    # 9. Deactivate session
    session.is_active = False
    session.submitted_at = now

    # 10. Update legacy Performance table for backward compatibility
    perf = db.query(Performance).filter_by(teacher_id=user.id, module_id=module_id).first()
    rating = "Excellent" if score_percentage >= 85 else "Good" if score_percentage >= 60 else "Needs Improvement"

    if not perf:
        perf = Performance(
            teacher_id=user.id,
            module_id=module_id,
            score=score_percentage,
            rating=rating,
            details=f"Attempt #{session.attempt_number}: {correct}/{total} ({time_taken_seconds}s)",
        )
        db.add(perf)
    else:
        perf.score = score_percentage
        perf.rating = rating
        perf.details = f"Attempt #{session.attempt_number}: {correct}/{total} ({time_taken_seconds}s)"

    db.commit()

    # 11. Log performance history for timeline tracking
    from services.tracking import log_performance_history
    log_performance_history(db, user.id, module_id, score_percentage, rating)

    # 12. Identify weak topics (Phase 3)
    def identify_weak_topics(feedback: list) -> list:
        """Identify topics where teacher struggled (2+ incorrect answers)"""
        from collections import Counter

        incorrect_topics = [
            fb.topic for fb in feedback
            if not fb.is_correct and fb.topic
        ]

        # Count topics and return those with 2+ incorrect answers
        topic_counts = Counter(incorrect_topics)
        weak = [topic for topic, count in topic_counts.items() if count >= 2]

        return weak[:5]  # Top 5 weak topics

    weak_topics = identify_weak_topics(feedback_list)

    # Update summary with weak topics
    if summary and weak_topics:
        summary.weak_topics = weak_topics

    # 13. Return enhanced result
    return EnhancedAssessmentResult(
        score_percentage=score_percentage,
        correct_count=correct,
        total_questions=total,
        time_taken_seconds=time_taken_seconds,
        attempt_number=session.attempt_number,
        improvement=improvement,
        feedback=feedback_list,
        weak_topics=weak_topics,
        next_attempt_available=limit_record.next_attempt_available if limit_record else None,
        attempts_used_this_month=limit_record.attempts_used if limit_record else 0,
        max_attempts_per_month=module.max_attempts_per_month or 3
    )


@router.post("/generate-with-session/{module_id}/{session_id}", response_model=GenerateAssessmentOut)
async def generate_assessment_with_session(
    module_id: int,
    session_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher")),
):
    """
    Generate questions AND link them to the active session
    This combines question generation with session tracking for Phase 2
    """
    from models_knowledge_tracking import AssessmentSession

    # Validate session
    session = db.query(AssessmentSession).filter_by(
        id=session_id,
        teacher_id=user.id,
        module_id=module_id,
        is_active=True
    ).first()

    if not session:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired session"
        )

    # Call existing generate logic
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

    # Generate questions
    if module_id == 1 or module.name == "Subject Knowledge & Content Expertise":
        print(f"[ENHANCED MODULE 1] Using Bloom's taxonomy generator")
        from services.enhanced_module1_generator import generate_enhanced_module1_questions

        questions = await generate_enhanced_module1_questions(
            teacher_profile=profile_data,
            board=board,
            state=state,
            n_questions=8
        )
    else:
        print(f"[AI AGENT] Generating 8 mixed difficulty questions")
        questions = await generate_mcqs(
            profile_data,
            module.name,
            board,
            n_questions=8,
            state=state,
            difficulty="mixed",
            db_session=db,
        )

    if questions is None:
        questions = []

    if not questions:
        raise HTTPException(500, "Failed to generate questions from AI agent.")

    # Save questions to database
    saved = []
    questions_for_session = []

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

            # Build session-friendly format
            questions_for_session.append({
                "id": s.id,
                "question": s.question,
                "options": json.loads(s.options_json),
                "correct_answer": s.correct_answer  # Store in session for grading
            })

    except Exception as e:
        print(f"[ERROR] Failed to save questions: {type(e).__name__}: {e}")
        raise HTTPException(500, f"Failed to save questions: {str(e)}")

    # Update session with questions
    session.questions_json = questions_for_session
    db.commit()

    # Return questions to frontend (without correct answers)
    out_questions = []
    for q in questions_for_session:
        out_questions.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"],
            "correct_answer": None  # Hide from frontend
        })

    return GenerateAssessmentOut(
        module_id=module_id,
        module_name=module.name,
        questions=out_questions
    )
