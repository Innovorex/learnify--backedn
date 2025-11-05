"""
Migration script to add category field to modules table
and categorize existing modules based on assessment_type
"""
from sqlalchemy import create_engine, text
from database import DATABASE_URL
import sys

def migrate_add_category():
    engine = create_engine(DATABASE_URL)

    try:
        with engine.connect() as conn:
            # Step 1: Add category column if it doesn't exist
            print("📝 Step 1: Adding category column to modules table...")
            try:
                conn.execute(text("""
                    ALTER TABLE modules
                    ADD COLUMN category VARCHAR(20) NOT NULL DEFAULT 'knowledge'
                """))
                conn.commit()
                print("✅ Category column added successfully")
            except Exception as e:
                if "already exists" in str(e) or "Duplicate column" in str(e):
                    print("ℹ️  Category column already exists, skipping...")
                else:
                    raise e

            # Step 2: Update existing modules based on assessment_type
            print("\n📝 Step 2: Categorizing existing modules...")

            # MCQ -> knowledge
            result = conn.execute(text("""
                UPDATE modules
                SET category = 'knowledge'
                WHERE assessment_type = 'mcq'
            """))
            conn.commit()
            print(f"✅ Updated {result.rowcount} MCQ modules → category: 'knowledge'")

            # Submission -> portfolio
            result = conn.execute(text("""
                UPDATE modules
                SET category = 'portfolio'
                WHERE assessment_type = 'submission'
            """))
            conn.commit()
            print(f"✅ Updated {result.rowcount} submission modules → category: 'portfolio'")

            # Outcome -> outcomes
            result = conn.execute(text("""
                UPDATE modules
                SET category = 'outcomes'
                WHERE assessment_type = 'outcome'
            """))
            conn.commit()
            print(f"✅ Updated {result.rowcount} outcome modules → category: 'outcomes'")

            # Step 3: Verify migration
            print("\n📝 Step 3: Verifying migration...")
            result = conn.execute(text("""
                SELECT category, assessment_type, COUNT(*) as count
                FROM modules
                GROUP BY category, assessment_type
                ORDER BY category, assessment_type
            """))

            print("\n📊 Module Distribution:")
            print("=" * 60)
            for row in result:
                print(f"  Category: {row[0]:12} | Type: {row[1]:12} | Count: {row[2]}")
            print("=" * 60)

            print("\n✅ Migration completed successfully!")

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        sys.exit(1)
    finally:
        engine.dispose()

if __name__ == "__main__":
    print("🚀 Starting migration: Add category field to modules")
    print("=" * 60)
    migrate_add_category()
