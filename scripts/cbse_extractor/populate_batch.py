#!/usr/bin/env python3
"""
Batch Database Populator
Populates syllabus_cache table from structured JSON files
"""

import psycopg2
import json
from pathlib import Path
from datetime import datetime
import sys

class BatchPopulator:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost", port=5432, database="te",
            user="innovorex", password="Innovorex@1"
        )
        self.cursor = self.conn.cursor()

        self.stats = {
            "total_files": 0,
            "successful": 0,
            "failed": 0,
            "skipped": 0,
            "updated": 0,
            "inserted": 0
        }

    def populate_from_directory(self, json_dir, dry_run=True):
        """Populate database from all JSON files in directory"""

        json_dir = Path(json_dir)
        json_files = sorted(json_dir.glob("cbse_grade_*.json"))
        self.stats["total_files"] = len(json_files)

        print(f"{'='*80}")
        print(f"BATCH POPULATION {'(DRY RUN)' if dry_run else '(LIVE)'}")
        print(f"{'='*80}")
        print(f"Found {len(json_files)} JSON files\n")

        for json_file in json_files:
            print(f"📄 {json_file.name}")

            try:
                with open(json_file, encoding='utf-8') as f:
                    data = json.load(f)

                # Validate
                self._validate_data(data)

                if not dry_run:
                    action = self._insert_or_update(data)
                    if action == "updated":
                        self.stats["updated"] += 1
                    else:
                        self.stats["inserted"] += 1
                    self.conn.commit()
                else:
                    print(f"  ✅ Valid (would {'update' if self._exists(data) else 'insert'})")

                self.stats["successful"] += 1

            except Exception as e:
                print(f"  ❌ Failed: {e}")
                self.stats["failed"] += 1
                if not dry_run:
                    self.conn.rollback()

            print()

        self._print_summary()

        if not dry_run:
            self.conn.commit()

        self.conn.close()

    def _validate_data(self, data):
        """Validate data structure"""
        required = ["board", "grade", "subject", "units"]
        for field in required:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        if not isinstance(data["units"], list):
            raise ValueError("'units' must be a list")

        if len(data["units"]) == 0:
            raise ValueError("No units found")

    def _exists(self, data):
        """Check if entry exists"""
        self.cursor.execute("""
            SELECT id FROM syllabus_cache
            WHERE board = %s AND grade = %s AND subject = %s
        """, (data["board"], str(data["grade"]), data["subject"]))

        return self.cursor.fetchone() is not None

    def _insert_or_update(self, data):
        """Insert or update syllabus entry"""

        # Check if exists
        self.cursor.execute("""
            SELECT id FROM syllabus_cache
            WHERE board = %s AND grade = %s AND subject = %s
        """, (data["board"], str(data["grade"]), data["subject"]))

        existing = self.cursor.fetchone()

        # Convert to JSON string
        syllabus_json = json.dumps(data, ensure_ascii=False)

        if existing:
            # Update
            self.cursor.execute("""
                UPDATE syllabus_cache
                SET syllabus_data = %s,
                    updated_at = %s,
                    state = %s
                WHERE board = %s AND grade = %s AND subject = %s
            """, (
                syllabus_json,
                datetime.now(),
                "National",
                data["board"],
                str(data["grade"]),
                data["subject"]
            ))
            print(f"  ✏️  Updated existing entry")
            return "updated"
        else:
            # Insert
            self.cursor.execute("""
                INSERT INTO syllabus_cache
                (state, board, grade, subject, syllabus_data, fetched_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                "National",
                data["board"],
                str(data["grade"]),
                data["subject"],
                syllabus_json,
                datetime.now(),
                datetime.now()
            ))
            print(f"  ➕ Inserted new entry")
            return "inserted"

    def _print_summary(self):
        """Print batch summary"""
        print(f"{'='*80}")
        print("BATCH SUMMARY")
        print(f"{'='*80}")
        print(f"Total Files:      {self.stats['total_files']}")
        print(f"✅ Successful:    {self.stats['successful']}")
        print(f"   - Inserted:    {self.stats['inserted']}")
        print(f"   - Updated:     {self.stats['updated']}")
        print(f"❌ Failed:        {self.stats['failed']}")
        print(f"⚠️  Skipped:       {self.stats['skipped']}")
        print(f"{'='*80}")

def main():
    """Main execution"""

    dry_run = "--live" not in sys.argv
    json_dir = "scripts/cbse_extractor/data/structured_json"

    populator = BatchPopulator()
    populator.populate_from_directory(json_dir, dry_run=dry_run)

if __name__ == "__main__":
    main()
