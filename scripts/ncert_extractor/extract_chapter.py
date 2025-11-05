#!/usr/bin/env python3
"""
Extract content from a single NCERT chapter PDF
Improved version that handles individual chapter files
"""

import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

import pdfplumber
import re
from pathlib import Path
from database import SessionLocal
from models import (NCERTTextbookContent, NCERTExample, NCERTExercise, NCERTImage)


def extract_chapter_info(first_page_text):
    """Extract chapter number and name from first page"""
    lines = first_page_text.split('\n')

    # Pattern: "REAL NUMBERS 1" or "1 REAL NUMBERS"
    for i, line in enumerate(lines[:10]):
        line = line.strip()
        # Try to find chapter name in first few lines
        if len(line) > 3 and line.isupper() and not line.startswith('CHAPTER'):
            # This might be the chapter name
            # Remove any numbers at start or end
            chapter_name = re.sub(r'^\d+\s*', '', line)
            chapter_name = re.sub(r'\s*\d+$', '', chapter_name)
            if len(chapter_name) > 3:
                return chapter_name.title()

    return "Unknown Chapter"


def extract_examples(page_texts):
    """Extract all examples from the chapter"""
    examples = []

    all_text = "\n".join(page_texts.values())

    # Pattern: Example 1 : text... Solution: text...
    pattern = r'Example\s+(\d+)\s*[:.]?\s*(.*?)(?=Example\s+\d+|EXERCISE|$)'

    matches = re.finditer(pattern, all_text, re.DOTALL | re.IGNORECASE)

    for match in matches:
        example_num = match.group(1)
        content = match.group(2).strip()

        if len(content) < 50:
            continue

        # Try to split problem and solution
        problem = content
        solution = ""

        # Look for solution markers
        for marker in ['Solution', 'SOLUTION', 'Answer', 'Proof']:
            if marker in content:
                parts = content.split(marker, 1)
                problem = parts[0].strip()
                solution = parts[1].strip() if len(parts) > 1 else ""
                break

        examples.append({
            'example_number': f"Example {example_num}",
            'problem_statement': problem[:3000],
            'solution_text': solution[:5000]
        })

    return examples


def extract_exercises(page_texts):
    """Extract exercise questions"""
    exercises = []

    all_text = "\n".join(page_texts.values())

    # Find EXERCISE section
    exercise_match = re.search(r'EXERCISE\s+(\d+\.?\d*)', all_text, re.IGNORECASE)
    if not exercise_match:
        return exercises

    exercise_num = exercise_match.group(1)

    # Get text after EXERCISE header
    exercise_start = exercise_match.end()
    exercise_text = all_text[exercise_start:]

    # Extract questions (numbered 1., 2., 3. etc.)
    question_pattern = r'^\s*(\d+)\.\s+(.+?)(?=^\s*\d+\.|$)'

    questions = re.finditer(question_pattern, exercise_text, re.MULTILINE | re.DOTALL)

    for q_match in questions:
        q_num = q_match.group(1)
        q_text = q_match.group(2).strip()

        # Stop at next major section
        if any(marker in q_text for marker in ['SUMMARY', 'CHAPTER', 'EXERCISE']):
            break

        if len(q_text) > 10 and len(q_text) < 3000:
            exercises.append({
                'exercise_number': f"Exercise {exercise_num}",
                'question_number': q_num,
                'question_text': q_text[:2000]
            })

    return exercises


def process_chapter(pdf_path, grade, subject, chapter_number):
    """Process a single chapter PDF"""

    pdf_path = Path(pdf_path)
    db = SessionLocal()

    print(f"\n{'='*80}")
    print(f"📖 Processing Chapter: {pdf_path.name}")
    print(f"   Grade {grade} - {subject} - Chapter {chapter_number}")
    print(f"{'='*80}\n")

    # Extract text from all pages
    page_texts = {}
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"Total pages: {total_pages}")

        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                page_texts[page_num] = text

        print(f"✅ Extracted text from {len(page_texts)} pages\n")

    # Get chapter name
    first_page = page_texts.get(1, "")
    chapter_name = extract_chapter_info(first_page)
    print(f"📚 Chapter Name: {chapter_name}\n")

    # Store main content
    all_text = "\n\n".join(page_texts.values())
    content = NCERTTextbookContent(
        board="CBSE",
        grade=grade,
        subject=subject,
        chapter_number=chapter_number,
        chapter_name=chapter_name,
        content_type="explanation",
        content_text=all_text[:50000],  # Store first 50K chars
        page_start=1,
        page_end=total_pages,
        extraction_method="pdf_extract"
    )
    db.add(content)
    db.flush()  # Get the ID

    # Extract examples
    print("📝 Extracting examples...")
    examples = extract_examples(page_texts)
    print(f"   Found {len(examples)} examples")

    for ex in examples:
        example = NCERTExample(
            content_id=content.id,
            grade=grade,
            subject=subject,
            chapter_name=chapter_name,
            **ex
        )
        db.add(example)

    # Extract exercises
    print("\n✏️  Extracting exercises...")
    exercises = extract_exercises(page_texts)
    print(f"   Found {len(exercises)} exercises")

    for ex in exercises:
        exercise = NCERTExercise(
            grade=grade,
            subject=subject,
            chapter_name=chapter_name,
            **ex
        )
        db.add(exercise)

    # Commit everything
    db.commit()

    print(f"\n{'='*80}")
    print(f"✅ Extraction Complete!")
    print(f"   Chapter: {chapter_name}")
    print(f"   Examples: {len(examples)}")
    print(f"   Exercises: {len(exercises)}")
    print(f"   Saved to database")
    print(f"{'='*80}\n")

    db.close()

    return {
        'chapter_name': chapter_name,
        'examples_count': len(examples),
        'exercises_count': len(exercises)
    }


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("\nUsage: python3 extract_chapter.py <pdf_path> <grade> <subject> <chapter_number>")
        print("\nExample:")
        print("  python3 extract_chapter.py ../ncert_pdfs/grade_10_math_ch01.pdf 10 Mathematics 1\n")
        sys.exit(1)

    pdf_path = sys.argv[1]
    grade = int(sys.argv[2])
    subject = sys.argv[3]
    chapter_num = int(sys.argv[4])

    process_chapter(pdf_path, grade, subject, chapter_num)
