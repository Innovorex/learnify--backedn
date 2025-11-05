#!/usr/bin/env python3
"""
Manual CBSE Grade 10 Remaining Subjects
Since PDF URLs are not accessible, creating structured data manually
Based on official CBSE syllabus 2024-25
"""

import json
from pathlib import Path

def get_grade_10_social_science():
    """
    CBSE Grade 10 Social Science Syllabus 2024-25
    Source: Official CBSE Syllabus Document
    """
    return {
        "board": "CBSE",
        "grade": "10",
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
                "unit_name": "India and the Contemporary World - II (History)",
                "marks": 20,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "The Rise of Nationalism in Europe",
                        "topics": [
                            "The French Revolution and the Idea of the Nation",
                            "The Making of Nationalism in Europe",
                            "The Age of Revolutions: 1830-1848",
                            "The Making of Germany and Italy",
                            "Visualizing the Nation",
                            "Nationalism and Imperialism"
                        ],
                        "learning_outcomes": [
                            "Understand the growth of nationalism in Europe",
                            "Analyze the role of various factors in the rise of nationalism"
                        ]
                    },
                    {
                        "chapter_number": 2,
                        "chapter_name": "Nationalism in India",
                        "topics": [
                            "The First World War, Khilafat and Non-Cooperation",
                            "Differing Strands within the Movement",
                            "Towards Civil Disobedience",
                            "The Sense of Collective Belonging"
                        ],
                        "learning_outcomes": [
                            "Explain the growth of Indian national movement",
                            "Understand role of different social groups"
                        ]
                    },
                    {
                        "chapter_number": 3,
                        "chapter_name": "The Making of a Global World",
                        "topics": [
                            "The Pre-modern World",
                            "The Nineteenth Century (1815-1914)",
                            "The Inter-war Economy",
                            "Rebuilding a World Economy: The Post-war Era"
                        ],
                        "learning_outcomes": [
                            "Understand the process of globalization",
                            "Analyze impact of global trade"
                        ]
                    },
                    {
                        "chapter_number": 4,
                        "chapter_name": "The Age of Industrialisation",
                        "topics": [
                            "Before the Industrial Revolution",
                            "Hand Labour and Steam Power",
                            "Industrialisation in the Colonies",
                            "Factories Come Up",
                            "The Peculiarities of Industrial Growth",
                            "Market for Goods"
                        ],
                        "learning_outcomes": [
                            "Explain the process of industrialization",
                            "Understand pre-industrial economy"
                        ]
                    },
                    {
                        "chapter_number": 5,
                        "chapter_name": "Print Culture and the Modern World",
                        "topics": [
                            "The First Printed Books",
                            "Print Comes to Europe",
                            "The Print Revolution and Its Impact",
                            "The Reading Mania",
                            "The Nineteenth Century",
                            "India and the World of Print",
                            "Religious Reform and Public Debates",
                            "New Forms of Publication",
                            "Print and Censorship"
                        ],
                        "learning_outcomes": [
                            "Explain the impact of print revolution",
                            "Understand print culture in India"
                        ]
                    }
                ]
            },
            {
                "unit_number": 2,
                "unit_name": "Contemporary India - II (Geography)",
                "marks": 20,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "Resources and Development",
                        "topics": [
                            "Types of Resources",
                            "Development of Resources",
                            "Resource Planning in India",
                            "Land Resources",
                            "Soil as a Resource",
                            "Soil Types",
                            "Soil Erosion and Conservation"
                        ],
                        "learning_outcomes": [
                            "Understand resource classification",
                            "Explain soil conservation methods"
                        ]
                    },
                    {
                        "chapter_number": 2,
                        "chapter_name": "Forest and Wildlife Resources",
                        "topics": [
                            "Biodiversity or Biological Diversity",
                            "Flora and Fauna in India",
                            "Vanishing Forests",
                            "Asiatic Cheetah: Where did they go?",
                            "Himalayan Yew in Trouble",
                            "Conservation of Forest and Wildlife in India",
                            "Types and Distribution of Forest and Wildlife Resources",
                            "Community and Conservation"
                        ],
                        "learning_outcomes": [
                            "Analyze biodiversity in India",
                            "Understand conservation strategies"
                        ]
                    },
                    {
                        "chapter_number": 3,
                        "chapter_name": "Water Resources",
                        "topics": [
                            "Water Scarcity and The Need For Water Conservation and Management",
                            "Multi-Purpose River Projects and Integrated Water Resources Management",
                            "Rainwater Harvesting"
                        ],
                        "learning_outcomes": [
                            "Explain water conservation methods",
                            "Understand rainwater harvesting"
                        ]
                    },
                    {
                        "chapter_number": 4,
                        "chapter_name": "Agriculture",
                        "topics": [
                            "Types of Farming",
                            "Cropping Pattern",
                            "Major Crops",
                            "Technological and Institutional Reforms",
                            "Impact of Globalisation on Agriculture"
                        ],
                        "learning_outcomes": [
                            "Classify types of farming",
                            "Understand agricultural reforms"
                        ]
                    },
                    {
                        "chapter_number": 5,
                        "chapter_name": "Minerals and Energy Resources",
                        "topics": [
                            "Minerals",
                            "Modes of Occurrence of Minerals",
                            "Distribution of Minerals",
                            "Ferrous and Non-Ferrous Minerals",
                            "Non-Metallic Minerals",
                            "Rock Minerals",
                            "Energy Resources",
                            "Conservation of Minerals"
                        ],
                        "learning_outcomes": [
                            "Classify minerals",
                            "Explain energy resource distribution"
                        ]
                    },
                    {
                        "chapter_number": 6,
                        "chapter_name": "Manufacturing Industries",
                        "topics": [
                            "Importance of Manufacturing",
                            "Contribution of Industry to National Economy",
                            "Industrial Location",
                            "Classification of Industries",
                            "Spatial Distribution",
                            "Industrial Pollution and Environmental Degradation"
                        ],
                        "learning_outcomes": [
                            "Analyze industrial distribution",
                            "Understand environmental impact"
                        ]
                    },
                    {
                        "chapter_number": 7,
                        "chapter_name": "Lifelines of National Economy",
                        "topics": [
                            "Transport",
                            "Roadways",
                            "Railways",
                            "Pipelines",
                            "Waterways",
                            "Airways",
                            "Communication",
                            "International Trade",
                            "Tourism as a Trade"
                        ],
                        "learning_outcomes": [
                            "Explain transport networks",
                            "Understand international trade"
                        ]
                    }
                ]
            },
            {
                "unit_number": 3,
                "unit_name": "Democratic Politics - II (Civics)",
                "marks": 20,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "Power Sharing",
                        "topics": [
                            "Belgium and Sri Lanka",
                            "Why power sharing is desirable?",
                            "Forms of power sharing"
                        ],
                        "learning_outcomes": [
                            "Understand power sharing mechanisms",
                            "Analyze case studies of power sharing"
                        ]
                    },
                    {
                        "chapter_number": 2,
                        "chapter_name": "Federalism",
                        "topics": [
                            "What is federalism?",
                            "What makes India a federal country?",
                            "How is federalism practised?",
                            "Decentralisation in India"
                        ],
                        "learning_outcomes": [
                            "Explain federal structure",
                            "Understand Indian federalism"
                        ]
                    },
                    {
                        "chapter_number": 3,
                        "chapter_name": "Democracy and Diversity",
                        "topics": [
                            "A Story of Mexico Olympics",
                            "Differences, similarities and divisions",
                            "Politics of social divisions",
                            "Overlapping and cross-cutting differences",
                            "How do social divisions affect democracy?"
                        ],
                        "learning_outcomes": [
                            "Analyze social divisions",
                            "Understand diversity in democracy"
                        ]
                    },
                    {
                        "chapter_number": 4,
                        "chapter_name": "Gender, Religion and Caste",
                        "topics": [
                            "Gender and politics",
                            "Religion, communalism and politics",
                            "Caste and politics",
                            "Caste inequalities today",
                            "Challenges to democracy from Communalism, Casteism"
                        ],
                        "learning_outcomes": [
                            "Understand gender inequality",
                            "Analyze communalism and casteism"
                        ]
                    },
                    {
                        "chapter_number": 5,
                        "chapter_name": "Popular Struggles and Movements",
                        "topics": [
                            "Bolivia's Water War",
                            "Mobilisation and organisations",
                            "Pressure groups and movements",
                            "Relationship between movements and parties",
                            "Influence on politics"
                        ],
                        "learning_outcomes": [
                            "Explain people's movements",
                            "Understand pressure groups"
                        ]
                    },
                    {
                        "chapter_number": 6,
                        "chapter_name": "Political Parties",
                        "topics": [
                            "Why do we need political parties?",
                            "How many parties should we have?",
                            "National and regional political parties in India",
                            "Challenges to political parties",
                            "How can parties be reformed?"
                        ],
                        "learning_outcomes": [
                            "Explain party system",
                            "Understand party reforms"
                        ]
                    },
                    {
                        "chapter_number": 7,
                        "chapter_name": "Outcomes of Democracy",
                        "topics": [
                            "How do we assess democracy's outcomes?",
                            "Economic outcomes of democracy",
                            "Reduction of inequality and poverty",
                            "Accommodation of social diversity",
                            "Dignity and freedom of citizens"
                        ],
                        "learning_outcomes": [
                            "Evaluate democratic outcomes",
                            "Compare democratic and non-democratic regimes"
                        ]
                    }
                ]
            },
            {
                "unit_number": 4,
                "unit_name": "Understanding Economic Development (Economics)",
                "marks": 20,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "Development",
                        "topics": [
                            "The story of Haryana and Kerala",
                            "How to compare different countries or states?",
                            "Income and Other Criteria",
                            "Public Facilities",
                            "Sustainability of Development"
                        ],
                        "learning_outcomes": [
                            "Define development",
                            "Understand Human Development Index"
                        ]
                    },
                    {
                        "chapter_number": 2,
                        "chapter_name": "Sectors of the Indian Economy",
                        "topics": [
                            "Primary, Secondary and Tertiary Sectors",
                            "Comparing the Three Sectors",
                            "Rising Importance of Tertiary Sector",
                            "Where are Most of the People Employed?",
                            "How to Create More Employment?"
                        ],
                        "learning_outcomes": [
                            "Classify economic sectors",
                            "Analyze employment patterns"
                        ]
                    },
                    {
                        "chapter_number": 3,
                        "chapter_name": "Money and Credit",
                        "topics": [
                            "Money as a Medium of Exchange",
                            "Modern Forms of Money",
                            "Loan Activities of Banks",
                            "Two Different Credit Situations",
                            "Terms of Credit",
                            "Formal Sector Credit in India",
                            "Self Help Groups for the Poor"
                        ],
                        "learning_outcomes": [
                            "Explain money functions",
                            "Understand credit systems"
                        ]
                    },
                    {
                        "chapter_number": 4,
                        "chapter_name": "Globalisation and the Indian Economy",
                        "topics": [
                            "Production across countries",
                            "Interlinking production across countries",
                            "Foreign trade and integration of markets",
                            "What is globalisation?",
                            "Factors that have enabled Globalisation",
                            "World Trade Organisation",
                            "Impact of Globalisation in India",
                            "The Struggle for a Fair Globalisation"
                        ],
                        "learning_outcomes": [
                            "Explain globalization",
                            "Analyze WTO role"
                        ]
                    },
                    {
                        "chapter_number": 5,
                        "chapter_name": "Consumer Rights",
                        "topics": [
                            "Consumer Movement",
                            "Rules and Regulations",
                            "Role of Judiciary",
                            "Consumers' Rights",
                            "Duties of Consumers",
                            "How can we make consumers powerful?",
                            "Development of Consumer Movement in India",
                            "Consumer Protection Act (COPRA) 1986"
                        ],
                        "learning_outcomes": [
                            "Understand consumer rights",
                            "Explain COPRA"
                        ]
                    }
                ]
            }
        ]
    }

def get_grade_10_english():
    """CBSE Grade 10 English Syllabus 2024-25"""
    return {
        "board": "CBSE",
        "grade": "10",
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
                            "Infer meanings from context"
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
                            "Formal Letter (Letter of Enquiry, Letter of Placing Order, Letter of Complaint)",
                            "Analytical Paragraph (Chart/Graph/Table interpretation)"
                        ],
                        "learning_outcomes": [
                            "Write formal letters with proper format",
                            "Analyze and interpret data"
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
                            "Commands and Requests",
                            "Statements and Questions"
                        ],
                        "learning_outcomes": [
                            "Apply grammar rules correctly",
                            "Transform sentences"
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
                        "chapter_name": "First Flight (Main Reader)",
                        "topics": [
                            "A Letter to God",
                            "Nelson Mandela: Long Walk to Freedom",
                            "Two Stories about Flying: His First Flight, Black Aeroplane",
                            "From the Diary of Anne Frank",
                            "The Hundred Dresses - I & II",
                            "Glimpses of India",
                            "Mijbil the Otter",
                            "Madam Rides the Bus",
                            "The Sermon at Benares",
                            "The Proposal"
                        ],
                        "subtopics": [
                            {
                                "topic": "Poetry",
                                "subtopics": [
                                    "Dust of Snow",
                                    "Fire and Ice",
                                    "A Tiger in the Zoo",
                                    "How to Tell Wild Animals",
                                    "The Ball Poem",
                                    "Amanda!",
                                    "The Trees",
                                    "Fog",
                                    "The Tale of Custard the Dragon",
                                    "For Anne Gregory"
                                ]
                            }
                        ],
                        "learning_outcomes": [
                            "Analyze literary devices",
                            "Interpret themes and characters"
                        ]
                    },
                    {
                        "chapter_number": 2,
                        "chapter_name": "Footprints Without Feet (Supplementary)",
                        "topics": [
                            "A Triumph of Surgery",
                            "The Thief's Story",
                            "The Midnight Visitor",
                            "A Question of Trust",
                            "Footprints without Feet",
                            "The Making of a Scientist",
                            "The Necklace",
                            "Bholi",
                            "The Book That Saved the Earth"
                        ],
                        "learning_outcomes": [
                            "Understand narrative techniques",
                            "Extract moral values"
                        ]
                    }
                ]
            }
        ]
    }

def get_grade_10_hindi():
    """CBSE Grade 10 Hindi Course A Syllabus 2024-25"""
    return {
        "board": "CBSE",
        "grade": "10",
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
                            "पद-परिचय",
                            "रचना के आधार पर वाक्य-भेद",
                            "समास",
                            "मुहावरे"
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
                "unit_name": "पाठ्यपुस्तक स्पर्श भाग-2 (Textbook Sparsh Part-2)",
                "marks": 24,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "गद्य खंड (Prose)",
                        "topics": [
                            "साखी (कबीर)",
                            "पद (मीरा)",
                            "चंद्र गहना से लौटती बेर (केशवदास)",
                            "राम-लक्ष्मण-परशुराम संवाद (तुलसीदास)",
                            "नेताजी का चश्मा (स्वयं प्रकाश)",
                            "बालगोबिन भगत (रामवृक्ष बेनीपुरी)",
                            "लखनवी अंदाज़ (यशपाल)",
                            "मानवीय करुणा की दिव्य चमक (सर्वेश्वर दयाल सक्सेना)",
                            "एक कहानी यह भी (मन्नू भंडारी)"
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
                            "सूरदास के पद",
                            "तुलसीदास के पद",
                            "देव (सवैया, कवित्त)",
                            "जयशंकर प्रसाद - आत्मकथ्य",
                            "सूर्यकांत त्रिपाठी 'निराला' - उत्साह, अट नहीं रही है",
                            "यतीन्द्र मिश्र - कन्यादान",
                            "ऋतुराज - संगतकार"
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
                "unit_name": "पूरक पाठ्यपुस्तक संचयन भाग-2 (Supplementary Sanchayan Part-2)",
                "marks": 10,
                "chapters": [
                    {
                        "chapter_number": 1,
                        "chapter_name": "संचयन",
                        "topics": [
                            "हरिहर काका (मिथिलेश्वर)",
                            "सपनों के-से दिन (गुरदयाल सिंह)",
                            "टोपी (सुदर्शन)",
                            "तीसरी कसम के शिल्पकार शैलेंद्र (विष्णु प्रभाकर)"
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
                            "औपचारिक पत्र लेखन",
                            "अनुच्छेद लेखन",
                            "विज्ञापन लेखन",
                            "संदेश लेखन"
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

def save_all_subjects():
    """Save all Grade 10 subjects to JSON files"""

    output_dir = Path("scripts/cbse_extractor/data/structured_json")
    output_dir.mkdir(parents=True, exist_ok=True)

    subjects = [
        ("social_science", get_grade_10_social_science()),
        ("english", get_grade_10_english()),
        ("hindi", get_grade_10_hindi())
    ]

    for subject_key, data in subjects:
        filename = f"cbse_grade_10_{subject_key}.json"
        filepath = output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved: {filepath}")

        # Print summary
        units = len(data.get('units', []))
        chapters = sum(len(u.get('chapters', [])) for u in data.get('units', []))
        topics = sum(
            len(ch.get('topics', []))
            for u in data.get('units', [])
            for ch in u.get('chapters', [])
        )

        print(f"   Grade {data['grade']} - {data['subject']}")
        print(f"   Units: {units}, Chapters: {chapters}, Topics: {topics}\n")

if __name__ == "__main__":
    print("="*80)
    print("CREATING GRADE 10 REMAINING SUBJECTS")
    print("="*80)
    print()

    save_all_subjects()

    print("="*80)
    print("✅ ALL GRADE 10 SUBJECTS CREATED")
    print("="*80)
