# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
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


@router.post("/login-with-erpnext")
async def login_with_erpnext(
    payload: LoginIn,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Login using ERPNext portal credentials or local credentials

    Flow:
    1. Try to authenticate against ERPNext portal
    2. If ERPNext auth fails, fall back to local authentication
    3. Check if user exists locally
    4. If not, create local account and sync profile (ERPNext only)
    5. If yes and data is stale, trigger background sync
    6. Issue local JWT token
    """
    from services.erpnext_client import get_erpnext_client
    from services.erpnext_sync_service import get_sync_service
    from datetime import datetime, timedelta

    # Step 1: Try to authenticate with ERPNext
    client = get_erpnext_client()
    erpnext_auth = await client.authenticate_user(payload.email, payload.password)

    # If ERPNext auth fails, try local authentication
    if not erpnext_auth["success"]:
        user = db.query(User).filter(User.email == payload.email.lower()).first()
        if user and verify_password(payload.password, user.password_hash):
            # Local authentication successful
            token = create_access_token({
                "user_id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role.value
            })
            return {
                "access_token": token,
                "token_type": "bearer",
                "user": UserOut.model_validate(user),
                "erpnext_synced": False
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

    # Step 2: Check if user exists locally
    user = db.query(User).filter(User.email == payload.email.lower()).first()

    if not user:
        # First-time login: Create user and sync profile
        sync_service = get_sync_service(db)
        sync_result = await sync_service.sync_teacher(payload.email)

        if not sync_result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to sync profile: {sync_result.get('error')}"
            )

        user = sync_result["user"]

        # Set password from ERPNext login (encrypted)
        user.password_hash = hash_password(payload.password)
        db.commit()
        db.refresh(user)

    else:
        # Existing user: Check if sync needed (> 24 hours old)
        needs_sync = False
        if user.erpnext_last_sync:
            age = datetime.now() - user.erpnext_last_sync
            if age > timedelta(hours=24):
                needs_sync = True
        else:
            needs_sync = True

        if needs_sync:
            # Trigger background sync
            sync_service = get_sync_service(db)
            background_tasks.add_task(sync_service.sync_teacher, payload.email)

    # Step 3: Issue local JWT token
    token = create_access_token({
        "user_id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role.value
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserOut.model_validate(user),
        "erpnext_synced": user.erpnext_synced
    }


@router.post("/student-login")
async def student_login(
    payload: LoginIn,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Student login using ERPNext portal credentials or local credentials

    Flow:
    1. Try to authenticate against ERPNext portal
    2. If ERPNext auth fails, fall back to local authentication
    3. Check if student exists locally
    4. If not, create account and sync student profile from ERPNext (ERPNext only)
    5. If yes and data is stale (>24h), trigger background sync
    6. Issue JWT token with student role
    """
    from services.erpnext_client import get_erpnext_client
    from services.erpnext_sync_service import get_sync_service
    from datetime import datetime, timedelta

    # Step 1: Try to authenticate with ERPNext
    client = get_erpnext_client()
    erpnext_auth = await client.authenticate_user(payload.email, payload.password)

    # If ERPNext auth fails, try local authentication
    if not erpnext_auth["success"]:
        user = db.query(User).filter(User.email == payload.email.lower()).first()
        if user and verify_password(payload.password, user.password_hash):
            # Local authentication successful
            token = create_access_token({
                "user_id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role.value
            })
            return {
                "access_token": token,
                "token_type": "bearer",
                "user": UserOut.model_validate(user),
                "student_synced": False
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

    # Step 2: Check if user exists locally
    user = db.query(User).filter(User.email == payload.email.lower()).first()

    student_synced = False

    if not user:
        # First-time login: Create student and sync profile
        sync_service = get_sync_service(db)
        sync_result = await sync_service.sync_student(payload.email)

        if not sync_result["success"]:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to sync student profile: {sync_result.get('error')}"
            )

        user = sync_result["user"]

        # Set password from ERPNext login
        user.password_hash = hash_password(payload.password)
        db.commit()
        db.refresh(user)

        student_synced = True

    else:
        # Existing user: Check if sync needed (> 24 hours old)
        needs_sync = False

        # Check last sync from student mapping table
        from sqlalchemy import text
        mapping = db.execute(
            text("SELECT last_synced_at FROM erpnext_student_mapping WHERE local_student_id = :user_id"),
            {"user_id": user.id}
        ).fetchone()

        if mapping and mapping[0]:
            age = datetime.now() - mapping[0]
            if age > timedelta(hours=24):
                needs_sync = True
        else:
            needs_sync = True

        if needs_sync:
            # Trigger background sync
            sync_service = get_sync_service(db)
            background_tasks.add_task(sync_service.sync_student, payload.email)

    # Step 3: Ensure user is student role
    if user.role.value != "student":
        raise HTTPException(
            status_code=403,
            detail="This login is for students only. Please use teacher login if you are a teacher."
        )

    # Step 4: Issue JWT token
    token = create_access_token({
        "user_id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role.value,
        "class": user.class_name,
        "section": user.section
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.value,
            "class_name": user.class_name,
            "section": user.section,
            "roll_number": user.roll_number
        },
        "student_synced": student_synced,
        "message": "Login successful! Profile synced from ERPNext." if student_synced else "Login successful!"
    }
