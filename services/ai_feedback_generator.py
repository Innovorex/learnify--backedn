"""
AI-powered feedback generation for assessment answers
Uses Garuda AI (primary) with OpenRouter fallback for generating contextual explanations
"""
import asyncio
import os
from typing import List, Dict, Optional
import httpx
import re

# Configuration
GARUDA_API_KEY = os.getenv("GARUDA_API_KEY", "")
GARUDA_API_URL = "https://api.garuda.ai/v1/chat/completions"
GARUDA_MODEL = "llama3.2:3b"  # Fast and efficient

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "meta-llama/llama-3.3-8b-instruct:free"


async def call_garuda_api(prompt: str, timeout: int = 10) -> Optional[str]:
    """Call Garuda AI API for feedback generation"""
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                GARUDA_API_URL,
                headers={
                    "Authorization": f"Bearer {GARUDA_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": GARUDA_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 300
                }
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                print(f"[GARUDA] API error: {response.status_code}")
                return None

    except Exception as e:
        print(f"[GARUDA] Exception: {type(e).__name__}: {e}")
        return None


async def call_openrouter_api(prompt: str, timeout: int = 10) -> Optional[str]:
    """Call OpenRouter API as fallback"""
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                OPENROUTER_API_URL,
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://learnify-teach.com",
                    "X-Title": "Learnify Teacher Assessment"
                },
                json={
                    "model": OPENROUTER_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 300
                }
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                print(f"[OPENROUTER] API error: {response.status_code}")
                return None

    except Exception as e:
        print(f"[OPENROUTER] Exception: {type(e).__name__}: {e}")
        return None


async def call_ai_with_fallback(prompt: str) -> str:
    """
    Call AI with Garuda primary and OpenRouter fallback
    Returns explanation text or empty string on failure
    """
    # Try Garuda first
    print("[AI FEEDBACK] Trying Garuda AI...")
    result = await call_garuda_api(prompt)

    if result:
        print("[AI FEEDBACK] ✓ Garuda AI success")
        return result

    # Fallback to OpenRouter
    print("[AI FEEDBACK] Garuda failed, trying OpenRouter fallback...")
    result = await call_openrouter_api(prompt)

    if result:
        print("[AI FEEDBACK] ✓ OpenRouter success")
        return result

    # Both failed
    print("[AI FEEDBACK] ✗ Both APIs failed")
    return "Unable to generate AI feedback at this time."


def extract_explanation(ai_response: str) -> str:
    """Extract explanation from AI response"""
    # Look for "Explanation:" label
    match = re.search(r'Explanation:\s*(.+?)(?:\n\n|Topic:|$)', ai_response, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # If no label found, return first 2-3 sentences
    sentences = re.split(r'[.!?]+\s+', ai_response.strip())
    return '. '.join(sentences[:3]) + '.' if sentences else ai_response.strip()


def extract_topic(ai_response: str) -> Optional[str]:
    """Extract topic from AI response"""
    # Look for "Topic:" label
    match = re.search(r'Topic:\s*(.+?)(?:\n|$)', ai_response, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Default topics based on keywords
    keywords_map = {
        'coordinate': 'Coordinate Geometry',
        'geometry': 'Geometry',
        'algebra': 'Algebra',
        'equation': 'Equations',
        'percentage': 'Percentages',
        'fraction': 'Fractions',
        'statistics': 'Statistics',
        'probability': 'Probability',
        'trigonometry': 'Trigonometry'
    }

    ai_lower = ai_response.lower()
    for keyword, topic in keywords_map.items():
        if keyword in ai_lower:
            return topic

    return None


async def generate_single_feedback(
    question: Dict,
    user_answer: Dict,
    subject: str = "Mathematics"
) -> Dict:
    """
    Generate AI feedback for a single question-answer pair

    Args:
        question: {"question": str, "options": List[str], "correct_answer": str}
        user_answer: {"question_id": int, "selected_answer": str, "is_correct": bool}
        subject: Subject name for context

    Returns:
        {"question_id": int, "explanation": str, "topic": str}
    """
    # Build prompt
    options_text = '\n'.join([f"{chr(65+i)}. {opt}" for i, opt in enumerate(question['options'])])

    prompt = f"""You are an expert {subject} educator helping a teacher understand assessment questions.

**Question:** {question['question']}

**Options:**
{options_text}

**Teacher's Answer:** {user_answer['selected_answer']}
**Correct Answer:** {question['correct_answer']}
**Result:** {'✓ Correct' if user_answer['is_correct'] else '✗ Incorrect'}

**Task:** Provide a brief pedagogical explanation (2-3 sentences) that:
1. Explains WHY the correct answer is correct (underlying concept)
2. If incorrect, explains the common misconception
3. Relates to classroom teaching context

**Format:**
Explanation: [Your 2-3 sentence explanation here]
Topic: [Single topic name, e.g., "Coordinate Geometry" or "Percentages"]"""

    # Call AI with fallback
    ai_response = await call_ai_with_fallback(prompt)

    # Parse response
    explanation = extract_explanation(ai_response)
    topic = extract_topic(ai_response)

    return {
        "question_id": user_answer['question_id'],
        "explanation": explanation,
        "topic": topic
    }


async def generate_feedback_for_answers(
    questions: List[Dict],
    user_answers: List[Dict],
    subject: str = "Mathematics"
) -> List[Dict]:
    """
    Generate AI feedback for multiple question-answer pairs in parallel

    Args:
        questions: List of question dicts with question, options, correct_answer
        user_answers: List of answer dicts with question_id, selected_answer, is_correct
        subject: Subject name for context

    Returns:
        List of feedback dicts: [{"question_id": int, "explanation": str, "topic": str}]
    """
    print(f"[AI FEEDBACK] Generating feedback for {len(questions)} questions in parallel...")

    # Create tasks for parallel execution
    tasks = [
        generate_single_feedback(q, ans, subject)
        for q, ans in zip(questions, user_answers)
    ]

    # Execute all in parallel with timeout
    try:
        feedback_list = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle any exceptions
        results = []
        for i, feedback in enumerate(feedback_list):
            if isinstance(feedback, Exception):
                print(f"[AI FEEDBACK] Error for question {user_answers[i]['question_id']}: {feedback}")
                results.append({
                    "question_id": user_answers[i]['question_id'],
                    "explanation": "Unable to generate feedback for this question.",
                    "topic": None
                })
            else:
                results.append(feedback)

        print(f"[AI FEEDBACK] ✓ Generated feedback for {len(results)} questions")
        return results

    except Exception as e:
        print(f"[AI FEEDBACK] Batch generation failed: {e}")
        # Return empty feedback for all
        return [
            {
                "question_id": ans['question_id'],
                "explanation": "Unable to generate feedback at this time.",
                "topic": None
            }
            for ans in user_answers
        ]


def extract_subject_from_module(module_name: str) -> str:
    """Extract subject from module name"""
    # Map module names to subjects
    subject_map = {
        "Subject Knowledge & Content Expertise": "Mathematics",
        "Pedagogical Skills": "Pedagogy",
        "Technology & Innovation": "Educational Technology",
        "Assessment & Evaluation": "Assessment Design"
    }

    for key, value in subject_map.items():
        if key in module_name:
            return value

    return "Mathematics"  # Default


if __name__ == "__main__":
    # Test the feedback generator
    import asyncio

    async def test():
        question = {
            "question": "What is 2 + 2?",
            "options": ["3", "4", "5", "6"],
            "correct_answer": "4"
        }

        user_answer = {
            "question_id": 1,
            "selected_answer": "4",
            "is_correct": True
        }

        feedback = await generate_single_feedback(question, user_answer)
        print("Feedback:", feedback)

    asyncio.run(test())
