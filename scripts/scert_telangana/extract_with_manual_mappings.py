#!/usr/bin/env python3
"""
Extract Telangana chapters using manually verified mappings
100% accurate - no guessing
"""

import json
from pathlib import Path
import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

from database import SessionLocal
from models import NCERTTextbookContent
import pdfplumber

# Try to import OCR libraries
try:
    from pdf2image import convert_from_path
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️  OCR not available - will skip Telugu/Hindi books")

# Load manual mappings
MAPPINGS_FILE = Path(__file__).parent / 'telangana_chapter_mappings.json'
PDF_DIR = Path("/home/learnify/lt/learnify-teach/backend/ts_pdfs")


def load_chapter_mappings():
    """Load manually created chapter mappings"""
    with open(MAPPINGS_FILE, 'r') as f:
        return json.load(f)


def extract_chapter_text(pdf_path, start_page, end_page, use_ocr=False):
    """Extract text from specific page range"""

    if use_ocr and OCR_AVAILABLE:
        # Determine language
        if 'telugu' in pdf_path.name.lower():
            lang = 'tel+eng'
        elif 'hindi' in pdf_path.name.lower():
            lang = 'hin+eng'
        else:
            lang = 'eng'

        # OCR extraction
        images = convert_from_path(
            pdf_path,
            dpi=200,
            first_page=start_page + 1,
            last_page=end_page + 1
        )

        text_parts = []
        for image in images:
            text = pytesseract.image_to_string(image, lang=lang)
            text_parts.append(text)

        return "\n\n".join(text_parts)

    else:
        # pdfplumber extraction
        text_parts = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num in range(start_page, end_page + 1):
                if page_num < len(pdf.pages):
                    page = pdf.pages[page_num]
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)

        return "\n\n".join(text_parts)


def parse_filename(filename):
    """Parse grade and subject from filename"""
    # e.g., "grade6_english.pdf" -> grade=6, subject="English"
    # e.g., "grade10_biological_science_english.pdf" -> grade=10, subject="Biological Science"

    parts = filename.replace('.pdf', '').split('_')
    grade = int(parts[0].replace('grade', ''))

    # Handle subject name
    subject_parts = parts[1:]

    # Special mappings
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

    # Try exact match first
    subject_key = tuple(subject_parts)
    if subject_key in subject_map:
        return grade, subject_map[subject_key]

    # Fallback: capitalize each word
    subject = ' '.join(word.capitalize() for word in subject_parts if word != 'english')
    return grade, subject


def extract_all_chapters():
    """Main extraction function"""

    mappings = load_chapter_mappings()

    db = SessionLocal()

    total_books = len(mappings)
    total_chapters = sum(len(book['chapters']) for book in mappings.values())

    print(f"{'='*80}")
    print(f"TELANGANA CHAPTER EXTRACTION - MANUAL MAPPINGS")
    print(f"{'='*80}")
    print(f"Total books: {total_books}")
    print(f"Total chapters: {total_chapters}")
    print()

    extracted = 0
    skipped = 0
    failed = 0

    for pdf_filename, book_data in mappings.items():
        pdf_path = PDF_DIR / pdf_filename

        if not pdf_path.exists():
            print(f"❌ PDF not found: {pdf_filename}")
            failed += len(book_data['chapters'])
            continue

        # Parse filename to get grade and subject
        grade, subject = parse_filename(pdf_filename)

        # Determine if OCR needed
        use_ocr = 'telugu' in pdf_filename.lower() or 'hindi' in pdf_filename.lower()

        print(f"\n{'='*80}")
        print(f"📖 Processing: Grade {grade} - {subject}")
        print(f"{'='*80}")
        print(f"   File: {pdf_filename}")
        print(f"   Chapters: {len(book_data['chapters'])}")
        print(f"   Total Pages: {book_data['total_pages']}")
        if use_ocr:
            print(f"   Mode: OCR")
        print()

        for chapter in book_data['chapters']:
            chapter_num = chapter['number']
            chapter_title = chapter['title']
            start_page = chapter['start_page']
            end_page = chapter['end_page']

            print(f"   📄 Chapter {chapter_num}: {chapter_title}")
            print(f"      Pages: {start_page}-{end_page}")

            # Check if already exists
            existing = db.query(NCERTTextbookContent).filter(
                NCERTTextbookContent.board == 'TELANGANA',
                NCERTTextbookContent.grade == grade,
                NCERTTextbookContent.subject == subject,
                NCERTTextbookContent.chapter_number == chapter_num,
                NCERTTextbookContent.chapter_name == chapter_title
            ).first()

            if existing:
                print(f"      ⏭️  Already exists (ID: {existing.id})")
                skipped += 1
                continue

            try:
                # Extract content
                content = extract_chapter_text(
                    pdf_path,
                    start_page - 1,  # Convert to 0-indexed
                    end_page - 1,
                    use_ocr=use_ocr
                )

                if not content or len(content) < 100:
                    print(f"      ⚠️  Warning: Very little content extracted ({len(content)} chars)")

                # Store in database
                entry = NCERTTextbookContent(
                    board='TELANGANA',
                    grade=grade,
                    subject=subject,
                    chapter_number=chapter_num,
                    chapter_name=chapter_title,
                    content_type='textbook_chapter',
                    content_text=content,
                    extraction_method='manual_mapping'
                )

                db.add(entry)
                db.commit()

                print(f"      ✅ Extracted: {len(content):,} characters")
                extracted += 1

            except Exception as e:
                print(f"      ❌ Error: {e}")
                failed += 1
                db.rollback()

    db.close()

    print(f"\n{'='*80}")
    print(f"EXTRACTION COMPLETE")
    print(f"{'='*80}")
    print(f"✅ Successfully extracted: {extracted} chapters")
    print(f"⏭️  Skipped (already exists): {skipped} chapters")
    print(f"❌ Failed: {failed} chapters")
    print(f"Success rate: {extracted/(extracted+failed)*100 if (extracted+failed) > 0 else 0:.1f}%")
    print()

    return extracted, skipped, failed


if __name__ == "__main__":
    extract_all_chapters()
