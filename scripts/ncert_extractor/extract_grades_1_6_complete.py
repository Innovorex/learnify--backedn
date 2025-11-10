#!/usr/bin/env python3
"""
Extract ALL Content for Grades 1-6
===================================
Extracts all 116 PDFs for Grades 1-6 covering:
- English
- Hindi (with OCR for proper Devanagari)
- Mathematics
- EVS (Environmental Studies)
- Science

This will complete the missing subjects for Grades 1-6.
"""

import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

import os
import re
from pathlib import Path
from typing import Tuple

# Import OCR for Hindi
try:
    import pytesseract
    from pdf2image import convert_from_path
    OCR_AVAILABLE = True
except:
    OCR_AVAILABLE = False

import pdfplumber
from database import SessionLocal
from models import NCERTTextbookContent


def extract_text_with_pdfplumber(pdf_path: str) -> str:
    """Extract text from PDF using pdfplumber (for English, Math, EVS, Science)"""
    all_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)

    return "\n\n".join(all_text)


def extract_text_with_ocr(pdf_path: str, dpi: int = 300) -> str:
    """Extract text from PDF using OCR (for Hindi PDFs)"""
    if not OCR_AVAILABLE:
        print("   ⚠️  OCR not available, using pdfplumber")
        return extract_text_with_pdfplumber(pdf_path)

    print(f"   📄 Converting to images (DPI: {dpi})...")
    images = convert_from_path(pdf_path, dpi=dpi)

    all_text = []
    for i, image in enumerate(images, 1):
        text = pytesseract.image_to_string(image, lang='hin')
        all_text.append(text)
        if i % 5 == 0:
            print(f"   ... OCR processed {i}/{len(images)} pages")

    return "\n\n".join(all_text)


def parse_filename(filename: str) -> Tuple[int, str, int, str]:
    """
    Parse PDF filename
    Returns: (grade, subject, chapter_num, book_name)
    """
    # Examples:
    # grade1_english_marigold_ch01.pdf
    # grade3_evs_looking_around_ch05.pdf
    # grade6_math_ganita_prakash_ch03.pdf

    match = re.match(r'grade(\d+)_([a-z]+)_([a-z_]+)_ch(\d+)\.pdf', filename)
    if match:
        grade = int(match.group(1))
        subject_key = match.group(2)
        book_key = match.group(3)
        chapter = int(match.group(4))

        # Create display names
        subject_map = {
            'english': 'English',
            'hindi': 'Hindi',
            'math': 'Mathematics',
            'evs': 'EVS',
            'science': 'Science'
        }

        subject = subject_map.get(subject_key, subject_key.title())
        book_name = book_key.replace('_', ' ').title()

        # Combined subject name
        if book_name:
            full_subject = f"{subject}_{book_name.replace(' ', '_')}"
        else:
            full_subject = subject

        return grade, full_subject, chapter, book_name

    return None, None, None, None


def should_use_ocr(subject: str) -> bool:
    """Determine if OCR should be used for this subject"""
    return 'hindi' in subject.lower()


def extract_all_grades_1_6():
    """Extract all PDFs for Grades 1-6"""

    pdf_dir = Path("/home/learnify/lt/learnify-teach/ncert_pdfs")
    db = SessionLocal()

    # Get all PDFs for grades 1-6
    all_pdfs = []
    for grade in range(1, 7):
        pdfs = sorted(pdf_dir.glob(f"grade{grade}_*.pdf"))
        all_pdfs.extend(pdfs)

    print("🚀 EXTRACTING ALL CONTENT - GRADES 1-6")
    print("=" * 70)
    print(f"Total PDFs to process: {len(all_pdfs)}")
    print("=" * 70)

    # Group by grade for display
    by_grade = {}
    for pdf in all_pdfs:
        for g in range(1, 7):
            if f"grade{g}_" in pdf.name:
                if g not in by_grade:
                    by_grade[g] = []
                by_grade[g].append(pdf)
                break

    for grade in sorted(by_grade.keys()):
        print(f"  Grade {grade}: {len(by_grade[grade])} PDFs")

    print("=" * 70)
    print("")

    total = len(all_pdfs)
    success = 0
    failed = 0
    skipped = 0

    for idx, pdf_path in enumerate(all_pdfs, 1):
        grade, subject, chapter_num, book_name = parse_filename(pdf_path.name)

        if not grade or not subject or not chapter_num:
            print(f"\n❌ [{idx}/{total}] Skipping {pdf_path.name} - invalid filename")
            skipped += 1
            continue

        chapter_name = f"Chapter {chapter_num}"

        print(f"\n{'='*70}")
        print(f"📚 [{idx}/{total}] Grade {grade} - {subject}")
        print(f"   Chapter {chapter_num}: {chapter_name}")
        print(f"   Book: {book_name}")
        print(f"   PDF: {pdf_path.name}")
        print(f"{'='*70}")

        try:
            # Check if already exists
            existing = db.query(NCERTTextbookContent).filter(
                NCERTTextbookContent.grade == grade,
                NCERTTextbookContent.subject == subject,
                NCERTTextbookContent.chapter_number == chapter_num
            ).first()

            if existing:
                print(f"⏭️  Already exists (ID: {existing.id}) - skipping")
                skipped += 1
                continue

            # Extract text
            use_ocr = should_use_ocr(subject)

            if use_ocr and OCR_AVAILABLE:
                print(f"🔍 Using OCR (Hindi content)...")
                content_text = extract_text_with_ocr(str(pdf_path), dpi=300)
            else:
                print(f"📄 Using pdfplumber...")
                content_text = extract_text_with_pdfplumber(str(pdf_path))

            if len(content_text.strip()) < 50:
                print(f"❌ Extracted text too short ({len(content_text)} chars) - skipping")
                failed += 1
                continue

            # Verify quality for Hindi
            if use_ocr:
                dev_chars = sum(1 for c in content_text if '\u0900' <= c <= '\u097F')
                total_chars = len([c for c in content_text if c.strip()])
                purity = dev_chars / total_chars * 100 if total_chars > 0 else 0
                print(f"   Devanagari: {purity:.1f}%")

            print(f"✅ Extracted: {len(content_text)} characters")
            print(f"   Preview: {content_text[:80]}...")

            # Save to database
            print(f"➕ Creating new entry")
            extraction_method = 'ocr_tesseract' if use_ocr else 'pdfplumber'
            new_content = NCERTTextbookContent(
                board='CBSE',
                grade=grade,
                subject=subject,
                chapter_number=chapter_num,
                chapter_name=chapter_name,
                content_text=content_text,
                content_type='full_chapter',
                extraction_method=extraction_method
            )
            db.add(new_content)
            db.commit()

            success += 1
            print(f"✅ Saved to database")

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            db.rollback()
            failed += 1
            continue

    db.close()

    # Final report
    print(f"\n{'='*70}")
    print(f"📊 EXTRACTION COMPLETE - GRADES 1-6")
    print(f"{'='*70}")
    print(f"Total PDFs:              {total}")
    print(f"✅ Successfully extracted: {success}")
    print(f"⏭️  Already existed:        {skipped}")
    print(f"❌ Failed:                 {failed}")
    print(f"Success rate:            {success/(total-skipped)*100 if total > skipped else 0:.1f}%")
    print(f"{'='*70}")

    # Quality summary
    print(f"\n📊 FINAL DATABASE STATUS")
    print(f"{'='*70}")

    db = SessionLocal()

    for grade in range(1, 7):
        total_chapters = db.query(NCERTTextbookContent).filter(
            NCERTTextbookContent.grade == grade
        ).count()

        subjects = db.query(NCERTTextbookContent.subject).filter(
            NCERTTextbookContent.grade == grade
        ).distinct().all()

        subject_list = ', '.join(s[0] for s in subjects[:5])
        if len(subjects) > 5:
            subject_list += f" (+{len(subjects)-5} more)"

        print(f"\nGrade {grade}: {total_chapters} chapters")
        print(f"  Subjects: {subject_list}")

    db.close()


if __name__ == "__main__":
    print("\n")
    extract_all_grades_1_6()
    print("\n✅ GRADES 1-6 EXTRACTION COMPLETE!\n")
