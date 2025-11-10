#!/usr/bin/env python3
"""
COMPREHENSIVE CHAPTER NAME REPAIR
Fixes all "Unknown Chapter" names using official NCERT mappings
"""

import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

from database import SessionLocal
from models import NCERTTextbookContent, NCERTExample, NCERTExercise
from sqlalchemy import or_
from comprehensive_chapter_names import NCERT_CHAPTER_NAMES, count_mappings

def normalize_subject_name(subject):
    """Normalize subject names to match our mappings"""
    # Handle variations in subject names
    subject_mappings = {
        'math': 'Mathematics',
        'science': 'Science',
        'Social Science': 'Social_Science',
        'Social_Science': 'Social_Science',
        'Social_Science_Complete': 'Social_Science',
        'English': 'English_First_Flight',
        'English_FirstFlight': 'English_First_Flight',
        'English_First_Flight': 'English_First_Flight',
        'English_Footprints': 'English_Footprints',
        'English_Beehive': 'English_Beehive',
        'English_Moments': 'English_Moments',
        'English_Marigold': 'English_Marigold',
        'English_Honeysuckle': 'English_Honeysuckle',
        'English_Honeycomb': 'English_Honeycomb',
        'English_Honeydew': 'English_Honeydew',
        'English_AlienHand': 'English_Alien_Hand',
        'Hindi': 'Hindi_Kshitij',
        'Hindi_Kshitij': 'Hindi_Kshitij',
        'Hindi_Kritika': 'Hindi_Kritika',
        'Hindi_Sparsh': 'Hindi_Sparsh',
        'Hindi_Sparsh_Complete': 'Hindi_Sparsh',
        'Hindi_Sparsh_Additional': 'Hindi_Sparsh',
        'Hindi_Vasant': 'Hindi_Vasant',
        'Hindi_Vasant_Complete': 'Hindi_Vasant',
    }

    return subject_mappings.get(subject, subject)


def repair_chapter_names():
    """Repair all corrupted chapter names"""
    db = SessionLocal()

    print("="*80)
    print("🔧 COMPREHENSIVE CHAPTER NAME REPAIR")
    print("="*80)
    print(f"Available mappings: {count_mappings()} chapters")
    print()

    # Find all entries with Unknown or corrupted chapter names
    corrupted = db.query(NCERTTextbookContent).filter(
        or_(
            NCERTTextbookContent.chapter_name.like('%Unknown%'),
            NCERTTextbookContent.chapter_name.like('%rrr%'),
            NCERTTextbookContent.chapter_name.like('%eee%'),
            NCERTTextbookContent.chapter_name.like('%ttt%'),
            NCERTTextbookContent.chapter_name.like('%sss%'),
            NCERTTextbookContent.chapter_name == None
        )
    ).all()

    print(f"Found {len(corrupted)} entries with corrupted chapter names")
    print()

    fixed_count = 0
    not_found_count = 0
    not_found_list = []

    for entry in corrupted:
        # Normalize subject name
        normalized_subject = normalize_subject_name(entry.subject)

        # Try to find official chapter name
        key = (entry.grade, normalized_subject, entry.chapter_number)

        if key in NCERT_CHAPTER_NAMES:
            official_name = NCERT_CHAPTER_NAMES[key]
            old_name = entry.chapter_name

            # Update chapter name
            entry.chapter_name = official_name
            fixed_count += 1

            print(f"✅ Grade {entry.grade} {entry.subject} Ch.{entry.chapter_number}")
            print(f"   Old: {old_name}")
            print(f"   New: {official_name}")
            print()
        else:
            not_found_count += 1
            not_found_list.append((entry.grade, entry.subject, entry.chapter_number))

    # Commit changes
    db.commit()

    print("="*80)
    print("📊 REPAIR SUMMARY")
    print("="*80)
    print(f"Total corrupted entries: {len(corrupted)}")
    print(f"Successfully fixed: {fixed_count}")
    print(f"Not found in mappings: {not_found_count}")
    print()

    if not_found_list:
        print("\n⚠️  CHAPTER NAMES NOT FOUND IN MAPPINGS:")
        print("-"*80)

        # Group by grade and subject
        by_grade_subject = {}
        for grade, subject, ch_num in not_found_list:
            key = (grade, subject)
            if key not in by_grade_subject:
                by_grade_subject[key] = []
            by_grade_subject[key].append(ch_num)

        for (grade, subject), chapters in sorted(by_grade_subject.items()):
            print(f"Grade {grade} {subject}: {len(chapters)} chapters - {sorted(chapters)}")

    print()
    print("="*80)

    db.close()

    return fixed_count, not_found_count


if __name__ == "__main__":
    fixed, not_found = repair_chapter_names()

    print(f"\n✅ Repair complete!")
    print(f"   Fixed: {fixed} chapters")
    print(f"   Remaining: {not_found} chapters need manual mapping")
