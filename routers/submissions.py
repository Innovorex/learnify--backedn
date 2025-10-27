# routers/submissions.py
import os, uuid
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db
from models import User, Module, TeacherSubmission, Performance
from schemas import SubmissionCreateOut, SubmissionValidateIn
from security import require_role
from datetime import datetime

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")

router = APIRouter(prefix="/submission", tags=["submission"])

@router.post("/upload/{module_id}", response_model=SubmissionCreateOut)
async def upload_submission(module_id: int,
                            file: UploadFile | None = File(default=None),
                            notes: str | None = Form(default=None),
                            db: Session = Depends(get_db),
                            user: User = Depends(require_role("teacher"))):
    module = db.query(Module).filter_by(id=module_id).first()
    if not module:
        raise HTTPException(404, "Module not found")
    if module.assessment_type != "submission":
        raise HTTPException(400, "This module is not submission-based")

    # Save file if provided
    saved_path = None
    if file:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        user_dir = os.path.join(UPLOAD_DIR, f"teacher_{user.id}")
        os.makedirs(user_dir, exist_ok=True)
        ext = os.path.splitext(file.filename or "")[-1]
        fname = f"{uuid.uuid4().hex}{ext}"
        saved_path = os.path.join(user_dir, fname)
        with open(saved_path, "wb") as f:
            f.write(await file.read())

    # (Optional) AI extraction / suggestion can be added here later.
    sub = TeacherSubmission(
        teacher_id=user.id,
        module_id=module_id,
        file_path=saved_path,
        notes=notes,
        extracted_text=None,
        ai_suggested_score=None,  # you can fill after OCR/LLM
        status="pending"
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return SubmissionCreateOut(submission_id=sub.id, status=sub.status, ai_suggested_score=sub.ai_suggested_score)

@router.post("/validate/{submission_id}")
def validate_submission(submission_id: int,
                        payload: SubmissionValidateIn,
                        db: Session = Depends(get_db),
                        admin: User = Depends(require_role("admin"))):
    sub = db.query(TeacherSubmission).filter_by(id=submission_id).first()
    if not sub:
        raise HTTPException(404, "Submission not found")

    if payload.status not in ("approved", "rejected"):
        raise HTTPException(400, "Invalid status")

    sub.status = payload.status
    sub.admin_validated_score = payload.admin_validated_score if payload.status == "approved" else 0
    db.commit()

    # When approved, write/update Performance for this module
    if payload.status == "approved":
        rating = "Excellent" if payload.admin_validated_score >= 85 else "Good" if payload.admin_validated_score >= 60 else "Needs Improvement"
        perf = db.query(Performance).filter_by(teacher_id=sub.teacher_id, module_id=sub.module_id).first()
        if not perf:
            perf = Performance(teacher_id=sub.teacher_id,
                               module_id=sub.module_id,
                               score=float(payload.admin_validated_score),
                               rating=rating,
                               details="Submission validated by admin")
            db.add(perf)
        else:
            perf.score = float(payload.admin_validated_score)
            perf.rating = rating
            perf.details = "Submission validated by admin"
        db.commit()

        # Log performance history for timeline tracking
        from services.tracking import log_performance_history
        log_performance_history(db, sub.teacher_id, sub.module_id, float(payload.admin_validated_score), rating)

    return {"ok": True, "submission_id": sub.id, "status": sub.status}

@router.get("/admin/all")
def get_all_submissions(
    status: str | None = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("admin"))
):
    """Get all submissions for admin review, optionally filtered by status"""
    query = db.query(TeacherSubmission, User, Module).join(
        User, TeacherSubmission.teacher_id == User.id
    ).join(
        Module, TeacherSubmission.module_id == Module.id
    )

    if status:
        query = query.filter(TeacherSubmission.status == status)

    results = query.order_by(TeacherSubmission.created_at.desc()).all()

    submissions = []
    for sub, teacher, module in results:
        submissions.append({
            "id": sub.id,
            "teacher_id": teacher.id,
            "teacher_name": teacher.name,
            "module_id": module.id,
            "module_name": module.name,
            "file_path": sub.file_path,
            "notes": sub.notes,
            "status": sub.status,
            "ai_suggested_score": sub.ai_suggested_score,
            "admin_validated_score": sub.admin_validated_score,
            "created_at": sub.created_at.isoformat() if sub.created_at else None
        })

    return {"submissions": submissions}

@router.get("/admin/file/{submission_id}")
def get_submission_file(
    submission_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("admin"))
):
    """Download/view the submitted file"""
    sub = db.query(TeacherSubmission).filter_by(id=submission_id).first()
    if not sub:
        raise HTTPException(404, "Submission not found")

    if not sub.file_path or not os.path.exists(sub.file_path):
        raise HTTPException(404, "File not found")

    return FileResponse(sub.file_path)
