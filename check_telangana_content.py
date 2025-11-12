"""
Check what Telangana State Board content exists in the database
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database connection
DATABASE_URL = "postgresql://innovorex:Innovorex%401@localhost:5432/te"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

print("=" * 80)
print("TELANGANA STATE BOARD CONTENT CHECK")
print("=" * 80)

# Check what Telangana content exists for Class 1
query = text("""
    SELECT
        grade,
        subject,
        chapter_name,
        COUNT(*) as content_pieces
    FROM ncert_textbook_content
    WHERE board = 'TELANGANA'
      AND grade = 1
    GROUP BY grade, subject, chapter_name
    ORDER BY subject, chapter_name
""")

result = session.execute(query)
rows = result.fetchall()

if rows:
    print(f"\n✅ Found {len(rows)} chapters for Telangana State Board Class 1:\n")
    for row in rows:
        print(f"  • {row.subject} - {row.chapter_name} ({row.content_pieces} pieces)")
else:
    print("\n❌ No Telangana State Board content found for Class 1")

# Check all grades for Telangana
query2 = text("""
    SELECT
        grade,
        COUNT(DISTINCT subject) as subjects,
        COUNT(DISTINCT chapter_name) as chapters,
        COUNT(*) as total_pieces
    FROM ncert_textbook_content
    WHERE board = 'TELANGANA'
    GROUP BY grade
    ORDER BY grade
""")

result2 = session.execute(query2)
rows2 = result2.fetchall()

print("\n" + "=" * 80)
print("TELANGANA CONTENT BY GRADE")
print("=" * 80)

if rows2:
    for row in rows2:
        print(f"  Grade {row.grade}: {row.subjects} subjects, {row.chapters} chapters, {row.total_pieces} content pieces")
else:
    print("  No Telangana content found at all")

# Check what subjects are available for Telangana
query3 = text("""
    SELECT DISTINCT subject
    FROM ncert_textbook_content
    WHERE board = 'TELANGANA'
    ORDER BY subject
""")

result3 = session.execute(query3)
subjects = [row.subject for row in result3.fetchall()]

print("\n" + "=" * 80)
print("TELANGANA SUBJECTS AVAILABLE")
print("=" * 80)
if subjects:
    for subject in subjects:
        print(f"  • {subject}")
else:
    print("  No subjects found")

session.close()
print("\n" + "=" * 80)
