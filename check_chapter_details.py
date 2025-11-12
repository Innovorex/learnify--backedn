"""
Check chapter details for Telangana State Board Class 1 Mathematics
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://innovorex:Innovorex%401@localhost:5432/te"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

print("=" * 80)
print("TELANGANA STATE BOARD - CLASS 1 MATHEMATICS - CHAPTER DETAILS")
print("=" * 80)

query = text("""
    SELECT
        chapter_number,
        chapter_name,
        topic_name,
        LEFT(content_text, 200) as content_preview
    FROM ncert_textbook_content
    WHERE board = 'TELANGANA'
      AND grade = 1
      AND subject ILIKE '%Mathematics%'
    ORDER BY chapter_number, id
    LIMIT 20
""")

result = session.execute(query)
rows = result.fetchall()

if rows:
    print(f"\nFound {len(rows)} content pieces:\n")
    for i, row in enumerate(rows, 1):
        print(f"{i}. Chapter {row.chapter_number}: {row.chapter_name}")
        if row.topic_name:
            print(f"   Topic: {row.topic_name}")
        print(f"   Content preview: {row.content_preview[:150]}...")
        print()
else:
    print("\n❌ No content found")

# Check CBSE Class 1 Math for comparison
print("\n" + "=" * 80)
print("CBSE - CLASS 1 MATHEMATICS - FOR COMPARISON")
print("=" * 80)

query2 = text("""
    SELECT DISTINCT
        chapter_number,
        chapter_name
    FROM ncert_textbook_content
    WHERE board = 'CBSE'
      AND grade = 1
      AND subject ILIKE '%Mathematics%'
    ORDER BY chapter_number
    LIMIT 10
""")

result2 = session.execute(query2)
rows2 = result2.fetchall()

if rows2:
    print(f"\nCBSE Class 1 Math Chapters:\n")
    for row in rows2:
        print(f"  Chapter {row.chapter_number}: {row.chapter_name}")
else:
    print("\n❌ No CBSE content found")

session.close()
print("\n" + "=" * 80)
