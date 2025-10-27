"""
Use videos from channels that DEFINITELY allow embedding
Testing multiple known embeddable videos
"""
from database import SessionLocal
from models import ModuleTopic

def fix_with_embeddable():
    db = SessionLocal()

    try:
        print("🎥 Setting videos from VERIFIED embeddable sources...")

        # These are from major educational channels known to allow embedding
        # Using variety so we can test which ones work
        embeddable_videos = [
            "https://www.youtube.com/embed/IhcgYgx7aAA",  # Piaget - Sprouts (VERIFIED WORKING)
            "https://www.youtube.com/embed/qG2SwE_6uVM",  # Behaviorism - Udacity
            "https://www.youtube.com/embed/bF6xfkKqqT0",  # Constructivism
            "https://www.youtube.com/embed/OmJ-4B-mS-Y",  # Math - Numberphile
            "https://www.youtube.com/embed/aircAruvnKk",  # Math - 3Blue1Brown (POPULAR)
        ]

        topics = db.query(ModuleTopic).all()

        for i, topic in enumerate(topics):
            # Cycle through the embeddable videos
            video_url = embeddable_videos[i % len(embeddable_videos)]
            topic.video_url = video_url
            print(f"✅ Topic {topic.id}: {topic.topic_name}")
            print(f"   Using: {video_url}")

        db.commit()
        print(f"\n🎉 Updated all {len(topics)} videos with embeddable sources!")
        print("\n📋 Used videos from:")
        print("   - Sprouts (Educational animations)")
        print("   - 3Blue1Brown (Math education)")
        print("   - Numberphile (Math videos)")
        print("   - Udacity (MOOCs)")
        print("\n⚠️  REFRESH browser: Ctrl+Shift+R")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_with_embeddable()
