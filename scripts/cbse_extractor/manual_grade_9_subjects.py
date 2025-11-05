#!/usr/bin/env python3
"""
Manual Grade 9 CBSE Syllabus Data
Complete structured data for all Grade 9 subjects based on official CBSE syllabus 2024-25
"""

import json
from pathlib import Path


def get_grade_9_mathematics():
    """Grade 9 Mathematics - Subject Code: 041"""
    return {
        "board": "CBSE",
        "grade": "9",
        "subject": "Mathematics",
        "subject_code": "041",
        "academic_year": "2024-25",
        "total_marks": 80,
        "theory_marks": 80,
        "practical_marks": 0,
        "internal_assessment": 20,
        "units": [
            {
                "unit_number": 1,
                "unit_name": "Number Systems",
                "marks": 8,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "Number Systems",
                        "topics": [
                            "Real numbers and their decimal expansions",
                            "Representation of real numbers on the number line",
                            "Operations on real numbers",
                            "Laws of exponents for real numbers",
                            "Rationalization of real numbers"
                        ],
                        "learning_outcomes": [
                            "Classify numbers as rational and irrational",
                            "Perform operations on real numbers",
                            "Represent real numbers on number line"
                        ]
                    }
                ]
            },
            {
                "unit_number": 2,
                "unit_name": "Algebra",
                "marks": 17,
                "chapters": [
                    {
                        "chapter_number": 2,
                        "chapter_name": "Polynomials",
                        "topics": [
                            "Definition of polynomial",
                            "Types of polynomials (linear, quadratic, cubic)",
                            "Zeroes of a polynomial",
                            "Remainder Theorem",
                            "Factor Theorem",
                            "Factorization of polynomials",
                            "Algebraic identities"
                        ],
                        "learning_outcomes": [
                            "Identify polynomials and their types",
                            "Apply Remainder and Factor Theorem",
                            "Factorize polynomials"
                        ]
                    },
                    {
                        "chapter_number": 3,
                        "chapter_name": "Linear Equations in Two Variables",
                        "topics": [
                            "Linear equations",
                            "Solution of a linear equation",
                            "Graph of a linear equation in two variables",
                            "Equations of lines parallel to x-axis and y-axis"
                        ],
                        "learning_outcomes": [
                            "Write linear equations in two variables",
                            "Find solutions and plot graphs",
                            "Interpret graphical representation"
                        ]
                    }
                ]
            },
            {
                "unit_number": 3,
                "unit_name": "Coordinate Geometry",
                "marks": 4,
                "chapters": [
                    {
                        "chapter_number": 4,
                        "chapter_name": "Coordinate Geometry",
                        "topics": [
                            "Cartesian plane",
                            "Coordinates of a point",
                            "Plotting points in Cartesian plane",
                            "Abscissa and ordinate"
                        ],
                        "learning_outcomes": [
                            "Locate points on Cartesian plane",
                            "Identify coordinates of given points"
                        ]
                    }
                ]
            },
            {
                "unit_number": 4,
                "unit_name": "Geometry",
                "marks": 28,
                "chapters": [
                    {
                        "chapter_number": 5,
                        "chapter_name": "Introduction to Euclid's Geometry",
                        "topics": [
                            "Euclid's definitions, axioms and postulates",
                            "Equivalent versions of Euclid's fifth postulate"
                        ],
                        "learning_outcomes": [
                            "Understand Euclid's approach to geometry",
                            "State and apply axioms and postulates"
                        ]
                    },
                    {
                        "chapter_number": 6,
                        "chapter_name": "Lines and Angles",
                        "topics": [
                            "Basic terms and definitions",
                            "Intersecting and non-intersecting lines",
                            "Pairs of angles (complementary, supplementary, adjacent, linear pair, vertically opposite)",
                            "Parallel lines and transversal",
                            "Angle sum property of a triangle"
                        ],
                        "learning_outcomes": [
                            "Identify different types of angles",
                            "Apply properties of parallel lines",
                            "Prove angle sum property"
                        ]
                    },
                    {
                        "chapter_number": 7,
                        "chapter_name": "Triangles",
                        "topics": [
                            "Congruence of triangles",
                            "Criteria for congruence (SSS, SAS, ASA, RHS)",
                            "Properties of triangles",
                            "Inequalities in triangles"
                        ],
                        "learning_outcomes": [
                            "Prove congruence of triangles",
                            "Apply congruence rules to solve problems"
                        ]
                    },
                    {
                        "chapter_number": 8,
                        "chapter_name": "Quadrilaterals",
                        "topics": [
                            "Properties of quadrilaterals",
                            "Parallelogram and its properties",
                            "Conditions for a quadrilateral to be a parallelogram",
                            "Properties of rectangle, rhombus, square, trapezium"
                        ],
                        "learning_outcomes": [
                            "Identify properties of quadrilaterals",
                            "Prove theorems on parallelograms",
                            "Apply properties to solve problems"
                        ]
                    },
                    {
                        "chapter_number": 9,
                        "chapter_name": "Circles",
                        "topics": [
                            "Chord of a circle",
                            "Properties of chords",
                            "Equal chords and their distances from centre",
                            "Angles subtended by an arc",
                            "Cyclic quadrilaterals"
                        ],
                        "learning_outcomes": [
                            "Apply properties of chords",
                            "Prove theorems on circles",
                            "Solve problems on cyclic quadrilaterals"
                        ]
                    }
                ]
            },
            {
                "unit_number": 5,
                "unit_name": "Mensuration",
                "marks": 13,
                "chapters": [
                    {
                        "chapter_number": 10,
                        "chapter_name": "Heron's Formula",
                        "topics": [
                            "Area of a triangle using Heron's formula",
                            "Application to find areas of quadrilaterals"
                        ],
                        "learning_outcomes": [
                            "Apply Heron's formula to find area",
                            "Solve real-life problems"
                        ]
                    },
                    {
                        "chapter_number": 11,
                        "chapter_name": "Surface Areas and Volumes",
                        "topics": [
                            "Surface area of cuboid and cube",
                            "Surface area of right circular cylinder",
                            "Surface area of right circular cone",
                            "Surface area of sphere and hemisphere",
                            "Volume of cuboid, cylinder, cone, sphere"
                        ],
                        "learning_outcomes": [
                            "Calculate surface areas and volumes",
                            "Apply formulas to solve problems"
                        ]
                    }
                ]
            },
            {
                "unit_number": 6,
                "unit_name": "Statistics and Probability",
                "marks": 10,
                "chapters": [
                    {
                        "chapter_number": 12,
                        "chapter_name": "Statistics",
                        "topics": [
                            "Collection of data",
                            "Presentation of data (tabular, graphical)",
                            "Measures of central tendency (mean, median, mode)",
                            "Bar graphs, histograms, frequency polygons"
                        ],
                        "learning_outcomes": [
                            "Organize and present data",
                            "Calculate mean, median, mode",
                            "Interpret statistical graphs"
                        ]
                    },
                    {
                        "chapter_number": 13,
                        "chapter_name": "Probability",
                        "topics": [
                            "Experimental approach to probability",
                            "Empirical probability",
                            "Classical probability"
                        ],
                        "learning_outcomes": [
                            "Calculate experimental probability",
                            "Distinguish between empirical and theoretical probability"
                        ]
                    }
                ]
            }
        ]
    }


def get_grade_9_science():
    """Grade 9 Science - Subject Code: 086"""
    return {
        "board": "CBSE",
        "grade": "9",
        "subject": "Science",
        "subject_code": "086",
        "academic_year": "2024-25",
        "total_marks": 80,
        "theory_marks": 80,
        "practical_marks": 0,
        "internal_assessment": 20,
        "units": [
            {
                "unit_number": 1,
                "unit_name": "Matter - Nature and Behaviour",
                "marks": 23,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "Matter in Our Surroundings",
                        "topics": [
                            "Physical nature of matter",
                            "Characteristics of particles of matter",
                            "States of matter (solid, liquid, gas)",
                            "Change of state",
                            "Evaporation"
                        ],
                        "learning_outcomes": [
                            "Classify matter based on physical properties",
                            "Explain interconversion of states"
                        ]
                    },
                    {
                        "chapter_number": 2,
                        "chapter_name": "Is Matter Around Us Pure",
                        "topics": [
                            "Mixtures and compounds",
                            "Types of mixtures (homogeneous, heterogeneous)",
                            "Solutions, suspensions, colloids",
                            "Separation techniques",
                            "Physical and chemical changes"
                        ],
                        "learning_outcomes": [
                            "Distinguish between mixtures and compounds",
                            "Apply separation techniques"
                        ]
                    },
                    {
                        "chapter_number": 3,
                        "chapter_name": "Atoms and Molecules",
                        "topics": [
                            "Laws of chemical combination",
                            "Dalton's atomic theory",
                            "Atoms, molecules, ions",
                            "Atomic and molecular mass",
                            "Mole concept",
                            "Chemical formula"
                        ],
                        "learning_outcomes": [
                            "Write chemical formulas",
                            "Apply mole concept in calculations"
                        ]
                    },
                    {
                        "chapter_number": 4,
                        "chapter_name": "Structure of the Atom",
                        "topics": [
                            "Discovery of electron, proton, neutron",
                            "Thomson's model",
                            "Rutherford's model",
                            "Bohr's model",
                            "Atomic number, mass number",
                            "Isotopes and isobars",
                            "Electronic configuration",
                            "Valency"
                        ],
                        "learning_outcomes": [
                            "Describe atomic models",
                            "Write electronic configuration",
                            "Calculate valency"
                        ]
                    }
                ]
            },
            {
                "unit_number": 2,
                "unit_name": "Organization in the Living World",
                "marks": 20,
                "chapters": [
                    {
                        "chapter_number": 5,
                        "chapter_name": "The Fundamental Unit of Life",
                        "topics": [
                            "Cell - basic unit of life",
                            "Cell organelles (nucleus, mitochondria, plastids, ER, Golgi apparatus, lysosomes, vacuoles)",
                            "Prokaryotic and eukaryotic cells",
                            "Plant cell and animal cell"
                        ],
                        "learning_outcomes": [
                            "Identify cell organelles and their functions",
                            "Differentiate plant and animal cells"
                        ]
                    },
                    {
                        "chapter_number": 6,
                        "chapter_name": "Tissues",
                        "topics": [
                            "Plant tissues (meristematic, permanent)",
                            "Animal tissues (epithelial, connective, muscular, nervous)",
                            "Structure and functions of tissues"
                        ],
                        "learning_outcomes": [
                            "Classify plant and animal tissues",
                            "Relate structure to function"
                        ]
                    }
                ]
            },
            {
                "unit_number": 3,
                "unit_name": "Motion, Force and Work",
                "marks": 27,
                "chapters": [
                    {
                        "chapter_number": 7,
                        "chapter_name": "Motion",
                        "topics": [
                            "Distance and displacement",
                            "Velocity and speed",
                            "Acceleration",
                            "Uniform and non-uniform motion",
                            "Graphical representation of motion",
                            "Equations of motion",
                            "Uniform circular motion"
                        ],
                        "learning_outcomes": [
                            "Distinguish between distance and displacement",
                            "Apply equations of motion",
                            "Interpret motion graphs"
                        ]
                    },
                    {
                        "chapter_number": 8,
                        "chapter_name": "Force and Laws of Motion",
                        "topics": [
                            "Force and its effects",
                            "Newton's laws of motion",
                            "Inertia",
                            "Momentum",
                            "Conservation of momentum",
                            "Action and reaction"
                        ],
                        "learning_outcomes": [
                            "State and apply Newton's laws",
                            "Solve problems on momentum"
                        ]
                    },
                    {
                        "chapter_number": 9,
                        "chapter_name": "Gravitation",
                        "topics": [
                            "Universal law of gravitation",
                            "Free fall",
                            "Mass and weight",
                            "Acceleration due to gravity",
                            "Archimedes' principle",
                            "Buoyancy",
                            "Relative density"
                        ],
                        "learning_outcomes": [
                            "Apply law of gravitation",
                            "Explain buoyancy and Archimedes' principle"
                        ]
                    },
                    {
                        "chapter_number": 10,
                        "chapter_name": "Work and Energy",
                        "topics": [
                            "Work done by a force",
                            "Energy (kinetic, potential)",
                            "Law of conservation of energy",
                            "Power",
                            "Commercial unit of energy"
                        ],
                        "learning_outcomes": [
                            "Calculate work and energy",
                            "Apply conservation of energy",
                            "Solve problems on power"
                        ]
                    },
                    {
                        "chapter_number": 11,
                        "chapter_name": "Sound",
                        "topics": [
                            "Nature of sound waves",
                            "Propagation of sound",
                            "Characteristics of sound (loudness, pitch, quality)",
                            "Reflection of sound (echo)",
                            "Range of hearing",
                            "Applications of ultrasound",
                            "Structure of human ear"
                        ],
                        "learning_outcomes": [
                            "Explain propagation of sound",
                            "Describe characteristics of sound waves",
                            "Apply echo principle"
                        ]
                    }
                ]
            },
            {
                "unit_number": 4,
                "unit_name": "Food, Food Production",
                "marks": 10,
                "chapters": [
                    {
                        "chapter_number": 12,
                        "chapter_name": "Improvement in Food Resources",
                        "topics": [
                            "Plant and animal breeding",
                            "Crop production management",
                            "Crop protection management",
                            "Animal husbandry",
                            "Cattle farming",
                            "Poultry farming",
                            "Fish production",
                            "Bee keeping"
                        ],
                        "learning_outcomes": [
                            "Explain crop production techniques",
                            "Describe animal husbandry practices"
                        ]
                    }
                ]
            }
        ]
    }


def get_grade_9_social_science():
    """Grade 9 Social Science - Subject Code: 087"""
    return {
        "board": "CBSE",
        "grade": "9",
        "subject": "Social Science",
        "subject_code": "087",
        "academic_year": "2024-25",
        "total_marks": 80,
        "theory_marks": 80,
        "practical_marks": 0,
        "internal_assessment": 20,
        "units": [
            {
                "unit_number": 1,
                "unit_name": "India and the Contemporary World - I (History)",
                "marks": 20,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "The French Revolution",
                        "topics": [
                            "French Society During the Late Eighteenth Century",
                            "The Outbreak of the Revolution",
                            "France Abolishes Monarchy and Becomes a Republic",
                            "The Reign of Terror",
                            "A Directory Rules France",
                            "Did Women have a Revolution?",
                            "The Abolition of Slavery",
                            "The Revolution and Everyday Life"
                        ],
                        "learning_outcomes": [
                            "Analyze causes of French Revolution",
                            "Understand impact on society and politics"
                        ]
                    },
                    {
                        "chapter_number": 2,
                        "chapter_name": "Socialism in Europe and the Russian Revolution",
                        "topics": [
                            "The Age of Social Change",
                            "The Russian Revolution",
                            "The February Revolution in Petrograd",
                            "What Changed after October",
                            "The Global Influence of the Russian Revolution"
                        ],
                        "learning_outcomes": [
                            "Explain rise of socialism",
                            "Analyze Russian Revolution and its impact"
                        ]
                    },
                    {
                        "chapter_number": 3,
                        "chapter_name": "Nazism and the Rise of Hitler",
                        "topics": [
                            "Birth of the Weimar Republic",
                            "Hitler's Rise to Power",
                            "The Nazi Worldview",
                            "Youth in Nazi Germany",
                            "The Art of Propaganda",
                            "Crimes Against Humanity"
                        ],
                        "learning_outcomes": [
                            "Understand rise of Nazism",
                            "Analyze impact of Nazi ideology"
                        ]
                    },
                    {
                        "chapter_number": 4,
                        "chapter_name": "Forest Society and Colonialism",
                        "topics": [
                            "Why Deforestation?",
                            "The Rise of Commercial Forestry",
                            "Rebellion in the Forest",
                            "Forest Transformations in Java"
                        ],
                        "learning_outcomes": [
                            "Explain colonial forest policies",
                            "Understand impact on forest communities"
                        ]
                    },
                    {
                        "chapter_number": 5,
                        "chapter_name": "Pastoralists in the Modern World",
                        "topics": [
                            "Pastoral Nomads and Their Movements",
                            "Colonial Rule and Pastoral Life",
                            "Pastoralism in Africa",
                            "Pastoralism in India"
                        ],
                        "learning_outcomes": [
                            "Understand pastoral communities",
                            "Analyze impact of colonialism on pastoralism"
                        ]
                    }
                ]
            },
            {
                "unit_number": 2,
                "unit_name": "Contemporary India - I (Geography)",
                "marks": 20,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "India - Size and Location",
                        "topics": [
                            "Location",
                            "India and the World",
                            "India's Neighbours"
                        ],
                        "learning_outcomes": [
                            "Locate India on world map",
                            "Understand India's strategic location"
                        ]
                    },
                    {
                        "chapter_number": 2,
                        "chapter_name": "Physical Features of India",
                        "topics": [
                            "The Himalayan Mountains",
                            "The Northern Plains",
                            "The Peninsular Plateau",
                            "The Indian Desert",
                            "The Coastal Plains",
                            "The Islands"
                        ],
                        "learning_outcomes": [
                            "Identify major physiographic divisions",
                            "Explain formation of landforms"
                        ]
                    },
                    {
                        "chapter_number": 3,
                        "chapter_name": "Drainage",
                        "topics": [
                            "The Himalayan Rivers",
                            "The Peninsular Rivers",
                            "Lakes",
                            "Role of Rivers in the Economy",
                            "River Pollution"
                        ],
                        "learning_outcomes": [
                            "Classify drainage systems",
                            "Explain importance of rivers"
                        ]
                    },
                    {
                        "chapter_number": 4,
                        "chapter_name": "Climate",
                        "topics": [
                            "Climate Controls",
                            "Factors Affecting India's Climate",
                            "The Indian Monsoon",
                            "The Seasons",
                            "Distribution of Rainfall",
                            "Monsoon as a Unifying Bond"
                        ],
                        "learning_outcomes": [
                            "Explain monsoon mechanism",
                            "Analyze climate patterns"
                        ]
                    },
                    {
                        "chapter_number": 5,
                        "chapter_name": "Natural Vegetation and Wildlife",
                        "topics": [
                            "Types of Vegetation",
                            "Tropical Rain Forests",
                            "Tropical Deciduous Forests",
                            "Thorny Bushes",
                            "Mountain Vegetation",
                            "Mangrove Forests",
                            "Wildlife",
                            "Conservation of Forest and Wildlife"
                        ],
                        "learning_outcomes": [
                            "Classify vegetation types",
                            "Understand conservation needs"
                        ]
                    },
                    {
                        "chapter_number": 6,
                        "chapter_name": "Population",
                        "topics": [
                            "Population Size and Distribution",
                            "Population Growth and Processes of Population Change",
                            "Age Composition",
                            "Sex Ratio",
                            "Literacy Rates",
                            "Health",
                            "National Population Policy"
                        ],
                        "learning_outcomes": [
                            "Analyze population distribution",
                            "Understand demographic indicators"
                        ]
                    }
                ]
            },
            {
                "unit_number": 3,
                "unit_name": "Democratic Politics - I (Civics)",
                "marks": 20,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "What is Democracy? Why Democracy?",
                        "topics": [
                            "What is democracy?",
                            "Features of democracy",
                            "Why democracy?",
                            "Broader meanings of democracy"
                        ],
                        "learning_outcomes": [
                            "Define democracy",
                            "Explain advantages of democracy"
                        ]
                    },
                    {
                        "chapter_number": 2,
                        "chapter_name": "Constitutional Design",
                        "topics": [
                            "Democratic Constitution in South Africa",
                            "Why do we need a Constitution?",
                            "Making of the Indian Constitution",
                            "Guiding values of Indian Constitution"
                        ],
                        "learning_outcomes": [
                            "Understand constitution-making process",
                            "Explain constitutional values"
                        ]
                    },
                    {
                        "chapter_number": 3,
                        "chapter_name": "Electoral Politics",
                        "topics": [
                            "Why Elections?",
                            "What is our System of Elections?",
                            "What makes an Election Democratic?",
                            "Electoral Politics in India"
                        ],
                        "learning_outcomes": [
                            "Explain electoral process",
                            "Understand free and fair elections"
                        ]
                    },
                    {
                        "chapter_number": 4,
                        "chapter_name": "Working of Institutions",
                        "topics": [
                            "How is the major policy decision taken?",
                            "Parliament",
                            "Political Executive",
                            "The Judiciary"
                        ],
                        "learning_outcomes": [
                            "Explain functioning of institutions",
                            "Understand checks and balances"
                        ]
                    },
                    {
                        "chapter_number": 5,
                        "chapter_name": "Democratic Rights",
                        "topics": [
                            "Life Without Rights",
                            "Rights in the Indian Constitution",
                            "Right to Equality",
                            "Right to Freedom",
                            "Right against Exploitation",
                            "Right to Freedom of Religion",
                            "Cultural and Educational Rights",
                            "Right to Constitutional Remedies",
                            "Expanding Scope of Rights"
                        ],
                        "learning_outcomes": [
                            "Explain fundamental rights",
                            "Understand right to constitutional remedies"
                        ]
                    }
                ]
            },
            {
                "unit_number": 4,
                "unit_name": "Economics (Understanding Economic Development - I)",
                "marks": 20,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "The Story of Village Palampur",
                        "topics": [
                            "Organisation of Production",
                            "Farming in Palampur",
                            "Non-farm Activities in Palampur"
                        ],
                        "learning_outcomes": [
                            "Understand production organization",
                            "Analyze economic activities in villages"
                        ]
                    },
                    {
                        "chapter_number": 2,
                        "chapter_name": "People as Resource",
                        "topics": [
                            "Economic Activities by Men and Women",
                            "Quality of Population",
                            "Unemployment",
                            "Education and Health"
                        ],
                        "learning_outcomes": [
                            "Explain human capital formation",
                            "Understand unemployment types"
                        ]
                    },
                    {
                        "chapter_number": 3,
                        "chapter_name": "Poverty as a Challenge",
                        "topics": [
                            "Poverty",
                            "Poverty Estimates",
                            "Vulnerable Groups",
                            "Inter-state Disparities",
                            "Global Poverty Scenario",
                            "Causes of Poverty",
                            "Anti-poverty Measures"
                        ],
                        "learning_outcomes": [
                            "Analyze poverty indicators",
                            "Evaluate anti-poverty programs"
                        ]
                    },
                    {
                        "chapter_number": 4,
                        "chapter_name": "Food Security in India",
                        "topics": [
                            "What is Food Security?",
                            "Why Food Security?",
                            "Who are Food Insecure?",
                            "Food Security in India",
                            "Buffer Stock",
                            "Public Distribution System",
                            "Role of Cooperatives in Food Security"
                        ],
                        "learning_outcomes": [
                            "Explain food security concept",
                            "Evaluate PDS effectiveness"
                        ]
                    }
                ]
            }
        ]
    }


def get_grade_9_english():
    """Grade 9 English - Subject Code: 184"""
    return {
        "board": "CBSE",
        "grade": "9",
        "subject": "English",
        "subject_code": "184",
        "academic_year": "2024-25",
        "total_marks": 80,
        "theory_marks": 80,
        "practical_marks": 0,
        "internal_assessment": 20,
        "units": [
            {
                "unit_number": 1,
                "unit_name": "Reading Skills",
                "marks": 20,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "Reading Comprehension",
                        "topics": [
                            "Factual passages",
                            "Discursive passages",
                            "Case-based passages"
                        ],
                        "learning_outcomes": [
                            "Extract main ideas and supporting details",
                            "Infer meanings from context",
                            "Analyze text structure"
                        ]
                    }
                ]
            },
            {
                "unit_number": 2,
                "unit_name": "Writing Skills and Grammar",
                "marks": 20,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "Writing Skills",
                        "topics": [
                            "Descriptive Paragraph (Person, Place, Event)",
                            "Story Writing",
                            "Diary Entry"
                        ],
                        "learning_outcomes": [
                            "Write descriptive paragraphs",
                            "Create engaging narratives",
                            "Express personal experiences"
                        ]
                    },
                    {
                        "chapter_number": 2,
                        "chapter_name": "Grammar",
                        "topics": [
                            "Tenses",
                            "Modals",
                            "Subject-Verb Agreement",
                            "Reported Speech",
                            "Determiners",
                            "Conjunctions"
                        ],
                        "learning_outcomes": [
                            "Apply grammar rules correctly",
                            "Transform sentences",
                            "Use appropriate tenses"
                        ]
                    }
                ]
            },
            {
                "unit_number": 3,
                "unit_name": "Literature Textbook and Supplementary Reading Text",
                "marks": 40,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "Beehive (Main Reader)",
                        "topics": [
                            "The Fun They Had",
                            "The Sound of Music",
                            "The Little Girl",
                            "A Truly Beautiful Mind",
                            "The Snake and the Mirror",
                            "My Childhood",
                            "Packing",
                            "Reach for the Top",
                            "The Bond of Love",
                            "Kathmandu",
                            "If I Were You"
                        ],
                        "subtopics": [
                            {
                                "topic": "Poetry",
                                "subtopics": [
                                    "The Road Not Taken",
                                    "Wind",
                                    "Rain on the Roof",
                                    "The Lake Isle of Innisfree",
                                    "A Legend of the Northland",
                                    "No Men Are Foreign",
                                    "The Duck and the Kangaroo",
                                    "On Killing a Tree",
                                    "The Snake Trying",
                                    "A Slumber Did My Spirit Seal"
                                ]
                            }
                        ],
                        "learning_outcomes": [
                            "Analyze literary devices",
                            "Interpret themes and characters",
                            "Appreciate poetic techniques"
                        ]
                    },
                    {
                        "chapter_number": 2,
                        "chapter_name": "Moments (Supplementary)",
                        "topics": [
                            "The Lost Child",
                            "The Adventures of Toto",
                            "Iswaran the Storyteller",
                            "In the Kingdom of Fools",
                            "The Happy Prince",
                            "Weathering the Storm in Ersama",
                            "The Last Leaf",
                            "A House is Not a Home",
                            "The Beggar"
                        ],
                        "learning_outcomes": [
                            "Understand narrative techniques",
                            "Extract moral values",
                            "Relate literature to life"
                        ]
                    }
                ]
            }
        ]
    }


def get_grade_9_hindi():
    """Grade 9 Hindi Course A - Subject Code: 002"""
    return {
        "board": "CBSE",
        "grade": "9",
        "subject": "Hindi Course A",
        "subject_code": "002",
        "academic_year": "2024-25",
        "total_marks": 80,
        "theory_marks": 80,
        "practical_marks": 0,
        "internal_assessment": 20,
        "units": [
            {
                "unit_number": 1,
                "unit_name": "अपठित बोध (Reading Comprehension)",
                "marks": 10,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "अपठित गद्यांश (Unseen Prose Passage)",
                        "topics": [
                            "तथ्यात्मक अपठित गद्यांश",
                            "विचारात्मक अपठित गद्यांश"
                        ],
                        "learning_outcomes": [
                            "गद्यांश का सार समझना",
                            "प्रश्नों के उत्तर देना"
                        ]
                    }
                ]
            },
            {
                "unit_number": 2,
                "unit_name": "व्यावहारिक व्याकरण (Applied Grammar)",
                "marks": 16,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "व्याकरण",
                        "topics": [
                            "शब्द और पद",
                            "अनुस्वार",
                            "अनुनासिक",
                            "उपसर्ग",
                            "प्रत्यय",
                            "समास",
                            "संधि",
                            "पर्यायवाची शब्द",
                            "विलोम शब्द"
                        ],
                        "learning_outcomes": [
                            "व्याकरण के नियम लागू करना",
                            "सही शब्द रचना"
                        ]
                    }
                ]
            },
            {
                "unit_number": 3,
                "unit_name": "पाठ्यपुस्तक स्पर्श भाग-1 (Textbook Sparsh Part-1)",
                "marks": 24,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "गद्य खंड (Prose)",
                        "topics": [
                            "दुःख का अधिकार (यशपाल)",
                            "एवरेस्ट: मेरी शिखर यात्रा (बचेंद्री पाल)",
                            "तुम कब जाओगे, अतिथि (शरद जोशी)",
                            "वैज्ञानिक चेतना के वाहक चंद्रशेखर वेंकट रामन् (धीरंजन मालवे)",
                            "धर्म की आड़ (गणेशशंकर विद्यार्थी)",
                            "शुक्रतारे के समान (स्वामी आनंद)"
                        ],
                        "learning_outcomes": [
                            "साहित्यिक तत्वों को समझना",
                            "लेखक के विचारों की व्याख्या"
                        ]
                    },
                    {
                        "chapter_number": 2,
                        "chapter_name": "काव्य खंड (Poetry)",
                        "topics": [
                            "रैदास - अब कैसे छूटे राम नाम रट लागी",
                            "रहीम - नई-नई लीक बनाती हैं",
                            "आदमीनामा (नजीर अकबराबादी)",
                            "एक फूल की चाह (सियारामशरण गुप्त)",
                            "गीत-अगीत (रामधारी सिंह 'दिनकर')",
                            "अग्नि पथ (हरिवंश राय बच्चन)",
                            "नए इलाके में (अरुण कमल)",
                            "खुशबू रचते हैं हाथ (अरविंद कुमार सिंह)"
                        ],
                        "learning_outcomes": [
                            "काव्य सौंदर्य की पहचान",
                            "भावार्थ की व्याख्या"
                        ]
                    }
                ]
            },
            {
                "unit_number": 4,
                "unit_name": "पूरक पाठ्यपुस्तक संचयन भाग-1 (Supplementary Sanchayan Part-1)",
                "marks": 10,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "संचयन",
                        "topics": [
                            "गिल्लू (महादेवी वर्मा)",
                            "स्मृति (श्रीराम शर्मा)",
                            "कल्लू कुम्हार की उनाकोटी (के. पी. सक्सेना)",
                            "मेरा छोटा सा निजी पुस्तकालय (धर्मवीर भारती)",
                            "हामिद खान (एस. के. पोट्टेक्काट)"
                        ],
                        "learning_outcomes": [
                            "कहानी के तत्वों को पहचानना",
                            "पात्रों का चरित्र-चित्रण"
                        ]
                    }
                ]
            },
            {
                "unit_number": 5,
                "unit_name": "लेखन (Writing)",
                "marks": 20,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "रचनात्मक लेखन",
                        "topics": [
                            "अनुच्छेद लेखन",
                            "पत्र लेखन (औपचारिक, अनौपचारिक)",
                            "संवाद लेखन",
                            "विज्ञापन लेखन",
                            "सूचना लेखन"
                        ],
                        "learning_outcomes": [
                            "सही प्रारूप में लिखना",
                            "विचारों को स्पष्ट करना"
                        ]
                    }
                ]
            }
        ]
    }


def generate_all_grade_9_json():
    """Generate JSON files for all Grade 9 subjects"""

    # Get all subject data
    subjects = {
        "mathematics": get_grade_9_mathematics(),
        "science": get_grade_9_science(),
        "social_science": get_grade_9_social_science(),
        "english": get_grade_9_english(),
        "hindi": get_grade_9_hindi()
    }

    # Create output directory
    output_dir = Path("scripts/cbse_extractor/data/structured_json")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate JSON files
    for subject_name, subject_data in subjects.items():
        filename = f"cbse_grade_9_{subject_name}.json"
        filepath = output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(subject_data, f, ensure_ascii=False, indent=2)

        print(f"✅ Generated: {filename}")
        print(f"   Size: {filepath.stat().st_size} bytes")

    print(f"\n✅ All Grade 9 JSON files generated in {output_dir}")


if __name__ == "__main__":
    generate_all_grade_9_json()
