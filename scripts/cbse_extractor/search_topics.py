#!/usr/bin/env python3
"""
CBSE Syllabus Topic Search Tool
Interactive search for topics across all grades and subjects
"""

import sys
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

from database import SessionLocal
from models import SyllabusCache
import json

def search_topic(search_term, grade=None, subject=None, show_details=False):
    """Search for topics in the CBSE syllabus database"""

    db = SessionLocal()

    query = db.query(SyllabusCache).filter(SyllabusCache.board == 'CBSE')

    if grade:
        query = query.filter(SyllabusCache.grade == str(grade))
    if subject:
        query = query.filter(SyllabusCache.subject.ilike(f'%{subject}%'))

    entries = query.all()
    results = []

    for entry in entries:
        try:
            data = json.loads(entry.syllabus_data)
            for unit in data.get('units', []):
                for chapter in unit.get('chapters', []):

                    # Search in topics
                    topics = chapter.get('topics', [])
                    for topic in topics:
                        if search_term.lower() in topic.lower():
                            results.append({
                                'grade': entry.grade,
                                'subject': entry.subject,
                                'subject_code': data.get('subject_code', 'N/A'),
                                'unit_number': unit.get('unit_number'),
                                'unit_name': unit['unit_name'],
                                'unit_marks': unit.get('marks', 0),
                                'chapter_number': chapter.get('chapter_number'),
                                'chapter_name': chapter['chapter_name'],
                                'topic': topic,
                                'learning_outcomes': chapter.get('learning_outcomes', []),
                                'all_topics': topics
                            })

                    # Also search in chapter names
                    if search_term.lower() in chapter.get('chapter_name', '').lower():
                        if not any(r['chapter_name'] == chapter['chapter_name'] and r['grade'] == entry.grade for r in results):
                            results.append({
                                'grade': entry.grade,
                                'subject': entry.subject,
                                'subject_code': data.get('subject_code', 'N/A'),
                                'unit_number': unit.get('unit_number'),
                                'unit_name': unit['unit_name'],
                                'unit_marks': unit.get('marks', 0),
                                'chapter_number': chapter.get('chapter_number'),
                                'chapter_name': chapter['chapter_name'],
                                'topic': f"[CHAPTER MATCH: {chapter['chapter_name']}]",
                                'learning_outcomes': chapter.get('learning_outcomes', []),
                                'all_topics': topics
                            })
        except Exception as e:
            pass

    db.close()

    # Print results
    if not results:
        print(f'\n❌ No results found for "{search_term}"')
        return

    print(f'\n✅ Found {len(results)} result(s) for "{search_term}":\n')
    print('='*80)

    for i, r in enumerate(results, 1):
        print(f'\n{i}. Grade {r["grade"]} - {r["subject"]} (Code: {r["subject_code"]})')
        print(f'   Unit {r["unit_number"]}: {r["unit_name"]} ({r["unit_marks"]} marks)')
        print(f'   Chapter {r["chapter_number"]}: {r["chapter_name"]}')
        print(f'   📝 Topic: {r["topic"]}')

        if show_details:
            print(f'\n   📚 All topics in this chapter ({len(r["all_topics"])})::')
            for j, t in enumerate(r['all_topics'], 1):
                print(f'      {j}. {t}')

            if r['learning_outcomes']:
                print(f'\n   🎯 Learning Outcomes:')
                for outcome in r['learning_outcomes']:
                    print(f'      • {outcome}')

        print('-'*80)

def list_all_subjects():
    """List all available subjects"""
    db = SessionLocal()
    entries = db.query(SyllabusCache).filter(SyllabusCache.board == 'CBSE').all()

    from collections import defaultdict
    by_grade = defaultdict(list)

    for entry in entries:
        by_grade[entry.grade].append(entry.subject)

    print('\n📚 Available Subjects by Grade:')
    print('='*80)

    for grade in sorted(by_grade.keys(), key=lambda x: int(x) if x.isdigit() else 99):
        subjects = sorted(set(by_grade[grade]))
        if 'computers' in [s.lower() for s in subjects]:
            subjects = [s for s in subjects if s.lower() != 'computers']
        print(f'\nGrade {grade}:')
        for subj in subjects:
            print(f'  • {subj}')

    print('='*80)
    db.close()

def main():
    """Main CLI interface"""

    if len(sys.argv) < 2:
        print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    CBSE SYLLABUS TOPIC SEARCH TOOL                         ║
╚════════════════════════════════════════════════════════════════════════════╝

Usage:
  python3 search_topics.py "search term" [options]

Options:
  --grade <1-10>     Filter by specific grade
  --subject <name>   Filter by subject (partial match)
  --details          Show detailed information (all topics, learning outcomes)
  --list             List all available subjects

Examples:
  python3 search_topics.py "Pythagoras"
  python3 search_topics.py "Photosynthesis" --grade 7
  python3 search_topics.py "Democracy" --subject "Social Science"
  python3 search_topics.py "Quadratic" --details
  python3 search_topics.py --list

Sample Queries to Try:
  • "French Revolution"
  • "Cell"
  • "Fractions"
  • "Constitution"
  • "Pollution"
  • "Newton"
  • "Electricity"
  • "Poetry"
  • "Water cycle"
  • "Nationalism"
""")
        return

    # Check for --list
    if '--list' in sys.argv:
        list_all_subjects()
        return

    # Parse arguments
    search_term = sys.argv[1]
    grade = None
    subject = None
    show_details = False

    if '--grade' in sys.argv:
        idx = sys.argv.index('--grade')
        if idx + 1 < len(sys.argv):
            grade = sys.argv[idx + 1]

    if '--subject' in sys.argv:
        idx = sys.argv.index('--subject')
        if idx + 1 < len(sys.argv):
            subject = sys.argv[idx + 1]

    if '--details' in sys.argv:
        show_details = True

    # Perform search
    search_topic(search_term, grade, subject, show_details)

if __name__ == '__main__':
    main()
