"""
Enhanced Subject Knowledge Question Generator
Uses LS syllabus + Concept Mapping + Bloom's Taxonomy for teacher-level questions
"""

import asyncio
from typing import Dict, List, Optional
from services.ls_syllabus_integration import ls_syllabus_service
from services.concept_mapper import concept_mapper, concept_db
from services.blooms_question_generator import blooms_generator, BloomLevel


class EnhancedSubjectQuestionGenerator:
    """
    Main orchestrator for generating enhanced subject knowledge questions

    Process:
    1. Fetch syllabus from LS database (CBSE/TS/AP)
    2. Extract topics and learning outcomes
    3. Map to core concepts and principles
    4. Generate Bloom's-based teacher-level questions
    5. Return balanced question set
    """

    async def generate_enhanced_questions(
        self,
        board: str,
        class_name: str,
        subject: str,
        teacher_profile: Dict = None,
        n_questions: int = 8,
        difficulty: str = "medium",
        focus_topics: List[str] = None
    ) -> List[Dict]:
        """
        Generate enhanced teacher-level questions

        Args:
            board: CBSE, Telangana, AP Board, etc.
            class_name: Grade/Class (9, 10, 11, 12)
            subject: Mathematics, Science, etc.
            teacher_profile: Teacher's education, experience for personalization
            n_questions: Number of questions to generate
            difficulty: easy/medium/hard
            focus_topics: Specific topics to focus on (optional)

        Returns:
            List of enhanced questions with Bloom's taxonomy levels
        """

        print(f"\n{'='*60}")
        print(f"ENHANCED SUBJECT QUESTION GENERATION")
        print(f"{'='*60}")
        print(f"Board: {board} | Class: {class_name} | Subject: {subject}")
        print(f"Questions: {n_questions} | Difficulty: {difficulty}")
        print(f"{'='*60}\n")

        # Step 1: Fetch syllabus from LS database
        print("[STEP 1] Fetching syllabus from LS database...")
        topics = await ls_syllabus_service.get_syllabus_topics(
            board=board,
            class_name=class_name,
            subject=subject
        )

        if not topics:
            print("[ERROR] No syllabus topics found. Using fallback.")
            return await self._generate_fallback_questions(
                board, class_name, subject, n_questions
            )

        print(f"[SUCCESS] Fetched {len(topics)} topics from syllabus")

        # Step 2: Select topics for question generation
        print("\n[STEP 2] Selecting topics for questions...")
        selected_topics = self._select_topics(topics, focus_topics, n_questions)
        print(f"[SUCCESS] Selected {len(selected_topics)} topics")

        # Step 3: Map concepts for each topic
        print("\n[STEP 3] Mapping core concepts and principles...")
        concept_maps = []

        for topic in selected_topics:
            print(f"  - Mapping: {topic['topic_name']}")

            # Check if pre-built concept map exists
            concept_map = concept_db.get_concept_map(topic['topic_name'])

            if not concept_map:
                # Generate concept map using AI
                concept_map = await concept_mapper.extract_concepts_from_topic(
                    board=board,
                    class_name=class_name,
                    subject=subject,
                    unit_name=topic.get('unit_name', ''),
                    topic_name=topic['topic_name']
                )

            # Enrich with syllabus data
            concept_map.update({
                'learning_outcomes': topic.get('learning_outcomes', []),
                'key_concepts_syllabus': topic.get('key_concepts', []),
                'subtopics': topic.get('subtopics', []),
                'weightage': topic.get('weightage', 10)
            })

            concept_maps.append(concept_map)

        print(f"[SUCCESS] Mapped {len(concept_maps)} concept maps")

        # Step 4: Generate Bloom's taxonomy questions
        print("\n[STEP 4] Generating Bloom's Taxonomy questions...")
        all_questions = []

        # Determine Bloom's distribution based on difficulty
        distribution = self._get_blooms_distribution(difficulty, n_questions)

        questions_per_topic = n_questions // len(concept_maps)
        remainder = n_questions % len(concept_maps)

        for idx, concept_map in enumerate(concept_maps):
            topic_name = concept_map.get('topic', 'Unknown')
            print(f"\n  Topic: {topic_name}")

            # Allocate questions for this topic
            topic_questions = questions_per_topic + (1 if idx < remainder else 0)

            # Generate balanced set for this topic
            topic_question_set = []

            for bloom_level, count in distribution.items():
                if count == 0:
                    continue

                # Scale count for this topic
                topic_count = max(1, count * topic_questions // n_questions)

                print(f"    - {bloom_level.name}: Generating {topic_count} questions")

                for i in range(topic_count):
                    try:
                        question = await blooms_generator.generate_question(
                            bloom_level=bloom_level,
                            concept_map=concept_map,
                            difficulty=difficulty
                        )

                        # Add metadata
                        question['source_topic'] = topic_name
                        question['source_unit'] = concept_map.get('unit_name', '')
                        question['board'] = board
                        question['class'] = class_name
                        question['subject'] = subject

                        topic_question_set.append(question)

                        # Add small delay to avoid rate limits
                        await asyncio.sleep(0.5)

                    except Exception as e:
                        print(f"      [ERROR] Failed to generate {bloom_level.name} question: {e}")

            all_questions.extend(topic_question_set[:topic_questions])

        print(f"\n[SUCCESS] Generated {len(all_questions)} total questions")

        # Step 5: Post-process and validate
        print("\n[STEP 5] Post-processing questions...")
        validated_questions = self._validate_questions(all_questions, n_questions)

        print(f"\n{'='*60}")
        print(f"GENERATION COMPLETE")
        print(f"{'='*60}")
        print(f"Total Questions: {len(validated_questions)}")
        self._print_summary(validated_questions)
        print(f"{'='*60}\n")

        return validated_questions

    def _select_topics(
        self,
        all_topics: List[Dict],
        focus_topics: Optional[List[str]],
        n_questions: int
    ) -> List[Dict]:
        """
        Select topics for question generation

        Strategy:
        - If focus_topics specified, use those
        - Otherwise, select diverse topics based on weightage
        - Aim for 2-3 topics to cover different concepts
        """

        if focus_topics:
            selected = [t for t in all_topics if t['topic_name'] in focus_topics]
            if selected:
                return selected[:3]  # Max 3 topics

        # Select diverse topics based on weightage
        # Sort by weightage (higher = more important)
        sorted_topics = sorted(
            all_topics,
            key=lambda x: x.get('weightage', 0),
            reverse=True
        )

        # Select top 2-3 topics
        num_topics = min(3, max(2, n_questions // 3))
        return sorted_topics[:num_topics]

    def _get_blooms_distribution(self, difficulty: str, n_questions: int) -> Dict[BloomLevel, int]:
        """
        Get Bloom's level distribution based on difficulty

        Easy: More Understand, less Analyze
        Medium: Balanced
        Hard: More Analyze/Evaluate, less Understand
        """

        if difficulty == "easy":
            distribution = {
                BloomLevel.UNDERSTAND: int(n_questions * 0.40),  # 40%
                BloomLevel.APPLY: int(n_questions * 0.35),       # 35%
                BloomLevel.ANALYZE: int(n_questions * 0.20),     # 20%
                BloomLevel.EVALUATE: int(n_questions * 0.05),    # 5%
            }
        elif difficulty == "hard":
            distribution = {
                BloomLevel.UNDERSTAND: int(n_questions * 0.15),  # 15%
                BloomLevel.APPLY: int(n_questions * 0.30),       # 30%
                BloomLevel.ANALYZE: int(n_questions * 0.35),     # 35%
                BloomLevel.EVALUATE: int(n_questions * 0.20),    # 20%
            }
        else:  # medium
            distribution = {
                BloomLevel.UNDERSTAND: int(n_questions * 0.25),  # 25%
                BloomLevel.APPLY: int(n_questions * 0.35),       # 35%
                BloomLevel.ANALYZE: int(n_questions * 0.30),     # 30%
                BloomLevel.EVALUATE: int(n_questions * 0.10),    # 10%
            }

        # Ensure total equals n_questions
        total = sum(distribution.values())
        if total < n_questions:
            distribution[BloomLevel.APPLY] += (n_questions - total)

        return distribution

    def _validate_questions(self, questions: List[Dict], target_count: int) -> List[Dict]:
        """
        Validate and clean up generated questions
        """

        validated = []

        for q in questions:
            # Ensure required fields exist
            if 'question' not in q or not q['question']:
                continue

            # Ensure options exist for MCQ
            if q.get('question_type') == 'mcq':
                if 'options' not in q or len(q.get('options', [])) != 4:
                    continue
                if 'correct_answer' not in q:
                    continue

            validated.append(q)

        # Trim to target count
        return validated[:target_count]

    def _print_summary(self, questions: List[Dict]):
        """Print summary of generated questions"""

        bloom_counts = {}
        for q in questions:
            level = q.get('bloom_level', 'Unknown')
            bloom_counts[level] = bloom_counts.get(level, 0) + 1

        print("\nBloom's Taxonomy Distribution:")
        for level, count in sorted(bloom_counts.items()):
            percentage = (count / len(questions) * 100) if questions else 0
            print(f"  - {level}: {count} questions ({percentage:.1f}%)")

    async def _generate_fallback_questions(
        self,
        board: str,
        class_name: str,
        subject: str,
        n_questions: int
    ) -> List[Dict]:
        """
        Fallback to basic questions if LS database unavailable
        """

        print("[FALLBACK] Using basic question generation")

        # Import existing generator
        from services.openrouter import generate_subject_knowledge_questions

        return await generate_subject_knowledge_questions(
            board=board,
            grade=class_name,
            subject=subject,
            n_questions=n_questions,
            difficulty="medium"
        )


# Global instance
enhanced_question_generator = EnhancedSubjectQuestionGenerator()
