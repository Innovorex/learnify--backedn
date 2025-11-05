# 🎯 COMPLETE EXECUTION PLAN: CBSE Syllabus (Grades 1-10)

## ✅ STATUS: Phase 1 COMPLETE (Grade 10: Maths & Science)

---

## 📊 CURRENT PROGRESS

### Completed:
- ✅ Grade 10 Mathematics (15 chapters, 7 units)
- ✅ Grade 10 Science (13 chapters, 5 units)

### Remaining:
- ⏳ Grade 10: Social Science, English, Hindi (3 subjects)
- ⏳ Grade 9: All 5 core subjects
- ⏳ Grades 6-8: 15 entries (5 subjects × 3 grades)
- ⏳ Grades 1-5: 20 entries (4 subjects × 5 grades)

**Total Needed: 45+ entries**
**Currently Have: 2/45 (4.4%)**

---

## 🚀 STEP-BY-STEP EXECUTION GUIDE

### PHASE 2: Complete Grade 10 (Remaining 3 Subjects)

#### Step 1: Add Grade 10 Social Science

```python
# Add to fetch_cbse_data.py

def fetch_grade_10_social_science(self):
    """Fetch real CBSE Grade 10 Social Science syllabus"""
    syllabus = {
        "board": "CBSE",
        "grade": "10",
        "subject": "Social Science",
        "subject_code": "087",
        "academic_year": "2024-25",
        "total_marks": 100,
        "theory_marks": 80,
        "internal_assessment": 20,
        "sections": [
            {
                "section": "History",
                "name": "India and the Contemporary World - II",
                "marks": 20,
                "chapters": [
                    {
                        "chapter": 1,
                        "name": "The Rise of Nationalism in Europe",
                        "topics": ["French Revolution", "Napoleon", "Unification of Italy and Germany"]
                    },
                    {
                        "chapter": 2,
                        "name": "Nationalism in India",
                        "topics": ["Non-Cooperation Movement", "Civil Disobedience", "Quit India Movement"]
                    },
                    {
                        "chapter": 3,
                        "name": "The Making of a Global World",
                        "topics": ["Trade routes", "Colonialism", "World Wars impact"]
                    },
                    {
                        "chapter": 4,
                        "name": "The Age of Industrialisation",
                        "topics": ["Factory system", "Industrial Revolution"]
                    },
                    {
                        "chapter": 5,
                        "name": "Print Culture and Modern World",
                        "topics": ["Printing press", "Impact on society"]
                    }
                ]
            },
            {
                "section": "Geography",
                "name": "Contemporary India - II",
                "marks": 20,
                "chapters": [
                    {
                        "chapter": 1,
                        "name": "Resources and Development",
                        "topics": ["Types of resources", "Resource planning", "Land resources"]
                    },
                    {
                        "chapter": 2,
                        "name": "Forest and Wildlife Resources",
                        "topics": ["Biodiversity", "Conservation", "Community participation"]
                    },
                    {
                        "chapter": 3,
                        "name": "Water Resources",
                        "topics": ["Water scarcity", "Irrigation", "Rainwater harvesting"]
                    },
                    {
                        "chapter": 4,
                        "name": "Agriculture",
                        "topics": ["Crop types", "Farming systems", "Agricultural reforms"]
                    },
                    {
                        "chapter": 5,
                        "name": "Minerals and Energy Resources",
                        "topics": ["Types of minerals", "Energy sources", "Conservation"]
                    },
                    {
                        "chapter": 6,
                        "name": "Manufacturing Industries",
                        "topics": ["Industrial location", "Types of industries"]
                    },
                    {
                        "chapter": 7,
                        "name": "Lifelines of National Economy",
                        "topics": ["Transport", "Communication", "Trade"]
                    }
                ]
            },
            {
                "section": "Civics",
                "name": "Democratic Politics - II",
                "marks": 20,
                "chapters": [
                    {
                        "chapter": 1,
                        "name": "Power Sharing",
                        "topics": ["Belgium model", "Forms of power sharing"]
                    },
                    {
                        "chapter": 2,
                        "name": "Federalism",
                        "topics": ["Federal features", "Indian federalism"]
                    },
                    {
                        "chapter": 3,
                        "name": "Democracy and Diversity",
                        "topics": ["Social divisions", "Political expression"]
                    },
                    {
                        "chapter": 4,
                        "name": "Gender, Religion and Caste",
                        "topics": ["Gender inequality", "Communalism", "Caste system"]
                    },
                    {
                        "chapter": 5,
                        "name": "Popular Struggles and Movements",
                        "topics": ["Social movements", "Pressure groups"]
                    },
                    {
                        "chapter": 6,
                        "name": "Political Parties",
                        "topics": ["Party system", "Functions", "Challenges"]
                    },
                    {
                        "chapter": 7,
                        "name": "Outcomes of Democracy",
                        "topics": ["Democratic outcomes", "Challenges"]
                    }
                ]
            },
            {
                "section": "Economics",
                "name": "Understanding Economic Development",
                "marks": 20,
                "chapters": [
                    {
                        "chapter": 1,
                        "name": "Development",
                        "topics": ["Economic development", "HDI", "Sustainability"]
                    },
                    {
                        "chapter": 2,
                        "name": "Sectors of the Indian Economy",
                        "topics": ["Primary, Secondary, Tertiary sectors"]
                    },
                    {
                        "chapter": 3,
                        "name": "Money and Credit",
                        "topics": ["Functions of money", "Banking", "Credit"]
                    },
                    {
                        "chapter": 4,
                        "name": "Globalisation and Indian Economy",
                        "topics": ["WTO", "Impact of globalization"]
                    },
                    {
                        "chapter": 5,
                        "name": "Consumer Rights",
                        "topics": ["Consumer protection", "COPRA"]
                    }
                ]
            }
        ]
    }
    return syllabus
```

#### Step 2: Add Grade 10 English

```python
def fetch_grade_10_english(self):
    """Fetch real CBSE Grade 10 English syllabus"""
    syllabus = {
        "board": "CBSE",
        "grade": "10",
        "subject": "English",
        "subject_code": "184",
        "academic_year": "2024-25",
        "total_marks": 100,
        "theory_marks": 80,
        "internal_assessment": 20,
        "sections": [
            {
                "section": "Reading",
                "marks": 20,
                "topics": [
                    "Comprehension passages",
                    "Note-making",
                    "Inferential reading"
                ]
            },
            {
                "section": "Writing and Grammar",
                "marks": 30,
                "topics": [
                    "Letter Writing: Formal and Informal",
                    "Article Writing",
                    "Analytical Paragraph",
                    "Tenses",
                    "Modals",
                    "Subject-Verb Agreement",
                    "Reported Speech",
                    "Active and Passive Voice"
                ]
            },
            {
                "section": "Literature",
                "marks": 30,
                "textbooks": [
                    {
                        "book": "First Flight",
                        "chapters": [
                            "A Letter to God",
                            "Nelson Mandela: Long Walk to Freedom",
                            "Two Stories about Flying",
                            "From the Diary of Anne Frank",
                            "The Hundred Dresses - I & II",
                            "Glimpses of India",
                            "Mijbil the Otter",
                            "Madam Rides the Bus",
                            "The Sermon at Benares",
                            "The Proposal"
                        ],
                        "poems": [
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
                    },
                    {
                        "book": "Footprints Without Feet",
                        "chapters": [
                            "A Triumph of Surgery",
                            "The Thief's Story",
                            "The Midnight Visitor",
                            "A Question of Trust",
                            "Footprints without Feet",
                            "The Making of a Scientist",
                            "The Necklace",
                            "Bholi",
                            "The Book That Saved the Earth"
                        ]
                    }
                ]
            }
        ]
    }
    return syllabus
```

#### Step 3: Run Updated Fetcher

```bash
# Update fetch_cbse_data.py with above functions
# Then run:
python3 scripts/cbse_syllabus/fetch_cbse_data.py

# Populate database:
python3 scripts/cbse_syllabus/populate_database.py
```

---

### PHASE 3: Grade 9 (All 5 Subjects)

Repeat similar pattern for Grade 9:
- Mathematics (Same units as Grade 10 but different chapters)
- Science
- Social Science
- English
- Hindi

**Estimated Time:** 2-3 hours for data structuring

---

### PHASE 4: Grades 6-8 (Middle School)

For Grades 6-8, use NCERT structure:

```python
# Example: Grade 8 Mathematics

def fetch_grade_8_mathematics(self):
    """Fetch CBSE Grade 8 Mathematics (NCERT-based)"""
    syllabus = {
        "board": "CBSE",
        "grade": "8",
        "subject": "Mathematics",
        "academic_year": "2024-25",
        "chapters": [
            {
                "chapter": 1,
                "name": "Rational Numbers",
                "topics": ["Properties", "Representation", "Operations"]
            },
            {
                "chapter": 2,
                "name": "Linear Equations in One Variable",
                "topics": ["Solving equations", "Applications"]
            },
            {
                "chapter": 3,
                "name": "Understanding Quadrilaterals",
                "topics": ["Types", "Properties", "Angle sum"]
            },
            # ... 16 chapters total
        ]
    }
    return syllabus
```

**Note:** For Grades 6-8, refer to NCERT textbooks directly as CBSE follows NCERT curriculum.

---

### PHASE 5: Grades 1-5 (Primary)

For primary classes:

```python
def fetch_grade_1_mathematics(self):
    """Fetch CBSE Grade 1 Mathematics"""
    syllabus = {
        "board": "CBSE",
        "grade": "1",
        "subject": "Mathematics",
        "academic_year": "2024-25",
        "chapters": [
            {"chapter": 1, "name": "Shapes and Space"},
            {"chapter": 2, "name": "Numbers from One to Nine"},
            {"chapter": 3, "name": "Addition"},
            {"chapter": 4, "name": "Subtraction"},
            {"chapter": 5, "name": "Numbers from Ten to Twenty"},
            {"chapter": 6, "name": "Time"},
            {"chapter": 7, "name": "Measurement"},
            {"chapter": 8, "name": "Numbers from Twenty-one to Fifty"},
            {"chapter": 9, "name": "Data Handling"},
            {"chapter": 10, "name": "Patterns"},
            {"chapter": 11, "name": "Numbers"},
            {"chapter": 12, "name": "Money"}
        ]
    }
    return syllabus

def fetch_grade_1_evs(self):
    """Fetch CBSE Grade 1 Environmental Studies"""
    syllabus = {
        "board": "CBSE",
        "grade": "1",
        "subject": "EVS",
        "academic_year": "2024-25",
        "themes": [
            "Family and Friends",
            "Food",
            "Shelter",
            "Water",
            "Travel",
            "Things We Make and Do"
        ]
    }
    return syllabus
```

---

## 📋 COMPLETE EXECUTION CHECKLIST

### ✅ Completed:
- [x] Grade 10 Mathematics
- [x] Grade 10 Science

### 🔄 In Progress:
- [ ] Grade 10 Social Science
- [ ] Grade 10 English
- [ ] Grade 10 Hindi

### 📝 Pending:

**Grade 9 (5 subjects):**
- [ ] Mathematics
- [ ] Science
- [ ] Social Science
- [ ] English
- [ ] Hindi

**Grade 8 (5 subjects):**
- [ ] Mathematics
- [ ] Science
- [ ] Social Science
- [ ] English
- [ ] Hindi

**Grade 7 (5 subjects):**
- [ ] Mathematics
- [ ] Science
- [ ] Social Science
- [ ] English
- [ ] Hindi

**Grade 6 (5 subjects):**
- [ ] Mathematics
- [ ] Science
- [ ] Social Science
- [ ] English
- [ ] Hindi

**Grades 1-5 (4 subjects each = 20 entries):**
Each grade needs:
- [ ] Mathematics
- [ ] English
- [ ] Hindi
- [ ] EVS

---

## 🛠️ QUICK COMMANDS

### 1. Fetch All Data:
```bash
cd /home/learnify/lt/learnify-teach/backend
python3 scripts/cbse_syllabus/fetch_cbse_data.py
```

### 2. Populate Database:
```bash
python3 scripts/cbse_syllabus/populate_database.py
```

### 3. Verify Data:
```bash
python3 -c "
import psycopg2
conn = psycopg2.connect(host='localhost', port=5432, database='te', user='innovorex', password='Innovorex@1')
cursor = conn.cursor()
cursor.execute('SELECT grade, subject FROM syllabus_cache WHERE board=\\'CBSE\\' ORDER BY grade, subject')
for row in cursor.fetchall():
    print(f'Grade {row[0]}: {row[1]}')
conn.close()
"
```

### 4. Clean Database:
```bash
python3 -c "
import psycopg2
conn = psycopg2.connect(host='localhost', port=5432, database='te', user='innovorex', password='Innovorex@1')
cursor = conn.cursor()
cursor.execute('DELETE FROM syllabus_cache WHERE board=\\'CBSE\\'')
conn.commit()
print(f'Deleted {cursor.rowcount} entries')
conn.close()
"
```

---

## 📊 TARGET METRICS

| Metric | Target | Current | Progress |
|--------|--------|---------|----------|
| Total Entries | 45+ | 2 | 4% |
| Grade 10 | 5 subjects | 2 | 40% |
| Grade 9 | 5 subjects | 0 | 0% |
| Grades 6-8 | 15 subjects | 0 | 0% |
| Grades 1-5 | 20 subjects | 0 | 0% |

---

## 🎯 NEXT IMMEDIATE STEPS

1. **Update fetch_cbse_data.py** with Grade 10 SST, English, Hindi functions
2. **Run fetcher** to generate JSON files
3. **Run populator** to insert into database
4. **Verify** data quality
5. **Repeat** for remaining grades

---

## 📚 RESOURCES

- **Official CBSE**: https://cbseacademic.nic.in/
- **NCERT Textbooks**: https://ncert.nic.in/textbook.php
- **CBSE Syllabus PDFs**: Check outputs/pdfs folder

---

**Last Updated:** 2025-11-03
**Status:** Phase 1 Complete (2/45 entries)
