#!/usr/bin/env python3
"""
Database Migration Runner
Applies the K-12 student support migration to the database
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in environment variables")
    print("Please set DATABASE_URL in .env file")
    sys.exit(1)

def run_migration():
    """Run the migration SQL script"""
    print("🔄 Starting database migration...")
    print(f"📊 Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'local'}")

    try:
        # Connect to database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Read migration SQL
        migration_file = Path(__file__).parent / "add_student_k12_support.sql"
        print(f"📄 Reading migration file: {migration_file.name}")

        with open(migration_file, 'r') as f:
            sql = f.read()

        # Execute migration
        print("⚙️  Executing migration...")
        cursor.execute(sql)
        conn.commit()

        # Verify tables were created
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name IN ('k12_assessments', 'k12_questions', 'k12_results')
            ORDER BY table_name;
        """)

        created_tables = cursor.fetchall()
        print("\n✅ Migration completed successfully!")
        print("\n📊 Created tables:")
        for table in created_tables:
            print(f"   ✓ {table[0]}")

        # Check if student fields were added
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'users'
            AND column_name IN ('class_name', 'section');
        """)

        added_columns = cursor.fetchall()
        if added_columns:
            print("\n👥 Updated users table:")
            for col in added_columns:
                print(f"   ✓ Added column: {col[0]}")

        cursor.close()
        conn.close()

        print("\n🎉 Migration successful! Backend is ready for K-12 student assessments.")

    except psycopg2.Error as e:
        print(f"\n❌ Migration failed: {e}")
        print("\nPlease check:")
        print("1. Database connection string is correct")
        print("2. Database server is running")
        print("3. You have proper permissions")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ Migration file not found: {migration_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 70)
    print(" K-12 Student Support Migration")
    print("=" * 70)
    print()
    run_migration()
