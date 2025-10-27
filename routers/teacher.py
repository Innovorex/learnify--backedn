# routers/teacher.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import TeacherProfile, User
from schemas import TeacherProfileIn, TeacherProfileOut
from security import get_current_user, require_role

router = APIRouter(prefix="/teacher", tags=["teacher"])

@router.post("/profile", response_model=TeacherProfileOut, status_code=201)
def create_profile(payload: TeacherProfileIn,
                   db: Session = Depends(get_db),
                   user: User = Depends(require_role("teacher"))):
    # Check if profile already exists
    exists = db.query(TeacherProfile).filter(TeacherProfile.user_id == user.id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Profile already exists")

    profile = TeacherProfile(
        user_id=user.id,
        education=payload.education,
        grades_teaching=payload.grades_teaching,
        subjects_teaching=payload.subjects_teaching,
        experience_years=payload.experience_years,
        board=payload.board,
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/profile/me", response_model=TeacherProfileOut)
def get_my_profile(db: Session = Depends(get_db),
                   user: User = Depends(require_role("teacher"))):
    profile = db.query(TeacherProfile).filter(TeacherProfile.user_id == user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
