"""
Bulk update videos for Modules 4-8 with user-provided URLs
"""
from database import SessionLocal
from models import ModuleTopic

def update_modules_4_to_8():
    """Update all videos for modules 4-8 with user-provided URLs"""
    db = SessionLocal()

    # All user-provided video URLs for Modules 4-8
    video_updates = {
        # MODULE 4 - Curriculum & Inclusion
        "Introduction to Curriculum Design": "https://www.youtube.com/embed/QViqFtUPtbk",
        "Inclusive Education Principles": "https://www.youtube.com/embed/Z3DeUrkQtq0",

        # MODULE 5 - Pedagogy of Mathematics
        "Nature of Mathematics": "https://www.youtube.com/embed/PiLclEjqjEQ",
        "Bloom's Taxonomy in Mathematics": "https://www.youtube.com/embed/600rj1DioxA",
        "Teaching Number Systems": "https://www.youtube.com/embed/qwHJtfEUCgE",
        "Teaching Algebra Concepts": "https://www.youtube.com/embed/MHeirBPOI6w",

        # MODULE 6 - Assessment for Learning
        "Formative vs Summative Assessment": "https://www.youtube.com/embed/SxRhhGpjuzg",
        "Designing Effective Math Assessments": "https://www.youtube.com/embed/FDkR8jAJepU",

        # MODULE 7 - Educational Technology
        "Digital Tools for Mathematics": "https://www.youtube.com/embed/2C3v1vGLfmQ",

        # MODULE 8 - Teacher Identity & Professional Ethics
        "Professional Ethics for Teachers": "https://www.youtube.com/embed/m4G8OYLPUho",
        "Teacher as Reflective Practitioner": "https://www.youtube.com/embed/8eVvmyDJ5S8",
    }

    print("🎬 Updating videos for Modules 4-8...\n")
    print("="*70)

    updated_count = 0
    not_found = []

    for topic_name, video_url in video_updates.items():
        topic = db.query(ModuleTopic).filter_by(topic_name=topic_name).first()
        if topic:
            old_url = topic.video_url
            topic.video_url = video_url
            print(f"✅ {topic_name}")
            print(f"   Old: {old_url}")
            print(f"   New: {video_url}\n")
            updated_count += 1
        else:
            not_found.append(topic_name)
            print(f"❌ Topic not found: {topic_name}\n")

    db.commit()
    db.close()

    print("="*70)
    print(f"✅ Successfully updated {updated_count}/{len(video_updates)} videos!")
    if not_found:
        print(f"\n⚠️  Topics not found ({len(not_found)}):")
        for topic in not_found:
            print(f"   - {topic}")
    print("="*70)
    print("\n🔄 REFRESH BROWSER: Ctrl + Shift + R\n")

if __name__ == "__main__":
    update_modules_4_to_8()
