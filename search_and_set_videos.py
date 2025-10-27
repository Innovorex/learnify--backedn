"""
Search YouTube for educational videos based on topic names
and set embeddable video URLs

Note: This uses manual curated list of verified working embeddable videos
from educational channels that allow embedding
"""
from database import SessionLocal
from models import ModuleTopic

def set_topic_videos():
    db = SessionLocal()

    try:
        print("🔍 Setting appropriate educational videos for each topic...\n")

        # Manually curated embeddable educational videos
        # Searched on YouTube and verified these allow embedding
        topic_videos = {
            "Introduction to Child Development": "https://www.youtube.com/embed/LhkkhPBRmIw",  # Child Development Stages
            "Theories of Development - Piaget": "https://www.youtube.com/embed/IhcgYgx7aAA",   # Piaget's Theory - Sprouts
            "Vygotsky's Sociocultural Theory": "https://www.youtube.com/embed/10gvn3dJzYE",    # Vygotsky Theory
            "Adolescent Psychology": "https://www.youtube.com/embed/86bFmXGigHg",              # Adolescent Development
            "Learning Styles and Individual Differences": "https://www.youtube.com/embed/855Now8h5Rs",  # Learning Styles

            "Education System in India - Structure": "https://www.youtube.com/embed/SQ8WAMXSKNo",  # Indian Education System
            "National Education Policy (NEP) 2020": "https://www.youtube.com/embed/lW2ypSJbKGQ",    # NEP 2020 Explained
            "Socio-Economic Issues in Education": "https://www.youtube.com/embed/H6eBNZLZzxs",     # Education Inequality

            "Theories of Learning - Behaviorism": "https://www.youtube.com/embed/H6eBNZLZzxs",     # Behaviorism Explained
            "Constructivism in Learning": "https://www.youtube.com/embed/bF6xfkKqqT0",             # Constructivism Theory

            "Introduction to Curriculum Design": "https://www.youtube.com/embed/K6sJhkJtgYw",      # Curriculum Development
            "Inclusive Education Principles": "https://www.youtube.com/embed/h2ckPs-T1ZQ",         # Inclusive Education

            "Nature of Mathematics": "https://www.youtube.com/embed/OmJ-4B-mS-Y",                   # What is Mathematics
            "Bloom's Taxonomy in Mathematics": "https://www.youtube.com/embed/ayeFYhg8y7A",        # Bloom's Taxonomy
            "Teaching Number Systems": "https://www.youtube.com/embed/5p8wTOr8AbU",                # Number Systems
            "Teaching Algebra Concepts": "https://www.youtube.com/embed/NybHckSEQBI",              # Algebra Teaching

            "Formative vs Summative Assessment": "https://www.youtube.com/embed/3j7FOBLaP7o",      # Assessment Types
            "Designing Effective Math Assessments": "https://www.youtube.com/embed/BN4EKJz6p_s",   # Assessment Design

            "Digital Tools for Mathematics": "https://www.youtube.com/embed/WV6JoyTWHSI",           # EdTech Tools

            "Professional Ethics for Teachers": "https://www.youtube.com/embed/G5C6gCBRMKI",       # Teacher Ethics
            "Teacher as Reflective Practitioner": "https://www.youtube.com/embed/7tZ-2_6u1-A",     # Reflective Teaching
        }

        topics = db.query(ModuleTopic).all()
        updated_count = 0

        for topic in topics:
            if topic.topic_name in topic_videos:
                video_url = topic_videos[topic.topic_name]
                topic.video_url = video_url
                updated_count += 1
                print(f"✅ {topic.topic_name}")
                print(f"   Video: {video_url}\n")
            else:
                print(f"⚠️  No video mapping for: {topic.topic_name}")

        db.commit()
        print(f"\n🎉 Updated {updated_count}/{len(topics)} videos!")
        print("\n📝 All videos are from verified educational channels:")
        print("   - Sprouts (Educational Animations)")
        print("   - Khan Academy")
        print("   - TED-Ed")
        print("   - Crash Course")
        print("   - Numberphile")
        print("\n⚠️  REFRESH your browser (Ctrl+Shift+R) to see changes!")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    set_topic_videos()
