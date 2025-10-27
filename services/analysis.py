# services/analysis.py
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from models import Performance, Module, TeacherProfile, GrowthPlan, User
from services.openrouter import OPENROUTER_API_KEY, OPENROUTER_MODEL, generate_subject_knowledge_questions_ai_requests
import os

# Default weights (tunable)
WEIGHTS = {"mcq": 0.5, "submission": 0.3, "outcome": 0.2}

def rating_from_score(score: float) -> str:
    if score >= 85: return "Excellent"
    if score >= 60: return "Good"
    return "Needs Improvement"

def collect_teacher_module_scores(db: Session, teacher_id: int):
    # join Performance + Module to get (score, assessment_type, module_name)
    rows = (db.query(Performance, Module)
              .join(Module, Performance.module_id == Module.id)
              .filter(Performance.teacher_id == teacher_id)
              .all())
    module_scores = []
    typed_scores = {"mcq": [], "submission": [], "outcome": []}
    for perf, mod in rows:
        module_scores.append({
            "module_id": mod.id,
            "module_name": mod.name,
            "assessment_type": mod.assessment_type,
            "score": perf.score,
            "rating": perf.rating
        })
        if mod.assessment_type in typed_scores:
            typed_scores[mod.assessment_type].append(perf.score)

    # compute per-type averages
    type_avgs = {}
    for t in typed_scores:
        scores = typed_scores[t]
        type_avgs[t] = sum(scores)/len(scores) if scores else 0.0

    # weighted overall
    overall = 0.0
    total_w = 0.0
    for t, w in WEIGHTS.items():
        overall += type_avgs[t] * w
        total_w += w
    overall = round(overall / total_w, 2) if total_w else 0.0

    return module_scores, type_avgs, overall

def benchmark_vs_cohort(db: Session, teacher_id: int):
    # Cohort: same board + any overlap in subjects/grades (simple filter)
    prof = db.query(TeacherProfile).filter_by(user_id=teacher_id).first()
    if not prof:
        return {"teacher_percentile": 0.0, "cohort_size": 0, "cohort_definition": {}}

    # Compute each teacher overall as above, then percentile rank
    # (For simplicity: compare means of all Performance for a teacher with same board)
    cohort_user_ids = [uid for (uid,) in
        db.query(User.id).join(TeacherProfile, TeacherProfile.user_id == User.id)
          .filter(TeacherProfile.board == prof.board)
          .all()
    ]

    # build map of teacher_id -> mean score across all their Performance
    means = []
    teacher_mean = 0.0
    for uid in cohort_user_ids:
        avg = db.query(func.avg(Performance.score)).filter(Performance.teacher_id == uid).scalar() or 0.0
        means.append((uid, float(avg)))
        if uid == teacher_id:
            teacher_mean = float(avg)

    # percentile: % of cohort <= teacher
    if not means:
        percentile = 0.0
    else:
        below = sum(1 for _, m in means if m <= teacher_mean)
        percentile = round((below / len(means)) * 100.0, 2)

    return {
        "teacher_percentile": percentile,
        "cohort_size": len(means),
        "cohort_definition": {
            "board": prof.board,
            "grades_teaching": prof.grades_teaching,
            "subjects_teaching": prof.subjects_teaching,
        }
    }

async def generate_growth_plan(db: Session, teacher_id: int, focus_areas: list[str] | None = None) -> str:
    # Identify weak types/modules to guide the prompt
    module_scores, type_avgs, overall = collect_teacher_module_scores(db, teacher_id)
    module_scores_sorted = sorted(module_scores, key=lambda m: m["score"])
    weak_modules = [m["module_name"] for m in module_scores_sorted[:3]] if module_scores_sorted else []
    weak_types = sorted(type_avgs.items(), key=lambda kv: kv[1])[:2]
    weak_types_names = [t for t, _ in weak_types]

    prof = db.query(TeacherProfile).filter_by(user_id=teacher_id).first()
    if not prof:
        edu = grades = subs = exp = board = "N/A"
    else:
        edu = prof.education
        grades = prof.grades_teaching
        subs = prof.subjects_teaching
        exp = prof.experience_years
        board = prof.board

    if focus_areas:
        weak_modules = focus_areas + weak_modules

    prompt = f"""You are an expert instructional coach specializing in Indian education systems. Create a detailed 30-day professional growth plan for a teacher.

TEACHER PROFILE:
- Education Level: {edu}
- Teaching Grades: {grades}
- Subject Areas: {subs}
- Years of Experience: {exp}
- Educational Board: {board}
- Current Performance Score: {overall}/100
- Improvement Areas: {weak_modules}
- Weak Assessment Types: {weak_types_names}

Create a comprehensive growth plan following this EXACT structure:

# 30-Day Professional Growth Plan

## Executive Summary
Write 2-3 sentences about the teacher's current status and main improvement goals.

## Week 1: Assessment & Foundation (Days 1-7)
### Goals:
- Goal 1 related to weak areas
- Goal 2 related to teaching methods

### Daily Action Items:
- **Day 1:** Specific task for {subs} teaching
- **Day 2:** Specific task for classroom management
- **Day 3:** Specific task for {board} curriculum alignment
- **Day 4-7:** Additional specific daily tasks

## Week 2: Skill Development (Days 8-14)
### Goals:
- Focus on {weak_types_names[0] if weak_types_names else 'assessment'} improvement
- Enhance pedagogical skills for {grades}

### Daily Action Items:
- **Day 8-14:** Seven specific daily improvement tasks

## Week 3: Implementation (Days 15-21)
### Goals:
- Apply new strategies in classroom
- Focus on weak modules: {weak_modules[:2] if weak_modules else ['general teaching']}

### Daily Action Items:
- **Day 15-21:** Seven specific implementation tasks

## Week 4: Evaluation & Mastery (Days 22-30)
### Goals:
- Assess progress and effectiveness
- Plan for continued growth

### Daily Action Items:
- **Day 22-30:** Nine specific evaluation and mastery tasks

## Free Resources for {subs} Teachers
1. Resource 1: [Specific name and description]
2. Resource 2: [Specific name and description]
3. Resource 3: [Specific name and description]
4. Resource 4: [Specific name and description]
5. Resource 5: [Specific name and description]

## {board} Board Specific Strategies
- Strategy 1 for {grades} {subs}
- Strategy 2 for {grades} {subs}
- Strategy 3 for {grades} {subs}

## Success Metrics
- Metric 1: How to measure improvement
- Metric 2: How to track progress
- Metric 3: Expected outcomes

IMPORTANT: Make this plan specific to {subs} subject, {grades} grade levels, {board} board curriculum, and address the specific weak areas: {weak_modules}. Include practical, actionable daily tasks."""

    try:
        response_content = generate_subject_knowledge_questions_ai_requests(prompt)

        if response_content.startswith("Error") or response_content.startswith("Exception"):
            raise Exception(f"OpenRouter API call failed: {response_content}")

        # The response_content from generate_subject_knowledge_questions_ai_requests is already the content string
        content = response_content

        # Validate content length and quality
        if len(content) < 500:
            print(f"Warning: AI response too short ({len(content)} chars), using fallback")
            content = generate_fallback_plan(subs, grades, board, weak_modules, overall)

    except Exception as e:
        print(f"Error generating AI growth plan: {e}")
        content = generate_fallback_plan(subs, grades, board, weak_modules, overall)

    # Store in DB
    gp = GrowthPlan(teacher_id=teacher_id, content=content)
    db.add(gp)
    db.commit()
    return content

def generate_fallback_plan(subjects: str, grades: str, board: str, weak_areas: list, score: float) -> str:
    """Generate a template-based fallback growth plan when AI fails"""
    weak_areas_str = ", ".join(weak_areas[:3]) if weak_areas else "general teaching skills"

    return f"""# 30-Day Professional Growth Plan for {subjects} Teacher

## Executive Summary
This growth plan is designed for a {subjects} teacher working with {grades} students under the {board} board. Current performance score is {score}/100, with focus areas including {weak_areas_str}.

## Week 1: Assessment & Foundation (Days 1-7)
### Goals:
- Assess current teaching methodologies and student engagement levels
- Review {board} curriculum guidelines for {subjects}

### Daily Action Items:
- **Day 1:** Conduct self-assessment of teaching practices for {subjects}
- **Day 2:** Review student feedback and performance data from recent assessments
- **Day 3:** Study {board} curriculum standards for {grades} {subjects}
- **Day 4:** Observe peer teachers or watch educational videos on {subjects} pedagogy
- **Day 5:** Create a baseline measurement of current classroom engagement
- **Day 6:** Identify 3 specific areas for improvement in {subjects} teaching
- **Day 7:** Plan Week 2 improvement activities based on assessment results

## Week 2: Skill Development (Days 8-14)
### Goals:
- Develop new teaching strategies for {subjects}
- Improve assessment methods and student engagement

### Daily Action Items:
- **Day 8:** Research and plan interactive activities for {subjects} concepts
- **Day 9:** Design formative assessment tools for {grades} level
- **Day 10:** Practice new questioning techniques for deeper learning
- **Day 11:** Create visual aids and learning materials for {subjects}
- **Day 12:** Develop differentiated instruction strategies for diverse learners
- **Day 13:** Plan technology integration for {subjects} lessons
- **Day 14:** Prepare lesson plans incorporating new strategies

## Week 3: Implementation (Days 15-21)
### Goals:
- Apply new teaching strategies in classroom
- Focus on improving weak areas: {weak_areas_str}

### Daily Action Items:
- **Day 15:** Implement first new teaching strategy in {subjects} class
- **Day 16:** Use improved assessment techniques with students
- **Day 17:** Apply differentiated instruction for diverse learning needs
- **Day 18:** Integrate technology tools in {subjects} lesson
- **Day 19:** Practice active learning techniques with {grades} students
- **Day 20:** Implement peer collaboration activities in {subjects}
- **Day 21:** Gather student feedback on new teaching approaches

## Week 4: Evaluation & Mastery (Days 22-30)
### Goals:
- Assess progress and effectiveness
- Plan for continued growth

### Daily Action Items:
- **Day 22:** Analyze student performance data from new teaching methods
- **Day 23:** Review student feedback and engagement observations
- **Day 24:** Compare current vs. baseline classroom engagement metrics
- **Day 25:** Document successful strategies for future use
- **Day 26:** Identify strategies that need refinement
- **Day 27:** Plan next month's professional development goals
- **Day 28:** Share successful practices with colleagues
- **Day 29:** Create action plan for continued improvement
- **Day 30:** Self-reflect and document growth journey

## Free Resources for {subjects} Teachers
1. **NCERT Teacher Resources**: Official {board} board materials and guidelines
2. **Khan Academy**: Free video lessons and practice exercises for {subjects}
3. **Coursera Teacher Professional Development**: Free courses on pedagogy
4. **YouTube Educational Channels**: Subject-specific teaching strategy videos
5. **National Education Portal (DIKSHA)**: Government resources for teachers

## {board} Board Specific Strategies
- Align all lessons with {board} learning outcomes for {grades}
- Use {board}-prescribed textbooks as primary resource for {subjects}
- Implement continuous and comprehensive evaluation (CCE) methods
- Focus on competency-based learning as per {board} guidelines

## Success Metrics
- **Student Engagement**: Measure through classroom participation and feedback
- **Assessment Performance**: Track improvement in student test scores
- **Teaching Effectiveness**: Monitor through peer feedback and self-reflection
- **Professional Growth**: Document new skills acquired and strategies mastered

## Next Steps
Continue this growth journey by setting new 30-day goals focused on advanced teaching techniques and student outcome improvements.
"""
