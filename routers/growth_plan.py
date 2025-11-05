"""
Growth Plan Router - Complete API for enhanced growth plan management
Handles generation, action tracking, insights, and preferences
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import User, GrowthPlan, GrowthPlanAction, GrowthPlanInsight, Performance
from schemas import (
    GrowthPlanOut, GrowthPlanGenerateRequest,
    ActionOut, ActionCompleteRequest,
    InsightOut, RegenerationTriggerOut
)
from security import require_role
from services.growth_plan_context import GrowthPlanContextCollector
from services.growth_plan_prompt_engineer import GrowthPlanPromptEngineer
from services.action_extractor import ActionExtractor
from services.openrouter import generate_subject_knowledge_questions_ai_requests
from datetime import datetime, timedelta
from typing import List, Optional
import json

router = APIRouter(prefix="/growth-plan", tags=["growth-plan"])


# ============================================================================
# GENERATION ENDPOINTS
# ============================================================================

@router.post("/generate", response_model=GrowthPlanOut)
async def generate_growth_plan(
    request: GrowthPlanGenerateRequest = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Generate comprehensive growth plan using full platform context
    Automatically extracts actionable items
    """
    try:
        # 1. Collect comprehensive context
        collector = GrowthPlanContextCollector(db)
        context = await collector.collect_full_context(user.id)

        # 2. Build AI prompt
        prompt_engineer = GrowthPlanPromptEngineer()
        focus_areas = request.focus_areas if request else None
        prompt = prompt_engineer.build_holistic_prompt(context, focus_areas=focus_areas)

        # 3. Generate with OpenRouter
        ai_response = generate_subject_knowledge_questions_ai_requests(prompt)

        if ai_response.startswith("Error") or len(ai_response) < 500:
            raise ValueError("AI generation failed or insufficient content")

        # 4. Deactivate old plans
        db.query(GrowthPlan).filter_by(
            teacher_id=user.id,
            is_active=True
        ).update({"is_active": False})

        # 5. Create new growth plan
        growth_plan = GrowthPlan(
            teacher_id=user.id,
            content=ai_response,
            generated_context=json.dumps(context),
            plan_version=1,
            is_active=True,
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        db.add(growth_plan)
        db.flush()  # Get ID before actions

        # 6. Extract and create actions
        extractor = ActionExtractor(db)
        actions = await extractor.extract_actions(ai_response, context, growth_plan.id)

        for action_data in actions:
            action = GrowthPlanAction(**action_data, growth_plan_id=growth_plan.id)
            db.add(action)

        db.commit()
        db.refresh(growth_plan)

        # 7. Format response
        return GrowthPlanOut(
            id=growth_plan.id,
            content=growth_plan.content,
            created_at=growth_plan.created_at.isoformat() if growth_plan.created_at else None,
            expires_at=growth_plan.expires_at.isoformat() if growth_plan.expires_at else None,
            actions=[{
                "id": a.id,
                "growth_plan_id": a.growth_plan_id,
                "action_type": a.action_type,
                "action_title": a.action_title,
                "action_description": a.action_description,
                "priority": a.priority,
                "target_date": a.target_date.isoformat() if a.target_date else None,
                "estimated_time_minutes": a.estimated_time_minutes,
                "target_cpd_module_id": a.target_cpd_module_id,
                "target_cpd_course_id": a.target_cpd_course_id,
                "target_career_module_id": a.target_career_module_id,
                "external_url": a.external_url,
                "status": a.status,
                "started_at": a.started_at.isoformat() if a.started_at else None,
                "completed_at": a.completed_at.isoformat() if a.completed_at else None,
                "time_spent_minutes": a.time_spent_minutes,
                "completion_notes": a.completion_notes,
                "display_order": a.display_order,
                "created_at": a.created_at.isoformat() if a.created_at else None
            } for a in growth_plan.actions],
            context_summary={
                "overall_score": context["cpd_performance"]["overall_score"],
                "focus_areas": [m["module_name"] for m in context["cpd_performance"]["weak_modules"][:3]],
                "trend": context["improvement_trends"]["trend"]
            }
        )

    except Exception as e:
        db.rollback()
        print(f"Error generating growth plan: {str(e)}")
        raise HTTPException(500, f"Failed to generate growth plan: {str(e)}")


@router.get("/current", response_model=GrowthPlanOut)
async def get_current_growth_plan(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """Get teacher's current active growth plan"""
    plan = db.query(GrowthPlan).filter_by(
        teacher_id=user.id,
        is_active=True
    ).order_by(GrowthPlan.created_at.desc()).first()

    if not plan:
        raise HTTPException(404, "No active growth plan found")

    return GrowthPlanOut(
        id=plan.id,
        content=plan.content,
        created_at=plan.created_at.isoformat() if plan.created_at else None,
        expires_at=plan.expires_at.isoformat() if plan.expires_at else None,
        actions=[{
            "id": a.id,
            "growth_plan_id": a.growth_plan_id,
            "action_type": a.action_type,
            "action_title": a.action_title,
            "action_description": a.action_description,
            "priority": a.priority,
            "target_date": a.target_date.isoformat() if a.target_date else None,
            "estimated_time_minutes": a.estimated_time_minutes,
            "target_cpd_module_id": a.target_cpd_module_id,
            "target_cpd_course_id": a.target_cpd_course_id,
            "target_career_module_id": a.target_career_module_id,
            "external_url": a.external_url,
            "status": a.status,
            "started_at": a.started_at.isoformat() if a.started_at else None,
            "completed_at": a.completed_at.isoformat() if a.completed_at else None,
            "time_spent_minutes": a.time_spent_minutes,
            "completion_notes": a.completion_notes,
            "display_order": a.display_order,
            "created_at": a.created_at.isoformat() if a.created_at else None
        } for a in plan.actions]
    )


@router.get("/should-regenerate", response_model=RegenerationTriggerOut)
async def check_regeneration_trigger(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Check if growth plan should be regenerated
    Returns trigger reason if applicable
    """
    latest_plan = db.query(GrowthPlan).filter_by(
        teacher_id=user.id,
        is_active=True
    ).order_by(GrowthPlan.created_at.desc()).first()

    if not latest_plan:
        return RegenerationTriggerOut(
            should_regenerate=True,
            reason="no_active_plan",
            urgency="high"
        )

    days_since = (datetime.utcnow() - latest_plan.created_at).days

    # Trigger 1: Time-based (30+ days)
    if days_since > 30:
        return RegenerationTriggerOut(
            should_regenerate=True,
            reason=f"Plan is {days_since} days old",
            urgency="medium"
        )

    # Trigger 2: All actions completed
    actions = latest_plan.actions
    if actions and all(a.status == "completed" for a in actions):
        return RegenerationTriggerOut(
            should_regenerate=True,
            reason="All actions completed! Time for new challenges.",
            urgency="high"
        )

    # Trigger 3: New assessment completed
    latest_assessment = db.query(Performance).filter_by(
        teacher_id=user.id
    ).order_by(Performance.created_at.desc()).first()

    if latest_assessment and latest_assessment.created_at > latest_plan.created_at:
        return RegenerationTriggerOut(
            should_regenerate=True,
            reason="New assessment completed with updated performance data",
            urgency="high"
        )

    # Trigger 4: Significant score change
    if latest_plan.generated_context:
        try:
            old_context = json.loads(latest_plan.generated_context)
            old_score = old_context.get("cpd_performance", {}).get("overall_score", 0)
            from services.analysis import collect_teacher_module_scores
            _, _, current_score = collect_teacher_module_scores(db, user.id)

            if abs(current_score - old_score) > 15:
                return RegenerationTriggerOut(
                    should_regenerate=True,
                    reason=f"Significant score change: {old_score:.0f}% → {current_score:.0f}%",
                    urgency="medium"
                )
        except:
            pass

    return RegenerationTriggerOut(
        should_regenerate=False,
        reason=None,
        urgency=None
    )


# ============================================================================
# ACTION MANAGEMENT ENDPOINTS
# ============================================================================

@router.get("/actions", response_model=List[ActionOut])
async def get_actions(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """Get all actions for current growth plan with optional filtering"""
    latest_plan = db.query(GrowthPlan).filter_by(
        teacher_id=user.id,
        is_active=True
    ).order_by(GrowthPlan.created_at.desc()).first()

    if not latest_plan:
        return []

    query = db.query(GrowthPlanAction).filter_by(growth_plan_id=latest_plan.id)

    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)

    actions = query.order_by(
        GrowthPlanAction.display_order,
        GrowthPlanAction.priority.desc()
    ).all()

    return [ActionOut(
        id=a.id,
        growth_plan_id=a.growth_plan_id,
        action_type=a.action_type,
        action_title=a.action_title,
        action_description=a.action_description,
        priority=a.priority,
        target_date=a.target_date.isoformat() if a.target_date else None,
        estimated_time_minutes=a.estimated_time_minutes,
        target_cpd_module_id=a.target_cpd_module_id,
        target_cpd_course_id=a.target_cpd_course_id,
        target_career_module_id=a.target_career_module_id,
        external_url=a.external_url,
        status=a.status,
        started_at=a.started_at.isoformat() if a.started_at else None,
        completed_at=a.completed_at.isoformat() if a.completed_at else None,
        time_spent_minutes=a.time_spent_minutes,
        completion_notes=a.completion_notes,
        display_order=a.display_order,
        created_at=a.created_at.isoformat() if a.created_at else None
    ) for a in actions]


@router.post("/actions/{action_id}/start")
async def start_action(
    action_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """Mark action as in-progress and track start time"""
    action = db.query(GrowthPlanAction).join(GrowthPlan).filter(
        GrowthPlanAction.id == action_id,
        GrowthPlan.teacher_id == user.id
    ).first()

    if not action:
        raise HTTPException(404, "Action not found")

    action.status = "in_progress"
    action.started_at = datetime.utcnow()
    db.commit()

    return {"success": True, "action_id": action_id, "status": "in_progress"}


@router.post("/actions/{action_id}/complete")
async def complete_action(
    action_id: int,
    request: ActionCompleteRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Mark action as completed
    Calculates time spent and checks for celebration triggers
    """
    action = db.query(GrowthPlanAction).join(GrowthPlan).filter(
        GrowthPlanAction.id == action_id,
        GrowthPlan.teacher_id == user.id
    ).first()

    if not action:
        raise HTTPException(404, "Action not found")

    action.status = "completed"
    action.completed_at = datetime.utcnow()
    action.completion_notes = request.notes
    action.evidence_urls = json.dumps(request.evidence_urls) if request.evidence_urls else None

    # Calculate time spent
    if action.started_at:
        time_spent = (action.completed_at - action.started_at).total_seconds() / 60
        action.time_spent_minutes = int(time_spent)

    db.commit()

    # Check completion statistics
    growth_plan = action.growth_plan
    all_actions = growth_plan.actions
    completed_count = len([a for a in all_actions if a.status == "completed"])
    total_count = len(all_actions)
    completion_percentage = (completed_count / total_count * 100) if total_count > 0 else 0

    # Celebration logic
    celebration = None
    if completed_count == total_count:
        celebration = {
            "type": "all_completed",
            "message": "🎉 Amazing! You've completed all actions in your growth plan!",
            "next_step": "Generate a new plan to continue your professional journey."
        }
    elif completed_count % 5 == 0:  # Milestone every 5 actions
        celebration = {
            "type": "milestone",
            "message": f"🏆 Milestone reached! {completed_count} actions completed!",
            "next_step": f"Keep going! Only {total_count - completed_count} actions remaining."
        }

    return {
        "success": True,
        "action_id": action_id,
        "completed_at": action.completed_at.isoformat(),
        "time_spent_minutes": action.time_spent_minutes,
        "progress": {
            "completed": completed_count,
            "total": total_count,
            "percentage": round(completion_percentage, 1)
        },
        "celebration": celebration
    }


@router.get("/progress")
async def get_progress_summary(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """Get comprehensive progress statistics"""
    latest_plan = db.query(GrowthPlan).filter_by(
        teacher_id=user.id,
        is_active=True
    ).first()

    if not latest_plan:
        return {"error": "No active plan"}

    actions = latest_plan.actions
    completed = [a for a in actions if a.status == "completed"]
    in_progress = [a for a in actions if a.status == "in_progress"]
    pending = [a for a in actions if a.status == "pending"]

    # Calculate streak
    streak_days = 0
    check_date = datetime.utcnow().date()
    for i in range(30):
        day_actions = [a for a in completed if a.completed_at and a.completed_at.date() == check_date]
        if day_actions:
            streak_days += 1
            check_date -= timedelta(days=1)
        else:
            break

    total_time_spent = sum(a.time_spent_minutes or 0 for a in completed)

    return {
        "plan_id": latest_plan.id,
        "created_at": latest_plan.created_at.isoformat() if latest_plan.created_at else None,
        "expires_at": latest_plan.expires_at.isoformat() if latest_plan.expires_at else None,
        "days_remaining": (latest_plan.expires_at - datetime.utcnow()).days if latest_plan.expires_at else None,
        "total_actions": len(actions),
        "completed_actions": len(completed),
        "in_progress_actions": len(in_progress),
        "pending_actions": len(pending),
        "completion_percentage": round((len(completed) / len(actions) * 100) if actions else 0, 1),
        "streak_days": streak_days,
        "total_time_spent_hours": round(total_time_spent / 60, 1)
    }


# ============================================================================
# INSIGHTS ENDPOINTS
# ============================================================================

@router.get("/insights", response_model=List[InsightOut])
async def get_relevant_insights(
    limit: int = Query(5, le=20),
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """
    Get relevant peer insights based on teacher's context
    Returns anonymized success stories
    """
    # Find verified insights ordered by helpful count
    insights = db.query(GrowthPlanInsight).filter(
        GrowthPlanInsight.is_verified == True
    ).order_by(
        GrowthPlanInsight.helpful_count.desc(),
        GrowthPlanInsight.created_at.desc()
    ).limit(limit).all()

    return [InsightOut(
        id=i.id,
        strategy_type=i.strategy_type,
        challenge=i.challenge,
        solution=i.solution,
        outcome=i.outcome,
        context_tags=json.loads(i.context_tags) if i.context_tags else [],
        view_count=i.view_count,
        helpful_count=i.helpful_count,
        not_helpful_count=i.not_helpful_count,
        try_count=i.try_count,
        is_verified=i.is_verified,
        is_featured=i.is_featured,
        contributed_by=i.contributed_by,
        created_at=i.created_at.isoformat() if i.created_at else None
    ) for i in insights]


@router.post("/insights/{insight_id}/helpful")
async def mark_insight_helpful(
    insight_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    """Mark an insight as helpful (upvote)"""
    insight = db.query(GrowthPlanInsight).filter_by(id=insight_id).first()

    if not insight:
        raise HTTPException(404, "Insight not found")

    insight.helpful_count += 1
    insight.view_count += 1
    db.commit()

    return {"success": True, "helpful_count": insight.helpful_count}
