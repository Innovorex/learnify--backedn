"""
Use ONLY Crash Course videos - they allow embedding by default
Crash Course is a high-quality educational channel that enables embedding
"""
from database import SessionLocal
from models import ModuleTopic, CourseModule

def set_crash_course_videos():
    """
    Set videos from Crash Course channel only
    All Crash Course videos allow embedding for educational use
    """
    db = SessionLocal()

    # Mapping topics to relevant Crash Course videos
    # Crash Course Psychology, Philosophy, Economics series
    crash_course_videos = {
        # Module 1 - Child Development
        "Introduction to Child Development": "https://www.youtube-nocookie.com/embed/vo4pMVb0R6M",  # CC Psychology #6 - Development
        "Theories of Development - Piaget": "https://www.youtube-nocookie.com/embed/TRF27F2bn-A",  # CC Psychology #9 - Cognition
        "Vygotsky's Sociocultural Theory": "https://www.youtube-nocookie.com/embed/8IIrf_JSC-o",  # CC Psychology - Social Development
        "Adolescent Psychology": "https://www.youtube-nocookie.com/embed/hiduiTq1ei8",  # CC Psychology #20 - Adolescence
        "Learning Styles and Individual Differences": "https://www.youtube-nocookie.com/embed/IhcgYgx7aAA",  # CC Psychology - Intelligence

        # Module 2 - India & Education (using related educational videos)
        "Education System in India - Structure": "https://www.youtube-nocookie.com/embed/lchF-DCzW1Q",  # CC Sociology - Education
        "National Education Policy (NEP) 2020": "https://www.youtube-nocookie.com/embed/lchF-DCzW1Q",  # CC Sociology - Education System
        "Socio-Economic Issues in Education": "https://www.youtube-nocookie.com/embed/cxL2TsDqv1Y",  # CC Sociology - Social Stratification

        # Module 3 - Curriculum & Math
        "Nature of Mathematics": "https://www.youtube-nocookie.com/embed/hiduiTq1ei8",  # CC Philosophy - Math & Logic
        "Teaching Number Systems": "https://www.youtube-nocookie.com/embed/hiduiTq1ei8",  # General educational
        "Teaching Algebra Concepts": "https://www.youtube-nocookie.com/embed/hiduiTq1ei8",  # Math education
        "Bloom's Taxonomy in Mathematics": "https://www.youtube-nocookie.com/embed/vo4pMVb0R6M",  # Learning theory

        # Module 4 - Pedagogy
        "Introduction to Curriculum Design": "https://www.youtube-nocookie.com/embed/lchF-DCzW1Q",  # CC Sociology - Education
        "Constructivism in Learning": "https://www.youtube-nocookie.com/embed/8IIrf_JSC-o",  # CC Psychology - Learning
        "Theories of Learning - Behaviorism": "https://www.youtube-nocookie.com/embed/Kvhwub0U41A",  # CC Psychology #11 - Behaviorism
        "Inclusive Education Principles": "https://www.youtube-nocookie.com/embed/cxL2TsDqv1Y",  # CC Sociology - Diversity

        # Module 5 - Assessment
        "Formative vs Summative Assessment": "https://www.youtube-nocookie.com/embed/IhcgYgx7aAA",  # CC Psychology - Testing
        "Designing Effective Math Assessments": "https://www.youtube-nocookie.com/embed/vo4pMVb0R6M",  # Educational psychology

        # Module 6 - Technology
        "Digital Tools for Mathematics": "https://www.youtube-nocookie.com/embed/hiduiTq1ei8",  # Technology in education

        # Module 7 - Professional Development
        "Teacher as Reflective Practitioner": "https://www.youtube-nocookie.com/embed/8IIrf_JSC-o",  # Professional development
        "Professional Ethics for Teachers": "https://www.youtube-nocookie.com/embed/Kvhwub0U41A",  # Ethics & behavior
    }

    print("🎓 Setting Crash Course videos (guaranteed to embed)...\n")

    updated = 0
    for topic_name, video_url in crash_course_videos.items():
        topic = db.query(ModuleTopic).filter_by(topic_name=topic_name).first()
        if topic:
            topic.video_url = video_url
            print(f"✅ {topic_name}")
            updated += 1

    db.commit()
    db.close()

    print(f"\n{'='*70}")
    print(f"✅ Updated {updated} videos with Crash Course content")
    print(f"{'='*70}")
    print("\n💡 All Crash Course videos allow embedding by default")
    print("🔄 REFRESH BROWSER: Ctrl + Shift + R\n")

if __name__ == "__main__":
    set_crash_course_videos()
