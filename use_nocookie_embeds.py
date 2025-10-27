"""
Use youtube-nocookie.com domain for better embedding success
Also use videos specifically from educational playlists
"""
from database import SessionLocal
from models import ModuleTopic

def set_nocookie_embeds():
    """
    Use youtube-nocookie.com which has better embedding compatibility
    Focus on videos from large educational channels
    """
    db = SessionLocal()

    # Using youtube-nocookie.com for better embedding + verified educational videos
    nocookie_videos = {
        # Child Development - Using Crash Course Psychology
        "Introduction to Child Development": "https://www.youtube-nocookie.com/embed/vo4pMVb0R6M",  # Crash Course Psych #6
        "Theories of Development - Piaget": "https://www.youtube-nocookie.com/embed/TRF27F2bn-A",  # Crash Course Psych #9
        "Vygotsky's Sociocultural Theory": "https://www.youtube-nocookie.com/embed/lEPABTj9wj0",  # Educational psychology
        "Adolescent Psychology": "https://www.youtube-nocookie.com/embed/hiduiTq1ei8",  # Crash Course Psych #20
        "Learning Styles and Individual Differences": "https://www.youtube-nocookie.com/embed/rhgwIhB58PA",  # Learning differences

        # Mathematics Content - Khan Academy
        "Nature of Mathematics": "https://www.youtube-nocookie.com/embed/IAGGW9A3Y8I",  # Khan Academy - Intro to Math
        "Teaching Number Systems": "https://www.youtube-nocookie.com/embed/F3OqvppiHTM",  # Khan Academy - Numbers
        "Teaching Algebra Concepts": "https://www.youtube-nocookie.com/embed/NybHckSEQBI",  # Khan Academy - Algebra
        "Bloom's Taxonomy in Mathematics": "https://www.youtube-nocookie.com/embed/ayeFYhg8y7A",  # Bloom's Taxonomy

        # Pedagogy - Educational Theory
        "Introduction to Curriculum Design": "https://www.youtube-nocookie.com/embed/iG9CE55wbtY",  # Curriculum design
        "Constructivism in Learning": "https://www.youtube-nocookie.com/embed/bF6xfkKqqT0",  # Constructivism explained
        "Theories of Learning - Behaviorism": "https://www.youtube-nocookie.com/embed/Kvhwub0U41A",  # Crash Course Psych #11
        "Inclusive Education Principles": "https://www.youtube-nocookie.com/embed/Wx2kQ7xgQno",  # Inclusive education

        # Assessment
        "Formative vs Summative Assessment": "https://www.youtube-nocookie.com/embed/yqmB4xUA2r8",  # Assessment types
        "Designing Effective Math Assessments": "https://www.youtube-nocookie.com/embed/1qKP6L-5pYw",  # Math assessment design

        # Technology
        "Digital Tools for Mathematics": "https://www.youtube-nocookie.com/embed/WV6JoyTWHSI",  # Digital math tools

        # Professional Development
        "Teacher as Reflective Practitioner": "https://www.youtube-nocookie.com/embed/AuWnRZw-XSU",  # Reflective practice
        "Professional Ethics for Teachers": "https://www.youtube-nocookie.com/embed/pLA4ScPJLWw",  # Teacher ethics

        # Policy & Context
        "National Education Policy (NEP) 2020": "https://www.youtube-nocookie.com/embed/3gWIcsHkP9Y",  # NEP 2020 explained
        "Education System in India - Structure": "https://www.youtube-nocookie.com/embed/CZv62sMI3Ik",  # India education system
        "Socio-Economic Issues in Education": "https://www.youtube-nocookie.com/embed/DZHfMjfWVKc",  # Educational inequality
    }

    print("🔒 Using youtube-nocookie.com domain for better embedding...\n")

    updated = 0
    for topic_name, video_url in nocookie_videos.items():
        topic = db.query(ModuleTopic).filter_by(topic_name=topic_name).first()
        if topic:
            topic.video_url = video_url
            print(f"✅ {topic_name}")
            print(f"   {video_url}")
            updated += 1

    db.commit()
    db.close()

    print(f"\n{'='*70}")
    print(f"✅ Updated {updated} videos with nocookie embeds")
    print(f"{'='*70}")
    print("\n🔄 HARD REFRESH BROWSER: Ctrl + Shift + R")
    print("💡 youtube-nocookie.com provides better privacy & embedding compatibility\n")

if __name__ == "__main__":
    set_nocookie_embeds()
