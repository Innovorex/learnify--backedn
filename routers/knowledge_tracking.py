"""
API Router for Knowledge Assessment Attempt Tracking
Handles: attempt limits, cooldowns, session management, performance tracking
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta, timezone
from typing import List
from database import get_db
from security import get_current_user
from models import User, Module
from models_knowledge_tracking import (
    TeacherAssessmentAttempt,
    TeacherAttemptLimit,
    TeacherAssessmentSummary,
    AssessmentSession
)
from schemas import EnhancedModuleWithAttempts, EligibilityCheck, SessionStart

router = APIRouter(prefix="/assessment/tracking", tags=["knowledge-tracking"])


def get_or_create_attempt_limit(
    db: Session,
    teacher_id: int,
    module_id: int,
    module: Module
) -> TeacherAttemptLimit:
    """Get or create attempt limit record for current month"""
    current_month = datetime.now(timezone.utc).strftime("%Y-%m")

    limit_record = db.query(TeacherAttemptLimit).filter(
        TeacherAttemptLimit.teacher_id == teacher_id,
        TeacherAttemptLimit.module_id == module_id,
        TeacherAttemptLimit.year_month == current_month
    ).first()

    if not limit_record:
        limit_record = TeacherAttemptLimit(
            teacher_id=teacher_id,
            module_id=module_id,
            year_month=current_month,
            attempts_used=0,
            max_attempts=module.max_attempts_per_month or 3,
            cooldown_hours=module.cooldown_hours or 24
        )
        db.add(limit_record)
        db.commit()
        db.refresh(limit_record)

    return limit_record


def get_or_create_summary(
    db: Session,
    teacher_id: int,
    module_id: int
) -> TeacherAssessmentSummary:
    """Get or create summary record"""
    summary = db.query(TeacherAssessmentSummary).filter(
        TeacherAssessmentSummary.teacher_id == teacher_id,
        TeacherAssessmentSummary.module_id == module_id
    ).first()

    if not summary:
        summary = TeacherAssessmentSummary(
            teacher_id=teacher_id,
            module_id=module_id
        )
        db.add(summary)
        db.commit()
        db.refresh(summary)

    return summary


@router.get("/overview", response_model=List[EnhancedModuleWithAttempts])
async def get_assessment_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all knowledge assessment modules with attempt tracking data
    Returns modules with: attempts used, scores, cooldown status, eligibility
    """
    # Get all knowledge category modules
    modules = db.query(Module).filter(Module.category == "knowledge").all()

    result = []
    current_month = datetime.now(timezone.utc).strftime("%Y-%m")

    for module in modules:
        # Get attempt limit for this month
        limit = get_or_create_attempt_limit(db, current_user.id, module.id, module)

        # Get summary stats
        summary = get_or_create_summary(db, current_user.id, module.id)

        # Check if can attempt
        can_attempt = True
        next_available = None

        # Check monthly limit
        if limit.attempts_used >= limit.max_attempts:
            can_attempt = False

        # Check cooldown
        if limit.next_attempt_available:
            # Make next_attempt_available timezone-aware if needed
            next_attempt_aware = limit.next_attempt_available.replace(tzinfo=timezone.utc) if limit.next_attempt_available.tzinfo is None else limit.next_attempt_available
            if datetime.now(timezone.utc) < next_attempt_aware:
                can_attempt = False
                next_available = next_attempt_aware

        # Build response
        module_data = EnhancedModuleWithAttempts(
            id=module.id,
            name=module.name,
            description=module.description,
            assessment_type=module.assessment_type,
            category=module.category,
            time_limit_minutes=module.time_limit_minutes,
            cooldown_hours=module.cooldown_hours,
            max_attempts_per_month=module.max_attempts_per_month,
            attempts_used_this_month=limit.attempts_used,
            total_attempts=summary.total_attempts,
            best_score=summary.best_score if summary.best_score > 0 else None,
            latest_score=summary.latest_score if summary.latest_score > 0 else None,
            next_attempt_available=next_available,
            can_attempt=can_attempt,
            improvement_rate=summary.improvement_rate
        )

        result.append(module_data)

    return result


@router.post("/check-eligibility/{module_id}", response_model=EligibilityCheck)
async def check_attempt_eligibility(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check if teacher can attempt this assessment now
    Returns: eligibility status, reason if not eligible, time remaining
    """
    # Get module
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    # Get attempt limit
    limit = get_or_create_attempt_limit(db, current_user.id, module_id, module)

    # Check 1: Monthly limit
    if limit.attempts_used >= limit.max_attempts:
        # Calculate days until next month
        now = datetime.now(timezone.utc)
        next_month = (now.replace(day=1) + timedelta(days=32)).replace(day=1)
        days_until = (next_month - now).days

        return EligibilityCheck(
            eligible=False,
            reason="monthly_limit_reached",
            hours_remaining=None,
            days_until_reset=days_until,
            attempts_used_this_month=limit.attempts_used,
            max_attempts_per_month=limit.max_attempts
        )

    # Check 2: Cooldown period
    if limit.next_attempt_available:
        next_attempt_aware = limit.next_attempt_available.replace(tzinfo=timezone.utc) if limit.next_attempt_available.tzinfo is None else limit.next_attempt_available
        if datetime.now(timezone.utc) < next_attempt_aware:
            time_diff = next_attempt_aware - datetime.now(timezone.utc)
            hours_remaining = time_diff.total_seconds() / 3600

            return EligibilityCheck(
                eligible=False,
                reason="cooldown_period",
                hours_remaining=hours_remaining,
                days_until_reset=None,
                attempts_used_this_month=limit.attempts_used,
                max_attempts_per_month=limit.max_attempts
            )

    # All checks passed
    return EligibilityCheck(
        eligible=True,
        reason=None,
        hours_remaining=None,
        days_until_reset=None,
        attempts_used_this_month=limit.attempts_used,
        max_attempts_per_month=limit.max_attempts
    )


@router.post("/start/{module_id}", response_model=SessionStart)
async def start_assessment_session(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Start a new assessment session
    - Checks eligibility
    - Creates session with timer
    - Returns session info with expiration time
    """
    # Get module
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    # Check eligibility
    eligibility = await check_attempt_eligibility(module_id, current_user, db)
    if not eligibility.eligible:
        raise HTTPException(
            status_code=403,
            detail=f"Cannot start assessment: {eligibility.reason}"
        )

    # Get next attempt number
    summary = get_or_create_summary(db, current_user.id, module_id)
    next_attempt = summary.total_attempts + 1

    # Deactivate any existing active sessions
    db.query(AssessmentSession).filter(
        AssessmentSession.teacher_id == current_user.id,
        AssessmentSession.module_id == module_id,
        AssessmentSession.is_active == True
    ).update({"is_active": False})

    # Create new session
    started_at = datetime.now(timezone.utc)
    expires_at = started_at + timedelta(minutes=module.time_limit_minutes or 30)

    session = AssessmentSession(
        teacher_id=current_user.id,
        module_id=module_id,
        attempt_number=next_attempt,
        started_at=started_at,
        expires_at=expires_at,
        is_active=True,
        questions_json=[]  # Will be populated when questions are generated
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return SessionStart(
        session_id=session.id,
        attempt_number=next_attempt,
        started_at=started_at,
        expires_at=expires_at,
        time_limit_minutes=module.time_limit_minutes or 30
    )


@router.get("/history/{module_id}")
async def get_attempt_history(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get attempt history for a specific module
    Returns all attempts with scores, dates, improvement
    """
    attempts = db.query(TeacherAssessmentAttempt).filter(
        TeacherAssessmentAttempt.teacher_id == current_user.id,
        TeacherAssessmentAttempt.module_id == module_id
    ).order_by(desc(TeacherAssessmentAttempt.completed_at)).all()

    if not attempts:
        return {
            "module_id": module_id,
            "total_attempts": 0,
            "attempts": []
        }

    # Calculate improvement for each attempt
    history = []
    for i, attempt in enumerate(reversed(attempts)):  # Chronological order
        improvement = None
        if i > 0:
            previous_score = history[i-1]["score_percentage"]
            improvement = ((attempt.score_percentage - previous_score) / previous_score) * 100

        history.append({
            "attempt_number": attempt.attempt_number,
            "score_percentage": attempt.score_percentage,
            "time_taken_seconds": attempt.time_taken_seconds,
            "completed_at": attempt.completed_at,
            "improvement": improvement
        })

    # Reverse to show most recent first
    history.reverse()

    # Get summary stats
    summary = get_or_create_summary(db, current_user.id, module_id)

    return {
        "module_id": module_id,
        "total_attempts": summary.total_attempts,
        "best_score": summary.best_score,
        "average_score": summary.average_score,
        "improvement_rate": summary.improvement_rate,
        "attempts": history
    }


@router.get("/analytics/{module_id}")
async def get_performance_analytics(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed performance analytics for a module
    Returns: score trends, weak topics, time analysis
    """
    # Get all attempts
    attempts = db.query(TeacherAssessmentAttempt).filter(
        TeacherAssessmentAttempt.teacher_id == current_user.id,
        TeacherAssessmentAttempt.module_id == module_id
    ).order_by(TeacherAssessmentAttempt.completed_at).all()

    if not attempts:
        return {
            "module_id": module_id,
            "message": "No attempts yet"
        }

    # Score trend
    score_trend = [
        {
            "attempt": a.attempt_number,
            "score": a.score_percentage,
            "date": a.completed_at
        }
        for a in attempts
    ]

    # Time analysis
    avg_time = sum(a.time_taken_seconds for a in attempts if a.time_taken_seconds) / len(attempts)

    # Get summary for weak topics
    summary = get_or_create_summary(db, current_user.id, module_id)

    return {
        "module_id": module_id,
        "score_trend": score_trend,
        "weak_topics": summary.weak_topics or [],
        "average_time_seconds": int(avg_time),
        "best_score": summary.best_score,
        "improvement_rate": summary.improvement_rate
    }
