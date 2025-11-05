#!/usr/bin/env python3
"""
Manual Grade 8 CBSE Syllabus Data
Complete structured data for all Grade 8 subjects based on NCERT textbooks 2024-25
"""

import json
from pathlib import Path


def get_grade_8_mathematics():
    """Grade 8 Mathematics - Based on NCERT"""
    return {
        "board": "CBSE",
        "grade": "8",
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
                "unit_name": "Rational Numbers",
                "marks": 6,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "Rational Numbers",
                        "topics": [
                            "Properties of rational numbers",
                            "Representation of rational numbers on number line",
                            "Rational numbers between two rational numbers",
                            "Operations on rational numbers",
                            "Additive and multiplicative identity"
                        ],
                        "learning_outcomes": [
                            "Perform operations on rational numbers",
                            "Apply properties of rational numbers"
                        ]
                    }
                ]
            },
            {
                "unit_number": 2,
                "unit_name": "Linear Equations in One Variable",
                "marks": 7,
                "chapters": [
                    {
                        "chapter_number": 2,
                        "chapter_name": "Linear Equations in One Variable",
                        "topics": [
                            "Solving linear equations with variables on both sides",
                            "Reducing equations to simpler form",
                            "Word problems on linear equations",
                            "Applications of linear equations"
                        ],
                        "learning_outcomes": [
                            "Solve linear equations",
                            "Apply to real-world problems"
                        ]
                    }
                ]
            },
            {
                "unit_number": 3,
                "unit_name": "Understanding Quadrilaterals",
                "marks": 6,
                "chapters": [
                    {
                        "chapter_number": 3,
                        "chapter_name": "Understanding Quadrilaterals",
                        "topics": [
                            "Polygons and their classification",
                            "Angle sum property of polygons",
                            "Types of quadrilaterals",
                            "Properties of parallelogram, rhombus, rectangle, square, trapezium",
                            "Some special parallelograms"
                        ],
                        "learning_outcomes": [
                            "Classify quadrilaterals",
                            "Apply angle sum properties"
                        ]
                    }
                ]
            },
            {
                "unit_number": 4,
                "unit_name": "Practical Geometry",
                "marks": 5,
                "chapters": [
                    {
                        "chapter_number": 4,
                        "chapter_name": "Practical Geometry",
                        "topics": [
                            "Constructing quadrilaterals",
                            "Construction when four sides and one diagonal are given",
                            "Construction when three sides and two diagonals are given",
                            "Construction when two adjacent sides and three angles are given"
                        ],
                        "learning_outcomes": [
                            "Construct quadrilaterals with given conditions",
                            "Use geometric tools accurately"
                        ]
                    }
                ]
            },
            {
                "unit_number": 5,
                "unit_name": "Data Handling",
                "marks": 5,
                "chapters": [
                    {
                        "chapter_number": 5,
                        "chapter_name": "Data Handling",
                        "topics": [
                            "Looking for information - organizing data",
                            "Grouping data",
                            "Circle graph or pie chart",
                            "Chance and probability",
                            "Getting a result"
                        ],
                        "learning_outcomes": [
                            "Organize and interpret data",
                            "Calculate probability of events"
                        ]
                    }
                ]
            },
            {
                "unit_number": 6,
                "unit_name": "Squares and Square Roots",
                "marks": 6,
                "chapters": [
                    {
                        "chapter_number": 6,
                        "chapter_name": "Squares and Square Roots",
                        "topics": [
                            "Properties of square numbers",
                            "Patterns in square numbers",
                            "Finding square of a number",
                            "Square roots",
                            "Finding square root by prime factorization",
                            "Finding square root by division method",
                            "Square roots of decimals"
                        ],
                        "learning_outcomes": [
                            "Find squares and square roots",
                            "Apply different methods for finding square roots"
                        ]
                    }
                ]
            },
            {
                "unit_number": 7,
                "unit_name": "Cubes and Cube Roots",
                "marks": 5,
                "chapters": [
                    {
                        "chapter_number": 7,
                        "chapter_name": "Cubes and Cube Roots",
                        "topics": [
                            "Cubes",
                            "Cube roots",
                            "Cube root through prime factorization"
                        ],
                        "learning_outcomes": [
                            "Find cubes and cube roots",
                            "Apply prime factorization method"
                        ]
                    }
                ]
            },
            {
                "unit_number": 8,
                "unit_name": "Comparing Quantities",
                "marks": 8,
                "chapters": [
                    {
                        "chapter_number": 8,
                        "chapter_name": "Comparing Quantities",
                        "topics": [
                            "Ratios and percentages",
                            "Profit and loss",
                            "Discount",
                            "Sales tax / Value Added Tax / Goods and Services Tax",
                            "Compound interest",
                            "Deducing a formula for compound interest"
                        ],
                        "learning_outcomes": [
                            "Solve problems on profit, loss, discount",
                            "Calculate compound interest",
                            "Understand taxation"
                        ]
                    }
                ]
            },
            {
                "unit_number": 9,
                "unit_name": "Algebraic Expressions and Identities",
                "marks": 10,
                "chapters": [
                    {
                        "chapter_number": 9,
                        "chapter_name": "Algebraic Expressions and Identities",
                        "topics": [
                            "Expressions with variables",
                            "Terms, factors and coefficients",
                            "Monomials, binomials, polynomials",
                            "Addition and subtraction of algebraic expressions",
                            "Multiplication of algebraic expressions",
                            "Identities: (a+b)², (a-b)², (a²-b²)",
                            "Applying identities"
                        ],
                        "learning_outcomes": [
                            "Perform operations on algebraic expressions",
                            "Apply algebraic identities"
                        ]
                    }
                ]
            },
            {
                "unit_number": 10,
                "unit_name": "Visualising Solid Shapes",
                "marks": 3,
                "chapters": [
                    {
                        "chapter_number": 10,
                        "chapter_name": "Visualising Solid Shapes",
                        "topics": [
                            "Views of 3D shapes",
                            "Mapping space around us",
                            "Faces, edges and vertices"
                        ],
                        "learning_outcomes": [
                            "Visualize 3D shapes from 2D representations",
                            "Identify faces, edges, vertices"
                        ]
                    }
                ]
            },
            {
                "unit_number": 11,
                "unit_name": "Mensuration",
                "marks": 8,
                "chapters": [
                    {
                        "chapter_number": 11,
                        "chapter_name": "Mensuration",
                        "topics": [
                            "Area of polygon",
                            "Area of trapezium",
                            "Solid shapes",
                            "Surface area of cube, cuboid, cylinder",
                            "Volume of cube, cuboid, cylinder"
                        ],
                        "learning_outcomes": [
                            "Calculate areas of polygons",
                            "Find surface area and volume of solids"
                        ]
                    }
                ]
            },
            {
                "unit_number": 12,
                "unit_name": "Exponents and Powers",
                "marks": 4,
                "chapters": [
                    {
                        "chapter_number": 12,
                        "chapter_name": "Exponents and Powers",
                        "topics": [
                            "Powers with negative exponents",
                            "Laws of exponents",
                            "Use of exponents to express small numbers in standard form"
                        ],
                        "learning_outcomes": [
                            "Apply laws of exponents",
                            "Express numbers in standard form"
                        ]
                    }
                ]
            },
            {
                "unit_number": 13,
                "unit_name": "Direct and Inverse Proportions",
                "marks": 7,
                "chapters": [
                    {
                        "chapter_number": 13,
                        "chapter_name": "Direct and Inverse Proportions",
                        "topics": [
                            "Direct proportion",
                            "Inverse proportion",
                            "Applications of direct and inverse proportions"
                        ],
                        "learning_outcomes": [
                            "Identify direct and inverse proportions",
                            "Solve problems using proportions"
                        ]
                    }
                ]
            },
            {
                "unit_number": 14,
                "unit_name": "Factorisation",
                "marks": 5,
                "chapters": [
                    {
                        "chapter_number": 14,
                        "chapter_name": "Factorisation",
                        "topics": [
                            "Factors of natural numbers",
                            "Factors of algebraic expressions",
                            "Method of common factors",
                            "Factorisation by regrouping terms",
                            "Factorisation using identities",
                            "Division of algebraic expressions"
                        ],
                        "learning_outcomes": [
                            "Factorize algebraic expressions",
                            "Divide algebraic expressions"
                        ]
                    }
                ]
            },
            {
                "unit_number": 15,
                "unit_name": "Introduction to Graphs",
                "marks": 5,
                "chapters": [
                    {
                        "chapter_number": 15,
                        "chapter_name": "Introduction to Graphs",
                        "topics": [
                            "Linear graphs",
                            "Some applications of linear graphs",
                            "Reading and interpreting graphs",
                            "Coordinate geometry"
                        ],
                        "learning_outcomes": [
                            "Plot and read graphs",
                            "Interpret real-world data from graphs"
                        ]
                    }
                ]
            }
        ]
    }


def get_grade_8_science():
    """Grade 8 Science - Based on NCERT"""
    return {
        "board": "CBSE",
        "grade": "8",
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
                "unit_name": "Crop Production and Management",
                "marks": 5,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "Crop Production and Management",
                        "topics": [
                            "Agricultural practices",
                            "Preparation of soil",
                            "Sowing",
                            "Adding manure and fertilizers",
                            "Irrigation",
                            "Protection from weeds",
                            "Harvesting",
                            "Storage",
                            "Food from animals"
                        ],
                        "learning_outcomes": [
                            "Explain agricultural practices",
                            "Understand crop management"
                        ]
                    }
                ]
            },
            {
                "unit_number": 2,
                "unit_name": "Microorganisms",
                "marks": 5,
                "chapters": [
                    {
                        "chapter_number": 2,
                        "chapter_name": "Microorganisms: Friend and Foe",
                        "topics": [
                            "Microorganisms and their types",
                            "Where do microorganisms live?",
                            "Useful microorganisms",
                            "Harmful microorganisms",
                            "Food preservation",
                            "Nitrogen fixation",
                            "Nitrogen cycle"
                        ],
                        "learning_outcomes": [
                            "Classify microorganisms",
                            "Explain nitrogen cycle"
                        ]
                    }
                ]
            },
            {
                "unit_number": 3,
                "unit_name": "Synthetic Fibres and Plastics",
                "marks": 5,
                "chapters": [
                    {
                        "chapter_number": 3,
                        "chapter_name": "Synthetic Fibres and Plastics",
                        "topics": [
                            "Types of fibres",
                            "Synthetic fibres (rayon, nylon, polyester, acrylic)",
                            "Characteristics of synthetic fibres",
                            "Plastics",
                            "Plastics as materials of choice",
                            "Plastics and environment"
                        ],
                        "learning_outcomes": [
                            "Distinguish natural and synthetic fibres",
                            "Understand environmental impact of plastics"
                        ]
                    }
                ]
            },
            {
                "unit_number": 4,
                "unit_name": "Materials: Metals and Non-Metals",
                "marks": 6,
                "chapters": [
                    {
                        "chapter_number": 4,
                        "chapter_name": "Materials: Metals and Non-Metals",
                        "topics": [
                            "Physical properties of metals and non-metals",
                            "Chemical properties of metals",
                            "Chemical properties of non-metals",
                            "Uses of metals and non-metals",
                            "Displacement reactions",
                            "Reactions of metals with acids, water, oxygen"
                        ],
                        "learning_outcomes": [
                            "Compare metals and non-metals",
                            "Predict reactivity of metals"
                        ]
                    }
                ]
            },
            {
                "unit_number": 5,
                "unit_name": "Coal and Petroleum",
                "marks": 5,
                "chapters": [
                    {
                        "chapter_number": 5,
                        "chapter_name": "Coal and Petroleum",
                        "topics": [
                            "Coal - a fossil fuel",
                            "Story of coal formation",
                            "Petroleum - a fossil fuel",
                            "Natural gas",
                            "Products from petroleum",
                            "Conservation of fossil fuels"
                        ],
                        "learning_outcomes": [
                            "Explain formation of fossil fuels",
                            "Understand need for conservation"
                        ]
                    }
                ]
            },
            {
                "unit_number": 6,
                "unit_name": "Combustion and Flame",
                "marks": 5,
                "chapters": [
                    {
                        "chapter_number": 6,
                        "chapter_name": "Combustion and Flame",
                        "topics": [
                            "What is combustion?",
                            "How do we control fire?",
                            "Types of combustion",
                            "Flame",
                            "Structure of a flame",
                            "Fuel and its efficiency",
                            "Harmful effects of burning fuels"
                        ],
                        "learning_outcomes": [
                            "Explain types of combustion",
                            "Describe flame structure"
                        ]
                    }
                ]
            },
            {
                "unit_number": 7,
                "unit_name": "Conservation of Plants and Animals",
                "marks": 6,
                "chapters": [
                    {
                        "chapter_number": 7,
                        "chapter_name": "Conservation of Plants and Animals",
                        "topics": [
                            "Deforestation and its causes",
                            "Consequences of deforestation",
                            "Conservation of forest and wildlife",
                            "Biosphere reserve",
                            "Flora and fauna",
                            "Endemic species",
                            "Wildlife sanctuary",
                            "National park",
                            "Red Data Book",
                            "Migration",
                            "Recycling of paper",
                            "Reforestation"
                        ],
                        "learning_outcomes": [
                            "Understand conservation methods",
                            "Explain biodiversity importance"
                        ]
                    }
                ]
            },
            {
                "unit_number": 8,
                "unit_name": "Cell Structure and Functions",
                "marks": 6,
                "chapters": [
                    {
                        "chapter_number": 8,
                        "chapter_name": "Cell - Structure and Functions",
                        "topics": [
                            "Discovery of cell",
                            "The cell",
                            "Organisms show variety in cell number, shape and size",
                            "Cell structure and function",
                            "Parts of the cell",
                            "Comparison of plant and animal cells"
                        ],
                        "learning_outcomes": [
                            "Identify cell parts and functions",
                            "Compare plant and animal cells"
                        ]
                    }
                ]
            },
            {
                "unit_number": 9,
                "unit_name": "Reproduction in Animals",
                "marks": 6,
                "chapters": [
                    {
                        "chapter_number": 9,
                        "chapter_name": "Reproduction in Animals",
                        "topics": [
                            "Modes of reproduction",
                            "Sexual reproduction",
                            "Asexual reproduction",
                            "Fertilization (internal and external)",
                            "Development of embryo",
                            "Viviparous and oviparous animals",
                            "Young ones to adults - metamorphosis"
                        ],
                        "learning_outcomes": [
                            "Explain modes of reproduction",
                            "Understand embryo development"
                        ]
                    }
                ]
            },
            {
                "unit_number": 10,
                "unit_name": "Reaching the Age of Adolescence",
                "marks": 5,
                "chapters": [
                    {
                        "chapter_number": 10,
                        "chapter_name": "Reaching the Age of Adolescence",
                        "topics": [
                            "Adolescence and puberty",
                            "Changes at puberty",
                            "Secondary sexual characteristics",
                            "Role of hormones in initiating reproductive function",
                            "Reproductive health",
                            "How the sex of baby is determined"
                        ],
                        "learning_outcomes": [
                            "Understand adolescence changes",
                            "Explain role of hormones"
                        ]
                    }
                ]
            },
            {
                "unit_number": 11,
                "unit_name": "Force and Pressure",
                "marks": 6,
                "chapters": [
                    {
                        "chapter_number": 11,
                        "chapter_name": "Force and Pressure",
                        "topics": [
                            "Force - a push or a pull",
                            "Forces are due to interaction",
                            "Types of forces (contact, non-contact)",
                            "Pressure",
                            "Pressure exerted by liquids and gases",
                            "Atmospheric pressure"
                        ],
                        "learning_outcomes": [
                            "Distinguish types of forces",
                            "Calculate pressure"
                        ]
                    }
                ]
            },
            {
                "unit_number": 12,
                "unit_name": "Friction",
                "marks": 5,
                "chapters": [
                    {
                        "chapter_number": 12,
                        "chapter_name": "Friction",
                        "topics": [
                            "Force of friction",
                            "Factors affecting friction",
                            "Friction: a necessary evil",
                            "Increasing and reducing friction",
                            "Wheels reduce friction",
                            "Fluid friction"
                        ],
                        "learning_outcomes": [
                            "Explain factors affecting friction",
                            "Apply methods to reduce friction"
                        ]
                    }
                ]
            },
            {
                "unit_number": 13,
                "unit_name": "Sound",
                "marks": 6,
                "chapters": [
                    {
                        "chapter_number": 13,
                        "chapter_name": "Sound",
                        "topics": [
                            "Sound is produced by a vibrating body",
                            "Sound produced by humans",
                            "Sound needs a medium for propagation",
                            "Sound waves are longitudinal waves",
                            "Characteristics of sound (amplitude, frequency, time period)",
                            "Audible and inaudible sounds",
                            "Noise and music",
                            "Noise pollution"
                        ],
                        "learning_outcomes": [
                            "Explain sound propagation",
                            "Understand noise pollution"
                        ]
                    }
                ]
            },
            {
                "unit_number": 14,
                "unit_name": "Chemical Effects of Electric Current",
                "marks": 6,
                "chapters": [
                    {
                        "chapter_number": 14,
                        "chapter_name": "Chemical Effects of Electric Current",
                        "topics": [
                            "Do liquids conduct electricity?",
                            "Chemical effects of electric current",
                            "Electroplating"
                        ],
                        "learning_outcomes": [
                            "Test electrical conductivity of liquids",
                            "Explain electroplating process"
                        ]
                    }
                ]
            },
            {
                "unit_number": 15,
                "unit_name": "Some Natural Phenomena",
                "marks": 5,
                "chapters": [
                    {
                        "chapter_number": 15,
                        "chapter_name": "Some Natural Phenomena",
                        "topics": [
                            "Lightning",
                            "Charging by rubbing",
                            "Types of charges and their interaction",
                            "Transfer of charge",
                            "The story of lightning",
                            "Lightning safety",
                            "Earthquakes"
                        ],
                        "learning_outcomes": [
                            "Explain electric charges",
                            "Understand earthquake phenomenon"
                        ]
                    }
                ]
            },
            {
                "unit_number": 16,
                "unit_name": "Light",
                "marks": 6,
                "chapters": [
                    {
                        "chapter_number": 16,
                        "chapter_name": "Light",
                        "topics": [
                            "Laws of reflection",
                            "Regular and diffused reflection",
                            "Reflected light can be reflected again",
                            "Multiple images",
                            "Sunlight - white or coloured",
                            "What is inside our eyes?",
                            "Care of the eyes",
                            "Visually impaired persons can read and write",
                            "Braille system"
                        ],
                        "learning_outcomes": [
                            "Apply laws of reflection",
                            "Understand human eye structure"
                        ]
                    }
                ]
            },
            {
                "unit_number": 17,
                "unit_name": "Stars and the Solar System",
                "marks": 5,
                "chapters": [
                    {
                        "chapter_number": 17,
                        "chapter_name": "Stars and the Solar System",
                        "topics": [
                            "The moon",
                            "The stars",
                            "Constellations",
                            "The solar system",
                            "Planets",
                            "Some other members of the solar system (asteroids, comets, meteors, meteorites)"
                        ],
                        "learning_outcomes": [
                            "Identify celestial objects",
                            "Understand solar system structure"
                        ]
                    }
                ]
            },
            {
                "unit_number": 18,
                "unit_name": "Pollution of Air and Water",
                "marks": 6,
                "chapters": [
                    {
                        "chapter_number": 18,
                        "chapter_name": "Pollution of Air and Water",
                        "topics": [
                            "Air pollution",
                            "How does air get polluted?",
                            "Case study: The Taj Mahal",
                            "Greenhouse effect",
                            "What can be done?",
                            "Water pollution",
                            "How does water get polluted?",
                            "What is potable water and how is water purified?",
                            "What can be done?"
                        ],
                        "learning_outcomes": [
                            "Identify sources of pollution",
                            "Suggest pollution control measures"
                        ]
                    }
                ]
            }
        ]
    }


def get_grade_8_social_science():
    """Grade 8 Social Science - Based on NCERT"""
    return {
        "board": "CBSE",
        "grade": "8",
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
                "unit_name": "Our Pasts - III (History)",
                "marks": 20,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "How, When and Where",
                        "topics": [
                            "How Important are Dates?",
                            "How Do We Periodise?",
                            "What is Colonial?",
                            "How Do We Know?"
                        ],
                        "learning_outcomes": [
                            "Understand historical periodization",
                            "Analyze colonial impact"
                        ]
                    },
                    {
                        "chapter_number": 2,
                        "chapter_name": "From Trade to Territory",
                        "topics": [
                            "East India Company comes East",
                            "East India Company begins trade in Bengal",
                            "The Battle of Plassey",
                            "Company rule expands",
                            "Setting up a new administration"
                        ],
                        "learning_outcomes": [
                            "Explain British expansion in India",
                            "Understand colonial administration"
                        ]
                    },
                    {
                        "chapter_number": 3,
                        "chapter_name": "Ruling the Countryside",
                        "topics": [
                            "Revenue for the Company",
                            "The problem of unpaid revenue",
                            "A new system is devised",
                            "Crops for Europe",
                            "Does color matter?"
                        ],
                        "learning_outcomes": [
                            "Analyze land revenue systems",
                            "Understand peasant conditions"
                        ]
                    },
                    {
                        "chapter_number": 4,
                        "chapter_name": "Tribals, Dikus and the Vision of a Golden Age",
                        "topics": [
                            "How did tribal groups live?",
                            "How did colonial rule affect tribal lives?",
                            "Birsa Munda and the movement",
                            "Tribal movements"
                        ],
                        "learning_outcomes": [
                            "Understand tribal lifestyles",
                            "Analyze impact of colonialism on tribals"
                        ]
                    },
                    {
                        "chapter_number": 5,
                        "chapter_name": "When People Rebel (1857 and After)",
                        "topics": [
                            "Policies and people",
                            "The revolt begins",
                            "How did the British see it?",
                            "What happened to the Mughal emperor?",
                            "Aftermath"
                        ],
                        "learning_outcomes": [
                            "Explain causes of 1857 revolt",
                            "Analyze consequences of the revolt"
                        ]
                    },
                    {
                        "chapter_number": 6,
                        "chapter_name": "Weavers, Iron Smelters and Factory Owners",
                        "topics": [
                            "Indian textiles and the world market",
                            "What happened to weavers?",
                            "Manchester comes to India",
                            "Iron smelters",
                            "The story of factories"
                        ],
                        "learning_outcomes": [
                            "Understand deindustrialization",
                            "Analyze growth of modern industry"
                        ]
                    },
                    {
                        "chapter_number": 7,
                        "chapter_name": "Civilising the Native, Educating the Nation",
                        "topics": [
                            "The British and education",
                            "Education for commerce",
                            "Debates over education",
                            "The rise of vernacular education",
                            "Women and education"
                        ],
                        "learning_outcomes": [
                            "Analyze colonial education policy",
                            "Understand educational reforms"
                        ]
                    },
                    {
                        "chapter_number": 8,
                        "chapter_name": "Women, Caste and Reform",
                        "topics": [
                            "Working towards change - status of women",
                            "Caste and social reform",
                            "Demands for equality and justice"
                        ],
                        "learning_outcomes": [
                            "Explain social reform movements",
                            "Understand women's rights movements"
                        ]
                    },
                    {
                        "chapter_number": 9,
                        "chapter_name": "The Making of the National Movement: 1870s-1947",
                        "topics": [
                            "Emergence of nationalism",
                            "The Congress and its leaders",
                            "The changing nature of the movement",
                            "Independence with partition"
                        ],
                        "learning_outcomes": [
                            "Trace growth of national movement",
                            "Understand partition of India"
                        ]
                    },
                    {
                        "chapter_number": 10,
                        "chapter_name": "India After Independence",
                        "topics": [
                            "A new and divided nation",
                            "The challenge of democracy",
                            "States reorganization",
                            "Planning for development"
                        ],
                        "learning_outcomes": [
                            "Understand post-independence challenges",
                            "Analyze nation-building process"
                        ]
                    }
                ]
            },
            {
                "unit_number": 2,
                "unit_name": "Resources and Development (Geography)",
                "marks": 20,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "Resources",
                        "topics": [
                            "Types of resources (natural, human-made, human)",
                            "Resource development",
                            "Resource planning",
                            "Conservation of resources",
                            "Sustainable development"
                        ],
                        "learning_outcomes": [
                            "Classify resources",
                            "Understand resource conservation"
                        ]
                    },
                    {
                        "chapter_number": 2,
                        "chapter_name": "Land, Soil, Water, Natural Vegetation and Wildlife Resources",
                        "topics": [
                            "Land as a resource",
                            "Land use pattern in India",
                            "Soil as a resource",
                            "Soil types and distribution",
                            "Soil degradation and conservation",
                            "Water resources",
                            "Water scarcity and conservation",
                            "Natural vegetation and wildlife"
                        ],
                        "learning_outcomes": [
                            "Explain land use patterns",
                            "Understand soil and water conservation"
                        ]
                    },
                    {
                        "chapter_number": 3,
                        "chapter_name": "Mineral and Power Resources",
                        "topics": [
                            "Types of minerals",
                            "Distribution of minerals",
                            "Ferrous and non-ferrous minerals",
                            "Energy resources (conventional and non-conventional)"
                        ],
                        "learning_outcomes": [
                            "Classify minerals",
                            "Compare energy resources"
                        ]
                    },
                    {
                        "chapter_number": 4,
                        "chapter_name": "Agriculture",
                        "topics": [
                            "Types of farming",
                            "Cropping seasons (Kharif, Rabi, Zaid)",
                            "Major crops (food and cash crops)",
                            "Agricultural development"
                        ],
                        "learning_outcomes": [
                            "Identify cropping patterns",
                            "Understand agricultural practices"
                        ]
                    },
                    {
                        "chapter_number": 5,
                        "chapter_name": "Industries",
                        "topics": [
                            "Classification of industries",
                            "Major industries in India (textile, iron and steel, cotton textile)",
                            "Industrial regions",
                            "Industrial pollution and environmental degradation"
                        ],
                        "learning_outcomes": [
                            "Classify industries",
                            "Analyze industrial distribution"
                        ]
                    },
                    {
                        "chapter_number": 6,
                        "chapter_name": "Human Resources",
                        "topics": [
                            "Distribution of population",
                            "Population density and distribution",
                            "Population change and migration",
                            "Age composition and sex ratio",
                            "Literacy",
                            "Health",
                            "Population policy"
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
                "unit_name": "Social and Political Life - III (Civics)",
                "marks": 20,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "The Indian Constitution",
                        "topics": [
                            "Why do we need a Constitution?",
                            "The making of the Constitution",
                            "Guiding principles of the Constitution",
                            "Fundamental Rights and Duties"
                        ],
                        "learning_outcomes": [
                            "Understand constitution-making",
                            "Explain fundamental rights"
                        ]
                    },
                    {
                        "chapter_number": 2,
                        "chapter_name": "Understanding Secularism",
                        "topics": [
                            "What is secularism?",
                            "Indian secularism",
                            "Why is secularism important?"
                        ],
                        "learning_outcomes": [
                            "Define secularism",
                            "Understand Indian secularism"
                        ]
                    },
                    {
                        "chapter_number": 3,
                        "chapter_name": "Why Do We Need a Parliament?",
                        "topics": [
                            "Why do we need two Houses of Parliament?",
                            "Why should people decide?",
                            "The role of Parliament"
                        ],
                        "learning_outcomes": [
                            "Explain parliamentary functions",
                            "Understand legislative process"
                        ]
                    },
                    {
                        "chapter_number": 4,
                        "chapter_name": "Understanding Laws",
                        "topics": [
                            "What is a law?",
                            "Role of judiciary in law-making",
                            "Unpopular and controversial laws",
                            "New laws for changing times"
                        ],
                        "learning_outcomes": [
                            "Understand law-making process",
                            "Explain role of judiciary"
                        ]
                    },
                    {
                        "chapter_number": 5,
                        "chapter_name": "Judiciary",
                        "topics": [
                            "What is the role of the judiciary?",
                            "What is an independent judiciary?",
                            "Structure of the courts in India",
                            "Different levels of courts"
                        ],
                        "learning_outcomes": [
                            "Explain judicial structure",
                            "Understand judicial independence"
                        ]
                    },
                    {
                        "chapter_number": 6,
                        "chapter_name": "Understanding Our Criminal Justice System",
                        "topics": [
                            "What is the criminal justice system?",
                            "Role of the police",
                            "Role of courts",
                            "Fair trial"
                        ],
                        "learning_outcomes": [
                            "Understand criminal justice system",
                            "Explain fair trial concept"
                        ]
                    },
                    {
                        "chapter_number": 7,
                        "chapter_name": "Understanding Marginalisation",
                        "topics": [
                            "Who are the marginalised?",
                            "Marginalisation and justice",
                            "Adivasis and marginalisation",
                            "Minorities and marginalisation"
                        ],
                        "learning_outcomes": [
                            "Identify marginalized groups",
                            "Understand social justice"
                        ]
                    },
                    {
                        "chapter_number": 8,
                        "chapter_name": "Confronting Marginalisation",
                        "topics": [
                            "Invoking fundamental rights",
                            "Laws for the marginalised",
                            "Protecting the rights of dalits and adivasis",
                            "Adivasi demands and the 1989 Act"
                        ],
                        "learning_outcomes": [
                            "Explain protective legislation",
                            "Understand rights of marginalised"
                        ]
                    },
                    {
                        "chapter_number": 9,
                        "chapter_name": "Public Facilities",
                        "topics": [
                            "What are public facilities?",
                            "Water as a public facility",
                            "Public facilities in India",
                            "Government's role"
                        ],
                        "learning_outcomes": [
                            "Identify public facilities",
                            "Understand government responsibilities"
                        ]
                    },
                    {
                        "chapter_number": 10,
                        "chapter_name": "Law and Social Justice",
                        "topics": [
                            "What is a worker's worth?",
                            "Enforcement of safety laws",
                            "Need for enforcement",
                            "Role of government"
                        ],
                        "learning_outcomes": [
                            "Explain labor laws",
                            "Understand social justice"
                        ]
                    }
                ]
            },
            {
                "unit_number": 4,
                "unit_name": "Economic Presence (Economics)",
                "marks": 20,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "The Story of Village Palampur",
                        "topics": [
                            "Farming in Palampur",
                            "Non-farm activities",
                            "Organisation of production"
                        ],
                        "learning_outcomes": [
                            "Understand rural economy",
                            "Analyze production factors"
                        ]
                    },
                    {
                        "chapter_number": 2,
                        "chapter_name": "People as Resource",
                        "topics": [
                            "Human capital formation",
                            "Education and health",
                            "Employment and unemployment"
                        ],
                        "learning_outcomes": [
                            "Explain human capital",
                            "Understand employment types"
                        ]
                    },
                    {
                        "chapter_number": 3,
                        "chapter_name": "Poverty as a Challenge",
                        "topics": [
                            "Understanding poverty",
                            "Poverty estimates",
                            "Anti-poverty measures",
                            "Challenges ahead"
                        ],
                        "learning_outcomes": [
                            "Analyze poverty indicators",
                            "Evaluate poverty alleviation programs"
                        ]
                    },
                    {
                        "chapter_number": 4,
                        "chapter_name": "Food Security in India",
                        "topics": [
                            "What is food security?",
                            "Buffer stock",
                            "Public Distribution System",
                            "Food security in India"
                        ],
                        "learning_outcomes": [
                            "Explain food security",
                            "Understand PDS mechanism"
                        ]
                    }
                ]
            }
        ]
    }


def get_grade_8_english():
    """Grade 8 English - Based on NCERT"""
    return {
        "board": "CBSE",
        "grade": "8",
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
                            "Literary passages"
                        ],
                        "learning_outcomes": [
                            "Extract main ideas",
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
                            "Messages",
                            "Notices",
                            "Paragraph writing",
                            "Story completion"
                        ],
                        "learning_outcomes": [
                            "Write formal messages and notices",
                            "Create coherent paragraphs",
                            "Develop narratives"
                        ]
                    },
                    {
                        "chapter_number": 2,
                        "chapter_name": "Grammar",
                        "topics": [
                            "Tenses",
                            "Modals",
                            "Active and Passive Voice",
                            "Reported Speech",
                            "Prepositions",
                            "Conjunctions"
                        ],
                        "learning_outcomes": [
                            "Apply grammar rules",
                            "Transform voice and speech",
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
                        "chapter_name": "Honeydew (Main Reader)",
                        "topics": [
                            "The Best Christmas Present in the World",
                            "The Tsunami",
                            "Glimpses of the Past",
                            "Bepin Choudhury's Lapse of Memory",
                            "The Summit Within",
                            "This is Jody's Fawn",
                            "A Visit to Cambridge",
                            "A Short Monsoon Diary",
                            "The Great Stone Face - I",
                            "The Great Stone Face - II"
                        ],
                        "subtopics": [
                            {
                                "topic": "Poetry",
                                "subtopics": [
                                    "The Ant and the Cricket",
                                    "Geography Lesson",
                                    "The Last Bargain",
                                    "The School Boy",
                                    "The Last Bargain",
                                    "On the Grasshopper and Cricket",
                                    "Chivvy"
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
                        "chapter_name": "It So Happened (Supplementary)",
                        "topics": [
                            "How the Camel Got His Hump",
                            "Children at Work",
                            "The Selfish Giant",
                            "The Treasure Within",
                            "Princess September",
                            "The Fight",
                            "The Open Window",
                            "Jalebis",
                            "The Comet - I",
                            "The Comet - II"
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


def get_grade_8_hindi():
    """Grade 8 Hindi Course A - Based on NCERT"""
    return {
        "board": "CBSE",
        "grade": "8",
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
                            "वाच्य",
                            "क्रिया विशेषण",
                            "समास",
                            "मुहावरे",
                            "संधि",
                            "उपसर्ग-प्रत्यय"
                        ],
                        "learning_outcomes": [
                            "व्याकरण के नियम लागू करना",
                            "सही वाक्य रचना"
                        ]
                    }
                ]
            },
            {
                "unit_number": 3,
                "unit_name": "पाठ्यपुस्तक वसंत भाग-3 (Textbook Vasant Part-3)",
                "marks": 24,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "गद्य खंड (Prose)",
                        "topics": [
                            "ध्वनि (सूर्यकांत त्रिपाठी 'निराला')",
                            "लाख की चूड़ियाँ (कामतानाथ)",
                            "बस की यात्रा (हरिशंकर परसाई)",
                            "दीवानों की हस्ती (भगवतीचरण वर्मा)",
                            "चिट्ठियों की अनूठी दुनिया (अज्ञात)",
                            "भगवान के डाकिए (रामधारी सिंह 'दिनकर')",
                            "क्या निराश हुआ जाए (हजारी प्रसाद द्विवेदी)",
                            "यह सबसे कठिन समय नहीं (जया जादवानी)"
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
                            "ध्वनि",
                            "लाख की चूड़ियाँ",
                            "बस की यात्रा",
                            "दीवानों की हस्ती",
                            "चिट्ठियों की अनूठी दुनिया"
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
                "unit_name": "पूरक पाठ्यपुस्तक भारत की खोज (Supplementary Bharat ki Khoj)",
                "marks": 10,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "भारत की खोज",
                        "topics": [
                            "अहमदनगर का किला",
                            "तलाश",
                            "सिंधु घाटी सभ्यता",
                            "युगों का दौर",
                            "नयी समस्याएँ",
                            "अंतिम दौर - एक",
                            "अंतिम दौर - दो",
                            "तनाव",
                            "दो पृष्ठभूमियाँ - भारतीय और अंग्रेज़ी"
                        ],
                        "learning_outcomes": [
                            "भारतीय इतिहास को समझना",
                            "सांस्कृतिक विरासत की पहचान"
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
                            "सूचना लेखन",
                            "विज्ञापन लेखन"
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


def generate_all_grade_8_json():
    """Generate JSON files for all Grade 8 subjects"""

    # Get all subject data
    subjects = {
        "mathematics": get_grade_8_mathematics(),
        "science": get_grade_8_science(),
        "social_science": get_grade_8_social_science(),
        "english": get_grade_8_english(),
        "hindi": get_grade_8_hindi()
    }

    # Create output directory
    output_dir = Path("scripts/cbse_extractor/data/structured_json")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate JSON files
    for subject_name, subject_data in subjects.items():
        filename = f"cbse_grade_8_{subject_name}.json"
        filepath = output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(subject_data, f, ensure_ascii=False, indent=2)

        print(f"✅ Generated: {filename}")
        print(f"   Size: {filepath.stat().st_size} bytes")

    print(f"\n✅ All Grade 8 JSON files generated in {output_dir}")


if __name__ == "__main__":
    generate_all_grade_8_json()
