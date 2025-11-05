"""
Database Migration - Add new columns to growth_plans table
"""
from database import engine
from sqlalchemy import text

def migrate():
    """Add new columns to growth_plans table"""

    migrations = [
        # Add generated_context column
        "ALTER TABLE growth_plans ADD COLUMN IF NOT EXISTS generated_context TEXT;",

        # Add plan_version column
        "ALTER TABLE growth_plans ADD COLUMN IF NOT EXISTS plan_version INTEGER DEFAULT 1;",

        # Add is_active column with index
        "ALTER TABLE growth_plans ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;",
        "CREATE INDEX IF NOT EXISTS idx_growth_plans_teacher_active ON growth_plans(teacher_id, is_active);",

        # Add expires_at column with index
        "ALTER TABLE growth_plans ADD COLUMN IF NOT EXISTS expires_at TIMESTAMP;",
        "CREATE INDEX IF NOT EXISTS idx_growth_plans_expires ON growth_plans(expires_at);",
    ]

    print("🔧 Running Growth Plans Table Migrations")
    print("=" * 70)

    with engine.connect() as conn:
        for i, sql in enumerate(migrations, 1):
            try:
                print(f"\n{i}. Executing: {sql[:60]}...")
                conn.execute(text(sql))
                conn.commit()
                print(f"   ✅ Success")
            except Exception as e:
                if "already exists" in str(e) or "duplicate" in str(e).lower():
                    print(f"   ⏭️  Already exists (skipped)")
                else:
                    print(f"   ⚠️  Error: {str(e)[:100]}")

    print("\n" + "=" * 70)
    print("✅ Migration Complete!")
    print("=" * 70)

    # Verify columns exist
    print("\n🔍 Verifying columns...")
    verify_sql = """
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = 'growth_plans'
        ORDER BY ordinal_position;
    """

    with engine.connect() as conn:
        result = conn.execute(text(verify_sql))
        columns = result.fetchall()

        print("\nColumns in growth_plans table:")
        for col in columns:
            print(f"   • {col[0]:<25} {col[1]:<20} (nullable: {col[2]})")

    print("\n✅ All columns verified!")

if __name__ == "__main__":
    migrate()
