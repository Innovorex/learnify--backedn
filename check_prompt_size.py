import os
from dotenv import load_dotenv
load_dotenv()

# Simulate the prompt being generated
board = "CBSE"
subject = "Maths"
grade = "5-7"
state = "Telangana"
difficulty = "medium"
n_questions = 3

prompt = f"""You are an expert curriculum developer creating assessment questions for teachers.

Generate {n_questions} multiple-choice questions to test a teacher's subject knowledge and content expertise.

TEACHER CONTEXT:
- Board/Curriculum: {board}
- Subject: {subject}
- Grade/Class: {grade}

QUESTION REQUIREMENTS:
1. Test teacher's mastery of {subject} content for {board} Board Grade {grade}
2. Focus on concepts, teaching sequences, learning outcomes
3. Questions should be about WHAT teachers should know about the subject content
4. Each question must have exactly 4 options (A, B, C, D)
5. Provide correct answer as single letter "A"/"B"/"C"/"D"
6. Questions and options MUST be in ENGLISH

IMPORTANT GUIDELINES:
- Write CLEAN questions without mentioning "{board}", "Grade {grade}", or curriculum references
- Focus on universal teaching knowledge for {subject}
- Test conceptual understanding, not policy knowledge
- Questions should sound natural and professional
- ALL text must be in English

EXAMPLE FORMAT (for Mathematics):
[
  {{"question": "Which concept should be taught before introducing fractions?", "options": ["A) Decimals", "B) Basic division and parts of a whole", "C) Percentages", "D) Algebra"], "correct_answer": "B"}},
  {{"question": "What is the most effective way to introduce multiplication?", "options": ["A) Start with large numbers", "B) Begin with repeated addition", "C) Use only memorization", "D) Skip to division"], "correct_answer": "B"}}
]

🎯 DIFFICULTY LEVEL: MEDIUM LEVEL: Application, analysis, moderate complexity

Return ONLY a JSON array of {n_questions} questions. No additional text. ALL text must be in English.
"""

print(f"Prompt length (chars): {len(prompt)}")
print(f"Estimated tokens (chars/4): ~{len(prompt)//4}")
print(f"\nPrompt preview (first 500 chars):\n{prompt[:500]}")
