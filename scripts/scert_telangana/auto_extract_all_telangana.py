#!/usr/bin/env python3
"""
Automatically extract ALL Telangana textbooks with intelligent chapter detection
- Uses TOC parsing where available
- Falls back to smart chapter detection
- Processes all 49 books in one run
"""

import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

import re
import json
from pathlib import Path
from database import SessionLocal
from models import NCERTTextbookContent
import pdfplumber

# Try OCR
try:
    from pdf2image import convert_from_path
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

PDF_DIR = Path("/home/learnify/lt/learnify-teach/backend/ts_pdfs")


def find_toc_page(pdf_path):
    """Find the TOC page in a PDF"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num in range(min(20, len(pdf.pages))):
                text = pdf.pages[page_num].extract_text()
                if text:
                    text_upper = text.upper()
                    if any(keyword in text_upper for keyword in ['CONTENTS', 'TABLE OF CONTENTS', 'INDEX']):
                        # Make sure it has chapter-like content
                        if any(marker in text for marker in ['1.', 'Chapter', 'Unit', 'Lesson']):
                            return page_num, text
    except:
        pass
    return None, None


def parse_toc_intelligently(toc_text, total_pages):
    """Parse TOC using multiple patterns"""
    chapters = []
    lines = toc_text.split('\n')

    # Pattern 1: "1. Title ... 10-20" or "1 Title 10-20"
    pattern1 = re.compile(r'^\s*(\d+)\.?\s+(.+?)\s+(\d+)\s*[-–]\s*(\d+)', re.MULTILINE)

    # Pattern 2: "Chapter 1 Title Page 10"
    pattern2 = re.compile(r'(?:Chapter|Unit|Lesson)\s+(\d+)[:\s]+(.+?)\s+.*?(\d+)(?:\s*[-–]\s*(\d+))?', re.IGNORECASE)

    # Pattern 3: Simple "Title Page 10-20"
    pattern3 = re.compile(r'([A-Z][A-Za-z\s\-,&]+?)\s+(\d+)\s*[-–]\s*(\d+)')

    # Try each pattern
    for line in lines:
        line = line.strip()
        if not line or len(line) < 5:
            continue

        # Try pattern 1
        match = pattern1.search(line)
        if match:
            num, title, start, end = match.groups()
            start, end = int(start), int(end)
            if 1 <= start < end <= total_pages and len(title.strip()) > 2:
                chapters.append({
                    'number': int(num),
                    'title': title.strip(),
                    'start_page': start,
                    'end_page': end
                })
                continue

        # Try pattern 2
        match = pattern2.search(line)
        if match:
            num, title, start = match.groups()[:3]
            end = match.group(4) if match.group(4) else None
            start = int(start)
            if end:
                end = int(end)
            else:
                # Estimate end page
                end = min(start + 20, total_pages)

            if 1 <= start <= total_pages and len(title.strip()) > 2:
                chapters.append({
                    'number': int(num),
                    'title': title.strip(),
                    'start_page': start,
                    'end_page': end
                })

    # Remove duplicates
    seen = set()
    unique_chapters = []
    for ch in chapters:
        key = (ch['number'], ch['title'])
        if key not in seen:
            seen.add(key)
            unique_chapters.append(ch)

    return sorted(unique_chapters, key=lambda x: x['number'])


def smart_chapter_split(total_pages, book_name):
    """Fallback: split into smart sections"""
    # Determine number of sections based on page count
    if total_pages <= 40:
        num_sections = 4
    elif total_pages <= 80:
        num_sections = 6
    elif total_pages <= 150:
        num_sections = 8
    else:
        num_sections = 10

    pages_per_section = total_pages // num_sections

    sections = []
    for i in range(num_sections):
        start = i * pages_per_section + 1
        end = (i + 1) * pages_per_section if i < num_sections - 1 else total_pages

        sections.append({
            'number': i + 1,
            'title': f'Section {i + 1}',
            'start_page': start,
            'end_page': end
        })

    return sections


def extract_text(pdf_path, start_page, end_page, use_ocr=False):
    """Extract text from page range"""
    if use_ocr and OCR_AVAILABLE:
        lang = 'tel+eng' if 'telugu' in pdf_path.name.lower() else 'hin+eng' if 'hindi' in pdf_path.name.lower() else 'eng'

        images = convert_from_path(pdf_path, dpi=200, first_page=start_page + 1, last_page=end_page + 1)
        return "\n\n".join([pytesseract.image_to_string(img, lang=lang) for img in images])

    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in range(start_page, min(end_page + 1, len(pdf.pages))):
            if page_num < len(pdf.pages):
                text = pdf.pages[page_num].extract_text()
                if text:
                    text_parts.append(text)
    return "\n\n".join(text_parts)


def parse_filename(filename):
    """Extract grade and subject from filename"""
    parts = filename.replace('.pdf', '').split('_')
    grade = int(parts[0].replace('grade', ''))

    subject_map = {
        ('biological', 'science', 'english'): 'Biological Science',
        ('physical', 'science', 'english'): 'Physical Science',
        ('environmental', 'education', 'english'): 'Environmental Education',
        ('social', 'studies', 'english'): 'Social Studies',
        ('english',): 'English',
        ('telugu', 'first', 'language'): 'Telugu First Language',
        ('telugu', 'second', 'language'): 'Telugu Second Language',
        ('hindi', 'first', 'language'): 'Hindi First Language',
        ('hindi', 'second', 'language'): 'Hindi Second Language',
        ('mathematics', 'english'): 'Mathematics',
        ('science', 'english'): 'Science',
        ('evs', 'english'): 'Evs'
    }

    subject_key = tuple(parts[1:])
    subject = subject_map.get(subject_key, ' '.join(word.capitalize() for word in parts[1:] if word != 'english'))

    return grade, subject


def process_all_pdfs():
    """Process all PDFs in the directory"""

    pdf_files = sorted(PDF_DIR.glob("grade*.pdf"))

    db = SessionLocal()

    total_extracted = 0
    total_skipped = 0
    total_failed = 0

    print("="*80)
    print("AUTOMATED TELANGANA EXTRACTION - ALL BOOKS")
    print("="*80)
    print(f"Found {len(pdf_files)} PDF files")
    print()

    for idx, pdf_path in enumerate(pdf_files, 1):
        print(f"\n{'='*80}")
        print(f"📖 [{idx}/{len(pdf_files)}] {pdf_path.name}")
        print(f"{'='*80}")

        try:
            grade, subject = parse_filename(pdf_path.name)
            use_ocr = 'telugu' in pdf_path.name.lower() or 'hindi' in pdf_path.name.lower()

            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)

            print(f"   Grade: {grade}, Subject: {subject}")
            print(f"   Total Pages: {total_pages}")
            if use_ocr:
                print(f"   Mode: OCR")

            # Try to find and parse TOC
            toc_page_num, toc_text = find_toc_page(pdf_path)

            if toc_page_num is not None and toc_text:
                print(f"   ✅ TOC found on page {toc_page_num + 1}")
                chapters = parse_toc_intelligently(toc_text, total_pages)

                if len(chapters) >= 3:
                    print(f"   ✅ Parsed {len(chapters)} chapters from TOC")
                else:
                    print(f"   ⚠️  Only found {len(chapters)} chapters, using smart split")
                    chapters = smart_chapter_split(total_pages, pdf_path.name)
            else:
                print(f"   ⚠️  No TOC found, using smart section split")
                chapters = smart_chapter_split(total_pages, pdf_path.name)

            print(f"   Processing {len(chapters)} chapters/sections...")
            print()

            # Extract each chapter
            for chapter in chapters:
                ch_num = chapter['number']
                ch_title = chapter['title']
                start = chapter['start_page']
                end = chapter['end_page']

                print(f"      📄 Chapter {ch_num}: {ch_title[:50]} (pages {start}-{end})")

                # Check if exists
                existing = db.query(NCERTTextbookContent).filter(
                    NCERTTextbookContent.board == 'TELANGANA',
                    NCERTTextbookContent.grade == grade,
                    NCERTTextbookContent.subject == subject,
                    NCERTTextbookContent.chapter_number == ch_num
                ).first()

                if existing:
                    print(f"         ⏭️  Skip (exists)")
                    total_skipped += 1
                    continue

                try:
                    # Extract content
                    content = extract_text(pdf_path, start - 1, end - 1, use_ocr=use_ocr)

                    if len(content) < 50:
                        print(f"         ⚠️  Very little content ({len(content)} chars)")

                    # Save to database
                    entry = NCERTTextbookContent(
                        board='TELANGANA',
                        grade=grade,
                        subject=subject,
                        chapter_number=ch_num,
                        chapter_name=ch_title,
                        content_type='textbook_chapter',
                        content_text=content,
                        extraction_method='auto_intelligent'
                    )

                    db.add(entry)
                    db.commit()

                    print(f"         ✅ Extracted ({len(content):,} chars)")
                    total_extracted += 1

                except Exception as e:
                    print(f"         ❌ Error: {e}")
                    total_failed += 1
                    db.rollback()

        except Exception as e:
            print(f"   ❌ Failed to process book: {e}")
            continue

    db.close()

    print(f"\n{'='*80}")
    print("EXTRACTION COMPLETE")
    print(f"{'='*80}")
    print(f"✅ Extracted: {total_extracted} chapters")
    print(f"⏭️  Skipped: {total_skipped} chapters")
    print(f"❌ Failed: {total_failed} chapters")
    print(f"Success rate: {total_extracted/(total_extracted+total_failed)*100 if (total_extracted+total_failed) > 0 else 0:.1f}%")


if __name__ == "__main__":
    process_all_pdfs()
