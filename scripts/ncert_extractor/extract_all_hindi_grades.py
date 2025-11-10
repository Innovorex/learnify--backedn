#!/usr/bin/env python3
"""
Extract ALL Hindi PDFs (Grades 1-10) with OCR
==============================================
Extracts all available Hindi PDFs using Tesseract OCR
and saves them to the database with proper Unicode Devanagari.

Total PDFs: 97
- Grade 1: 1 PDF
- Grade 7: 16 PDFs
- Grade 8: 22 PDFs
- Grade 9: 29 PDFs
- Grade 10: 29 PDFs
"""

import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

import os
import re
from pathlib import Path
from typing import Tuple
import pytesseract
from pdf2image import convert_from_path
from database import SessionLocal
from models import NCERTTextbookContent


def extract_text_from_pdf_ocr(pdf_path: str, dpi: int = 300) -> str:
    """Extract text from PDF using OCR"""
    print(f"   📄 Converting PDF to images (DPI: {dpi})...")
    images = convert_from_path(pdf_path, dpi=dpi)
    print(f"   ✅ Converted {len(images)} pages")

    all_text = []
    for i, image in enumerate(images, 1):
        text = pytesseract.image_to_string(image, lang='hin')
        all_text.append(text)
        if i % 5 == 0:
            print(f"   ... processed {i}/{len(images)} pages")

    return "\n\n".join(all_text)


def parse_filename(filename: str) -> Tuple[int, str, int, str]:
    """
    Parse PDF filename to extract grade, book, chapter number

    Returns: (grade, book, chapter_num, book_display_name)
    """
    # Examples:
    # grade9_hindi_kshitij_ch01.pdf
    # grade7_hindi_mahabharat_ch01.pdf
    # grade1_hindi_rimjhim_ch01.pdf

    match = re.match(r'grade(\d+)_hindi_([a-z_]+)_ch(\d+)\.pdf', filename)
    if match:
        grade = int(match.group(1))
        book = match.group(2)
        chapter = int(match.group(3))

        # Convert book name to display format
        book_display = book.replace('_', ' ').title()

        return grade, book, chapter, book_display

    return None, None, None, None


def get_chapter_name(grade: int, book: str, chapter_num: int) -> str:
    """
    Get chapter name if known, otherwise return generic name
    """
    # You can add specific chapter names here later
    # For now, return generic name
    return f"Chapter {chapter_num}"


def extract_all_hindi_pdfs():
    """Extract ALL Hindi PDFs from grades 1-10"""

    pdf_dir = Path("/home/learnify/lt/learnify-teach/ncert_pdfs")
    db = SessionLocal()

    # Get all Hindi PDFs
    all_hindi_pdfs = sorted(pdf_dir.glob("*hindi*.pdf"))

    print("🚀 EXTRACTING ALL HINDI CONTENT (GRADES 1-10)")
    print("=" * 70)
    print(f"Total PDFs to process: {len(all_hindi_pdfs)}")
    print("=" * 70)

    # Group by grade for reporting
    by_grade = {}
    for pdf in all_hindi_pdfs:
        for g in range(1, 11):
            if f"grade{g}_" in pdf.name:
                if g not in by_grade:
                    by_grade[g] = []
                by_grade[g].append(pdf)
                break

    for grade in sorted(by_grade.keys()):
        print(f"  Grade {grade}: {len(by_grade[grade])} PDFs")

    print("=" * 70)
    print("")

    total = len(all_hindi_pdfs)
    success = 0
    failed = 0
    skipped = 0

    for idx, pdf_path in enumerate(all_hindi_pdfs, 1):
        grade, book, chapter_num, book_display = parse_filename(pdf_path.name)

        if not grade or not book or not chapter_num:
            print(f"\n❌ [{idx}/{total}] Skipping {pdf_path.name} - invalid filename format")
            skipped += 1
            continue

        subject = f"Hindi_{book_display.replace(' ', '_')}"
        chapter_name = get_chapter_name(grade, book, chapter_num)

        print(f"\n{'='*70}")
        print(f"📚 [{idx}/{total}] Grade {grade} - {subject}")
        print(f"   Chapter {chapter_num}: {chapter_name}")
        print(f"   PDF: {pdf_path.name}")
        print(f"{'='*70}")

        try:
            # Extract text using OCR
            print(f"🔍 Running OCR...")
            content_text = extract_text_from_pdf_ocr(str(pdf_path), dpi=300)

            if len(content_text.strip()) < 50:
                print(f"❌ Extracted text too short ({len(content_text)} chars) - skipping")
                failed += 1
                continue

            # Verify quality
            dev_chars = sum(1 for c in content_text if '\u0900' <= c <= '\u097F')
            total_chars = len([c for c in content_text if c.strip()])
            purity = dev_chars / total_chars * 100 if total_chars > 0 else 0

            print(f"✅ OCR Complete!")
            print(f"   Devanagari: {purity:.1f}%")
            print(f"   Length: {len(content_text)} characters")
            print(f"   Preview: {content_text[:80]}...")

            # Check if entry exists
            existing = db.query(NCERTTextbookContent).filter(
                NCERTTextbookContent.grade == grade,
                NCERTTextbookContent.subject == subject,
                NCERTTextbookContent.chapter_number == chapter_num
            ).first()

            if existing:
                print(f"📝 Updating existing entry (ID: {existing.id})")
                existing.chapter_name = chapter_name
                existing.content_text = content_text
            else:
                print(f"➕ Creating new entry")
                new_content = NCERTTextbookContent(
                    board='CBSE',
                    grade=grade,
                    subject=subject,
                    chapter_number=chapter_num,
                    chapter_name=chapter_name,
                    content_text=content_text,
                    content_type='full_chapter',
                    extraction_method='ocr_tesseract'
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
    print(f"📊 EXTRACTION COMPLETE")
    print(f"{'='*70}")
    print(f"Total PDFs:          {total}")
    print(f"✅ Successfully extracted: {success}")
    print(f"❌ Failed:           {failed}")
    print(f"⏭️  Skipped:          {skipped}")
    print(f"Success rate:        {success/total*100:.1f}%")
    print(f"{'='*70}")

    # Quality summary
    print(f"\n📊 QUALITY VERIFICATION")
    print(f"{'='*70}")

    db = SessionLocal()
    all_hindi = db.query(NCERTTextbookContent).filter(
        NCERTTextbookContent.subject.ilike('%hindi%')
    ).all()

    ocr_quality = sum(1 for h in all_hindi if sum(1 for c in h.content_text if '\u0900' <= c <= '\u097F') / max(len([c for c in h.content_text if c.strip()]), 1) * 100 >= 92)

    print(f"Total Hindi chapters in DB: {len(all_hindi)}")
    print(f"OCR Quality (≥92%):         {ocr_quality}")
    print(f"OCR Coverage:               {ocr_quality/len(all_hindi)*100:.1f}%")
    print(f"{'='*70}")

    db.close()


if __name__ == "__main__":
    print("\n")
    extract_all_hindi_pdfs()
    print("\n✅ ALL HINDI CONTENT EXTRACTION COMPLETE!\n")
