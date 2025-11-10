#!/usr/bin/env python3
"""
Improved Chapter Name Extractor
Fixes OCR artifacts and extracts proper chapter names from NCERT PDFs
"""

import re
import pdfplumber
from pathlib import Path


def clean_ocr_artifacts(text):
    """Remove OCR artifacts like repeated characters"""
    # Remove patterns like "Rrrrr" (5+ repeated chars)
    cleaned = re.sub(r'([A-Za-z])\1{4,}', lambda m: m.group(1), text)

    # Remove excessive punctuation
    cleaned = re.sub(r'([?!.]){3,}', lambda m: m.group(1), cleaned)

    # Remove standalone single letters separated by spaces
    cleaned = re.sub(r'\b([A-Z])\s+([A-Z])\s+([A-Z])\s', '', cleaned)

    return cleaned.strip()


def extract_chapter_name_improved(pdf_path, chapter_number=None):
    """
    Extract chapter name from PDF with improved logic

    Handles:
    - OCR artifacts
    - Multiple name formats
    - Special characters
    - Mixed case
    """

    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Check first 3 pages for chapter name
            for page_num in range(min(3, len(pdf.pages))):
                page = pdf.pages[page_num]
                text = page.extract_text()

                if not text:
                    continue

                lines = text.split('\n')

                # Strategy 1: Look for "CHAPTER X" pattern
                for i, line in enumerate(lines[:20]):  # First 20 lines
                    line = line.strip()

                    # Pattern: "CHAPTER 1" or "Chapter 1"
                    chapter_match = re.search(r'(?:CHAPTER|Chapter)\s+(\d+)', line, re.IGNORECASE)
                    if chapter_match:
                        # Next line(s) likely contain chapter name
                        chapter_name_parts = []
                        for j in range(i+1, min(i+5, len(lines))):
                            next_line = lines[j].strip()

                            # Skip empty lines
                            if not next_line or len(next_line) < 3:
                                continue

                            # Skip lines that are likely headers/footers
                            if any(keyword in next_line.lower() for keyword in ['ncert', 'page', 'mathematics', 'science']):
                                if len(chapter_name_parts) > 0:  # Already found some name
                                    break
                                continue

                            # This looks like part of chapter name
                            if len(next_line) > 3 and len(next_line) < 100:
                                chapter_name_parts.append(next_line)

                            # Stop if we have enough
                            if len(chapter_name_parts) >= 2 or len(' '.join(chapter_name_parts)) > 15:
                                break

                        if chapter_name_parts:
                            raw_name = ' '.join(chapter_name_parts)
                            cleaned = clean_ocr_artifacts(raw_name)

                            # Title case and remove extra spaces
                            cleaned = ' '.join(cleaned.split()).title()

                            # Validate: not too short, not corrupted
                            if len(cleaned) >= 5 and not re.search(r'([A-Z])\1{3,}', cleaned):
                                return cleaned

                # Strategy 2: Look for large uppercase text (chapter title)
                for i, line in enumerate(lines[:15]):
                    line = line.strip()

                    # Potential chapter name:
                    # - Uppercase
                    # - Not too short (>5 chars)
                    # - Not too long (<80 chars)
                    # - Doesn't contain common header words
                    if (len(line) > 5 and len(line) < 80 and
                        line.isupper() and
                        not any(word in line for word in ['NCERT', 'PAGE', 'CHAPTER', 'EXERCISE'])):

                        # Clean and validate
                        cleaned = clean_ocr_artifacts(line)

                        # Remove chapter numbers at start/end
                        cleaned = re.sub(r'^\d+\s*', '', cleaned)
                        cleaned = re.sub(r'\s*\d+$', '', cleaned)

                        if len(cleaned) >= 5:
                            # Check if it's not corrupted (no excessive repeated chars)
                            if not re.search(r'([A-Z])\1{3,}', cleaned):
                                return cleaned.title()

                # Strategy 3: Use filename as fallback
                if chapter_number:
                    # Try to extract from filename pattern
                    filename = Path(pdf_path).stem

                    # Pattern like: "gemh101" -> "Grade X Math Chapter 1"
                    # Pattern like: "iesc102" -> "Grade 9 Science Chapter 2"

                    # For now, return a descriptive name
                    return f"Chapter {chapter_number}"

    except Exception as e:
        print(f"Error extracting chapter name from {pdf_path}: {e}")

    return "Unknown Chapter"


def get_official_chapter_names():
    """
    Mapping of grade/subject/chapter to official NCERT chapter names
    Based on official NCERT textbooks
    """

    official_names = {
        # Grade 10 Mathematics
        (10, 'Mathematics', 1): 'Real Numbers',
        (10, 'Mathematics', 2): 'Polynomials',
        (10, 'Mathematics', 3): 'Pair of Linear Equations in Two Variables',
        (10, 'Mathematics', 4): 'Quadratic Equations',
        (10, 'Mathematics', 5): 'Arithmetic Progressions',
        (10, 'Mathematics', 6): 'Triangles',
        (10, 'Mathematics', 7): 'Coordinate Geometry',
        (10, 'Mathematics', 8): 'Introduction to Trigonometry',
        (10, 'Mathematics', 9): 'Some Applications of Trigonometry',
        (10, 'Mathematics', 10): 'Circles',
        (10, 'Mathematics', 11): 'Constructions',
        (10, 'Mathematics', 12): 'Areas Related to Circles',
        (10, 'Mathematics', 13): 'Surface Areas and Volumes',
        (10, 'Mathematics', 14): 'Statistics',
        (10, 'Mathematics', 15): 'Probability',

        # Grade 10 Science
        (10, 'Science', 1): 'Chemical Reactions and Equations',
        (10, 'Science', 2): 'Acids, Bases and Salts',
        (10, 'Science', 3): 'Metals and Non-metals',
        (10, 'Science', 4): 'Carbon and its Compounds',
        (10, 'Science', 5): 'Periodic Classification of Elements',
        (10, 'Science', 6): 'Life Processes',
        (10, 'Science', 7): 'Control and Coordination',
        (10, 'Science', 8): 'How do Organisms Reproduce?',
        (10, 'Science', 9): 'Heredity and Evolution',
        (10, 'Science', 10): 'Light - Reflection and Refraction',
        (10, 'Science', 11): 'Human Eye and Colourful World',
        (10, 'Science', 12): 'Electricity',
        (10, 'Science', 13): 'Magnetic Effects of Electric Current',

        # Grade 9 Science
        (9, 'Science', 1): 'Matter in Our Surroundings',
        (9, 'Science', 2): 'Is Matter Around Us Pure?',
        (9, 'Science', 3): 'Atoms and Molecules',
        (9, 'Science', 4): 'Structure of the Atom',
        (9, 'Science', 5): 'The Fundamental Unit of Life',
        (9, 'Science', 6): 'Tissues',
        (9, 'Science', 7): 'Diversity in Living Organisms',
        (9, 'Science', 8): 'Motion',
        (9, 'Science', 9): 'Force and Laws of Motion',
        (9, 'Science', 10): 'Gravitation',
        (9, 'Science', 11): 'Work and Energy',
        (9, 'Science', 12): 'Sound',
        (9, 'Science', 13): 'Why Do We Fall Ill',
        (9, 'Science', 14): 'Natural Resources',
        (9, 'Science', 15): 'Improvement in Food Resources',

        # Grade 9 Social Science
        (9, 'Social Science', 1): 'The French Revolution',
        (9, 'Social Science', 2): 'Socialism in Europe and the Russian Revolution',
        (9, 'Social Science', 3): 'Nazism and the Rise of Hitler',
        (9, 'Social Science', 4): 'Forest Society and Colonialism',
        (9, 'Social Science', 5): 'Pastoralists in the Modern World',
        (9, 'Social Science', 6): 'Climate',
        (9, 'Social Science', 7): 'Population',
        (9, 'Social Science', 8): 'Drainage',

        # Add more as needed...
    }

    return official_names


# Test function
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 improved_chapter_extractor.py <pdf_path> [chapter_number]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    chapter_num = int(sys.argv[2]) if len(sys.argv) > 2 else None

    name = extract_chapter_name_improved(pdf_path, chapter_num)
    print(f"\n✅ Extracted Chapter Name: {name}\n")
