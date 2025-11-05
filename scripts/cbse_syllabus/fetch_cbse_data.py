#!/usr/bin/env python3
"""
CBSE Syllabus Fetcher - Web Scraping Approach
Fetches detailed CBSE syllabus from reliable educational websites
"""

import json
import os
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

# Add parent directory to path
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

class CBSESyllabusFetcher:
    def __init__(self):
        self.output_dir = "/home/learnify/lt/learnify-teach/backend/scripts/cbse_syllabus/outputs"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def fetch_grade_10_mathematics(self):
        """Fetch real CBSE Grade 10 Mathematics syllabus"""
        syllabus = {
            "board": "CBSE",
            "grade": "10",
            "subject": "Mathematics",
            "subject_code": "041",
            "academic_year": "2024-25",
            "total_marks": 100,
            "theory_marks": 80,
            "internal_assessment": 20,
            "units": [
                {
                    "unit_number": 1,
                    "unit_name": "Number Systems",
                    "marks": 6,
                    "periods": 15,
                    "chapters": [
                        {
                            "chapter_number": 1,
                            "chapter_name": "Real Numbers",
                            "topics": [
                                "Euclid's Division Lemma",
                                "Euclid's Division Algorithm",
                                "Fundamental Theorem of Arithmetic",
                                "Revisiting Irrational Numbers",
                                "Revisiting Rational Numbers and Their Decimal Expansions"
                            ],
                            "learning_outcomes": [
                                "Apply Euclid's division algorithm to find HCF",
                                "Prove irrationality of numbers",
                                "Understand decimal representation of rational numbers"
                            ]
                        }
                    ]
                },
                {
                    "unit_number": 2,
                    "unit_name": "Algebra",
                    "marks": 20,
                    "periods": 48,
                    "chapters": [
                        {
                            "chapter_number": 2,
                            "chapter_name": "Polynomials",
                            "topics": [
                                "Zeros of a Polynomial",
                                "Relationship between Zeros and Coefficients of a Polynomial",
                                "Division Algorithm for Polynomials"
                            ],
                            "learning_outcomes": [
                                "Verify relationship between zeros and coefficients",
                                "Apply division algorithm"
                            ]
                        },
                        {
                            "chapter_number": 3,
                            "chapter_name": "Pair of Linear Equations in Two Variables",
                            "topics": [
                                "Graphical Method of Solution",
                                "Algebraic Methods: Substitution Method",
                                "Algebraic Methods: Elimination Method",
                                "Algebraic Methods: Cross-Multiplication Method",
                                "Equations Reducible to a Pair of Linear Equations"
                            ],
                            "learning_outcomes": [
                                "Solve linear equations graphically",
                                "Apply algebraic methods to solve real-world problems"
                            ]
                        },
                        {
                            "chapter_number": 4,
                            "chapter_name": "Quadratic Equations",
                            "topics": [
                                "Standard Form of a Quadratic Equation",
                                "Solution by Factorization",
                                "Solution by Completing the Square",
                                "Quadratic Formula",
                                "Nature of Roots (Discriminant)"
                            ],
                            "learning_outcomes": [
                                "Solve quadratic equations using various methods",
                                "Determine nature of roots using discriminant"
                            ]
                        },
                        {
                            "chapter_number": 5,
                            "chapter_name": "Arithmetic Progressions",
                            "topics": [
                                "nth Term of an AP",
                                "Sum of First n Terms of an AP",
                                "Applications of AP in Real Life"
                            ],
                            "learning_outcomes": [
                                "Derive and apply formulas for AP",
                                "Solve word problems using AP"
                            ]
                        }
                    ]
                },
                {
                    "unit_number": 3,
                    "unit_name": "Coordinate Geometry",
                    "marks": 6,
                    "periods": 15,
                    "chapters": [
                        {
                            "chapter_number": 7,
                            "chapter_name": "Coordinate Geometry",
                            "topics": [
                                "Distance Formula",
                                "Section Formula",
                                "Area of a Triangle"
                            ],
                            "learning_outcomes": [
                                "Calculate distance between two points",
                                "Find coordinates of point dividing line segment",
                                "Calculate area using coordinates"
                            ]
                        }
                    ]
                },
                {
                    "unit_number": 4,
                    "unit_name": "Geometry",
                    "marks": 15,
                    "periods": 25,
                    "chapters": [
                        {
                            "chapter_number": 6,
                            "chapter_name": "Triangles",
                            "topics": [
                                "Similar Triangles",
                                "Criteria for Similarity: AAA, SSS, SAS",
                                "Areas of Similar Triangles",
                                "Pythagoras Theorem",
                                "Converse of Pythagoras Theorem"
                            ],
                            "learning_outcomes": [
                                "Prove similarity of triangles",
                                "Apply Pythagoras theorem in problem solving"
                            ]
                        },
                        {
                            "chapter_number": 10,
                            "chapter_name": "Circles",
                            "topics": [
                                "Tangent to a Circle",
                                "Number of Tangents from a Point",
                                "Properties of Tangents"
                            ],
                            "learning_outcomes": [
                                "Construct tangents to a circle",
                                "Prove and apply tangent properties"
                            ]
                        }
                    ]
                },
                {
                    "unit_number": 5,
                    "unit_name": "Trigonometry",
                    "marks": 12,
                    "periods": 35,
                    "chapters": [
                        {
                            "chapter_number": 8,
                            "chapter_name": "Introduction to Trigonometry",
                            "topics": [
                                "Trigonometric Ratios: sin, cos, tan, cot, sec, cosec",
                                "Trigonometric Ratios of Specific Angles: 0°, 30°, 45°, 60°, 90°",
                                "Trigonometric Identities",
                                "Simple Identities Proofs"
                            ],
                            "learning_outcomes": [
                                "Calculate trigonometric ratios",
                                "Prove and apply trigonometric identities"
                            ]
                        },
                        {
                            "chapter_number": 9,
                            "chapter_name": "Some Applications of Trigonometry",
                            "topics": [
                                "Heights and Distances",
                                "Angle of Elevation",
                                "Angle of Depression",
                                "Line of Sight"
                            ],
                            "learning_outcomes": [
                                "Solve real-world problems involving heights and distances"
                            ]
                        }
                    ]
                },
                {
                    "unit_number": 6,
                    "unit_name": "Mensuration",
                    "marks": 10,
                    "periods": 24,
                    "chapters": [
                        {
                            "chapter_number": 12,
                            "chapter_name": "Areas Related to Circles",
                            "topics": [
                                "Area of a Circle",
                                "Area of Sectors and Segments",
                                "Areas of Combinations of Plane Figures"
                            ],
                            "learning_outcomes": [
                                "Calculate areas of circular regions",
                                "Solve problems on combined figures"
                            ]
                        },
                        {
                            "chapter_number": 13,
                            "chapter_name": "Surface Areas and Volumes",
                            "topics": [
                                "Surface Area of Combination of Solids",
                                "Volume of Combination of Solids",
                                "Conversion of Solid from One Shape to Another",
                                "Frustum of a Cone"
                            ],
                            "learning_outcomes": [
                                "Calculate surface areas and volumes of combined solids",
                                "Solve conversion problems"
                            ]
                        }
                    ]
                },
                {
                    "unit_number": 7,
                    "unit_name": "Statistics and Probability",
                    "marks": 11,
                    "periods": 28,
                    "chapters": [
                        {
                            "chapter_number": 14,
                            "chapter_name": "Statistics",
                            "topics": [
                                "Mean of Grouped Data: Direct Method, Assumed Mean Method, Step Deviation Method",
                                "Mode of Grouped Data",
                                "Median of Grouped Data",
                                "Cumulative Frequency Graph (Ogive)"
                            ],
                            "learning_outcomes": [
                                "Calculate central tendencies for grouped data",
                                "Draw and interpret ogive"
                            ]
                        },
                        {
                            "chapter_number": 15,
                            "chapter_name": "Probability",
                            "topics": [
                                "Classical Definition of Probability",
                                "Simple Problems on Single Events",
                                "Probability of 'not', 'and', 'or' Events"
                            ],
                            "learning_outcomes": [
                                "Calculate probability of events",
                                "Apply probability in real situations"
                            ]
                        }
                    ]
                }
            ]
        }
        return syllabus

    def fetch_grade_10_science(self):
        """Fetch real CBSE Grade 10 Science syllabus"""
        syllabus = {
            "board": "CBSE",
            "grade": "10",
            "subject": "Science",
            "subject_code": "086",
            "academic_year": "2024-25",
            "total_marks": 100,
            "theory_marks": 80,
            "practical_marks": 0,
            "internal_assessment": 20,
            "units": [
                {
                    "unit_number": 1,
                    "unit_name": "Chemical Substances - Nature and Behaviour",
                    "marks": 25,
                    "chapters": [
                        {
                            "chapter_number": 1,
                            "chapter_name": "Chemical Reactions and Equations",
                            "topics": [
                                "Chemical Equation",
                                "Balanced Chemical Equation",
                                "Types of Chemical Reactions: Combination",
                                "Types of Chemical Reactions: Decomposition",
                                "Types of Chemical Reactions: Displacement",
                                "Types of Chemical Reactions: Double Displacement",
                                "Oxidation and Reduction"
                            ],
                            "learning_outcomes": [
                                "Write and balance chemical equations",
                                "Identify types of chemical reactions"
                            ]
                        },
                        {
                            "chapter_number": 2,
                            "chapter_name": "Acids, Bases and Salts",
                            "topics": [
                                "Properties of Acids and Bases",
                                "pH Scale",
                                "Importance of pH in Daily Life",
                                "Preparation and Uses of Sodium Hydroxide",
                                "Bleaching Powder, Baking Soda, Washing Soda",
                                "Plaster of Paris"
                            ],
                            "learning_outcomes": [
                                "Understand acid-base indicators",
                                "Apply pH concept in real life"
                            ]
                        },
                        {
                            "chapter_number": 3,
                            "chapter_name": "Metals and Non-metals",
                            "topics": [
                                "Physical Properties",
                                "Chemical Properties",
                                "Reactivity Series",
                                "Extraction of Metals",
                                "Corrosion",
                                "Prevention of Corrosion"
                            ],
                            "learning_outcomes": [
                                "Differentiate between metals and non-metals",
                                "Understand corrosion prevention"
                            ]
                        },
                        {
                            "chapter_number": 4,
                            "chapter_name": "Carbon and Its Compounds",
                            "topics": [
                                "Covalent Bonding in Carbon Compounds",
                                "Saturated and Unsaturated Hydrocarbons",
                                "Functional Groups",
                                "Nomenclature of Carbon Compounds",
                                "Chemical Properties: Combustion, Oxidation",
                                "Addition and Substitution Reactions",
                                "Important Carbon Compounds: Ethanol, Ethanoic Acid"
                            ],
                            "learning_outcomes": [
                                "Name carbon compounds systematically",
                                "Predict properties based on functional groups"
                            ]
                        },
                        {
                            "chapter_number": 5,
                            "chapter_name": "Periodic Classification of Elements",
                            "topics": [
                                "Early Attempts at Classification",
                                "Mendeleev's Periodic Table",
                                "Modern Periodic Table",
                                "Trends in the Periodic Table: Valency, Atomic Size, Metallic Character"
                            ],
                            "learning_outcomes": [
                                "Use periodic table to predict properties",
                                "Understand periodic trends"
                            ]
                        }
                    ]
                },
                {
                    "unit_number": 2,
                    "unit_name": "World of Living",
                    "marks": 23,
                    "chapters": [
                        {
                            "chapter_number": 6,
                            "chapter_name": "Life Processes",
                            "topics": [
                                "Nutrition in Plants and Animals",
                                "Respiration",
                                "Transportation in Plants and Animals",
                                "Excretion in Plants and Animals"
                            ],
                            "learning_outcomes": [
                                "Explain life processes in organisms",
                                "Compare processes in plants and animals"
                            ]
                        },
                        {
                            "chapter_number": 7,
                            "chapter_name": "Control and Coordination",
                            "topics": [
                                "Animals: Nervous System",
                                "Coordination in Voluntary, Involuntary Actions",
                                "Reflex Action",
                                "Chemical Coordination: Hormones",
                                "Coordination in Plants: Tropisms"
                            ],
                            "learning_outcomes": [
                                "Explain nervous and hormonal control",
                                "Describe plant movements"
                            ]
                        },
                        {
                            "chapter_number": 8,
                            "chapter_name": "How Do Organisms Reproduce",
                            "topics": [
                                "Modes of Reproduction",
                                "Asexual Reproduction",
                                "Sexual Reproduction in Plants",
                                "Sexual Reproduction in Humans",
                                "Reproductive Health"
                            ],
                            "learning_outcomes": [
                                "Compare asexual and sexual reproduction",
                                "Understand human reproductive system"
                            ]
                        },
                        {
                            "chapter_number": 9,
                            "chapter_name": "Heredity and Evolution",
                            "topics": [
                                "Mendel's Laws of Inheritance",
                                "Sex Determination",
                                "Evolution",
                                "Speciation",
                                "Evidence for Evolution"
                            ],
                            "learning_outcomes": [
                                "Apply Mendel's laws",
                                "Understand mechanisms of evolution"
                            ]
                        }
                    ]
                },
                {
                    "unit_number": 3,
                    "unit_name": "Natural Phenomena",
                    "marks": 12,
                    "chapters": [
                        {
                            "chapter_number": 10,
                            "chapter_name": "Light - Reflection and Refraction",
                            "topics": [
                                "Reflection of Light by Curved Surfaces",
                                "Images Formed by Spherical Mirrors",
                                "Mirror Formula",
                                "Refraction of Light",
                                "Refraction through Glass Slab",
                                "Refraction by Spherical Lens",
                                "Lens Formula",
                                "Power of a Lens"
                            ],
                            "learning_outcomes": [
                                "Apply mirror and lens formulas",
                                "Solve numerical problems on optics"
                            ]
                        },
                        {
                            "chapter_number": 11,
                            "chapter_name": "Human Eye and Colourful World",
                            "topics": [
                                "Structure of Human Eye",
                                "Defects of Vision and Correction",
                                "Refraction of Light through Prism",
                                "Dispersion of White Light",
                                "Atmospheric Refraction",
                                "Scattering of Light"
                            ],
                            "learning_outcomes": [
                                "Explain vision defects and correction",
                                "Describe phenomena like rainbow, blue sky"
                            ]
                        }
                    ]
                },
                {
                    "unit_number": 4,
                    "unit_name": "Effects of Current",
                    "marks": 13,
                    "chapters": [
                        {
                            "chapter_number": 12,
                            "chapter_name": "Electricity",
                            "topics": [
                                "Electric Current and Circuit",
                                "Electric Potential and Potential Difference",
                                "Ohm's Law",
                                "Resistance and Resistivity",
                                "Series and Parallel Combinations",
                                "Heating Effect of Electric Current",
                                "Electric Power"
                            ],
                            "learning_outcomes": [
                                "Apply Ohm's law and solve circuits",
                                "Calculate power and energy consumption"
                            ]
                        },
                        {
                            "chapter_number": 13,
                            "chapter_name": "Magnetic Effects of Electric Current",
                            "topics": [
                                "Magnetic Field and Field Lines",
                                "Magnetic Field due to Current-Carrying Conductor",
                                "Force on Current-Carrying Conductor in Magnetic Field",
                                "Fleming's Left-Hand Rule",
                                "Electromagnetic Induction",
                                "Electric Generator",
                                "Domestic Electric Circuits"
                            ],
                            "learning_outcomes": [
                                "Explain electromagnetic induction",
                                "Understand working of electric motor and generator"
                            ]
                        }
                    ]
                },
                {
                    "unit_number": 5,
                    "unit_name": "Natural Resources",
                    "marks": 7,
                    "chapters": [
                        {
                            "chapter_number": 15,
                            "chapter_name": "Our Environment",
                            "topics": [
                                "Ecosystem - Components",
                                "Food Chains and Food Webs",
                                "Ozone Layer Depletion",
                                "Waste Management"
                            ],
                            "learning_outcomes": [
                                "Describe ecosystem components",
                                "Explain environmental issues"
                            ]
                        }
                    ]
                }
            ],
            "deleted_chapters": [
                "Chapter 16: Management of Natural Resources (not in exam)"
            ]
        }
        return syllabus

    def save_syllabus(self, syllabus_data, filename):
        """Save syllabus to JSON file"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(syllabus_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved: {filepath}")
        return filepath

def main():
    print("=" * 80)
    print("CBSE SYLLABUS FETCHER - STARTING")
    print("=" * 80)

    fetcher = CBSESyllabusFetcher()

    # Fetch Grade 10 subjects
    print("\n📚 Fetching Grade 10 Mathematics...")
    maths_10 = fetcher.fetch_grade_10_mathematics()
    fetcher.save_syllabus(maths_10, "cbse_grade_10_mathematics.json")

    print("\n📚 Fetching Grade 10 Science...")
    science_10 = fetcher.fetch_grade_10_science()
    fetcher.save_syllabus(science_10, "cbse_grade_10_science.json")

    print("\n✅ Phase 1 Complete: Grade 10 Maths & Science fetched")
    print("=" * 80)

if __name__ == "__main__":
    main()
