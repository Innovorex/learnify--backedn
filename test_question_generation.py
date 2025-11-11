#!/usr/bin/env python3
"""
Test script to verify question generation with Claude Haiku fallback
"""
import sys
import os
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import asyncio
from services.openrouter import generate_mcqs

async def test_question_generation():
    """Test question generation for Subject Knowledge module"""

    print("="*80)
    print("TESTING QUESTION GENERATION WITH CLAUDE HAIKU FALLBACK")
    print("="*80)

    # Mock teacher profile
    profile = {
        "education": "B.Ed, M.A",
        "grades_teaching": "6,7,8",
        "subjects_teaching": "Mathematics, Science",
        "experience_years": 5
    }

    module_name = "Subject Knowledge & Content Expertise"
    board = "CBSE"
    state = "Telangana"

    print(f"\nTest Parameters:")
    print(f"  Module: {module_name}")
    print(f"  Board: {board}")
    print(f"  State: {state}")
    print(f"  Grades: {profile['grades_teaching']}")
    print(f"  Subjects: {profile['subjects_teaching']}")
    print(f"\nGenerating 5 questions...\n")
    print("-"*80)

    try:
        # Generate questions
        questions = await generate_mcqs(
            profile=profile,
            module_name=module_name,
            board=board,
            n_questions=5,
            state=state,
            difficulty="medium",
            db_session=None
        )

        print(f"\n{'='*80}")
        print(f"RESULTS")
        print(f"{'='*80}")

        if questions and len(questions) > 0:
            print(f"✅ SUCCESS! Generated {len(questions)} questions\n")

            for i, q in enumerate(questions, 1):
                print(f"Question {i}:")
                print(f"  Q: {q.get('question', 'N/A')}")
                print(f"  Options: {q.get('options', [])}")
                print(f"  Correct: {q.get('correct_answer', 'N/A')}")
                print()
        else:
            print("❌ FAILED! No questions generated")
            return False

        print("="*80)
        print("✅ TEST PASSED - Question generation is working!")
        print("="*80)
        return True

    except Exception as e:
        print(f"\n{'='*80}")
        print(f"❌ TEST FAILED - Exception occurred")
        print(f"{'='*80}")
        print(f"Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_question_generation())
    sys.exit(0 if result else 1)
