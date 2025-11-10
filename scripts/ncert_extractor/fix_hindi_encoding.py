#!/usr/bin/env python3
"""
Fix Hindi Encoding - Convert Chanakya/Kruti Dev to Unicode
===========================================================
This script uses a comprehensive mapping to convert legacy Chanakya font
encoding (used in NCERT Hindi PDFs) to proper Unicode Devanagari.

Based on standard Kruti Dev/Chanakya to Unicode mapping tables.
"""

import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

import pdfplumber
from database import SessionLocal
from models import NCERTTextbookContent
from sqlalchemy import or_

# Comprehensive Chanakya to Unicode mapping
# Based on Kruti Dev font standard
CHAN_TO_UNICODE = {
    # Consonants - Single
    'd': 'क', 'D': 'क्', '[k': 'ख', '[': 'ख्', 'x': 'ग', 'X': 'ग्',
    '?k': 'घ', '?': 'घ्', 'ª': 'ङ',
    'p': 'च', 'P': 'च्', 'N': 'छ', 't': 'ज', 'T': 'ज्',
    '÷': 'झ', '×': 'झ्', '´': 'ञ',
    'V': 'ट', 'B': 'ठ', 'M': 'ड', '¡': 'ढ', '.': 'ण',
    'r': 'त', 'R': 'त्', 'F': 'थ', 'n': 'द', 'N': 'द्',
    '/k': 'ध', '\\': 'ध्', 'u': 'न', 'U': 'न्',
    'i': 'प', 'I': 'प्', 'iQ': 'फ', 'Q': 'फ्', 'c': 'ब', 'C': 'ब्',
    'Hk': 'भ', 'H': 'भ्', 'e': 'म', 'E': 'म्',
    ';': 'य', 'Y': 'य्', 'j': 'र', 'J': 'र्', 'y': 'ल', 'Y': 'ल्',
    'o': 'व', 'O': 'व्', '\'k': 'श', '\"': 'ष', 'l': 'स', 'L': 'स्',
    'g': 'ह', 'G': 'ह्', 'K': 'ज्ञ', 'Kk': 'ज्ञा',

    # Vowel signs (matras)
    'k': 'ा', 'h': 'ि', 'Z': 'ी', 'q': 'ु', 'w': 'ू',
    's': 'े', 'S': 'ै', 'ksa': 'ों', 'kas': 'ौ',

    # Independent vowels
    'v': 'अ', 'vk': 'आ', 'b': 'इ', 'bZ': 'ई',
    'mq': 'उ', 'Å': 'ऊ', '½': 'ऋ',

    # Special characters
    '&': 'ं', 'a': '्', 'A': 'ः', '~': 'ऽ',
    '।': '।', '॥': '॥',

    # Common word patterns (most frequent)
    'dks': 'को', 'dk': 'का', 'dh': 'की', 'ds': 'के', 'osQ': 'के',
    'esa': 'में', 'ls': 'से', 'us': 'ने', 'ij': 'पर', 'Fkk': 'था',
    'Fks': 'थे', 'Fkh': 'थी', 'gS': 'है', 'gSa': 'हैं', 'ugha': 'नहीं',
    'vkSj': 'और', 'rFkk': 'तथा', 'vFkok': 'अथवा',
}

def convert_chanakya_to_unicode(text):
    """
    Convert Chanakya encoded text to Unicode Devanagari

    Uses multi-pass strategy:
    1. Replace longer patterns first (words)
    2. Replace individual characters
    3. Handle special combinations
    """
    if not text or len(text) == 0:
        return text

    result = text

    # Sort by length (longest first) to match longer patterns before shorter ones
    sorted_mappings = sorted(CHAN_TO_UNICODE.items(), key=lambda x: -len(x[0]))

    for chanakya, unicode_char in sorted_mappings:
        result = result.replace(chanakya, unicode_char)

    return result

def test_with_sample():
    """Test conversion with actual PDF sample"""
    test_pdf = "../../../ncert_pdfs/grade10_hindi_sparsh_ch07.pdf"

    print("Testing Chanakya to Unicode conversion:")
    print("=" * 60)

    with pdfplumber.open(test_pdf) as pdf:
        page = pdf.pages[0]
        orig_text = page.extract_text()

        print(f"\nOriginal (Chanakya): {orig_text[:150]}")

        converted = convert_chanakya_to_unicode(orig_text)

        print(f"\nConverted (Unicode): {converted[:150]}")

        # Check if Devanagari is present
        devanagari_count = sum(1 for c in converted if '\u0900' <= c <= '\u097F')
        total_chars = len([c for c in converted if c.strip()])

        print(f"\nDevanagari characters: {devanagari_count}/{total_chars}")
        print(f"Conversion rate: {devanagari_count/total_chars*100:.1f}%")

        if devanagari_count > total_chars * 0.5:
            print("\n✅ SUCCESS! Conversion working!")
            return True
        else:
            print("\n❌ Conversion needs improvement")
            return False

def fix_database_content():
    """Fix all corrupted Hindi content in database"""
    db = SessionLocal()

    try:
        # Get all Hindi content
        hindi_contents = db.query(NCERTTextbookContent).filter(
            or_(
                NCERTTextbookContent.subject.ilike('%hindi%'),
                NCERTTextbookContent.subject.ilike('%kshitij%'),
                NCERTTextbookContent.subject.ilike('%kritika%'),
                NCERTTextbookContent.subject.ilike('%sparsh%')
            )
        ).all()

        print(f"\nFound {len(hindi_contents)} Hindi content pieces to fix")
        print("=" * 60)

        fixed_count = 0

        for content in hindi_contents:
            # Check if already has Devanagari
            has_devanagari = any('\u0900' <= c <= '\u097F' for c in content.content_text[:100])

            if not has_devanagari:
                # Convert from Chanakya to Unicode
                old_text = content.content_text
                new_text = convert_chanakya_to_unicode(old_text)

                # Verify conversion worked
                has_dev_after = any('\u0900' <= c <= '\u097F' for c in new_text[:100])

                if has_dev_after:
                    content.content_text = new_text
                    fixed_count += 1

                    if fixed_count <= 3:
                        print(f"\n✅ Fixed Ch{content.chapter_number} ({content.subject}):")
                        print(f"   Before: {old_text[:80]}...")
                        print(f"   After:  {new_text[:80]}...")

        # Commit changes
        db.commit()

        print(f"\n{'='*60}")
        print(f"✅ Fixed {fixed_count}/{len(hindi_contents)} content pieces")
        print(f"{'='*60}")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Hindi Encoding Fix Tool")
    print("=" * 60)

    # First test with sample
    success = test_with_sample()

    if success:
        print("\n\nReady to fix database content.")
        response = input("Proceed with database fix? (yes/no): ")

        if response.lower() == 'yes':
            fix_database_content()
    else:
        print("\n⚠️  Conversion not accurate enough. Need to improve mapping.")
