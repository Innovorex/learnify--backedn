"""
Update course name from "Bachelor of Education (B.Ed) - Mathematics"
to "Professional Teacher Development Program"
"""
from database import SessionLocal
from models import CareerCourse

def update_course_name():
    """Update the course name"""
    db = SessionLocal()

    # Find the B.Ed Mathematics course
    course = db.query(CareerCourse).filter(
        CareerCourse.course_name.like("%B.Ed%Mathematics%")
    ).first()

    if not course:
        # Try alternative search
        course = db.query(CareerCourse).filter(
            CareerCourse.course_type == "B.Ed"
        ).first()

    if course:
        old_name = course.course_name
        course.course_name = "Professional Teacher Development Program"
        db.commit()

        print(f"✅ Course name updated successfully!")
        print(f"   Old: {old_name}")
        print(f"   New: {course.course_name}")
        print(f"\n🔄 Refresh your browser to see the new name!")
    else:
        print("❌ Course not found!")
        # Show all courses
        all_courses = db.query(CareerCourse).all()
        print(f"\nAvailable courses ({len(all_courses)}):")
        for c in all_courses:
            print(f"  - ID: {c.id}, Name: {c.course_name}, Type: {c.course_type}")

    db.close()

if __name__ == "__main__":
    update_course_name()
