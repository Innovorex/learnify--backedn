#!/usr/bin/env python3
"""
Extract ALL Missing CBSE Content (Complete Extraction)
========================================================
This script extracts all CBSE content for Grades 1-10 covering:
- All subjects: English, Hindi, Mathematics, Science, EVS, Social Science
- Uses OCR for Hindi content
- Uses pdfplumber for other subjects
- Includes proper extraction_method field
"""

import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

import os
import re
from pathlib import Path
from typing import Tuple, List

# Import OCR for Hindi
try:
    import pytesseract
    from pdf2image import convert_from_path
    OCR_AVAILABLE = True
except:
    OCR_AVAILABLE = False
    print("⚠️  OCR not available - Hindi extraction may fail")

import pdfplumber
from database import SessionLocal
from models import NCERTTextbookContent
from sqlalchemy import func


def extract_text_with_pdfplumber(pdf_path: str) -> str:
    """Extract text from PDF using pdfplumber"""
    all_text = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text.append(text)

        return "\n\n".join(all_text)
    except Exception as e:
        print(f"   ⚠️  pdfplumber error: {e}")
        return ""


def extract_text_with_ocr(pdf_path: str, dpi: int = 300) -> str:
    """Extract text from PDF using OCR with Hindi language support"""
    if not OCR_AVAILABLE:
        return ""

    try:
        # Convert PDF to images
        images = convert_from_path(pdf_path, dpi=dpi)

        all_text = []
        for i, image in enumerate(images):
            # Use Hindi + English language
            text = pytesseract.image_to_string(image, lang='hin+eng')
            if text.strip():
                all_text.append(text)

        return "\n\n".join(all_text)
    except Exception as e:
        print(f"   ⚠️  OCR error: {e}")
        return ""


def should_use_ocr(subject: str) -> bool:
    """Determine if OCR should be used based on subject"""
    hindi_subjects = ['Hindi', 'hindi', 'Vasant', 'Sparsh', 'Kshitij', 'Kritika', 'BharatKiKhoj']
    return any(h in subject for h in hindi_subjects)


def parse_filename(filename: str) -> Tuple[int, str, int, str]:
    """Parse PDF filename to extract grade, subject, chapter number"""
    # Pattern: grade_X_Subject_Name_chYY.pdf
    pattern = r'grade_(\d+)_([A-Za-z_]+?)(?:_Complete|_Additional)?_ch(\d+)\.pdf'
    match = re.match(pattern, filename)

    if match:
        grade = int(match.group(1))
        subject = match.group(2)
        chapter_num = int(match.group(3))

        # Normalize subject name
        book_name = subject

        return grade, subject, chapter_num, book_name

    return None, None, None, None


def get_all_pdfs(pdf_dir: Path) -> List[Path]:
    """Get all PDF files sorted by name"""
    pdfs = list(pdf_dir.glob("*.pdf"))
    return sorted(pdfs)


def main():
    pdf_directory = Path("/home/learnify/lt/learnify-teach/backend/ncert_pdfs")

    print("=" * 80)
    print("CBSE COMPLETE EXTRACTION - ALL GRADES & SUBJECTS")
    print("=" * 80)
    print(f"PDF Directory: {pdf_directory}")
    print(f"OCR Available: {OCR_AVAILABLE}")
    print("=" * 80)

    if not pdf_directory.exists():
        print(f"❌ Error: PDF directory not found: {pdf_directory}")
        return

    # Get all PDFs
    all_pdfs = get_all_pdfs(pdf_directory)

    if not all_pdfs:
        print(f"❌ No PDF files found in {pdf_directory}")
        return

    print(f"\n📚 Found {len(all_pdfs)} PDF files")

    # Group by grade
    by_grade = {}
    for pdf_path in all_pdfs:
        grade, _, _, _ = parse_filename(pdf_path.name)
        if grade:
            if grade not in by_grade:
                by_grade[grade] = []
            by_grade[grade].append(pdf_path)

    print(f"\nPDFs by grade:")
    for grade in sorted(by_grade.keys()):
        print(f"  Grade {grade:2d}: {len(by_grade[grade]):3d} PDFs")

    # Database connection
    db = SessionLocal()

    # Check current database status
    print("\n" + "=" * 80)
    print("CURRENT DATABASE STATUS")
    print("=" * 80)

    for grade in range(1, 11):
        count = db.query(func.count(NCERTTextbookContent.id)).filter(
            NCERTTextbookContent.board == 'CBSE',
            NCERTTextbookContent.grade == grade
        ).scalar()
        print(f"Grade {grade:2d}: {count:3d} chapters in database")

    print("\n" + "=" * 80)
    print("STARTING EXTRACTION")
    print("=" * 80)

    total = len(all_pdfs)
    success = 0
    failed = 0
    skipped = 0

    for idx, pdf_path in enumerate(all_pdfs, 1):
        grade, subject, chapter_num, book_name = parse_filename(pdf_path.name)

        if not grade or not subject or chapter_num is None:
            print(f"\n❌ [{idx}/{total}] Skipping {pdf_path.name} - invalid filename")
            skipped += 1
            continue

        chapter_name = f"Chapter {chapter_num}"

        print(f"\n{'='*80}")
        print(f"📚 [{idx}/{total}] Grade {grade} - {subject} - Chapter {chapter_num}")
        print(f"   PDF: {pdf_path.name}")
        print(f"{'='*80}")

        try:
            # Check if already exists
            existing = db.query(NCERTTextbookContent).filter(
                NCERTTextbookContent.board == 'CBSE',
                NCERTTextbookContent.grade == grade,
                NCERTTextbookContent.subject == subject,
                NCERTTextbookContent.chapter_number == chapter_num
            ).first()

            if existing:
                print(f"⏭️  Already exists (ID: {existing.id}) - skipping")
                skipped += 1
                continue

            # Determine extraction method
            use_ocr = should_use_ocr(subject)

            # Extract text
            if use_ocr and OCR_AVAILABLE:
                print(f"🔍 Using OCR (Hindi content)...")
                content_text = extract_text_with_ocr(str(pdf_path), dpi=300)
                extraction_method = 'ocr_tesseract'
            else:
                print(f"📄 Using pdfplumber...")
                content_text = extract_text_with_pdfplumber(str(pdf_path))
                extraction_method = 'pdfplumber'

            if len(content_text.strip()) < 50:
                print(f"❌ Extracted text too short ({len(content_text)} chars) - skipping")
                failed += 1
                continue

            # Quality check for Hindi
            if use_ocr:
                dev_chars = sum(1 for c in content_text if '\u0900' <= c <= '\u097F')
                total_chars = len([c for c in content_text if c.strip()])
                purity = dev_chars / total_chars * 100 if total_chars > 0 else 0
                print(f"   Devanagari purity: {purity:.1f}%")

                if purity < 5:
                    print(f"⚠️  Low Devanagari content - might not be Hindi")

            print(f"✅ Extracted: {len(content_text):,} characters")
            print(f"   Preview: {content_text[:100].strip()}...")

            # Save to database
            print(f"💾 Saving to database...")
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
            print(f"✅ Saved successfully (ID: {new_content.id})")

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            db.rollback()
            failed += 1
            continue

    db.close()

    # Final report
    print(f"\n{'='*80}")
    print("EXTRACTION COMPLETE")
    print(f"{'='*80}")
    print(f"Total PDFs:              {total}")
    print(f"✅ Successfully extracted: {success}")
    print(f"⏭️  Already existed:        {skipped}")
    print(f"❌ Failed:                 {failed}")
    print(f"Success rate:            {success / (total - skipped) * 100 if (total - skipped) > 0 else 0:.1f}%")
    print(f"{'='*80}")

    # Final database status
    db = SessionLocal()
    print(f"\n{'='*80}")
    print("FINAL DATABASE STATUS")
    print(f"{'='*80}")

    total_chapters = 0
    for grade in range(1, 11):
        count = db.query(func.count(NCERTTextbookContent.id)).filter(
            NCERTTextbookContent.board == 'CBSE',
            NCERTTextbookContent.grade == grade
        ).scalar()
        total_chapters += count
        print(f"Grade {grade:2d}: {count:3d} chapters")

    print(f"\nTotal CBSE chapters: {total_chapters}")
    print(f"{'='*80}")

    db.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Extraction interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
