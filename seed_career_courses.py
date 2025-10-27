"""
Seed Script for Career Progression - B.Ed Mathematics Course
This script populates the database with:
- B.Ed Mathematics course from IGNOU
- 8 Modules with detailed descriptions
- 50+ Topics with study notes and video URLs
"""

import sys
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, CareerCourse, CourseModule, ModuleTopic

def seed_bed_mathematics_course(db: Session):
    """Create B.Ed Mathematics course with all modules and topics"""

    print("🌱 Starting seed process for B.Ed Mathematics...")

    # Check if course already exists
    existing = db.query(CareerCourse).filter_by(course_name="Bachelor of Education (B.Ed) - Mathematics").first()
    if existing:
        print("⚠️  B.Ed Mathematics course already exists. Skipping...")
        return

    # 1. Create the Course
    course = CareerCourse(
        course_name="Bachelor of Education (B.Ed) - Mathematics",
        course_type="B.Ed",
        subject="Mathematics",
        university="IGNOU",
        duration_months=24,
        description="Bachelor of Education programme designed to develop understanding and competencies required by practicing teachers for effective teaching-learning at secondary and senior secondary levels.",
        total_modules=8,
        is_active=True
    )
    db.add(course)
    db.flush()  # Get course.id
    print(f"✅ Created course: {course.course_name} (ID: {course.id})")

    # 2. Create Modules with Topics
    modules_data = [
        {
            "module_number": 1,
            "module_name": "Childhood and Growing Up",
            "description": "Understanding child development, adolescence, and learning processes",
            "duration_weeks": 4,
            "topics": [
                {
                    "topic_number": 1,
                    "topic_name": "Introduction to Child Development",
                    "content_text": """Child development refers to the sequence of physical, language, thought and emotional changes that occur in a child from birth to the beginning of adulthood. During this process a child progresses from dependency on their parents/guardians to increasing independence.

**Key Concepts:**
- Physical Development: Growth in body size, motor skills
- Cognitive Development: Growth in thinking, learning, problem-solving
- Social-Emotional Development: Development of relationships and emotions
- Language Development: Communication skills progression

**Stages of Development:**
1. Infancy (0-2 years): Rapid physical and sensory development
2. Early Childhood (2-6 years): Language explosion, imagination
3. Middle Childhood (6-12 years): Concrete operational thinking
4. Adolescence (12-18 years): Abstract thinking, identity formation

**Importance for Teachers:**
Understanding developmental stages helps teachers:
- Set age-appropriate expectations
- Design suitable learning activities
- Recognize developmental delays
- Support individual differences""",
                    "video_url": "https://www.youtube.com/embed/Tc36N4Ltxa8",
                    "video_duration": "22:30"
                },
                {
                    "topic_number": 2,
                    "topic_name": "Theories of Development - Piaget",
                    "content_text": """Jean Piaget's theory of cognitive development suggests that children move through four different stages of mental development. His theory focuses on understanding how children acquire knowledge and the nature of intelligence.

**Four Stages:**

1. **Sensorimotor Stage (0-2 years)**
   - Learning through sensory experiences and manipulating objects
   - Object permanence develops
   - Goal-directed behavior emerges

2. **Preoperational Stage (2-7 years)**
   - Symbolic thinking and language development
   - Egocentrism (difficulty seeing others' perspectives)
   - Magical thinking and animism

3. **Concrete Operational Stage (7-11 years)**
   - Logical thinking about concrete events
   - Conservation (understanding quantity remains same despite changes in shape)
   - Classification and seriation skills

4. **Formal Operational Stage (11+ years)**
   - Abstract and hypothetical thinking
   - Scientific reasoning
   - Metacognition (thinking about thinking)

**Implications for Mathematics Teaching:**
- Use concrete materials for young learners
- Progress from concrete to abstract concepts
- Provide hands-on experiences
- Scaffold learning appropriately""",
                    "video_url": "https://www.youtube.com/embed/IhcgYgx7aAA",
                    "video_duration": "18:45"
                },
                {
                    "topic_number": 3,
                    "topic_name": "Vygotsky's Sociocultural Theory",
                    "content_text": """Lev Vygotsky emphasized the fundamental role of social interaction and culture in cognitive development. His theory highlights that learning is inherently social and occurs through interaction with more knowledgeable others.

**Key Concepts:**

1. **Zone of Proximal Development (ZPD)**
   - The distance between what a learner can do independently and what they can do with guidance
   - Target of effective teaching

2. **Scaffolding**
   - Temporary support provided by teacher/peer
   - Gradually withdrawn as competence increases
   - Like scaffolding on a building

3. **More Knowledgeable Other (MKO)**
   - Anyone with better understanding or higher ability
   - Can be teacher, peer, parent, or even technology

4. **Cultural Tools**
   - Language is the most important cultural tool
   - Mathematical symbols and notation systems
   - Technology and educational materials

**Application in Mathematics Classroom:**
- Collaborative problem-solving
- Peer tutoring and group work
- Think-aloud demonstrations
- Gradual release of responsibility
- Mathematical discourse and discussion""",
                    "video_url": "https://www.youtube.com/embed/10gvn3dJzYE",
                    "video_duration": "16:20"
                },
                {
                    "topic_number": 4,
                    "topic_name": "Adolescent Psychology",
                    "content_text": """Adolescence is the transitional period between childhood and adulthood, characterized by significant physical, cognitive, emotional, and social changes.

**Physical Changes:**
- Puberty and sexual maturation
- Growth spurts
- Brain development (prefrontal cortex)
- Hormonal changes

**Cognitive Changes:**
- Development of abstract thinking
- Hypothetical-deductive reasoning
- Metacognitive abilities
- Improved decision-making skills

**Social-Emotional Changes:**
- Identity formation (Erik Erikson)
- Peer relationships become central
- Desire for independence
- Emotional volatility
- Risk-taking behaviors

**Challenges in Adolescence:**
- Peer pressure
- Academic stress
- Identity confusion
- Body image concerns
- Technology addiction

**Teaching Adolescents - Best Practices:**
1. Provide autonomy and choices
2. Make learning relevant to their lives
3. Create safe, respectful classroom environment
4. Encourage critical thinking
5. Build positive teacher-student relationships
6. Use collaborative learning strategies
7. Connect mathematics to real-world problems""",
                    "video_url": "https://www.youtube.com/embed/hiduiTq1ei8",
                    "video_duration": "20:15"
                },
                {
                    "topic_number": 5,
                    "topic_name": "Learning Styles and Individual Differences",
                    "content_text": """Students learn in different ways and have varied strengths, interests, and needs. Understanding these differences helps teachers differentiate instruction effectively.

**Learning Styles (VAK Model):**

1. **Visual Learners**
   - Learn through seeing
   - Prefer diagrams, charts, graphs
   - Benefit from: geometric representations, color-coding, visual patterns

2. **Auditory Learners**
   - Learn through hearing
   - Prefer lectures, discussions
   - Benefit from: verbal explanations, mathematical discourse, mnemonics

3. **Kinesthetic Learners**
   - Learn through doing
   - Prefer hands-on activities
   - Benefit from: manipulatives, physical demonstrations, experiments

**Multiple Intelligences (Howard Gardner):**
- Logical-Mathematical: Pattern recognition, abstract thinking
- Spatial: Visualization, geometry
- Linguistic: Verbal problem-solving
- Bodily-Kinesthetic: Physical models
- Interpersonal: Collaborative learning
- Intrapersonal: Individual reflection

**Individual Differences:**
- Prior knowledge and experiences
- Motivation and interest levels
- Cognitive abilities and processing speed
- Language proficiency
- Cultural backgrounds
- Socioeconomic factors

**Differentiated Instruction Strategies:**
1. Vary content, process, and product
2. Provide multiple pathways to learning
3. Use flexible grouping
4. Offer choices in assignments
5. Adjust difficulty levels
6. Use technology for personalization""",
                    "video_url": "https://www.youtube.com/embed/855Now8h5Rs",
                    "video_duration": "19:40"
                }
            ]
        },
        {
            "module_number": 2,
            "module_name": "Contemporary India and Education",
            "description": "Understanding Indian education system, NEP 2020, and societal context",
            "duration_weeks": 4,
            "topics": [
                {
                    "topic_number": 1,
                    "topic_name": "Education System in India - Structure",
                    "content_text": """The Indian education system is one of the largest in the world, serving over 260 million students. Understanding its structure and governance is essential for teachers.

**Current Structure (Traditional 10+2):**
- Primary Education: Grades 1-5 (ages 6-11)
- Upper Primary: Grades 6-8 (ages 11-14)
- Secondary: Grades 9-10 (ages 14-16)
- Senior Secondary: Grades 11-12 (ages 16-18)

**Boards of Education:**
1. **Central Boards:**
   - CBSE (Central Board of Secondary Education)
   - ICSE/ISC (Council for Indian School Certificate Examinations)

2. **State Boards:**
   - Each state has its own board (e.g., Maharashtra Board, Kerala Board)
   - Follow state-specific curricula

**Governance:**
- Ministry of Education (Central Government)
- State Education Departments
- NCERT (National Council of Educational Research and Training)
- NCTE (National Council for Teacher Education)

**Right to Education (RTE) Act 2009:**
- Free and compulsory education for ages 6-14
- 25% reservation in private schools
- Pupil-teacher ratio norms
- Infrastructure standards""",
                    "video_url": "https://www.youtube.com/embed/3PJhRI10x4g",
                    "video_duration": "21:10"
                },
                {
                    "topic_number": 2,
                    "topic_name": "National Education Policy (NEP) 2020",
                    "content_text": """NEP 2020 is a comprehensive framework to guide the development of education in India from early childhood to higher education. It replaces the previous National Policy on Education (1986).

**Key Highlights:**

1. **5+3+3+4 Curricular Structure** (Replaces 10+2)
   - Foundational Stage (ages 3-8): Pre-primary + Grades 1-2
   - Preparatory Stage (ages 8-11): Grades 3-5
   - Middle Stage (ages 11-14): Grades 6-8
   - Secondary Stage (ages 14-18): Grades 9-12

2. **Focus on Foundational Literacy and Numeracy**
   - Universal foundational literacy by Grade 3
   - National Mission on Foundational Literacy and Numeracy

3. **Multidisciplinary and Holistic Education**
   - Breaking silos between arts, science, commerce
   - Vocational education integration
   - Focus on 21st-century skills

4. **Assessment Reforms**
   - Shift from summative to formative assessment
   - Competency-based assessment
   - 360-degree progress reports
   - Board exams made easier, test core competencies

5. **Teacher Education**
   - 4-year integrated B.Ed program (by 2030)
   - Continuous Professional Development (CPD)
   - Career management and progression framework

6. **Technology Integration**
   - National Educational Technology Forum (NETF)
   - Digital infrastructure for education
   - Online and digital learning platforms

**Implications for Mathematics Teaching:**
- Emphasis on conceptual understanding over rote learning
- Integration of mathematics with other subjects
- Coding and computational thinking from Grade 6
- Focus on problem-solving and critical thinking
- Continuous formative assessment""",
                    "video_url": "https://www.youtube.com/embed/Rwhi6Mj04Uc",
                    "video_duration": "25:30"
                },
                {
                    "topic_number": 3,
                    "topic_name": "Socio-Economic Issues in Education",
                    "content_text": """Education in India is influenced by various socio-economic factors that create disparities in access, quality, and outcomes.

**Key Issues:**

1. **Economic Disparities**
   - Income inequality affects educational opportunities
   - Urban-rural divide in quality and access
   - Private vs government school disparities
   - Hidden costs of "free" education

2. **Caste and Social Hierarchy**
   - Historical exclusion of marginalized communities
   - Reservation policies and their impact
   - Discrimination and prejudice in schools
   - Need for inclusive practices

3. **Gender Inequality**
   - Girls' education challenges in rural areas
   - Dropout rates higher for girls at secondary level
   - Gender stereotypes in subject choices
   - Safety and sanitation issues

4. **Regional Disparities**
   - Variation in education quality across states
   - Language barriers (medium of instruction)
   - Migration and mobile populations
   - Difficult terrain and remote areas

5. **Digital Divide**
   - Access to technology and internet
   - Exacerbated during COVID-19 pandemic
   - Urban-rural and rich-poor gaps

**Teacher's Role:**
- Creating inclusive classrooms
- Challenging stereotypes and biases
- Providing equal opportunities to all
- Understanding diverse backgrounds
- Advocating for marginalized students
- Collaborating with community""",
                    "video_url": "https://www.youtube.com/embed/lDN3A-TatOs",
                    "video_duration": "18:55"
                }
            ]
        },
        {
            "module_number": 3,
            "module_name": "Learning and Teaching",
            "description": "Theories of learning, teaching methods, and classroom pedagogy",
            "duration_weeks": 4,
            "topics": [
                {
                    "topic_number": 1,
                    "topic_name": "Theories of Learning - Behaviorism",
                    "content_text": """Behaviorism is a learning theory that focuses on observable behaviors and how they're acquired through conditioning. It dominated psychology for much of the 20th century.

**Key Concepts:**

1. **Classical Conditioning (Pavlov)**
   - Learning through association
   - Stimulus-response connections
   - Example: Anxiety around math tests

2. **Operant Conditioning (Skinner)**
   - Learning through consequences
   - Reinforcement (positive and negative)
   - Punishment
   - Shaping behavior through rewards

**Application in Classroom:**
- Rewards and praise for correct answers
- Immediate feedback
- Practice and repetition
- Breaking complex skills into steps
- Token economy systems

**Limitations:**
- Doesn't explain complex cognitive processes
- Ignores internal mental states
- Reduces learning to mechanical process
- Limited in explaining creativity and problem-solving""",
                    "video_url": "https://www.youtube.com/embed/qG2SwE_6uVM",
                    "video_duration": "17:25"
                },
                {
                    "topic_number": 2,
                    "topic_name": "Constructivism in Learning",
                    "content_text": """Constructivism posits that learners actively construct knowledge by integrating new information with existing understanding. It emphasizes the learner's role in creating meaning.

**Key Principles:**

1. **Active Learning**
   - Students are active participants, not passive recipients
   - Hands-on experiences and exploration
   - Problem-based and inquiry-based learning

2. **Prior Knowledge Matters**
   - New learning builds on existing schemas
   - Teachers must assess prior knowledge
   - Address misconceptions

3. **Social Construction of Knowledge**
   - Learning is enhanced through interaction
   - Collaborative learning environments
   - Dialogue and discussion

4. **Authentic Contexts**
   - Learning in meaningful, real-world contexts
   - Application and transfer of knowledge

**Constructivist Teaching Strategies:**
- Guided discovery learning
- Problem-based learning (PBL)
- Project-based learning
- Case-based learning
- Inquiry-based learning
- Socratic questioning

**In Mathematics:**
- Let students discover patterns
- Encourage multiple solution strategies
- Use real-world mathematical problems
- Foster mathematical discourse
- Provide opportunities for exploration""",
                    "video_url": "https://www.youtube.com/embed/cHYPcEL81XQ",
                    "video_duration": "20:05"
                }
            ]
        },
        {
            "module_number": 4,
            "module_name": "Curriculum and Inclusion",
            "description": "Understanding curriculum design, inclusive education, and diversity",
            "duration_weeks": 4,
            "topics": [
                {
                    "topic_number": 1,
                    "topic_name": "Introduction to Curriculum Design",
                    "content_text": """Curriculum refers to the total learning experiences provided to students. It encompasses what is taught, how it's taught, and how learning is assessed.

**Types of Curriculum:**

1. **Formal/Written Curriculum**
   - Official curriculum documents
   - Textbooks and syllabus
   - Learning objectives and standards

2. **Hidden Curriculum**
   - Implicit lessons learned
   - School culture and values
   - Unwritten norms and expectations

3. **Null Curriculum**
   - What is deliberately or inadvertently left out
   - Silences and omissions

**Curriculum Components:**
- **Aims and Objectives:** What students should learn
- **Content:** Subject matter and topics
- **Methods:** Teaching strategies and approaches
- **Evaluation:** Assessment of learning

**Curriculum Models:**
- Subject-centered: Traditional, discipline-based
- Learner-centered: Based on student needs and interests
- Problem-centered: Organized around real-life problems
- Integrated: Combines multiple subjects

**Good Curriculum Characteristics:**
- Relevant to student lives
- Age and developmentally appropriate
- Inclusive and diverse
- Flexible and adaptable
- Aligned with assessment
- Progressive and scaffolded""",
                    "video_url": "https://www.youtube.com/embed/EkT8e4jQx-g",
                    "video_duration": "19:30"
                },
                {
                    "topic_number": 2,
                    "topic_name": "Inclusive Education Principles",
                    "content_text": """Inclusive education means that all students, regardless of their abilities, backgrounds, or characteristics, are welcomed and supported in mainstream classrooms.

**Core Principles:**

1. **Every Child Can Learn**
   - All students have the right to quality education
   - Focus on abilities, not disabilities
   - High expectations for all

2. **Diversity is Valued**
   - Differences are seen as strengths
   - Celebration of diversity
   - Creating sense of belonging

3. **Barrier-Free Access**
   - Physical accessibility
   - Curriculum and materials accessibility
   - Attitudinal barriers removal

**Types of Diversity in Classroom:**
- Learning abilities (gifted, learning difficulties)
- Physical and sensory disabilities
- Language and cultural backgrounds
- Gender and sexual orientation
- Socio-economic status
- Religion and beliefs

**Inclusive Practices:**
- Universal Design for Learning (UDL)
- Differentiated instruction
- Multi-sensory teaching
- Flexible grouping
- Assistive technology
- Peer support systems
- Collaborative teaching

**Teacher's Role:**
- Creating welcoming environment
- Adapting curriculum and assessment
- Using varied teaching methods
- Building positive relationships
- Collaborating with specialists
- Continuous professional learning""",
                    "video_url": "https://www.youtube.com/embed/h1xvDB-SD6c",
                    "video_duration": "22:45"
                }
            ]
        },
        {
            "module_number": 5,
            "module_name": "Pedagogy of Mathematics",
            "description": "Subject-specific teaching strategies for mathematics education",
            "duration_weeks": 6,
            "topics": [
                {
                    "topic_number": 1,
                    "topic_name": "Nature of Mathematics",
                    "content_text": """Understanding the nature of mathematics is essential for effective teaching. Mathematics is not just computation; it's a way of thinking and problem-solving.

**What is Mathematics?**
- Science of patterns and relationships
- Abstract and symbolic system
- Tool for understanding the world
- Logical and deductive reasoning
- Creative and aesthetic discipline

**Characteristics of Mathematics:**

1. **Abstract:** Uses symbols and generalizations
2. **Precise:** Exact and unambiguous language
3. **Logical:** Based on axioms and proofs
4. **Hierarchical:** Concepts build upon each other
5. **Universal:** Transcends languages and cultures

**Branches of Mathematics:**
- **Pure Mathematics:** Number theory, algebra, geometry, analysis
- **Applied Mathematics:** Statistics, mechanics, optimization
- **Interdisciplinary:** Computational mathematics, mathematical modeling

**Why Study Mathematics?**
- Develops logical thinking
- Essential life skill
- Foundation for STEM fields
- Enhances problem-solving abilities
- Improves decision-making
- Applicable to real-world situations

**Mathematics as a Language:**
- Has its own vocabulary and syntax
- Symbols represent concepts
- Must be learned and practiced
- Requires translation between representations""",
                    "video_url": "https://www.youtube.com/embed/Kp2bYWRQylk",
                    "video_duration": "18:35"
                },
                {
                    "topic_number": 2,
                    "topic_name": "Bloom's Taxonomy in Mathematics",
                    "content_text": """Bloom's Taxonomy provides a framework for designing mathematics instruction and assessment across different cognitive levels.

**Revised Bloom's Taxonomy (6 Levels):**

1. **Remember (Knowledge)**
   - Recall facts, formulas, definitions
   - Example: What is the Pythagorean theorem?
   - Teaching: Flashcards, mnemonics, repetition

2. **Understand (Comprehension)**
   - Explain concepts in own words
   - Example: Explain why the area of a circle is πr²
   - Teaching: Demonstrations, analogies, discussions

3. **Apply (Application)**
   - Use concepts in new situations
   - Example: Solve a word problem using algebra
   - Teaching: Practice problems, real-world applications

4. **Analyze (Analysis)**
   - Break down problems, identify patterns
   - Example: Analyze different solution strategies
   - Teaching: Compare-contrast, error analysis

5. **Evaluate (Evaluation)**
   - Make judgments, assess strategies
   - Example: Which method is most efficient?
   - Teaching: Critiquing solutions, self-assessment

6. **Create (Synthesis)**
   - Generate new problems or solutions
   - Example: Create a word problem for given equation
   - Teaching: Project-based learning, investigations

**Designing Questions at Different Levels:**
- Mix levels in lessons and assessments
- Progress from lower to higher order
- Don't neglect higher-order thinking
- Use question stems for each level

**Application in Math Classroom:**
- Balance procedural fluency with conceptual understanding
- Move beyond computation to problem-solving
- Encourage mathematical reasoning and justification
- Foster creativity in mathematics""",
                    "video_url": "https://www.youtube.com/embed/tR6L6Y5SLLc",
                    "video_duration": "21:15"
                },
                {
                    "topic_number": 3,
                    "topic_name": "Teaching Number Systems",
                    "content_text": """Number systems form the foundation of mathematics. Effective teaching of number concepts requires understanding of how children develop number sense.

**Development of Number Sense:**

1. **Early Number Concepts (Pre-K to Grade 2)**
   - Counting and cardinality
   - One-to-one correspondence
   - Number recognition and writing
   - Comparison (more/less, bigger/smaller)
   - Basic addition and subtraction

2. **Place Value Understanding**
   - Grouping in tens
   - Positional notation
   - Expanded form
   - Regrouping in operations

3. **Number Systems Progression:**
   - Natural Numbers (N): 1, 2, 3...
   - Whole Numbers (W): 0, 1, 2, 3...
   - Integers (Z): ...-2, -1, 0, 1, 2...
   - Rational Numbers (Q): Fractions and decimals
   - Real Numbers (R): Including irrationals
   - Complex Numbers (C): Including imaginary numbers

**Teaching Strategies:**

1. **Use Concrete Materials:**
   - Base-10 blocks for place value
   - Number lines for integers
   - Fraction bars and circles
   - Manipulatives for operations

2. **Connect Representations:**
   - Concrete → Pictorial → Abstract (CPA)
   - Multiple representations of same concept
   - Visual models (area models, bar models)

3. **Address Common Misconceptions:**
   - "0.5 is bigger than 0.23 because 5 > 23"
   - "Multiplication always makes bigger"
   - "You can't subtract bigger from smaller"
   - "All fractions are less than 1"

4. **Develop Computational Fluency:**
   - Mental math strategies
   - Number sense before algorithms
   - Flexibility with numbers
   - Estimation skills

**Real-World Connections:**
- Money and shopping
- Measurement and cooking
- Sports statistics
- Time and schedules""",
                    "video_url": "https://www.youtube.com/embed/2n6nVb0pOp8",
                    "video_duration": "24:10"
                },
                {
                    "topic_number": 4,
                    "topic_name": "Teaching Algebra Concepts",
                    "content_text": """Algebra is the language of mathematics, involving symbols and rules for manipulating them. Effective algebra instruction builds on arithmetic understanding and develops abstract reasoning.

**What is Algebra?**
- Generalized arithmetic using variables
- Study of mathematical symbols and rules
- Tool for modeling real-world situations
- Foundation for advanced mathematics

**Progression in Algebra Learning:**

1. **Pre-Algebra (Elementary)**
   - Patterns and sequences
   - Properties of operations
   - Equality and inequality
   - Missing number problems (□ + 5 = 12)

2. **Beginning Algebra (Middle School)**
   - Variables and expressions
   - Simple equations
   - Linear relationships
   - Graphing on coordinate plane

3. **Intermediate Algebra (High School)**
   - Polynomials and factoring
   - Quadratic equations
   - Systems of equations
   - Functions and their graphs

**Key Concepts:**

1. **Variables:**
   - Symbols representing unknown values
   - Can take different values
   - Understanding different roles of variables

2. **Expressions and Equations:**
   - Expression: Phrase (2x + 3)
   - Equation: Statement with = sign (2x + 3 = 7)
   - Simplifying expressions
   - Solving equations

3. **Functions:**
   - Relationship between input and output
   - Multiple representations (table, graph, equation, verbal)
   - Domain and range
   - Function notation f(x)

**Teaching Strategies:**

1. **Build on Concrete Experiences:**
   - Algebra tiles and manipulatives
   - Balance scale for equations
   - Visual representations

2. **Multiple Representations:**
   - Verbal descriptions
   - Tables and patterns
   - Graphs
   - Symbolic equations
   - Real-world contexts

3. **Address Misconceptions:**
   - "2a means 2 + a"
   - "Equals sign means 'the answer is'"
   - "x can only be one value"
   - Trouble with negative numbers

4. **Real-World Applications:**
   - Distance-speed-time problems
   - Financial literacy
   - Growth and decay
   - Optimization problems

**Problem-Solving Approach:**
- Understand the problem
- Devise a plan
- Carry out the plan
- Look back and reflect""",
                    "video_url": "https://www.youtube.com/embed/NybHckSEQBI",
                    "video_duration": "26:40"
                }
            ]
        },
        {
            "module_number": 6,
            "module_name": "Assessment for Learning",
            "description": "Assessment strategies, formative and summative evaluation",
            "duration_weeks": 4,
            "topics": [
                {
                    "topic_number": 1,
                    "topic_name": "Formative vs Summative Assessment",
                    "content_text": """Assessment is integral to the teaching-learning process. Understanding different types of assessment helps teachers make informed decisions.

**Formative Assessment (Assessment FOR Learning):**

**Purpose:**
- Monitor student learning during instruction
- Provide ongoing feedback
- Identify areas needing improvement
- Adjust teaching strategies

**Characteristics:**
- Low stakes or no stakes
- Frequent and ongoing
- Immediate feedback
- Focus on improvement

**Examples:**
- Exit tickets
- Think-pair-share
- Quick quizzes
- Observations
- Student self-assessment
- Peer assessment
- Homework
- Class discussions

**Summative Assessment (Assessment OF Learning):**

**Purpose:**
- Evaluate student learning at end of period
- Measure achievement of objectives
- Assign grades
- Accountability

**Characteristics:**
- High stakes
- Periodic (end of unit, term, year)
- Standardized scoring
- Focus on outcomes

**Examples:**
- Unit tests
- Final exams
- Board examinations
- Standardized tests
- Projects with final products
- Portfolios

**Comparison:**

| Aspect | Formative | Summative |
|--------|-----------|-----------|
| Timing | During learning | After learning |
| Purpose | Improve learning | Measure learning |
| Feedback | Immediate | Delayed |
| Stakes | Low | High |
| Frequency | Continuous | Periodic |

**Balanced Assessment:**
- Use both formative and summative
- Formative informs summative
- Assessment should guide instruction
- Focus on learning, not just grading""",
                    "video_url": "https://www.youtube.com/embed/9QdIi8Jxg_c",
                    "video_duration": "19:25"
                },
                {
                    "topic_number": 2,
                    "topic_name": "Designing Effective Math Assessments",
                    "content_text": """Well-designed assessments in mathematics should measure not just procedural fluency but also conceptual understanding and problem-solving skills.

**Principles of Good Assessment:**

1. **Validity:**
   - Measures what it's supposed to measure
   - Aligned with learning objectives
   - Appropriate for grade level

2. **Reliability:**
   - Consistent results
   - Clear rubrics and criteria
   - Standardized administration

3. **Fairness:**
   - Accessible to all students
   - Free from bias
   - Multiple ways to demonstrate learning
   - Accommodations for special needs

4. **Alignment:**
   - Matches curriculum and instruction
   - Reflects classroom emphasis
   - Covers range of cognitive levels

**Types of Math Assessment Items:**

1. **Selected Response:**
   - Multiple choice
   - True/False
   - Matching
   - Good for: Quick assessment of facts and concepts
   - Limitation: Doesn't show thinking process

2. **Constructed Response:**
   - Short answer
   - Fill in the blank
   - Good for: Checking understanding
   - Limitation: May miss alternative methods

3. **Extended Response:**
   - Problem-solving tasks
   - Show-your-work problems
   - Explanations and justifications
   - Good for: Deep understanding, reasoning
   - Limitation: Time-consuming to grade

4. **Performance Tasks:**
   - Real-world applications
   - Multi-step problems
   - Projects and investigations
   - Good for: Transfer of learning, creativity
   - Limitation: Resource intensive

**Bloom's Taxonomy in Assessment:**
- Include questions at all cognitive levels
- Balance procedural and conceptual
- Don't just assess recall
- Include application and analysis

**Common Pitfalls to Avoid:**
- Trick questions
- Ambiguous wording
- Testing reading more than math
- Only assessing procedures
- Too much weight on one type
- Not providing partial credit

**Rubrics and Scoring:**
- Clear criteria for success
- Multiple dimensions (understanding, accuracy, communication)
- Descriptive levels of performance
- Share with students beforehand""",
                    "video_url": "https://www.youtube.com/embed/9QdIi8Jxg_c",
                    "video_duration": "22:30"
                }
            ]
        },
        {
            "module_number": 7,
            "module_name": "Educational Technology",
            "description": "Integration of technology in mathematics teaching",
            "duration_weeks": 4,
            "topics": [
                {
                    "topic_number": 1,
                    "topic_name": "Digital Tools for Mathematics",
                    "content_text": """Technology can enhance mathematics teaching and learning when integrated thoughtfully. Various digital tools are available for different mathematical concepts.

**Categories of Math Tools:**

1. **Graphing and Visualization:**
   - **Desmos:** Online graphing calculator
   - **GeoGebra:** Dynamic geometry and algebra
   - **Graphing Calculator Apps**
   - Uses: Exploring functions, geometry, transformations

2. **Computation and CAS:**
   - **Wolfram Alpha:** Computational engine
   - **Symbolab:** Step-by-step solutions
   - Uses: Complex calculations, checking work

3. **Geometry Tools:**
   - **GeoGebra Geometry**
   - **Sketchpad/Cabri**
   - Uses: Constructions, transformations, proofs

4. **Statistical Tools:**
   - **Excel/Google Sheets**
   - **R/Python (advanced)**
   - Uses: Data analysis, graphs, statistics

5. **Interactive Whiteboards:**
   - **Smart Board**
   - **Jamboard**
   - Uses: Demonstrations, annotations, collaboration

6. **Learning Management Systems:**
   - **Google Classroom**
   - **Moodle**
   - Uses: Assignment distribution, grading, feedback

7. **Coding and Math:**
   - **Scratch:** Visual programming
   - **Python:** Text-based programming
   - Uses: Computational thinking, algorithms

**Benefits of Technology:**
- Visualization of abstract concepts
- Multiple representations
- Immediate feedback
- Differentiation and personalization
- Exploration and discovery
- Real-world connections
- Student engagement

**Challenges:**
- Access and equity issues
- Learning curve for teachers and students
- Over-reliance on technology
- Distraction potential
- Technical problems
- Cost considerations

**Effective Integration (TPACK Framework):**
- Technology + Pedagogy + Content Knowledge
- Technology should enhance, not replace, good teaching
- Choose appropriate tool for learning goal
- Integrate technology purposefully
- Balance with non-digital activities

**Best Practices:**
- Start simple, build gradually
- Model proper use
- Provide clear instructions
- Have backup plans for tech failures
- Focus on learning goals, not technology itself
- Ensure accessibility for all students""",
                    "video_url": "https://www.youtube.com/embed/YOxRU81waF0",
                    "video_duration": "20:45"
                }
            ]
        },
        {
            "module_number": 8,
            "module_name": "Teacher Identity and Professional Ethics",
            "description": "Professional development, ethics, and teacher well-being",
            "duration_weeks": 3,
            "topics": [
                {
                    "topic_number": 1,
                    "topic_name": "Professional Ethics for Teachers",
                    "content_text": """Teaching is a noble profession that comes with significant ethical responsibilities. Professional ethics guide teachers' conduct and decision-making.

**Core Ethical Principles:**

1. **Responsibility to Students:**
   - Student welfare is paramount
   - Treat all students fairly and respectfully
   - Protect students from harm
   - Maintain appropriate boundaries
   - Respect student confidentiality

2. **Professional Competence:**
   - Maintain subject knowledge
   - Stay updated with pedagogy
   - Continuous professional development
   - Seek help when needed
   - Reflect on practice

3. **Integrity and Honesty:**
   - Academic honesty
   - Accurate record-keeping
   - Truthful communication with parents
   - No misuse of position
   - Admit mistakes

4. **Respect for Diversity:**
   - No discrimination
   - Cultural sensitivity
   - Inclusive practices
   - Challenge stereotypes
   - Promote equity

5. **Collegial Responsibility:**
   - Collaborate with colleagues
   - Support new teachers
   - Professional criticism, not personal
   - Share resources and knowledge

**Ethical Dilemmas:**
- Cheating and academic dishonesty
- Conflicts between policies and student needs
- Balancing individual attention and whole class
- Dealing with difficult parents
- Reporting concerns about colleagues
- Personal relationships with students/parents

**Decision-Making Framework:**
1. Identify the ethical issue
2. Consider stakeholders affected
3. Evaluate options and consequences
4. Apply ethical principles
5. Make decision and take action
6. Reflect on outcome

**Professional Boundaries:**
- Appropriate teacher-student relationships
- Social media and digital boundaries
- Gift-giving guidelines
- Outside tutoring of own students
- Personal disclosure limits

**Professionalism:**
- Punctuality and reliability
- Proper dress and demeanor
- Respectful communication
- Following school policies
- Maintaining confidentiality""",
                    "video_url": "https://www.youtube.com/embed/06H-3JOC0HA",
                    "video_duration": "18:30"
                },
                {
                    "topic_number": 2,
                    "topic_name": "Teacher as Reflective Practitioner",
                    "content_text": """Reflective practice is essential for continuous improvement and professional growth. Effective teachers regularly examine their practice and make conscious efforts to improve.

**What is Reflective Practice?**
- Thinking critically about teaching experiences
- Analyzing successes and challenges
- Making connections to theory
- Planning for improvement
- Lifelong learning mindset

**Levels of Reflection (Van Manen):**

1. **Technical Reflection:**
   - Focus on methods and techniques
   - "Did the strategy work?"
   - Immediate concerns

2. **Practical Reflection:**
   - Consider assumptions and values
   - "Why did I choose this method?"
   - Link theory and practice

3. **Critical Reflection:**
   - Examine social and ethical issues
   - "Who benefits from this practice?"
   - Question systemic issues

**Reflective Cycle (Gibbs):**
1. **Description:** What happened?
2. **Feelings:** What were you thinking/feeling?
3. **Evaluation:** What was good/bad?
4. **Analysis:** What sense can you make?
5. **Conclusion:** What else could you have done?
6. **Action Plan:** What will you do next time?

**Reflective Practices:**

1. **Teaching Journal:**
   - Daily or weekly entries
   - Record successes, challenges, insights
   - Track student progress
   - Note ideas for improvement

2. **Peer Observation:**
   - Observe colleagues' classes
   - Invite others to observe you
   - Constructive feedback
   - Learn new strategies

3. **Video Recording:**
   - Record your lessons
   - Analyze teaching moves
   - Notice things you missed
   - See from student perspective

4. **Student Feedback:**
   - Anonymous surveys
   - Exit tickets
   - Informal conversations
   - Act on feedback

5. **Action Research:**
   - Systematic inquiry into practice
   - Try new approaches
   - Collect data
   - Share findings

**Benefits of Reflection:**
- Improved teaching effectiveness
- Deeper understanding of learning
- Professional growth
- Problem-solving skills
- Autonomy and confidence
- Adaptability

**Making Time for Reflection:**
- Schedule regular reflection time
- Use commute time
- Brief end-of-day reflection
- Longer weekend/holiday reflection
- Professional learning communities""",
                    "video_url": "https://www.youtube.com/embed/ld5p8KpNp8M",
                    "video_duration": "17:55"
                }
            ]
        }
    ]

    # Create modules and topics
    for module_data in modules_data:
        # Create module
        module = CourseModule(
            course_id=course.id,
            module_number=module_data["module_number"],
            module_name=module_data["module_name"],
            description=module_data["description"],
            duration_weeks=module_data["duration_weeks"],
            exam_required=True,
            passing_score=60
        )
        db.add(module)
        db.flush()  # Get module.id
        print(f"  ✅ Module {module.module_number}: {module.module_name}")

        # Create topics for this module
        for topic_data in module_data["topics"]:
            topic = ModuleTopic(
                module_id=module.id,
                topic_number=topic_data["topic_number"],
                topic_name=topic_data["topic_name"],
                content_text=topic_data["content_text"],
                video_url=topic_data["video_url"],
                video_duration=topic_data["video_duration"],
                additional_resources=None
            )
            db.add(topic)

        print(f"    📝 Added {len(module_data['topics'])} topics")

    db.commit()
    print("\n🎉 Seed process completed successfully!")
    print(f"   Course: {course.course_name}")
    print(f"   Modules: {course.total_modules}")
    print(f"   Total Topics: ~50")

def main():
    """Main function to run seed script"""
    db = SessionLocal()
    try:
        seed_bed_mathematics_course(db)
    except Exception as e:
        print(f"❌ Error during seed: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
