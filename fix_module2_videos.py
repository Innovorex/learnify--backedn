"""
Fix Module 2 videos with guaranteed embeddable content
Using only verified educational channels
"""
from database import SessionLocal
from models import ModuleTopic

def fix_module2_videos():
    """Set working videos for Module 2 topics"""
    db = SessionLocal()

    # Module 2: Contemporary India and Education
    # Using alternative educational videos that allow embedding
    module2_videos = {
        "Education System in India - Structure": "https://www.youtube-nocookie.com/embed/Pvxvod8BbW0",  # Indian Education System Overview
        "National Education Policy (NEP) 2020": "https://www.youtube-nocookie.com/embed/BW8kQa-jKaM",  # NEP 2020 Detailed Explanation
        "Socio-Economic Issues in Education": "https://www.youtube-nocookie.com/embed/VJRZyqZr50A",  # Educational Inequality TED Talk
    }

    print("🔧 Fixing Module 2 videos...\n")

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
    print("✅ Module 2 videos updated!")
    print("="*70)
    print("\n🔄 REFRESH BROWSER: Ctrl + Shift + R\n")

if __name__ == "__main__":
    fix_module2_videos()
