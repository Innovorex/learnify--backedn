#!/usr/bin/env python3
"""
Generate Module 1 Questions - Live Demo
Demonstrates enhanced question generation with Bloom's Taxonomy
"""

import os
import json
import requests
import time

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")
OPENROUTER_MODEL = "anthropic/claude-haiku-4.5"  # Premium model for quality


def call_ai(prompt, max_tokens=3000):
    """Call OpenRouter API"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://learnify-teach.com",
        "X-Title": "Learnify Teach - Module 1"
    }

    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert teacher assessment creator."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.3
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=120
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code}"

    except Exception as e:
        return f"Exception: {e}"


def generate_enhanced_module1_question(bloom_level, topic_info):
    """Generate one enhanced question"""

    level_prompts = {
        "UNDERSTAND": """
Generate a question testing CONCEPTUAL UNDERSTANDING (Bloom's Level 2: Understand).

Requirements:
✅ Test WHY or HOW something works
✅ Require explaining relationships between concepts
✅ NOT just "What is X?" - must be deeper
✅ Focus on teacher's conceptual grasp

Example: "Why does a passenger jerk forward when a bus suddenly stops? Explain using Newton's laws."
""",
        "APPLY": """
Generate a question testing APPLICATION (Bloom's Level 3: Apply).

Requirements:
✅ Present a NEW real-world scenario
✅ Test ability to apply concepts in practice
✅ May involve teaching demonstrations or experiments
✅ Connect theory to practice

Example: "A teacher wants to demonstrate momentum conservation with colliding carts. Which Newton's law is the foundation?"
""",
        "ANALYZE": """
Generate a question testing ANALYSIS (Bloom's Level 4: Analyze).

Requirements:
✅ Present a student MISCONCEPTION or error
✅ Test ability to IDENTIFY THE FLAW
✅ Require diagnosing the conceptual gap
✅ Focus on teacher's error-correction ability

Example: "A student says 'Action-reaction cancel, so nothing moves.' What's the flaw?"
""",
        "EVALUATE": """
Generate a question testing EVALUATION (Bloom's Level 5: Evaluate).

Requirements:
✅ Require JUDGING quality of teaching approaches
✅ Test pedagogical decision-making
✅ Ask which method/sequence is BEST and WHY
✅ Focus on pedagogical content knowledge (PCK)

Example: "Evaluate which teaching sequence is most effective for Newton's laws: (A) 1st→2nd→3rd, (B) Concrete examples→1st→3rd→2nd. Justify."
"""
    }

    prompt = f"""{level_prompts[bloom_level]}

TOPIC: {topic_info['topic']}
SUBJECT: {topic_info['subject']} - Grade {topic_info['grade']}
BOARD: {topic_info['board']}

CORE CONCEPTS:
{chr(10).join(['- ' + c for c in topic_info.get('concepts', [])])}

COMMON MISCONCEPTIONS:
{chr(10).join(['- ' + m for m in topic_info.get('misconceptions', [])])}

CRITICAL: This is for TEACHERS, not students. Test deep subject expertise.

Return ONLY valid JSON:
{{
    "question": "Full question text",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "correct_answer": "B",
    "explanation": "Why correct answer is right, why others are wrong",
    "bloom_level": "{bloom_level}",
    "tests": "What skill/knowledge this assesses"
}}
"""

    response = call_ai(prompt)

    # Extract JSON
    import re
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except:
            pass

    return None


def main():
    """Generate 8 Module 1 questions with Bloom's taxonomy"""

    print("\n" + "="*80)
    print("MODULE 1: SUBJECT KNOWLEDGE & CONTENT EXPERTISE")
    print("="*80)
    print("\nTeacher Profile:")
    print("  - Education: B.Sc Mathematics")
    print("  - Teaching: Grade 9, CBSE")
    print("  - Subjects: Mathematics, Science")
    print("\nGenerating: 8 Enhanced Questions (Bloom's Taxonomy Levels 2-5)")
    print("="*80 + "\n")

    # Topic configuration (Newton's Laws for Science)
    topic_info = {
        "topic": "Newton's Laws of Motion",
        "subject": "Science (Physics)",
        "grade": "9",
        "board": "CBSE",
        "concepts": [
            "Force: Push or pull that changes motion state",
            "Inertia: Resistance to motion change",
            "Mass: Measure of inertia",
            "Acceleration: Rate of velocity change",
            "Friction: Opposes relative motion",
            "Action-Reaction: Equal and opposite forces on different objects"
        ],
        "misconceptions": [
            "Force needed to maintain constant velocity",
            "Action-reaction forces cancel out",
            "Heavier objects fall faster",
            "Mass and weight are same"
        ]
    }

    # Bloom's distribution: 2 Understand, 3 Apply, 2 Analyze, 1 Evaluate
    distribution = [
        "UNDERSTAND", "UNDERSTAND",
        "APPLY", "APPLY", "APPLY",
        "ANALYZE", "ANALYZE",
        "EVALUATE"
    ]

    questions = []

    for idx, bloom_level in enumerate(distribution, 1):
        print(f"[{idx}/8] Generating {bloom_level} question...", end=" ", flush=True)

        question = generate_enhanced_module1_question(bloom_level, topic_info)

        if question:
            questions.append(question)
            print("✓")
        else:
            print("✗ (failed)")

        # Rate limiting
        if idx < len(distribution):
            time.sleep(1.5)

    # Display results
    print("\n" + "="*80)
    print(f"✅ GENERATED {len(questions)}/8 QUESTIONS")
    print("="*80 + "\n")

    for idx, q in enumerate(questions, 1):
        print(f"\n{'─'*80}")
        print(f"QUESTION {idx} | Bloom's Level: {q.get('bloom_level', 'N/A')}")
        print(f"{'─'*80}")
        print(f"\n{q.get('question', '')}")

        print("\nOptions:")
        for opt in q.get('options', []):
            marker = " ← CORRECT" if opt.startswith(q.get('correct_answer', 'X')) else ""
            print(f"  {opt}{marker}")

        print(f"\n💡 Explanation:")
        explanation = q.get('explanation', 'N/A')
        # Wrap explanation
        import textwrap
        wrapped = textwrap.fill(explanation, width=76, initial_indent="   ", subsequent_indent="   ")
        print(wrapped)

        print(f"\n🎯 Tests: {q.get('tests', 'N/A')}")

    # Save to file
    output_file = "/tmp/module1_enhanced_questions.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print("\n" + "="*80)
    print(f"💾 Questions saved to: {output_file}")
    print("="*80)

    # Summary
    bloom_counts = {}
    for q in questions:
        level = q.get('bloom_level', 'Unknown')
        bloom_counts[level] = bloom_counts.get(level, 0) + 1

    print("\n📊 Bloom's Taxonomy Distribution:")
    for level in ["UNDERSTAND", "APPLY", "ANALYZE", "EVALUATE"]:
        count = bloom_counts.get(level, 0)
        percentage = (count / len(questions) * 100) if questions else 0
        bar = "█" * count
        print(f"  {level:12} : {bar} {count} ({percentage:.0f}%)")

    print("\n✅ GENERATION COMPLETE!\n")

    return questions


if __name__ == "__main__":
    main()
