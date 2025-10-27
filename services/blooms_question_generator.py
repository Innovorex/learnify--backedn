"""
Bloom's Taxonomy Question Generator
Generates teacher-level questions across 6 cognitive levels for Subject Knowledge module
"""

import json
from typing import Dict, List
from enum import Enum


class BloomLevel(Enum):
    """Bloom's Taxonomy Cognitive Levels"""
    REMEMBER = 1      # Recall facts (avoid for teachers)
    UNDERSTAND = 2    # Explain concepts
    APPLY = 3         # Use in new situations
    ANALYZE = 4       # Break down, find patterns
    EVALUATE = 5      # Judge, critique
    CREATE = 6        # Design, construct


class BloomsQuestionGenerator:
    """
    Generate questions at different Bloom's levels for teacher assessment
    """

    def __init__(self):
        self.question_templates = self._init_templates()

    def _init_templates(self) -> Dict:
        """
        Question templates for each Bloom's level
        """
        return {
            BloomLevel.UNDERSTAND: {
                "conceptual_why": [
                    "Why does {phenomenon} occur in the context of {concept}?",
                    "How does {concept_1} relate to {concept_2} in {topic}?",
                    "Explain why {statement} is true/false in terms of {underlying_principle}.",
                    "What is the conceptual basis for {rule/formula} in {topic}?"
                ],
                "student_explanation": [
                    "A student asks: '{student_question}'. How would you explain {concept} to clarify this?",
                    "How would you help students understand the difference between {concept_1} and {concept_2}?",
                    "Explain {concept} in a way that connects to students' prior knowledge of {prerequisite}."
                ]
            },

            BloomLevel.APPLY: {
                "real_world": [
                    "How would you use {concept} to explain {real_world_phenomenon}?",
                    "Apply {principle} to solve this teaching scenario: {scenario}",
                    "Which concept from {topic} best explains {everyday_situation}?"
                ],
                "cross_topic": [
                    "How does {concept_from_topic_1} connect to {concept_from_topic_2}?",
                    "Apply your knowledge of {topic} to design an experiment that demonstrates {principle}.",
                    "Use {mathematical_concept} to model {real_world_problem}."
                ]
            },

            BloomLevel.ANALYZE: {
                "misconception": [
                    "A student believes '{misconception}'. Analyze the flaw in this reasoning.",
                    "Why might students confuse {concept_1} with {concept_2}?",
                    "Identify which prerequisite knowledge gap leads to {common_error}."
                ],
                "compare_contrast": [
                    "Compare {concept_1} and {concept_2}. What are the key distinctions teachers must understand?",
                    "Analyze the relationship between {principle_1} and {principle_2}.",
                    "Break down {complex_concept} into its component concepts for teaching."
                ],
                "error_analysis": [
                    "A student solved this problem incorrectly: {student_work}. Analyze the error.",
                    "Examine this student reasoning: {reasoning}. What conceptual gap exists?",
                    "Which of these student errors indicates a deeper misconception: {options}?"
                ]
            },

            BloomLevel.EVALUATE: {
                "teaching_approach": [
                    "Evaluate which teaching sequence is most effective for {topic}: {options}",
                    "Which demonstration best illustrates {principle}? Justify your choice.",
                    "Assess the pedagogical value of using {analogy} to teach {concept}."
                ],
                "solution_critique": [
                    "A student uses {method} to solve {problem}. Evaluate this approach.",
                    "Judge which explanation of {concept} is most accurate and pedagogically sound: {options}",
                    "Critique this textbook explanation of {topic}: {explanation}"
                ]
            },

            BloomLevel.CREATE: {
                "design_activity": [
                    "Design a 5-minute demonstration to show {principle} using {available_resources}.",
                    "Create an analogy to help Grade {grade} students understand {abstract_concept}.",
                    "Develop a sequence of questions to guide students from {misconception} to {correct_understanding}."
                ],
                "problem_creation": [
                    "Create a real-world problem that requires applying {concept_1} and {concept_2} together.",
                    "Design an assessment question that tests deep understanding of {principle}, not just recall.",
                    "Construct a lesson plan segment addressing the misconception: {misconception}."
                ]
            }
        }

    async def generate_question(
        self,
        bloom_level: BloomLevel,
        concept_map: Dict,
        question_type: str = None,
        difficulty: str = "medium"
    ) -> Dict:
        """
        Generate a single question at specified Bloom's level

        Args:
            bloom_level: Cognitive level (UNDERSTAND, APPLY, etc.)
            concept_map: Output from ConceptMapper
            question_type: Specific template type (optional)
            difficulty: easy/medium/hard

        Returns:
            {
                "question": "...",
                "options": ["A)", "B)", "C)", "D)"],
                "correct_answer": "B",
                "bloom_level": "Apply",
                "explanation": "...",
                "tests": "What this question assesses"
            }
        """

        from services.openrouter import generate_questions_with_claude_haiku

        # Build context from concept map
        context = self._build_context(concept_map)

        # Get appropriate prompt based on Bloom's level
        prompt = self._build_prompt(bloom_level, context, difficulty)

        # Generate question using AI
        response = await generate_questions_with_claude_haiku(prompt, max_tokens=3000)

        # Parse response
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            question_data = json.loads(json_match.group())
            question_data['bloom_level'] = bloom_level.name
            return question_data

        # Fallback
        return self._generate_fallback_question(bloom_level, concept_map)

    def _build_context(self, concept_map: Dict) -> str:
        """Build rich context string from concept map"""

        topic = concept_map.get('topic', 'Unknown Topic')
        concepts = concept_map.get('core_concepts', [])
        principles = concept_map.get('underlying_principles', [])
        misconceptions = concept_map.get('common_misconceptions', [])
        applications = concept_map.get('real_world_applications', [])

        context = f"""
TOPIC: {topic}

CORE CONCEPTS:
{self._format_list(concepts)}

UNDERLYING PRINCIPLES:
{self._format_list(principles)}

COMMON STUDENT MISCONCEPTIONS:
{self._format_list(misconceptions)}

REAL-WORLD APPLICATIONS:
{self._format_list(applications)}
"""
        return context

    def _format_list(self, items: List[str]) -> str:
        """Format list items with bullets"""
        if not items:
            return "- None specified"
        return "\n".join([f"- {item}" for item in items])

    def _build_prompt(self, bloom_level: BloomLevel, context: str, difficulty: str) -> str:
        """Build AI prompt based on Bloom's level"""

        level_instructions = {
            BloomLevel.UNDERSTAND: """
Generate a question testing CONCEPTUAL UNDERSTANDING (Bloom's: Understand).

Question should:
✅ Test WHY or HOW something works, not just WHAT it is
✅ Require explaining relationships between concepts
✅ Address teacher's ability to clarify concepts for students
✅ Go beyond recall to comprehension

Example:
"Why does a passenger in a bus jerk forward when the bus suddenly stops? Explain in terms of Newton's laws."

NOT: "What is Newton's first law?" (too basic)
""",
            BloomLevel.APPLY: """
Generate a question testing APPLICATION (Bloom's: Apply).

Question should:
✅ Present a new real-world scenario requiring concept application
✅ Test ability to use knowledge in unfamiliar contexts
✅ Connect theory to practice
✅ May involve cross-topic connections

Example:
"A teacher wants to demonstrate conservation of momentum using two colliding trolleys. Which Newton's law provides the theoretical foundation, and why?"
""",
            BloomLevel.ANALYZE: """
Generate a question testing ANALYSIS (Bloom's: Analyze).

Question should:
✅ Require breaking down concepts or identifying patterns
✅ Test ability to find flaws in reasoning (misconception handling)
✅ Compare and contrast related concepts
✅ Analyze student errors and diagnose knowledge gaps

Example:
"A student claims: 'Action and reaction forces cancel out, so nothing should move.' Identify the conceptual flaw in this reasoning and explain which principle the student misunderstands."
""",
            BloomLevel.EVALUATE: """
Generate a question testing EVALUATION (Bloom's: Evaluate).

Question should:
✅ Require judging quality of approaches or explanations
✅ Test ability to select best teaching methods
✅ Critique solutions or teaching materials
✅ Justify choices with pedagogical reasoning

Example:
"Evaluate which teaching sequence is most effective for introducing Newton's laws: (A) 1st→2nd→3rd, (B) 3rd→1st→2nd, (C) 2nd→1st→3rd. Justify your choice."
""",
            BloomLevel.CREATE: """
Generate a question testing CREATION (Bloom's: Create).

Question should:
✅ Require designing demonstrations, analogies, or lesson segments
✅ Test ability to synthesize knowledge into teaching tools
✅ May be open-ended or require creative problem-solving
✅ Focus on pedagogical content knowledge (PCK)

Example:
"Design a simple classroom demonstration using household items (ball, book, table) to simultaneously illustrate all three of Newton's laws."
"""
        }

        instruction = level_instructions.get(bloom_level, level_instructions[BloomLevel.UNDERSTAND])

        prompt = f"""You are creating a TEACHER ASSESSMENT QUESTION for the "Subject Knowledge & Content Expertise" module.

{context}

{instruction}

DIFFICULTY LEVEL: {difficulty.upper()}
{"- Involves multiple concepts" if difficulty == "hard" else "- Straightforward scenario" if difficulty == "easy" else "- Moderate complexity"}

CRITICAL REQUIREMENTS:
1. This is for TEACHERS, not students
2. Test DEEP subject matter expertise
3. Question must require {bloom_level.name}-level thinking
4. Provide 4 options (A, B, C, D) if MCQ
5. Include detailed explanation of correct answer
6. NO pedagogy questions (this is pure subject knowledge)

Return ONLY valid JSON:
{{
    "question": "The question text",
    "question_type": "mcq" or "scenario",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "correct_answer": "B",
    "explanation": "Detailed explanation of why correct answer is right and why others are wrong",
    "tests": "Brief description of what this question assesses",
    "difficulty": "{difficulty}",
    "cognitive_level": "{bloom_level.name}"
}}

If open-ended/scenario question, omit "options" and "correct_answer" but include "rubric" with scoring criteria.
"""

        return prompt

    def _generate_fallback_question(self, bloom_level: BloomLevel, concept_map: Dict) -> Dict:
        """Generate basic fallback question if AI fails"""

        topic = concept_map.get('topic', 'Subject Knowledge')

        return {
            "question": f"Explain the key principles underlying {topic}.",
            "question_type": "open_ended",
            "bloom_level": bloom_level.name,
            "tests": f"Understanding of {topic}",
            "difficulty": "medium"
        }

    async def generate_balanced_question_set(
        self,
        concept_map: Dict,
        total_questions: int = 8,
        difficulty: str = "medium"
    ) -> List[Dict]:
        """
        Generate a balanced set of questions across Bloom's levels

        Distribution:
        - Understand: 25% (2 questions)
        - Apply: 30% (2-3 questions)
        - Analyze: 30% (2-3 questions)
        - Evaluate: 15% (1 question)
        - Create: 0% (too complex for auto-grading)

        Args:
            concept_map: From ConceptMapper
            total_questions: Number of questions to generate
            difficulty: Overall difficulty level

        Returns:
            List of question dictionaries
        """

        distribution = {
            BloomLevel.UNDERSTAND: 2,
            BloomLevel.APPLY: 3,
            BloomLevel.ANALYZE: 2,
            BloomLevel.EVALUATE: 1
        }

        questions = []

        for bloom_level, count in distribution.items():
            for i in range(count):
                try:
                    question = await self.generate_question(
                        bloom_level=bloom_level,
                        concept_map=concept_map,
                        difficulty=difficulty
                    )
                    questions.append(question)
                except Exception as e:
                    print(f"[ERROR] Failed to generate {bloom_level.name} question: {e}")
                    # Add fallback
                    questions.append(self._generate_fallback_question(bloom_level, concept_map))

        return questions


# Global instance
blooms_generator = BloomsQuestionGenerator()
