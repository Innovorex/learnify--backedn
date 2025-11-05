# NCERT Textbook Content Extraction Plan
## Extract Real Textbook Content for CBSE Syllabus (Grades 1-10)

**Date:** 2025-11-04
**Status:** 📋 **PLANNING PHASE - REVISED**
**Goal:** Extract actual NCERT textbook content (exact text, images, examples, exercises) for all CBSE topics

---

## 🎯 Executive Summary - REVISED APPROACH

### What We Have Now:
- ✅ Complete CBSE syllabus structure (46 subjects, 431 chapters, ~2000+ topics)
- ✅ Topic names and learning outcomes
- ✅ Unit and chapter organization

### What We Need to Extract:
- ❌ **Exact textbook content** (paragraphs, explanations as written in NCERT)
- ❌ **Textbook examples** (verbatim from NCERT books)
- ❌ **Textbook exercises** (exact questions from NCERT)
- ❌ **Diagrams and images** (from NCERT books)
- ❌ **Activity boxes and supplementary material**

### Source:
- **NCERT Official Textbooks** (ncert.nic.in)
- **PDF Format** - All textbooks freely available
- **Grades 1-10, All subjects**

---

## 📋 NEW STRATEGIC APPROACH

### **NCERT Content Extraction - Direct from Textbooks** ⭐⭐⭐ **RECOMMENDED**

**Why This Approach:**
- ✅ **100% Authentic** - Official government-approved content
- ✅ **Already Aligned** - Perfectly matches CBSE syllabus
- ✅ **Free & Legal** - NCERT content is in public domain for educational use
- ✅ **Complete** - All explanations, examples, exercises included
- ✅ **Quality Assured** - Created by expert educators

**Challenges:**
- ⚠️ Requires PDF extraction and OCR
- ⚠️ Manual cleanup and formatting needed
- ⚠️ Image extraction and storage
- ⚠️ Copyright compliance (educational fair use)

**Timeline:** 8-10 weeks for all grades
**Cost:** ₹2-3 lakhs (mostly manual effort)
**Quality:** ⭐⭐⭐⭐⭐ (Official NCERT content)

---

## 🚀 Implementation Plan - NCERT Extraction

---

## Phase 1: Setup & Infrastructure (Week 1)

### 1.1 Database Schema for Textbook Content
```sql
-- Textbook content storage
CREATE TABLE ncert_textbook_content (
    id SERIAL PRIMARY KEY,

    -- Linking to syllabus
    syllabus_topic_id INT,  -- Link to our syllabus database
    grade INT NOT NULL,
    subject VARCHAR(100),
    chapter_number INT,
    chapter_name VARCHAR(200),
    section_name VARCHAR(200),  -- Section within chapter

    -- Textbook metadata
    textbook_name VARCHAR(200),  -- e.g., "Mathematics Class 10"
    ncert_book_code VARCHAR(50), -- e.g., "JEMH1"
    page_start INT,
    page_end INT,

    -- Content (EXACT from textbook)
    content_type VARCHAR(50), -- 'explanation', 'example', 'exercise', 'activity', 'summary'
    content_text TEXT,  -- Extracted text (formatted)
    content_html TEXT,  -- HTML formatted version
    original_formatting_notes TEXT,  -- Bold, italic, special formatting

    -- Mathematical/Scientific content
    has_formulas BOOLEAN DEFAULT FALSE,
    formulas JSONB,  -- LaTeX or MathML format

    -- Visual content
    has_images BOOLEAN DEFAULT FALSE,
    images JSONB,  -- Array of image data
    has_diagrams BOOLEAN DEFAULT FALSE,
    diagrams JSONB,
    has_tables BOOLEAN DEFAULT FALSE,
    tables JSONB,

    -- Ordering
    sequence_order INT,  -- Order within chapter

    -- Metadata
    extraction_date TIMESTAMP DEFAULT NOW(),
    extraction_method VARCHAR(50), -- 'pdf_extract', 'ocr', 'manual'
    quality_check_status VARCHAR(20), -- 'pending', 'reviewed', 'approved'
    reviewed_by VARCHAR(100),

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Examples from textbook
CREATE TABLE ncert_examples (
    id SERIAL PRIMARY KEY,
    textbook_content_id INT REFERENCES ncert_textbook_content(id),

    example_number VARCHAR(20), -- e.g., "Example 1", "Example 2.3"
    example_title TEXT,  -- If any
    problem_statement TEXT,  -- Exact problem as in textbook
    solution TEXT,  -- Step-by-step solution
    solution_steps JSONB,  -- Structured steps

    has_images BOOLEAN,
    images JSONB,

    page_number INT,
    sequence_order INT
);

-- Exercises from textbook
CREATE TABLE ncert_exercises (
    id SERIAL PRIMARY KEY,
    textbook_content_id INT REFERENCES ncert_textbook_content(id),

    exercise_number VARCHAR(20), -- e.g., "Exercise 1.1", "Exercise 2.2"
    exercise_name TEXT,

    question_number VARCHAR(20), -- e.g., "1", "2(a)", "3(i)"
    question_text TEXT,  -- Exact question from textbook
    question_type VARCHAR(50), -- 'short', 'long', 'mcq', 'true_false', 'fill_blanks'

    hints TEXT,  -- If provided in textbook
    answer TEXT,  -- If answer key available
    solution TEXT,  -- If solution provided

    difficulty_indicated VARCHAR(20), -- If textbook marks it (optional, challenging, etc.)

    has_images BOOLEAN,
    images JSONB,

    page_number INT,
    marks INT,  -- If specified
    sequence_order INT
);

-- Images and diagrams
CREATE TABLE ncert_images (
    id SERIAL PRIMARY KEY,

    source_table VARCHAR(50), -- 'textbook_content', 'examples', 'exercises'
    source_id INT,

    image_type VARCHAR(50), -- 'diagram', 'photograph', 'illustration', 'chart', 'graph'
    image_url TEXT,  -- S3 or local storage path
    image_caption TEXT,  -- Caption from textbook
    image_description TEXT,  -- Alt text for accessibility

    original_page_number INT,
    image_format VARCHAR(10), -- 'png', 'jpg', 'svg'
    image_size_bytes INT,

    extracted_at TIMESTAMP DEFAULT NOW()
);

-- Activity boxes (Do This, Think, Discuss, etc.)
CREATE TABLE ncert_activities (
    id SERIAL PRIMARY KEY,
    textbook_content_id INT REFERENCES ncert_textbook_content(id),

    activity_type VARCHAR(50), -- 'think', 'discuss', 'do_this', 'try_this', 'project'
    activity_title TEXT,
    activity_description TEXT,
    instructions JSONB,  -- Step-by-step if provided

    materials_needed TEXT,  -- If specified
    estimated_time VARCHAR(50),  -- If specified

    page_number INT,
    sequence_order INT
);
```

### 1.2 Extraction Pipeline Setup
```python
# Project structure
ncert_extraction/
├── downloaders/
│   ├── download_ncert_pdfs.py       # Download all NCERT PDFs
│   └── pdf_catalog.json             # Catalog of all textbooks
├── extractors/
│   ├── pdf_text_extractor.py        # Extract text from PDFs
│   ├── image_extractor.py           # Extract images/diagrams
│   ├── formula_extractor.py         # Extract mathematical formulas
│   ├── table_extractor.py           # Extract tables
│   └── structure_parser.py          # Parse chapter/section structure
├── processors/
│   ├── content_formatter.py         # Format extracted content
│   ├── example_parser.py            # Parse examples
│   ├── exercise_parser.py           # Parse exercises
│   ├── activity_parser.py           # Parse activity boxes
│   └── image_processor.py           # Process and store images
├── validators/
│   ├── content_validator.py         # Validate extraction quality
│   ├── completeness_checker.py      # Check if all content extracted
│   └── manual_review_queue.py       # Flag items for manual review
└── storage/
    ├── database_loader.py           # Load into PostgreSQL
    └── image_storage.py             # Upload to S3/local storage
```

---

## Phase 2: NCERT PDF Acquisition (Week 1)

### 2.1 Download All NCERT Textbooks

**NCERT Official Sources:**
```
Primary Source: https://ncert.nic.in/textbook.php
Alternative: https://ncert.nic.in/pdf/
```

**Textbook Catalog (Grades 1-10):**

```python
NCERT_TEXTBOOKS = {
    # Grade 1
    "1": {
        "Mathematics": "https://ncert.nic.in/textbook/pdf/aemh1dd.pdf",
        "English - Marigold": "https://ncert.nic.in/textbook/pdf/aeen1dd.pdf",
        "Hindi - Rimjhim": "https://ncert.nic.in/textbook/pdf/aehn1dd.pdf",
        "EVS - Looking Around": "https://ncert.nic.in/textbook/pdf/aeev1dd.pdf"
    },

    # Grade 2
    "2": {
        "Mathematics": "https://ncert.nic.in/textbook/pdf/bemh1dd.pdf",
        "English - Marigold": "https://ncert.nic.in/textbook/pdf/been1dd.pdf",
        "Hindi - Rimjhim": "https://ncert.nic.in/textbook/pdf/behn1dd.pdf",
        "EVS - Looking Around": "https://ncert.nic.in/textbook/pdf/beev1dd.pdf"
    },

    # ... Similar for Grades 3-5

    # Grade 6
    "6": {
        "Mathematics": "https://ncert.nic.in/textbook/pdf/femh1dd.pdf",
        "Science": "https://ncert.nic.in/textbook/pdf/fesc1dd.pdf",
        "Social Science - History": "https://ncert.nic.in/textbook/pdf/fess1dd.pdf",
        "Social Science - Geography": "https://ncert.nic.in/textbook/pdf/fess2dd.pdf",
        "Social Science - Civics": "https://ncert.nic.in/textbook/pdf/fess3dd.pdf",
        "English - Honeysuckle": "https://ncert.nic.in/textbook/pdf/feeh1dd.pdf",
        "English - A Pact with the Sun": "https://ncert.nic.in/textbook/pdf/feeh2dd.pdf",
        "Hindi - Vasant": "https://ncert.nic.in/textbook/pdf/fehh1dd.pdf",
        "Hindi - Bal Ram Katha": "https://ncert.nic.in/textbook/pdf/fehh2dd.pdf"
    },

    # ... Similar for Grades 7-8

    # Grade 9
    "9": {
        "Mathematics": "https://ncert.nic.in/textbook/pdf/iemh1dd.pdf",
        "Science": "https://ncert.nic.in/textbook/pdf/iesc1dd.pdf",
        "Social Science - India and Contemporary World I": "https://ncert.nic.in/textbook/pdf/iess1dd.pdf",
        "Social Science - Contemporary India I": "https://ncert.nic.in/textbook/pdf/iess2dd.pdf",
        "Social Science - Democratic Politics I": "https://ncert.nic.in/textbook/pdf/iess3dd.pdf",
        "Social Science - Economics": "https://ncert.nic.in/textbook/pdf/iess4dd.pdf",
        "English - Beehive": "https://ncert.nic.in/textbook/pdf/ieeh1dd.pdf",
        "English - Moments": "https://ncert.nic.in/textbook/pdf/ieeh2dd.pdf",
        "Hindi - Sparsh": "https://ncert.nic.in/textbook/pdf/iehh1dd.pdf",
        "Hindi - Sanchayan": "https://ncert.nic.in/textbook/pdf/iehh2dd.pdf"
    },

    # Grade 10
    "10": {
        "Mathematics": "https://ncert.nic.in/textbook/pdf/jemh1dd.pdf",
        "Science": "https://ncert.nic.in/textbook/pdf/jesc1dd.pdf",
        "Social Science - India and Contemporary World II": "https://ncert.nic.in/textbook/pdf/jess1dd.pdf",
        "Social Science - Contemporary India II": "https://ncert.nic.in/textbook/pdf/jess2dd.pdf",
        "Social Science - Democratic Politics II": "https://ncert.nic.in/textbook/pdf/jess3dd.pdf",
        "Social Science - Understanding Economic Development": "https://ncert.nic.in/textbook/pdf/jess4dd.pdf",
        "English - First Flight": "https://ncert.nic.in/textbook/pdf/jeeh1dd.pdf",
        "English - Footprints without Feet": "https://ncert.nic.in/textbook/pdf/jeeh2dd.pdf",
        "Hindi - Sparsh": "https://ncert.nic.in/textbook/pdf/jehh1dd.pdf",
        "Hindi - Sanchayan": "https://ncert.nic.in/textbook/pdf/jehh2dd.pdf"
    }
}
```

**Download Script:**
```python
import requests
import os
from pathlib import Path

def download_all_ncert_pdfs():
    """
    Download all NCERT textbooks for Grades 1-10
    """

    base_dir = Path("ncert_textbooks")
    base_dir.mkdir(exist_ok=True)

    for grade, subjects in NCERT_TEXTBOOKS.items():
        grade_dir = base_dir / f"grade_{grade}"
        grade_dir.mkdir(exist_ok=True)

        for subject, url in subjects.items():
            filename = f"{subject.replace(' ', '_')}.pdf"
            filepath = grade_dir / filename

            if filepath.exists():
                print(f"✓ Already downloaded: {filename}")
                continue

            try:
                print(f"Downloading: Grade {grade} - {subject}...")
                response = requests.get(url, timeout=300)

                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"✓ Downloaded: {filename} ({len(response.content)} bytes)")
                else:
                    print(f"✗ Failed: {subject} (Status: {response.status_code})")

            except Exception as e:
                print(f"✗ Error downloading {subject}: {e}")

    print("\n✅ Download complete!")
```

**Deliverable:** All NCERT PDFs downloaded locally (~1-2 GB total)

---

## Phase 3: Content Extraction (Weeks 2-6)

### 3.1 Text Extraction from PDFs

**Tools:**
- **PyPDF2** / **pdfplumber** - Primary extraction
- **OCR (Tesseract)** - For scanned pages / images
- **pdf2image** - Convert PDFs to images for OCR

**Extraction Process:**
```python
import pdfplumber
from PIL import Image
import pytesseract

def extract_text_from_pdf(pdf_path):
    """
    Extract text from NCERT PDF with high accuracy
    """

    extracted_content = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):

            # Try direct text extraction first
            text = page.extract_text()

            if text and len(text.strip()) > 50:
                # Good text extraction
                extracted_content.append({
                    'page': page_num,
                    'text': text,
                    'method': 'direct',
                    'quality': 'high'
                })
            else:
                # Fall back to OCR
                image = page.to_image(resolution=300)
                pil_image = image.original

                # OCR with pytesseract
                ocr_text = pytesseract.image_to_string(
                    pil_image,
                    lang='eng+hin',  # English + Hindi
                    config='--psm 6'  # Assume uniform text block
                )

                extracted_content.append({
                    'page': page_num,
                    'text': ocr_text,
                    'method': 'ocr',
                    'quality': 'medium'
                })

    return extracted_content
```

### 3.2 Structure Parsing

**Identify Document Structure:**
```python
def parse_chapter_structure(extracted_text, textbook_metadata):
    """
    Parse NCERT textbook structure:
    - Chapter headings
    - Section headings
    - Subsections
    - Examples
    - Exercises
    - Activity boxes
    """

    structure = {
        'chapters': []
    }

    # Patterns for different elements
    patterns = {
        'chapter': r'^CHAPTER\s+(\d+)\s*\n\s*(.+)$',
        'section': r'^\d+\.\d+\s+(.+)$',
        'example': r'^Example\s+\d+\.?\d*\s*[:\-]?',
        'exercise': r'^EXERCISE\s+\d+\.\d+',
        'activity': r'^(TRY THIS|THINK|DISCUSS|DO THIS):?',
        'summary': r'^(SUMMARY|WHAT HAVE WE DISCUSSED)',
    }

    current_chapter = None
    current_section = None

    for page_data in extracted_text:
        text = page_data['text']
        lines = text.split('\n')

        for line in lines:
            # Detect chapter headings
            if re.match(patterns['chapter'], line, re.I):
                if current_chapter:
                    structure['chapters'].append(current_chapter)

                current_chapter = {
                    'chapter_number': extract_chapter_number(line),
                    'chapter_name': extract_chapter_name(line),
                    'start_page': page_data['page'],
                    'sections': [],
                    'content': []
                }

            # Detect sections
            elif re.match(patterns['section'], line):
                if current_chapter:
                    current_section = {
                        'section_name': line.strip(),
                        'start_page': page_data['page'],
                        'content': []
                    }
                    current_chapter['sections'].append(current_section)

            # Detect examples
            elif re.match(patterns['example'], line, re.I):
                # Parse example content
                example = extract_example(lines, current_index, page_data['page'])
                if current_section:
                    current_section['content'].append({
                        'type': 'example',
                        'content': example
                    })

            # Similar for exercises, activities, etc.

    return structure
```

### 3.3 Example Extraction

```python
def extract_examples(chapter_content, page_number):
    """
    Extract solved examples from textbook
    Format: Example number, problem, solution
    """

    examples = []

    # Pattern: "Example 1:" or "Example 2.1" etc.
    example_pattern = r'Example\s+(\d+\.?\d*)\s*[:\-]?\s*(.*?)(?=Example\s+\d+|EXERCISE|$)'

    matches = re.finditer(example_pattern, chapter_content, re.DOTALL | re.I)

    for match in matches:
        example_num = match.group(1)
        example_content = match.group(2).strip()

        # Separate problem and solution
        # Usually "Solution:" appears between them
        parts = example_content.split('Solution:', 1)

        if len(parts) == 2:
            problem = parts[0].strip()
            solution = parts[1].strip()
        else:
            # Sometimes it's implicit
            problem, solution = split_problem_solution(example_content)

        examples.append({
            'example_number': example_num,
            'problem_statement': problem,
            'solution': solution,
            'page_number': page_number
        })

    return examples
```

### 3.4 Exercise Extraction

```python
def extract_exercises(chapter_content, page_number):
    """
    Extract exercise questions from textbook
    """

    exercises = []

    # Pattern: "EXERCISE 1.1" or "Exercise 2.2"
    exercise_pattern = r'EXERCISE\s+(\d+\.\d+)(.*?)(?=EXERCISE\s+\d+|$)'

    matches = re.finditer(exercise_pattern, chapter_content, re.DOTALL | re.I)

    for match in matches:
        exercise_num = match.group(1)
        exercise_content = match.group(2).strip()

        # Extract individual questions
        # Usually numbered: "1.", "2.", etc.
        question_pattern = r'(\d+\.)\s+(.*?)(?=\n\d+\.|\Z)'

        questions = re.finditer(question_pattern, exercise_content, re.DOTALL)

        for q in questions:
            q_num = q.group(1).strip('.')
            q_text = q.group(2).strip()

            exercises.append({
                'exercise_number': exercise_num,
                'question_number': q_num,
                'question_text': q_text,
                'page_number': page_number
            })

    return exercises
```

### 3.5 Image & Diagram Extraction

```python
import fitz  # PyMuPDF

def extract_images_from_pdf(pdf_path, output_dir):
    """
    Extract all images and diagrams from NCERT PDF
    """

    pdf_document = fitz.open(pdf_path)
    extracted_images = []

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)

            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            # Save image
            image_filename = f"grade_{grade}_page_{page_num+1}_img_{img_index+1}.{image_ext}"
            image_path = output_dir / image_filename

            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)

            # Get image position and context
            image_rect = page.get_image_bbox(img[7])

            extracted_images.append({
                'filename': image_filename,
                'page_number': page_num + 1,
                'position': {
                    'x0': image_rect.x0,
                    'y0': image_rect.y0,
                    'x1': image_rect.x1,
                    'y1': image_rect.y1
                },
                'format': image_ext,
                'size_bytes': len(image_bytes)
            })

    return extracted_images
```

### 3.6 Formula Extraction (for Math/Science)

```python
def extract_formulas(text_content):
    """
    Extract mathematical formulas and convert to LaTeX
    """

    # Patterns for common mathematical notation
    formula_patterns = [
        r'([a-z])\s*=\s*([^,\.]+)',  # Simple equations
        r'\\frac\{.*?\}\{.*?\}',      # Fractions
        r'\^\{.*?\}',                  # Superscripts
        r'\_\{.*?\}',                  # Subscripts
    ]

    formulas = []

    for pattern in formula_patterns:
        matches = re.finditer(pattern, text_content)
        for match in matches:
            formulas.append({
                'original_text': match.group(0),
                'latex_format': convert_to_latex(match.group(0)),
                'position': match.start()
            })

    return formulas
```

**Timeline for Extraction:**
- Week 2: Grades 9-10 (Priority)
- Week 3: Grades 6-8
- Week 4-5: Grades 3-5
- Week 6: Grades 1-2

---

## Phase 4: Content Processing & Formatting (Weeks 6-7)

### 4.1 Clean and Format Content

```python
def clean_extracted_content(raw_content):
    """
    Clean up OCR errors, formatting issues
    """

    cleaned = raw_content

    # Fix common OCR errors
    ocr_corrections = {
        'l1': '11',
        '0ne': 'One',
        'tw0': 'two',
        # ... more corrections
    }

    for wrong, correct in ocr_corrections.items():
        cleaned = cleaned.replace(wrong, correct)

    # Fix spacing issues
    cleaned = re.sub(r'\s+', ' ', cleaned)

    # Fix broken words (hyphenation at line breaks)
    cleaned = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', cleaned)

    return cleaned
```

### 4.2 Link to Syllabus Database

```python
def link_textbook_to_syllabus(textbook_content, syllabus_db):
    """
    Link extracted textbook content to our existing syllabus structure
    """

    # For each chapter in textbook
    for chapter in textbook_content['chapters']:

        # Find matching chapter in syllabus database
        syllabus_chapter = find_syllabus_chapter(
            grade=textbook_content['grade'],
            subject=textbook_content['subject'],
            chapter_name=chapter['chapter_name']
        )

        if syllabus_chapter:
            # Link all content from this chapter
            for section in chapter['sections']:
                for content_item in section['content']:

                    # Find matching topic
                    topic = find_matching_topic(
                        section['section_name'],
                        syllabus_chapter['topics']
                    )

                    if topic:
                        # Store linkage
                        store_textbook_content(
                            syllabus_topic_id=topic['id'],
                            content=content_item
                        )
```

### 4.3 Quality Assurance Checks

```python
def validate_extraction_quality(extracted_content, original_pdf):
    """
    Validate that extraction is complete and accurate
    """

    checks = {
        'page_count_match': check_page_count(extracted_content, original_pdf),
        'all_chapters_found': check_all_chapters_extracted(extracted_content),
        'all_examples_found': check_examples_complete(extracted_content),
        'all_exercises_found': check_exercises_complete(extracted_content),
        'images_extracted': check_images_extracted(extracted_content),
        'text_quality': assess_text_quality(extracted_content),
        'formatting_preserved': check_formatting(extracted_content)
    }

    # Calculate quality score
    quality_score = sum(checks.values()) / len(checks) * 100

    if quality_score < 90:
        flag_for_manual_review(extracted_content, checks)

    return {
        'passed': quality_score >= 90,
        'score': quality_score,
        'checks': checks
    }
```

---

## Phase 5: Manual Review & Correction (Weeks 7-8)

### 5.1 Review Queue

**Items Requiring Manual Review:**
1. OCR quality < 85%
2. Complex diagrams/tables
3. Mathematical formulas (verification)
4. Hindi/regional language content
5. Special formatting (boxes, callouts)

### 5.2 Review Process

```python
# Review Dashboard
review_dashboard = {
    'total_items': 5000,
    'auto_extracted': 4200,
    'needs_review': 800,
    'reviewed': 300,
    'approved': 250,
    'pending': 500,

    'by_grade': {
        '10': {'pending': 50, 'approved': 150},
        '9': {'pending': 80, 'approved': 120},
        # ...
    },

    'by_issue_type': {
        'poor_ocr': 200,
        'complex_diagrams': 150,
        'formulas': 250,
        'tables': 100,
        'hindi_text': 100
    }
}
```

### 5.3 Manual Correction Tools

```
Web-based Review Interface:
- Show original PDF page side-by-side with extracted content
- Allow editing of extracted text
- Upload/replace images
- Mark as approved/needs-rework
- Assign to reviewers
```

**Team for Review:**
- 2-3 subject experts (part-time)
- 1 technical editor (formatting)
- 1 Hindi language expert

---

## Phase 6: Storage & Database Population (Week 9)

### 6.1 Batch Load to Database

```python
def populate_database_with_ncert_content():
    """
    Load all extracted and reviewed content into database
    """

    for grade in range(1, 11):
        for subject in get_subjects_for_grade(grade):

            # Get extracted content
            textbook_content = load_extracted_content(grade, subject)

            # Validate
            if validate_content(textbook_content):

                # Populate tables
                for chapter in textbook_content['chapters']:

                    # Main content
                    for section in chapter['sections']:
                        content_id = insert_textbook_content(section)

                        # Examples
                        for example in section['examples']:
                            insert_example(content_id, example)

                        # Exercises
                        for exercise in section['exercises']:
                            insert_exercise(content_id, exercise)

                        # Activities
                        for activity in section['activities']:
                            insert_activity(content_id, activity)

                    # Images
                    for image in chapter['images']:
                        upload_image_to_storage(image)
                        insert_image_metadata(content_id, image)

                print(f"✓ Loaded: Grade {grade} - {subject}")
```

### 6.2 Image Storage

```
Options:
1. AWS S3 (recommended for production)
2. Local file storage (for development)
3. CDN (for fast delivery)

Structure:
/ncert_images/
  ├─ grade_1/
  │   ├─ mathematics/
  │   │   ├─ chapter_1/
  │   │   │   ├─ img_001.png
  │   │   │   └─ diagram_002.png
  │   │   └─ chapter_2/
  │   └─ english/
  └─ grade_10/
      └─ ...
```

---

## Phase 7: API Development & Integration (Week 10)

### 7.1 Content Delivery APIs

```python
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/textbook/content/{grade}/{subject}/{chapter}")
async def get_chapter_content(grade: int, subject: str, chapter: str):
    """
    Get complete textbook content for a chapter
    Returns: explanations, examples, exercises as in NCERT book
    """

    content = db.query(NCERTTextbookContent).filter(
        NCERTTextbookContent.grade == grade,
        NCERTTextbookContent.subject == subject,
        NCERTTextbookContent.chapter_name.ilike(f"%{chapter}%")
    ).all()

    if not content:
        raise HTTPException(status_code=404, detail="Chapter not found")

    return {
        'chapter_name': content[0].chapter_name,
        'textbook_name': content[0].textbook_name,
        'sections': format_sections(content),
        'examples': get_examples_for_chapter(content[0].id),
        'exercises': get_exercises_for_chapter(content[0].id),
        'activities': get_activities_for_chapter(content[0].id),
        'images': get_images_for_chapter(content[0].id)
    }

@router.get("/textbook/example/{example_id}")
async def get_example(example_id: int):
    """
    Get a specific solved example from textbook
    """
    example = db.query(NCERTExamples).filter(
        NCERTExamples.id == example_id
    ).first()

    if not example:
        raise HTTPException(status_code=404, detail="Example not found")

    return {
        'example_number': example.example_number,
        'problem_statement': example.problem_statement,
        'solution': example.solution,
        'solution_steps': example.solution_steps,
        'images': get_images_for_example(example_id)
    }

@router.get("/textbook/exercise/{grade}/{subject}/{exercise_number}")
async def get_exercise(grade: int, subject: str, exercise_number: str):
    """
    Get all questions from a specific exercise
    (e.g., Exercise 1.1, Exercise 2.3)
    """
    exercises = db.query(NCERTExercises).filter(
        NCERTExercises.grade == grade,
        NCERTExercises.subject == subject,
        NCERTExercises.exercise_number == exercise_number
    ).order_by(NCERTExercises.sequence_order).all()

    return {
        'exercise_number': exercise_number,
        'total_questions': len(exercises),
        'questions': [format_question(q) for q in exercises]
    }

@router.get("/textbook/search")
async def search_textbook_content(
    keyword: str,
    grade: Optional[int] = None,
    subject: Optional[str] = None
):
    """
    Search across all textbook content
    """
    query = db.query(NCERTTextbookContent)

    # Apply filters
    if grade:
        query = query.filter(NCERTTextbookContent.grade == grade)
    if subject:
        query = query.filter(NCERTTextbookContent.subject.ilike(f"%{subject}%"))

    # Search in text
    query = query.filter(
        NCERTTextbookContent.content_text.ilike(f"%{keyword}%")
    )

    results = query.limit(50).all()

    return {
        'keyword': keyword,
        'results_count': len(results),
        'results': [format_search_result(r) for r in results]
    }
```

---

## 📊 Resource Requirements - REVISED

### Team Requirements:
| Role | Number | Time Commitment | Cost (INR/month) |
|------|--------|----------------|------------------|
| Python Developer (Extraction) | 1 | Full-time (10 weeks) | ₹70,000 - ₹1,00,000 |
| Data Entry / QA Specialist | 2 | Full-time (6 weeks) | ₹30,000 each |
| Subject Experts (Review) | 3 | Part-time (6 weeks, 10 hrs/week) | ₹20,000 each |
| Technical Editor | 1 | Part-time (4 weeks) | ₹25,000 |
| Backend Developer (APIs) | 1 | Full-time (2 weeks) | ₹60,000 - ₹90,000 |
| **Total** | **8** | **10 weeks** | **₹2,50,000 - ₹3,50,000** |

### Technology Costs:
| Item | Cost (INR) |
|------|-----------|
| OCR Software (if needed) | ₹10,000 |
| Image Storage (S3/CDN) | ₹5,000/month |
| Database & Hosting | ₹10,000/month |
| PDF Processing Tools | ₹5,000 |
| **Total** | **₹30,000 - ₹50,000** |

### **Grand Total: ₹2,80,000 - ₹4,00,000**

**Note:** No AI API costs since we're extracting directly from PDFs!

---

## 📅 Timeline - REVISED

```
Week 1: Setup & PDF Download
  ├─ Day 1-2: Database schema design
  ├─ Day 3-4: Extraction pipeline setup
  ├─ Day 5-7: Download all NCERT PDFs

Week 2: Extract Grades 9-10 (Priority)
  ├─ Mathematics, Science (both grades)
  ├─ Social Science (all 4 books per grade)
  └─ English, Hindi

Week 3: Extract Grades 6-8
  ├─ All subjects, all grades
  └─ Initial QA checks

Week 4-5: Extract Grades 3-5
  ├─ Mathematics, English, Hindi, EVS
  └─ Process and format content

Week 6: Extract Grades 1-2
  ├─ All subjects
  └─ Complete initial extraction

Week 7-8: Manual Review & Correction
  ├─ Review flagged items
  ├─ Correct OCR errors
  ├─ Verify formulas and diagrams
  └─ Approve content

Week 9: Database Population
  ├─ Batch load all content
  ├─ Upload images to storage
  └─ Create linkages to syllabus

Week 10: API Development & Testing
  ├─ Build content delivery APIs
  ├─ Integration testing
  └─ User acceptance testing

Total: 10 weeks
```

---

## 🎯 What You'll Get - EXACT NCERT CONTENT

### For Each Topic/Chapter:

```json
{
  "grade": 10,
  "subject": "Mathematics",
  "chapter": "Real Numbers",

  "textbook_content": {
    "introduction": "Exact text from NCERT book...",
    "sections": [
      {
        "section_name": "1.1 Introduction",
        "content": "Exact explanatory text from textbook...",
        "page_numbers": [1, 2]
      },
      {
        "section_name": "1.2 Euclid's Division Lemma",
        "content": "Exact text explaining the concept...",
        "page_numbers": [3, 4, 5]
      }
    ]
  },

  "examples": [
    {
      "example_number": "Example 1",
      "problem": "Exact problem statement from book...",
      "solution": "Exact step-by-step solution from book...",
      "page": 5
    },
    {
      "example_number": "Example 2",
      "problem": "...",
      "solution": "...",
      "page": 7
    }
  ],

  "exercises": {
    "Exercise 1.1": [
      {
        "question_number": "1",
        "question": "Exact question from textbook...",
        "page": 10
      },
      {
        "question_number": "2",
        "question": "...",
        "page": 10
      }
    ],
    "Exercise 1.2": [...]
  },

  "images": [
    {
      "image_url": "https://cdn.../grade10_math_ch1_img1.png",
      "caption": "Figure 1.1 from textbook",
      "page": 4
    }
  ],

  "activities": [
    {
      "type": "TRY THIS",
      "description": "Exact activity text from textbook...",
      "page": 6
    }
  ]
}
```

**This is 100% authentic NCERT content - exactly as students read in their textbooks!**

---

## 🚦 Legal Considerations

### Copyright & Fair Use:

✅ **ALLOWED (Educational Fair Use):**
- Extracting for educational platform
- Non-commercial educational use
- Attributing source (NCERT)
- Not distributing PDFs themselves

⚠️ **BEST PRACTICES:**
- Add "Source: NCERT Class X Mathematics Textbook" on every page
- Link to original NCERT website
- Use for teaching purposes only
- Don't sell the extracted content separately
- Don't claim copyright over NCERT content

**NCERT Policy:**
NCERT textbooks are publicly funded and meant for educational purposes. Extracting content for a teaching platform (non-commercial educational use) typically falls under fair use.

**Recommendation:** Add clear attribution and consider reaching out to NCERT for explicit permission if scaling commercially.

---

## 📈 Success Metrics

### Extraction Completeness:
- ✅ 100% of chapters extracted
- ✅ 100% of examples extracted
- ✅ 100% of exercises extracted
- ✅ 90%+ of images extracted
- ✅ 100% of syllabus topics mapped

### Quality Metrics:
- ✅ 95%+ text extraction accuracy
- ✅ 90%+ formula extraction accuracy
- ✅ 100% manual review for Grades 9-10
- ✅ 80%+ manual review for Grades 6-8
- ✅ Sample review for Grades 1-5

### Performance Metrics:
- ✅ API response time <500ms
- ✅ Image loading <2 seconds
- ✅ Full chapter load <3 seconds

---

## 💡 Advantages of This Approach

| Aspect | NCERT Extraction | AI Generation |
|--------|------------------|---------------|
| **Authenticity** | ⭐⭐⭐⭐⭐ 100% official | ⭐⭐⭐ AI-generated |
| **Student Trust** | ⭐⭐⭐⭐⭐ Exact textbook | ⭐⭐⭐ May differ |
| **Accuracy** | ⭐⭐⭐⭐⭐ Govt-approved | ⭐⭐⭐⭐ Needs review |
| **Exam Alignment** | ⭐⭐⭐⭐⭐ Perfect | ⭐⭐⭐⭐ Good |
| **Cost** | ⭐⭐⭐⭐ One-time effort | ⭐⭐⭐ Ongoing API costs |
| **Time** | ⭐⭐⭐ 10 weeks | ⭐⭐⭐⭐ 4-5 weeks |
| **Copyright** | ⭐⭐⭐⭐ Fair use | ⭐⭐⭐⭐⭐ No issues |

---

## 🎓 Recommended Next Steps

1. **Approve Budget & Timeline**
   - ₹3-4 lakhs total
   - 10 weeks timeline
   - Team of 8 people

2. **Start with Pilot (Week 1-2)**
   - Extract Grade 10 Mathematics completely
   - Test extraction quality
   - Validate database structure
   - If successful, proceed with all grades

3. **Prioritize Grades**
   - **Phase 1:** Grades 9-10 (Weeks 2-3)
   - **Phase 2:** Grades 6-8 (Weeks 4-5)
   - **Phase 3:** Grades 1-5 (Weeks 6-7)

4. **Setup Infrastructure**
   - Database tables
   - Extraction pipeline
   - Review dashboard
   - Image storage

---

## 📞 Questions to Answer:

1. **Budget:** Approved for ₹3-4 lakhs?
2. **Timeline:** 10 weeks acceptable?
3. **Team:** Can hire 8 people (mix of full-time & part-time)?
4. **Priority:** Start with all grades or Grades 9-10 first?
5. **Quality:** What % manual review acceptable?
6. **Storage:** AWS S3 or local storage for images?
7. **Copyright:** Comfortable with educational fair use?

---

**Status:** 📋 **REVISED PLAN READY - NCERT EXTRACTION APPROACH**

**This approach gives you 100% authentic NCERT textbook content - exactly what students study from!**

*Ready to execute when approved.*
