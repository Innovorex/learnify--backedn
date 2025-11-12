#!/usr/bin/env python3
"""
Enhanced chapter extraction with intelligent detection
- Improved TOC parsing with multiple patterns
- Chapter detection from page content (headers, titles)
- Smart section splitting as fallback
- Deletes old single-chapter entries and re-extracts properly
"""

import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

import re
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


def find_toc_advanced(pdf_path):
    """Advanced TOC detection"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num in range(min(25, len(pdf.pages))):
                text = pdf.pages[page_num].extract_text()
                if not text:
                    continue

                text_upper = text.upper()
                # Look for TOC indicators
                if any(kw in text_upper for kw in ['CONTENTS', 'TABLE OF CONTENTS', 'INDEX']):
                    # Must have chapter-like patterns
                    if re.search(r'\d+\.?\s+.{3,}\s+\d+', text) or \
                       re.search(r'(Chapter|Unit|Lesson)\s+\d+', text, re.IGNORECASE):
                        return page_num, text
    except:
        pass
    return None, None


def parse_toc_enhanced(toc_text, total_pages):
    """Enhanced TOC parsing with multiple patterns"""
    chapters = []
    lines = toc_text.split('\n')

    # Pattern 1: "1. Title ... 10-20" or "1 Title 10-20"
    pattern1 = re.compile(r'^\s*(\d+)\.?\s+(.{3,60}?)\s+(\d+)\s*[-–—]\s*(\d+)', re.MULTILINE)

    # Pattern 2: "Chapter/Unit/Lesson 1 Title ... 10"
    pattern2 = re.compile(r'(?:Chapter|Unit|Lesson)\s+(\d+)[:\s.,]+(.{3,60}?)\s+.*?(\d+)(?:\s*[-–—]\s*(\d+))?', re.IGNORECASE)

    # Pattern 3: Just number and title with page
    pattern3 = re.compile(r'^(\d+)\.\s+([A-Z][A-Za-z\s\-,&\(\)]{3,50})\s+(\d+)$', re.MULTILINE)

    # Pattern 4: S.No format (common in Telangana books)
    pattern4 = re.compile(r'^\d+\.\s+(.{3,60}?)\s+(\d+)\s*[-–—]\s*(\d+)', re.MULTILINE)

    for line in lines:
        line = line.strip()
        if len(line) < 5:
            continue

        # Try pattern 1
        match = pattern1.search(line)
        if match:
            num, title, start, end = match.groups()
            start, end = int(start), int(end)
            if 1 <= start < end <= total_pages + 50 and len(title.strip()) > 2:
                chapters.append({
                    'number': int(num),
                    'title': title.strip(),
                    'start_page': start,
                    'end_page': min(end, total_pages)
                })
                continue

        # Try pattern 2
        match = pattern2.search(line)
        if match:
            num, title, start = match.groups()[:3]
            end = match.group(4) if match.group(4) else None
            start = int(start)

            if not end or int(end) > total_pages + 50:
                # Estimate end page
                end = min(start + 25, total_pages)
            else:
                end = int(end)

            if 1 <= start <= total_pages + 20 and len(title.strip()) > 2:
                chapters.append({
                    'number': int(num),
                    'title': title.strip(),
                    'start_page': start,
                    'end_page': min(end, total_pages)
                })

    # Remove duplicates by chapter number and title
    seen = set()
    unique = []
    for ch in chapters:
        key = (ch['number'], ch['title'][:20])
        if key not in seen:
            seen.add(key)
            unique.append(ch)

    # Sort and fix overlapping page ranges
    unique.sort(key=lambda x: x['number'])

    # Adjust end pages to avoid overlaps
    for i in range(len(unique) - 1):
        if unique[i]['end_page'] >= unique[i+1]['start_page']:
            unique[i]['end_page'] = unique[i+1]['start_page'] - 1

    return unique


def detect_chapters_from_content(pdf_path, total_pages):
    """Detect chapters by analyzing page content"""
    chapters = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            chapter_num = 1
            current_start = 1

            # Sample every 10th page for chapter markers
            for page_num in range(0, min(total_pages, len(pdf.pages)), 10):
                text = pdf.pages[page_num].extract_text()
                if not text:
                    continue

                # Look for chapter markers
                lines = text.split('\n')[:5]  # First 5 lines

                for line in lines:
                    # Pattern: "Chapter 1" or "CHAPTER 1" or "Unit 1"
                    match = re.search(r'(Chapter|Unit|Lesson)\s+(\d+)[:\s]*(.*)', line, re.IGNORECASE)
                    if match:
                        title = match.group(3).strip() or f"Chapter {match.group(2)}"

                        # Save previous chapter
                        if len(chapters) > 0:
                            chapters[-1]['end_page'] = page_num

                        chapters.append({
                            'number': int(match.group(2)),
                            'title': title[:50],
                            'start_page': page_num + 1,
                            'end_page': total_pages  # Will be updated
                        })
                        break

            # Update last chapter end page
            if chapters and chapters[-1]['end_page'] == total_pages:
                pass  # Already correct

    except:
        pass

    return chapters if len(chapters) >= 3 else []


def smart_split_enhanced(total_pages, book_name):
    """Enhanced smart splitting"""
    # Determine sections based on content type and size
    if 'language' in book_name.lower() or 'telugu' in book_name.lower() or 'hindi' in book_name.lower():
        # Language books typically have many small lessons
        num_sections = min(12, max(8, total_pages // 15))
    elif total_pages <= 50:
        num_sections = 5
    elif total_pages <= 100:
        num_sections = 8
    elif total_pages <= 200:
        num_sections = 12
    else:
        num_sections = 15

    pages_per_section = total_pages // num_sections

    sections = []
    for i in range(num_sections):
        start = i * pages_per_section + 1
        end = (i + 1) * pages_per_section if i < num_sections - 1 else total_pages

        sections.append({
            'number': i + 1,
            'title': f'Chapter {i + 1}',
            'start_page': start,
            'end_page': end
        })

    return sections


def extract_text(pdf_path, start_page, end_page, use_ocr=False):
    """Extract text from page range"""
    if use_ocr and OCR_AVAILABLE:
        lang = 'tel+eng' if 'telugu' in pdf_path.name.lower() else \
               'hin+eng' if 'hindi' in pdf_path.name.lower() else 'eng'

        images = convert_from_path(pdf_path, dpi=200,
                                  first_page=start_page + 1,
                                  last_page=end_page + 1)
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
    """Parse grade and subject from filename"""
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


def main():
    """Main extraction function"""

    # Get all PDFs
    pdf_files = sorted(PDF_DIR.glob("grade*.pdf"))

    db = SessionLocal()

    # First, delete all single-chapter entries (they're not properly split)
    print("="*80)
    print("STEP 1: CLEANING UP SINGLE-CHAPTER ENTRIES")
    print("="*80)

    single_chapter_entries = db.query(NCERTTextbookContent).filter(
        NCERTTextbookContent.board == 'TELANGANA'
    ).all()

    to_delete = []
    for entry in single_chapter_entries:
        # Check if this book has only 1 chapter
        count = db.query(NCERTTextbookContent).filter(
            NCERTTextbookContent.board == 'TELANGANA',
            NCERTTextbookContent.grade == entry.grade,
            NCERTTextbookContent.subject == entry.subject
        ).count()

        if count == 1:
            to_delete.append(entry)

    print(f"Found {len(to_delete)} single-chapter entries to delete and re-extract")

    for entry in to_delete:
        db.delete(entry)

    db.commit()
    print(f"✅ Deleted {len(to_delete)} entries")
    print()

    # Now extract all books with enhanced detection
    print("="*80)
    print("STEP 2: ENHANCED CHAPTER EXTRACTION")
    print("="*80)
    print(f"Processing {len(pdf_files)} PDFs...")
    print()

    total_extracted = 0
    total_skipped = 0
    total_failed = 0

    for idx, pdf_path in enumerate(pdf_files, 1):
        print(f"\n{'='*80}")
        print(f"📖 [{idx}/{len(pdf_files)}] {pdf_path.name}")
        print(f"{'='*80}")

        try:
            grade, subject = parse_filename(pdf_path.name)
            use_ocr = 'telugu' in pdf_path.name.lower() or 'hindi' in pdf_path.name.lower()

            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)

            print(f"   Grade {grade}, Subject: {subject}, Pages: {total_pages}")

            # Try multiple detection methods
            chapters = []

            # Method 1: Advanced TOC parsing
            toc_page, toc_text = find_toc_advanced(pdf_path)
            if toc_page is not None:
                print(f"   ✅ TOC found (page {toc_page + 1})")
                chapters = parse_toc_enhanced(toc_text, total_pages)
                if len(chapters) >= 3:
                    print(f"   ✅ Extracted {len(chapters)} chapters from TOC")

            # Method 2: Content-based detection
            if len(chapters) < 3:
                print(f"   🔍 Trying content-based detection...")
                chapters = detect_chapters_from_content(pdf_path, total_pages)
                if len(chapters) >= 3:
                    print(f"   ✅ Detected {len(chapters)} chapters from content")

            # Method 3: Smart splitting
            if len(chapters) < 3:
                print(f"   📊 Using enhanced smart split...")
                chapters = smart_split_enhanced(total_pages, pdf_path.name)
                print(f"   ✅ Created {len(chapters)} sections")

            # Extract each chapter
            for chapter in chapters:
                ch_num = chapter['number']
                ch_title = chapter['title']
                start = chapter['start_page']
                end = chapter['end_page']

                print(f"      📄 Ch {ch_num}: {ch_title[:40]}... (p{start}-{end})", end=' ')

                # Check if exists
                existing = db.query(NCERTTextbookContent).filter(
                    NCERTTextbookContent.board == 'TELANGANA',
                    NCERTTextbookContent.grade == grade,
                    NCERTTextbookContent.subject == subject,
                    NCERTTextbookContent.chapter_number == ch_num
                ).first()

                if existing:
                    print("⏭️")
                    total_skipped += 1
                    continue

                try:
                    content = extract_text(pdf_path, start - 1, end - 1, use_ocr=use_ocr)

                    entry = NCERTTextbookContent(
                        board='TELANGANA',
                        grade=grade,
                        subject=subject,
                        chapter_number=ch_num,
                        chapter_name=ch_title,
                        content_type='textbook_chapter',
                        content_text=content,
                        extraction_method='enhanced_auto'
                    )

                    db.add(entry)
                    db.commit()

                    print(f"✅ ({len(content):,} chars)")
                    total_extracted += 1

                except Exception as e:
                    print(f"❌ {str(e)[:30]}")
                    total_failed += 1
                    db.rollback()

        except Exception as e:
            print(f"   ❌ Book error: {e}")
            continue

    db.close()

    print(f"\n{'='*80}")
    print("EXTRACTION COMPLETE!")
    print(f"{'='*80}")
    print(f"✅ Extracted: {total_extracted}")
    print(f"⏭️  Skipped: {total_skipped}")
    print(f"❌ Failed: {total_failed}")


if __name__ == "__main__":
    main()
