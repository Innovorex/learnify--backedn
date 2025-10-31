"""
AI Question Generator for K-12 Assessments
==========================================
Generates MCQ questions using OpenRouter API with REAL CBSE syllabus content.
Falls back to sample questions if API is unavailable.
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def generate_questions(board, class_name, subject, chapter, num_questions=10, syllabus_content=None):
    """
    Calls OpenRouter to generate multiple-choice questions.
    Now uses REAL CBSE syllabus content when available!
    Falls back to sample questions if API fails.

    Args:
        board: Board name (e.g., 'CBSE')
        class_name: Class (e.g., '9', '10')
        subject: Subject name (e.g., 'Mathematics')
        chapter: Chapter name (e.g., 'Real Numbers')
        num_questions: Number of questions to generate
        syllabus_content: Optional full syllabus content for context

    Returns:
        List of question dictionaries with question, options, correct_answer, difficulty
    """

    # Enhanced prompt with real syllabus content
    if syllabus_content:
        prompt = f"""
You are an expert {board} Class {class_name} {subject} question paper setter.

Using the following OFFICIAL CBSE SYLLABUS CONTENT for "{chapter}",
generate {num_questions} high-quality multiple-choice questions (MCQs).

OFFICIAL CBSE SYLLABUS CONTENT:
{syllabus_content[:3000]}

REQUIREMENTS:
- Questions MUST be based on the specific syllabus content above
- Follow CBSE exam pattern and marking scheme
- Include conceptual, application, and analytical questions
- Ensure all options are clear and plausible
- Vary difficulty: 30% easy, 50% medium, 20% hard

Output valid JSON array (NO markdown, just JSON):
[
  {{
    "question": "What is the HCF of 12 and 18?",
    "options": {{"A": "2", "B": "3", "C": "6", "D": "12"}},
    "correct_answer": "C",
    "difficulty": "easy"
  }}
]
"""
    else:
        # Fallback to generic prompt if no syllabus content
        prompt = f"""
Generate {num_questions} multiple choice questions (MCQs) for {board} Class {class_name} {subject},
Chapter: {chapter}. Output valid JSON with a list of objects like:
[
  {{
    "question": "What is the HCF of 12 and 18?",
    "options": {{"A": "2", "B": "3", "C": "6", "D": "12"}},
    "correct_answer": "C",
    "difficulty": "easy"
  }}
]
"""

    # Try API first
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",  # LT backend port
            "X-Title": "Learnify K-12 Assessment Platform"
        }
        payload = {
            "model": "openai/gpt-4o-mini",   # Paid GPT-4o Mini (cheap & good)
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        data = response.json()

        if "error" in data:
            print(f"❌ API Error: {data['error']}")
            print("⚠️ API key invalid. Falling back to sample questions...")
            return generate_sample_questions(subject, chapter, num_questions)

        content = data["choices"][0]["message"]["content"]
        print("📝 AI Content:", content[:200])

        # Extract JSON from markdown code block if present
        if "```json" in content:
            json_str = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            json_str = content.split("```")[1].split("```")[0].strip()
        else:
            json_str = content.strip()

        # Try to parse, handling incomplete JSON
        try:
            questions = json.loads(json_str)
        except json.JSONDecodeError:
            # Try to find and extract just the complete JSON array
            import re
            match = re.search(r'\[[\s\S]*\]', content)
            if match:
                json_str = match.group(0)
                questions = json.loads(json_str)
            else:
                raise

        print(f"✅ Successfully parsed {len(questions)} questions")
        return questions

    except Exception as e:
        print("❌ Error with AI API:", e)
        print("⚠️ Using sample questions instead...")
        return generate_sample_questions(subject, chapter, num_questions)


def generate_sample_questions(subject, chapter, num_questions=10):
    """
    Generate sample questions when API is unavailable.
    """
    print(f"📝 Generating {num_questions} sample questions for {subject} - {chapter}")

    questions = []
    for i in range(min(num_questions, 10)):
        questions.append({
            "question": f"Question {i+1}: What is a key concept in {chapter}?",
            "options": {
                "A": f"Option A about {chapter}",
                "B": f"Option B about {chapter}",
                "C": f"Correct answer about {chapter}",
                "D": f"Option D about {chapter}"
            },
            "correct_answer": "C",
            "difficulty": "medium"
        })

    return questions


def generate_questions_from_material(
    material_content: str,
    subject: str,
    class_name: str,
    num_questions: int = 10
) -> list:
    """
    Generate questions from uploaded teaching material content

    Uses OpenRouter with the material content as context instead of syllabus.

    Args:
        material_content: Extracted text content from the material (page range)
        subject: Subject name (e.g., 'Mathematics')
        class_name: Class level (e.g., '9', '10')
        num_questions: Number of questions to generate

    Returns:
        List of question dictionaries with question, options, correct_answer, difficulty
    """

    # Limit content to avoid token limits (first 4000 chars)
    limited_content = material_content[:4000]

    prompt = f"""You are an expert teacher creating assessment questions for Class {class_name} {subject}.

TEACHING MATERIAL CONTENT:
{limited_content}

Generate {num_questions} multiple-choice questions (MCQs) based ONLY on the material content above.

REQUIREMENTS:
- Questions must be based on content from the material
- Include 4 options (A, B, C, D) for each question
- Mark the correct answer clearly
- Difficulty should match Class {class_name} level
- Cover different topics from the material
- Ensure options are clear and plausible
- Avoid trivial or ambiguous questions

Return ONLY a valid JSON array (no markdown, no explanations):
[
  {{
    "question": "Question text here",
    "options": {{
      "A": "Option A text",
      "B": "Option B text",
      "C": "Option C text",
      "D": "Option D text"
    }},
    "correct_answer": "A",
    "difficulty": "medium"
  }}
]
"""

    try:
        print(f"[MATERIAL QUESTION GEN] Generating {num_questions} questions from material...")
        print(f"[MATERIAL QUESTION GEN] Content length: {len(limited_content)} chars")

        if not OPENROUTER_API_KEY:
            print("[MATERIAL QUESTION GEN] No OpenRouter API key - returning sample questions")
            return _generate_sample_questions_material(subject, class_name, num_questions)

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "meta-llama/llama-3.3-70b-instruct",
            "messages": [
                {"role": "system", "content": "You are an expert question generator for K-12 assessments."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 4000,
            "temperature": 0.7
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=120
        )

        if response.status_code == 200:
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"]

            # Extract JSON from response
            ai_response = ai_response.strip()
            if ai_response.startswith("```json"):
                ai_response = ai_response[7:]
            if ai_response.startswith("```"):
                ai_response = ai_response[3:]
            if ai_response.endswith("```"):
                ai_response = ai_response[:-3]
            ai_response = ai_response.strip()

            questions = json.loads(ai_response)

            print(f"[MATERIAL QUESTION GEN] ✓ Successfully generated {len(questions)} questions")

            return questions[:num_questions]

        else:
            print(f"[MATERIAL QUESTION GEN] API error: {response.status_code}")
            return _generate_sample_questions_material(subject, class_name, num_questions)

    except Exception as e:
        print(f"[MATERIAL QUESTION GEN ERROR] {e}")
        return _generate_sample_questions_material(subject, class_name, num_questions)


def _generate_sample_questions_material(subject: str, class_name: str, num_questions: int = 10) -> list:
    """
    Generate sample questions when material-based AI generation fails

    Returns:
        List of sample question dictionaries
    """
    print(f"[MATERIAL QUESTION GEN] Generating {num_questions} sample questions as fallback")

    questions = []
    for i in range(num_questions):
        questions.append({
            "question": f"Sample Question {i + 1} for Class {class_name} {subject} (from material)",
            "options": {
                "A": f"Sample option A",
                "B": f"Sample option B",
                "C": f"Sample option C (Correct)",
                "D": f"Sample option D"
            },
            "correct_answer": "C",
            "difficulty": "medium"
        })

    return questions
