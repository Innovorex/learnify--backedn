"""
Seed Growth Plan Insights
Creates sample peer insights for the community learning feature
"""
from database import SessionLocal
from models import GrowthPlanInsight
from datetime import datetime

def seed_insights():
    db = SessionLocal()

    insights_data = [
        {
            "strategy_type": "cpd_improvement",
            "challenge": "Low score in Pedagogical Skills & Classroom Practice (42%)",
            "solution": "I watched 3 DIKSHA videos daily during my commute, practiced the techniques in my classroom with Grade 7 students, and reflected on what worked using the AI Tutor to discuss challenges. I focused on active learning strategies and formative assessment.",
            "outcome": "Score improved from 42% to 81% in 6 weeks. Student engagement increased dramatically, and my principal noticed the improvement.",
            "context_tags": '["grade_6-8", "mathematics", "cbse", "pedagogical_skills"]',
            "helpful_count": 124,
            "view_count": 450,
            "is_verified": True,
            "is_featured": True,
            "contributed_by": "Grade 7 Math Teacher, 8 years experience"
        },
        {
            "strategy_type": "cpd_improvement",
            "challenge": "Struggled with Assessment & Feedback module (48% score)",
            "solution": "Used AI Tutor to understand Bloom's Taxonomy deeply, then created 5 practice assessments using different question types. The platform feedback helped me improve question quality. I also enrolled in NCERT's assessment design course.",
            "outcome": "Assessment & Feedback score: 48% → 76% in 4 weeks. Now my questions test higher-order thinking effectively.",
            "context_tags": '["grade_9-10", "science", "state_board", "assessment"]',
            "helpful_count": 89,
            "view_count": 320,
            "is_verified": True,
            "is_featured": False,
            "contributed_by": "Grade 9 Science Teacher, 12 years experience"
        },
        {
            "strategy_type": "career_completion",
            "challenge": "Struggling to complete B.Ed modules while teaching full-time",
            "solution": "Created a strict schedule: 1 hour every morning before school (5:30-6:30 AM) for B.Ed study. Used weekends for practice exams. Joined a WhatsApp study group with 5 other teachers for motivation and doubt-clearing.",
            "outcome": "Completed all 8 B.Ed modules in 10 months. Passed final exams with 78% average. The morning routine became a habit.",
            "context_tags": '["b.ed", "career_progression", "time_management"]',
            "helpful_count": 156,
            "view_count": 580,
            "is_verified": True,
            "is_featured": True,
            "contributed_by": "Primary School Teacher, 6 years experience"
        },
        {
            "strategy_type": "ai_tutor_usage",
            "challenge": "Difficulty explaining complex algebraic concepts to Grade 8 students",
            "solution": "Used AI Tutor to explore 10 different ways to explain quadratic equations. Practiced explaining each approach, got feedback, and refined my teaching strategy. Created visual aids based on AI Tutor suggestions.",
            "outcome": "Student test scores on algebra improved by 25%. Students say math is now 'easier to understand'. Gained confidence in teaching difficult concepts.",
            "context_tags": '["grade_8", "mathematics", "algebra", "ai_tutor"]',
            "helpful_count": 67,
            "view_count": 210,
            "is_verified": True,
            "is_featured": False,
            "contributed_by": "Grade 8 Math Teacher, 5 years experience"
        },
        {
            "strategy_type": "material_creation",
            "challenge": "No organized teaching materials, preparing lessons took 2+ hours daily",
            "solution": "Spent one weekend creating a template library for common lesson types. Started uploading 1 completed lesson plan per week to the platform. Reused and modified templates for new topics. Built a personal material bank over 3 months.",
            "outcome": "Lesson prep time reduced to 30-45 minutes. Have 50+ quality materials uploaded. Other teachers use my materials too, which motivates me to create more.",
            "context_tags": '["material_creation", "time_management", "efficiency"]',
            "helpful_count": 103,
            "view_count": 390,
            "is_verified": True,
            "is_featured": False,
            "contributed_by": "Grade 6-7 English Teacher, 7 years experience"
        },
        {
            "strategy_type": "cpd_improvement",
            "challenge": "Technology & Innovation module score stuck at 55% despite multiple attempts",
            "solution": "Realized I was focusing on theory without practice. Started using 1 new EdTech tool every week in my classroom (Google Classroom, Kahoot, Padlet, etc.). Documented what worked and what didn't. Retook assessments after practical experience.",
            "outcome": "Score jumped to 85% after practical implementation. Now comfortably integrate technology in daily teaching. Students love interactive lessons.",
            "context_tags": '["technology", "innovation", "edtech", "practical_learning"]',
            "helpful_count": 92,
            "view_count": 340,
            "is_verified": True,
            "is_featured": True,
            "contributed_by": "Grade 10 Social Studies Teacher, 10 years experience"
        }
    ]

    try:
        # Check if insights already exist
        existing_count = db.query(GrowthPlanInsight).count()
        if existing_count > 0:
            print(f"⚠️  Database already has {existing_count} insights. Skipping seed.")
            return

        # Insert insights
        for data in insights_data:
            insight = GrowthPlanInsight(**data)
            db.add(insight)

        db.commit()
        print(f"✅ Successfully seeded {len(insights_data)} growth plan insights!")

        # Verify
        total = db.query(GrowthPlanInsight).count()
        verified = db.query(GrowthPlanInsight).filter_by(is_verified=True).count()
        featured = db.query(GrowthPlanInsight).filter_by(is_featured=True).count()

        print(f"\n📊 Insights Summary:")
        print(f"   Total: {total}")
        print(f"   Verified: {verified}")
        print(f"   Featured: {featured}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding insights: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_insights()
