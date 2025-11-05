# CURRENT ASSESSMENT SYSTEM - HOW IT WORKS

**Analysis Date**: 2025-11-04
**System**: Learnify Teach Platform

---

## OVERVIEW

The current system generates **MCQ assessments for teachers** (not students) to test their subject knowledge as part of professional development modules. Here's how it works:

---

## 1. CURRENT ARCHITECTURE

### **A. Question Generation Flow**

```
Teacher Profile → Module Selection → AI Question Generator → Database → Frontend Display
```

**Key Components**:
1. **Teacher Profile Data**: Grades teaching, subjects, board (CBSE/State), experience
2. **Module System**: 9 professional development modules (Subject Knowledge, Pedagogy, etc.)
3. **AI Generator**: OpenRouter API (GPT-4o-mini) generates MCQs
4. **Database Storage**: Questions saved to `assessment_questions` table
5. **Assessment Session**: Timed sessions with attempt tracking

---

## 2. HOW QUESTIONS ARE CURRENTLY GENERATED

### **File**: `/backend/routers/assessments.py`

**Endpoint**: `POST /assessment/generate/{module_id}`

**Process**:

#### Step 1: Get Teacher Context
```python
profile_data = {
    "education": profile.education,
    "grades_teaching": profile.grades_teaching,  # e.g., "9,10"
    "subjects_teaching": profile.subjects_teaching,  # e.g., "Mathematics,Science"
    "experience_years": profile.experience_years,
    "board": "CBSE",
    "state": "Telangana"
}
```

#### Step 2: Call AI Generator
```python
# For Module 1 (Subject Knowledge):
questions = await generate_enhanced_module1_questions(
    teacher_profile=profile_data,
    board=board,
    state=state,
    n_questions=8
)

# For other modules:
questions = await generate_mcqs(
    profile_data,
    module.name,
    board,
    n_questions=8,
    state=state,
    difficulty="mixed"
)
```

#### Step 3: AI Prompt Structure

**File**: `/backend/services/ai_question_generator.py`

```python
prompt = f"""
You are an expert {board} Class {class_name} {subject} question paper setter.

Using the following OFFICIAL CBSE SYLLABUS CONTENT for "{chapter}",
generate {num_questions} high-quality MCQs.

OFFICIAL CBSE SYLLABUS CONTENT:
{syllabus_content[:3000]}  # Uses actual syllabus if available

REQUIREMENTS:
- Questions MUST be based on specific syllabus content
- Follow CBSE exam pattern and marking scheme
- Include conceptual, application, and analytical questions
- Vary difficulty: 30% easy, 50% medium, 20% hard

Output valid JSON array:
[
  {{
    "question": "What is the HCF of 12 and 18?",
    "options": {{"A": "2", "B": "3", "C": "6", "D": "12"}},
    "correct_answer": "C",
    "difficulty": "easy"
  }}
]
"""
```

#### Step 4: Save to Database
```python
aq = AssessmentQuestion(
    teacher_id=user.id,
    module_id=module_id,
    question=q.get("question"),
    options_json=json.dumps(norm_opts),
    correct_answer=q.get("correct_answer")
)
db.add(aq)
```

---

## 3. CURRENT DATABASE SCHEMA

### **Table**: `assessment_questions`
```sql
CREATE TABLE assessment_questions (
    id SERIAL PRIMARY KEY,
    teacher_id INTEGER REFERENCES users(id),
    module_id INTEGER REFERENCES modules(id),
    question TEXT NOT NULL,
    options_json TEXT,  -- JSON array of 4 options
    correct_answer VARCHAR(1),  -- A, B, C, or D
    created_at TIMESTAMP DEFAULT NOW()
);
```

### **Table**: `assessment_responses`
```sql
CREATE TABLE assessment_responses (
    id SERIAL PRIMARY KEY,
    teacher_id INTEGER,
    module_id INTEGER,
    question_id INTEGER REFERENCES assessment_questions(id),
    selected_answer VARCHAR(1),
    is_correct BOOLEAN,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### **Table**: `assessment_sessions` (Phase 2)
```sql
CREATE TABLE assessment_sessions (
    id SERIAL PRIMARY KEY,
    teacher_id INTEGER,
    module_id INTEGER,
    attempt_number INTEGER,
    started_at TIMESTAMP,
    expires_at TIMESTAMP,
    questions_json JSONB,  -- Stores all questions for this session
    is_active BOOLEAN DEFAULT TRUE,
    submitted_at TIMESTAMP
);
```

---

## 4. CURRENT FEATURES

### **A. Question Generation**
✅ **AI-Powered**: Uses OpenRouter API (GPT-4o-mini)
✅ **Context-Aware**: Takes teacher profile, board, state into account
✅ **Syllabus-Aligned**: Can accept syllabus content as context
✅ **Bloom's Taxonomy**: Module 1 uses Bloom's levels (Remember, Understand, Apply, Analyze, Evaluate, Create)
✅ **Difficulty Variation**: Generates mix of easy, medium, hard questions

### **B. Assessment Execution**
✅ **Timed Sessions**: 15-30 minutes per assessment
✅ **Auto-Fail on Timeout**: If time expires, score = 0
✅ **Attempt Tracking**: Records all attempts with timestamps
✅ **Cooldown Period**: 24-hour wait between attempts
✅ **Monthly Limits**: Max 3 attempts per module per month

### **C. Feedback & Analytics**
✅ **Immediate Scoring**: Auto-graded MCQs
✅ **AI-Generated Explanations**: For each question (Phase 3)
✅ **Weak Topic Identification**: Identifies topics with 2+ incorrect answers
✅ **Performance Tracking**: Best score, average score, improvement rate
✅ **Attempt History**: Full history of all attempts

---

## 5. WHAT'S MISSING (For Student Assessments)

### **Current System** (Teacher Professional Development):
- ❌ No NCERT content integration
- ❌ No chapter-specific question generation
- ❌ No student-facing assessments
- ❌ No question bank management
- ❌ No teacher-created assessments
- ❌ No blueprint-based generation
- ❌ No CBSE syllabus mapping
- ❌ No multi-question-type support (only MCQs)

### **What We Need to Add** (For Students):

1. **NCERT Content Integration**
   - Query `ncert_textbook_content` table
   - Extract relevant sections for questions
   - Use examples and exercises as source material

2. **Chapter-Specific Generation**
   - Select chapters from dropdown
   - Generate questions from those chapters only
   - Reference NCERT page numbers

3. **Blueprint-Based System**
   - Define marks distribution
   - Define question type distribution (MCQ, Short, Long, Case)
   - Define difficulty distribution
   - Define Bloom's level distribution

4. **Question Types**
   - MCQ (1 mark)
   - Short Answer (2-3 marks)
   - Long Answer (5 marks)
   - Case-Based (4-5 marks)
   - Assertion-Reasoning
   - Fill in the blanks
   - Match the following

5. **Teacher Assessment Builder**
   - UI wizard for creating assessments
   - Chapter selection from NCERT database
   - Blueprint configuration
   - Question preview and editing
   - PDF export
   - Answer key generation

---

## 6. HOW CURRENT SYSTEM GENERATES QUESTIONS

### **Example Flow**:

**Input**:
```json
{
  "teacher_id": 123,
  "module_id": 1,
  "profile": {
    "grades_teaching": "9,10",
    "subjects_teaching": "Mathematics",
    "board": "CBSE"
  }
}
```

**AI Prompt Sent**:
```
Generate 8 MCQs for CBSE Class 9-10 Mathematics teachers.
Focus on Subject Knowledge & Content Expertise.
Include questions on:
- Real Numbers (Bloom's: Understand, Apply)
- Polynomials (Bloom's: Apply, Analyze)
- Linear Equations (Bloom's: Remember, Apply)

Mix difficulty: 30% easy, 50% medium, 20% hard
```

**AI Response**:
```json
[
  {
    "question": "The decimal expansion of 22/7 is:",
    "options": {
      "A": "Terminating",
      "B": "Non-terminating repeating",
      "C": "Non-terminating non-repeating",
      "D": "Cannot be determined"
    },
    "correct_answer": "B",
    "difficulty": "easy"
  },
  ... 7 more questions
]
```

**Stored in Database**: 8 questions saved with `teacher_id=123`, `module_id=1`

**Displayed to Teacher**: Multiple choice quiz interface

**Submission**: Teacher submits answers → Auto-graded → Score & feedback shown

---

## 7. KEY DIFFERENCES: CURRENT vs NEEDED

| Feature | Current System | Needed for Students |
|---------|---------------|-------------------|
| **Purpose** | Teacher professional development | Student assessments |
| **Users** | Teachers only | Teachers create, Students take |
| **Question Source** | Generic syllabus prompts | NCERT textbook content |
| **Question Types** | MCQ only | MCQ, Short, Long, Case-based |
| **Content Base** | AI-generated from scratch | NCERT chapters (467 extracted) |
| **Customization** | Fixed 8 questions per module | Teacher defines count, types, marks |
| **Blueprint** | No blueprint | Full blueprint support |
| **Syllabus Mapping** | Generic board/state | Specific NCERT chapters |
| **Assessment Builder** | No UI for teachers | Full wizard UI needed |
| **Question Bank** | Temporary (per session) | Persistent, reusable bank |
| **PDF Export** | No | Yes, with answer key |
| **Marking Scheme** | Simple correct/incorrect | Stepwise marking rubric |

---

## 8. CURRENT LIMITATIONS

### **For Student Assessment Use**:

1. **No NCERT Integration**:
   - Current system doesn't query `ncert_textbook_content` table
   - Questions are generated generically, not from specific chapters
   - No way to select specific NCERT chapters

2. **Limited Question Types**:
   - Only MCQs supported
   - No short answer, long answer, case-based questions
   - No descriptive answer support

3. **No Teacher Control**:
   - Teachers can't customize blueprint
   - Can't select specific topics/chapters
   - Can't adjust marks distribution
   - Can't edit generated questions

4. **No Reusability**:
   - Questions are session-specific
   - No persistent question bank
   - Can't reuse questions across assessments

5. **No CBSE Pattern Compliance**:
   - Doesn't follow CBSE blue print (Section A, B, C, etc.)
   - No competency-based questions
   - No case studies

---

## 9. WHAT WE CAN REUSE

### **From Current System**:

✅ **AI Question Generation Logic**:
- OpenRouter integration
- Prompt engineering patterns
- JSON parsing and validation
- Error handling and fallbacks

✅ **Database Models**:
- Question storage structure
- Response tracking
- Session management
- Attempt tracking

✅ **Scoring Engine**:
- Auto-grading logic
- Feedback generation
- Analytics calculation

✅ **API Patterns**:
- FastAPI endpoint structure
- Authentication/authorization
- Error handling

### **What Needs to Be Built**:

🔨 **NCERT Content Retrieval Service**:
```python
def get_chapter_content(grade, subject, chapter_ids):
    # Query ncert_textbook_content table
    # Return relevant text, examples, exercises
```

🔨 **Multi-Type Question Generator**:
```python
async def generate_assessment_questions(
    grade, subject, chapters,
    blueprint  # {mcq: 10, short: 5, long: 3, case: 1}
):
    # Generate different question types
```

🔨 **Blueprint Validator**:
```python
def validate_blueprint(questions, blueprint):
    # Ensure marks distribution matches
    # Check question type counts
```

🔨 **Assessment Builder UI**:
- Chapter selection interface
- Blueprint configuration wizard
- Question preview and editing
- PDF generation

---

## 10. RECOMMENDED INTEGRATION STRATEGY

### **Phase 1: Foundation** (Week 1-2)
- Create CBSE syllabus mapping table
- Link NCERT chapters to syllabus units
- Build content retrieval service

### **Phase 2: Question Generation** (Week 3-4)
- Extend AI generator for multi-type questions
- Add NCERT content as context to prompts
- Implement blueprint-based generation

### **Phase 3: Teacher Interface** (Week 5-6)
- Build assessment builder UI
- Chapter selection from NCERT database
- Blueprint configuration wizard

### **Phase 4: Question Bank** (Week 7-8)
- Persistent question storage
- Browse/search/filter functionality
- Reusability features

### **Phase 5: PDF & Export** (Week 9-10)
- Generate question papers
- Generate answer keys
- CBSE-compliant formatting

---

## 11. EXAMPLE: HOW NEW SYSTEM SHOULD WORK

### **Teacher Creates Assessment**:

1. **Select Grade & Subject**: Class 10 Mathematics
2. **Select Chapters**: Real Numbers, Polynomials
3. **Configure Blueprint**:
   ```json
   {
     "mcq": {"count": 10, "marks_each": 1},
     "short_answer": {"count": 5, "marks_each": 2},
     "long_answer": {"count": 3, "marks_each": 5},
     "case_based": {"count": 1, "marks_each": 4}
   }
   ```
4. **Set Difficulty**: Easy 40%, Medium 40%, Hard 20%
5. **Generate**: AI fetches NCERT content and generates questions
6. **Review**: Teacher previews and can edit/replace questions
7. **Finalize**: Export as PDF or publish to students

### **System Process**:

```python
# 1. Fetch NCERT content for selected chapters
content = db.query(NCERTTextbookContent).filter(
    NCERTTextbookContent.grade == 10,
    NCERTTextbookContent.subject == "Mathematics",
    NCERTTextbookContent.chapter.in_([1, 2])
).all()

# 2. Build context for AI
context = f"""
Chapter 1: Real Numbers
{content[0].full_text[:2000]}

Chapter 2: Polynomials
{content[1].full_text[:2000]}
"""

# 3. Generate questions with context
questions = await generate_questions_from_ncert(
    content=context,
    blueprint=blueprint,
    difficulty_distribution={"easy": 40, "medium": 40, "hard": 20}
)

# 4. Validate and save to question bank
validate_blueprint(questions, blueprint)
save_to_question_bank(questions)

# 5. Create assessment
assessment = create_assessment(
    teacher_id=teacher.id,
    questions=questions,
    total_marks=40,
    title="Unit Test - Real Numbers & Polynomials"
)
```

---

## SUMMARY

**Current System**: Teacher professional development with AI-generated MCQs
**Needed System**: Student assessment builder with NCERT-based multi-type questions
**Key Gap**: NCERT content integration + multi-type questions + teacher control
**Reusable**: AI generation patterns, database models, scoring engine
**New Builds**: NCERT integration, blueprint system, assessment builder UI

The foundation exists, but significant new development is needed to support student assessments with NCERT content.
