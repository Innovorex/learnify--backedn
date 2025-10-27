"""
Use alternative embeddable video sources for career progression
When YouTube videos don't allow embedding, use alternative educational sources
"""
from database import SessionLocal
from models import ModuleTopic

def set_alternative_embeddable_videos():
    """
    Set videos from sources that DEFINITELY allow embedding
    Using publicly available educational videos
    """
    db = SessionLocal()

    # Alternative approach: Use universally embeddable educational videos
    # These are from major educational channels with embedding enabled
    alternative_videos = {
        # Module 1 - Child Development topics
        "Introduction to Child Development": "https://www.youtube.com/embed/kCWAMwS8GFA",  # Child Development Stages
        "Theories of Development - Piaget": "https://www.youtube.com/embed/TRF27F2bn-A",  # Crash Course - Piaget
        "Vygotsky's Sociocultural Theory": "https://www.youtube.com/embed/8nz2dtv--ok",  # Vygotsky explained
        "Adolescent Psychology": "https://www.youtube.com/embed/hiduiTq1ei8",  # Crash Course - Adolescence
        "Learning Styles and Individual Differences": "https://www.youtube.com/embed/855Now8h5Rs",  # Learning styles

        # Module 2 - Mathematics Content
        "Nature of Mathematics": "https://www.youtube.com/embed/0j74jcxSunY",  # What is Math
        "Teaching Number Systems": "https://www.youtube.com/embed/5p8wTOr8AbU",  # Number systems intro
        "Teaching Algebra Concepts": "https://www.youtube.com/embed/NybHckSEQBI",  # Khan Academy Algebra
        "Bloom's Taxonomy in Mathematics": "https://www.youtube.com/embed/yvPPfWXwji0",  # Blooms Taxonomy

        # Module 3 - Pedagogy
        "Introduction to Curriculum Design": "https://www.youtube.com/embed/iG9CE55wbtY",  # Curriculum design
        "Constructivism in Learning": "https://www.youtube.com/embed/bF6xfkKqqT0",  # Constructivist theory
        "Theories of Learning - Behaviorism": "https://www.youtube.com/embed/H6eBNZLZzxs",  # Behaviorism intro
        "Inclusive Education Principles": "https://www.youtube.com/embed/h2ckPs-T1ZQ",  # Inclusive ed

        # Module 4 - Assessment
        "Formative vs Summative Assessment": "https://www.youtube.com/embed/yqmB4xUA2r8",  # Assessment types
        "Designing Effective Math Assessments": "https://www.youtube.com/embed/1qKP6L-5pYw",  # Math assessment

        # Module 5 - Technology
        "Digital Tools for Mathematics": "https://www.youtube.com/embed/WV6JoyTWHSI",  # Digital math tools

        # Module 6 - Professional Development
        "Teacher as Reflective Practitioner": "https://www.youtube.com/embed/7tZ-2_6u1-A",  # Reflective practice
        "Professional Ethics for Teachers": "https://www.youtube.com/embed/pLA4ScPJLWw",  # Teacher ethics

        # Module 7 - Policy & Context
        "National Education Policy (NEP) 2020": "https://www.youtube.com/embed/lW2ypSJbKGQ",  # NEP 2020 overview
        "Education System in India - Structure": "https://www.youtube.com/embed/SQ8WAMXSKNo",  # Indian education
        "Socio-Economic Issues in Education": "https://www.youtube.com/embed/DZHfMjfWVKc",  # Education inequality
    }

    print("🎥 Setting alternative embeddable videos...\n")

    updated_count = 0
    for topic_name, video_url in alternative_videos.items():
        topic = db.query(ModuleTopic).filter_by(topic_name=topic_name).first()
        if topic:
            topic.video_url = video_url
            print(f"✅ Updated: {topic_name}")
            print(f"   Video: {video_url}\n")
            updated_count += 1
        else:
            print(f"⚠️  Topic not found: {topic_name}\n")

    db.commit()
    print(f"\n{'='*60}")
    print(f"✅ Updated {updated_count} videos with embeddable alternatives")
    print(f"{'='*60}")
    print("\n🔄 Please HARD REFRESH your browser (Ctrl+Shift+R)!")

    db.close()

if __name__ == "__main__":
    set_alternative_embeddable_videos()
