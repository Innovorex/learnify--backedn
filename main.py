from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, teacher, student, modules, assessments, submissions, outcomes, performance, tracking, courses, admin, career_progression, ai_tutor, materials
from security import get_current_user, require_role
from models import User
from models_cpd import CPDCourse, TeacherCourseRecommendation, TeacherCourseProgress

# ✅ NEW IMPORTS
from dotenv import load_dotenv
import os

# ✅ Load environment variables - Override system env vars with .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"), override=True)
api_key = os.getenv("OPENROUTER_API_KEY", "")
print("🔑 OpenRouter Key Loaded:", "✔️" if api_key else "❌ Missing")
if api_key:
    print(f"🔑 Using API Key (first 20 chars): {api_key[:20]}...")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Teacher Evaluation Backend - Phase 1")


# ✅ CORS configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://104.251.271.92:3000",
    "http://104.251.217.92:3000",
    "http://104.251.217.119:3000",
    "https://104.251.271.92",
    "https://104.251.217.92",
    "https://104.251.217.119",
    "https://learnifyteach.innovorex.co.in",  # Production HTTPS frontend
    "http://learnifyteach.innovorex.co.in",   # HTTP redirect
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routers AFTER CORS setup
app.include_router(auth.router)
app.include_router(teacher.router)
app.include_router(student.router)  # NEW: Student K-12 Assessments
app.include_router(modules.router)
app.include_router(assessments.router)
app.include_router(submissions.router)
app.include_router(outcomes.router)
app.include_router(performance.router)
app.include_router(tracking.router)
app.include_router(courses.router)
app.include_router(admin.router)
app.include_router(career_progression.router, prefix="/api")  # NEW: Career Progression
app.include_router(ai_tutor.router)  # NEW: AI Tutor
app.include_router(materials.router, prefix="/api")  # NEW: Teaching Materials Upload

@app.get("/")
def root():
    return {"status": "ok", "message": "Teacher Evaluation API is running", "version": "1.0"}

@app.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role.value}

@app.get("/admin/ping")
def admin_ping(user: User = Depends(require_role("admin"))):
    return {"ok": True, "who": user.email}
