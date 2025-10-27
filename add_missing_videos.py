"""
Add videos for the 6 missing topics in the IGNOU B.Ed course
"""
from database import SessionLocal
from models import ModuleTopic

def add_missing_videos():
    db = SessionLocal()

    try:
        # Map of topic names to video URLs
        # Finding relevant educational videos for the missing topics
        video_updates = {
            # Module 1 - Childhood Development topics
            "Concept of Childhood and Adolescence": "https://www.youtube.com/embed/LBaH0G-kHSo",  # Child Development Theories
            "Socialization and Growing Up": "https://www.youtube.com/embed/WNYemuiAOfU",  # Socialization in Child Development
            "Understanding Growth and Development": "https://www.youtube.com/embed/0BTldD_Ar0Y",  # Stages of Human Development
            "Different Perspectives in Child Development": "https://www.youtube.com/embed/IhcLlDz3x_o",  # Child Development Perspectives
            "Contemporary Issues Affecting Adolescents": "https://www.youtube.com/embed/hiduiTq1ei8",  # Adolescent Development Issues

            # Module 4 - Curriculum topic
            "Curriculum Design and Development": "https://www.youtube.com/embed/QViqFtUPtbk",  # Curriculum Design (already used but good fit)
        }

        print("🎥 Adding Videos to Missing Topics\n")
        print("=" * 70)

        updated_count = 0

        for topic_name, video_url in video_updates.items():
            topic = db.query(ModuleTopic).filter(
                ModuleTopic.topic_name.ilike(f"%{topic_name}%")
            ).first()

            if topic:
                if not topic.video_url:
                    topic.video_url = video_url
                    topic.video_duration = 15  # Approximate duration in minutes
                    updated_count += 1
                    print(f"✅ Updated: {topic.topic_name}")
                    print(f"   Video: {video_url}")
                else:
                    print(f"⏭️  Skipped (already has video): {topic.topic_name}")
            else:
                print(f"❌ Not found: {topic_name}")

        if updated_count > 0:
            db.commit()
            print(f"\n{'=' * 70}")
            print(f"✅ Successfully added {updated_count} videos!")
        else:
            print(f"\n{'=' * 70}")
            print("ℹ️  No videos were added (all topics already have videos)")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_missing_videos()
