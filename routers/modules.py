# routers/modules.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Module
from schemas import ModuleOut, ModuleIn
from typing import Optional

router = APIRouter(prefix="/modules", tags=["modules"])

@router.post("/", response_model=ModuleOut, status_code=201)
def create_module(module_in: ModuleIn, db: Session = Depends(get_db)):
    db_module = Module(**module_in.dict())
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module

@router.get("/", response_model=list[ModuleOut])
def list_modules(
    category: Optional[str] = Query(None, description="Filter by category: knowledge, portfolio, outcomes"),
    db: Session = Depends(get_db)
):
    """
    Get all modules, optionally filtered by category.

    Categories:
    - knowledge: MCQ-based knowledge assessments
    - portfolio: Submission-based portfolio evidence
    - outcomes: Student outcome tracking
    """
    query = db.query(Module)

    if category:
        query = query.filter(Module.category == category)

    return query.all()

@router.get("/categories/summary")
def get_category_summary(db: Session = Depends(get_db)):
    """
    Get count of modules in each category for dashboard stats.

    Returns:
    {
        "knowledge": 6,
        "portfolio": 3,
        "outcomes": 1,
        "total": 10
    }
    """
    results = db.query(
        Module.category,
        func.count(Module.id).label('count')
    ).group_by(Module.category).all()

    summary = {row.category: row.count for row in results}
    summary['total'] = sum(summary.values())

    return summary
