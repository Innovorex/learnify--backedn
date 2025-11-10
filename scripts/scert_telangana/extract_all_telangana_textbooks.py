#!/usr/bin/env python3
"""
Extract ALL Telangana State Board Textbooks
============================================
Processes all 60 Telangana SCERT textbooks:
1. Parses Table of Contents
2. Identifies chapter boundaries
3. Splits PDFs into individual chapters
4. Extracts content (with OCR for Telugu/Hindi)
5. Saves to database with board='TELANGANA'
"""

import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

import os
import re
import gc  # ADDED: Garbage collection for memory management
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Import OCR libraries
try:
    import pytesseract
    from pdf2image import convert_from_path
    OCR_AVAILABLE = True
except:
    OCR_AVAILABLE = False
    print("⚠️  OCR not available")

import PyPDF2
import pdfplumber
from database import SessionLocal
from models import NCERTTextbookContent
from sqlalchemy import func


def should_use_ocr(filename: str) -> Tuple[bool, str]:
    """Determine if OCR should be used and which language"""
    if 'telugu' in filename.lower():
        return True, 'tel+eng'
    elif 'hindi' in filename.lower():
        return True, 'hin+eng'
    else:
        return False, 'eng'


def extract_text_with_pdfplumber(pdf_path: str, start_page: int, end_page: int) -> str:
    """Extract text from specific page range using pdfplumber"""
    all_text = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num in range(start_page, min(end_page + 1, len(pdf.pages))):
                page = pdf.pages[page_num]
                text = page.extract_text()
                if text:
                    all_text.append(text)

        return "\n\n".join(all_text)
    except Exception as e:
        print(f"   ⚠️  pdfplumber error: {e}")
        return ""


def extract_text_with_ocr(pdf_path: str, start_page: int, end_page: int, lang: str = 'tel+eng', dpi: int = 200) -> str:
    """Extract text from specific page range using OCR (200 DPI for memory efficiency)"""
    if not OCR_AVAILABLE:
        return ""

    try:
        # Convert specific pages to images (200 DPI uses ~40% less memory than 300 DPI)
        images = convert_from_path(
            pdf_path,
            dpi=dpi,
            first_page=start_page + 1,  # pdf2image uses 1-indexed
            last_page=end_page + 1
        )

        all_text = []
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang=lang)
            if text.strip():
                all_text.append(text)

        return "\n\n".join(all_text)
    except Exception as e:
        print(f"   ⚠️  OCR error: {e}")
        return ""


def parse_toc_from_pdf(pdf_path: str) -> List[Dict]:
    """
    Parse Table of Contents from PDF
    Returns list of chapters with start/end pages
    """
    chapters = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Check first 20 pages for TOC
            toc_text = ""
            for i in range(min(20, len(pdf.pages))):
                page_text = pdf.pages[i].extract_text()
                if page_text:
                    toc_text += page_text + "\n"

            # Look for chapter patterns
            # Pattern 1: "01 Real Numbers ... 1 - 28"
            # Pattern 2: "1. Real Numbers ... 1-28"
            # Pattern 3: "Chapter 1: Real Numbers ... Page 1"

            lines = toc_text.split('\n')

            for line in lines:
                # Pattern: Number followed by name and page range
                match = re.search(r'(\d+)\s+([A-Za-z\s\-&,]+?)\s+(?:\d+\s+)?(?:\w+\s+)?(\d+)\s*[-–]\s*(\d+)', line)

                if match:
                    ch_num = int(match.group(1))
                    ch_name = match.group(2).strip()
                    start_page = int(match.group(3))
                    end_page = int(match.group(4))

                    # Filter out noise (too short names, invalid ranges)
                    if len(ch_name) >= 3 and end_page > start_page and end_page - start_page < 100:
                        chapters.append({
                            'number': ch_num,
                            'name': ch_name,
                            'start': start_page,
                            'end': end_page
                        })

            # Remove duplicates and sort
            seen = set()
            unique_chapters = []
            for ch in chapters:
                key = (ch['number'], ch['name'])
                if key not in seen:
                    seen.add(key)
                    unique_chapters.append(ch)

            unique_chapters.sort(key=lambda x: x['number'])

            return unique_chapters

    except Exception as e:
        print(f"   ⚠️  TOC parsing error: {e}")
        return []


def parse_filename(filename: str) -> Tuple[int, str, str]:
    """
    Parse Telangana PDF filename
    Returns: (grade, subject, medium)
    Example: grade10_mathematics_english.pdf -> (10, 'Mathematics', 'English')
    """
    pattern = r'grade(\d+)_([a-z_]+?)(?:_(english|telugu|hindi))?.pdf'
    match = re.match(pattern, filename.lower())

    if match:
        grade = int(match.group(1))
        subject_raw = match.group(2)
        medium = match.group(3) if match.group(3) else 'english'

        # Normalize subject name
        subject = subject_raw.replace('_', ' ').title()

        return grade, subject, medium

    return None, None, None


def get_page_offset(pdf_path: str, first_chapter_start: int) -> int:
    """
    Calculate offset between TOC page numbers and actual PDF page indices
    """
    # Most Telangana textbooks have ~10 pages of front matter
    # TOC says "page 1" but it's actually around page 11 in PDF
    return 10  # Default offset, can be refined per book


def main():
    pdf_directory = Path("/home/learnify/lt/learnify-teach/backend/ts_pdfs")

    print("=" * 90)
    print("TELANGANA STATE BOARD - COMPLETE EXTRACTION")
    print("=" * 90)
    print(f"PDF Directory: {pdf_directory}")
    print(f"OCR Available: {OCR_AVAILABLE}")
    print("=" * 90)

    if not pdf_directory.exists():
        print(f"❌ Error: PDF directory not found: {pdf_directory}")
        return

    # Get all textbook PDFs
    all_pdfs = sorted(list(pdf_directory.glob("grade*.pdf")))

    if not all_pdfs:
        print(f"❌ No PDF files found in {pdf_directory}")
        return

    print(f"\n📚 Found {len(all_pdfs)} textbooks")

    # Database connection
    db = SessionLocal()

    # Statistics
    total_textbooks = len(all_pdfs)
    total_chapters = 0
    successful_chapters = 0
    failed_chapters = 0
    skipped_textbooks = 0

    for idx, pdf_path in enumerate(all_pdfs, 1):
        filename = pdf_path.name
        grade, subject, medium = parse_filename(filename)

        if not grade or not subject:
            print(f"\n❌ [{idx}/{total_textbooks}] Skipping {filename} - invalid filename")
            skipped_textbooks += 1
            continue

        print(f"\n{'='*90}")
        print(f"📖 [{idx}/{total_textbooks}] Grade {grade} - {subject} ({medium.title()} Medium)")
        print(f"   File: {filename}")
        print(f"{'='*90}")

        # Parse Table of Contents
        print(f"📑 Parsing Table of Contents...")
        chapters = parse_toc_from_pdf(str(pdf_path))

        if not chapters:
            print(f"   ⚠️  No chapters found in TOC - trying simple extraction")
            # Fallback: treat entire book as one chapter
            chapters = [{
                'number': 1,
                'name': f'{subject} Complete',
                'start': 1,
                'end': 100  # Will be adjusted
            }]

        print(f"   ✅ Found {len(chapters)} chapters")

        # Calculate page offset
        page_offset = get_page_offset(str(pdf_path), chapters[0]['start'] if chapters else 1)

        # Process each chapter
        for ch in chapters:
            ch_num = ch['number']
            ch_name = ch['name']
            toc_start = ch['start']
            toc_end = ch['end']

            # Convert TOC pages to actual PDF page indices (0-indexed)
            pdf_start = toc_start + page_offset - 1
            pdf_end = toc_end + page_offset - 1

            print(f"\n   📄 Chapter {ch_num}: {ch_name}")
            print(f"      TOC Pages: {toc_start}-{toc_end} → PDF Pages: {pdf_start}-{pdf_end}")

            total_chapters += 1

            try:
                # Check if already exists
                existing = db.query(NCERTTextbookContent).filter(
                    NCERTTextbookContent.board == 'TELANGANA',
                    NCERTTextbookContent.grade == grade,
                    NCERTTextbookContent.subject == subject,
                    NCERTTextbookContent.chapter_number == ch_num
                ).first()

                if existing:
                    print(f"      ⏭️  Already exists (ID: {existing.id}) - skipping")
                    successful_chapters += 1
                    continue

                # Determine extraction method
                use_ocr, ocr_lang = should_use_ocr(filename)

                # Extract content
                if use_ocr and OCR_AVAILABLE:
                    print(f"      🔍 Using OCR ({ocr_lang}) at 200 DPI...")
                    content_text = extract_text_with_ocr(str(pdf_path), pdf_start, pdf_end, ocr_lang, dpi=200)
                    extraction_method = f'ocr_tesseract_{ocr_lang}_200dpi'
                else:
                    print(f"      📄 Using pdfplumber...")
                    content_text = extract_text_with_pdfplumber(str(pdf_path), pdf_start, pdf_end)
                    extraction_method = 'pdfplumber'

                if len(content_text.strip()) < 100:
                    print(f"      ❌ Extracted text too short ({len(content_text)} chars) - skipping")
                    failed_chapters += 1
                    continue

                print(f"      ✅ Extracted: {len(content_text):,} characters")
                print(f"         Preview: {content_text[:80].strip()}...")

                # Save to database
                print(f"      💾 Saving to database...")
                new_content = NCERTTextbookContent(
                    board='TELANGANA',
                    grade=grade,
                    subject=subject,
                    chapter_number=ch_num,
                    chapter_name=ch_name,
                    content_text=content_text,
                    content_type='full_chapter',
                    extraction_method=extraction_method
                )
                db.add(new_content)
                db.commit()

                successful_chapters += 1
                print(f"      ✅ Saved (ID: {new_content.id})")

            except Exception as e:
                print(f"      ❌ Error: {e}")
                import traceback
                traceback.print_exc()
                db.rollback()
                failed_chapters += 1
                continue

        # ADDED: Memory cleanup after each PDF
        db.commit()  # Ensure all chapters are saved
        gc.collect()  # Force garbage collection to free memory
        print(f"   🧹 Memory cleanup complete\n")

    db.close()

    # Final report
    print(f"\n{'='*90}")
    print("EXTRACTION COMPLETE")
    print(f"{'='*90}")
    print(f"Total textbooks:           {total_textbooks}")
    print(f"Skipped textbooks:         {skipped_textbooks}")
    print(f"Total chapters found:      {total_chapters}")
    print(f"✅ Successfully extracted:  {successful_chapters}")
    print(f"❌ Failed:                  {failed_chapters}")
    print(f"Success rate:              {successful_chapters / total_chapters * 100 if total_chapters > 0 else 0:.1f}%")
    print(f"{'='*90}")

    # Final database status
    db = SessionLocal()
    telangana_total = db.query(func.count(NCERTTextbookContent.id)).filter(
        NCERTTextbookContent.board == 'TELANGANA'
    ).scalar()

    print(f"\n📊 Total Telangana chapters in database: {telangana_total}")

    # By grade
    print(f"\nBy Grade:")
    for grade in range(1, 11):
        count = db.query(func.count(NCERTTextbookContent.id)).filter(
            NCERTTextbookContent.board == 'TELANGANA',
            NCERTTextbookContent.grade == grade
        ).scalar()
        if count > 0:
            print(f"  Grade {grade:2d}: {count:3d} chapters")

    db.close()
    print(f"{'='*90}")


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
