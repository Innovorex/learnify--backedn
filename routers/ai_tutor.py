"""
AI Tutor API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from security import get_current_user
from services.ai_tutor_orchestrator import ai_tutor_orchestrator

router = APIRouter(prefix="/api/ai-tutor", tags=["AI Tutor"])


# Request/Response Models
class StartSessionRequest(BaseModel):
    topic_name: str = Field(..., description="Topic to learn about")
    subject: str = Field(..., description="Subject name")
    grade: str = Field(..., description="Grade level")
    state: str = Field(default="Telangana", description="State for syllabus")
    board: str = Field(default="State Board", description="Board for syllabus")

    model_config = {
        "protected_namespaces": ()
    }


class ChatRequest(BaseModel):
    session_id: int = Field(..., description="Active session ID")
    message: str = Field(..., description="Teacher's question/message")


class SessionResponse(BaseModel):
    session_id: int
    initial_message: str
    syllabus_fetched: bool
    pedagogy_sources: List[dict]
    model_used: str
    created_at: str

    model_config = {
        "protected_namespaces": ()
    }


class ChatResponse(BaseModel):
    session_id: int
    response: str
    additional_sources: List[dict]
    model_used: str
    timestamp: str

    model_config = {
        "protected_namespaces": ()
    }


class SessionHistoryResponse(BaseModel):
    session_id: int
    topic_name: str
    subject: str
    grade: str
    status: str
    created_at: str
    last_activity: str
    message_count: int


# Helper Functions
def get_teacher_qualification(user_id: int, db: Session) -> bool:
    """Check if teacher has B.Ed/M.Ed qualification"""
    try:
        result = db.execute(
            text("SELECT has_bed, has_med FROM teacher_profiles WHERE user_id = :user_id"),
            {"user_id": user_id}
        ).fetchone()

        if result:
            return result[0] or result[1]
        return False

    except Exception as e:
        print(f"[API ERROR] Failed to get teacher qualification: {e}")
        return False


def create_session_db(
    teacher_id: int,
    topic_name: str,
    subject: str,
    grade: str,
    state: str,
    board: str,
    is_bed_qualified: bool,
    db: Session
) -> int:
    """Create new session in database"""
    try:
        session_type = "subject_tutoring" if is_bed_qualified else "pedagogy_tutoring"

        result = db.execute(
            text("""
                INSERT INTO ai_tutor_sessions (
                    teacher_id, topic_name, subject, grade, state, board,
                    session_type, is_bed_qualified, status, created_at, last_activity
                )
                VALUES (:teacher_id, :topic_name, :subject, :grade, :state, :board,
                        :session_type, :is_bed_qualified, 'active', NOW(), NOW())
                RETURNING id
            """),
            {
                "teacher_id": teacher_id,
                "topic_name": topic_name,
                "subject": subject,
                "grade": grade,
                "state": state,
                "board": board,
                "session_type": session_type,
                "is_bed_qualified": is_bed_qualified
            }
        )
        session_id = result.fetchone()[0]
        db.commit()

        print(f"[API] Created session {session_id} for teacher {teacher_id}")
        return session_id

    except Exception as e:
        db.rollback()
        print(f"[API ERROR] Failed to create session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create session"
        )


def save_message_db(
    session_id: int,
    role: str,
    message_content: str,
    agent_name: Optional[str],
    model_used: Optional[str],
    metadata: Optional[dict],
    db: Session
):
    """Save message to database"""
    try:
        import json

        db.execute(
            text("""
                INSERT INTO ai_tutor_messages (
                    session_id, role, message_content, agent_name, model_used, metadata, created_at
                )
                VALUES (:session_id, :role, :message_content, :agent_name, :model_used, CAST(:metadata AS jsonb), NOW())
            """),
            {
                "session_id": session_id,
                "role": role,
                "message_content": message_content,
                "agent_name": agent_name,
                "model_used": model_used,
                "metadata": json.dumps(metadata) if metadata else None
            }
        )

        db.execute(
            text("UPDATE ai_tutor_sessions SET last_activity = NOW() WHERE id = :session_id"),
            {"session_id": session_id}
        )

        db.commit()

    except Exception as e:
        db.rollback()
        print(f"[API ERROR] Failed to save message: {e}")


# API Endpoints
@router.post("/start-session", response_model=SessionResponse)
async def start_ai_tutor_session(
    request: StartSessionRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new AI Tutor session"""
    teacher_id = current_user.id

    if current_user.role.value != 'teacher':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="AI Tutor is only available for teachers"
        )

    try:
        is_bed_qualified = get_teacher_qualification(teacher_id, db)

        session_id = create_session_db(
            teacher_id=teacher_id,
            topic_name=request.topic_name,
            subject=request.subject,
            grade=request.grade,
            state=request.state,
            board=request.board,
            is_bed_qualified=is_bed_qualified,
            db=db
        )

        result = await ai_tutor_orchestrator.start_session(
            session_id=session_id,
            teacher_id=teacher_id,
            topic_name=request.topic_name,
            subject=request.subject,
            grade=request.grade,
            state=request.state,
            board=request.board,
            is_bed_qualified=is_bed_qualified
        )

        save_message_db(
            session_id=session_id,
            role="assistant",
            message_content=result["initial_message"],
            agent_name="AI Tutor",
            model_used=result["model_used"],
            metadata={
                "pedagogy_sources": result["pedagogy_sources"],
                "syllabus_fetched": result["syllabus_fetched"]
            },
            db=db
        )

        return SessionResponse(
            session_id=session_id,
            initial_message=result["initial_message"],
            syllabus_fetched=result["syllabus_fetched"],
            pedagogy_sources=result["pedagogy_sources"],
            model_used=result["model_used"],
            created_at=datetime.now().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"[API ERROR] Start session failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start AI Tutor session: {str(e)}"
        )


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai_tutor(
    request: ChatRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message in an active session"""
    teacher_id = current_user.id

    try:
        result = db.execute(
            text("""
                SELECT subject, grade, is_bed_qualified, status
                FROM ai_tutor_sessions
                WHERE id = :session_id AND teacher_id = :teacher_id
            """),
            {"session_id": request.session_id, "teacher_id": teacher_id}
        ).fetchone()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found or unauthorized"
            )

        session = {
            "subject": result[0],
            "grade": result[1],
            "is_bed_qualified": result[2],
            "status": result[3]
        }

        if session['status'] != 'active':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session is not active"
            )

        save_message_db(
            session_id=request.session_id,
            role="user",
            message_content=request.message,
            agent_name=None,
            model_used=None,
            metadata=None,
            db=db
        )

        result = await ai_tutor_orchestrator.chat(
            session_id=request.session_id,
            user_message=request.message,
            subject=session['subject'],
            grade=session['grade'],
            is_bed_qualified=session['is_bed_qualified']
        )

        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )

        save_message_db(
            session_id=request.session_id,
            role="assistant",
            message_content=result["response"],
            agent_name="AI Tutor",
            model_used=result["model_used"],
            metadata={"additional_sources": result["additional_sources"]},
            db=db
        )

        return ChatResponse(
            session_id=request.session_id,
            response=result["response"],
            additional_sources=result["additional_sources"],
            model_used=result["model_used"],
            timestamp=result["timestamp"]
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"[API ERROR] Chat failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )


@router.get("/sessions", response_model=List[SessionHistoryResponse])
async def get_teacher_sessions(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all AI Tutor sessions for the current teacher"""
    teacher_id = current_user.id

    try:
        results = db.execute(
            text("""
                SELECT
                    s.id as session_id,
                    s.topic_name,
                    s.subject,
                    s.grade,
                    s.status,
                    s.created_at,
                    s.last_activity,
                    COUNT(m.id) as message_count
                FROM ai_tutor_sessions s
                LEFT JOIN ai_tutor_messages m ON s.id = m.session_id
                WHERE s.teacher_id = :teacher_id
                GROUP BY s.id
                ORDER BY s.last_activity DESC
                LIMIT 50
            """),
            {"teacher_id": teacher_id}
        ).fetchall()

        return [
            SessionHistoryResponse(
                session_id=row[0],
                topic_name=row[1],
                subject=row[2],
                grade=row[3],
                status=row[4],
                created_at=row[5].isoformat(),
                last_activity=row[6].isoformat(),
                message_count=row[7]
            )
            for row in results
        ]

    except Exception as e:
        print(f"[API ERROR] Failed to get sessions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve sessions"
        )


@router.get("/session/{session_id}/messages")
async def get_session_messages(
    session_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all messages for a specific session"""
    teacher_id = current_user.id

    try:
        session_check = db.execute(
            text("""
                SELECT id FROM ai_tutor_sessions
                WHERE id = :session_id AND teacher_id = :teacher_id
            """),
            {"session_id": session_id, "teacher_id": teacher_id}
        ).fetchone()

        if not session_check:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        messages = db.execute(
            text("""
                SELECT
                    role,
                    message_content,
                    agent_name,
                    model_used,
                    metadata,
                    created_at
                FROM ai_tutor_messages
                WHERE session_id = :session_id
                ORDER BY created_at ASC
            """),
            {"session_id": session_id}
        ).fetchall()

        return {
            "session_id": session_id,
            "messages": [
                {
                    "role": m[0],
                    "content": m[1],
                    "agent": m[2],
                    "model": m[3],
                    "metadata": m[4],
                    "timestamp": m[5].isoformat()
                }
                for m in messages
            ]
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"[API ERROR] Failed to get messages: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve messages"
        )


@router.patch("/session/{session_id}/close")
async def close_session(
    session_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Close an active AI Tutor session"""
    teacher_id = current_user.id

    try:
        result = db.execute(
            text("""
                UPDATE ai_tutor_sessions
                SET status = 'completed'
                WHERE id = :session_id AND teacher_id = :teacher_id AND status = 'active'
                RETURNING id
            """),
            {"session_id": session_id, "teacher_id": teacher_id}
        ).fetchone()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Active session not found"
            )

        db.commit()
        ai_tutor_orchestrator.clear_session(session_id)

        return {"message": "Session closed successfully", "session_id": session_id}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"[API ERROR] Failed to close session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to close session"
        )
