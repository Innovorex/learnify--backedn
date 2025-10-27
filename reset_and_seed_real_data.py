"""
COMPLETE RESET AND FRESH START WITH REAL IGNOU DATA

WARNING: This will delete ALL career progression data including:
- All courses
- All modules and topics
- All enrollments and progress
- All certificates

This gives you a clean slate with authentic IGNOU B.Ed content.
"""

import sys
from sqlalchemy import text
from database import SessionLocal, engine
from models import Base

def confirm_reset():
    """Ask for confirmation before proceeding"""
    print("="*70)
    print("⚠️  WARNING: COMPLETE DATABASE RESET ⚠️")
    print("="*70)
    print()
    print("This will DELETE ALL career progression data:")
    print("  ❌ All courses")
    print("  ❌ All modules and topics")
    print("  ❌ All teacher enrollments")
    print("  ❌ All progress tracking")
    print("  ❌ All certificates")
    print()
    print("After reset, you will have:")
    print("  ✅ Fresh database with REAL IGNOU B.Ed content")
    print("  ✅ Authentic syllabus structure")
    print("  ✅ Clean slate for new enrollments")
    print()

    response = input("Type 'YES' to proceed with reset: ")
    return response.strip().upper() == "YES"

def reset_career_progression_tables():
    """Drop and recreate career progression tables"""
    db = SessionLocal()

    print("\n🗑️  Dropping career progression tables...")

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

    print("  ✅ All tables recreated successfully")

def main():
    """Main reset and seed process"""

    print("\n" + "="*70)
    print("🔄 FRESH START: Reset & Seed Real IGNOU B.Ed Data")
    print("="*70 + "\n")

    # Step 1: Confirm
    if not confirm_reset():
        print("\n❌ Reset cancelled by user")
        sys.exit(0)

    # Step 2: Reset tables
    print("\n" + "="*70)
    print("STEP 1: Resetting Database")
    print("="*70)
    reset_career_progression_tables()

    # Step 3: Seed real IGNOU data
    print("\n" + "="*70)
    print("STEP 2: Seeding Real IGNOU B.Ed Data")
    print("="*70 + "\n")

    # Import and run the real seed script
    from seed_real_ignou_bed import seed_real_ignou_bed
    seed_real_ignou_bed()

    print("\n" + "="*70)
    print("✅ FRESH START COMPLETE!")
    print("="*70)
    print()
    print("📊 Summary:")
    print("  ✅ Database reset successful")
    print("  ✅ Real IGNOU B.Ed data loaded")
    print("  ✅ 8 modules with authentic content")
    print("  ✅ 21+ topics from official IGNOU syllabus")
    print()
    print("🔄 Next Steps:")
    print("  1. Restart your backend server")
    print("  2. Refresh your browser")
    print("  3. Teachers can now enroll in the updated course")
    print("  4. Previous enrollments have been cleared")
    print()

if __name__ == "__main__":
    main()
