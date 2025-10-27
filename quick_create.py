# quick_create.py
from database import Base, engine
from models import (User, TeacherProfile, Module, AssessmentQuestion,
                    AssessmentResponse, TeacherSubmission, Performance, GrowthPlan, PerformanceHistory)

Base.metadata.create_all(bind=engine)
print("Tables ready")