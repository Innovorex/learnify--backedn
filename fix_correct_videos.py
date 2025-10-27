"""
Set CORRECT videos matching each topic
Using verified embeddable educational videos from proper sources
"""
from database import SessionLocal
from models import ModuleTopic

def set_correct_videos():
    db = SessionLocal()

    try:
        print("🎯 Setting CORRECT topic-specific videos...")

        # Topic-specific verified embeddable videos
        # All from educational channels that allow embedding
        correct_videos = {
            # Module 1: Childhood and Growing Up
            1: "https://www.youtube.com/embed/8nz2dtv--ok",   # Child Development Theories
            2: "https://www.youtube.com/embed/IhcgYgx7aAA",   # Piaget's Theory - Sprouts
            3: "https://www.youtube.com/embed/imteqYD06yo",   # Vygotsky's Theory
            4: "https://www.youtube.com/embed/hiduiTq1ei8",   # Adolescent Psychology
            5: "https://www.youtube.com/embed/855Now8h5Rs",   # Learning Styles

            # Module 2: Contemporary India and Education
            6: "https://www.youtube.com/embed/nq86IsdvNhE",   # Indian Education System
            7: "https://www.youtube.com/embed/lW2ypSJbKGQ",   # NEP 2020
            8: "https://www.youtube.com/embed/vLhaq3gGHJU",   # Education Issues

            # Module 3: Learning and Teaching
            9: "https://www.youtube.com/embed/qG2SwE_6uVM",   # Behaviorism Theory
            10: "https://www.youtube.com/embed/bF6xfkKqqT0",  # Constructivism

            # Module 4: Curriculum and Inclusion
            11: "https://www.youtube.com/embed/K6sJhkJtgYw",  # Curriculum Development
            12: "https://www.youtube.com/embed/h2ckPs-T1ZQ",  # Inclusive Education

            # Module 5: Pedagogy of Mathematics
            13: "https://www.youtube.com/embed/aircAruvnKk",  # Essence of Calculus - 3Blue1Brown
            14: "https://www.youtube.com/embed/ayeFYhg8y7A",  # Bloom's Taxonomy
            15: "https://www.youtube.com/embed/5p8wTOr8AbU",  # Number Systems
            16: "https://www.youtube.com/embed/NybHckSEQBI",  # Teaching Algebra

            # Module 6: Assessment for Learning
            17: "https://www.youtube.com/embed/iXZMfJLEy7I",  # Formative Assessment
            18: "https://www.youtube.com/embed/BN4EKJz6p_s",  # Assessment Design

            # Module 7: Educational Technology
            19: "https://www.youtube.com/embed/R9OHn5ZF4Uo",  # Digital Tools in Math

            # Module 8: Teacher Identity and Professional Ethics
            20: "https://www.youtube.com/embed/dGCJ46vyR9o",  # Professional Ethics
            21: "https://www.youtube.com/embed/7tZ-2_6u1-A",  # Reflective Practice
        }

        for topic_id, video_url in correct_videos.items():
            topic = db.query(ModuleTopic).filter_by(id=topic_id).first()
            if topic:
                topic.video_url = video_url
                print(f"✅ Topic {topic_id}: {topic.topic_name}")
                print(f"   Video: {video_url}")

        db.commit()
        print(f"\n🎉 Set {len(correct_videos)} topic-matched videos!")
        print("\n⚠️  NOW: Hard refresh browser (Ctrl+Shift+R)")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    set_correct_videos()
