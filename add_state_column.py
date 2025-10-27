"""
Add state column to teacher_profiles table
"""
import sys
import os
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from database import engine
from sqlalchemy import text

def add_state_column():
    """Add state column if it doesn't exist"""
    with engine.connect() as conn:
        try:
            # Check if column exists
            result = conn.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='teacher_profiles' AND column_name='state'
            """))

            if result.fetchone() is None:
                # Add column
                conn.execute(text("""
                    ALTER TABLE teacher_profiles
                    ADD COLUMN state VARCHAR(50) DEFAULT 'Telangana'
                """))
                conn.commit()
                print("[SUCCESS] Added 'state' column to teacher_profiles table")
            else:
                print("[INFO] 'state' column already exists")

        except Exception as e:
            print(f"[ERROR] {e}")

if __name__ == "__main__":
    add_state_column()
