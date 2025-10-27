"""
Set specific videos for Module 3 as provided by user
"""
from database import SessionLocal
from models import ModuleTopic

def set_module3_videos():
    """Set user-provided specific videos for Module 3"""
    db = SessionLocal()

    # User-provided specific video URLs for Module 3
    module3_videos = {
        "Theories of Learning - Behaviorism": "https://www.youtube.com/embed/KYDYzR-ZWRQ",
        "Constructivism in Learning": "https://www.youtube.com/embed/YkPjTJ6L2RI"
    }

    print("🎯 Setting user-specified videos for Module 3...\n")

    for topic_name, video_url in module3_videos.items():
        topic = db.query(ModuleTopic).filter_by(topic_name=topic_name).first()
        if topic:
            old_url = topic.video_url
            topic.video_url = video_url
            print(f"✅ {topic_name}")
            print(f"   Old: {old_url}")
            print(f"   New: {video_url}\n")
        else:
            print(f"❌ Topic not found: {topic_name}\n")

    db.commit()
    db.close()

    print("="*70)
    print("✅ Module 3 videos updated!")
    print("="*70)
    print("\n🔄 REFRESH BROWSER: Ctrl + Shift + R\n")

if __name__ == "__main__":
    set_module3_videos()
