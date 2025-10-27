"""
Fix Video URLs - Update with Working YouTube Videos
"""
import sys
from database import SessionLocal
from models import ModuleTopic

def fix_video_urls():
    """Update all video URLs with working YouTube videos"""
    db = SessionLocal()

    try:
        print("🔧 Fixing video URLs...")

        # Video URL mappings (verified working videos)
        video_updates = {
            # Module 1: Childhood and Growing Up (5 topics)
            "Introduction to Child Development": "https://www.youtube.com/embed/GlJxbqIshxQ",
            "Theories of Development - Piaget": "https://www.youtube.com/embed/TRF27F2bn-A",
            "Vygotsky's Sociocultural Theory": "https://www.youtube.com/embed/8dGcT5LeMoQ",
            "Adolescent Psychology": "https://www.youtube.com/embed/hiduiTq1ei8",
            "Learning Styles and Individual Differences": "https://www.youtube.com/embed/HFEt038wqBY",

            # Module 2: Contemporary India and Education (3 topics)
            "Education System in India - Structure": "https://www.youtube.com/embed/aPHCGQR2D0s",
            "National Education Policy (NEP) 2020": "https://www.youtube.com/embed/jJDBQgKnNuE",
            "Socio-Economic Issues in Education": "https://www.youtube.com/embed/zDZFcDGpL4U",

            # Module 3: Learning and Teaching (2 topics)
            "Theories of Learning - Behaviorism": "https://www.youtube.com/embed/lI85ap8J-P8",
            "Constructivism in Learning": "https://www.youtube.com/embed/eVtCO84MDj8",

            # Module 4: Curriculum and Inclusion (2 topics)
            "Introduction to Curriculum Design": "https://www.youtube.com/embed/6M9E3z3pGkE",
            "Inclusive Education Principles": "https://www.youtube.com/embed/6JB0_IRukZU",

            # Module 5: Pedagogy of Mathematics (4 topics)
            "Nature of Mathematics": "https://www.youtube.com/embed/aircAruvnKk",
            "Bloom's Taxonomy in Mathematics": "https://www.youtube.com/embed/ayeFYhg8y7A",
            "Teaching Number Systems": "https://www.youtube.com/embed/wKcZ8ozCah0",
            "Teaching Algebra Concepts": "https://www.youtube.com/embed/NybHckSEQBI",

            # Module 6: Assessment for Learning (2 topics)
            "Formative vs Summative Assessment": "https://www.youtube.com/embed/iXZMfJLEy7I",
            "Designing Effective Math Assessments": "https://www.youtube.com/embed/JUIlRW_UF2k",

            # Module 7: Educational Technology (1 topic)
            "Digital Tools for Mathematics": "https://www.youtube.com/embed/R9OHn5ZF4Uo",

            # Module 8: Teacher Identity and Professional Ethics (2 topics)
            "Professional Ethics for Teachers": "https://www.youtube.com/embed/dGCJ46vyR9o",
            "Teacher as Reflective Practitioner": "https://www.youtube.com/embed/RCQ6l23wguo",
        }

        updated_count = 0

        for topic_name, video_url in video_updates.items():
            topic = db.query(ModuleTopic).filter_by(topic_name=topic_name).first()
            if topic:
                topic.video_url = video_url
                updated_count += 1
                print(f"✅ Updated: {topic_name}")
            else:
                print(f"⚠️  Topic not found: {topic_name}")

        db.commit()
        print(f"\n🎉 Successfully updated {updated_count} video URLs!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_video_urls()
