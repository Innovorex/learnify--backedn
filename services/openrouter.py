# services/openrouter.py
import os, json, asyncio, time
import requests
from .curriculum_data import curriculum_service

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-8b-instruct:free") # Default to a common OpenRouter model

def generate_subject_knowledge_questions_ai_requests(prompt_text: str, max_retries: int = 3):
    """
    Generate subject knowledge questions via OpenRouter API using requests.
    Includes retry logic with exponential backoff for rate limits.
    """
    api_key_for_call = OPENROUTER_API_KEY
    model_for_call = OPENROUTER_MODEL

    print(f"DEBUG: API Call - OPENROUTER_API_KEY (first 15 chars): {api_key_for_call[:15] if api_key_for_call else 'None'}...")
    print(f"DEBUG: API Call - OPENROUTER_MODEL: {model_for_call}")

    headers = {
        "Authorization": f"Bearer {api_key_for_call}",
        "HTTP-Referer": "https://openrouter.ai/",
        "X-Title": "TeacherApp AI Assessment Generator"
    }

    data = {
        "model": model_for_call,
        "messages": [
            {"role": "system", "content": "You are an AI question generator for teachers."},
            {"role": "user", "content": prompt_text}
        ],
        "max_tokens": 4000,  # Increased from 2500 to ensure complete JSON responses
    }

    for attempt in range(max_retries):
        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                                     headers=headers, json=data, timeout=120)

            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            elif response.status_code == 429:
                # Rate limit hit
                wait_time = (2 ** attempt) * 2  # Exponential backoff: 2s, 4s, 8s
                print(f"[RATE LIMIT] Hit rate limit. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}...")
                time.sleep(wait_time)
                continue
            else:
                return f"Error {response.status_code}: {response.text}"
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 2
                print(f"[ERROR] API call failed: {str(e)}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            return f"Exception while contacting OpenRouter: {str(e)}"

    return "Error: Maximum retries exceeded due to rate limiting"

def _format_curriculum_context(curriculum_data: dict, board: str, subject: str, grade: str) -> str:
    """Format curriculum data for prompt context"""
    if not curriculum_data or 'units' not in curriculum_data:
        return f"Standard {board} curriculum for {subject} Grade {grade}"

    context = f"\n[CURRICULUM] OFFICIAL {board.upper()} {subject.upper()} GRADE {grade} CURRICULUM:\n"

    for unit_name, unit_data in curriculum_data['units'].items():
        context += f"\n* UNIT: {unit_name}\n"
        context += f"   Weightage: {unit_data.get('weightage', 'N/A')}\n"

        if 'topics' in unit_data:
            context += f"   Topics: {', '.join(unit_data['topics'])}\n"

        if 'learning_outcomes' in unit_data:
            context += f"   Learning Outcomes:\n"
            for outcome in unit_data['learning_outcomes'][:3]:  # Limit to 3 outcomes
                context += f"   - {outcome}\n"

    # Add real-world applications
    if 'real_world_applications' in curriculum_data:
        context += f"\n[APPLICATIONS] REAL-WORLD APPLICATIONS:\n"
        for app in curriculum_data['real_world_applications'][:4]:
            context += f"   - {app}\n"

    # Add common misconceptions
    if 'common_misconceptions' in curriculum_data:
        context += f"\nCOMMON STUDENT MISCONCEPTIONS TO ADDRESS:\n"
        for misconception in curriculum_data['common_misconceptions'][:3]:
            context += f"   - {misconception}\n"

    # Add prerequisite knowledge
    if 'prerequisite_knowledge' in curriculum_data:
        context += f"\n[PREREQUISITES] PREREQUISITE KNOWLEDGE:\n"
        for prereq in curriculum_data['prerequisite_knowledge'][:3]:
            context += f"   - {prereq}\n"

    return context

def _format_assessment_guidelines(curriculum_data: dict) -> str:
    """Format assessment pattern information"""
    if not curriculum_data or 'assessment_pattern' not in curriculum_data:
        return "Follow standard assessment patterns"

    assessment = curriculum_data['assessment_pattern']
    guidelines = f"\n[ASSESSMENT] ASSESSMENT PATTERN:\n"
    guidelines += f"- Total Marks: {assessment.get('total_marks', 100)}\n"
    guidelines += f"- Theory Exam: {assessment.get('theory_exam', 80)} marks\n"
    guidelines += f"- Internal Assessment: {assessment.get('internal_assessment', 20)} marks\n"

    if 'question_types' in assessment:
        guidelines += f"- Question Distribution: {assessment['question_types']}\n"

    if 'competency_framework' in curriculum_data:
        guidelines += f"\n[COMPETENCY] COMPETENCY FRAMEWORK:\n"
        for comp, desc in curriculum_data['competency_framework'].items():
            guidelines += f"- {comp.replace('_', ' ').title()}: {desc}\n"

    return guidelines

def _get_forbidden_topics(module_name: str) -> str:
    """Get forbidden topics for a specific module to prevent mixing"""
    forbidden_map = {
        "Subject Knowledge & Content Expertise": [
            "Classroom management techniques",
            "Teaching methodologies and pedagogy",
            "Educational technology and digital tools",
            "Assessment methods and feedback strategies",
            "Inclusive teaching practices",
            "Professional ethics and conduct"
        ],
        "Pedagogical Skills & Classroom Practice": [
            "Subject-specific curriculum content",
            "Mathematical formulas and concepts",
            "Scientific theories and principles",
            "Educational technology tools",
            "Assessment rubrics and grading",
            "Professional ethics and accountability"
        ],
        "Use of Technology & Innovation": [
            "Subject content and curriculum knowledge",
            "Classroom management strategies",
            "Assessment and feedback methods",
            "Professional ethics",
            "Inclusive teaching practices"
        ],
        "Assessment & Feedback": [
            "Subject content knowledge",
            "Teaching methodologies",
            "Educational technology tools",
            "Professional ethics",
            "Classroom management"
        ],
        "Inclusivity, Values & Dispositions": [
            "Subject content knowledge",
            "Teaching methodologies",
            "Educational technology",
            "Assessment methods",
            "Professional ethics"
        ],
        "Professional Ethics & Teacher Accountability": [
            "Subject content knowledge",
            "Teaching methodologies",
            "Educational technology",
            "Assessment methods",
            "Inclusive practices"
        ]
    }

    forbidden_topics = forbidden_map.get(module_name, [])
    if forbidden_topics:
        return "- " + "\n- ".join(forbidden_topics)
    return "No specific forbidden topics defined"

def _get_module_specific_examples(module_name: str, board: str, grade: str, subject: str) -> str:
    """Get module-specific examples to guide question generation"""
    examples = {
        "Subject Knowledge & Content Expertise": """[
  {"question":"Which mathematical concept should be taught before introducing quadratic equations?","options":["A) Coordinate geometry","B) Linear equations and factorization","C) Statistics and probability","D) Mensuration"],"correct_answer":"B"},
  {"question":"What is the most effective sequence for teaching algebraic expressions?","options":["A) Start with complex polynomials","B) Begin with basic operations and simple terms","C) Jump directly to factorization","D) Focus only on word problems"],"correct_answer":"B"},
  {"question":"Which learning outcome is most important when teaching trigonometric ratios?","options":["A) Memorizing all formulas","B) Understanding the relationship between angles and sides","C) Solving only textbook problems","D) Learning historical development"],"correct_answer":"B"}
]""",

        "Pedagogical Skills & Classroom Practice": """[
  {"question":"Which classroom management strategy is most effective for engaging passive learners?","options":["A) Increased homework assignments","B) Think-pair-share activities","C) Silent individual work","D) Teacher-centered lectures"],"correct_answer":"B"},
  {"question":"What is the most appropriate way to structure a 45-minute lesson?","options":["A) 40 min lecture, 5 min questions","B) 5 min intro, 30 min activities, 10 min recap","C) 45 min continuous instruction","D) 15 min theory, 30 min silent work"],"correct_answer":"B"},
  {"question":"Which technique best promotes student participation in classroom discussions?","options":["A) Cold calling random students","B) Wait time and open-ended questions","C) Yes/no questions only","D) Teacher providing all answers"],"correct_answer":"B"}
]""",

        "Use of Technology & Innovation": """[
  {"question":"Which digital tool is most effective for creating interactive mathematics lessons?","options":["A) MS Word documents","B) GeoGebra or Desmos","C) PowerPoint slides only","D) Printed worksheets"],"correct_answer":"B"},
  {"question":"What is the primary benefit of using educational apps in classrooms?","options":["A) Reducing teacher workload","B) Replacing textbooks completely","C) Enhancing student engagement and understanding","D) Eliminating homework needs"],"correct_answer":"C"},
  {"question":"Which technology integration approach follows the TPACK framework?","options":["A) Using technology for entertainment","B) Combining technology, pedagogy, and content knowledge","C) Technology-only lessons","D) Avoiding technology completely"],"correct_answer":"B"}
]""",

        "Assessment & Feedback": """[
  {"question":"Which type of assessment is most suitable for monitoring daily learning progress?","options":["A) Annual examinations","B) Formative assessments","C) Standardized tests","D) Peer evaluation only"],"correct_answer":"B"},
  {"question":"What is the most effective way to provide feedback on student work?","options":["A) Grade only with no comments","B) Specific, actionable, and timely feedback","C) General praise without specifics","D) Comparison with other students"],"correct_answer":"B"},
  {"question":"Which assessment strategy best supports differentiated learning?","options":["A) Single format tests for all","B) Multiple assessment formats and options","C) Oral tests only","D) Group assessments exclusively"],"correct_answer":"B"}
]""",

        "Inclusivity, Values & Dispositions": """[
  {"question":"How should a teacher address cultural diversity in the classroom?","options":["A) Ignore cultural differences","B) Incorporate diverse perspectives and examples","C) Use only local examples","D) Separate students by culture"],"correct_answer":"B"},
  {"question":"What is the best approach for supporting students with learning disabilities?","options":["A) Lower expectations for all tasks","B) Provide appropriate accommodations and modifications","C) Exclude them from group activities","D) Give identical support to all students"],"correct_answer":"B"},
  {"question":"Which practice promotes an inclusive classroom environment?","options":["A) Uniform teaching methods for all","B) Recognizing and valuing individual differences","C) Competitive ranking systems","D) Single learning style approach"],"correct_answer":"B"}
]""",

        "Professional Ethics & Teacher Accountability": """[
  {"question":"What should a teacher do when discovering a colleague is not following professional standards?","options":["A) Ignore the situation","B) Report directly to parents","C) Address it professionally through appropriate channels","D) Criticize publicly"],"correct_answer":"C"},
  {"question":"How should confidential student information be handled?","options":["A) Share freely with other teachers","B) Maintain strict confidentiality as per policies","C) Discuss in social settings","D) Post on social media"],"correct_answer":"B"},
  {"question":"What is a teacher's primary ethical responsibility?","options":["A) Completing paperwork on time","B) Ensuring student learning and well-being","C) Following administrator preferences","D) Maintaining personal friendships"],"correct_answer":"B"}
]"""
    }

    return examples.get(module_name, """[
  {"question":"What is an important principle in effective teaching?","options":["A) One-size-fits-all approach","B) Adapting to student needs","C) Rigid adherence to schedules","D) Avoiding student feedback"],"correct_answer":"B"}
]""")

def _validate_module_isolation(questions: list, module_name: str) -> list:
    """Validate that questions are specific to the requested module"""
    validated_questions = []

    # STRICTLY FORBIDDEN CONTENT - Never include these in any questions
    globally_forbidden = [
        "state board grade 5", "grade 5 computer science", "primary school computer",
        "elementary computer science", "basic computer skills grade 5",
        "state syllabus grade 5", "computer fundamentals grade 5"
    ]

    # Keywords that indicate mixing with other modules
    module_keywords = {
        "Subject Knowledge & Content Expertise": {
            "forbidden": ["classroom management", "teaching method", "pedagogy", "assessment strategy",
                         "feedback", "technology", "digital tool", "ethics", "inclusive", "diversity"],
            "required": []  # Relaxed validation - no required keywords
        },
        "Pedagogical Skills & Classroom Practice": {
            "forbidden": ["curriculum content", "mathematical formula", "scientific theory", "technology tool",
                         "assessment rubric", "ethics", "professional conduct"],
            "required": ["teaching", "classroom", "pedagogy", "instruction", "lesson", "student engagement"]
        },
        "Use of Technology & Innovation": {
            "forbidden": ["curriculum content", "classroom management", "assessment method", "ethics"],
            "required": ["technology", "digital", "ICT", "innovation", "tool", "platform"]
        },
        "Assessment & Feedback": {
            "forbidden": ["curriculum content", "teaching method", "technology", "ethics"],
            "required": ["assessment", "feedback", "evaluation", "grading", "rubric"]
        },
        "Inclusivity, Values & Dispositions": {
            "forbidden": ["curriculum content", "teaching method", "technology", "assessment"],
            "required": ["inclusive", "diversity", "cultural", "values", "empathy"]
        },
        "Professional Ethics & Teacher Accountability": {
            "forbidden": ["curriculum content", "teaching method", "technology", "assessment"],
            "required": ["ethics", "professional", "accountability", "conduct", "responsibility"]
        }
    }

    keywords = module_keywords.get(module_name, {"forbidden": [], "required": []})

    for question in questions:
        question_text = question.get("question", "").lower()
        options_text = " ".join(question.get("options", [])).lower()
        full_text = question_text + " " + options_text

        # Check for globally forbidden content first
        has_globally_forbidden = any(forbidden in full_text for forbidden in globally_forbidden)
        if has_globally_forbidden:
            pass  # Skip forbidden content
            continue

        # Check for module-specific forbidden keywords
        has_forbidden = any(keyword in full_text for keyword in keywords["forbidden"])
        # Check for required keywords (at least one should be present)
        has_required = any(keyword in full_text for keyword in keywords["required"]) if keywords["required"] else True

        if not has_forbidden and has_required:
            validated_questions.append(question)
        else:
            pass  # Skip mismatched questions

    return validated_questions

def _create_fallback_questions(module_name: str, board: str, subject: str, grade: str) -> list:
    """No fallback questions - force AI generation to work properly"""
    return []

async def generate_subject_knowledge_questions_ai(
    board: str,
    subject: str,
    grade: str,
    n_questions: int = 10,
    state: str = "Telangana",
    difficulty: str = "medium",
    db_session = None
) -> list[dict]:
    """
    Generate subject knowledge questions using AI with real syllabus from AI Agent

    Args:
        board: Board name (CBSE, State Board, etc.)
        subject: Subject name
        grade: Grade/Class
        n_questions: Number of questions to generate
        state: State name for curriculum (Telangana, AP, etc.)
        difficulty: Question difficulty (easy/medium/hard)
        db_session: Database session for syllabus caching

    Returns:
        List of question dictionaries
    """
    print(f"[AI] Generating {difficulty} difficulty questions for {state} {board} {subject} Grade {grade}")

    # Fetch real syllabus using AI Agent
    syllabus_context = ""
    if db_session:
        try:
            from services.syllabus_service import syllabus_service
            syllabus_data = await syllabus_service.get_syllabus(
                db_session, state, board, grade, subject
            )

            if syllabus_data and 'units' in syllabus_data:
                syllabus_context = "\n📚 REAL CURRICULUM FROM " + state.upper() + " " + board.upper() + ":\n"
                for unit_name, unit_info in syllabus_data['units'].items():
                    syllabus_context += f"\nUnit: {unit_name}\n"
                    if 'topics' in unit_info:
                        syllabus_context += f"Topics: {', '.join(unit_info['topics'][:5])}\n"
                    if 'learning_outcomes' in unit_info:
                        syllabus_context += f"Learning Outcomes: {', '.join(unit_info['learning_outcomes'][:3])}\n"

                print(f"[SYLLABUS] Using real curriculum with {len(syllabus_data['units'])} units")

                # Add delay between syllabus fetch and question generation to avoid rate limits
                print(f"[DELAY] Waiting 3s before question generation to avoid rate limits...")
                await asyncio.sleep(3)
        except Exception as e:
            print(f"[SYLLABUS WARNING] Could not fetch syllabus: {e}")

    # Difficulty level instructions
    difficulty_instructions = {
        "easy": "EASY LEVEL: Basic recall, simple understanding, straightforward concepts",
        "medium": "MEDIUM LEVEL: Application, analysis, moderate complexity",
        "hard": "HARD LEVEL: Complex scenarios, synthesis, evaluation, critical thinking"
    }.get(difficulty, "MEDIUM LEVEL")

    # Language-specific instructions - GENERATE IN NATIVE SCRIPT
    language_instructions = ""
    is_indian_language = subject.lower() in ["telugu", "hindi", "tamil", "kannada", "malayalam", "bengali", "marathi", "gujarati", "urdu"]

    if is_indian_language:
        # Map subjects to their script examples
        script_examples = {
            "telugu": {
                "script": "Telugu (తెలుగు)",
                "example": '{{"question": "\'సంధి\' అంటే ఏమిటి?", "options": ["A) రెండు అక్షరాల కలయిక", "B) రెండు పదాల కలయిక", "C) రెండు వాక్యాల కలయిక", "D) రెండు పద్యాల కలయిక"], "correct_answer": "B"}}'
            },
            "hindi": {
                "script": "Hindi (हिंदी)",
                "example": '{{"question": "\'संधि\' का अर्थ क्या है?", "options": ["A) दो अक्षरों का मेल", "B) दो शब्दों का मेल", "C) दो वाक्यों का मेल", "D) दो पदों का मेल"], "correct_answer": "B"}}'
            },
            "tamil": {
                "script": "Tamil (தமிழ்)",
                "example": '{{"question": "\'புணர்ச்சி\' என்றால் என்ன?", "options": ["A) இரண்டு எழுத்துகளின் இணைப்பு", "B) இரண்டு சொற்களின் இணைப்பு", "C) இரண்டு வாக்கியங்களின் இணைப்பு", "D) இரண்டு பத்திகளின் இணைப்பு"], "correct_answer": "B"}}'
            }
        }

        script_info = script_examples.get(subject.lower(), {"script": f"{subject}", "example": ""})

        language_instructions = f"""
🌐 CRITICAL LANGUAGE REQUIREMENT - READ CAREFULLY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ ALL questions and options MUST be in {script_info['script']} NATIVE SCRIPT
✅ Use ONLY {subject.upper()} language - NO English words
✅ NO transliteration - pure native script only
✅ Write naturally as a native {subject} speaker would write
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 CURRICULUM CONTEXT FOR {board.upper()} BOARD - GRADE {grade}:
{"For Telugu subject in Telangana State Board, the curriculum includes:" if board.lower() in ["telangana", "telangana state", "ts board", "state board"] and subject.lower() == "telugu" else f"For {subject} language subject in {board} Board Grade {grade}, focus on:"}
- {"తెలుగు బాషా పాండిత్యం (Language Proficiency)" if board.lower() in ["telangana", "state board"] and subject.lower() == "telugu" else "Letters/Alphabets and pronunciation (అక్షరాలు/वर्णमाला)"}
- {"వ్యాకరణం: సంధులు, సమాసాలు, అలంకారాలు (Grammar: Sandhi, Samasa, Alankaras)" if board.lower() in ["telangana", "state board"] and subject.lower() == "telugu" else "Grammar concepts appropriate for Grade {grade}"}
- {"పద్య, గద్య పఠనం (Poetry and Prose reading)" if board.lower() in ["telangana", "state board"] and subject.lower() == "telugu" else "Reading comprehension skills"}
- {"వ్యాస రచన, పత్ర లేఖనం (Essay writing, Letter writing)" if board.lower() in ["telangana", "state board"] and subject.lower() == "telugu" else "Writing skills progression"}
- {"పర్యాయపదాలు, వ్యతిరేక పదాలు (Synonyms, Antonyms)" if board.lower() in ["telangana", "state board"] and subject.lower() == "telugu" else "Vocabulary building"}
- {"తెలుగు సాహిత్యం మరియు కవులు (Telugu Literature and Poets)" if board.lower() in ["telangana", "state board"] and subject.lower() == "telugu" else "Literature prescribed in syllabus"}

📝 EXAMPLE FORMAT (MUST FOLLOW THIS PATTERN):
{script_info['example']}

⚠️ IMPORTANT:
- Questions test TEACHER's PURE SUBJECT KNOWLEDGE of {subject} content
- Focus on grammar rules, vocabulary, literature, language concepts
- Grade {grade} appropriate {subject} content from {board} Board
- NO pedagogy - only {subject} language content itself
"""

    prompt = f"""You are an expert {subject} subject matter expert creating assessment questions to test teachers' pure subject knowledge.

Generate {n_questions} multiple-choice questions to test a teacher's DEEP SUBJECT KNOWLEDGE of {subject} content.

SUBJECT CONTEXT:
- Board/Curriculum: {board}
- Subject: {subject}
- Grade/Class: {grade}

🎯 CRITICAL: PURE SUBJECT CONTENT ONLY - NO PEDAGOGY!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Questions MUST test actual {subject} concepts, formulas, theories, facts
✅ Test WHAT content exists in the {subject} curriculum
✅ Focus on subject matter expertise: definitions, relationships, applications
✅ Ask about mathematical/scientific/subject concepts themselves

❌ NO questions about "how to teach" or "teaching methods"
❌ NO questions about "classroom strategies" or "lesson planning"
❌ NO questions about "student misconceptions" or "learning sequences"
❌ NO pedagogical content - ONLY pure {subject} knowledge
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUESTION REQUIREMENTS:
1. Test teacher's SUBJECT MATTER EXPERTISE in {subject} for Grade {grade}
2. Focus on concepts, formulas, definitions, theorems, facts from {subject}
3. Questions should be about PURE {subject} CONTENT KNOWLEDGE
4. Each question must have exactly 4 options (A, B, C, D)
5. Provide correct answer as single letter "A"/"B"/"C"/"D"
6. {"✅ Questions and options MUST be in NATIVE SCRIPT (తెలుగు/हिंदी/தமிழ்) - NO ENGLISH" if is_indian_language else "Questions and options MUST be in ENGLISH"}

EXAMPLE FORMAT (for Mathematics - PURE SUBJECT CONTENT):
[
  {{"question": "What is the relationship between the sides of a right triangle?", "options": ["A) a + b = c", "B) a² + b² = c²", "C) a × b = c", "D) a² - b² = c²"], "correct_answer": "B"}},
  {{"question": "Which property states that a × (b + c) = (a × b) + (a × c)?", "options": ["A) Commutative property", "B) Associative property", "C) Distributive property", "D) Identity property"], "correct_answer": "C"}},
  {{"question": "What is the formula for the area of a circle?", "options": ["A) 2πr", "B) πr²", "C) πd", "D) 2πr²"], "correct_answer": "B"}}
]

EXAMPLE FORMAT (for Science - PURE SUBJECT CONTENT):
[
  {{"question": "What is the chemical formula for water?", "options": ["A) H₂O", "B) CO₂", "C) NaCl", "D) O₂"], "correct_answer": "A"}},
  {{"question": "Which force pulls objects toward the Earth?", "options": ["A) Magnetic force", "B) Electric force", "C) Gravitational force", "D) Friction"], "correct_answer": "C"}}
]

{language_instructions if language_instructions else ""}

{syllabus_context if syllabus_context else ""}

🎯 DIFFICULTY LEVEL: {difficulty_instructions}

{"🔴 FINAL REMINDER: Return ONLY a JSON array. ALL questions/options in NATIVE " + subject.upper() + " SCRIPT. NO English words." if is_indian_language else "Return ONLY a JSON array of " + str(n_questions) + " questions. No additional text. ALL text must be in English."}
"""

    # Use the requests-based function
    response_content = generate_subject_knowledge_questions_ai_requests(prompt)

    if response_content.startswith("Error") or response_content.startswith("Exception"):
        print(f"[ERROR] OpenRouter API call failed: {response_content}")
        return await generate_basic_fallback_questions(
            subject=subject,
            grade=grade,
            board=board,
            state=state,
            difficulty=difficulty,
            n_questions=n_questions,
            is_indian_language=is_indian_language
        )

    content = response_content.strip()

    # Extract JSON from response - handle potential markdown code blocks and backticks
    if content.startswith('```json'):
        content = content[7:]
    if content.startswith('```'):
        content = content[3:]
    if content.endswith('```'):
        content = content[:-3]

    # Remove single backticks that wrap the JSON
    if content.startswith('`') and content.endswith('`'):
        content = content[1:-1]

    content = content.strip()

    # Extract JSON array
    start = content.find('[')
    end = content.rfind(']') + 1

    if start >= 0 and end > start:
        json_str = content[start:end]

        # Try to fix common JSON issues
        try:
            questions = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"[WARNING] JSON parse error: {e}")
            print(f"[DEBUG] Attempting to fix JSON...")

            # Try to fix by removing potential trailing commas and fixing quotes
            import re
            json_str = re.sub(r',\s*}', '}', json_str)  # Remove trailing commas in objects
            json_str = re.sub(r',\s*]', ']', json_str)  # Remove trailing commas in arrays

            try:
                questions = json.loads(json_str)
                print(f"[SUCCESS] Fixed JSON and parsed successfully")
            except json.JSONDecodeError as e2:
                print(f"[ERROR] Could not fix JSON: {e2}")
                print(f"[DEBUG] Problematic JSON snippet: {json_str[max(0, e2.pos-100):min(len(json_str), e2.pos+100)]}")
                return []

        if isinstance(questions, list) and len(questions) > 0:
            print(f"[AI] Successfully generated {len(questions)} questions for {subject}")
            # Validate all questions have required fields
            valid_questions = []
            for q in questions:
                if isinstance(q, dict) and q.get("question") and q.get("options") and q.get("correct_answer"):
                    valid_questions.append(q)
                else:
                    print(f"[WARNING] Skipping invalid question: {q}")

            if len(valid_questions) > 0:
                print(f"[DEBUG] Returning {len(valid_questions)} valid questions")
                return valid_questions
            else:
                print(f"[ERROR] No valid questions found after validation")
                return []
        else:
            print(f"[ERROR] Questions list is empty or invalid")
            return []
    else:
        print(f"[ERROR] Failed to parse AI response as JSON array")
        print(f"[DEBUG] Response preview: {content[:500]}")
        return []

async def generate_basic_fallback_questions(
    subject: str,
    grade: str,
    board: str,
    state: str,
    difficulty: str,
    n_questions: int,
    is_indian_language: bool
) -> list[dict]:
    """
    AI-powered fallback when rate limited.
    Skips syllabus fetching, uses only general knowledge + basic context.
    Single API call - reduces rate limit risk.
    """
    print(f"[FALLBACK AI] Generating {difficulty} {subject} questions for grade {grade} without syllabus")

    # Determine if native language script needed
    script_examples = {
        "telugu": {
            "script": "Telugu (తెలుగు)",
            "example": '{{"question": "తరగతి ' + grade + ' విద్యార్థులకు తెలుగు వ్యాకరణం నేర్పేటప్పుడు మొదట ఏమి నేర్పాలి?", "options": ["అ) అచ్చులు", "ఆ) హల్లులు", "ఇ) పదాలు", "ఈ) వాక్యాలు"], "correct_answer": "A"}}'
        },
        "hindi": {
            "script": "Hindi (हिंदी)",
            "example": '{{"question": "कक्षा ' + grade + ' के छात्रों को हिंदी व्याकरण सिखाते समय पहले क्या पढ़ाना चाहिए?", "options": ["A) स्वर", "B) व्यंजन", "C) शब्द", "D) वाक्य"], "correct_answer": "A"}}'
        },
        "tamil": {
            "script": "Tamil (தமிழ்)",
            "example": '{{"question": "வகுப்பு ' + grade + ' மாணவர்களுக்கு தமிழ் இலக்கணம் கற்பிக்கும்போது முதலில் என்ன கற்பிக்க வேண்டும்?", "options": ["அ) உயிர் எழுத்துக்கள்", "ஆ) மெய் எழுத்துக்கள்", "இ) சொற்கள்", "ஈ) வாக்கியங்கள்"], "correct_answer": "A"}}'
        }
    }

    language_key = subject.lower()
    script_info = script_examples.get(language_key)

    if is_indian_language and script_info:
        language_instructions = f"""
🌐 CRITICAL LANGUAGE REQUIREMENT:
✅ ALL questions and options MUST be in {script_info['script']} NATIVE SCRIPT
✅ Use ONLY {subject.upper()} language - NO English words
✅ Write naturally as a native {subject} speaker would write

Example format:
{script_info['example']}
"""
    else:
        language_instructions = "Write questions in English."

    # Difficulty-based complexity
    difficulty_guidance = {
        "easy": "Basic recall and understanding. Focus on fundamental concepts and simple applications.",
        "medium": "Application and analysis. Require deeper understanding and practical knowledge.",
        "hard": "Advanced analysis, synthesis, and evaluation. Include complex scenarios and nuanced understanding."
    }

    complexity = difficulty_guidance.get(difficulty, difficulty_guidance["medium"])

    # Simplified prompt without syllabus context
    prompt = f"""You are an expert {board} board teacher for grade {grade} {subject} in {state}.

Generate {n_questions} pedagogically sound MCQ questions to test a TEACHER's subject knowledge.

{language_instructions}

DIFFICULTY LEVEL: {difficulty.upper()}
{complexity}

CONTEXT:
- Board: {board}
- State: {state}
- Grade Level: {grade}
- Subject: {subject}

Questions should test teacher's understanding of:
1. Core subject concepts appropriate for grade {grade}
2. Common teaching approaches
3. Student misconceptions
4. Effective explanations

Return ONLY a valid JSON array with this EXACT structure:
[
  {{
    "question": "Your question text here",
    "options": ["A) First option", "B) Second option", "C) Third option", "D) Fourth option"],
    "correct_answer": "A"
  }}
]

REQUIREMENTS:
- Exactly {n_questions} questions
- Each question must have exactly 4 options (A, B, C, D)
- correct_answer must be "A", "B", "C", or "D"
- NO markdown, NO explanations, ONLY the JSON array
"""

    # The API key is already loaded by load_dotenv in main.py
    # and used by generate_subject_knowledge_questions_ai_requests

    response_content = generate_subject_knowledge_questions_ai_requests(prompt)

    if response_content.startswith("Error") or response_content.startswith("Exception"):
        print(f"[FALLBACK AI ERROR] OpenRouter API call failed: {response_content}")
        return []

    content = response_content.strip()

    # Clean markdown and backticks
    if content.startswith('```json'):
        content = content[7:]
    if content.startswith('```'):
        content = content[3:]
    if content.endswith('```'):
        content = content[:-3]
    # Remove single backticks that wrap the JSON
    if content.startswith('`') and content.endswith('`'):
        content = content[1:-1]
    content = content.strip()

    # Extract JSON
    start = content.find('[')
    end = content.rfind(']') + 1

    if start >= 0 and end > start:
        json_str = content[start:end]

        # Fix common JSON issues
        import re
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)

        try:
            questions = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"[WARNING] JSON parse error in fallback: {e}")
            print(f"[DEBUG] Attempting to fix JSON in fallback...")
            # Try to fix by removing potential trailing commas and fixing quotes
            json_str = re.sub(r',\s*}', '}', json_str)  # Remove trailing commas in objects
            json_str = re.sub(r',\s*]', ']', json_str)  # Remove trailing commas in arrays
            try:
                questions = json.loads(json_str)
                print(f"[SUCCESS] Fixed JSON in fallback and parsed successfully")
            except json.JSONDecodeError as e2:
                print(f"[ERROR] Could not fix JSON in fallback: {e2}")
                print(f"[DEBUG] Problematic JSON snippet: {json_str[max(0, e2.pos-100):min(len(json_str), e2.pos+100)]}")
                return []

        if isinstance(questions, list) and len(questions) > 0:
            print(f"[FALLBACK AI] Successfully generated {len(questions)} questions")
            return questions

    print("[FALLBACK AI] Failed to parse response")
    return []

async def generate_mcqs(
    profile: dict,
    module_name: str,
    board: str,
    n_questions: int = 10,
    state: str = "Telangana",
    difficulty: str = "medium",
    db_session = None
) -> list[dict]:
    """
    Returns a list of dicts: [{"question": "...", "options": ["A","B","C","D"], "correct_answer": "B"}, ...]

    NEW: Now supports AI Agent with state-specific curriculum fetching and difficulty levels
    """
    # Get curriculum data for enhanced question generation
    subjects_teaching = profile.get('subjects_teaching', '')
    grades_teaching = profile.get('grades_teaching', '')

    # Extract primary subject and grade for curriculum lookup
    primary_subject = subjects_teaching.split(',')[0].strip() if subjects_teaching else 'Mathematics'
    primary_grade = grades_teaching.split(',')[0].strip() if grades_teaching else '5'

    # Get grade number for age-appropriate questions
    grade_num = curriculum_service._normalize_grade(primary_grade)

    # For Subject Knowledge module, use AI Agent with real syllabus
    if module_name == "Subject Knowledge & Content Expertise":
        return await generate_subject_knowledge_questions_ai(
            board=board,
            subject=primary_subject,
            grade=primary_grade,
            n_questions=n_questions,
            state=state,
            difficulty=difficulty,
            db_session=db_session
        )

    # For other modules, use standard teacher evaluation approach
    curriculum_data = curriculum_service.get_enhanced_curriculum_context(board, primary_subject, primary_grade)

    # Create module-specific prompts
    module_descriptions = {
        "Subject Knowledge & Content Expertise": f"""
FOCUS AREA: {module_name}
Generate questions ONLY about subject mastery, curriculum knowledge, and content expertise specific to {board} board.

[CURRICULUM] CURRICULUM-BASED CONTENT:
{_format_curriculum_context(curriculum_data, board, primary_subject, primary_grade)}

Question Areas (ALL must be related to {module_name}):
1. Deep knowledge of {board} syllabus for {profile.get('subjects_teaching')} in grades {profile.get('grades_teaching')}
2. Understanding of topic sequence and prerequisite concepts as per {board} curriculum
3. Knowledge of learning outcomes and competencies for specific topics in {board} standards
4. Cross-curricular connections within {profile.get('subjects_teaching')} subjects
5. Application of subject knowledge to real-world contexts as per {board} guidelines
6. Understanding of common student misconceptions in {profile.get('subjects_teaching')}
7. Unit-wise weightage and assessment patterns as per official {board} guidelines
8. Competency framework and learning outcomes for each curriculum unit

STRICT REQUIREMENTS:
- ALL questions must be about SUBJECT KNOWLEDGE & CONTENT EXPERTISE only
- NO questions about classroom management, teaching methods, or other modules
- Focus on curriculum content, concept mastery, and subject-specific knowledge
- Questions must test what teachers should KNOW about their subject content per {board} standards
- Use REAL curriculum data, unit weightages, and official learning outcomes
- Questions should reflect actual assessment patterns and competency frameworks""",

        "Pedagogical Skills & Classroom Practice": f"""
FOCUS AREA: {module_name}
Generate questions ONLY about lesson planning, classroom management, and student engagement techniques.

STRICT REQUIREMENTS:
- ALL questions must be about PEDAGOGICAL SKILLS & CLASSROOM PRACTICE only
- NO questions about subject content, curriculum knowledge, or academic topics
- NO questions about technology, assessment, ethics, or inclusivity
- Focus ONLY on teaching methods, classroom strategies, and pedagogical approaches
- Questions about lesson structure, student engagement, classroom management, teaching strategies""",

        "Use of Technology & Innovation": f"""
FOCUS AREA: {module_name}
Generate questions ONLY about ICT integration, digital tools, and innovative teaching methods.

STRICT REQUIREMENTS:
- ALL questions must be about TECHNOLOGY & INNOVATION only
- NO questions about subject content, pedagogy, assessment, or ethics
- Focus ONLY on digital tools, educational technology, ICT integration
- Questions about educational apps, online platforms, digital resources, tech-enhanced learning""",

        "Assessment & Feedback": f"""
FOCUS AREA: {module_name}
Generate questions ONLY about formative/summative assessment and constructive feedback strategies.

STRICT REQUIREMENTS:
- ALL questions must be about ASSESSMENT & FEEDBACK only
- NO questions about subject content, teaching methods, technology, or ethics
- Focus ONLY on evaluation methods, feedback techniques, assessment tools
- Questions about grading, rubrics, peer assessment, self-assessment, feedback delivery""",

        "Inclusivity, Values & Dispositions": f"""
FOCUS AREA: {module_name}
Generate questions ONLY about diversity sensitivity, empathy, and inclusive teaching practices.

STRICT REQUIREMENTS:
- ALL questions must be about INCLUSIVITY, VALUES & DISPOSITIONS only
- NO questions about subject content, teaching methods, technology, or assessment
- Focus ONLY on diversity, inclusion, empathy, cultural sensitivity
- Questions about supporting diverse learners, inclusive practices, cultural awareness""",

        "Professional Ethics & Teacher Accountability": f"""
FOCUS AREA: {module_name}
Generate questions ONLY about integrity, teacher conduct, and professional responsibility.

STRICT REQUIREMENTS:
- ALL questions must be about PROFESSIONAL ETHICS & ACCOUNTABILITY only
- NO questions about subject content, teaching methods, technology, or assessment
- Focus ONLY on ethical conduct, professional standards, accountability
- Questions about teacher responsibilities, ethical dilemmas, professional boundaries"""
    }

    module_focus = module_descriptions.get(module_name, f"""
FOCUS AREA: {module_name}
Generate questions specifically about: {module_name}
""")

    prompt = f"""
You are an expert teacher evaluator for {board} education board curriculum.
Generate {n_questions} multiple-choice questions for teacher assessment.

Teacher Profile:
- Education: {profile.get('education')}
- Grades Teaching: {profile.get('grades_teaching')}
- Subjects Teaching: {profile.get('subjects_teaching')}
- Experience (years): {profile.get('experience_years')}
- Board/Curriculum: {board}

{module_focus}

Board-Specific Context:
- For CBSE: Use NCERT curriculum, learning outcomes, competency-based approach (CBE)
  * Theory Exam: 80 marks (40% MCQs, 40% Short/Long Answer, 20% Competency-based)
  * Internal Assessment: 20 marks
  * Focus on Conceptual Understanding, Procedural Fluency, Problem Solving, Reasoning, Communication
- For State Board: Use state-specific curriculum and local educational context
- For ICSE: Use CISCE curriculum standards and evaluation patterns
- For IB/IGCSE: Use international curriculum standards

[CURRICULUM] REAL CURRICULUM DATA INTEGRATION:
{_format_assessment_guidelines(curriculum_data) if module_name == 'Subject Knowledge & Content Expertise' else 'Focus strictly on module-specific content only'}

[CRITICAL] RULES - STRICTLY ENFORCE:
- Generate questions ONLY for the module: "{module_name}"
- Do NOT mix questions from other teacher evaluation modules
- ABSOLUTELY NO questions about other modules (if generating for Subject Knowledge, NO pedagogy questions; if generating for Pedagogy, NO subject content questions)
- All questions must be specific to {board} board curriculum
- Test knowledge relevant to grades {profile.get('grades_teaching')} and subjects {profile.get('subjects_teaching')}
- Each question MUST have exactly 4 options
- Provide correct answer as single letter "A"/"B"/"C"/"D"
- Return STRICT JSON array only, no commentary

[GUIDELINES] QUESTION WRITING GUIDELINES:
- Write CLEAN, PROFESSIONAL questions without curriculum meta-references
- NEVER start questions with "According to [Board] curriculum..." or "In [Board] Grade [X]..."
- NEVER mention board names, grade levels, or curriculum references in question text
- Write direct, clear questions that test knowledge naturally
- Focus on concepts, skills, and best practices rather than policy knowledge
- Questions should sound like professional teacher assessment items

FORBIDDEN TOPICS FOR THIS MODULE "{module_name}":
{_get_forbidden_topics(module_name)}

Example questions based on EXACT module "{module_name}":
{_get_module_specific_examples(module_name, board, primary_grade, primary_subject)}

FINAL VALIDATION CHECKLIST:
Before generating questions, verify EVERY question meets these criteria:
1. Question is ONLY about "{module_name}"
2. Question does NOT mention topics from other modules
3. Question tests knowledge specific to this module only
4. Question follows {board} curriculum standards
5. All 4 options are plausible and module-specific
"""
    response_content = generate_subject_knowledge_questions_ai_requests(prompt)

    if response_content.startswith("Error") or response_content.startswith("Exception"):
        print(f"[ERROR] OpenRouter API call failed: {response_content}")
        return []

    content = response_content
    try:
        # Try to extract JSON from the response if it contains other text
        start = content.find('[')
        end = content.rfind(']') + 1
        if start >= 0 and end > start:
            json_str = content[start:end]
            questions = json.loads(json_str)
            assert isinstance(questions, list)
        else:
            questions = json.loads(content)
            assert isinstance(questions, list)

        # Validate questions are module-specific
        questions = _validate_module_isolation(questions, module_name)

    except Exception as e:
        print(f"Error parsing questions: {e}")
        # DEBUG: Show actual response to understand the issue
        print(f"[DEBUG] Raw API response length: {len(content)} chars")
        print(f"[DEBUG] Raw API response preview (first 1000 chars):")
        print(content[:1000])

        # Check if response appears truncated
        if not content.strip().endswith(']'):
            print(f"[WARNING] Response appears truncated - does not end with ']'")
            print(f"[DEBUG] Last 200 chars: {content[-200:]}")

        print(f"[DEBUG] Attempting to fix JSON with more aggressive repair...")

        # Try more aggressive JSON fixing
        try:
            import re
            # Remove any text before the first [
            start = content.find('[')
            end = content.rfind(']')

            if start < 0:
                print(f"[ERROR] No opening bracket '[' found in response")
                questions = []
                return questions

            if end < 0 or end <= start:
                print(f"[ERROR] Response truncated - attempting to close JSON...")
                # Try to find the last complete question object
                json_str = content[start:]
                # Find the last complete object by looking for the last }}
                last_complete = json_str.rfind('}}')
                if last_complete > 0:
                    json_str = json_str[:last_complete + 2] + ']'
                    print(f"[DEBUG] Attempting to parse truncated JSON with {len(json_str)} chars...")
                else:
                    print(f"[ERROR] Cannot find any complete question objects")
                    questions = []
                    return questions
            else:
                json_str = content[start:end + 1]

            # Fix common issues
            json_str = re.sub(r',\s*}', '}', json_str)  # Remove trailing commas in objects
            json_str = re.sub(r',\s*]', ']', json_str)  # Remove trailing commas in arrays
            json_str = re.sub(r'}\s*{', '},{', json_str)  # Add commas between objects

            print(f"[DEBUG] Attempting to parse cleaned JSON...")
            questions = json.loads(json_str)
            print(f"[SUCCESS] Managed to parse {len(questions)} questions after aggressive repair!")
            return questions
        except Exception as repair_error:
            print(f"[ERROR] Aggressive repair also failed: {repair_error}")

        questions = []
    return questions

async def generate_curriculum_questions(subject: str, grade: str, grade_num: int, board: str, n_questions: int = 10) -> list[dict]:
    """
    Generate curriculum-specific questions for Subject Knowledge & Content Expertise module
    Returns mixed format questions without board labels
    """

    print(f"[DEBUG] generate_curriculum_questions called: board={board}, subject={subject}, grade={grade}")

    # Get curriculum data
    curriculum_data = curriculum_service.get_curriculum_data(board, subject, grade)

    print(f"[DEBUG] Curriculum data available: {bool(curriculum_data)}, has units: {bool(curriculum_data and 'units' in curriculum_data)}")

    if not curriculum_data or 'units' not in curriculum_data:
        print(f"[WARNING] No curriculum data found for {board}/{subject}/{grade}, generating questions using AI without curriculum context")
        # Use AI to generate questions even without curriculum data
        return await generate_subject_knowledge_questions_ai(board, subject, grade, n_questions)

    # Generate only MCQ questions for assessment system
    question_types = [
        {"type": "mcq", "count": n_questions}
    ]

    # Create context appropriate for the grade level
    if grade_num <= 5:
        context_level = "primary"
        vocabulary = "simple, everyday language"
        examples = "toys, games, family, school activities"
    elif grade_num <= 8:
        context_level = "middle"
        vocabulary = "grade-appropriate terminology"
        examples = "school projects, sports, daily activities"
    else:
        context_level = "secondary"
        vocabulary = "subject-specific terminology"
        examples = "real-world applications, practical scenarios"

    # Get available units
    units = list(curriculum_data['units'].keys())

    prompt = f"""
You are creating {n_questions} multiple-choice questions to evaluate teacher knowledge of {subject} curriculum content expertise.

CURRICULUM KNOWLEDGE AREAS:
{_format_curriculum_units(curriculum_data)}

TEACHER EVALUATION FOCUS:
- Test teacher's mastery of subject content knowledge
- Evaluate understanding of curriculum scope and sequence
- Assess knowledge of learning objectives and outcomes
- Test awareness of prerequisite concepts and connections

CRITICAL INSTRUCTIONS:
- Create EXACTLY {n_questions} multiple-choice questions
- NO mention of board names, curriculum standards, or grade references in questions
- Focus on subject content knowledge teachers should possess
- Test conceptual understanding, not policy knowledge
- Each question must have exactly 4 options (A, B, C, D)

REQUIRED JSON FORMAT:
[
  {{"question": "Which mathematical concept should be taught before introducing quadratic equations?", "options": ["A) Coordinate geometry", "B) Linear equations and factorization", "C) Statistics and probability", "D) Mensuration"], "correct_answer": "B"}},
  {{"question": "What is the most effective sequence for teaching algebraic expressions?", "options": ["A) Start with complex polynomials", "B) Begin with basic operations and simple terms", "C) Jump directly to factorization", "D) Focus only on word problems"], "correct_answer": "B"}}
]

Create {n_questions} subject knowledge questions now. Return only the JSON array.
"""

    response_content = generate_subject_knowledge_questions_ai_requests(prompt)

    if response_content.startswith("Error") or response_content.startswith("Exception"):
        print(f"[ERROR] OpenRouter API call failed: {response_content}")
        return []

    content = response_content
    try:
        # Extract JSON from response
        start = content.find('[')
        end = content.rfind(']') + 1
        print(f"[DEBUG] Content length: {len(content)}, JSON start: {start}, end: {end}")
        if start >= 0 and end > start:
            json_str = content[start:end]
            questions = json.loads(json_str)
            assert isinstance(questions, list)
        else:
            questions = json.loads(content)
            assert isinstance(questions, list)

        print(f"[DEBUG] Parsed {len(questions)} questions from API")

        # Light validation - only remove clearly problematic questions
        validated_questions = []
        for i, q in enumerate(questions):
            if isinstance(q, dict) and q.get("question"):
                # Only filter out questions with explicit board mentions
                question_text = str(q.get("question", "")).lower()
                if "state board" in question_text or "cbse" in question_text or "ncert" in question_text:
                    print(f"[DEBUG] Question {i} filtered (board mention): {question_text[:80]}")
                    continue
                validated_questions.append(q)
            else:
                print(f"[DEBUG] Question {i} filtered (invalid format): {q}")

        print(f"[AI] Generated {len(validated_questions)} questions successfully")

        # If we don't have enough questions, try to get more from AI
        if len(validated_questions) < n_questions:
            print(f"Only got {len(validated_questions)}/{n_questions} questions - using what we have")

        return validated_questions[:n_questions] if validated_questions else []

    except Exception as e:
        print(f"Error parsing curriculum questions: {e}")
        # DEBUG: Safe Unicode content debugging
        # print(f"Raw content length: {len(content)} chars")
        # print(f"Content preview: {content[:200].encode('ascii', 'replace').decode('ascii')}...")
        # Force AI to work - no fallbacks allowed
        return []

def _format_curriculum_units(curriculum_data: dict) -> str:
    """Format curriculum units for prompt"""
    if 'units' not in curriculum_data:
        return "Standard curriculum topics"

    units_text = ""
    for unit_name, unit_data in curriculum_data['units'].items():
        units_text += f"\n- {unit_name}"
        if 'topics' in unit_data:
            topics = unit_data['topics'][:3]  # Show first 3 topics
            units_text += f": {', '.join(topics)}"

    return units_text

def _format_question_types(question_types: list) -> str:
    """Format question type distribution"""
    distribution = ""
    for qt in question_types:
        distribution += f"\n- {qt['count']} {qt['type'].replace('_', ' ').title()} questions"

    return distribution

def _validate_curriculum_questions(questions: list, subject: str, grade_num: int) -> list:
    """Validate curriculum questions for appropriateness"""
    validated = []

    # Forbidden terms that shouldn't appear in questions
    forbidden_terms = [
        "cbse", "icse", "ncert", "state board", "curriculum", "syllabus",
        "according to", " board ", "ncert", "textbook", "as per", "guidelines",
        "grade 10", "class 9", "class 10", "grade 9", "higher secondary", "board exam",
        "curriculum standard", "learning outcome", "assessment pattern", "official",
        "prescribed by", "mentioned in", "specified in", "based on curriculum",
        "grade 1", "grade 2", "grade 3", "grade 4", "grade 5", "grade 6",
        "grade 7", "grade 8", "grade 11", "grade 12", "class 1", "class 2",
        "class 3", "class 4", "class 5", "class 6", "class 7", "class 8",
        "class 11", "class 12"
    ]

    for question in questions:
        if not isinstance(question, dict):
            continue

        question_text = str(question.get("question", "")).lower()

        # Check for forbidden terms
        has_forbidden = False
        for term in forbidden_terms:
            if term in question_text:
                pass  # Skip forbidden terms
                has_forbidden = True
                break

        if has_forbidden:
            continue

        # Check if question is age-appropriate length (more lenient)
        if len(question_text.split()) > 40:  # Too complex
            pass  # Skip long questions
            continue

        validated.append(question)

    return validated

def _create_mixed_fallback_questions(subject: str, grade: str, count: int) -> list:
    """No fallback questions - AI must work properly"""
    return []
