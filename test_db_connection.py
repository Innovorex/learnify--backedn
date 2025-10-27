import asyncio
import asyncpg

async def test_connection():
    try:
        # Test with individual parameters
        print("Testing connection with individual parameters...")
        conn = await asyncpg.connect(
            host="127.0.0.1",
            port=5432,
            user="innovorex",
            password="Innovorex@1",
            database="ai_assessment"
        )
        print("✓ Connected successfully!")

        # Test query
        rows = await conn.fetch("SELECT COUNT(*) FROM syllabus_master WHERE board='CBSE'")
        print(f"✓ Found {rows[0]['count']} CBSE syllabi")

        # Test actual query
        rows = await conn.fetch("""
            SELECT t.chapter_name, t.topic_name
            FROM syllabus_topics t
            JOIN syllabus_master m ON t.syllabus_id = m.id
            WHERE m.board = 'CBSE'
                AND m.class_name = '8'
                AND m.subject = 'Mathematics'
                AND m.is_active = true
            LIMIT 5
        """)
        print(f"✓ Found {len(rows)} topics for Grade 8 Math:")
        for row in rows:
            print(f"  - {row['chapter_name']}")

        await conn.close()
        print("✓ Connection closed")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test_connection())
