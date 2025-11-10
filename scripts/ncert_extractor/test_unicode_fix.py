#!/usr/bin/env python3
"""
Test if we can find a pattern to decode the Chanakya font encoding
by analyzing the actual glyphs
"""
import pdfplumber
from collections import Counter

test_pdf = "../../../ncert_pdfs/grade10_hindi_sparsh_ch07.pdf"

with pdfplumber.open(test_pdf) as pdf:
    page = pdf.pages[0]
    
    # Get all characters with their properties
    chars_data = []
    if hasattr(page, 'chars'):
        for char in page.chars[:100]:
            chars_data.append({
                'text': char.get('text', ''),
                'font': char.get('fontname', ''),
                'size': char.get('size', 0)
            })
    
    print("Sample character analysis:")
    for i, c in enumerate(chars_data[:20]):
        print(f"{i:2d}. '{c['text']}' (U+{ord(c['text']):04X}) Font: {c['font']}")
    
    # Try to find if there's a pattern
    print("\nMost common characters:")
    text = page.extract_text()
    counter = Counter(text[:200])
    for char, count in counter.most_common(15):
        print(f"'{char}' (U+{ord(char):04X}): {count} times")
        
