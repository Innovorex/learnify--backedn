#!/usr/bin/env python3
"""
Repair Corrupted Chapter Names in Database
Fixes "Unknown Chapter", OCR artifacts, and assigns proper names
"""

import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

from database import SessionLocal
from models import NCERTTextbookContent
from sqlalchemy import or_
import re


# Official NCERT Chapter Names by Grade/Subject/Chapter
OFFICIAL_CHAPTER_NAMES = {
    # Grade 10 Mathematics
    (10, 'Mathematics', 1): 'Real Numbers',
    (10, 'Mathematics', 2): 'Polynomials',
    (10, 'Mathematics', 3): 'Pair of Linear Equations in Two Variables',
    (10, 'Mathematics', 4): 'Quadratic Equations',
    (10, 'Mathematics', 5): 'Arithmetic Progressions',
    (10, 'Mathematics', 6): 'Triangles',
    (10, 'Mathematics', 7): 'Coordinate Geometry',
    (10, 'Mathematics', 8): 'Introduction to Trigonometry',
    (10, 'Mathematics', 9): 'Some Applications of Trigonometry',
    (10, 'Mathematics', 10): 'Circles',
    (10, 'Mathematics', 11): 'Constructions',
    (10, 'Mathematics', 12): 'Areas Related to Circles',
    (10, 'Mathematics', 13): 'Surface Areas and Volumes',
    (10, 'Mathematics', 14): 'Statistics',
    (10, 'Mathematics', 15): 'Probability',

    # Grade 10 Science
    (10, 'Science', 1): 'Chemical Reactions and Equations',
    (10, 'Science', 2): 'Acids, Bases and Salts',
    (10, 'Science', 3): 'Metals and Non-metals',
    (10, 'Science', 4): 'Carbon and its Compounds',
    (10, 'Science', 5): 'Periodic Classification of Elements',
    (10, 'Science', 6): 'Life Processes',
    (10, 'Science', 7): 'Control and Coordination',
    (10, 'Science', 8): 'How do Organisms Reproduce?',
    (10, 'Science', 9): 'Heredity and Evolution',
    (10, 'Science', 10): 'Light - Reflection and Refraction',
    (10, 'Science', 11): 'Human Eye and Colourful World',
    (10, 'Science', 12): 'Electricity',
    (10, 'Science', 13): 'Magnetic Effects of Electric Current',

    # Grade 9 Science
    (9, 'science', 1): 'Matter in Our Surroundings',
    (9, 'science', 2): 'Is Matter Around Us Pure?',
    (9, 'science', 3): 'Atoms and Molecules',
    (9, 'science', 4): 'Structure of the Atom',
    (9, 'science', 5): 'The Fundamental Unit of Life',
    (9, 'science', 6): 'Tissues',
    (9, 'science', 7): 'Diversity in Living Organisms',
    (9, 'science', 8): 'Motion',
    (9, 'science', 9): 'Force and Laws of Motion',
    (9, 'science', 10): 'Gravitation',
    (9, 'science', 11): 'Work and Energy',
    (9, 'science', 12): 'Sound',
    (9, 'science', 13): 'Why Do We Fall Ill',
    (9, 'science', 14): 'Natural Resources',
    (9, 'science', 15): 'Improvement in Food Resources',

    # Grade 9 Mathematics
    (9, 'Mathematics', 1): 'Number Systems',
    (9, 'Mathematics', 2): 'Polynomials',
    (9, 'Mathematics', 3): 'Coordinate Geometry',
    (9, 'Mathematics', 4): 'Linear Equations in Two Variables',
    (9, 'Mathematics', 5): 'Introduction to Euclid\'s Geometry',
    (9, 'Mathematics', 6): 'Lines and Angles',
    (9, 'Mathematics', 7): 'Triangles',
    (9, 'Mathematics', 8): 'Quadrilaterals',
    (9, 'Mathematics', 9): 'Areas of Parallelograms and Triangles',
    (9, 'Mathematics', 10): 'Circles',
    (9, 'Mathematics', 11): 'Constructions',
    (9, 'Mathematics', 12): 'Heron\'s Formula',
    (9, 'Mathematics', 13): 'Surface Areas and Volumes',
    (9, 'Mathematics', 14): 'Statistics',
    (9, 'Mathematics', 15): 'Probability',

    # Grade 8 Math
    (8, 'math', 1): 'Rational Numbers',
    (8, 'math', 2): 'Linear Equations in One Variable',
    (8, 'math', 3): 'Understanding Quadrilaterals',
    (8, 'math', 4): 'Practical Geometry',
    (8, 'math', 5): 'Data Handling',
    (8, 'math', 6): 'Squares and Square Roots',
    (8, 'math', 7): 'Cubes and Cube Roots',
    (8, 'math', 8): 'Comparing Quantities',
    (8, 'math', 9): 'Algebraic Expressions and Identities',
    (8, 'math', 10): 'Visualising Solid Shapes',
    (8, 'math', 11): 'Mensuration',
    (8, 'math', 12): 'Exponents and Powers',
    (8, 'math', 13): 'Direct and Inverse Proportions',
    (8, 'math', 14): 'Factorisation',
    (8, 'math', 15): 'Introduction to Graphs',
    (8, 'math', 16): 'Playing with Numbers',

    # Grade 7 Mathematics
    (7, 'Mathematics', 1): 'Integers',
    (7, 'Mathematics', 2): 'Fractions and Decimals',
    (7, 'Mathematics', 3): 'Data Handling',
    (7, 'Mathematics', 4): 'Simple Equations',
    (7, 'Mathematics', 5): 'Lines and Angles',
    (7, 'Mathematics', 6): 'The Triangle and its Properties',
    (7, 'Mathematics', 7): 'Congruence of Triangles',
    (7, 'Mathematics', 8): 'Comparing Quantities',
    (7, 'Mathematics', 9): 'Rational Numbers',
    (7, 'Mathematics', 10): 'Practical Geometry',
    (7, 'Mathematics', 11): 'Perimeter and Area',
    (7, 'Mathematics', 12): 'Algebraic Expressions',
    (7, 'Mathematics', 13): 'Exponents and Powers',
    (7, 'Mathematics', 14): 'Symmetry',
    (7, 'Mathematics', 15): 'Visualising Solid Shapes',

    # Grade 9 Social Science
    (9, 'Social Science', 1): 'The French Revolution',
    (9, 'Social Science', 2): 'Socialism in Europe and the Russian Revolution',
    (9, 'Social Science', 3): 'Nazism and the Rise of Hitler',
    (9, 'Social Science', 4): 'Forest Society and Colonialism',
    (9, 'Social Science', 5): 'Pastoralists in the Modern World',
    (9, 'Social Science', 6): 'Climate',
    (9, 'Social Science', 7): 'Population',
    (9, 'Social Science', 8): 'Drainage',
    (9, 'Social Science', 9): 'India - Size and Location',
    (9, 'Social Science', 10): 'Physical Features of India',
}


def is_corrupted(chapter_name):
    """Check if chapter name is corrupted"""
    if not chapter_name:
        return True

    if chapter_name == "Unknown Chapter":
        return True

    # Check for OCR artifacts (repeated characters like "Rrrrr")
    if re.search(r'([A-Za-z])\1{3,}', chapter_name):
        return True

    # Check for excessive punctuation
    if re.search(r'[?!]{3,}', chapter_name):
        return True

    # Check for very short names (likely incomplete)
    if len(chapter_name) < 3:
        return True

    return False


def repair_chapter_names():
    """Repair all corrupted chapter names in database"""

    db = SessionLocal()

    print("=" * 100)
    print("🔧 CHAPTER NAME REPAIR TOOL")
    print("=" * 100)

    # Find all corrupted entries
    corrupted = db.query(NCERTTextbookContent).filter(
        or_(
            NCERTTextbookContent.chapter_name.like('%Unknown%'),
            NCERTTextbookContent.chapter_name.like('%rrr%'),
            NCERTTextbookContent.chapter_name.like('%eee%'),
            NCERTTextbookContent.chapter_name.like('%iii%'),
            NCERTTextbookContent.chapter_name.like('%ooo%'),
            NCERTTextbookContent.chapter_name.like('%???%'),
            NCERTTextbookContent.chapter_name.like('%Limate%'),
            NCERTTextbookContent.chapter_name.like('%Rainage%'),
            NCERTTextbookContent.chapter_name.like('%Opulation%')
        )
    ).all()

    print(f"\n📊 Found {len(corrupted)} corrupted entries\n")

    fixed_count = 0
    unable_to_fix = []

    for entry in corrupted:
        grade = entry.grade
        subject = entry.subject
        chapter_num = entry.chapter_number

        # Try to find official name
        key = (grade, subject, chapter_num)

        # Try variations (case differences)
        official_name = None
        for subj_variant in [subject, subject.lower(), subject.title(), subject.upper()]:
            test_key = (grade, subj_variant, chapter_num)
            if test_key in OFFICIAL_CHAPTER_NAMES:
                official_name = OFFICIAL_CHAPTER_NAMES[test_key]
                break

        if official_name:
            print(f"✅ Fixing: Grade {grade} {subject} Ch.{chapter_num}")
            print(f"   Old: {entry.chapter_name}")
            print(f"   New: {official_name}\n")

            entry.chapter_name = official_name
            fixed_count += 1
        else:
            print(f"⚠️  Unable to fix: Grade {grade} {subject} Ch.{chapter_num} - {entry.chapter_name}")
            unable_to_fix.append((grade, subject, chapter_num, entry.chapter_name))

    # Commit changes
    db.commit()

    print("=" * 100)
    print(f"✅ REPAIR COMPLETE")
    print("=" * 100)
    print(f"Fixed: {fixed_count} chapters")
    print(f"Unable to fix: {len(unable_to_fix)} chapters")

    if unable_to_fix:
        print("\n📋 Entries that need manual review:")
        for grade, subject, ch_num, name in unable_to_fix[:20]:
            print(f"   Grade {grade} | {subject:20} | Ch.{ch_num:2} | {name}")

    print("=" * 100)

    db.close()

    return fixed_count, unable_to_fix


if __name__ == "__main__":
    fixed, unable = repair_chapter_names()

    print(f"\n✅ Repaired {fixed} chapter names successfully!")

    if unable:
        print(f"\n⚠️  {len(unable)} entries need additional official chapter mapping")
        print("   Add them to OFFICIAL_CHAPTER_NAMES dictionary and run again")
