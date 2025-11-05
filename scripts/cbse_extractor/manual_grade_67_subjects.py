#!/usr/bin/env python3
"""
Manual Grade 6 & 7 CBSE Syllabus Data
Structured data for Grades 6-7 based on NCERT textbooks 2024-25
"""

import json
from pathlib import Path


def get_grade_7_mathematics():
    return {
        "board": "CBSE", "grade": "7", "subject": "Mathematics", "subject_code": "041",
        "academic_year": "2024-25", "total_marks": 80, "theory_marks": 80,
        "practical_marks": 0, "internal_assessment": 20,
        "units": [
            {"unit_number": 1, "unit_name": "Integers", "marks": 6, "chapters": [
                {"chapter_number": 1, "chapter_name": "Integers",
                 "topics": ["Properties of integers", "Multiplication and division", "Closure property"],
                 "learning_outcomes": ["Perform operations on integers"]}
            ]},
            {"unit_number": 2, "unit_name": "Fractions and Decimals", "marks": 7, "chapters": [
                {"chapter_number": 2, "chapter_name": "Fractions and Decimals",
                 "topics": ["Operations on fractions", "Multiplication of fractions", "Division of fractions", "Decimals"],
                 "learning_outcomes": ["Solve problems using fractions and decimals"]}
            ]},
            {"unit_number": 3, "unit_name": "Data Handling", "marks": 7, "chapters": [
                {"chapter_number": 3, "chapter_name": "Data Handling",
                 "topics": ["Mean, median, mode", "Bar graphs", "Probability"],
                 "learning_outcomes": ["Organize and interpret data"]}
            ]},
            {"unit_number": 4, "unit_name": "Simple Equations", "marks": 7, "chapters": [
                {"chapter_number": 4, "chapter_name": "Simple Equations",
                 "topics": ["Setting up equations", "Solving equations", "Applications"],
                 "learning_outcomes": ["Solve linear equations"]}
            ]},
            {"unit_number": 5, "unit_name": "Lines and Angles", "marks": 6, "chapters": [
                {"chapter_number": 5, "chapter_name": "Lines and Angles",
                 "topics": ["Related angles", "Pairs of lines", "Transversal"],
                 "learning_outcomes": ["Identify angle relationships"]}
            ]},
            {"unit_number": 6, "unit_name": "The Triangle and its Properties", "marks": 6, "chapters": [
                {"chapter_number": 6, "chapter_name": "The Triangle and its Properties",
                 "topics": ["Medians", "Altitudes", "Exterior angles", "Pythagoras theorem"],
                 "learning_outcomes": ["Apply triangle properties"]}
            ]},
            {"unit_number": 7, "unit_name": "Congruence of Triangles", "marks": 7, "chapters": [
                {"chapter_number": 7, "chapter_name": "Congruence of Triangles",
                 "topics": ["Congruence criteria (SSS, SAS, ASA, RHS)"],
                 "learning_outcomes": ["Prove triangle congruence"]}
            ]},
            {"unit_number": 8, "unit_name": "Comparing Quantities", "marks": 8, "chapters": [
                {"chapter_number": 8, "chapter_name": "Comparing Quantities",
                 "topics": ["Ratios", "Percentages", "Profit and loss", "Simple interest"],
                 "learning_outcomes": ["Solve percentage problems"]}
            ]},
            {"unit_number": 9, "unit_name": "Rational Numbers", "marks": 6, "chapters": [
                {"chapter_number": 9, "chapter_name": "Rational Numbers",
                 "topics": ["Need for rational numbers", "Positive and negative rational numbers", "Operations"],
                 "learning_outcomes": ["Perform operations on rational numbers"]}
            ]},
            {"unit_number": 10, "unit_name": "Practical Geometry", "marks": 5, "chapters": [
                {"chapter_number": 10, "chapter_name": "Practical Geometry",
                 "topics": ["Construction of triangles"],
                 "learning_outcomes": ["Construct triangles"]}
            ]},
            {"unit_number": 11, "unit_name": "Perimeter and Area", "marks": 10, "chapters": [
                {"chapter_number": 11, "chapter_name": "Perimeter and Area",
                 "topics": ["Squares and rectangles", "Triangles", "Parallelograms", "Circles"],
                 "learning_outcomes": ["Calculate areas and perimeters"]}
            ]},
            {"unit_number": 12, "unit_name": "Algebraic Expressions", "marks": 8, "chapters": [
                {"chapter_number": 12, "chapter_name": "Algebraic Expressions",
                 "topics": ["Expressions", "Terms", "Addition and subtraction", "Using algebraic expressions"],
                 "learning_outcomes": ["Simplify algebraic expressions"]}
            ]},
            {"unit_number": 13, "unit_name": "Exponents and Powers", "marks": 5, "chapters": [
                {"chapter_number": 13, "chapter_name": "Exponents and Powers",
                 "topics": ["Exponents", "Laws of exponents", "Miscellaneous examples using the laws"],
                 "learning_outcomes": ["Apply laws of exponents"]}
            ]},
            {"unit_number": 14, "unit_name": "Symmetry", "marks": 5, "chapters": [
                {"chapter_number": 14, "chapter_name": "Symmetry",
                 "topics": ["Lines of symmetry", "Rotational symmetry"],
                 "learning_outcomes": ["Identify symmetry in figures"]}
            ]},
            {"unit_number": 15, "unit_name": "Visualising Solid Shapes", "marks": 3, "chapters": [
                {"chapter_number": 15, "chapter_name": "Visualising Solid Shapes",
                 "topics": ["Plane figures and solid shapes", "Faces, edges, vertices"],
                 "learning_outcomes": ["Visualize 3D shapes"]}
            ]}
        ]
    }


def get_grade_7_science():
    return {
        "board": "CBSE", "grade": "7", "subject": "Science", "subject_code": "086",
        "academic_year": "2024-25", "total_marks": 80, "theory_marks": 80,
        "practical_marks": 0, "internal_assessment": 20,
        "units": [
            {"unit_number": 1, "unit_name": "Nutrition in Plants", "marks": 5, "chapters": [
                {"chapter_number": 1, "chapter_name": "Nutrition in Plants",
                 "topics": ["Modes of nutrition", "Photosynthesis", "Nutrients"],
                 "learning_outcomes": ["Explain photosynthesis"]}
            ]},
            {"unit_number": 2, "unit_name": "Nutrition in Animals", "marks": 5, "chapters": [
                {"chapter_number": 2, "chapter_name": "Nutrition in Animals",
                 "topics": ["Different ways of taking food", "Digestion in humans"],
                 "learning_outcomes": ["Describe digestive system"]}
            ]},
            {"unit_number": 3, "unit_name": "Heat", "marks": 6, "chapters": [
                {"chapter_number": 3, "chapter_name": "Heat",
                 "topics": ["Hot and cold", "Temperature", "Transfer of heat"],
                 "learning_outcomes": ["Distinguish heat and temperature"]}
            ]},
            {"unit_number": 4, "unit_name": "Acids, Bases and Salts", "marks": 6, "chapters": [
                {"chapter_number": 4, "chapter_name": "Acids, Bases and Salts",
                 "topics": ["Acids", "Bases", "Neutralisation", "Indicators"],
                 "learning_outcomes": ["Test using indicators"]}
            ]},
            {"unit_number": 5, "unit_name": "Physical and Chemical Changes", "marks": 5, "chapters": [
                {"chapter_number": 5, "chapter_name": "Physical and Chemical Changes",
                 "topics": ["Physical changes", "Chemical changes", "Rusting", "Crystallisation"],
                 "learning_outcomes": ["Distinguish types of changes"]}
            ]},
            {"unit_number": 6, "unit_name": "Weather, Climate and Adaptations", "marks": 5, "chapters": [
                {"chapter_number": 6, "chapter_name": "Weather, Climate and Adaptations of Animals to Climate",
                 "topics": ["Weather", "Climate", "Climate and adaptation"],
                 "learning_outcomes": ["Explain adaptations"]}
            ]},
            {"unit_number": 7, "unit_name": "Winds, Storms and Cyclones", "marks": 5, "chapters": [
                {"chapter_number": 7, "chapter_name": "Winds, Storms and Cyclones",
                 "topics": ["Air pressure", "Wind currents", "Cyclones"],
                 "learning_outcomes": ["Understand cyclone formation"]}
            ]},
            {"unit_number": 8, "unit_name": "Soil", "marks": 5, "chapters": [
                {"chapter_number": 8, "chapter_name": "Soil",
                 "topics": ["Soil teeming with life", "Soil profile", "Soil types"],
                 "learning_outcomes": ["Classify soil types"]}
            ]},
            {"unit_number": 9, "unit_name": "Respiration in Organisms", "marks": 5, "chapters": [
                {"chapter_number": 9, "chapter_name": "Respiration in Organisms",
                 "topics": ["Breathing", "Respiration", "Types of respiration"],
                 "learning_outcomes": ["Explain respiration process"]}
            ]},
            {"unit_number": 10, "unit_name": "Transportation in Animals and Plants", "marks": 5, "chapters": [
                {"chapter_number": 10, "chapter_name": "Transportation in Animals and Plants",
                 "topics": ["Circulatory system", "Excretion", "Transport in plants"],
                 "learning_outcomes": ["Describe transport systems"]}
            ]},
            {"unit_number": 11, "unit_name": "Reproduction in Plants", "marks": 6, "chapters": [
                {"chapter_number": 11, "chapter_name": "Reproduction in Plants",
                 "topics": ["Modes of reproduction", "Sexual reproduction", "Seed formation and dispersal"],
                 "learning_outcomes": ["Explain plant reproduction"]}
            ]},
            {"unit_number": 12, "unit_name": "Motion and Time", "marks": 6, "chapters": [
                {"chapter_number": 12, "chapter_name": "Motion and Time",
                 "topics": ["Slow or fast", "Speed", "Distance-time graphs"],
                 "learning_outcomes": ["Calculate speed"]}
            ]},
            {"unit_number": 13, "unit_name": "Electric Current and its Effects", "marks": 6, "chapters": [
                {"chapter_number": 13, "chapter_name": "Electric Current and its Effects",
                 "topics": ["Symbols for components", "Heating effect", "Magnetic effect"],
                 "learning_outcomes": ["Explain effects of current"]}
            ]},
            {"unit_number": 14, "unit_name": "Light", "marks": 6, "chapters": [
                {"chapter_number": 14, "chapter_name": "Light",
                 "topics": ["Light travels in straight lines", "Reflection", "Spherical mirrors"],
                 "learning_outcomes": ["Apply laws of reflection"]}
            ]},
            {"unit_number": 15, "unit_name": "Water: A Precious Resource", "marks": 5, "chapters": [
                {"chapter_number": 15, "chapter_name": "Water: A Precious Resource",
                 "topics": ["How much water is available?", "Water management", "Conservation"],
                 "learning_outcomes": ["Understand water conservation"]}
            ]},
            {"unit_number": 16, "unit_name": "Forests: Our Lifeline", "marks": 5, "chapters": [
                {"chapter_number": 16, "chapter_name": "Forests: Our Lifeline",
                 "topics": ["Forest ecosystem", "Forest products", "Conservation"],
                 "learning_outcomes": ["Explain forest importance"]}
            ]},
            {"unit_number": 17, "unit_name": "Wastewater Story", "marks": 5, "chapters": [
                {"chapter_number": 17, "chapter_name": "Wastewater Story",
                 "topics": ["Water pollution", "Wastewater treatment", "Sewage treatment"],
                 "learning_outcomes": ["Understand wastewater management"]}
            ]}
        ]
    }


def get_grade_7_social_science():
    return {
        "board": "CBSE", "grade": "7", "subject": "Social Science", "subject_code": "087",
        "academic_year": "2024-25", "total_marks": 80, "theory_marks": 80,
        "practical_marks": 0, "internal_assessment": 20,
        "units": [
            {"unit_number": 1, "unit_name": "History - Our Pasts - II", "marks": 20, "chapters": [
                {"chapter_number": 1, "chapter_name": "Tracing Changes Through a Thousand Years",
                 "topics": ["New and old terminologies", "Historical sources", "New social and political groups"],
                 "learning_outcomes": ["Understand medieval period"]},
                {"chapter_number": 2, "chapter_name": "New Kings and Kingdoms",
                 "topics": ["Emergence of new dynasties", "Administration", "Chola empire"],
                 "learning_outcomes": ["Analyze medieval kingdoms"]},
                {"chapter_number": 3, "chapter_name": "The Delhi Sultans",
                 "topics": ["Establishment of Delhi Sultanate", "Administration", "Architecture"],
                 "learning_outcomes": ["Explain Sultanate rule"]},
                {"chapter_number": 4, "chapter_name": "The Mughal Empire",
                 "topics": ["Establishment and expansion", "Mughal administration", "Relations with other rulers"],
                 "learning_outcomes": ["Understand Mughal rule"]},
                {"chapter_number": 5, "chapter_name": "Rulers and Buildings",
                 "topics": ["Temples", "Mosques", "Forts", "Tombs"],
                 "learning_outcomes": ["Appreciate medieval architecture"]},
                {"chapter_number": 6, "chapter_name": "Towns, Traders and Craftspersons",
                 "topics": ["Medieval towns", "Trade", "Crafts"],
                 "learning_outcomes": ["Understand medieval economy"]},
                {"chapter_number": 7, "chapter_name": "Tribes, Nomads and Settled Communities",
                 "topics": ["Pastoral communities", "Tribal societies", "Gonds and Ahoms"],
                 "learning_outcomes": ["Analyze tribal societies"]},
                {"chapter_number": 8, "chapter_name": "Devotional Paths to the Divine",
                 "topics": ["Bhakti and Sufi movements", "Saints and their teachings"],
                 "learning_outcomes": ["Understand religious movements"]},
                {"chapter_number": 9, "chapter_name": "The Making of Regional Cultures",
                 "topics": ["Regional languages", "Kathak", "Miniature paintings"],
                 "learning_outcomes": ["Appreciate regional diversity"]},
                {"chapter_number": 10, "chapter_name": "Eighteenth-Century Political Formations",
                 "topics": ["Emergence of new states", "Decline of Mughal empire", "Regional powers"],
                 "learning_outcomes": ["Analyze 18th century politics"]}
            ]},
            {"unit_number": 2, "unit_name": "Geography - Our Environment", "marks": 20, "chapters": [
                {"chapter_number": 1, "chapter_name": "Environment",
                 "topics": ["Natural environment", "Human environment", "Interaction"],
                 "learning_outcomes": ["Understand environment components"]},
                {"chapter_number": 2, "chapter_name": "Inside Our Earth",
                 "topics": ["Earth's interior", "Rocks", "Minerals"],
                 "learning_outcomes": ["Explain earth structure"]},
                {"chapter_number": 3, "chapter_name": "Our Changing Earth",
                 "topics": ["Lithospheric plates", "Earthquakes", "Volcanoes"],
                 "learning_outcomes": ["Understand earth processes"]},
                {"chapter_number": 4, "chapter_name": "Air",
                 "topics": ["Atmosphere composition", "Air pressure", "Winds"],
                 "learning_outcomes": ["Explain atmospheric phenomena"]},
                {"chapter_number": 5, "chapter_name": "Water",
                 "topics": ["Hydrological cycle", "Distribution", "Ocean currents"],
                 "learning_outcomes": ["Understand water cycle"]},
                {"chapter_number": 6, "chapter_name": "Natural Vegetation and Wildlife",
                 "topics": ["Types of vegetation", "Wildlife", "Conservation"],
                 "learning_outcomes": ["Classify vegetation types"]},
                {"chapter_number": 7, "chapter_name": "Human Environment - Settlement, Transport and Communication",
                 "topics": ["Settlements", "Transport", "Communication"],
                 "learning_outcomes": ["Analyze human settlements"]},
                {"chapter_number": 8, "chapter_name": "Human Environment Interactions - The Tropical and the Subtropical Region",
                 "topics": ["Amazon basin", "Ganga-Brahmaputra basin"],
                 "learning_outcomes": ["Compare regional environments"]},
                {"chapter_number": 9, "chapter_name": "Life in the Temperate Grasslands",
                 "topics": ["Prairies", "Velds", "Life and activities"],
                 "learning_outcomes": ["Understand grassland life"]},
                {"chapter_number": 10, "chapter_name": "Life in the Deserts",
                 "topics": ["Sahara", "Ladakh", "Adaptations"],
                 "learning_outcomes": ["Explain desert adaptations"]}
            ]},
            {"unit_number": 3, "unit_name": "Civics - Social and Political Life - II", "marks": 20, "chapters": [
                {"chapter_number": 1, "chapter_name": "On Equality",
                 "topics": ["Equality in democracy", "Issues of equality"],
                 "learning_outcomes": ["Understand equality concept"]},
                {"chapter_number": 2, "chapter_name": "Role of the Government in Health",
                 "topics": ["Healthcare in India", "Public and private health facilities"],
                 "learning_outcomes": ["Analyze healthcare system"]},
                {"chapter_number": 3, "chapter_name": "How the State Government Works",
                 "topics": ["Legislative Assembly", "Chief Minister", "Governor"],
                 "learning_outcomes": ["Explain state governance"]},
                {"chapter_number": 4, "chapter_name": "Growing up as Boys and Girls",
                 "topics": ["Gender roles", "Discrimination", "Inequality"],
                 "learning_outcomes": ["Identify gender issues"]},
                {"chapter_number": 5, "chapter_name": "Women Change the World",
                 "topics": ["Women's movements", "Achievements", "Challenges"],
                 "learning_outcomes": ["Appreciate women's contribution"]},
                {"chapter_number": 6, "chapter_name": "Understanding Media",
                 "topics": ["Mass media", "Technology", "Media influence"],
                 "learning_outcomes": ["Analyze media role"]},
                {"chapter_number": 7, "chapter_name": "Understanding Advertising",
                 "topics": ["Purpose of advertisements", "Brand building", "Media and technology"],
                 "learning_outcomes": ["Critically evaluate advertisements"]},
                {"chapter_number": 8, "chapter_name": "Markets Around Us",
                 "topics": ["Weekly markets", "Shopping complexes", "Chain of markets"],
                 "learning_outcomes": ["Understand market types"]},
                {"chapter_number": 9, "chapter_name": "A Shirt in the Market",
                 "topics": ["Cotton farming", "Weavers", "Merchants"],
                 "learning_outcomes": ["Trace product journey"]},
                {"chapter_number": 10, "chapter_name": "Struggles for Equality",
                 "topics": ["Tawa Matsya Sangh", "Struggle for rights"],
                 "learning_outcomes": ["Appreciate people's movements"]}
            ]},
            {"unit_number": 4, "unit_name": "Economics", "marks": 20, "chapters": [
                {"chapter_number": 1, "chapter_name": "Understanding Economy",
                 "topics": ["Economic activities", "Sectors", "Employment"],
                 "learning_outcomes": ["Understand basic economics"]}
            ]}
        ]
    }


def get_grade_7_english():
    return {
        "board": "CBSE", "grade": "7", "subject": "English", "subject_code": "184",
        "academic_year": "2024-25", "total_marks": 80, "theory_marks": 80,
        "practical_marks": 0, "internal_assessment": 20,
        "units": [
            {"unit_number": 1, "unit_name": "Reading Skills", "marks": 20, "chapters": [
                {"chapter_number": 1, "chapter_name": "Reading Comprehension",
                 "topics": ["Factual passages", "Discursive passages", "Literary passages"],
                 "learning_outcomes": ["Extract main ideas", "Infer meanings"]}
            ]},
            {"unit_number": 2, "unit_name": "Writing Skills and Grammar", "marks": 20, "chapters": [
                {"chapter_number": 1, "chapter_name": "Writing Skills",
                 "topics": ["Messages", "Postcards", "Notices", "Paragraph writing"],
                 "learning_outcomes": ["Write formal messages"]},
                {"chapter_number": 2, "chapter_name": "Grammar",
                 "topics": ["Tenses", "Modals", "Active-Passive Voice", "Reported Speech"],
                 "learning_outcomes": ["Apply grammar rules"]}
            ]},
            {"unit_number": 3, "unit_name": "Literature", "marks": 40, "chapters": [
                {"chapter_number": 1, "chapter_name": "Honeycomb (Main Reader)",
                 "topics": ["Three Questions", "A Gift of Chappals", "Gopal and the Hilsa Fish", "The Ashes That Made Trees Bloom", "Quality", "Expert Detectives", "The Invention of Vita-Wonk", "Fire: Friend and Foe", "A Bicycle in Good Repair", "The Story of Cricket"],
                 "learning_outcomes": ["Analyze literary devices"]},
                {"chapter_number": 2, "chapter_name": "An Alien Hand (Supplementary)",
                 "topics": ["The Tiny Teacher", "Bringing Up Kari", "The Desert", "The Cop and the Anthem", "Golu Grows a Nose", "I Want Something in a Cage", "Chandni", "The Bear Story", "A Tiger in the House", "An Alien Hand"],
                 "learning_outcomes": ["Understand narrative techniques"]}
            ]}
        ]
    }


def get_grade_7_hindi():
    return {
        "board": "CBSE", "grade": "7", "subject": "Hindi Course A", "subject_code": "002",
        "academic_year": "2024-25", "total_marks": 80, "theory_marks": 80,
        "practical_marks": 0, "internal_assessment": 20,
        "units": [
            {"unit_number": 1, "unit_name": "अपठित बोध", "marks": 10, "chapters": [
                {"chapter_number": 1, "chapter_name": "अपठित गद्यांश",
                 "topics": ["तथ्यात्मक गद्यांश", "विचारात्मक गद्यांश"],
                 "learning_outcomes": ["गद्यांश को समझना"]}
            ]},
            {"unit_number": 2, "unit_name": "व्यावहारिक व्याकरण", "marks": 16, "chapters": [
                {"chapter_number": 1, "chapter_name": "व्याकरण",
                 "topics": ["संज्ञा", "सर्वनाम", "विशेषण", "क्रिया", "वाक्य रचना"],
                 "learning_outcomes": ["व्याकरण नियम लागू करना"]}
            ]},
            {"unit_number": 3, "unit_name": "पाठ्यपुस्तक वसंत भाग-2", "marks": 24, "chapters": [
                {"chapter_number": 1, "chapter_name": "गद्य खंड",
                 "topics": ["हम पंछी उन्मुक्त गगन के", "दादी माँ", "हिमालय की बेटियाँ", "कठपुतली", "मिठाईवाला", "रक्त और हमारा शरीर", "पापा खो गए", "शाम - एक किसान", "चिड़िया की बच्ची", "अपूर्व अनुभव"],
                 "learning_outcomes": ["साहित्यिक तत्व समझना"]}
            ]},
            {"unit_number": 4, "unit_name": "पूरक पाठ्यपुस्तक महाभारत", "marks": 10, "chapters": [
                {"chapter_number": 1, "chapter_name": "महाभारत",
                 "topics": ["हार की जीत", "दान का हिसाब", "मित्र को पत्र", "अपना-अपना दुःख", "विश्वेश्वरैया", "गुण्डा", "संघर्ष के कारण मैं तुनुकमिज़ाज हो गया", "आश्रम का अनुमानित व्यय", "टोपी"],
                 "learning_outcomes": ["नैतिक मूल्य समझना"]}
            ]},
            {"unit_number": 5, "unit_name": "लेखन", "marks": 20, "chapters": [
                {"chapter_number": 1, "chapter_name": "रचनात्मक लेखन",
                 "topics": ["अनुच्छेद", "पत्र", "संवाद", "सूचना"],
                 "learning_outcomes": ["सही प्रारूप में लिखना"]}
            ]}
        ]
    }


# Grade 6 functions
def get_grade_6_mathematics():
    return {
        "board": "CBSE", "grade": "6", "subject": "Mathematics", "subject_code": "041",
        "academic_year": "2024-25", "total_marks": 80, "theory_marks": 80,
        "practical_marks": 0, "internal_assessment": 20,
        "units": [
            {"unit_number": 1, "unit_name": "Knowing Our Numbers", "marks": 5, "chapters": [
                {"chapter_number": 1, "chapter_name": "Knowing Our Numbers",
                 "topics": ["Comparing numbers", "Large numbers", "Estimation", "Roman numerals"],
                 "learning_outcomes": ["Compare and order numbers"]}
            ]},
            {"unit_number": 2, "unit_name": "Whole Numbers", "marks": 5, "chapters": [
                {"chapter_number": 2, "chapter_name": "Whole Numbers",
                 "topics": ["Number line", "Properties of whole numbers", "Patterns"],
                 "learning_outcomes": ["Apply properties of whole numbers"]}
            ]},
            {"unit_number": 3, "unit_name": "Playing with Numbers", "marks": 5, "chapters": [
                {"chapter_number": 3, "chapter_name": "Playing with Numbers",
                 "topics": ["Factors and multiples", "Prime and composite numbers", "HCF and LCM"],
                 "learning_outcomes": ["Find factors and multiples"]}
            ]},
            {"unit_number": 4, "unit_name": "Basic Geometrical Ideas", "marks": 6, "chapters": [
                {"chapter_number": 4, "chapter_name": "Basic Geometrical Ideas",
                 "topics": ["Points", "Lines", "Line segments", "Rays", "Angles", "Triangles", "Quadrilaterals", "Circles"],
                 "learning_outcomes": ["Identify geometric shapes"]}
            ]},
            {"unit_number": 5, "unit_name": "Understanding Elementary Shapes", "marks": 6, "chapters": [
                {"chapter_number": 5, "chapter_name": "Understanding Elementary Shapes",
                 "topics": ["Measuring line segments", "Angles", "Types of angles", "Polygons"],
                 "learning_outcomes": ["Classify angles and shapes"]}
            ]},
            {"unit_number": 6, "unit_name": "Integers", "marks": 7, "chapters": [
                {"chapter_number": 6, "chapter_name": "Integers",
                 "topics": ["Negative numbers", "Operations on integers", "Number line"],
                 "learning_outcomes": ["Perform operations on integers"]}
            ]},
            {"unit_number": 7, "unit_name": "Fractions", "marks": 8, "chapters": [
                {"chapter_number": 7, "chapter_name": "Fractions",
                 "topics": ["Types of fractions", "Like and unlike fractions", "Operations on fractions"],
                 "learning_outcomes": ["Solve problems using fractions"]}
            ]},
            {"unit_number": 8, "unit_name": "Decimals", "marks": 7, "chapters": [
                {"chapter_number": 8, "chapter_name": "Decimals",
                 "topics": ["Tenths and hundredths", "Comparing decimals", "Operations on decimals"],
                 "learning_outcomes": ["Use decimals in calculations"]}
            ]},
            {"unit_number": 9, "unit_name": "Data Handling", "marks": 6, "chapters": [
                {"chapter_number": 9, "chapter_name": "Data Handling",
                 "topics": ["Recording data", "Organizing data", "Pictographs", "Bar graphs"],
                 "learning_outcomes": ["Represent data graphically"]}
            ]},
            {"unit_number": 10, "unit_name": "Mensuration", "marks": 7, "chapters": [
                {"chapter_number": 10, "chapter_name": "Mensuration",
                 "topics": ["Perimeter", "Area of rectangle and square"],
                 "learning_outcomes": ["Calculate perimeter and area"]}
            ]},
            {"unit_number": 11, "unit_name": "Algebra", "marks": 7, "chapters": [
                {"chapter_number": 11, "chapter_name": "Algebra",
                 "topics": ["Variables", "Algebraic expressions", "Equations"],
                 "learning_outcomes": ["Form algebraic expressions"]}
            ]},
            {"unit_number": 12, "unit_name": "Ratio and Proportion", "marks": 8, "chapters": [
                {"chapter_number": 12, "chapter_name": "Ratio and Proportion",
                 "topics": ["Ratios", "Equivalent ratios", "Unitary method", "Proportion"],
                 "learning_outcomes": ["Solve proportion problems"]}
            ]},
            {"unit_number": 13, "unit_name": "Symmetry", "marks": 6, "chapters": [
                {"chapter_number": 13, "chapter_name": "Symmetry",
                 "topics": ["Lines of symmetry", "Symmetrical figures"],
                 "learning_outcomes": ["Identify symmetry"]}
            ]},
            {"unit_number": 14, "unit_name": "Practical Geometry", "marks": 7, "chapters": [
                {"chapter_number": 14, "chapter_name": "Practical Geometry",
                 "topics": ["Construction of circles", "Construction of line segments", "Perpendiculars", "Angles"],
                 "learning_outcomes": ["Construct geometric figures"]}
            ]}
        ]
    }


def get_grade_6_science():
    return {
        "board": "CBSE", "grade": "6", "subject": "Science", "subject_code": "086",
        "academic_year": "2024-25", "total_marks": 80, "theory_marks": 80,
        "practical_marks": 0, "internal_assessment": 20,
        "units": [
            {"unit_number": 1, "unit_name": "Food", "marks": 6, "chapters": [
                {"chapter_number": 1, "chapter_name": "Food: Where Does it Come From?",
                 "topics": ["Food sources", "Plant and animal products"],
                 "learning_outcomes": ["Identify food sources"]},
                {"chapter_number": 2, "chapter_name": "Components of Food",
                 "topics": ["Nutrients", "Balanced diet", "Deficiency diseases"],
                 "learning_outcomes": ["Plan balanced diet"]}
            ]},
            {"unit_number": 2, "unit_name": "Materials", "marks": 8, "chapters": [
                {"chapter_number": 3, "chapter_name": "Fibre to Fabric",
                 "topics": ["Plant fibres", "Animal fibres", "Spinning", "Weaving"],
                 "learning_outcomes": ["Trace fabric production"]},
                {"chapter_number": 4, "chapter_name": "Sorting Materials into Groups",
                 "topics": ["Properties of materials", "Classification"],
                 "learning_outcomes": ["Classify materials"]},
                {"chapter_number": 5, "chapter_name": "Separation of Substances",
                 "topics": ["Methods of separation", "Sedimentation", "Filtration"],
                 "learning_outcomes": ["Apply separation techniques"]},
                {"chapter_number": 6, "chapter_name": "Changes Around Us",
                 "topics": ["Reversible and irreversible changes"],
                 "learning_outcomes": ["Distinguish types of changes"]}
            ]},
            {"unit_number": 3, "unit_name": "The World of the Living", "marks": 10, "chapters": [
                {"chapter_number": 7, "chapter_name": "Getting to Know Plants",
                 "topics": ["Parts of plants", "Leaf structure", "Root types"],
                 "learning_outcomes": ["Identify plant parts"]},
                {"chapter_number": 8, "chapter_name": "Body Movements",
                 "topics": ["Human body movements", "Joints", "Gait of animals"],
                 "learning_outcomes": ["Explain movement mechanisms"]},
                {"chapter_number": 9, "chapter_name": "The Living Organisms - Characteristics and Habitats",
                 "topics": ["Characteristics of living things", "Adaptations", "Habitats"],
                 "learning_outcomes": ["Identify adaptations"]}
            ]},
            {"unit_number": 4, "unit_name": "Moving Things, People and Ideas", "marks": 8, "chapters": [
                {"chapter_number": 10, "chapter_name": "Motion and Measurement of Distances",
                 "topics": ["Motion types", "Measuring length", "Standard units"],
                 "learning_outcomes": ["Measure distances"]},
                {"chapter_number": 11, "chapter_name": "Light, Shadows and Reflections",
                 "topics": ["Light sources", "Shadows", "Mirrors"],
                 "learning_outcomes": ["Explain light phenomena"]},
                {"chapter_number": 12, "chapter_name": "Electricity and Circuits",
                 "topics": ["Electric cells", "Bulbs", "Circuits", "Conductors and insulators"],
                 "learning_outcomes": ["Construct simple circuits"]}
            ]},
            {"unit_number": 5, "unit_name": "How Things Work", "marks": 7, "chapters": [
                {"chapter_number": 13, "chapter_name": "Fun with Magnets",
                 "topics": ["Magnetic and non-magnetic materials", "Poles", "Finding directions"],
                 "learning_outcomes": ["Use magnets"]},
                {"chapter_number": 14, "chapter_name": "Water",
                 "topics": ["Sources of water", "Water cycle", "Conservation"],
                 "learning_outcomes": ["Explain water cycle"]},
                {"chapter_number": 15, "chapter_name": "Air Around Us",
                 "topics": ["Air composition", "Properties of air", "Air pollution"],
                 "learning_outcomes": ["Understand air properties"]},
                {"chapter_number": 16, "chapter_name": "Garbage In, Garbage Out",
                 "topics": ["Dealing with garbage", "Recycling", "Composting"],
                 "learning_outcomes": ["Practice waste management"]}
            ]}
        ]
    }


def get_grade_6_social_science():
    return {
        "board": "CBSE", "grade": "6", "subject": "Social Science", "subject_code": "087",
        "academic_year": "2024-25", "total_marks": 80, "theory_marks": 80,
        "practical_marks": 0, "internal_assessment": 20,
        "units": [
            {"unit_number": 1, "unit_name": "History - Our Pasts - I", "marks": 20, "chapters": [
                {"chapter_number": 1, "chapter_name": "What, Where, How and When?",
                 "topics": ["Sources of history", "Archaeological sources", "Periodization"],
                 "learning_outcomes": ["Understand historical sources"]},
                {"chapter_number": 2, "chapter_name": "From Hunting-Gathering to Growing Food",
                 "topics": ["Stone Age", "Early farmers", "Domestication"],
                 "learning_outcomes": ["Trace human evolution"]},
                {"chapter_number": 3, "chapter_name": "In the Earliest Cities",
                 "topics": ["Harappan civilization", "Cities", "Trade"],
                 "learning_outcomes": ["Analyze Harappan culture"]},
                {"chapter_number": 4, "chapter_name": "What Books and Burials Tell Us",
                 "topics": ["Vedic texts", "Social groups", "Megaliths"],
                 "learning_outcomes": ["Interpret ancient texts"]},
                {"chapter_number": 5, "chapter_name": "Kingdoms, Kings and an Early Republic",
                 "topics": ["Mahajanapadas", "Republics", "Administration"],
                 "learning_outcomes": ["Compare governance systems"]},
                {"chapter_number": 6, "chapter_name": "New Questions and Ideas",
                 "topics": ["Mahavira", "Buddha", "Upanishads"],
                 "learning_outcomes": ["Understand religious ideas"]},
                {"chapter_number": 7, "chapter_name": "Ashoka, The Emperor Who Gave Up War",
                 "topics": ["Mauryan empire", "Dhamma", "Inscriptions"],
                 "learning_outcomes": ["Analyze Ashoka's reign"]},
                {"chapter_number": 8, "chapter_name": "Vital Villages, Thriving Towns",
                 "topics": ["Agriculture", "Crafts", "Trade"],
                 "learning_outcomes": ["Understand ancient economy"]},
                {"chapter_number": 9, "chapter_name": "Traders, Kings and Pilgrims",
                 "topics": ["Silk Route", "Buddhism spread", "Trade networks"],
                 "learning_outcomes": ["Trace trade routes"]},
                {"chapter_number": 10, "chapter_name": "New Empires and Kingdoms",
                 "topics": ["Gupta empire", "Harshavardhana", "Pallavas"],
                 "learning_outcomes": ["Analyze post-Mauryan period"]},
                {"chapter_number": 11, "chapter_name": "Buildings, Paintings and Books",
                 "topics": ["Stupas", "Temples", "Paintings", "Literature"],
                 "learning_outcomes": ["Appreciate ancient art"]}
            ]},
            {"unit_number": 2, "unit_name": "Geography - The Earth: Our Habitat", "marks": 20, "chapters": [
                {"chapter_number": 1, "chapter_name": "The Earth in the Solar System",
                 "topics": ["Solar system", "Planets", "Earth"],
                 "learning_outcomes": ["Understand solar system"]},
                {"chapter_number": 2, "chapter_name": "Globe: Latitudes and Longitudes",
                 "topics": ["Globe", "Latitude", "Longitude", "Heat zones"],
                 "learning_outcomes": ["Locate places using coordinates"]},
                {"chapter_number": 3, "chapter_name": "Motions of the Earth",
                 "topics": ["Rotation", "Revolution", "Seasons"],
                 "learning_outcomes": ["Explain earth's motions"]},
                {"chapter_number": 4, "chapter_name": "Maps",
                 "topics": ["Map types", "Scale", "Symbols"],
                 "learning_outcomes": ["Read and interpret maps"]},
                {"chapter_number": 5, "chapter_name": "Major Domains of the Earth",
                 "topics": ["Lithosphere", "Atmosphere", "Hydrosphere", "Biosphere"],
                 "learning_outcomes": ["Identify earth's domains"]},
                {"chapter_number": 6, "chapter_name": "Major Landforms of the Earth",
                 "topics": ["Mountains", "Plateaus", "Plains"],
                 "learning_outcomes": ["Classify landforms"]},
                {"chapter_number": 7, "chapter_name": "Our Country - India",
                 "topics": ["Location", "Size", "Political divisions"],
                 "learning_outcomes": ["Locate India on map"]},
                {"chapter_number": 8, "chapter_name": "India: Climate, Vegetation and Wildlife",
                 "topics": ["Seasons", "Vegetation types", "Wildlife"],
                 "learning_outcomes": ["Explain India's climate"]}
            ]},
            {"unit_number": 3, "unit_name": "Civics - Social and Political Life - I", "marks": 20, "chapters": [
                {"chapter_number": 1, "chapter_name": "Understanding Diversity",
                 "topics": ["Diversity in India", "Unity in diversity"],
                 "learning_outcomes": ["Appreciate diversity"]},
                {"chapter_number": 2, "chapter_name": "Diversity and Discrimination",
                 "topics": ["Prejudice", "Discrimination", "Inequality"],
                 "learning_outcomes": ["Identify discrimination"]},
                {"chapter_number": 3, "chapter_name": "What is Government?",
                 "topics": ["Need for government", "Types", "Levels"],
                 "learning_outcomes": ["Understand government functions"]},
                {"chapter_number": 4, "chapter_name": "Key Elements of a Democratic Government",
                 "topics": ["Participation", "Accountability", "Equality"],
                 "learning_outcomes": ["Explain democratic principles"]},
                {"chapter_number": 5, "chapter_name": "Panchayati Raj",
                 "topics": ["Local self-government", "Gram Panchayat", "Block", "District"],
                 "learning_outcomes": ["Understand local governance"]},
                {"chapter_number": 6, "chapter_name": "Rural Administration",
                 "topics": ["Police", "Patwari", "Land records"],
                 "learning_outcomes": ["Explain rural administration"]},
                {"chapter_number": 7, "chapter_name": "Urban Administration",
                 "topics": ["Municipal corporation", "Ward", "Services"],
                 "learning_outcomes": ["Understand urban governance"]},
                {"chapter_number": 8, "chapter_name": "Rural Livelihoods",
                 "topics": ["Agriculture", "Non-farm activities"],
                 "learning_outcomes": ["Analyze rural economy"]},
                {"chapter_number": 9, "chapter_name": "Urban Livelihoods",
                 "topics": ["Street vendors", "Factories", "Offices"],
                 "learning_outcomes": ["Understand urban economy"]}
            ]},
            {"unit_number": 4, "unit_name": "Economics", "marks": 20, "chapters": [
                {"chapter_number": 1, "chapter_name": "Understanding Economic Activities",
                 "topics": ["Needs and wants", "Goods and services"],
                 "learning_outcomes": ["Understand basic economics"]}
            ]}
        ]
    }


def get_grade_6_english():
    return {
        "board": "CBSE", "grade": "6", "subject": "English", "subject_code": "184",
        "academic_year": "2024-25", "total_marks": 80, "theory_marks": 80,
        "practical_marks": 0, "internal_assessment": 20,
        "units": [
            {"unit_number": 1, "unit_name": "Reading Skills", "marks": 20, "chapters": [
                {"chapter_number": 1, "chapter_name": "Reading Comprehension",
                 "topics": ["Factual passages", "Literary passages"],
                 "learning_outcomes": ["Extract information from text"]}
            ]},
            {"unit_number": 2, "unit_name": "Writing Skills and Grammar", "marks": 20, "chapters": [
                {"chapter_number": 1, "chapter_name": "Writing Skills",
                 "topics": ["Picture composition", "Messages", "Informal letters", "Paragraph writing"],
                 "learning_outcomes": ["Write creative compositions"]},
                {"chapter_number": 2, "chapter_name": "Grammar",
                 "topics": ["Nouns", "Pronouns", "Adjectives", "Verbs", "Tenses", "Articles"],
                 "learning_outcomes": ["Apply basic grammar rules"]}
            ]},
            {"unit_number": 3, "unit_name": "Literature", "marks": 40, "chapters": [
                {"chapter_number": 1, "chapter_name": "Honeysuckle (Main Reader)",
                 "topics": ["A House, A Home", "The Kite", "The Quarrel", "Beauty", "Where Do All the Teachers Go?", "The Wonderful Words", "Vocation", "What If"],
                 "learning_outcomes": ["Appreciate poetry"]},
                {"chapter_number": 2, "chapter_name": "A Pact with the Sun (Supplementary)",
                 "topics": ["A Tale of Two Birds", "The Friendly Mongoose", "The Shepherd's Treasure", "The Old-Clock Shop", "Tansen", "The Monkey and the Crocodile", "The Wonder Called Sleep", "A Desert's Thirst Quencher", "A Strange Wrestling Match"],
                 "learning_outcomes": ["Extract moral lessons"]}
            ]}
        ]
    }


def get_grade_6_hindi():
    return {
        "board": "CBSE", "grade": "6", "subject": "Hindi Course A", "subject_code": "002",
        "academic_year": "2024-25", "total_marks": 80, "theory_marks": 80,
        "practical_marks": 0, "internal_assessment": 20,
        "units": [
            {"unit_number": 1, "unit_name": "अपठित बोध", "marks": 10, "chapters": [
                {"chapter_number": 1, "chapter_name": "अपठित गद्यांश",
                 "topics": ["गद्यांश पढ़ना और समझना"],
                 "learning_outcomes": ["अपठित गद्यांश समझना"]}
            ]},
            {"unit_number": 2, "unit_name": "व्यावहारिक व्याकरण", "marks": 16, "chapters": [
                {"chapter_number": 1, "chapter_name": "व्याकरण",
                 "topics": ["संज्ञा", "सर्वनाम", "विशेषण", "क्रिया", "वाक्य"],
                 "learning_outcomes": ["व्याकरण के मूल नियम"]}
            ]},
            {"unit_number": 3, "unit_name": "पाठ्यपुस्तक वसंत भाग-1", "marks": 24, "chapters": [
                {"chapter_number": 1, "chapter_name": "गद्य और पद्य",
                 "topics": ["वह चिड़िया जो", "बचपन", "नादान दोस्त", "चाँद से थोड़ी-सी गप्पें", "अक्षरों का महत्त्व", "पार नज़र के", "साथी हाथ बढ़ाना"],
                 "learning_outcomes": ["कविता और कहानी समझना"]}
            ]},
            {"unit_number": 4, "unit_name": "पूरक पाठ्यपुस्तक बाल रामकथा", "marks": 10, "chapters": [
                {"chapter_number": 1, "chapter_name": "बाल रामकथा",
                 "topics": ["अवधपुरी में राम", "जंगल और जनकपुर", "दो वरदान", "राम का वनगमन", "चित्रकूट में भरत", "दंडक वन में दस वर्ष", "सोने का हिरण", "सीता की खोज", "राम और सुग्रीव", "लंका में हनुमान", "लंका विजय", "राम का राज्याभिषेक"],
                 "learning_outcomes": ["रामकथा की जानकारी"]}
            ]},
            {"unit_number": 5, "unit_name": "लेखन", "marks": 20, "chapters": [
                {"chapter_number": 1, "chapter_name": "रचनात्मक लेखन",
                 "topics": ["अनुच्छेद", "पत्र", "चित्र वर्णन"],
                 "learning_outcomes": ["सरल लेखन"]}
            ]}
        ]
    }


def generate_all_json():
    """Generate JSON files for all Grade 6 & 7 subjects"""

    subjects = {
        "7": {
            "mathematics": get_grade_7_mathematics(),
            "science": get_grade_7_science(),
            "social_science": get_grade_7_social_science(),
            "english": get_grade_7_english(),
            "hindi": get_grade_7_hindi()
        },
        "6": {
            "mathematics": get_grade_6_mathematics(),
            "science": get_grade_6_science(),
            "social_science": get_grade_6_social_science(),
            "english": get_grade_6_english(),
            "hindi": get_grade_6_hindi()
        }
    }

    output_dir = Path("scripts/cbse_extractor/data/structured_json")
    output_dir.mkdir(parents=True, exist_ok=True)

    for grade, grade_subjects in subjects.items():
        for subject_name, subject_data in grade_subjects.items():
            filename = f"cbse_grade_{grade}_{subject_name}.json"
            filepath = output_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(subject_data, f, ensure_ascii=False, indent=2)

            print(f"✅ Generated: {filename} ({filepath.stat().st_size} bytes)")

    print(f"\n✅ All Grade 6-7 JSON files generated in {output_dir}")


if __name__ == "__main__":
    generate_all_json()
