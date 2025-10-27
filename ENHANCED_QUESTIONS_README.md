# Enhanced Subject Knowledge Question Generation System

## Overview

This system generates **teacher-level assessment questions** for the "Subject Knowledge & Content Expertise" module using:

1. ✅ **Authentic Syllabus** from LS database (CBSE/Telangana/AP boards)
2. ✅ **Concept Mapping** (topics → core concepts → principles)
3. ✅ **Bloom's Taxonomy** (Understand → Apply → Analyze → Evaluate)
4. ✅ **Misconception Handling** (tests teacher's ability to clarify student errors)
5. ✅ **Pedagogical Content Knowledge** (PCK-focused questions)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│         ENHANCED SUBJECT QUESTION GENERATOR                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │  1. LS SYLLABUS INTEGRATION                        │    │
│  │     - Fetches from LS PostgreSQL database          │    │
│  │     - CBSE, Telangana, AP boards                   │    │
│  │     - Returns: topics, learning outcomes, concepts │    │
│  └────────────────────────────────────────────────────┘    │
│                        ↓                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │  2. CONCEPT MAPPER                                 │    │
│  │     - Extracts core concepts from topics           │    │
│  │     - Maps underlying principles                   │    │
│  │     - Identifies misconceptions                    │    │
│  │     - Finds real-world applications                │    │
│  └────────────────────────────────────────────────────┘    │
│                        ↓                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │  3. BLOOM'S TAXONOMY GENERATOR                     │    │
│  │     - Level 2: Understand (Why/How questions)      │    │
│  │     - Level 3: Apply (Real-world scenarios)        │    │
│  │     - Level 4: Analyze (Misconceptions, errors)    │    │
│  │     - Level 5: Evaluate (Teaching approaches)      │    │
│  └────────────────────────────────────────────────────┘    │
│                        ↓                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │  4. AI QUESTION GENERATION (Claude Haiku 4.5)      │    │
│  │     - Sophisticated prompts per Bloom's level      │    │
│  │     - Teacher-expertise focused                    │    │
│  │     - Multi-language support (Telugu, Hindi)       │    │
│  └────────────────────────────────────────────────────┘    │
│                        ↓                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │  5. OUTPUT: ENHANCED QUESTIONS                     │    │
│  │     - Balanced Bloom's distribution                │    │
│  │     - Detailed explanations                        │    │
│  │     - Metadata (topic, unit, difficulty)           │    │
│  └────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Components

### 1. **LS Syllabus Integration** (`ls_syllabus_integration.py`)

Connects to LS database to fetch authentic syllabus data:

```python
from services.ls_syllabus_integration import ls_syllabus_service

# Fetch all topics for a subject
topics = await ls_syllabus_service.get_syllabus_topics(
    board="CBSE",
    class_name="9",
    subject="Science"
)

# Each topic contains:
# - unit_name, chapter_name, topic_name
# - learning_outcomes[] (what students should achieve)
# - key_concepts[] (core concepts)
# - subtopics[]
# - difficulty_level, weightage
```

**Fallback**: If LS database unavailable, uses existing `curriculum_data.py`

---

### 2. **Concept Mapper** (`concept_mapper.py`)

Maps student-level topics to teacher-level understanding:

```python
from services.concept_mapper import concept_mapper

# Extract concepts from a topic
concept_map = await concept_mapper.extract_concepts_from_topic(
    board="CBSE",
    class_name="9",
    subject="Science",
    unit_name="Force and Laws of Motion",
    topic_name="Newton's Laws of Motion"
)

# Returns:
{
    "topic": "Newton's Laws of Motion",
    "core_concepts": [
        "Force: A push or pull that changes motion",
        "Inertia: Tendency to resist motion change",
        "Mass: Measure of inertia",
        ...
    ],
    "underlying_principles": [
        "Net force determines acceleration, not individual forces",
        "Forces always occur in pairs on different objects",
        ...
    ],
    "common_misconceptions": [
        "Force is needed to maintain constant velocity",
        "Action-reaction forces cancel out",
        ...
    ],
    "real_world_applications": [
        "Seat belts (inertia protection)",
        "Rocket propulsion (action-reaction)",
        ...
    ]
}
```

**Pre-built Library**: Common topics like "Newton's Laws", "Linear Equations" have pre-mapped concepts in `ConceptDatabase`

---

### 3. **Bloom's Taxonomy Generator** (`blooms_question_generator.py`)

Generates questions at specific cognitive levels:

```python
from services.blooms_question_generator import blooms_generator, BloomLevel

# Generate a Level 4 (Analyze) question
question = await blooms_generator.generate_question(
    bloom_level=BloomLevel.ANALYZE,
    concept_map=concept_map,
    difficulty="medium"
)

# Returns:
{
    "question": "A student claims 'Action and reaction cancel, so nothing moves.' Identify the flaw.",
    "options": [
        "A) They act on different objects",
        "B) Student's weight > seat force",
        "C) Friction prevents motion",
        "D) Only for moving objects"
    ],
    "correct_answer": "A",
    "bloom_level": "ANALYZE",
    "explanation": "Action-reaction pairs act on DIFFERENT objects...",
    "tests": "Understanding of force pairs and misconception handling"
}
```

**Bloom's Levels Supported**:
- **Understand** (25%): Why/How questions
- **Apply** (35%): Real-world scenarios
- **Analyze** (30%): Misconception handling, error analysis
- **Evaluate** (10%): Best teaching approaches

---

### 4. **Enhanced Question Generator** (`enhanced_subject_questions.py`)

Main orchestrator - brings everything together:

```python
from services.enhanced_subject_questions import enhanced_question_generator

# Generate 8 enhanced questions
questions = await enhanced_question_generator.generate_enhanced_questions(
    board="CBSE",
    class_name="9",
    subject="Science",
    n_questions=8,
    difficulty="medium",
    focus_topics=["Newton's Laws of Motion"]  # Optional
)

# Process:
# 1. Fetch syllabus from LS database
# 2. Select 2-3 high-weightage topics
# 3. Map concepts for each topic
# 4. Generate balanced Bloom's questions
# 5. Validate and return
```

---

## Question Examples

### **Example 1: Understand Level** (Conceptual Why/How)

```
Question: Why does a passenger in a bus jerk forward when the bus suddenly stops?

Options:
A) The bus pushes the passenger forward
B) The passenger's inertia keeps them moving forward
C) Air pressure inside the bus pushes them
D) Friction with the seat reduces suddenly

Correct Answer: B

Explanation: When the bus stops suddenly, the passenger's body tends to
maintain its state of motion due to inertia (Newton's 1st Law). The lower
part of the body in contact with the seat stops with the bus, but the upper
body continues moving forward, causing the jerk.

Bloom's Level: UNDERSTAND
Tests: Conceptual understanding of inertia and Newton's First Law
```

---

### **Example 2: Apply Level** (Real-world Application)

```
Question: A teacher wants to demonstrate conservation of momentum using two
colliding trolleys. Which Newton's law provides the theoretical foundation?

Options:
A) Newton's First Law (Inertia)
B) Newton's Second Law (F = ma)
C) Newton's Third Law (Action-Reaction)
D) All three laws equally

Correct Answer: C

Explanation: During collision, the trolleys exert equal and opposite forces
on each other (Newton's 3rd Law). This results in equal and opposite changes
in momentum, leading to momentum conservation. While F=ma is involved in
calculating momentum change, the action-reaction principle is the direct
foundation.

Bloom's Level: APPLY
Tests: Application of Newton's laws to experimental design
```

---

### **Example 3: Analyze Level** (Misconception Handling)

```
Question: A Grade 9 student reasons: "When I sit in a chair, my weight
(action) pushes down and the chair pushes up (reaction). These are equal and
opposite, so they cancel out and I should be floating."

What is the conceptual flaw in this reasoning?

Options:
A) Action-reaction pairs act on DIFFERENT objects, not the same object
B) The student's weight is actually greater than the chair's upward force
C) Friction between body and chair prevents floating
D) Action-reaction principle only applies to objects in motion

Correct Answer: A

Explanation: The student has confused a Newton's 3rd Law pair with balanced
forces. Action-reaction pairs ALWAYS act on different objects:
- Student pushes chair DOWN (action on chair)
- Chair pushes student UP (reaction on student)

These DON'T cancel because they act on different objects. The forces that
balance on the student are: weight (down) and normal force from chair (up).

Bloom's Level: ANALYZE
Tests: Ability to identify and correct misconception about action-reaction pairs
```

---

### **Example 4: Evaluate Level** (Teaching Approach)

```
Question: A teacher is planning to introduce Newton's Laws to Grade 9 students.
Evaluate which sequence would be most pedagogically effective:

A) 1st Law → 2nd Law → 3rd Law (historical order)
B) 2nd Law (F=ma) → 1st Law (special case) → 3rd Law
C) Concrete examples → 1st Law → 3rd Law → 2nd Law with math
D) All three laws simultaneously with one demonstration

Options reasoning:
A) Follows Newton's original presentation, builds intuition before math
B) Starts with most powerful law, shows 1st as special case
C) Concrete before abstract, delays mathematical complexity
D) Efficient but cognitively overloading

Correct Answer: C

Explanation: Best practice for Grade 9:
1. START with relatable phenomena (bus stopping, rocket launch)
2. Build intuitive understanding of inertia (1st Law) - no math
3. Introduce action-reaction with hands-on (3rd Law) - observable
4. THEN formalize with F=ma (2nd Law) - requires algebraic maturity

This follows constructivist learning principles: concrete → abstract,
phenomena → principles, qualitative → quantitative.

Bloom's Level: EVALUATE
Tests: Pedagogical content knowledge and sequencing decisions
```

---

## Usage in Learnify-Teach

### **Option 1: Replace Existing Generator**

Modify `routers/assessments.py`:

```python
from services.enhanced_subject_questions import enhanced_question_generator

@router.post("/assessment/generate/{module_id}")
async def generate_module_assessment(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get teacher profile
    teacher_profile = db.query(TeacherProfile).filter(...).first()

    # For Subject Knowledge module (module_id = 1)
    if module_id == 1:
        questions = await enhanced_question_generator.generate_enhanced_questions(
            board=teacher_profile.board,
            class_name=teacher_profile.grades_teaching.split(',')[0],
            subject=teacher_profile.subjects_teaching.split(',')[0],
            n_questions=8,
            difficulty="medium"
        )
    else:
        # Use existing generators for other modules
        questions = await generate_other_module_questions(...)

    # Save to database
    ...
```

---

### **Option 2: A/B Test**

Run both generators in parallel, let teachers choose:

```python
# Premium feature flag
if teacher.subscription_tier == "premium":
    questions = await enhanced_question_generator.generate_enhanced_questions(...)
else:
    questions = await generate_subject_knowledge_questions(...)  # Existing
```

---

## Configuration

### **Environment Variables**

```bash
# .env file
LS_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/learnify_syllabus
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=anthropic/claude-haiku-4.5  # Recommended for quality
```

### **Bloom's Distribution** (Adjustable)

In `enhanced_subject_questions.py`:

```python
def _get_blooms_distribution(difficulty, n_questions):
    if difficulty == "medium":
        return {
            BloomLevel.UNDERSTAND: 25%,   # Conceptual why/how
            BloomLevel.APPLY: 35%,        # Real-world scenarios
            BloomLevel.ANALYZE: 30%,      # Misconception handling
            BloomLevel.EVALUATE: 10%      # Teaching approaches
        }
```

---

## Cost Analysis

### **With Claude Haiku 4.5**

**Per Question Set** (8 questions):
- Input tokens: ~4,000 tokens (syllabus + concept map + prompts)
- Output tokens: ~2,500 tokens (8 detailed questions with explanations)

```
Cost = (4000 × $0.000001) + (2500 × $0.000005)
     = $0.004 + $0.0125
     = $0.0165 per 8 questions
     = ₹1.37 per assessment (at ₹83/USD)
```

**Monthly Cost** (1000 teachers, 6 assessments/month):
```
1000 teachers × 6 assessments × $0.0165 = $99/month = ₹8,217/month
```

**With Question Bank** (after building library):
```
80% from bank (free) + 20% new generation
= $99 × 0.20 = $19.80/month = ₹1,643/month
```

---

## Testing

Run the test suite:

```bash
cd /home/hub_ai/learnify-teach/backend

# Test with Physics
python test_enhanced_questions.py

# Test specific Bloom's level
python -c "
import asyncio
from services.blooms_question_generator import blooms_generator, BloomLevel
from services.concept_mapper import concept_db

async def test():
    concept_map = concept_db.get_concept_map('Newton\\'s Laws of Motion')
    q = await blooms_generator.generate_question(BloomLevel.ANALYZE, concept_map)
    print(q)

asyncio.run(test())
"
```

---

## Advantages Over Current System

| Feature | Current | Enhanced |
|---------|---------|----------|
| **Source** | Generic AI prompt | LS database syllabus |
| **Cognitive Level** | Remember (Level 1) | Understand → Evaluate (Levels 2-5) |
| **Question Type** | "What is X?" | "Why/How does X work?" |
| **Misconceptions** | Not addressed | Explicitly tested |
| **Real-world** | Minimal | Every topic |
| **PCK** | None | Teaching approach questions |
| **Syllabus Alignment** | Approximate | Exact (from LS) |
| **Telugu Quality** | Poor (Llama 3.3) | Excellent (Claude Haiku) |
| **Consistency** | Variable | High (structured prompts) |

---

## Roadmap

### **Phase 1: MVP** ✅ COMPLETE
- [x] LS database integration
- [x] Concept mapper
- [x] Bloom's taxonomy generator
- [x] Enhanced orchestrator
- [x] Testing framework

### **Phase 2: Production** (Week 1-2)
- [ ] Integrate into `routers/assessments.py`
- [ ] Add question bank table to database
- [ ] Build initial bank (500 questions)
- [ ] Add quality scoring metrics

### **Phase 3: Scale** (Week 3-4)
- [ ] Multi-subject support (all CBSE subjects)
- [ ] State board expansion (TS, AP complete coverage)
- [ ] Adaptive difficulty based on teacher performance
- [ ] Question reuse optimization

### **Phase 4: Intelligence** (Month 2)
- [ ] Curriculum coverage tracking (ensure all topics tested)
- [ ] Personalized question selection
- [ ] Auto-retire poor-quality questions
- [ ] Teacher feedback integration

---

## Support

For questions or issues:
1. Check logs: `/var/log/learnify-teach/enhanced_questions.log`
2. Validate LS database connection: `psql $LS_DATABASE_URL -c "SELECT COUNT(*) FROM syllabus_topics"`
3. Test AI connectivity: `curl https://openrouter.ai/api/v1/models -H "Authorization: Bearer $OPENROUTER_API_KEY"`

---

## Summary

This enhanced system transforms Subject Knowledge assessment from **basic recall** to **deep pedagogical expertise testing**. Teachers are evaluated on:

✅ Conceptual understanding (Why/How)
✅ Application to real-world scenarios
✅ Ability to handle student misconceptions
✅ Pedagogical content knowledge
✅ Critical analysis and evaluation skills

**Result**: Teachers who pass demonstrate not just subject knowledge, but the ability to **teach effectively** at that level.
