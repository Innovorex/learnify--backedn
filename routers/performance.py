# routers/performance.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Module, Performance, GrowthPlan, User
from schemas import PerformanceSummaryOut, ModuleScore, BenchmarkOut, GrowthPlanIn, GrowthPlanOut
from security import require_role
from services.analysis import collect_teacher_module_scores, rating_from_score, benchmark_vs_cohort, generate_growth_plan, WEIGHTS

router = APIRouter(prefix="/performance", tags=["performance"])

@router.get("/summary/me", response_model=PerformanceSummaryOut)
def my_summary(db: Session = Depends(get_db), user: User = Depends(require_role("teacher"))):
    module_scores, type_avgs, overall = collect_teacher_module_scores(db, user.id)
    # enrich + rating
    module_scores_out = [ModuleScore(**ms) for ms in module_scores]
    weighted_breakdown = {
        "mcq": round(type_avgs["mcq"], 2),
        "submission": round(type_avgs["submission"], 2),
        "outcome": round(type_avgs["outcome"], 2),
    }
    bench = benchmark_vs_cohort(db, user.id)
    bench_out = BenchmarkOut(**bench)
    return PerformanceSummaryOut(
        overall_score=overall,
        overall_rating=rating_from_score(overall),
        weighted_breakdown=weighted_breakdown,
        module_scores=module_scores_out,
        benchmark=bench_out
    )

@router.get("/admin/teacher/{teacher_id}", response_model=PerformanceSummaryOut)
def admin_teacher_summary(teacher_id: int,
                          db: Session = Depends(get_db),
                          admin: User = Depends(require_role("admin"))):
    module_scores, type_avgs, overall = collect_teacher_module_scores(db, teacher_id)
    module_scores_out = [ModuleScore(**ms) for ms in module_scores]
    weighted_breakdown = {
        "mcq": round(type_avgs["mcq"], 2),
        "submission": round(type_avgs["submission"], 2),
        "outcome": round(type_avgs["outcome"], 2),
    }
    bench = benchmark_vs_cohort(db, teacher_id)
    bench_out = BenchmarkOut(**bench)
    return PerformanceSummaryOut(
        overall_score=overall,
        overall_rating=rating_from_score(overall),
        weighted_breakdown=weighted_breakdown,
        module_scores=module_scores_out,
        benchmark=bench_out
    )

@router.post("/growth-plan/me", response_model=GrowthPlanOut)
async def make_growth_plan_me(payload: GrowthPlanIn | None = None,
                              db: Session = Depends(get_db),
                              user: User = Depends(require_role("teacher"))):
    content = await generate_growth_plan(db, user.id, focus_areas=(payload.focus_areas if payload else None))
    return GrowthPlanOut(content=content)

@router.get("/admin/leaderboard")
def admin_leaderboard(limit: int = 20,
                      db: Session = Depends(get_db),
                      admin: User = Depends(require_role("admin"))):
    # Rank by average performance.score across modules
    from sqlalchemy import func
    rows = (db.query(Performance.teacher_id, func.avg(Performance.score).label("avg_score"))
              .group_by(Performance.teacher_id)
              .order_by(func.avg(Performance.score).desc())
              .limit(limit)
              .all())
    # Return simple list
    out = []
    for tid, avg in rows:
        u = db.query(User).filter_by(id=tid).first()
        out.append({"teacher_id": tid, "name": u.name if u else f"Teacher {tid}", "avg_score": round(float(avg or 0.0), 2)})
    return {"weights": WEIGHTS, "leaderboard": out}