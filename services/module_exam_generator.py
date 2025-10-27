"""
Module Exam Generator Service
Generates AI-powered exam questions for career progression course modules
"""

import os
import json
import re
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from models import CourseModule, ModuleTopic, ModuleExamQuestion

# Use existing OpenRouter setup
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-8b-instruct:free")


def generate_module_exam_questions(
    module: CourseModule,
    db: Session,
    n_questions: int = 25,
    force_regenerate: bool = False
) -> List[Dict]:
    """
    Generate exam questions for a module using AI

    Args:
        module: CourseModule object
        db: Database session
        n_questions: Number of questions to generate (default 25)
        force_regenerate: If True, regenerate even if questions exist

    Returns:
        List of question dictionaries
    """

    # Check if questions already exist for this module
    if not force_regenerate:
        existing_questions = db.query(ModuleExamQuestion).filter(
            ModuleExamQuestion.module_id == module.id
        ).all()

        if existing_questions and len(existing_questions) >= n_questions:
            print(f"[EXAM] Using existing {len(existing_questions)} questions for Module {module.module_number}")
            return [
                {
                    "id": q.id,
                    "question": q.question,
                    "options": json.loads(q.options_json),
                    "correct_answer": q.correct_answer,
                    "difficulty": q.difficulty
                }
                for q in existing_questions[:n_questions]
            ]

    print(f"[EXAM] Generating {n_questions} new questions for Module {module.module_number}: {module.module_name}")

    # Get topics for this module
    topics = db.query(ModuleTopic).filter(
        ModuleTopic.module_id == module.id
    ).order_by(ModuleTopic.topic_number).all()

    if not topics:
        print(f"[ERROR] No topics found for module {module.id}")
        return []

    # Build context from topics
    topic_context = "\n".join([
        f"{i+1}. {topic.topic_name}"
        for i, topic in enumerate(topics)
    ])

    # Calculate difficulty distribution (40% medium, 60% hard)
    n_medium = int(n_questions * 0.4)
    n_hard = n_questions - n_medium

    # Build AI prompt
    prompt = f"""Generate {n_questions} multiple-choice questions for a B.Ed (Bachelor of Education) examination.

**Module Details:**
Module {module.module_number}: {module.module_name}
Description: {module.description}

**Topics Covered:**
{topic_context}

**Question Requirements:**
- Total Questions: {n_questions}
- Difficulty Distribution:
  * {n_medium} Medium difficulty questions (40%)
  * {n_hard} Hard difficulty questions (60%)
- Question Level: B.Ed (teacher education level)
- Focus: Deep understanding of educational concepts, theories, and applications
- Include scenario-based questions where appropriate
- Questions should test teachers' professional knowledge

**Format Requirements:**
- Each question must have exactly 4 options (A, B, C, D)
- Options should be labeled as "A) ...", "B) ...", "C) ...", "D) ..."
- One option must be clearly correct
- Other options should be plausible distractors
- Questions should be clear and unambiguous

**Return ONLY a JSON array in this exact format:**
[
  {{
    "question": "What is the primary focus of Piaget's theory of cognitive development?",
    "options": ["A) Social interaction", "B) Stages of mental development", "C) Behavioral conditioning", "D) Language acquisition"],
    "correct_answer": "B",
    "difficulty": "medium"
  }},
  {{
    "question": "In Vygotsky's sociocultural theory, what is the Zone of Proximal Development?",
    "options": ["A) The range of tasks a child can do independently", "B) The difference between what a learner can do with and without guidance", "C) The age range for cognitive development stages", "D) The cultural context of learning"],
    "correct_answer": "B",
    "difficulty": "hard"
  }}
]

Generate {n_questions} questions now. Return ONLY the JSON array, no other text."""

    # Call AI using existing infrastructure
    try:
        from services.openrouter import generate_subject_knowledge_questions_ai_requests
        response_content = generate_subject_knowledge_questions_ai_requests(prompt)

        if response_content.startswith("Error") or response_content.startswith("Exception"):
            print(f"[ERROR] AI API call failed: {response_content}")
            return []

        # Parse JSON response
        content = response_content.strip()

        # Clean markdown code blocks
        if content.startswith('```json'):
            content = content[7:]
        if content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        if content.startswith('`') and content.endswith('`'):
            content = content[1:-1]
        content = content.strip()

        # Extract JSON array
        start = content.find('[')
        end = content.rfind(']') + 1

        if start >= 0 and end > start:
            json_str = content[start:end]

            # Fix common JSON issues
            json_str = re.sub(r',\s*}', '}', json_str)
            json_str = re.sub(r',\s*]', ']', json_str)

            try:
                questions = json.loads(json_str)

                if not isinstance(questions, list):
                    print(f"[ERROR] Response is not a list")
                    return []

                print(f"[AI] Generated {len(questions)} questions")

                # Validate and save questions to database
                saved_questions = []
                for q in questions:
                    if not isinstance(q, dict):
                        continue
                    if not all(k in q for k in ["question", "options", "correct_answer"]):
                        print(f"[WARNING] Skipping invalid question: {q}")
                        continue

                    # Normalize correct_answer (extract just the letter)
                    correct_answer = str(q['correct_answer']).strip().upper()
                    if correct_answer.startswith('('):
                        correct_answer = correct_answer[1]
                    elif ')' in correct_answer:
                        correct_answer = correct_answer.split(')')[0]
                    correct_answer = correct_answer[0] if correct_answer else "A"

                    # Save to database
                    exam_question = ModuleExamQuestion(
                        module_id=module.id,
                        question=q['question'],
                        options_json=json.dumps(q['options'], ensure_ascii=False),
                        correct_answer=correct_answer,
                        difficulty=q.get('difficulty', 'medium')
                    )
                    db.add(exam_question)
                    db.flush()

                    saved_questions.append({
                        "id": exam_question.id,
                        "question": exam_question.question,
                        "options": q['options'],
                        "correct_answer": exam_question.correct_answer,
                        "difficulty": exam_question.difficulty
                    })

                db.commit()
                print(f"[SUCCESS] Saved {len(saved_questions)} questions to database")
                return saved_questions

            except json.JSONDecodeError as e:
                print(f"[ERROR] JSON parse error: {e}")
                print(f"[DEBUG] Attempted to parse: {json_str[:200]}...")
                return []
        else:
            print(f"[ERROR] Could not find JSON array in response")
            return []

    except Exception as e:
        print(f"[ERROR] Exception in generate_module_exam_questions: {e}")
        import traceback
        traceback.print_exc()
        return []


def get_exam_questions_for_module(
    module_id: int,
    db: Session,
    include_answers: bool = False
) -> List[Dict]:
    """
    Get exam questions for a module from database

    Args:
        module_id: Module ID
        db: Database session
        include_answers: If True, include correct answers (for grading)

    Returns:
        List of question dictionaries
    """
    questions = db.query(ModuleExamQuestion).filter(
        ModuleExamQuestion.module_id == module_id
    ).all()

    result = []
    for q in questions:
        question_dict = {
            "id": q.id,
            "question": q.question,
            "options": json.loads(q.options_json),
            "difficulty": q.difficulty
        }

        if include_answers:
            question_dict["correct_answer"] = q.correct_answer

        result.append(question_dict)

    return result
