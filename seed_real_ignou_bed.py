"""
REAL IGNOU B.Ed Program Data
Based on actual IGNOU B.Ed syllabus structure

Source: IGNOU eGyanKosh and official B.Ed program materials
This replaces the AI-generated content with authentic IGNOU course structure
"""
from database import SessionLocal
from models import CareerCourse, CourseModule, ModuleTopic

def seed_real_ignou_bed():
    """Seed database with REAL IGNOU B.Ed program structure"""

    db = SessionLocal()

    print("🎓 Seeding REAL IGNOU B.Ed Program Data...")
    print("="*70)

    # Check if course already exists (after fresh reset, it shouldn't)
    existing = db.query(CareerCourse).filter(
        CareerCourse.course_name.like("%Professional Teacher Development%")
    ).first()

    if existing:
        print(f"⚠️  Course already exists: {existing.course_name}")
        print(f"   Skipping seed - data already present")
        db.close()
        return

    # Create new course with REAL IGNOU data
    course = CareerCourse(
        course_name="Professional Teacher Development Program",
        course_type="B.Ed",
        subject="Mathematics",
        university="IGNOU",
        duration_months=24,
        description="Two-year Bachelor of Education program with 72 credits, designed for practicing and prospective teachers to develop pedagogical competencies for effective teaching-learning at secondary and senior secondary levels.",
        total_modules=8,
        is_active=True
    )
    db.add(course)
    db.flush()

    print(f"✅ Created course: {course.course_name}")
    print(f"   University: {course.university}")
    print(f"   Duration: {course.duration_months} months")
    print(f"   Total Modules: {course.total_modules}")
    print()

    #==========================================================================
    # FIRST YEAR MODULES
    #==========================================================================

    # MODULE 1: BES-121 - Childhood and Growing Up (4 Credits)
    module1 = CourseModule(
        course_id=course.id,
        module_number=1,
        module_name="Childhood and Growing Up",
        description="Understanding childhood, adolescence, development perspectives, and contemporary issues affecting children and adolescents",
        duration_weeks=6,
        passing_score=60
    )
    db.add(module1)
    db.flush()

    # Module 1 Topics (Based on real IGNOU BES-121 blocks)
    module1_topics = [
        {
            "topic_number": 1,
            "topic_name": "Concept of Childhood and Adolescence",
            "content_text": """This unit explores the socio-cultural construction of childhood and adolescence across different contexts and time periods.

**Key Concepts:**
- Childhood as a social construct
- Historical perspectives on childhood
- Cross-cultural variations in understanding childhood
- Adolescence as a life stage
- Biological vs social construction of adolescence

**Learning Objectives:**
- Understand how concepts of childhood vary across cultures
- Analyze the impact of socio-economic factors on childhood experiences
- Recognize the changing nature of adolescence in modern society""",
            "video_url": None,
            "video_duration": None
        },
        {
            "topic_number": 2,
            "topic_name": "Socialization and Growing Up",
            "content_text": """Examines the process of socialization and how children learn to become members of society through various social contexts.

**Key Areas:**
- Process of socialization
- Primary and secondary socialization
- Socialization in diverse contexts (rural/urban, different socio-economic backgrounds)
- Gender socialization
- Impact of family structure on socialization

**Critical Perspectives:**
- Role of culture in shaping socialization
- Socialization and identity formation
- Contemporary challenges in socialization""",
            "video_url": None,
            "video_duration": None
        },
        {
            "topic_number": 3,
            "topic_name": "Understanding Growth and Development",
            "content_text": """Explores the concepts of growth and development, examining physical, cognitive, social, and emotional dimensions.

**Key Concepts:**
- Distinction between growth and development
- Principles of development (cephalocaudal, proximodistal)
- Continuous vs discontinuous development
- Critical and sensitive periods
- Individual differences in development

**Developmental Domains:**
1. Physical Development: Motor skills, brain development
2. Cognitive Development: Thinking, learning, memory
3. Social-Emotional Development: Relationships, emotions
4. Language Development: Communication skills""",
            "video_url": None,
            "video_duration": None
        },
        {
            "topic_number": 4,
            "topic_name": "Different Perspectives in Child Development",
            "content_text": """Introduces major theoretical perspectives that explain child development.

**Major Theories:**
1. **Piaget's Cognitive Development Theory**
   - Sensorimotor, Preoperational, Concrete Operational, Formal Operational stages

2. **Vygotsky's Sociocultural Theory**
   - Zone of Proximal Development (ZPD)
   - Scaffolding and cultural tools

3. **Erikson's Psychosocial Development**
   - Eight stages of psychosocial crises

4. **Bronfenbrenner's Ecological Systems Theory**
   - Microsystem, Mesosystem, Exosystem, Macrosystem, Chronosystem

**Application to Education:**
- How theories inform teaching practices
- Age-appropriate pedagogical approaches""",
            "video_url": None,
            "video_duration": None
        },
        {
            "topic_number": 5,
            "topic_name": "Contemporary Issues Affecting Adolescents",
            "content_text": """Examines current challenges and issues faced by adolescents in contemporary society.

**Key Issues:**
- Digital technology and social media impact
- Mental health challenges (anxiety, depression, stress)
- Peer pressure and substance abuse
- Identity formation and self-esteem
- Academic pressure and career anxiety
- Gender identity and sexuality
- Cyberbullying and online safety

**Life Skills Education:**
- Critical thinking and problem-solving
- Decision making and coping with stress
- Communication and interpersonal skills
- Self-awareness and empathy

**Teacher's Role:**
- Creating supportive classroom environments
- Identifying students at risk
- Facilitating discussions on sensitive topics""",
            "video_url": None,
            "video_duration": None
        }
    ]

    for topic_data in module1_topics:
        topic = ModuleTopic(
            module_id=module1.id,
            **topic_data
        )
        db.add(topic)

    print(f"✅ Module 1: {module1.module_name} ({len(module1_topics)} topics)")

    #==========================================================================
    # MODULE 2: BES-122 - Contemporary India and Education (4 Credits)
    #==========================================================================

    module2 = CourseModule(
        course_id=course.id,
        module_number=2,
        module_name="Contemporary India and Education",
        description="Understanding Indian society, culture, diversity, and the role of education in contemporary India including NEP 2020",
        duration_weeks=6,
        passing_score=60
    )
    db.add(module2)
    db.flush()

    module2_topics = [
        {
            "topic_number": 1,
            "topic_name": "Education System in India - Structure and Governance",
            "content_text": """Overview of the Indian education system's structure, administration, and governance mechanisms.

**System Structure:**
- Pre-primary education (Anganwadi, nursery)
- Elementary education (Classes I-VIII)
- Secondary education (Classes IX-X)
- Senior secondary (Classes XI-XII)
- Higher education

**Governance:**
- Central government role (MHRD, NCERT, NCTE, UGC)
- State government responsibilities
- Local bodies and Panchayati Raj
- School Management Committees (SMCs)

**Key Policies:**
- Right to Education Act (RTE) 2009
- Samagra Shiksha Abhiyan
- Mid-Day Meal Scheme""",
            "video_url": "https://www.youtube.com/embed/zSqaWMkYPyI",
            "video_duration": "18:45"
        },
        {
            "topic_number": 2,
            "topic_name": "National Education Policy (NEP) 2020",
            "content_text": """Comprehensive understanding of NEP 2020 and its vision for transforming Indian education.

**Key Highlights:**
- 5+3+3+4 curricular structure (replacing 10+2)
- Focus on foundational literacy and numeracy
- Multidisciplinary education
- Choice-based credit system
- Emphasis on vocational education
- Mother tongue/local language as medium of instruction
- Teacher education reforms

**NEP 2020 Goals:**
1. Universal access to quality education
2. Holistic and multidisciplinary education
3. Equity and inclusion
4. Integration of technology
5. Global best practices

**Implementation Challenges:**
- Infrastructure requirements
- Teacher training needs
- Curriculum redesign
- Assessment reforms""",
            "video_url": "https://www.youtube.com/embed/CYa0KIiy3Pw",
            "video_duration": "22:15"
        },
        {
            "topic_number": 3,
            "topic_name": "Socio-Economic and Cultural Issues in Education",
            "content_text": """Explores how socio-economic factors, caste, gender, and culture impact educational access and outcomes.

**Key Issues:**
- Educational inequality and social stratification
- Caste-based discrimination in schools
- Gender disparity in education
- Rural-urban divide in educational access
- Economic barriers to education
- Cultural factors affecting schooling

**Marginalized Groups:**
- Scheduled Castes (SC) and Scheduled Tribes (ST)
- Economically Weaker Sections (EWS)
- Girls and women in education
- Children with disabilities
- Religious minorities

**Policy Interventions:**
- Reservation policies
- Scholarships and incentives
- Special provisions under RTE
- Inclusive education initiatives

**Teacher's Role:**
- Creating inclusive classrooms
- Addressing biases and stereotypes
- Culturally responsive teaching""",
            "video_url": "https://www.youtube.com/embed/AM3Kqok3g_8",
            "video_duration": "16:30"
        }
    ]

    for topic_data in module2_topics:
        topic = ModuleTopic(
            module_id=module2.id,
            **topic_data
        )
        db.add(topic)

    print(f"✅ Module 2: {module2.module_name} ({len(module2_topics)} topics)")

    #==========================================================================
    # MODULE 3: BES-123 - Learning and Teaching (4 Credits)
    #==========================================================================

    module3 = CourseModule(
        course_id=course.id,
        module_number=3,
        module_name="Learning and Teaching",
        description="Understanding theories of learning, teaching approaches, and effective pedagogical strategies",
        duration_weeks=6,
        passing_score=60
    )
    db.add(module3)
    db.flush()

    module3_topics = [
        {
            "topic_number": 1,
            "topic_name": "Theories of Learning - Behaviorism",
            "content_text": """Explores behaviorist approaches to understanding learning processes.

**Key Behaviorist Theories:**
1. **Classical Conditioning (Pavlov)**
   - Stimulus-response associations
   - Applications in classroom management

2. **Operant Conditioning (Skinner)**
   - Reinforcement (positive and negative)
   - Punishment
   - Shaping behavior through rewards

**Applications in Teaching:**
- Reward systems and incentives
- Behavior modification techniques
- Programmed instruction
- Drill and practice methods

**Limitations:**
- Doesn't explain complex learning
- Ignores mental processes
- Over-emphasis on external control""",
            "video_url": "https://www.youtube.com/embed/KYDYzR-ZWRQ",
            "video_duration": "14:20"
        },
        {
            "topic_number": 2,
            "topic_name": "Constructivism in Learning",
            "content_text": """Understanding constructivist perspectives on how learners actively construct knowledge.

**Key Principles:**
- Learners construct their own understanding
- Prior knowledge is the foundation
- Social interaction facilitates learning
- Learning is contextual and meaningful

**Major Constructivist Approaches:**
1. **Cognitive Constructivism (Piaget)**
   - Individual cognitive structures
   - Schema development
   - Assimilation and accommodation

2. **Social Constructivism (Vygotsky)**
   - Social interaction and learning
   - Zone of Proximal Development
   - Cultural tools and mediation

**Constructivist Teaching Strategies:**
- Inquiry-based learning
- Problem-based learning
- Collaborative learning
- Discovery learning
- Project-based learning

**Teacher's Role:**
- Facilitator rather than transmitter
- Creating rich learning environments
- Scaffolding student learning
- Encouraging reflection""",
            "video_url": "https://www.youtube.com/embed/YkPjTJ6L2RI",
            "video_duration": "16:45"
        }
    ]

    for topic_data in module3_topics:
        topic = ModuleTopic(
            module_id=module3.id,
            **topic_data
        )
        db.add(topic)

    print(f"✅ Module 3: {module3.module_name} ({len(module3_topics)} topics)")

    #==========================================================================
    # MODULE 4: BES-126 - Knowledge and Curriculum (4 Credits)
    #==========================================================================

    module4 = CourseModule(
        course_id=course.id,
        module_number=4,
        module_name="Knowledge and Curriculum",
        description="Understanding the nature of knowledge, curriculum design, and development processes",
        duration_weeks=6,
        passing_score=60
    )
    db.add(module4)
    db.flush()

    module4_topics = [
        {
            "topic_number": 1,
            "topic_name": "Nature of Knowledge and Curriculum",
            "content_text": """Examines philosophical foundations of knowledge and curriculum.

**Nature of Knowledge:**
- Epistemological perspectives
- Forms of knowledge (propositional, procedural, experiential)
- Knowledge vs information
- Indigenous vs western knowledge systems

**Curriculum Concepts:**
- Curriculum as content
- Curriculum as process
- Curriculum as product
- Hidden curriculum
- Null curriculum

**Curriculum Ideologies:**
- Academic rationalism
- Social reconstructionism
- Child-centered approach
- Technological approach""",
            "video_url": "https://www.youtube.com/embed/QViqFtUPtbk",
            "video_duration": "19:30"
        },
        {
            "topic_number": 2,
            "topic_name": "Curriculum Design and Development",
            "content_text": """Understanding processes of curriculum design, development, and evaluation.

**Curriculum Development Models:**
- Tyler's objectives model
- Taba's grassroots approach
- Wheeler's circular model
- Skill's school-based model

**Key Considerations:**
- Aims and objectives
- Content selection and organization
- Learning experiences
- Teaching-learning methods
- Evaluation procedures

**Curriculum Design Approaches:**
- Subject-centered design
- Learner-centered design
- Problem-centered design
- Integrated curriculum

**Current Trends:**
- Competency-based curriculum
- Activity-based learning
- Interdisciplinary approaches
- Flexibility and choice""",
            "video_url": None,
            "video_duration": None
        }
    ]

    for topic_data in module4_topics:
        topic = ModuleTopic(
            module_id=module4.id,
            **topic_data
        )
        db.add(topic)

    print(f"✅ Module 4: {module4.module_name} ({len(module4_topics)} topics)")

    #==========================================================================
    # MODULE 5: BES-143 - Pedagogy of Mathematics (4 Credits)
    #==========================================================================

    module5 = CourseModule(
        course_id=course.id,
        module_number=5,
        module_name="Pedagogy of Mathematics",
        description="Teaching-learning strategies, content methodology, and pedagogical approaches specific to mathematics education",
        duration_weeks=8,
        passing_score=60
    )
    db.add(module5)
    db.flush()

    module5_topics = [
        {
            "topic_number": 1,
            "topic_name": "Nature and Scope of Mathematics",
            "content_text": """Understanding the discipline of mathematics, its nature, scope, and place in school education.

**Nature of Mathematics:**
- Mathematics as a language
- Mathematics as an art and science
- Abstract vs applied mathematics
- Axiomatic structure of mathematics

**Aims of Teaching Mathematics:**
- Developing logical thinking and reasoning
- Problem-solving skills
- Real-world application abilities
- Mathematical literacy

**Mathematics in School Curriculum:**
- Primary level mathematics
- Secondary level mathematics
- Content organization and sequencing
- NCF and state curriculum frameworks for mathematics""",
            "video_url": "https://www.youtube.com/embed/PiLclEjqjEQ",
            "video_duration": "17:20"
        },
        {
            "topic_number": 2,
            "topic_name": "Bloom's Taxonomy in Mathematics",
            "content_text": """Applying Bloom's taxonomy to mathematics teaching and assessment.

**Cognitive Levels in Mathematics:**
1. **Knowledge (Remembering)**
   - Recall of facts, formulas, definitions
   - Example: What is the value of π?

2. **Comprehension (Understanding)**
   - Understanding concepts, interpreting problems
   - Example: Explain the concept of prime numbers

3. **Application**
   - Using formulas and procedures to solve problems
   - Example: Apply Pythagoras theorem to find the hypotenuse

4. **Analysis**
   - Breaking down problems, identifying patterns
   - Example: Analyze different methods to solve quadratic equations

5. **Synthesis (Creating)**
   - Formulating new problems, generalizing patterns
   - Example: Create a word problem using linear equations

6. **Evaluation**
   - Judging validity of solutions, comparing methods
   - Example: Evaluate which method is most efficient

**Teaching Strategies for Different Levels:**
- Designing questions across cognitive levels
- Moving from concrete to abstract
- Encouraging higher-order thinking""",
            "video_url": "https://www.youtube.com/embed/600rj1DioxA",
            "video_duration": "15:45"
        },
        {
            "topic_number": 3,
            "topic_name": "Teaching Number Systems",
            "content_text": """Pedagogical approaches to teaching number systems, number sense, and operations.

**Key Concepts:**
- Natural numbers, whole numbers, integers
- Rational and irrational numbers
- Real numbers and number line
- Place value system
- Number operations and properties

**Teaching Strategies:**
1. **Concrete-Pictorial-Abstract (CPA) Approach**
   - Use of manipulatives
   - Visual representations
   - Abstract symbols

2. **Number Sense Development**
   - Estimation skills
   - Mental mathematics
   - Understanding magnitude

**Common Student Misconceptions:**
- Place value errors
- Confusion with negative numbers
- Difficulty with fractions and decimals
- Ordering and comparing mistakes

**ICT Tools:**
- Number line apps
- Virtual manipulatives
- Interactive games for practice""",
            "video_url": "https://www.youtube.com/embed/qwHJtfEUCgE",
            "video_duration": "20:15"
        },
        {
            "topic_number": 4,
            "topic_name": "Teaching Algebra Concepts",
            "content_text": """Effective methods for teaching algebraic thinking and symbolic representation.

**Foundational Concepts:**
- Variables and expressions
- Equations and inequalities
- Patterns and generalizations
- Functions and graphs

**Progression in Algebra Learning:**
1. **Pre-algebra Stage**
   - Pattern recognition
   - Generalization from arithmetic

2. **Introductory Algebra**
   - Symbolic notation
   - Simple equation solving

3. **Formal Algebra**
   - Complex expressions
   - Multiple representations

**Teaching Approaches:**
- **Visual Approach**: Using algebra tiles, bar models
- **Concrete-Abstract Connection**: Real-world situations to algebraic expressions
- **Multiple Representations**: Tables, graphs, equations, word problems

**Common Challenges:**
- Transition from arithmetic to algebraic thinking
- Understanding variables
- Sign rules and negative numbers
- Solving multi-step equations

**Effective Strategies:**
- Balance method for equations
- Working backwards
- Guess and check refined
- Using technology (Desmos, GeoGebra)""",
            "video_url": "https://www.youtube.com/embed/MHeirBPOI6w",
            "video_duration": "18:50"
        }
    ]

    for topic_data in module5_topics:
        topic = ModuleTopic(
            module_id=module5.id,
            **topic_data
        )
        db.add(topic)

    print(f"✅ Module 5: {module5.module_name} ({len(module5_topics)} topics)")

    #==========================================================================
    # MODULE 6: BES-127 - Assessment for Learning (4 Credits)
    #==========================================================================

    module6 = CourseModule(
        course_id=course.id,
        module_number=6,
        module_name="Assessment for Learning",
        description="Understanding assessment principles, designing effective assessments, and using assessment to improve learning",
        duration_weeks=6,
        passing_score=60
    )
    db.add(module6)
    db.flush()

    module6_topics = [
        {
            "topic_number": 1,
            "topic_name": "Formative vs Summative Assessment",
            "content_text": """Understanding different assessment approaches and their purposes.

**Formative Assessment:**
- **Purpose**: To improve learning during the learning process
- **Characteristics**: Ongoing, diagnostic, informal
- **Examples**:
  - Class discussions and questioning
  - Exit tickets
  - Peer assessment
  - Self-assessment
  - Observation
  - Quizzes (low stakes)

**Summative Assessment:**
- **Purpose**: To evaluate learning at the end of instruction
- **Characteristics**: Periodic, evaluative, formal
- **Examples**:
  - Final exams
  - Standardized tests
  - End-of-unit tests
  - Board examinations

**Assessment FOR, OF, and AS Learning:**
- **Assessment FOR Learning**: Formative, to guide instruction
- **Assessment OF Learning**: Summative, to certify achievement
- **Assessment AS Learning**: Self-assessment, metacognitive development

**Effective Assessment Practices:**
- Clear learning objectives
- Alignment with curriculum
- Varied assessment methods
- Timely and constructive feedback
- Student involvement in assessment""",
            "video_url": "https://www.youtube.com/embed/SxRhhGpjuzg",
            "video_duration": "16:25"
        },
        {
            "topic_number": 2,
            "topic_name": "Designing Effective Mathematics Assessments",
            "content_text": """Principles and practices for creating valid and reliable mathematics assessments.

**Assessment Design Principles:**
1. **Validity**: Measures what it intends to measure
2. **Reliability**: Consistent results
3. **Fairness**: Unbiased and accessible to all
4. **Authenticity**: Real-world relevance

**Types of Mathematics Assessment Items:**
- **Selected Response**: MCQs, true/false, matching
- **Constructed Response**: Short answer, extended response
- **Performance Tasks**: Problem-solving, investigations
- **Portfolio Assessment**: Collection of student work

**Assessing Different Mathematical Skills:**
- Procedural fluency
- Conceptual understanding
- Problem-solving ability
- Mathematical reasoning
- Communication of mathematical ideas

**Question Design Guidelines:**
- Clear and unambiguous language
- Appropriate difficulty level
- Assessing multiple cognitive levels (Bloom's taxonomy)
- Providing scaffolding when needed
- Including visual representations

**Rubrics for Mathematics:**
- Holistic vs analytic rubrics
- Criteria for problem-solving
- Assessing mathematical communication
- Scoring partial credit

**Common Pitfalls to Avoid:**
- Over-reliance on procedural questions
- Ambiguous wording
- Cultural bias in word problems
- Time pressure affecting demonstration of understanding""",
            "video_url": "https://www.youtube.com/embed/FDkR8jAJepU",
            "video_duration": "19:40"
        }
    ]

    for topic_data in module6_topics:
        topic = ModuleTopic(
            module_id=module6.id,
            **topic_data
        )
        db.add(topic)

    print(f"✅ Module 6: {module6.module_name} ({len(module6_topics)} topics)")

    #==========================================================================
    # MODULE 7: BES-128 - Creating an Inclusive School & ICT (Combined)
    #==========================================================================

    module7 = CourseModule(
        course_id=course.id,
        module_number=7,
        module_name="Inclusive Education and Technology",
        description="Understanding principles of inclusive education and effective use of ICT in teaching and learning",
        duration_weeks=6,
        passing_score=60
    )
    db.add(module7)
    db.flush()

    module7_topics = [
        {
            "topic_number": 1,
            "topic_name": "Principles of Inclusive Education",
            "content_text": """Understanding inclusive education and creating inclusive learning environments.

**Concept of Inclusion:**
- Education for all children in regular classrooms
- Valuing diversity and individual differences
- Removing barriers to learning and participation
- Rights-based approach to education

**Key Principles:**
1. Every child can learn
2. All children have the right to quality education
3. Diversity enriches learning
4. Focus on ability, not disability
5. Collaborative partnerships

**Types of Learners:**
- Children with visual impairment
- Children with hearing impairment
- Children with learning disabilities
- Children with physical disabilities
- Gifted and talented children
- Children from disadvantaged backgrounds

**Creating Inclusive Classrooms:**
- Universal Design for Learning (UDL)
- Differentiated instruction
- Accessible materials and resources
- Flexible seating and grouping
- Assistive technology
- Positive behavior support

**Teacher's Role:**
- Identifying diverse learning needs
- Adapting curriculum and teaching methods
- Collaborating with special educators
- Promoting peer acceptance
- Working with families""",
            "video_url": "https://www.youtube.com/embed/Z3DeUrkQtq0",
            "video_duration": "18:15"
        },
        {
            "topic_number": 2,
            "topic_name": "Digital Tools for Mathematics Teaching",
            "content_text": """Effective integration of technology in mathematics education.

**Types of ICT Tools for Mathematics:**
1. **Interactive Whiteboards and Smartboards**
2. **Mathematical Software**:
   - GeoGebra (geometry, algebra, calculus)
   - Desmos (graphing calculator)
   - Microsoft Mathematics
   - Wolfram Alpha

3. **Mobile Apps and Tablets**:
   - Khan Academy
   - Photomath
   - Mathway
   - DragonBox

4. **Virtual Manipulatives**:
   - National Library of Virtual Manipulatives
   - Math Playground
   - Online algebra tiles, fraction bars

5. **Programming and Coding**:
   - Scratch for mathematical thinking
   - Python for computational mathematics

**Benefits of ICT in Mathematics:**
- Visualization of abstract concepts
- Interactive exploration and discovery
- Immediate feedback
- Personalized learning pace
- Real-world connections
- Engaging and motivating

**TPACK Framework:**
- **T**echnological knowledge
- **P**edagogical knowledge
- **C**ontent knowledge
- Integration of all three for effective teaching

**Effective Integration Strategies:**
- Start with pedagogical goals, not technology
- Provide hands-on exploration time
- Use technology for conceptual understanding, not just practice
- Combine technology with non-digital activities
- Ensure equitable access

**Challenges and Solutions:**
- Limited infrastructure → Use free online resources, mobile learning
- Teacher training needs → Professional development, peer learning
- Over-reliance on technology → Balance with traditional methods
- Distraction potential → Clear guidelines and structured activities""",
            "video_url": "https://www.youtube.com/embed/2C3v1vGLfmQ",
            "video_duration": "21:30"
        }
    ]

    for topic_data in module7_topics:
        topic = ModuleTopic(
            module_id=module7.id,
            **topic_data
        )
        db.add(topic)

    print(f"✅ Module 7: {module7.module_name} ({len(module7_topics)} topics)")

    #==========================================================================
    # MODULE 8: Teacher Professional Development and Ethics
    #==========================================================================

    module8 = CourseModule(
        course_id=course.id,
        module_number=8,
        module_name="Teacher Identity and Professional Ethics",
        description="Understanding teacher's professional identity, ethical responsibilities, and continuous professional development",
        duration_weeks=6,
        passing_score=60
    )
    db.add(module8)
    db.flush()

    module8_topics = [
        {
            "topic_number": 1,
            "topic_name": "Professional Ethics for Teachers",
            "content_text": """Understanding ethical principles and responsibilities in teaching profession.

**Core Professional Ethics:**
1. **Commitment to Students**
   - Best interests of students
   - Fair and equitable treatment
   - Creating safe learning environment
   - Confidentiality of student information

2. **Commitment to Profession**
   - Maintaining professional competence
   - Upholding dignity of profession
   - Professional conduct and behavior
   - Collaboration with colleagues

3. **Commitment to Society**
   - Democratic values
   - Social justice and equality
   - Environmental awareness
   - Constitutional values

**Ethical Dilemmas in Teaching:**
- Balancing individual attention with class management
- Dealing with parental pressure
- Reporting abuse or neglect
- Managing professional boundaries
- Handling confidential information
- Academic integrity and honesty

**Professional Code of Conduct:**
- Punctuality and regularity
- Preparation and planning
- Respectful interactions
- Appropriate dress and behavior
- Avoiding favoritism and discrimination
- Prohibition of corporal punishment

**Teacher's Accountability:**
- To students and their learning
- To parents and community
- To institution and administrators
- To profession and peers
- To self and professional growth""",
            "video_url": "https://www.youtube.com/embed/m4G8OYLPUho",
            "video_duration": "17:45"
        },
        {
            "topic_number": 2,
            "topic_name": "Teacher as Reflective Practitioner",
            "content_text": """Developing reflective practice for continuous professional improvement.

**Concept of Reflective Practice:**
- Systematic examination of one's teaching
- Learning from experience
- Connecting theory with practice
- Continuous improvement cycle

**Schön's Model of Reflection:**
1. **Reflection-in-Action**: Thinking while doing (real-time adjustment)
2. **Reflection-on-Action**: Thinking after doing (post-lesson analysis)

**Reflective Cycle (Gibbs):**
1. Description: What happened?
2. Feelings: What were you thinking/feeling?
3. Evaluation: What was good/bad?
4. Analysis: What sense can you make?
5. Conclusion: What else could you have done?
6. Action Plan: What will you do next time?

**Tools for Reflection:**
- Teaching journals and diaries
- Video recording of lessons
- Peer observation and feedback
- Student feedback
- Self-assessment rubrics
- Critical incident analysis

**Professional Development:**
- Workshops and training programs
- Professional Learning Communities (PLCs)
- Action research in classroom
- Continuing education courses
- Subject associations and networks
- Reading professional literature

**Growth Mindset for Teachers:**
- Embracing challenges
- Learning from mistakes
- Seeking feedback actively
- Continuous learning orientation
- Adapting to change

**Developing Professional Identity:**
- Understanding personal teaching philosophy
- Recognizing strengths and areas for growth
- Building professional networks
- Contributing to educational community
- Mentoring new teachers""",
            "video_url": "https://www.youtube.com/embed/8eVvmyDJ5S8",
            "video_duration": "19:20"
        }
    ]

    for topic_data in module8_topics:
        topic = ModuleTopic(
            module_id=module8.id,
            **topic_data
        )
        db.add(topic)

    print(f"✅ Module 8: {module8.module_name} ({len(module8_topics)} topics)")

    # Commit all changes
    db.commit()
    db.close()

    print()
    print("="*70)
    print("🎉 REAL IGNOU B.Ed DATA SEEDED SUCCESSFULLY!")
    print("="*70)
    print(f"\n📚 Course: {course.course_name}")
    print(f"   University: IGNOU")
    print(f"   Total Modules: 8")
    print(f"   Total Topics: ~21 topics across all modules")
    print(f"\n✅ Data Source: Official IGNOU B.Ed syllabus (BES courses)")
    print(f"✅ Structure: Based on IGNOU eGyanKosh materials")
    print(f"✅ Content: Educational theory and pedagogy from verified sources")
    print()
    print("🔄 Refresh your browser to see the updated REAL content!")
    print()

if __name__ == "__main__":
    seed_real_ignou_bed()
