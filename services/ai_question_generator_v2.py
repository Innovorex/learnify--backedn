"""
AI Question Generator V2 - Multi-Type Questions from NCERT Content
===================================================================
Generates various question types (MCQ, True/False, Short Answer, etc.)
from NCERT textbook content WITHOUT referencing specific example numbers.

Key Features:
- Generates concept-based questions (NO "Example 1.1" references)
- Supports 6 question types
- Uses cleaned NCERT content
- Returns questions with educational metadata
"""

import json
import re
from typing import List, Dict, Optional
from services.openrouter import generate_subject_knowledge_questions_ai_requests


class AIQuestionGeneratorV2:
    """
    AI-powered question generator supporting multiple question types
    """

    def __init__(self):
        self.supported_types = [
            "multiple_choice",
            "true_false",
            "short_answer",
            "fill_blank",
            "multi_select",
            "ordering"
        ]

    def generate_questions(
        self,
        ncert_content: Dict,
        question_spec: Dict[str, int],
        grade: int,
        subject: str,
        chapter: str,
        language: str = "English"
    ) -> List[Dict]:
        """
        Generate questions based on NCERT content

        Args:
            ncert_content: From NCERTContentService.get_chapter_content()
            question_spec: {"multiple_choice": 6, "true_false": 4, ...}
            grade: 10
            subject: "Science"
            chapter: "Chemical Reactions and Equations"

        Returns:
            [
                {
                    "question": "What type of change occurs when ice melts?",
                    "question_type": "multiple_choice",
                    "question_data": {
                        "options": {"A": "Chemical", "B": "Physical", "C": "Both", "D": "Neither"},
                        "correct_answer": "B"
                    },
                    "difficulty": "easy",
                    "marks": 1,
                    "concept_tested": "Physical vs Chemical Change",
                    "explanation": "Ice melting is physical change..."
                },
                ...
            ]
        """

        all_questions = []

        # Generate each question type separately
        for q_type, count in question_spec.items():
            if count == 0:
                continue

            if q_type not in self.supported_types:
                print(f"⚠️  Unknown question type: {q_type}, skipping...")
                continue

            print(f"🔄 Generating {count} {q_type} questions...")

            # Call appropriate generator
            if q_type == "multiple_choice":
                questions = self._generate_mcq(ncert_content, count, grade, subject, chapter, language)
            elif q_type == "true_false":
                questions = self._generate_true_false(ncert_content, count, grade, subject, chapter, language)
            elif q_type == "short_answer":
                questions = self._generate_short_answer(ncert_content, count, grade, subject, chapter, language)
            elif q_type == "fill_blank":
                questions = self._generate_fill_blank(ncert_content, count, grade, subject, chapter, language)
            elif q_type == "multi_select":
                questions = self._generate_multi_select(ncert_content, count, grade, subject, chapter, language)
            elif q_type == "ordering":
                questions = self._generate_ordering(ncert_content, count, grade, subject, chapter, language)
            else:
                questions = []

            all_questions.extend(questions)
            print(f"✅ Generated {len(questions)} {q_type} questions")

        print(f"✅ Total: {len(all_questions)} questions generated")
        return all_questions

    def _generate_mcq(self, ncert_content: Dict, count: int, grade: int, subject: str, chapter: str, language: str = "English") -> List[Dict]:
        """Generate Multiple Choice Questions"""

        language_instruction = f"🌐 LANGUAGE REQUIREMENT: Generate ALL questions, options, and explanations in {language}." if language != "English" else ""

        prompt = f"""You are an expert CBSE Class {grade} {subject} teacher.

{language_instruction}

TEXTBOOK CONTENT (Chapter: {chapter}):
{ncert_content['cleaned_content'][:4000]}

KEY CONCEPTS:
{', '.join(ncert_content['key_concepts'][:10])}

TASK: Generate {count} multiple-choice questions (MCQs) based on the concepts in the content.

🚫 CRITICAL REQUIREMENTS - READ CAREFULLY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Questions must be STANDALONE and CONCEPT-BASED
2. DO NOT reference "Example 1.1", "Exercise 2.3", "Activity 1.2" or ANY numbered examples
3. DO NOT mention page numbers, textbook sections, or figure numbers
4. Questions should test understanding of CONCEPTS, not memory of specific examples
5. Each question should have 4 options (A, B, C, D)
6. Questions must be answerable by a student who studied the concepts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ GOOD EXAMPLES (concept-based, standalone):
- "What type of change occurs when ice melts into water?"
- "Which of the following is an example of a chemical change?"
- "What is the main characteristic that distinguishes physical from chemical changes?"

❌ BAD EXAMPLES (avoid these):
- "In Example 1.1, what was the temperature mentioned?"
- "According to the activity on page 15, what happened?"
- "Referring to Exercise 2.3, solve question 5"

OUTPUT FORMAT (Valid JSON array):
[
  {{
    "question": "What type of change occurs when ice melts into water?",
    "options": {{
      "A": "Chemical change",
      "B": "Physical change",
      "C": "Both physical and chemical",
      "D": "Neither physical nor chemical"
    }},
    "correct_answer": "B",
    "difficulty": "easy",
    "concept_tested": "Physical vs Chemical Change",
    "explanation": "Ice melting is a physical change because only the state changes, not the chemical composition."
  }}
]

Generate {count} questions following this EXACT format. Return ONLY the JSON array, no extra text.
"""

        response = generate_subject_knowledge_questions_ai_requests(prompt)
        questions_data = self._parse_json_response(response)

        # Format for storage
        formatted = []
        for q in questions_data:
            formatted.append({
                "question": q["question"],
                "question_type": "multiple_choice",
                "question_data": {
                    "options": q["options"],
                    "correct_answer": q["correct_answer"]
                },
                "difficulty": q.get("difficulty", "medium"),
                "marks": 1,
                "concept_tested": q.get("concept_tested", ""),
                "explanation": q.get("explanation", "")
            })

        return formatted

    def _generate_true_false(self, ncert_content: Dict, count: int, grade: int, subject: str, chapter: str, language: str = "English") -> List[Dict]:
        """Generate True/False Questions"""

        language_instruction = f"🌐 LANGUAGE REQUIREMENT: Generate ALL questions and explanations in {language}.\n\n" if language != "English" else ""

        prompt = f"""{language_instruction}You are an expert CBSE Class {grade} {subject} teacher.

TEXTBOOK CONTENT (Chapter: {chapter}):
{ncert_content['cleaned_content'][:4000]}

TASK: Generate {count} True/False questions based on the concepts.

🚫 CRITICAL REQUIREMENTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Statements must be concept-based and standalone
2. DO NOT reference example numbers, page numbers, or specific activities
3. Statements should test understanding of facts and concepts
4. Mix of true and false statements (balanced)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ GOOD EXAMPLES:
- "A chemical change results in the formation of new substances."
- "Rusting of iron is a physical change."
- "During a physical change, the chemical composition remains the same."

❌ BAD EXAMPLES (avoid these):
- "In Example 1.1, the final answer was 25."
- "The activity on page 10 showed that water boils at 100°C."

OUTPUT FORMAT (Valid JSON array):
[
  {{
    "statement": "A chemical change results in the formation of new substances.",
    "correct_answer": true,
    "difficulty": "easy",
    "concept_tested": "Characteristics of Chemical Change",
    "explanation": "Chemical changes produce new substances with different properties."
  }}
]

Generate {count} statements. Return ONLY the JSON array.
"""

        response = generate_subject_knowledge_questions_ai_requests(prompt)
        questions_data = self._parse_json_response(response)

        formatted = []
        for q in questions_data:
            formatted.append({
                "question": q["statement"],
                "question_type": "true_false",
                "question_data": {
                    "correct_answer": q["correct_answer"]
                },
                "difficulty": q.get("difficulty", "medium"),
                "marks": 1,
                "concept_tested": q.get("concept_tested", ""),
                "explanation": q.get("explanation", "")
            })

        return formatted

    def _generate_short_answer(self, ncert_content: Dict, count: int, grade: int, subject: str, chapter: str, language: str = "English") -> List[Dict]:
        """Generate Short Answer Questions (2-3 marks)"""

        language_instruction = f"🌐 LANGUAGE REQUIREMENT: Generate ALL questions and sample answers in {language}.\n\n" if language != "English" else ""

        prompt = f"""{language_instruction}You are an expert CBSE Class {grade} {subject} teacher.

TEXTBOOK CONTENT (Chapter: {chapter}):
{ncert_content['cleaned_content'][:4000]}

TASK: Generate {count} short answer questions (2-3 marks, 30-50 words answer).

🚫 CRITICAL REQUIREMENTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Questions must be concept-based
2. DO NOT reference example numbers or page numbers
3. Questions should require explanation/description
4. Provide a sample answer for each
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ GOOD EXAMPLES:
- "Define oxidation and give one example."
- "Explain the difference between physical and chemical changes."
- "Why is rusting considered a chemical change?"

OUTPUT FORMAT (Valid JSON array):
[
  {{
    "question": "Define oxidation and give one example.",
    "sample_answer": "Oxidation is the addition of oxygen or removal of hydrogen. Example: Rusting of iron (Fe + O2 → Fe2O3).",
    "max_words": 50,
    "difficulty": "medium",
    "marks": 2,
    "concept_tested": "Oxidation"
  }}
]

Generate {count} questions. Return ONLY the JSON array.
"""

        response = generate_subject_knowledge_questions_ai_requests(prompt)
        questions_data = self._parse_json_response(response)

        formatted = []
        for q in questions_data:
            formatted.append({
                "question": q["question"],
                "question_type": "short_answer",
                "question_data": {
                    "sample_answer": q["sample_answer"],
                    "max_words": q.get("max_words", 50)
                },
                "difficulty": q.get("difficulty", "medium"),
                "marks": q.get("marks", 2),
                "concept_tested": q.get("concept_tested", "")
            })

        return formatted

    def _generate_fill_blank(self, ncert_content: Dict, count: int, grade: int, subject: str, chapter: str, language: str = "English") -> List[Dict]:
        """Generate Fill in the Blank Questions"""

        language_instruction = f"🌐 LANGUAGE REQUIREMENT: Generate ALL questions and answers in {language}.\n\n" if language != "English" else ""

        prompt = f"""{language_instruction}You are an expert CBSE Class {grade} {subject} teacher.

TEXTBOOK CONTENT (Chapter: {chapter}):
{ncert_content['cleaned_content'][:4000]}

TASK: Generate {count} fill-in-the-blank questions.

REQUIREMENTS:
1. Concept-based sentences with key terms removed
2. Use ___ to indicate blanks
3. Provide correct answers

EXAMPLES:
✅ "The process of burning of a substance in the presence of oxygen is called ___." (Answer: combustion)
✅ "A change in which new substances are formed is called a ___ change." (Answer: chemical)

OUTPUT FORMAT (Valid JSON array):
[
  {{
    "question": "The process of burning in the presence of oxygen is called ___.",
    "correct_answers": ["combustion"],
    "difficulty": "easy",
    "concept_tested": "Combustion"
  }}
]

Generate {count} questions. Return ONLY the JSON array.
"""

        response = generate_subject_knowledge_questions_ai_requests(prompt)
        questions_data = self._parse_json_response(response)

        formatted = []
        for q in questions_data:
            formatted.append({
                "question": q["question"],
                "question_type": "fill_blank",
                "question_data": {
                    "correct_answers": q["correct_answers"]
                },
                "difficulty": q.get("difficulty", "medium"),
                "marks": 1,
                "concept_tested": q.get("concept_tested", "")
            })

        return formatted

    def _generate_multi_select(self, ncert_content: Dict, count: int, grade: int, subject: str, chapter: str, language: str = "English") -> List[Dict]:
        """Generate Multi-Select Questions (multiple correct answers)"""

        language_instruction = f"🌐 LANGUAGE REQUIREMENT: Generate ALL questions and options in {language}.\n\n" if language != "English" else ""

        prompt = f"""{language_instruction}Generate {count} multi-select questions where 2-3 options are correct.

TEXTBOOK CONTENT:
{ncert_content['cleaned_content'][:4000]}

EXAMPLE:
"Which of the following are examples of chemical changes? (Select all that apply)"
Options: A) Rusting, B) Melting ice, C) Burning wood, D) Digestion
Correct: A, C, D

OUTPUT FORMAT:
[
  {{
    "question": "...",
    "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
    "correct_answers": ["A", "C", "D"],
    "difficulty": "medium",
    "concept_tested": "Chemical Changes"
  }}
]

Generate {count} questions. Return ONLY JSON array.
"""

        response = generate_subject_knowledge_questions_ai_requests(prompt)
        questions_data = self._parse_json_response(response)

        formatted = []
        for q in questions_data:
            formatted.append({
                "question": q["question"],
                "question_type": "multi_select",
                "question_data": {
                    "options": q["options"],
                    "correct_answers": q["correct_answers"]
                },
                "difficulty": q.get("difficulty", "medium"),
                "marks": 2,
                "concept_tested": q.get("concept_tested", "")
            })

        return formatted

    def _generate_ordering(self, ncert_content: Dict, count: int, grade: int, subject: str, chapter: str, language: str = "English") -> List[Dict]:
        """Generate Ordering Questions (arrange in sequence)"""

        language_instruction = f"🌐 LANGUAGE REQUIREMENT: Generate ALL questions and items in {language}.\n\n" if language != "English" else ""

        prompt = f"""{language_instruction}Generate {count} ordering questions where items must be arranged in correct sequence.

TEXTBOOK CONTENT:
{ncert_content['cleaned_content'][:4000]}

EXAMPLE:
"Arrange the following steps of the water cycle in correct order:"
Items: ["Condensation", "Evaporation", "Precipitation", "Collection"]
Correct order: [1, 0, 2, 3] (indices: Evaporation first, then Condensation, etc.)

OUTPUT FORMAT:
[
  {{
    "question": "Arrange the steps in correct order:",
    "items": ["Step A", "Step B", "Step C", "Step D"],
    "correct_order": [1, 0, 2, 3],
    "difficulty": "hard",
    "concept_tested": "Process Understanding"
  }}
]

Generate {count} questions. Return ONLY JSON array.
"""

        response = generate_subject_knowledge_questions_ai_requests(prompt)
        questions_data = self._parse_json_response(response)

        formatted = []
        for q in questions_data:
            formatted.append({
                "question": q["question"],
                "question_type": "ordering",
                "question_data": {
                    "items": q["items"],
                    "correct_order": q["correct_order"]
                },
                "difficulty": q.get("difficulty", "hard"),
                "marks": 2,
                "concept_tested": q.get("concept_tested", "")
            })

        return formatted

    def _parse_json_response(self, response: str) -> list:
        """Parse JSON from AI response (handles markdown code blocks)"""

        # Remove markdown code blocks
        content = response.strip()

        if content.startswith('```json'):
            content = content[7:]
        if content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]

        # Remove single backticks
        if content.startswith('`') and content.endswith('`'):
            content = content[1:-1]

        content = content.strip()

        # Extract JSON array
        start = content.find('[')
        end = content.rfind(']') + 1

        if start >= 0 and end > start:
            json_str = content[start:end]

            # Fix common JSON issues
            import re
            json_str = re.sub(r',\s*}', '}', json_str)  # Remove trailing commas in objects
            json_str = re.sub(r',\s*]', ']', json_str)  # Remove trailing commas in arrays

            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"❌ JSON parse error: {e}")
                print(f"   Content preview: {json_str[:200]}")
                return []
        else:
            print(f"❌ Could not find JSON array in response")
            return []


# Factory function
def get_question_generator() -> AIQuestionGeneratorV2:
    """Get AI question generator instance"""
    return AIQuestionGeneratorV2()
