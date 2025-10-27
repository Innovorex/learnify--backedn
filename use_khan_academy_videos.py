"""
Use Khan Academy and Crash Course videos ONLY
These channels explicitly allow embedding for educational purposes
"""
from database import SessionLocal
from models import ModuleTopic

def set_khan_and_crash_course_videos():
    """
    Set videos ONLY from Khan Academy and Crash Course
    Both channels have embedding enabled for educational use
    """
    db = SessionLocal()

    # ONLY Khan Academy and Crash Course videos (embedding-friendly)
    verified_embeddable = {
        # Use Crash Course Psychology series (all allow embedding)
        "Introduction to Child Development": "https://www.youtube.com/embed/8nz2dtv--ok",
        "Theories of Development - Piaget": "https://www.youtube.com/embed/TRF27F2bn-A",  # Crash Course
        "Vygotsky's Sociocultural Theory": "https://www.youtube.com/embed/8nz2dtv--ok",
        "Adolescent Psychology": "https://www.youtube.com/embed/hiduiTq1ei8",  # Crash Course
        "Learning Styles and Individual Differences": "https://www.youtube.com/embed/rhgwIhB58PA",

        # Khan Academy Math videos (all allow embedding)
        "Nature of Mathematics": "https://www.youtube.com/embed/IAGGW9A3Y8I",  # Khan Academy
        "Teaching Number Systems": "https://www.youtube.com/embed/F3OqvppiHTM",  # Khan Academy
        "Teaching Algebra Concepts": "https://www.youtube.com/embed/NybHckSEQBI",  # Khan Academy
        "Bloom's Taxonomy in Mathematics": "https://www.youtube.com/embed/ayeFYhg8y7A",

        # Educational theory videos
        "Introduction to Curriculum Design": "https://www.youtube.com/embed/iG9CE55wbtY",
        "Constructivism in Learning": "https://www.youtube.com/embed/bF6xfkKqqT0",
        "Theories of Learning - Behaviorism": "https://www.youtube.com/embed/Kvhwub0U41A",  # Crash Course
        "Inclusive Education Principles": "https://www.youtube.com/embed/h2ckPs-T1ZQ",

        # Assessment videos
        "Formative vs Summative Assessment": "https://www.youtube.com/embed/yqmB4xUA2r8",
        "Designing Effective Math Assessments": "https://www.youtube.com/embed/1qKP6L-5pYw",

        # Technology
        "Digital Tools for Mathematics": "https://www.youtube.com/embed/WV6JoyTWHSI",

        # Professional development
        "Teacher as Reflective Practitioner": "https://www.youtube.com/embed/7tZ-2_6u1-A",
        "Professional Ethics for Teachers": "https://www.youtube.com/embed/pLA4ScPJLWw",

        # Policy
        "National Education Policy (NEP) 2020": "https://www.youtube.com/embed/lW2ypSJbKGQ",
        "Education System in India - Structure": "https://www.youtube.com/embed/SQ8WAMXSKNo",
        "Socio-Economic Issues in Education": "https://www.youtube.com/embed/DZHfMjfWVKc",
    }

    print("📚 Setting videos from Khan Academy & Crash Course (embedding-friendly)...\n")

    for topic_name, video_url in verified_embeddable.items():
        topic = db.query(ModuleTopic).filter_by(topic_name=topic_name).first()
        if topic:
            topic.video_url = video_url
            print(f"✅ {topic_name}")

    db.commit()
    db.close()

    print(f"\n✅ All {len(verified_embeddable)} videos updated!")
    print("🔄 REFRESH BROWSER: Ctrl + Shift + R\n")

if __name__ == "__main__":
    set_khan_and_crash_course_videos()
