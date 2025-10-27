"""
AUTOMATIC RESET AND SEED WITH REAL IGNOU DATA
No confirmation required - runs automatically
"""

from sqlalchemy import text
from database import SessionLocal, engine
from models import Base

def reset_career_progression_tables():
    """Drop and recreate career progression tables"""
    db = SessionLocal()

    print("🗑️  Dropping career progression tables...")

    # Drop tables in correct order (respecting foreign keys)
    tables_to_drop = [
        "course_certificates",
        "module_exam_responses",
        "module_exam_questions",
        "topic_progress",
        "module_progress",
        "teacher_career_enrollments",
        "module_topics",
        "course_modules",
        "career_courses"
    ]

    for table in tables_to_drop:
        try:
            db.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
            print(f"  ✅ Dropped {table}")
        except Exception as e:
            print(f"  ⚠️  {table}: {e}")

    db.commit()
    db.close()

    print("\n🔨 Recreating tables with fresh schema...")

    # Recreate only career progression tables
    from models import (
        CareerCourse, CourseModule, ModuleTopic,
        TeacherCareerEnrollment, ModuleProgress, TopicProgress,
        ModuleExamQuestion, ModuleExamResponse, CourseCertificate
    )

    Base.metadata.create_all(bind=engine, tables=[
        CareerCourse.__table__,
        CourseModule.__table__,
        ModuleTopic.__table__,
        TeacherCareerEnrollment.__table__,
        ModuleProgress.__table__,
        TopicProgress.__table__,
        ModuleExamQuestion.__table__,
        ModuleExamResponse.__table__,
        CourseCertificate.__table__
    ])

    print("  ✅ All tables recreated successfully\n")

def main():
    """Main reset and seed process"""

    print("\n" + "="*70)
    print("🔄 FRESH START: Automatic Reset & Seed Real IGNOU B.Ed Data")
    print("="*70)
    print()
    print("⚠️  This will DELETE ALL career progression data")
    print("✅ Then load REAL IGNOU B.Ed content")
    print()

    # Step 1: Reset tables
    print("="*70)
    print("STEP 1: Resetting Database")
    print("="*70 + "\n")
    reset_career_progression_tables()

    # Step 2: Seed real IGNOU data
    print("="*70)
    print("STEP 2: Seeding Real IGNOU B.Ed Data")
    print("="*70 + "\n")

    # Import and run the real seed script
    from seed_real_ignou_bed import seed_real_ignou_bed
    seed_real_ignou_bed()

    print("\n" + "="*70)
    print("✅ FRESH START COMPLETE!")
    print("="*70)
    print()
    print("📊 What Changed:")
    print("  ✅ Database reset successful")
    print("  ✅ Real IGNOU B.Ed data loaded")
    print("  ✅ 8 modules with authentic content from IGNOU")
    print("  ✅ 21+ topics from official BES courses")
    print("  ❌ All previous enrollments cleared")
    print()
    print("🔄 Next Steps:")
    print("  1. Refresh your browser (Ctrl + Shift + R)")
    print("  2. Teachers need to re-enroll in the course")
    print("  3. Course now has REAL IGNOU syllabus structure")
    print()

if __name__ == "__main__":
    main()
