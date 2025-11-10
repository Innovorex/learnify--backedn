#!/usr/bin/env python3
"""
Test Hindi Question Generation
===============================
Tests if Hindi questions are being generated correctly from NCERT content.
"""

import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

from database import SessionLocal
from models import NCERTTextbookContent
from services.ai_question_generator_v2 import AIQuestionGeneratorV2

def test_hindi_question_generation():
    """Test Hindi question generation with actual NCERT content"""

    db = SessionLocal()

    # Get a Grade 10 Hindi chapter
    hindi_chapter = db.query(NCERTTextbookContent).filter(
        NCERTTextbookContent.grade == 10,
        NCERTTextbookContent.subject.ilike('%hindi%')
    ).first()

    if not hindi_chapter:
        print("❌ No Hindi chapter found in database")
        db.close()
        return False

    print("=" * 70)
    print("HINDI QUESTION GENERATION TEST")
    print("=" * 70)
    print(f"\n📚 Testing with:")
    print(f"   Grade: {hindi_chapter.grade}")
    print(f"   Subject: {hindi_chapter.subject}")
    print(f"   Chapter: {hindi_chapter.chapter_number} - {hindi_chapter.chapter_name}")
    print(f"   Content length: {len(hindi_chapter.content_text)} characters")

    # Check content quality
    dev_chars = sum(1 for c in hindi_chapter.content_text if '\u0900' <= c <= '\u097F')
    total_chars = len([c for c in hindi_chapter.content_text if c.strip()])
    content_purity = dev_chars / total_chars * 100 if total_chars > 0 else 0

    print(f"   Content Devanagari: {content_purity:.1f}%")
    print(f"   Content preview: {hindi_chapter.content_text[:100]}...")

    # Create AI generator
    print(f"\n🤖 Generating 3 MCQ questions in Hindi...")
    print("=" * 70)

    generator = AIQuestionGeneratorV2()

    # Prepare content
    ncert_content = {
        'cleaned_content': hindi_chapter.content_text[:4000],
        'topics': ['हिंदी साहित्य', 'कविता', 'कहानी'],
        'key_terms': ['भाषा', 'साहित्य', 'कविता', 'लेखक', 'रचना'],
        'key_concepts': ['साहित्यिक विश्लेषण', 'काव्य सौंदर्य', 'भाषा कौशल']
    }

    try:
        questions = generator._generate_mcq(
            ncert_content=ncert_content,
            count=3,
            grade=10,
            subject="Hindi",
            chapter=hindi_chapter.chapter_name or "Unknown Chapter",
            language="Hindi"
        )

        if not questions:
            print("❌ No questions generated")
            db.close()
            return False

        print(f"\n✅ Generated {len(questions)} questions")
        print("=" * 70)

        # Display questions
        all_question_text = ""
        for i, q in enumerate(questions, 1):
            question_text = q.get('question_text', 'N/A')
            explanation = q.get('explanation', 'N/A')
            options = q.get('options', [])

            all_question_text += question_text + " " + explanation + " "
            for opt in options:
                all_question_text += opt.get('option_text', '') + " "

            print(f"\n📝 प्रश्न {i}:")
            if question_text != 'N/A':
                print(f"   {question_text}")
            else:
                print(f"   ⚠️ Question text missing")

            print(f"\n   विकल्प:")
            for j, opt in enumerate(options, 1):
                is_correct = "✓" if opt.get('is_correct') else " "
                opt_text = opt.get('option_text', 'N/A')
                print(f"     [{is_correct}] {chr(64+j)}) {opt_text}")

            if explanation != 'N/A':
                print(f"\n   व्याख्या: {explanation[:150]}...")

        # Analyze Hindi quality
        dev_q = sum(1 for c in all_question_text if '\u0900' <= c <= '\u097F')
        total_q = len([c for c in all_question_text if c.strip()])

        if total_q > 0:
            question_purity = dev_q / total_q * 100

            print("\n" + "=" * 70)
            print(f"📊 QUALITY ANALYSIS:")
            print("=" * 70)
            print(f"   Input Content Devanagari: {content_purity:.1f}%")
            print(f"   Generated Questions Devanagari: {question_purity:.1f}%")
            print(f"   Total Devanagari characters: {dev_q}/{total_q}")

            if question_purity >= 50:
                print(f"\n   ✅ SUCCESS! Questions generated in Hindi ({question_purity:.1f}% Devanagari)")
                success = True
            elif question_purity >= 30:
                print(f"\n   ⚠️ PARTIAL SUCCESS: Questions have {question_purity:.1f}% Hindi")
                print(f"      (May have some English mixed in)")
                success = True
            else:
                print(f"\n   ❌ FAILURE: Questions mostly in English ({question_purity:.1f}% Hindi)")
                success = False

            # Additional checks
            if question_purity < content_purity:
                print(f"\n   ⚠️ NOTE: Question purity ({question_purity:.1f}%) lower than content ({content_purity:.1f}%)")
                print(f"      This is normal - AI may use some English technical terms")

            db.close()
            return success
        else:
            print("\n❌ No text in questions to analyze")
            db.close()
            return False

    except Exception as e:
        print(f"\n❌ Error generating questions: {e}")
        import traceback
        traceback.print_exc()
        db.close()
        return False


if __name__ == "__main__":
    print("\n")
    success = test_hindi_question_generation()
    print("\n" + "=" * 70)

    if success:
        print("✅ HINDI QUESTION GENERATION IS WORKING!")
        print("\nYou can now:")
        print("  1. Create Hindi assessments via the UI")
        print("  2. Questions will be generated in Hindi automatically")
        print("  3. Students can take tests in proper Hindi")
    else:
        print("❌ HINDI QUESTION GENERATION NEEDS ATTENTION")
        print("\nTroubleshooting:")
        print("  1. Check if Hindi content exists in database")
        print("  2. Verify content has Devanagari script (>80%)")
        print("  3. Check AI API configuration")

    print("=" * 70 + "\n")

    sys.exit(0 if success else 1)
