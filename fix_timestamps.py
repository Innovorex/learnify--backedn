"""Fix assessment_sessions timestamps to use TIMESTAMPTZ"""
from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    # Convert to TIMESTAMPTZ (timestamp with time zone)
    print("Converting started_at to TIMESTAMPTZ...")
    conn.execute(text("ALTER TABLE assessment_sessions ALTER COLUMN started_at TYPE TIMESTAMPTZ USING started_at AT TIME ZONE 'UTC'"))

    print("Converting expires_at to TIMESTAMPTZ...")
    conn.execute(text("ALTER TABLE assessment_sessions ALTER COLUMN expires_at TYPE TIMESTAMPTZ USING expires_at AT TIME ZONE 'UTC'"))

    print("Converting submitted_at to TIMESTAMPTZ...")
    conn.execute(text("ALTER TABLE assessment_sessions ALTER COLUMN submitted_at TYPE TIMESTAMPTZ USING submitted_at AT TIME ZONE 'UTC'"))

    conn.commit()
    print("✓ Timestamps fixed!")
