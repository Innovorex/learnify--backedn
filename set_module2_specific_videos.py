"""
Set specific videos for Module 2 as requested by user
Using the exact video URLs provided
"""
from database import SessionLocal
from models import ModuleTopic

def set_module2_specific_videos():
    """Set user-provided specific videos for Module 2"""
    db = SessionLocal()

    # User-provided specific video URLs for Module 2
    module2_videos = {
        "Education System in India - Structure": "https://www.youtube.com/embed/zSqaWMkYPyI",
        "National Education Policy (NEP) 2020": "https://www.youtube.com/embed/CYa0KIiy3Pw",
        "Socio-Economic Issues in Education": "https://www.youtube.com/embed/AM3Kqok3g_8"
    }

    print("🎯 Setting user-specified videos for Module 2...\n")

    for topic_name, video_url in module2_videos.items():
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
    print("✅ Module 2 videos updated with user-specified URLs!")
    print("="*70)
    print("\n🔄 REFRESH BROWSER: Ctrl + Shift + R\n")

if __name__ == "__main__":
    set_module2_specific_videos()
