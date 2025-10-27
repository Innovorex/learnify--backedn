"""
Concept Mapping Service
Maps student syllabus topics → core concepts → underlying principles
Uses LS database syllabus as source of truth
"""

import json
from typing import Dict, List, Optional
from sqlalchemy.orm import Session


class ConceptMapper:
    """
    Extracts core concepts and principles from syllabus topics
    """

    def __init__(self, ls_db_connection_string: str = None):
        """
        Initialize with LS database connection
        """
        self.ls_db = ls_db_connection_string or "postgresql://postgres:postgres@localhost:5432/learnify_syllabus"

    async def extract_concepts_from_topic(
        self,
        board: str,
        class_name: str,
        subject: str,
        unit_name: str,
        topic_name: str
    ) -> Dict:
        """
        Extract core concepts from a specific topic using LS database

        Returns:
        {
            "topic": "Newton's Laws of Motion",
            "core_concepts": ["Force", "Inertia", "Acceleration", "Mass"],
            "underlying_principles": [...],
            "misconceptions": [...],
            "real_world_applications": [...]
        }
        """

        # TODO: Query LS database for topic details
        # For now, using AI-powered concept extraction

        from services.openrouter import generate_questions_with_claude_haiku

        prompt = f"""Analyze this syllabus topic and extract the core concepts, principles, and teaching considerations.

TOPIC: {topic_name}
UNIT: {unit_name}
SUBJECT: {subject} - Grade {class_name} ({board})

Extract and return JSON with this structure:
{{
    "topic": "{topic_name}",
    "core_concepts": [
        "Concept 1 (brief definition)",
        "Concept 2 (brief definition)"
    ],
    "underlying_principles": [
        "Principle 1: explanation",
        "Principle 2: explanation"
    ],
    "prerequisite_knowledge": [
        "What students must know before this topic"
    ],
    "common_misconceptions": [
        "Misconception 1: Why students think this",
        "Misconception 2: Why students think this"
    ],
    "real_world_applications": [
        "Application 1: context",
        "Application 2: context"
    ],
    "cross_curricular_connections": [
        "Connection to other subjects/topics"
    ],
    "key_vocabulary": [
        "Term 1", "Term 2"
    ]
}}

Focus on TEACHER-LEVEL understanding. What must a teacher know to effectively teach this topic?
"""

        response = await generate_questions_with_claude_haiku(prompt)

        # Parse JSON response
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            concept_map = json.loads(json_match.group())
            return concept_map

        # Fallback
        return {
            "topic": topic_name,
            "core_concepts": [],
            "underlying_principles": [],
            "misconceptions": [],
            "real_world_applications": []
        }

    async def map_unit_concepts(
        self,
        board: str,
        class_name: str,
        subject: str,
        unit_name: str,
        syllabus_data: Dict
    ) -> Dict:
        """
        Map all concepts in a unit

        Args:
            syllabus_data: From LS database with structure:
            {
                "unit_name": "Force and Laws of Motion",
                "learning_outcomes": [...],
                "key_concepts": [...],
                "topics": [...]
            }

        Returns:
            Complete concept map for the unit
        """

        unit_concepts = {
            "unit": unit_name,
            "topics": []
        }

        # Extract from syllabus data if available
        if syllabus_data and 'topics' in syllabus_data:
            for topic in syllabus_data['topics']:
                topic_map = await self.extract_concepts_from_topic(
                    board, class_name, subject, unit_name, topic
                )
                unit_concepts['topics'].append(topic_map)

        # Aggregate unit-level concepts
        all_concepts = []
        all_principles = []
        all_misconceptions = []

        for topic_map in unit_concepts['topics']:
            all_concepts.extend(topic_map.get('core_concepts', []))
            all_principles.extend(topic_map.get('underlying_principles', []))
            all_misconceptions.extend(topic_map.get('common_misconceptions', []))

        unit_concepts['unit_core_concepts'] = list(set(all_concepts))
        unit_concepts['unit_principles'] = list(set(all_principles))
        unit_concepts['unit_misconceptions'] = list(set(all_misconceptions))

        return unit_concepts


class ConceptDatabase:
    """
    Pre-built concept mappings for common topics
    Used as fallback when LS database query fails
    """

    CONCEPT_LIBRARY = {
        # Science - Physics
        "Newton's Laws of Motion": {
            "core_concepts": [
                "Force: A push or pull that can change an object's state of motion",
                "Inertia: Tendency of objects to resist changes in motion",
                "Mass: Measure of inertia; amount of matter in object",
                "Acceleration: Rate of change of velocity",
                "Friction: Force that opposes relative motion",
                "Action-Reaction Pairs: Equal and opposite forces on different objects"
            ],
            "underlying_principles": [
                "Objects maintain constant velocity unless acted upon by net external force",
                "Acceleration is directly proportional to net force and inversely proportional to mass (F=ma)",
                "Forces always occur in pairs acting on different objects",
                "Net force determines change in motion, not individual forces",
                "Frame of reference affects motion observation"
            ],
            "prerequisite_knowledge": [
                "Concept of velocity and acceleration",
                "Vector vs scalar quantities",
                "Basic force concept",
                "Speed and distance relationships"
            ],
            "common_misconceptions": [
                "Heavier objects fall faster (ignoring air resistance)",
                "Force is needed to keep object moving at constant velocity",
                "Action and reaction forces cancel each other (acting on same object)",
                "Friction is always harmful/unwanted",
                "Mass and weight are the same thing",
                "Velocity and acceleration are the same",
                "Objects stop because 'force runs out'"
            ],
            "real_world_applications": [
                "Seat belts and airbags (inertia protection)",
                "Rocket propulsion (action-reaction)",
                "Sports: throwing, kicking, jumping (force and acceleration)",
                "Vehicle braking systems (friction)",
                "Space travel (motion in absence of friction)"
            ],
            "teaching_sequence": [
                "Start with everyday examples (pushing cart, stopping bus)",
                "Build intuition about inertia before formal law",
                "Use demonstrations (coin-card trick, skateboard push)",
                "Address misconceptions explicitly with counter-examples",
                "Connect mathematical form F=ma to conceptual understanding"
            ]
        },

        # Mathematics
        "Linear Equations in One Variable": {
            "core_concepts": [
                "Variable: Unknown quantity represented by symbol",
                "Equation: Mathematical statement of equality",
                "Solution: Value that satisfies the equation",
                "Transposition: Moving terms across equals sign",
                "Linear: Highest power of variable is 1"
            ],
            "underlying_principles": [
                "Equality is maintained by performing same operation on both sides",
                "Inverse operations undo each other",
                "Multiple forms can represent same equation",
                "Verification confirms solution validity"
            ],
            "prerequisite_knowledge": [
                "Basic arithmetic operations",
                "Concept of variables",
                "Order of operations (BODMAS/PEMDAS)",
                "Positive and negative numbers"
            ],
            "common_misconceptions": [
                "Signs flip automatically when moving across equals (without understanding)",
                "Can't have variable on both sides",
                "Every equation has exactly one solution",
                "x = 5 and 5 = x are different",
                "Must solve in specific order"
            ],
            "real_world_applications": [
                "Age problems",
                "Money and shopping calculations",
                "Distance-speed-time problems",
                "Sharing/distribution problems",
                "Simple interest calculations"
            ],
            "teaching_sequence": [
                "Start with balance/scale analogy",
                "Simple equations first (x + 3 = 7)",
                "Build to variables on both sides",
                "Then variables with coefficients",
                "Finally complex multi-step equations"
            ]
        },

        # Add more topics as needed
    }

    @classmethod
    def get_concept_map(cls, topic_name: str) -> Optional[Dict]:
        """
        Get pre-built concept map for a topic
        """
        return cls.CONCEPT_LIBRARY.get(topic_name)

    @classmethod
    def add_concept_map(cls, topic_name: str, concept_map: Dict):
        """
        Add new concept map to library
        """
        cls.CONCEPT_LIBRARY[topic_name] = concept_map


# Global instance
concept_mapper = ConceptMapper()
concept_db = ConceptDatabase()
