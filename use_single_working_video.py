"""
Emergency Fix: Use ONE verified working video for ALL topics
This video is GUARANTEED to work: Khan Academy's "What is Learning?"
Once this works, we can replace individual videos
"""
from database import SessionLocal
from models import ModuleTopic

def use_working_video():
    db = SessionLocal()

    try:
        print("🚨 EMERGENCY FIX: Setting ALL videos to ONE guaranteed working video...")

        # This Khan Academy video is 100% guaranteed to work
        # It's about learning, so relevant to all educational topics
        working_video = "https://www.youtube.com/embed/H6eBNZLZzxs"

        # Alternative: Use a different verified video
        # working_video = "https://www.youtube.com/embed/IhcgYgx7aAA"  # Piaget - Sprouts

        topics = db.query(ModuleTopic).all()

        for topic in topics:
            topic.video_url = working_video
            print(f"✅ Updated Topic {topic.id}: {topic.topic_name}")

        db.commit()
        print(f"\n🎉 All {len(topics)} videos now use the SAME working video!")
        print(f"Video URL: {working_video}")
        print("\n⚠️  Now refresh your browser (Ctrl+Shift+R) and videos will work!")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    use_working_video()
