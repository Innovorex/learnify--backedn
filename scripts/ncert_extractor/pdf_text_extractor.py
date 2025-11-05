#!/usr/bin/env python3
"""
NCERT PDF Text Extractor
Extract text content, examples, exercises, and images from NCERT PDFs
"""

import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

import pdfplumber
import PyPDF2
import fitz  # PyMuPDF
import re
from pathlib import Path
from database import SessionLocal
from models import (NCERTTextbookContent, NCERTExample, NCERTExercise,
                   NCERTImage, NCERTActivity, NCERTPDFSource)
import json


class NCERTTextExtractor:
    """Extract text and content from NCERT PDF"""

    def __init__(self, pdf_path, grade, subject):
        self.pdf_path = Path(pdf_path)
        self.grade = grade
        self.subject = subject
        self.db = SessionLocal()

    def extract_full_text(self):
        """Extract all text from PDF using pdfplumber"""
        print(f"\n📖 Extracting text from: {self.pdf_path.name}")

        full_text = []
        page_texts = {}

        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                total_pages = len(pdf.pages)
                print(f"   Total pages: {total_pages}")

                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        page_texts[page_num] = text
                        full_text.append(text)

                    if page_num % 10 == 0:
                        print(f"   Processed: {page_num}/{total_pages} pages", end='\r')

                print(f"\n   ✅ Extracted text from {len(page_texts)} pages")

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return None, {}

        return "\n\n".join(full_text), page_texts

    def identify_chapters(self, page_texts):
        """Identify chapter boundaries from page texts"""
        chapters = []

        chapter_pattern = r'CHAPTER\s+(\d+)\s*\n\s*([A-Z][A-Z\s]+)'
        alternative_pattern = r'(\d+)\s*\.\s*([A-Z][A-Z\s]+)\s*$'

        for page_num, text in page_texts.items():
            lines = text.split('\n')

            for i, line in enumerate(lines):
                # Match "CHAPTER 1 REAL NUMBERS"
                match = re.search(chapter_pattern, line)
                if match:
                    chapter_num = int(match.group(1))
                    chapter_name = match.group(2).strip().title()
                    chapters.append({
                        'chapter_number': chapter_num,
                        'chapter_name': chapter_name,
                        'start_page': page_num
                    })
                    print(f"   📑 Found Chapter {chapter_num}: {chapter_name} (Page {page_num})")

        # Set end pages
        for i in range(len(chapters) - 1):
            chapters[i]['end_page'] = chapters[i + 1]['start_page'] - 1

        if chapters:
            chapters[-1]['end_page'] = max(page_texts.keys())

        print(f"\n   ✅ Identified {len(chapters)} chapters")
        return chapters

    def extract_examples(self, text, chapter_name, page_num):
        """Extract solved examples from text"""
        examples = []

        # Pattern: "Example 1" or "Example 1 :" followed by problem and solution
        example_pattern = r'(?:Example|EXAMPLE)\s+(\d+\.?\d*)\s*[:.]?\s*(.*?)(?=(?:Example|EXAMPLE|EXERCISE|$))'

        matches = re.finditer(example_pattern, text, re.DOTALL | re.IGNORECASE)

        for match in matches:
            example_num = match.group(1)
            content = match.group(2).strip()

            if len(content) > 50:  # Ensure it's substantial content
                # Try to split into problem and solution
                solution_markers = ['Solution', 'SOLUTION', 'Answer', 'ANSWER']
                problem_statement = content
                solution_text = ""

                for marker in solution_markers:
                    if marker in content:
                        parts = content.split(marker, 1)
                        problem_statement = parts[0].strip()
                        solution_text = parts[1].strip() if len(parts) > 1 else ""
                        break

                example = NCERTExample(
                    grade=self.grade,
                    subject=self.subject,
                    chapter_name=chapter_name,
                    example_number=f"Example {example_num}",
                    problem_statement=problem_statement[:2000],  # Limit length
                    solution_text=solution_text[:4000],
                    page_number=page_num
                )
                examples.append(example)

        return examples

    def extract_exercises(self, text, chapter_name, page_num):
        """Extract exercise questions from text"""
        exercises = []

        # Pattern for exercises: "EXERCISE 1.1", "EXERCISE 1.2"
        exercise_pattern = r'(?:EXERCISE|Exercise)\s+(\d+\.?\d*)'
        exercise_match = re.search(exercise_pattern, text, re.IGNORECASE)

        if exercise_match:
            exercise_num = exercise_match.group(1)

            # Extract questions after the exercise header
            # Pattern: "1.", "2.", etc. at start of line
            question_pattern = r'^\s*(\d+)\.\s+(.+?)(?=^\s*\d+\.|$)'

            questions = re.finditer(question_pattern, text, re.MULTILINE | re.DOTALL)

            for q_match in questions:
                q_num = q_match.group(1)
                q_text = q_match.group(2).strip()

                if len(q_text) > 10:  # Ensure it's a real question
                    exercise = NCERTExercise(
                        grade=self.grade,
                        subject=self.subject,
                        chapter_name=chapter_name,
                        exercise_number=f"Exercise {exercise_num}",
                        question_number=q_num,
                        question_text=q_text[:2000],
                        page_number=page_num
                    )
                    exercises.append(exercise)

        return exercises

    def extract_images(self, save_dir="/home/learnify/lt/learnify-teach/backend/ncert_images"):
        """Extract images from PDF using PyMuPDF"""
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)

        images = []

        try:
            doc = fitz.open(self.pdf_path)
            total_images = 0

            for page_num in range(len(doc)):
                page = doc[page_num]
                image_list = page.get_images()

                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]

                    # Save image
                    filename = f"grade_{self.grade}_{self.subject.replace(' ', '_')}_p{page_num + 1}_img{img_index + 1}.{image_ext}"
                    image_path = save_dir / filename

                    with open(image_path, "wb") as img_file:
                        img_file.write(image_bytes)

                    # Create database record
                    image_record = NCERTImage(
                        grade=self.grade,
                        subject=self.subject,
                        chapter_name="Unknown",  # Will be linked later
                        image_type="diagram",
                        file_path=str(image_path),
                        file_format=image_ext,
                        file_size_kb=len(image_bytes) // 1024,
                        page_number=page_num + 1
                    )
                    images.append(image_record)
                    total_images += 1

            print(f"   ✅ Extracted {total_images} images")

        except Exception as e:
            print(f"   ❌ Image extraction error: {str(e)}")

        return images

    def process_pdf(self):
        """Main processing pipeline"""
        print(f"\n{'='*80}")
        print(f"🔍 Processing: Grade {self.grade} - {self.subject}")
        print(f"{'='*80}")

        # Extract full text
        full_text, page_texts = self.extract_full_text()
        if not full_text:
            return False

        # Identify chapters
        chapters = self.identify_chapters(page_texts)

        # Extract content for each chapter
        all_examples = []
        all_exercises = []

        for chapter in chapters:
            chapter_num = chapter['chapter_number']
            chapter_name = chapter['chapter_name']
            start_page = chapter['start_page']
            end_page = chapter['end_page']

            print(f"\n📖 Processing Chapter {chapter_num}: {chapter_name}")

            # Get chapter text
            chapter_text = "\n\n".join([
                page_texts.get(p, "") for p in range(start_page, end_page + 1)
            ])

            # Store main content
            content = NCERTTextbookContent(
                board="CBSE",
                grade=self.grade,
                subject=self.subject,
                chapter_number=chapter_num,
                chapter_name=chapter_name,
                content_type="explanation",
                content_text=chapter_text[:10000],  # Store first 10K chars
                page_start=start_page,
                page_end=end_page,
                extraction_method="pdf_extract"
            )
            self.db.add(content)

            # Extract examples
            examples = self.extract_examples(chapter_text, chapter_name, start_page)
            all_examples.extend(examples)
            print(f"   📝 Extracted {len(examples)} examples")

            # Extract exercises
            exercises = self.extract_exercises(chapter_text, chapter_name, start_page)
            all_exercises.extend(exercises)
            print(f"   ✏️  Extracted {len(exercises)} exercises")

        # Save all to database
        for example in all_examples:
            self.db.add(example)

        for exercise in all_exercises:
            self.db.add(exercise)

        # Extract images
        print(f"\n🖼️  Extracting images...")
        images = self.extract_images()
        for image in images:
            self.db.add(image)

        # Update PDF source record
        pdf_record = self.db.query(NCERTPDFSource).filter(
            NCERTPDFSource.grade == self.grade,
            NCERTPDFSource.subject == self.subject
        ).first()

        if pdf_record:
            pdf_record.extraction_status = "completed"
            pdf_record.total_content_items = len(chapters)
            pdf_record.total_examples = len(all_examples)
            pdf_record.total_exercises = len(all_exercises)
            pdf_record.total_images = len(images)

        # Commit all changes
        self.db.commit()

        print(f"\n{'='*80}")
        print(f"✅ Extraction Complete!")
        print(f"   Chapters: {len(chapters)}")
        print(f"   Examples: {len(all_examples)}")
        print(f"   Exercises: {len(all_exercises)}")
        print(f"   Images: {len(images)}")
        print(f"{'='*80}\n")

        self.db.close()
        return True


def main():
    """CLI interface"""
    if len(sys.argv) < 4:
        print("\nUsage: python3 pdf_text_extractor.py <pdf_path> <grade> <subject>")
        print("\nExample:")
        print("  python3 pdf_text_extractor.py ../ncert_pdfs/test_grade_9_math.pdf 9 Mathematics\n")
        return

    pdf_path = sys.argv[1]
    grade = int(sys.argv[2])
    subject = sys.argv[3]

    extractor = NCERTTextExtractor(pdf_path, grade, subject)
    extractor.process_pdf()


if __name__ == "__main__":
    main()
