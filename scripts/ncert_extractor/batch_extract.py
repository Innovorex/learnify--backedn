#!/usr/bin/env python3
"""
Batch extract all chapters for a given grade and subject
"""

import sys
import subprocess
from pathlib import Path

def batch_extract(grade, subject, chapter_start, chapter_end, file_pattern):
    """Extract multiple chapters in batch"""

    total = chapter_end - chapter_start + 1
    success = 0
    failed = 0

    print(f"\n{'='*80}")
    print(f"Batch Extraction: Grade {grade} {subject}")
    print(f"Chapters: {chapter_start} to {chapter_end} ({total} chapters)")
    print(f"{'='*80}\n")

    for i in range(chapter_start, chapter_end + 1):
        chapter_num = f"{i:02d}"
        pdf_file = file_pattern.format(chapter=chapter_num)

        pdf_path = Path(pdf_file)
        if not pdf_path.exists() or pdf_path.stat().st_size == 0:
            print(f"❌ Chapter {i}: File not found or empty")
            failed += 1
            continue

        print(f"[{i-chapter_start+1}/{total}] Processing Chapter {i}...")

        try:
            result = subprocess.run([
                'python3', 'extract_chapter.py',
                pdf_file, str(grade), subject, str(i)
            ], capture_output=True, text=True, timeout=120)

            if result.returncode == 0:
                # Parse output for stats
                output = result.stdout
                if 'examples' in output and 'exercises' in output:
                    for line in output.split('\n'):
                        if 'Found' in line and 'examples' in line:
                            print(f"   ✅ {line.strip()}")
                        if 'Found' in line and 'exercises' in line:
                            print(f"   ✅ {line.strip()}")
                success += 1
            else:
                print(f"   ❌ Extraction failed: {result.stderr[:100]}")
                failed += 1

        except subprocess.TimeoutExpired:
            print(f"   ❌ Timeout")
            failed += 1
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}")
            failed += 1

    print(f"\n{'='*80}")
    print(f"Batch Extraction Complete!")
    print(f"   Success: {success}/{total}")
    print(f"   Failed: {failed}/{total}")
    print(f"{'='*80}\n")

    return success, failed

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("\nUsage: python3 batch_extract.py <grade> <subject> <start_ch> <end_ch> <file_pattern>")
        print("\nExample:")
        print("  python3 batch_extract.py 10 Mathematics 5 14 '../ncert_pdfs/grade_10_math_ch{chapter}.pdf'\n")
        sys.exit(1)

    grade = int(sys.argv[1])
    subject = sys.argv[2]
    start_ch = int(sys.argv[3])
    end_ch = int(sys.argv[4])
    pattern = sys.argv[5]

    batch_extract(grade, subject, start_ch, end_ch, pattern)
