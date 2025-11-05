#!/usr/bin/env python3
"""
Manual Grade 1-5 CBSE Syllabus Data
Structured data based on NCERT textbooks 2024-25
Subjects: Mathematics, English, Hindi, EVS (Environmental Studies)
"""

import json
from pathlib import Path


def create_primary_grade_subject(grade, subject, subject_code, units_data):
    """Helper to create subject structure"""
    return {
        "board": "CBSE",
        "grade": str(grade),
        "subject": subject,
        "subject_code": subject_code,
        "academic_year": "2024-25",
        "total_marks": 100,
        "theory_marks": 100,
        "practical_marks": 0,
        "internal_assessment": 0,
        "units": units_data
    }


# Grade 5 Subjects
def get_grade_5_mathematics():
    return create_primary_grade_subject("5", "Mathematics", "041", [
        {"unit_number": 1, "unit_name": "The Fish Tale", "marks": 8, "chapters": [
            {"chapter_number": 1, "chapter_name": "The Fish Tale",
             "topics": ["Large numbers", "Estimation"],
             "learning_outcomes": ["Read and write large numbers"]}
        ]},
        {"unit_number": 2, "unit_name": "Shapes and Angles", "marks": 10, "chapters": [
            {"chapter_number": 2, "chapter_name": "Shapes and Angles",
             "topics": ["Polygons", "Angles", "Types of angles"],
             "learning_outcomes": ["Identify shapes and angles"]}
        ]},
        {"unit_number": 3, "unit_name": "How Many Squares?", "marks": 8, "chapters": [
            {"chapter_number": 3, "chapter_name": "How Many Squares?",
             "topics": ["Area", "Perimeter"],
             "learning_outcomes": ["Calculate area and perimeter"]}
        ]},
        {"unit_number": 4, "unit_name": "Parts and Wholes", "marks": 12, "chapters": [
            {"chapter_number": 4, "chapter_name": "Parts and Wholes",
             "topics": ["Fractions", "Operations on fractions"],
             "learning_outcomes": ["Work with fractions"]}
        ]},
        {"unit_number": 5, "unit_name": "Does it Look the Same?", "marks": 8, "chapters": [
            {"chapter_number": 5, "chapter_name": "Does it Look the Same?",
             "topics": ["Symmetry", "Patterns"],
             "learning_outcomes": ["Identify symmetry"]}
        ]},
        {"unit_number": 6, "unit_name": "Be My Multiple, I'll be Your Factor", "marks": 10, "chapters": [
            {"chapter_number": 6, "chapter_name": "Be My Multiple, I'll be Your Factor",
             "topics": ["Factors", "Multiples", "Prime numbers"],
             "learning_outcomes": ["Find factors and multiples"]}
        ]},
        {"unit_number": 7, "unit_name": "Can You See the Pattern?", "marks": 8, "chapters": [
            {"chapter_number": 7, "chapter_name": "Can You See the Pattern?",
             "topics": ["Number patterns", "Sequences"],
             "learning_outcomes": ["Identify patterns"]}
        ]},
        {"unit_number": 8, "unit_name": "Mapping Your Way", "marks": 8, "chapters": [
            {"chapter_number": 8, "chapter_name": "Mapping Your Way",
             "topics": ["Maps", "Directions", "Scale"],
             "learning_outcomes": ["Read simple maps"]}
        ]},
        {"unit_number": 9, "unit_name": "Boxes and Sketches", "marks": 8, "chapters": [
            {"chapter_number": 9, "chapter_name": "Boxes and Sketches",
             "topics": ["3D shapes", "Views"],
             "learning_outcomes": ["Visualize 3D objects"]}
        ]},
        {"unit_number": 10, "unit_name": "Tenths and Hundredths", "marks": 10, "chapters": [
            {"chapter_number": 10, "chapter_name": "Tenths and Hundredths",
             "topics": ["Decimals", "Place value"],
             "learning_outcomes": ["Work with decimals"]}
        ]},
        {"unit_number": 11, "unit_name": "Area and its Boundary", "marks": 10, "chapters": [
            {"chapter_number": 11, "chapter_name": "Area and its Boundary",
             "topics": ["Area of rectangles", "Perimeter"],
             "learning_outcomes": ["Calculate areas"]}
        ]}
    ])


def get_grade_5_english():
    return create_primary_grade_subject("5", "English", "184", [
        {"unit_number": 1, "unit_name": "Reading", "marks": 30, "chapters": [
            {"chapter_number": 1, "chapter_name": "Marigold (Textbook)",
             "topics": ["Ice-cream Man", "Wonderful Waste!", "Bamboo Curry", "Crying", "My Shadow", "The Little Bully", "Nobody's Friend", "Class Discussion", "Topsy-Turvy Land", "Sing a Song of People"],
             "learning_outcomes": ["Read with comprehension", "Appreciate poetry"]}
        ]},
        {"unit_number": 2, "unit_name": "Writing", "marks": 25, "chapters": [
            {"chapter_number": 1, "chapter_name": "Composition",
             "topics": ["Picture composition", "Story writing", "Letter writing"],
             "learning_outcomes": ["Write creative texts"]}
        ]},
        {"unit_number": 3, "unit_name": "Grammar", "marks": 25, "chapters": [
            {"chapter_number": 1, "chapter_name": "Grammar",
             "topics": ["Nouns", "Pronouns", "Verbs", "Adjectives", "Tenses", "Sentences"],
             "learning_outcomes": ["Apply grammar rules"]}
        ]},
        {"unit_number": 4, "unit_name": "Listening and Speaking", "marks": 20, "chapters": [
            {"chapter_number": 1, "chapter_name": "Oral Communication",
             "topics": ["Listening comprehension", "Speaking activities"],
             "learning_outcomes": ["Communicate orally"]}
        ]}
    ])


def get_grade_5_hindi():
    return create_primary_grade_subject("5", "Hindi Course A", "002", [
        {"unit_number": 1, "unit_name": "पठन (Reading)", "marks": 30, "chapters": [
            {"chapter_number": 1, "chapter_name": "रिमझिम (पाठ्यपुस्तक)",
             "topics": ["राख की रस्सी", "फसलों के त्यौहार", "खिलौनेवाला", "नन्हा फनकार", "जहाँ चाह वहाँ राह", "चिट्ठी का सफ़र", "डाकिए की कहानी, पोस्टमैन की कहानी", "पुस्तकों की दुनिया", "सच्चे मित्र"],
             "learning_outcomes": ["पढ़ना और समझना"]}
        ]},
        {"unit_number": 2, "unit_name": "लेखन (Writing)", "marks": 25, "chapters": [
            {"chapter_number": 1, "chapter_name": "रचना",
             "topics": ["अनुच्छेद लेखन", "पत्र लेखन", "चित्र वर्णन"],
             "learning_outcomes": ["सरल रचना लिखना"]}
        ]},
        {"unit_number": 3, "unit_name": "व्याकरण (Grammar)", "marks": 25, "chapters": [
            {"chapter_number": 1, "chapter_name": "व्याकरण",
             "topics": ["संज्ञा", "सर्वनाम", "विशेषण", "क्रिया", "लिंग", "वचन"],
             "learning_outcomes": ["व्याकरण के नियम"]}
        ]},
        {"unit_number": 4, "unit_name": "श्रवण और वाचन (Listening and Speaking)", "marks": 20, "chapters": [
            {"chapter_number": 1, "chapter_name": "मौखिक संचार",
             "topics": ["सुनना", "बोलना"],
             "learning_outcomes": ["मौखिक संचार"]}
        ]}
    ])


def get_grade_5_evs():
    return create_primary_grade_subject("5", "Environmental Studies", "188", [
        {"unit_number": 1, "unit_name": "Family and Friends", "marks": 15, "chapters": [
            {"chapter_number": 1, "chapter_name": "Super Senses",
             "topics": ["Animal senses", "Human senses"],
             "learning_outcomes": ["Understand senses"]},
            {"chapter_number": 2, "chapter_name": "A Snake Charmer's Story",
             "topics": ["Snakes", "Traditional occupations"],
             "learning_outcomes": ["Appreciate diversity"]}
        ]},
        {"unit_number": 2, "unit_name": "Food", "marks": 15, "chapters": [
            {"chapter_number": 3, "chapter_name": "From Tasting to Digesting",
             "topics": ["Taste", "Digestion"],
             "learning_outcomes": ["Understand digestion"]},
            {"chapter_number": 4, "chapter_name": "Mangoes Round the Year",
             "topics": ["Food preservation", "Seasons"],
             "learning_outcomes": ["Identify preservation methods"]}
        ]},
        {"unit_number": 3, "unit_name": "Shelter", "marks": 15, "chapters": [
            {"chapter_number": 5, "chapter_name": "Seeds and Seeds",
             "topics": ["Types of seeds", "Seed dispersal"],
             "learning_outcomes": ["Classify seeds"]},
            {"chapter_number": 6, "chapter_name": "Every Drop Counts",
             "topics": ["Water sources", "Water conservation"],
             "learning_outcomes": ["Conserve water"]}
        ]},
        {"unit_number": 4, "unit_name": "Water", "marks": 15, "chapters": [
            {"chapter_number": 7, "chapter_name": "Experiments with Water",
             "topics": ["Properties of water", "Floating and sinking"],
             "learning_outcomes": ["Conduct simple experiments"]},
            {"chapter_number": 8, "chapter_name": "A Treat for Mosquitoes",
             "topics": ["Mosquito breeding", "Diseases"],
             "learning_outcomes": ["Prevent diseases"]}
        ]},
        {"unit_number": 5, "unit_name": "Travel", "marks": 20, "chapters": [
            {"chapter_number": 9, "chapter_name": "Up You Go!",
             "topics": ["Mountains", "Life in mountains"],
             "learning_outcomes": ["Understand mountain life"]},
            {"chapter_number": 10, "chapter_name": "Walls Tell Stories",
             "topics": ["Historical monuments", "Architecture"],
             "learning_outcomes": ["Appreciate heritage"]}
        ]},
        {"unit_number": 6, "unit_name": "Things We Make and Do", "marks": 20, "chapters": [
            {"chapter_number": 11, "chapter_name": "Sunita in Space",
             "topics": ["Space", "Astronauts"],
             "learning_outcomes": ["Learn about space"]},
            {"chapter_number": 12, "chapter_name": "What if it Finishes?",
             "topics": ["Natural resources", "Conservation"],
             "learning_outcomes": ["Value natural resources"]}
        ]}
    ])


# Grade 4 Subjects (similar simplified structure)
def get_grade_4_mathematics():
    return create_primary_grade_subject("4", "Mathematics", "041", [
        {"unit_number": 1, "unit_name": "Building with Bricks", "marks": 15, "chapters": [
            {"chapter_number": 1, "chapter_name": "Building with Bricks",
             "topics": ["Counting", "Large numbers", "Place value"],
             "learning_outcomes": ["Understand place value"]}
        ]},
        {"unit_number": 2, "unit_name": "Long and Short", "marks": 15, "chapters": [
            {"chapter_number": 2, "chapter_name": "Long and Short",
             "topics": ["Measurement", "Length", "Units"],
             "learning_outcomes": ["Measure lengths"]}
        ]},
        {"unit_number": 3, "unit_name": "A Trip to Bhopal", "marks": 15, "chapters": [
            {"chapter_number": 3, "chapter_name": "A Trip to Bhopal",
             "topics": ["Addition", "Subtraction", "Word problems"],
             "learning_outcomes": ["Solve word problems"]}
        ]},
        {"unit_number": 4, "unit_name": "Tick-Tick-Tick", "marks": 15, "chapters": [
            {"chapter_number": 4, "chapter_name": "Tick-Tick-Tick",
             "topics": ["Time", "Calendar"],
             "learning_outcomes": ["Tell time"]}
        ]},
        {"unit_number": 5, "unit_name": "The Way the World Looks", "marks": 10, "chapters": [
            {"chapter_number": 5, "chapter_name": "The Way the World Looks",
             "topics": ["Shapes", "Patterns"],
             "learning_outcomes": ["Identify shapes"]}
        ]},
        {"unit_number": 6, "unit_name": "The Junk Seller", "marks": 15, "chapters": [
            {"chapter_number": 6, "chapter_name": "The Junk Seller",
             "topics": ["Weight", "Measurement"],
             "learning_outcomes": ["Compare weights"]}
        ]},
        {"unit_number": 7, "unit_name": "Jugs and Mugs", "marks": 15, "chapters": [
            {"chapter_number": 7, "chapter_name": "Jugs and Mugs",
             "topics": ["Capacity", "Volume"],
             "learning_outcomes": ["Measure capacity"]}
        ]}
    ])


def get_grade_4_english():
    return create_primary_grade_subject("4", "English", "184", [
        {"unit_number": 1, "unit_name": "Reading and Literature", "marks": 40, "chapters": [
            {"chapter_number": 1, "chapter_name": "Marigold",
             "topics": ["Wake Up!", "Noses", "Run!", "Why?", "Don't be Afraid of the Dark", "The Donkey", "Trees", "The Little Fir Tree"],
             "learning_outcomes": ["Read and comprehend"]}
        ]},
        {"unit_number": 2, "unit_name": "Writing", "marks": 30, "chapters": [
            {"chapter_number": 1, "chapter_name": "Composition",
             "topics": ["Sentences", "Paragraphs", "Stories"],
             "learning_outcomes": ["Write simple texts"]}
        ]},
        {"unit_number": 3, "unit_name": "Grammar", "marks": 30, "chapters": [
            {"chapter_number": 1, "chapter_name": "Grammar",
             "topics": ["Nouns", "Verbs", "Adjectives", "Sentences"],
             "learning_outcomes": ["Use grammar correctly"]}
        ]}
    ])


def get_grade_4_hindi():
    return create_primary_grade_subject("4", "Hindi Course A", "002", [
        {"unit_number": 1, "unit_name": "पठन", "marks": 40, "chapters": [
            {"chapter_number": 1, "chapter_name": "रिमझिम",
             "topics": ["मन के भोले-भाले बादल", "जैसा सवाल वैसा जवाब", "किरमिच की गेंद", "पापा जब बच्चे थे", "दोस्त की पोशाक", "नाव बनाओ नाव बनाओ", "दान का हिसाब"],
             "learning_outcomes": ["पाठ समझना"]}
        ]},
        {"unit_number": 2, "unit_name": "लेखन", "marks": 30, "chapters": [
            {"chapter_number": 1, "chapter_name": "रचना",
             "topics": ["वाक्य", "अनुच्छेद"],
             "learning_outcomes": ["सरल लेखन"]}
        ]},
        {"unit_number": 3, "unit_name": "व्याकरण", "marks": 30, "chapters": [
            {"chapter_number": 1, "chapter_name": "व्याकरण",
             "topics": ["संज्ञा", "सर्वनाम", "विशेषण"],
             "learning_outcomes": ["व्याकरण समझना"]}
        ]}
    ])


def get_grade_4_evs():
    return create_primary_grade_subject("4", "Environmental Studies", "188", [
        {"unit_number": 1, "unit_name": "Family and Friends", "marks": 20, "chapters": [
            {"chapter_number": 1, "chapter_name": "Going to School",
             "topics": ["Different ways of going to school"],
             "learning_outcomes": ["Appreciate diversity"]},
            {"chapter_number": 2, "chapter_name": "Ear to Ear",
             "topics": ["Hearing", "Sound"],
             "learning_outcomes": ["Understand senses"]}
        ]},
        {"unit_number": 2, "unit_name": "Food", "marks": 20, "chapters": [
            {"chapter_number": 3, "chapter_name": "A Day with Nandu",
             "topics": ["Elephants", "Animals"],
             "learning_outcomes": ["Learn about animals"]},
            {"chapter_number": 4, "chapter_name": "The Story of Amrita",
             "topics": ["Trees", "Environment"],
             "learning_outcomes": ["Value environment"]}
        ]},
        {"unit_number": 3, "unit_name": "Water", "marks": 20, "chapters": [
            {"chapter_number": 5, "chapter_name": "Anita and the Honeybees",
             "topics": ["Bees", "Honey"],
             "learning_outcomes": ["Learn about insects"]},
            {"chapter_number": 6, "chapter_name": "Omana's Journey",
             "topics": ["Travel", "Places"],
             "learning_outcomes": ["Understand geography"]}
        ]},
        {"unit_number": 4, "unit_name": "Shelter", "marks": 20, "chapters": [
            {"chapter_number": 7, "chapter_name": "From the Window",
             "topics": ["Observation", "Changes"],
             "learning_outcomes": ["Observe surroundings"]},
            {"chapter_number": 8, "chapter_name": "Reaching Grandmother's House",
             "topics": ["Transport", "Journey"],
             "learning_outcomes": ["Learn about transport"]}
        ]},
        {"unit_number": 5, "unit_name": "Travel", "marks": 20, "chapters": [
            {"chapter_number": 9, "chapter_name": "Changing Families",
             "topics": ["Family types", "Changes"],
             "learning_outcomes": ["Understand family structures"]},
            {"chapter_number": 10, "chapter_name": "Hu Tu Tu, Hu Tu Tu",
             "topics": ["Games", "Exercise"],
             "learning_outcomes": ["Value physical activity"]}
        ]}
    ])


# Grade 3 Subjects
def get_grade_3_mathematics():
    return create_primary_grade_subject("3", "Mathematics", "041", [
        {"unit_number": 1, "unit_name": "Where to Look From?", "marks": 20, "chapters": [
            {"chapter_number": 1, "chapter_name": "Where to Look From?",
             "topics": ["Observation", "Directions"],
             "learning_outcomes": ["Understand viewpoints"]}
        ]},
        {"unit_number": 2, "unit_name": "Fun with Numbers", "marks": 25, "chapters": [
            {"chapter_number": 2, "chapter_name": "Fun with Numbers",
             "topics": ["Counting", "Numbers up to 1000"],
             "learning_outcomes": ["Count and order numbers"]}
        ]},
        {"unit_number": 3, "unit_name": "Give and Take", "marks": 25, "chapters": [
            {"chapter_number": 3, "chapter_name": "Give and Take",
             "topics": ["Addition", "Subtraction"],
             "learning_outcomes": ["Add and subtract"]}
        ]},
        {"unit_number": 4, "unit_name": "Long and Short", "marks": 15, "chapters": [
            {"chapter_number": 4, "chapter_name": "Long and Short",
             "topics": ["Measurement", "Comparison"],
             "learning_outcomes": ["Measure and compare"]}
        ]},
        {"unit_number": 5, "unit_name": "Shapes and Designs", "marks": 15, "chapters": [
            {"chapter_number": 5, "chapter_name": "Shapes and Designs",
             "topics": ["2D shapes", "Patterns"],
             "learning_outcomes": ["Identify shapes"]}
        ]}
    ])


def get_grade_3_english():
    return create_primary_grade_subject("3", "English", "184", [
        {"unit_number": 1, "unit_name": "Reading", "marks": 50, "chapters": [
            {"chapter_number": 1, "chapter_name": "Marigold",
             "topics": ["Nina and the Baby Sparrows", "The Enormous Turnip", "Sea Song", "A Little Fish Story", "The Balloon Man", "The Yellow Butterfly"],
             "learning_outcomes": ["Read simple texts"]}
        ]},
        {"unit_number": 2, "unit_name": "Writing and Grammar", "marks": 50, "chapters": [
            {"chapter_number": 1, "chapter_name": "Language Skills",
             "topics": ["Writing sentences", "Basic grammar"],
             "learning_outcomes": ["Write simple sentences"]}
        ]}
    ])


def get_grade_3_hindi():
    return create_primary_grade_subject("3", "Hindi Course A", "002", [
        {"unit_number": 1, "unit_name": "पठन", "marks": 50, "chapters": [
            {"chapter_number": 1, "chapter_name": "रिमझिम",
             "topics": ["कक्का", "मन करता है", "बहादुर बित्तो", "हम भी सीखें", "चाँद वाली अम्मा", "गुड्डे की नाक", "दादी की सीख"],
             "learning_outcomes": ["सरल पाठ पढ़ना"]}
        ]},
        {"unit_number": 2, "unit_name": "लेखन और व्याकरण", "marks": 50, "chapters": [
            {"chapter_number": 1, "chapter_name": "भाषा कौशल",
             "topics": ["वाक्य", "मूल व्याकरण"],
             "learning_outcomes": ["सरल वाक्य लिखना"]}
        ]}
    ])


def get_grade_3_evs():
    return create_primary_grade_subject("3", "Environmental Studies", "188", [
        {"unit_number": 1, "unit_name": "Family and Friends", "marks": 25, "chapters": [
            {"chapter_number": 1, "chapter_name": "Poonams Day Out",
             "topics": ["Daily routine", "Time"],
             "learning_outcomes": ["Understand daily activities"]},
            {"chapter_number": 2, "chapter_name": "The Plant Fairy",
             "topics": ["Plants", "Parts of plants"],
             "learning_outcomes": ["Identify plant parts"]}
        ]},
        {"unit_number": 2, "unit_name": "Food and Shelter", "marks": 25, "chapters": [
            {"chapter_number": 3, "chapter_name": "Water O Water!",
             "topics": ["Uses of water", "Sources"],
             "learning_outcomes": ["Value water"]},
            {"chapter_number": 4, "chapter_name": "Our First School",
             "topics": ["School", "Learning"],
             "learning_outcomes": ["Appreciate school"]}
        ]},
        {"unit_number": 3, "unit_name": "Living and Non-living", "marks": 25, "chapters": [
            {"chapter_number": 5, "chapter_name": "Chhotu's House",
             "topics": ["Houses", "Types of houses"],
             "learning_outcomes": ["Compare houses"]},
            {"chapter_number": 6, "chapter_name": "Foods We Eat",
             "topics": ["Food", "Healthy eating"],
             "learning_outcomes": ["Identify healthy food"]}
        ]},
        {"unit_number": 4, "unit_name": "Animals and Plants", "marks": 25, "chapters": [
            {"chapter_number": 7, "chapter_name": "Saying Without Speaking",
             "topics": ["Communication", "Signs"],
             "learning_outcomes": ["Understand communication"]},
            {"chapter_number": 8, "chapter_name": "Flying High",
             "topics": ["Birds", "Flight"],
             "learning_outcomes": ["Learn about birds"]}
        ]}
    ])


# Grade 2 Subjects
def get_grade_2_mathematics():
    return create_primary_grade_subject("2", "Mathematics", "041", [
        {"unit_number": 1, "unit_name": "Numbers", "marks": 40, "chapters": [
            {"chapter_number": 1, "chapter_name": "What is Long, What is Round?",
             "topics": ["Shapes", "Counting"],
             "learning_outcomes": ["Count objects"]},
            {"chapter_number": 2, "chapter_name": "Counting in Groups",
             "topics": ["Grouping", "Tens and ones"],
             "learning_outcomes": ["Group objects"]}
        ]},
        {"unit_number": 2, "unit_name": "Operations", "marks": 30, "chapters": [
            {"chapter_number": 3, "chapter_name": "How Much Can You Carry?",
             "topics": ["Addition", "Subtraction"],
             "learning_outcomes": ["Add and subtract small numbers"]}
        ]},
        {"unit_number": 3, "unit_name": "Patterns and Shapes", "marks": 30, "chapters": [
            {"chapter_number": 4, "chapter_name": "Counting in Tens",
             "topics": ["Skip counting", "Patterns"],
             "learning_outcomes": ["Identify patterns"]}
        ]}
    ])


def get_grade_2_english():
    return create_primary_grade_subject("2", "English", "184", [
        {"unit_number": 1, "unit_name": "Reading", "marks": 50, "chapters": [
            {"chapter_number": 1, "chapter_name": "Marigold",
             "topics": ["First Day at School", "Haldi's Adventure", "I am Lucky!", "A Smile", "The Wind and the Sun"],
             "learning_outcomes": ["Read simple stories"]}
        ]},
        {"unit_number": 2, "unit_name": "Writing", "marks": 50, "chapters": [
            {"chapter_number": 1, "chapter_name": "Language Practice",
             "topics": ["Writing words", "Simple sentences"],
             "learning_outcomes": ["Write basic sentences"]}
        ]}
    ])


def get_grade_2_hindi():
    return create_primary_grade_subject("2", "Hindi Course A", "002", [
        {"unit_number": 1, "unit_name": "पठन", "marks": 50, "chapters": [
            {"chapter_number": 1, "chapter_name": "रिमझिम",
             "topics": ["आम की कहानी", "भालू ने खेली फुटबॉल", "म्याऊँ, म्याऊँ!!", "अधिकार", "बहुत हुआ"],
             "learning_outcomes": ["कहानी पढ़ना"]}
        ]},
        {"unit_number": 2, "unit_name": "लेखन", "marks": 50, "chapters": [
            {"chapter_number": 1, "chapter_name": "भाषा अभ्यास",
             "topics": ["शब्द", "वाक्य"],
             "learning_outcomes": ["शब्द और वाक्य लिखना"]}
        ]}
    ])


def get_grade_2_evs():
    return create_primary_grade_subject("2", "Environmental Studies", "188", [
        {"unit_number": 1, "unit_name": "My Family and Friends", "marks": 33, "chapters": [
            {"chapter_number": 1, "chapter_name": "What's in My Name?",
             "topics": ["Names", "Family"],
             "learning_outcomes": ["Understand identity"]},
            {"chapter_number": 2, "chapter_name": "My Family",
             "topics": ["Family members", "Relationships"],
             "learning_outcomes": ["Value family"]}
        ]},
        {"unit_number": 2, "unit_name": "Living Things", "marks": 34, "chapters": [
            {"chapter_number": 3, "chapter_name": "Animals and Their Young Ones",
             "topics": ["Baby animals", "Animal homes"],
             "learning_outcomes": ["Identify animals"]},
            {"chapter_number": 4, "chapter_name": "Plants Around Us",
             "topics": ["Types of plants", "Uses"],
             "learning_outcomes": ["Appreciate plants"]}
        ]},
        {"unit_number": 3, "unit_name": "Food and Water", "marks": 33, "chapters": [
            {"chapter_number": 5, "chapter_name": "Food We Eat",
             "topics": ["Food types", "Healthy food"],
             "learning_outcomes": ["Choose healthy food"]},
            {"chapter_number": 6, "chapter_name": "Water",
             "topics": ["Uses of water", "Saving water"],
             "learning_outcomes": ["Save water"]}
        ]}
    ])


# Grade 1 Subjects
def get_grade_1_mathematics():
    return create_primary_grade_subject("1", "Mathematics", "041", [
        {"unit_number": 1, "unit_name": "Numbers 1-9", "marks": 50, "chapters": [
            {"chapter_number": 1, "chapter_name": "Numbers and Counting",
             "topics": ["Counting 1-9", "Number names", "Before-after"],
             "learning_outcomes": ["Count and recognize numbers 1-9"]}
        ]},
        {"unit_number": 2, "unit_name": "Shapes and Patterns", "marks": 50, "chapters": [
            {"chapter_number": 2, "chapter_name": "Basic Shapes",
             "topics": ["Circle", "Triangle", "Square", "Rectangle"],
             "learning_outcomes": ["Identify basic shapes"]}
        ]}
    ])


def get_grade_1_english():
    return create_primary_grade_subject("1", "English", "184", [
        {"unit_number": 1, "unit_name": "Reading", "marks": 50, "chapters": [
            {"chapter_number": 1, "chapter_name": "Marigold",
             "topics": ["A Happy Child", "Three Little Pigs", "The Bubble, the Straw, and the Shoe", "Lalu and Peelu"],
             "learning_outcomes": ["Read simple rhymes"]}
        ]},
        {"unit_number": 2, "unit_name": "Writing", "marks": 50, "chapters": [
            {"chapter_number": 1, "chapter_name": "Letters and Words",
             "topics": ["Alphabets", "Simple words"],
             "learning_outcomes": ["Write alphabets and words"]}
        ]}
    ])


def get_grade_1_hindi():
    return create_primary_grade_subject("1", "Hindi Course A", "002", [
        {"unit_number": 1, "unit_name": "पठन", "marks": 50, "chapters": [
            {"chapter_number": 1, "chapter_name": "रिमझिम",
             "topics": ["झूला", "आम की टोकरी", "आम की कहानी", "पत्ते ही पत्ते"],
             "learning_outcomes": ["कविता पढ़ना"]}
        ]},
        {"unit_number": 2, "unit_name": "लेखन", "marks": 50, "chapters": [
            {"chapter_number": 1, "chapter_name": "अक्षर और शब्द",
             "topics": ["वर्णमाला", "सरल शब्द"],
             "learning_outcomes": ["अक्षर और शब्द लिखना"]}
        ]}
    ])


def get_grade_1_evs():
    return create_primary_grade_subject("1", "Environmental Studies", "188", [
        {"unit_number": 1, "unit_name": "Myself", "marks": 33, "chapters": [
            {"chapter_number": 1, "chapter_name": "My Body",
             "topics": ["Body parts", "Senses"],
             "learning_outcomes": ["Identify body parts"]}
        ]},
        {"unit_number": 2, "unit_name": "My Family and School", "marks": 34, "chapters": [
            {"chapter_number": 2, "chapter_name": "My Family",
             "topics": ["Family members"],
             "learning_outcomes": ["Know family members"]},
            {"chapter_number": 3, "chapter_name": "My School",
             "topics": ["School building", "Classroom"],
             "learning_outcomes": ["Familiarize with school"]}
        ]},
        {"unit_number": 3, "unit_name": "Plants and Animals", "marks": 33, "chapters": [
            {"chapter_number": 4, "chapter_name": "Animals Around Us",
             "topics": ["Pet animals", "Wild animals"],
             "learning_outcomes": ["Name animals"]},
            {"chapter_number": 5, "chapter_name": "Plants",
             "topics": ["Trees", "Flowers"],
             "learning_outcomes": ["Identify plants"]}
        ]}
    ])


def generate_all_primary_json():
    """Generate JSON files for all Grade 1-5 subjects"""

    subjects_by_grade = {
        "5": {
            "mathematics": get_grade_5_mathematics(),
            "english": get_grade_5_english(),
            "hindi": get_grade_5_hindi(),
            "evs": get_grade_5_evs()
        },
        "4": {
            "mathematics": get_grade_4_mathematics(),
            "english": get_grade_4_english(),
            "hindi": get_grade_4_hindi(),
            "evs": get_grade_4_evs()
        },
        "3": {
            "mathematics": get_grade_3_mathematics(),
            "english": get_grade_3_english(),
            "hindi": get_grade_3_hindi(),
            "evs": get_grade_3_evs()
        },
        "2": {
            "mathematics": get_grade_2_mathematics(),
            "english": get_grade_2_english(),
            "hindi": get_grade_2_hindi(),
            "evs": get_grade_2_evs()
        },
        "1": {
            "mathematics": get_grade_1_mathematics(),
            "english": get_grade_1_english(),
            "hindi": get_grade_1_hindi(),
            "evs": get_grade_1_evs()
        }
    }

    output_dir = Path("scripts/cbse_extractor/data/structured_json")
    output_dir.mkdir(parents=True, exist_ok=True)

    total_generated = 0
    for grade, grade_subjects in subjects_by_grade.items():
        for subject_name, subject_data in grade_subjects.items():
            filename = f"cbse_grade_{grade}_{subject_name}.json"
            filepath = output_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(subject_data, f, ensure_ascii=False, indent=2)

            print(f"✅ Grade {grade} - {subject_name.title()}: {filepath.stat().st_size} bytes")
            total_generated += 1

    print(f"\n{'='*80}")
    print(f"✅ All {total_generated} Primary Grade (1-5) JSON files generated successfully!")
    print(f"{'='*80}")


if __name__ == "__main__":
    generate_all_primary_json()
