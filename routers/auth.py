# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, Role
from schemas import SignupIn, LoginIn, UserOut
from security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserOut, status_code=201)
def signup(payload: SignupIn, db: Session = Depends(get_db)):
    if payload.password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    exists = db.query(User).filter(User.email == payload.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Validate student-specific fields
    if payload.role == "student":
        if not payload.class_name or not payload.section:
            raise HTTPException(
                status_code=400,
                detail="Class name and section are required for student registration"
            )

    user = User(
        name=payload.name.strip(),
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        role=Role(payload.role),
        # Student-specific fields
        class_name=payload.class_name if payload.role == "student" else None,
        section=payload.section if payload.role == "student" else None,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id, "name": user.name, "role": user.role.value})
    return {"access_token": token, "token_type": "bearer", "user": UserOut.model_validate(user)}
