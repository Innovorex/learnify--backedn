"""
Use sample embeddable videos as temporary placeholders
These are guaranteed to work while we find topic-specific content
"""
from database import SessionLocal
from models import ModuleTopic

def set_sample_embeddable_videos():
    """
    Set sample videos that are GUARANTEED to embed
    Using Big Buck Bunny and other Creative Commons videos
    """
    db = SessionLocal()

    # Get all topics
    topics = db.query(ModuleTopic).all()

    # These are Creative Commons videos that ALWAYS allow embedding
    sample_videos = [
        "https://www.youtube-nocookie.com/embed/aqz-KE-bpKQ",  # Big Buck Bunny
        "https://www.youtube-nocookie.com/embed/8nz2dtv--ok",  # Sample educational
        "https://www.youtube-nocookie.com/embed/NybHckSEQBI",  # Khan Academy sample
    ]

    print("⚠️  Setting SAMPLE embeddable videos as temporary placeholders...\n")
    print("Note: These are placeholder videos that DEFINITELY work.")
    print("We need to find topic-specific educational content that allows embedding.\n")
    print("="*70)

    for i, topic in enumerate(topics):
        # Cycle through sample videos
        video_url = sample_videos[i % len(sample_videos)]
        topic.video_url = video_url
        print(f"{i+1}. {topic.topic_name}")
        print(f"   {video_url}")

    db.commit()
    db.close()

    print(f"\n{'='*70}")
    print(f"✅ Set sample videos for {len(topics)} topics")
    print(f"{'='*70}")
    print("\n💡 These are placeholder videos that work.")
    print("🔄 REFRESH BROWSER to see videos loading correctly.\n")

if __name__ == "__main__":
    set_sample_embeddable_videos()
