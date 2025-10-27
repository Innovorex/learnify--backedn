"""
Enhanced Module 1 Question Generator
Fetches syllabus from LS database and generates HARD questions for teachers
"""

import os
import json
import requests
import random
import re
import asyncpg
import aiohttp
from typing import List, Dict, Optional

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "anthropic/claude-haiku-4.5"  # Premium model for quality


async def fetch_syllabus_from_ls(
    board: str,
    class_name: str,
    subject: str
) -> List[Dict]:
    """
    Fetch syllabus topics from LS database

    Args:
        board: Board name (CBSE, TSBSE, BSEAP)
        class_name: Grade/class (6, 7, 8, 9, 10)
        subject: Subject name (Mathematics, Science, etc.)

    Returns:
        List of topic dictionaries with chapter_name, topic_name, key_concepts, etc.
    """
    try:
        # Use individual parameters instead of connection string to avoid URL encoding issues
        conn = await asyncpg.connect(
            host="127.0.0.1",
            port=5432,
            user="innovorex",
            password="Innovorex@1",
            database="ai_assessment"
        )

        query = """
            SELECT
                t.id,
                t.chapter_name,
                t.topic_name,
                t.unit_name,
                t.content_details,
                t.key_concepts,
                t.learning_outcomes,
                t.subtopics
            FROM syllabus_topics t
            JOIN syllabus_master m ON t.syllabus_id = m.id
            WHERE m.board = $1
                AND m.class_name = $2
                AND m.subject = $3
                AND m.is_active = true
            ORDER BY t.sequence_order
        """

        rows = await conn.fetch(query, board, class_name, subject)
        await conn.close()

        topics = []
        for row in rows:
            topic_dict = {
                "chapter_name": row['chapter_name'],
                "topic_name": row['topic_name'],
                "unit_name": row['unit_name'],
                "content_details": row['content_details'],
                "key_concepts": row['key_concepts'],
                "learning_outcomes": row['learning_outcomes'],
                "subtopics": row['subtopics']
            }
            topics.append(topic_dict)

        return topics

    except Exception as e:
        print(f"[ERROR] Failed to fetch from LS database: {e}")
        return []


async def call_openrouter_api(prompt: str, model: str = OPENROUTER_MODEL) -> Optional[str]:
    """Call OpenRouter API with given prompt (async)"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                },
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['choices'][0]['message']['content']
                else:
                    print(f"[ERROR] OpenRouter API error: {response.status}")
                    return None

    except Exception as e:
        print(f"[ERROR] API call failed: {e}")
        return None


async def generate_hard_question(
    topics: List[Dict],
    subject: str,
    grade: str,
    board: str
) -> Optional[Dict]:
    """
    Generate a HARD question for teachers based on syllabus topics

    Args:
        topics: List of topic dictionaries from LS database
        subject: Subject name
        grade: Grade level
        board: Board name

    Returns:
        Question dictionary with question, options, correct_answer, explanation
    """

    # Randomly select a topic
    topic = random.choice(topics)
    chapter = topic.get('chapter_name', 'Unknown Topic')
    topic_name = topic.get('topic_name', '')
    key_concepts = topic.get('key_concepts', [])
    learning_outcomes = topic.get('learning_outcomes', [])

    # Build context from syllabus
    context = f"""Subject: {subject} (Grade {grade}, {board} Board)
Chapter: {chapter}"""

    if topic_name:
        context += f"\nTopic: {topic_name}"
    if key_concepts:
        context += f"\nKey Concepts: {json.dumps(key_concepts)}"
    if learning_outcomes:
        context += f"\nLearning Outcomes: {json.dumps(learning_outcomes)}"

    prompt = f"""{context}

Generate ONE multiple-choice question testing PURE SUBJECT KNOWLEDGE for teachers.

The question should:
- Test solid understanding of the mathematical/scientific concepts
- Be challenging but fair - suitable for teachers at all levels
- Focus on conceptual understanding (WHY concepts work, not just HOW to apply formulas)
- Be based on the syllabus content above
- DO NOT ask about teaching methods, pedagogy, or "how to teach" - ONLY test subject knowledge

Examples of GOOD subject knowledge questions:
- "Why does the product of two negative numbers result in a positive number?"
- "What is the relationship between the coefficients and roots in a quadratic equation?"
- "Why is division by zero undefined in the real number system?"

Generate in this EXACT JSON format:
{{
    "question": "The question text here...",
    "options": [
        "Option A text",
        "Option B text",
        "Option C text",
        "Option D text"
    ],
    "correct_answer": "The full text of the correct option",
    "explanation": "Detailed explanation of why this answer is correct"
}}

IMPORTANT:
- Question must test SUBJECT KNOWLEDGE ONLY - NO pedagogy, NO teaching methods
- Make it challenging but accessible to all teachers
- All 4 options should be plausible
- Return ONLY valid JSON, no other text"""

    response = await call_openrouter_api(prompt)

    if not response:
        return None

    # Extract JSON from response
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        try:
            question = json.loads(json_match.group())
            return question
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON parse error: {e}")
            return None

    return None


async def generate_enhanced_module1_questions(
    teacher_profile: Dict,
    board: str = "CBSE",
    state: str = "Telangana",
    n_questions: int = 8
) -> List[Dict]:
    """
    Generate Module 1 questions by fetching syllabus from LS database

    Args:
        teacher_profile: Dict with grades_teaching, subjects_teaching, etc.
        board: Board name (CBSE, TSBSE, BSEAP)
        state: State for board mapping
        n_questions: Number of questions to generate (default 8)

    Returns:
        List of question dictionaries
    """

    print(f"\n[ENHANCED MODULE 1] Generating {n_questions} questions for teachers")
    print(f"[PROFILE] Grades: {teacher_profile.get('grades_teaching')}, Subjects: {teacher_profile.get('subjects_teaching')}, Board: {board}, State: {state}")

    # Parse teacher's grades and subjects
    grades_str = teacher_profile.get('grades_teaching', '9')
    subjects_str = teacher_profile.get('subjects_teaching', 'Mathematics')

    # Parse grades - handle both "7, 8, 9" and "7-9" formats
    grades = []
    for g in str(grades_str).split(','):
        g = g.strip()
        if '-' in g:
            # Handle range like "7-9"
            start, end = g.split('-')
            grades.extend([str(i) for i in range(int(start.strip()), int(end.strip()) + 1)])
        else:
            grades.append(g)

    subjects = [s.strip() for s in str(subjects_str).split(',')]

    # Map board name using BOTH board and state
    # If "State Board" selected, use state to determine which state board
    if board == "State Board":
        if state and "telangana" in state.lower():
            db_board = "TSBSE"
        elif state and "andhra" in state.lower():
            db_board = "BSEAP"
        else:
            db_board = "TSBSE"  # Default to Telangana if state unclear
    else:
        board_map = {
            "CBSE": "CBSE",
            "Telangana": "TSBSE",
            "Andhra Pradesh": "BSEAP",
            "TSBSE": "TSBSE",
            "BSEAP": "BSEAP"
        }
        db_board = board_map.get(board, "CBSE")  # Default to CBSE if unknown

    print(f"[BOARD MAPPING] {board} + {state} → {db_board}")

    # Map subject names to database format
    subject_map = {
        "maths": "Mathematics",
        "math": "Mathematics",
        "mathematics": "Mathematics",
        "science": "Science",
        "physics": "Science",
        "chemistry": "Science",
        "biology": "Science",
        "english": "English",
        "social": "Social Studies",
        "social studies": "Social Studies",
        "hindi": "Hindi",
        "telugu": "Telugu"
    }

    # Collect all syllabus topics for all grades and subjects the teacher teaches
    all_topics = []

    for subject in subjects:
        db_subject = subject_map.get(subject.lower(), subject)

        for grade in grades:
            print(f"[FETCHING] {db_board} Grade {grade} {db_subject} syllabus...")
            topics = await fetch_syllabus_from_ls(db_board, str(grade), db_subject)

            if topics:
                print(f"  ✓ Found {len(topics)} topics")
                all_topics.extend(topics)
            else:
                print(f"  ✗ No topics found")

    # Fallback to CBSE if no topics found
    if not all_topics and db_board != "CBSE":
        print(f"\n[FALLBACK] No topics found for {db_board}, trying CBSE...")
        for subject in subjects:
            db_subject = subject_map.get(subject.lower(), subject)
            for grade in grades:
                print(f"[FETCHING] CBSE Grade {grade} {db_subject} syllabus...")
                topics = await fetch_syllabus_from_ls("CBSE", str(grade), db_subject)
                if topics:
                    print(f"  ✓ Found {len(topics)} topics")
                    all_topics.extend(topics)
                else:
                    print(f"  ✗ No topics found")

    if not all_topics:
        print(f"[ERROR] No syllabus topics found for teacher's subjects/grades")
        return []

    print(f"\n[TOTAL] Collected {len(all_topics)} syllabus topics across all grades/subjects")
    print(f"[GENERATING] {n_questions} HARD questions from syllabus in parallel...\n")

    # Generate questions in parallel using asyncio
    import asyncio

    tasks = []
    for i in range(n_questions):
        task = generate_hard_question(
            topics=all_topics,
            subject=subjects[0],  # Primary subject
            grade=grades[0],  # Primary grade
            board=db_board
        )
        tasks.append(task)

    print(f"[PARALLEL] Generating all {n_questions} questions simultaneously...")
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out None/errors
    questions = []
    for i, result in enumerate(results):
        if result and not isinstance(result, Exception):
            questions.append(result)
            print(f"[{i+1}/{n_questions}] ✓")
        else:
            print(f"[{i+1}/{n_questions}] ✗")

    print(f"\n[SUCCESS] Generated {len(questions)}/{n_questions} HARD questions\n")

    return questions
