# services/curriculum_data.py
import httpx
import asyncio
from typing import Dict, List, Any

class CurriculumDataService:
    """Service to fetch and provide curriculum-specific data for question generation"""

    def __init__(self):
        self.curriculum_cache = {}
        self.official_sources = {
            "CBSE": {
                "base_url": "https://cbseacademic.nic.in",
                "syllabus_patterns": [
                    "/web_material/CurriculumMain26/Sec/{subject}_Sec_2025-26.pdf",
                    "/curriculum_2026.html"
                ]
            },
            "NCERT": {
                "base_url": "https://ncert.nic.in",
                "learning_outcomes": "/pdf/publication/otherpublications/learning_outcomes.pdf"
            }
        }

    def get_cbse_mathematics_curriculum(self, grade: str) -> Dict[str, Any]:
        """Get CBSE Mathematics curriculum data for specific grade"""
        grade_num = self._normalize_grade(grade)

        if grade_num == 1:
            return self._get_grade_1_cbse_math()
        elif grade_num == 2:
            return self._get_grade_2_cbse_math()
        elif grade_num == 3:
            return self._get_grade_3_cbse_math()
        elif grade_num == 4:
            return self._get_grade_4_cbse_math()
        elif grade_num == 5:
            return self._get_grade_5_cbse_math()
        elif grade_num == 6:
            return self._get_grade_6_cbse_math()
        elif grade_num == 7:
            return self._get_grade_7_cbse_math()
        elif grade_num == 8:
            return self._get_grade_8_cbse_math()
        elif grade_num == 9:
            return self._get_grade_9_cbse_math()
        elif grade_num == 10:
            return self._get_grade_10_cbse_math()
        else:
            return {}

    def _normalize_grade(self, grade: str) -> int:
        """Convert grade string to number"""
        grade_str = str(grade).lower().strip()
        if grade_str in ["1", "i", "class 1", "grade 1", "first"]:
            return 1
        elif grade_str in ["2", "ii", "class 2", "grade 2", "second"]:
            return 2
        elif grade_str in ["3", "iii", "class 3", "grade 3", "third"]:
            return 3
        elif grade_str in ["4", "iv", "class 4", "grade 4", "fourth"]:
            return 4
        elif grade_str in ["5", "v", "class 5", "grade 5", "fifth"]:
            return 5
        elif grade_str in ["6", "vi", "class 6", "grade 6", "sixth"]:
            return 6
        elif grade_str in ["7", "vii", "class 7", "grade 7", "seventh"]:
            return 7
        elif grade_str in ["8", "viii", "class 8", "grade 8", "eighth"]:
            return 8
        elif grade_str in ["9", "ix", "class 9", "grade 9", "ninth"]:
            return 9
        elif grade_str in ["10", "x", "class 10", "grade 10", "tenth"]:
            return 10
        return 0

    def _get_grade_5_cbse_math(self) -> Dict[str, Any]:
        """CBSE Grade 5 Mathematics curriculum"""
        return {
            "units": {
                "Numbers and Operations": {
                    "weightage": "25%",
                    "topics": [
                        "Large Numbers (up to 10 lakhs)",
                        "Place Value and Face Value",
                        "Addition and Subtraction of Large Numbers",
                        "Multiplication (3-digit by 2-digit)",
                        "Division (4-digit by 2-digit)",
                        "Factors and Multiples",
                        "Prime and Composite Numbers"
                    ],
                    "learning_outcomes": [
                        "Read and write numbers up to 10 lakhs",
                        "Understand place value system",
                        "Perform operations on large numbers",
                        "Identify factors and multiples",
                        "Distinguish prime and composite numbers"
                    ]
                },
                "Fractions and Decimals": {
                    "weightage": "20%",
                    "topics": [
                        "Proper, Improper and Mixed Fractions",
                        "Equivalent Fractions",
                        "Addition and Subtraction of Fractions",
                        "Introduction to Decimals",
                        "Decimal Place Value",
                        "Addition and Subtraction of Decimals"
                    ],
                    "learning_outcomes": [
                        "Identify different types of fractions",
                        "Compare and order fractions",
                        "Perform basic operations on fractions",
                        "Understand decimal notation",
                        "Add and subtract decimals"
                    ]
                },
                "Geometry": {
                    "weightage": "20%",
                    "topics": [
                        "Lines, Line Segments and Rays",
                        "Angles - Types and Measurement",
                        "Triangles - Types and Properties",
                        "Circles - Center, Radius, Diameter",
                        "Quadrilaterals - Rectangle, Square, Parallelogram",
                        "Symmetry"
                    ],
                    "learning_outcomes": [
                        "Identify basic geometric shapes",
                        "Classify angles and triangles",
                        "Understand properties of shapes",
                        "Recognize symmetrical figures",
                        "Draw basic geometric figures"
                    ]
                },
                "Measurement": {
                    "weightage": "15%",
                    "topics": [
                        "Length - km, m, cm, mm",
                        "Weight - kg, g",
                        "Capacity - l, ml",
                        "Time - Hours, Minutes, Seconds",
                        "Area and Perimeter of Simple Shapes",
                        "Money - Rupees and Paise"
                    ],
                    "learning_outcomes": [
                        "Convert between units of measurement",
                        "Solve problems involving measurement",
                        "Calculate area and perimeter",
                        "Work with time and money",
                        "Apply measurement in real situations"
                    ]
                },
                "Data Handling": {
                    "weightage": "10%",
                    "topics": [
                        "Collection and Organization of Data",
                        "Pictographs",
                        "Bar Graphs",
                        "Reading and Interpreting Simple Charts"
                    ],
                    "learning_outcomes": [
                        "Collect and organize data",
                        "Create simple pictographs",
                        "Read and interpret bar graphs",
                        "Draw conclusions from data"
                    ]
                },
                "Patterns": {
                    "weightage": "10%",
                    "topics": [
                        "Number Patterns",
                        "Shape Patterns",
                        "Growing Patterns",
                        "Pattern Rules"
                    ],
                    "learning_outcomes": [
                        "Identify number patterns",
                        "Continue pattern sequences",
                        "Create their own patterns",
                        "Explain pattern rules"
                    ]
                }
            },
            "assessment_pattern": {
                "total_marks": 100,
                "theory_exam": 80,
                "internal_assessment": 20,
                "question_types": {
                    "mcq": "20%",
                    "fill_blanks": "15%",
                    "short_answer": "35%",
                    "word_problems": "20%",
                    "true_false": "10%"
                }
            },
            "age_appropriate_features": {
                "vocabulary": "Simple, everyday language",
                "context": "Real-life situations familiar to children",
                "difficulty": "Age-appropriate problem solving",
                "examples": "Toys, games, school, family scenarios"
            }
        }

    # Placeholder methods for all grade levels
    def _get_grade_1_cbse_math(self) -> Dict[str, Any]:
        return {"units": {"Numbers 1-100": {"topics": ["Counting", "Addition", "Subtraction"]}}}

    def _get_grade_2_cbse_math(self) -> Dict[str, Any]:
        return {"units": {"Numbers 1-1000": {"topics": ["Place Value", "Addition", "Subtraction", "Multiplication"]}}}

    def _get_grade_3_cbse_math(self) -> Dict[str, Any]:
        return {"units": {"Numbers and Operations": {"topics": ["4-digit numbers", "Multiplication", "Division", "Fractions"]}}}

    def _get_grade_4_cbse_math(self) -> Dict[str, Any]:
        return {"units": {"Numbers and Operations": {"topics": ["5-digit numbers", "Factors", "Multiples", "Fractions", "Decimals"]}}}

    def _get_grade_6_cbse_math(self) -> Dict[str, Any]:
        return {"units": {"Algebra": {"topics": ["Variables", "Expressions", "Equations"]}, "Geometry": {"topics": ["Angles", "Triangles"]}}}

    def _get_grade_7_cbse_math(self) -> Dict[str, Any]:
        return {"units": {"Algebra": {"topics": ["Linear Equations", "Ratios"]}, "Geometry": {"topics": ["Congruence", "Symmetry"]}}}

    def _get_grade_8_cbse_math(self) -> Dict[str, Any]:
        return {"units": {"Algebra": {"topics": ["Factorization", "Linear Equations"]}, "Geometry": {"topics": ["Quadrilaterals", "Area"]}}}

    def _get_grade_9_cbse_math(self) -> Dict[str, Any]:
        return {"units": {"Number Systems": {"topics": ["Real Numbers"]}, "Algebra": {"topics": ["Polynomials", "Linear Equations"]}}}

    def _get_grade_10_cbse_math(self) -> Dict[str, Any]:
        return {
            "units": {
                "Number Systems": {
                    "weightage": "6%",
                    "topics": ["Real Numbers", "Irrational numbers", "Rational numbers and their decimal expansions"]
                },
                "Algebra": {
                    "weightage": "25%",
                    "topics": ["Polynomials", "Pair of Linear Equations in Two Variables", "Quadratic Equations"]
                }
            }
        }

    def get_cbse_science_curriculum(self, grade: str) -> Dict[str, Any]:
        """Get CBSE Science curriculum data for specific grade"""
        if grade in ["9", "10", "IX", "X"]:
            return {
                "units": {
                    "Physics": {
                        "topics": ["Light", "Electricity", "Magnetic Effects of Current", "Sources of Energy"],
                        "weightage": "25%"
                    },
                    "Chemistry": {
                        "topics": ["Acids, Bases and Salts", "Metals and Non-metals", "Carbon Compounds", "Periodic Classification"],
                        "weightage": "25%"
                    },
                    "Biology": {
                        "topics": ["Life Processes", "Control and Coordination", "Reproduction", "Heredity and Evolution"],
                        "weightage": "50%"
                    }
                }
            }
        return {}

    def get_curriculum_data(self, board: str, subject: str, grade: str) -> Dict[str, Any]:
        """Get curriculum data for specific board, subject and grade"""
        key = f"{board.lower()}_{subject.lower()}_{grade.lower()}"

        if key in self.curriculum_cache:
            return self.curriculum_cache[key]

        curriculum_data = {}

        if board.upper() == "CBSE":
            if "math" in subject.lower():
                curriculum_data = self.get_cbse_mathematics_curriculum(grade)
            elif "science" in subject.lower():
                curriculum_data = self.get_cbse_science_curriculum(grade)

        elif board.upper() == "ICSE":
            if "math" in subject.lower():
                curriculum_data = self.get_icse_mathematics_curriculum(grade)
            else:
                curriculum_data = {"note": "ICSE curriculum", "board": "ICSE"}

        elif board.upper() in ["STATE", "STATE BOARD"]:
            if "math" in subject.lower():
                curriculum_data = self.get_state_board_mathematics_curriculum(grade)
            else:
                curriculum_data = {"note": "State Board curriculum", "board": "State"}

        self.curriculum_cache[key] = curriculum_data
        return curriculum_data

    def get_icse_mathematics_curriculum(self, grade: str) -> Dict[str, Any]:
        """Get ICSE Mathematics curriculum data for specific grade"""
        base_curriculum = self.get_cbse_mathematics_curriculum(grade)
        if base_curriculum:
            base_curriculum["board_features"] = {
                "approach": "Comprehensive and application-based",
                "emphasis": "Practical problem solving"
            }
        return base_curriculum

    def get_state_board_mathematics_curriculum(self, grade: str) -> Dict[str, Any]:
        """Get State Board Mathematics curriculum data for specific grade"""
        base_curriculum = self.get_cbse_mathematics_curriculum(grade)
        if base_curriculum:
            base_curriculum["board_features"] = {
                "approach": "State-specific with local context",
                "emphasis": "Regional examples"
            }
        return base_curriculum

    def get_enhanced_curriculum_context(self, board: str, subject: str, grade: str) -> Dict[str, Any]:
        """Get enhanced curriculum context with real-world application examples"""
        base_data = self.get_curriculum_data(board, subject, grade)

        if not base_data:
            return base_data

        # Add real-world application context
        base_data["real_world_applications"] = self._get_real_world_applications(subject, grade)
        base_data["common_misconceptions"] = self._get_common_misconceptions(subject, grade)
        base_data["prerequisite_knowledge"] = self._get_prerequisite_knowledge(subject, grade)

        return base_data

    def _get_real_world_applications(self, subject: str, grade: str) -> List[str]:
        """Get real-world applications for subject topics"""
        if "math" in subject.lower():
            return [
                "Using numbers in shopping and money calculations",
                "Measuring ingredients while cooking",
                "Understanding time and schedules",
                "Calculating distances and travel time",
                "Organizing data from surveys and games",
                "Creating patterns in art and crafts"
            ]
        return ["Real-life problem solving", "Practical applications"]

    def _get_common_misconceptions(self, subject: str, grade: str) -> List[str]:
        """Get common student misconceptions for the subject"""
        if "math" in subject.lower():
            return [
                "Confusing place value positions",
                "Difficulty with borrowing in subtraction",
                "Mixing up multiplication tables",
                "Not understanding fraction equivalence",
                "Confusion between area and perimeter"
            ]
        return ["Common learning challenges"]

    def _get_prerequisite_knowledge(self, subject: str, grade: str) -> List[str]:
        """Get prerequisite knowledge for the subject and grade"""
        grade_num = self._normalize_grade(grade)
        if "math" in subject.lower() and grade_num == 5:
            return [
                "Basic addition and subtraction (Grade 1-2)",
                "Multiplication tables up to 10 (Grade 3-4)",
                "Understanding of place value (Grade 2-4)",
                "Basic shapes and measurements (Grade 1-4)",
                "Simple data collection (Grade 3-4)"
            ]
        return []

# Global instance
curriculum_service = CurriculumDataService()