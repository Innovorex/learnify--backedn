#!/usr/bin/env python3
"""
Batch Extract Hindi PDFs with OCR
==================================
Extracts all available Grade 9-10 Hindi PDFs using Tesseract OCR
and saves them to the database with proper Unicode Devanagari.
"""

import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

import os
import re
from pathlib import Path
from typing import List, Tuple
import pytesseract
from pdf2image import convert_from_path
from database import SessionLocal
from models import NCERTTextbookContent

# Chapter name mappings
CHAPTER_NAMES = {
    # Grade 9 - Kshitij
    ("grade9", "kshitij", 1): "दो बैलों की कथा",
    ("grade9", "kshitij", 2): "ल्हासा की ओर",
    ("grade9", "kshitij", 3): "उपभोक्तावाद की संस्कृति",
    ("grade9", "kshitij", 4): "साँवले सपनों की याद",
    ("grade9", "kshitij", 5): "नाना साहब की पुत्री देवी मैना को भस्म कर दिया गया",
    ("grade9", "kshitij", 6): "प्रेमचंद के फटे जूते",
    ("grade9", "kshitij", 7): "मेरे बचपन के दिन",
    ("grade9", "kshitij", 8): "एक कुत्ता और एक मैना",
    ("grade9", "kshitij", 9): "साखियाँ एवं सबद",
    ("grade9", "kshitij", 10): "वाख",
    ("grade9", "kshitij", 11): "सवैये",
    ("grade9", "kshitij", 12): "कैदी और कोकिला",
    ("grade9", "kshitij", 13): "ग्राम श्री",

    # Grade 9 - Kritika
    ("grade9", "kritika", 1): "इस जल प्रलय में",
    ("grade9", "kritika", 2): "मेरे संग की औरतें",
    ("grade9", "kritika", 3): "रीढ़ की हड्डी",

    # Grade 9 - Sparsh
    ("grade9", "sparsh", 1): "दुःख का अधिकार",
    ("grade9", "sparsh", 2): "एवरेस्ट: मेरी शिखर यात्रा",
    ("grade9", "sparsh", 3): "तुम कब जाओगे, अतिथि",
    ("grade9", "sparsh", 4): "वैज्ञानिक चेतना के वाहक चंद्रशेखर वेंकट रामन",
    ("grade9", "sparsh", 5): "धर्म की आड़",
    ("grade9", "sparsh", 6): "शुक्रतारे के समान",
    ("grade9", "sparsh", 7): "रीढ़ की हड्डी",
    ("grade9", "sparsh", 8): "दोहे",
    ("grade9", "sparsh", 9): "आदमीनामा",
    ("grade9", "sparsh", 10): "एक फूल की चाह",

    # Grade 9 - Sanchayan
    ("grade9", "sanchayan", 1): "गिल्लू",
    ("grade9", "sanchayan", 2): "स्मृति",
    ("grade9", "sanchayan", 3): "कल्लू कुम्हार की उनाकोटी",

    # Grade 10 - Kshitij
    ("grade10", "kshitij", 1): "सूरदास के पद",
    ("grade10", "kshitij", 2): "राम-लक्ष्मण-परशुराम संवाद",
    ("grade10", "kshitij", 3): "सवैया और कवित्त",
    ("grade10", "kshitij", 4): "आत्मकथ्य",
    ("grade10", "kshitij", 5): "उत्साह और अट नहीं रही है",
    ("grade10", "kshitij", 6): "यह दंतुरित मुस्कान और फसल",
    ("grade10", "kshitij", 7): "छाया मत छूना",
    ("grade10", "kshitij", 8): "कन्यादान",
    ("grade10", "kshitij", 9): "संगतकार",
    ("grade10", "kshitij", 10): "नेताजी का चश्मा",
    ("grade10", "kshitij", 11): "बालगोबिन भगत",
    ("grade10", "kshitij", 12): "लखनवी अंदाज",

    # Grade 10 - Kritika
    ("grade10", "kritika", 1): "माता का आंचल",
    ("grade10", "kritika", 2): "जॉर्ज पंचम की नाक",
    ("grade10", "kritika", 3): "साना-साना हाथ जोड़ि",

    # Grade 10 - Sparsh
    ("grade10", "sparsh", 1): "साखी",
    ("grade10", "sparsh", 2): "पद",
    ("grade10", "sparsh", 3): "दोहे",
    ("grade10", "sparsh", 4): "मनुष्यता",
    ("grade10", "sparsh", 5): "पर्वत प्रदेश में पावस",
    ("grade10", "sparsh", 6): "मधुर-मधुर मेरे दीपक जल",
    ("grade10", "sparsh", 7): "तोप",
    ("grade10", "sparsh", 8): "कर चले हम फिदा",
    ("grade10", "sparsh", 9): "आत्मत्राण",
    ("grade10", "sparsh", 10): "बड़े भाई साहब",
    ("grade10", "sparsh", 11): "डायरी का एक पन्ना",
    ("grade10", "sparsh", 12): "तताँरा-वामीरो कथा",
    ("grade10", "sparsh", 13): "तीसरी कसम के शिल्पकार शैलेंद्र",
    ("grade10", "sparsh", 14): "गिरगिट",
}


def extract_text_from_pdf_ocr(pdf_path: str, dpi: int = 300) -> str:
    """Extract text from PDF using OCR"""
    images = convert_from_path(pdf_path, dpi=dpi)
    all_text = []

    for i, image in enumerate(images, 1):
        text = pytesseract.image_to_string(image, lang='hin')
        all_text.append(text)

    return "\n\n".join(all_text)


def parse_filename(filename: str) -> Tuple[str, str, int]:
    """Parse PDF filename to extract grade, book, chapter number"""
    # Example: grade9_hindi_kshitij_ch01.pdf
    match = re.match(r'grade(\d+)_hindi_([a-z]+)_ch(\d+)\.pdf', filename)
    if match:
        grade = f"grade{match.group(1)}"
        book = match.group(2)
        chapter = int(match.group(3))
        return grade, book, chapter
    return None, None, None


def batch_extract_hindi():
    """Extract all Hindi PDFs and save to database"""
    pdf_dir = Path("/home/learnify/lt/learnify-teach/ncert_pdfs")
    db = SessionLocal()

    # Get all Hindi PDFs
    hindi_pdfs = sorted(pdf_dir.glob("grade*_hindi_*.pdf"))
    grade_9_10_pdfs = [p for p in hindi_pdfs if 'grade9' in p.name or 'grade10' in p.name]

    print(f"🚀 Starting OCR Batch Extraction")
    print(f"=" * 70)
    print(f"Total PDFs to process: {len(grade_9_10_pdfs)}")
    print(f"=" * 70)

    total = len(grade_9_10_pdfs)
    success = 0
    failed = 0

    for idx, pdf_path in enumerate(grade_9_10_pdfs, 1):
        grade_str, book, chapter_num = parse_filename(pdf_path.name)

        if not grade_str or not book or not chapter_num:
            print(f"\n❌ [{idx}/{total}] Skipping {pdf_path.name} - invalid filename")
            failed += 1
            continue

        grade = int(grade_str.replace("grade", ""))
        subject = f"Hindi_{book.capitalize()}"

        # Get chapter name
        chapter_name = CHAPTER_NAMES.get((grade_str, book, chapter_num), f"Chapter {chapter_num}")

        print(f"\n{'='*70}")
        print(f"📚 [{idx}/{total}] Grade {grade} - {subject} - Ch{chapter_num}")
        print(f"   Chapter: {chapter_name}")
        print(f"   PDF: {pdf_path.name}")
        print(f"{'='*70}")

        try:
            # Extract text using OCR
            print(f"🔍 Running OCR (DPI: 300)...")
            content_text = extract_text_from_pdf_ocr(str(pdf_path), dpi=300)

            # Verify quality
            dev_chars = sum(1 for c in content_text if '\u0900' <= c <= '\u097F')
            total_chars = len([c for c in content_text if c.strip()])

            if total_chars == 0:
                print(f"❌ No text extracted - skipping")
                failed += 1
                continue

            purity = dev_chars / total_chars * 100
            print(f"✅ OCR Complete: {purity:.1f}% Devanagari ({len(content_text)} chars)")

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
                    grade=grade,
                    subject=subject,
                    chapter_number=chapter_num,
                    chapter_name=chapter_name,
                    content_text=content_text
                )
                db.add(new_content)

            db.commit()
            success += 1

            print(f"✅ Saved to database")
            print(f"   Preview: {content_text[:100]}...")

        except Exception as e:
            print(f"❌ Error: {e}")
            db.rollback()
            failed += 1
            continue

    db.close()

    print(f"\n{'='*70}")
    print(f"📊 BATCH EXTRACTION COMPLETE")
    print(f"{'='*70}")
    print(f"Total PDFs: {total}")
    print(f"✅ Successfully extracted: {success}")
    print(f"❌ Failed: {failed}")
    print(f"Success rate: {success/total*100:.1f}%")
    print(f"{'='*70}")


if __name__ == "__main__":
    batch_extract_hindi()
