#!/usr/bin/env python3
"""
CBSE Syllabus Database Populator
Loads JSON syllabus files and populates PostgreSQL database
"""

import json
import os
import sys
from datetime import datetime
import psycopg2
from psycopg2.extras import Json

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "te",
    "user": "innovorex",
    "password": "Innovorex@1"
}

class SyllabusPopulator:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.outputs_dir = "/home/learnify/lt/learnify-teach/backend/scripts/cbse_syllabus/outputs"

    def connect_db(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            print("✅ Database connected successfully")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            sys.exit(1)

    def close_db(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("✅ Database connection closed")

    def clean_old_entries(self):
        """Remove old placeholder entries"""
        try:
            # Delete entries with grade ranges or placeholder content
            self.cursor.execute("""
                DELETE FROM syllabus_cache
                WHERE board = 'CBSE'
                AND (
                    grade LIKE '%-%'
                    OR syllabus_data LIKE '%Basic concepts%'
                    OR syllabus_data LIKE '%Advanced topics%'
                );
            """)
            deleted_count = self.cursor.rowcount
            self.conn.commit()
            print(f"✅ Cleaned {deleted_count} old/placeholder entries")
        except Exception as e:
            print(f"⚠️  Warning during cleanup: {e}")
            self.conn.rollback()

    def insert_syllabus(self, syllabus_data):
        """Insert or update syllabus in database"""
        grade = syllabus_data.get("grade")
        subject = syllabus_data.get("subject")
        board = syllabus_data.get("board", "CBSE")
        state = "National"  # CBSE is national board

        try:
            # Check if entry exists
            self.cursor.execute("""
                SELECT id FROM syllabus_cache
                WHERE board = %s AND grade = %s AND subject = %s
            """, (board, grade, subject))

            existing = self.cursor.fetchone()

            # Convert to JSON string
            syllabus_json = json.dumps(syllabus_data, ensure_ascii=False)

            if existing:
                # Update existing entry
                self.cursor.execute("""
                    UPDATE syllabus_cache
                    SET syllabus_data = %s,
                        updated_at = %s,
                        state = %s
                    WHERE board = %s AND grade = %s AND subject = %s
                """, (syllabus_json, datetime.now(), state, board, grade, subject))
                print(f"   ✏️  Updated: Grade {grade} - {subject}")
            else:
                # Insert new entry
                self.cursor.execute("""
                    INSERT INTO syllabus_cache
                    (state, board, grade, subject, syllabus_data, fetched_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (state, board, grade, subject, syllabus_json, datetime.now(), datetime.now()))
                print(f"   ➕ Inserted: Grade {grade} - {subject}")

            self.conn.commit()
            return True

        except Exception as e:
            print(f"   ❌ Error inserting Grade {grade} - {subject}: {e}")
            self.conn.rollback()
            return False

    def load_and_populate(self, filename):
        """Load JSON file and populate database"""
        filepath = os.path.join(self.outputs_dir, filename)

        if not os.path.exists(filepath):
            print(f"⚠️  File not found: {filepath}")
            return False

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                syllabus_data = json.load(f)

            return self.insert_syllabus(syllabus_data)

        except Exception as e:
            print(f"❌ Error loading {filename}: {e}")
            return False

    def verify_data(self):
        """Verify inserted data"""
        try:
            self.cursor.execute("""
                SELECT grade, subject,
                       LENGTH(syllabus_data) as data_size,
                       updated_at
                FROM syllabus_cache
                WHERE board = 'CBSE'
                ORDER BY
                    CASE
                        WHEN grade ~ '^[0-9]+$' THEN CAST(grade AS INTEGER)
                        ELSE 999
                    END,
                    subject;
            """)

            rows = self.cursor.fetchall()

            print(f"\n{'='*80}")
            print("DATABASE VERIFICATION")
            print(f"{'='*80}")
            print(f"Total CBSE Entries: {len(rows)}\n")

            for row in rows:
                grade, subject, size, updated = row
                print(f"✅ Grade {grade:<3} | {subject:<25} | {size:>6} chars | {updated}")

            return len(rows)

        except Exception as e:
            print(f"❌ Verification error: {e}")
            return 0

def main():
    print("=" * 80)
    print("CBSE SYLLABUS DATABASE POPULATOR")
    print("=" * 80)

    populator = SyllabusPopulator()

    # Connect to database
    print("\n1️⃣  Connecting to database...")
    populator.connect_db()

    # Clean old entries
    print("\n2️⃣  Cleaning old placeholder entries...")
    populator.clean_old_entries()

    # Populate Grade 10 data
    print("\n3️⃣  Populating Grade 10 syllabus...")

    files_to_load = [
        "cbse_grade_10_mathematics.json",
        "cbse_grade_10_science.json"
    ]

    success_count = 0
    for filename in files_to_load:
        if populator.load_and_populate(filename):
            success_count += 1

    print(f"\n   Loaded: {success_count}/{len(files_to_load)} files")

    # Verify data
    print("\n4️⃣  Verifying database...")
    total_entries = populator.verify_data()

    # Close connection
    print(f"\n5️⃣  Closing database connection...")
    populator.close_db()

    print(f"\n{'='*80}")
    print(f"✅ POPULATION COMPLETE!")
    print(f"   Total CBSE entries in database: {total_entries}")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
