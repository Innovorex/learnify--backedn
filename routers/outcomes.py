# routers/outcomes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, Module, Performance
from schemas import OutcomeIngestIn
from security import require_role

router = APIRouter(prefix="/outcomes", tags=["outcomes"])

@router.post("/ingest/{module_id}")
def ingest_outcomes(module_id: int,
                    payload: OutcomeIngestIn,
                    db: Session = Depends(get_db),
                    admin: User = Depends(require_role("admin"))):
    module = db.query(Module).filter_by(id=module_id).first()
    if not module:
        raise HTTPException(404, "Module not found")
    if module.assessment_type != "outcome":
        raise HTTPException(400, "This module is not outcome-based")

    # Very simple aggregation: average value -> score out of 100
    if not payload.entries:
        raise HTTPException(400, "No entries provided")
    avg = sum([e.value for e in payload.entries]) / len(payload.entries)

    # For demo: attach to ALL teachers? Usually you’d target a specific teacher_id.
    # Here we’ll require a query param or change later; for now raise to be explicit.
    raise HTTPException(400, "Design decision: supply a teacher_id or batch mapping in a future step.")
