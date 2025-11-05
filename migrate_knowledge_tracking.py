"""
Migration script to add Knowledge Assessment Tracking tables and update modules table
"""
from sqlalchemy import create_engine, text
from database import DATABASE_URL, Base, engine
import models  # Import main models first
from models_knowledge_tracking import (
    TeacherAssessmentAttempt,
    TeacherAttemptLimit,
    TeacherAssessmentSummary,
    AssessmentSession
)
import sys

def migrate_knowledge_tracking():
    """Create all knowledge tracking tables and update modules"""

    try:
        print("🚀 Starting Knowledge Assessment Tracking Migration")
        print("=" * 70)

        # Step 1: Add new columns to modules table
        print("\n📝 Step 1: Adding timer fields to modules table...")
        with engine.connect() as conn:
            try:
                # Add time_limit_minutes
                conn.execute(text("""
                    ALTER TABLE modules
                    ADD COLUMN IF NOT EXISTS time_limit_minutes INTEGER DEFAULT 30
                """))
                print("  ✅ Added time_limit_minutes column")

                # Add cooldown_hours
                conn.execute(text("""
                    ALTER TABLE modules
                    ADD COLUMN IF NOT EXISTS cooldown_hours INTEGER DEFAULT 24
                """))
                print("  ✅ Added cooldown_hours column")

                # Add max_attempts_per_month
                conn.execute(text("""
                    ALTER TABLE modules
                    ADD COLUMN IF NOT EXISTS max_attempts_per_month INTEGER DEFAULT 3
                """))
                print("  ✅ Added max_attempts_per_month column")

                conn.commit()
            except Exception as e:
                if "already exists" in str(e) or "Duplicate column" in str(e):
                    print("  ℹ️  Columns already exist, skipping...")
                else:
                    raise e

        # Step 2: Create new tracking tables
        print("\n📝 Step 2: Creating knowledge tracking tables...")
        Base.metadata.create_all(bind=engine, tables=[
            TeacherAssessmentAttempt.__table__,
            TeacherAttemptLimit.__table__,
            TeacherAssessmentSummary.__table__,
            AssessmentSession.__table__
        ])
        print("  ✅ Created teacher_assessment_attempts table")
        print("  ✅ Created teacher_attempt_limits table")
        print("  ✅ Created teacher_assessment_summary table")
        print("  ✅ Created assessment_sessions table")

        # Step 3: Verify tables
        print("\n📝 Step 3: Verifying tables...")
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name LIKE '%assessment%'
                ORDER BY table_name
            """))

            print("\n📊 Assessment-related Tables:")
            print("=" * 70)
            for row in result:
                print(f"  ✓ {row[0]}")

        print("\n" + "=" * 70)
        print("✅ Migration completed successfully!")
        print("\n🎯 Next Steps:")
        print("  1. Restart backend server")
        print("  2. Test attempt tracking endpoints")
        print("  3. Verify timer and cooldown functionality")

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    migrate_knowledge_tracking()
