#!/usr/bin/env python3
"""
Estimate remaining NCERT content to extract based on official CBSE curriculum
"""

# COMPLETE NCERT TEXTBOOK CATALOG (Based on official NCERT/CBSE curriculum)
# Source: ncert.nic.in textbook listings

COMPLETE_NCERT_CATALOG = {
    "Grade 10": {
        "Mathematics": 15,
        "Science": 16,
        "Social_Science": 22,  # Integrated (History + Geography + Political Science + Economics)
        "English_First_Flight": 11,
        "English_Footprints": 10,
        "Hindi_Kshitij": 17,
        "Hindi_Kritika": 5,
        "Hindi_Sparsh": 17,
        "Hindi_Sanchayan": 3,
    },
    "Grade 9": {
        "Mathematics": 15,
        "Science": 15,
        "Social_Science": 22,  # Integrated
        "English_Beehive": 11,
        "English_Moments": 10,
        "Hindi_Kshitij": 17,
        "Hindi_Kritika": 5,
        "Hindi_Sparsh": 13,
        "Hindi_Sanchayan": 3,
    },
    "Grade 8": {
        "Mathematics": 16,
        "Science": 18,
        "Social_Science": 22,  # Integrated
        "English_Honeydew": 10,
        "English_It_So_Happened": 10,
        "Hindi_Vasant": 18,
        "Hindi_Durva": 18,
        "Hindi_Bharat_Ki_Khoj": 11,
    },
    "Grade 7": {
        "Mathematics": 15,
        "Science": 18,
        "Social_Science": 22,  # Integrated
        "English_Honeycomb": 10,
        "English_An_Alien_Hand": 10,
        "Hindi_Vasant": 20,
        "Hindi_Durva": 15,
        "Hindi_Mahabharat": 10,
    },
    "Grade 6": {
        "Mathematics": 14,
        "Science": 16,
        "Social_Science": 22,  # Integrated
        "English_Honeysuckle": 10,
        "English_A_Pact_with_the_Sun": 10,
        "Hindi_Vasant": 16,
        "Hindi_Durva": 28,
        "Hindi_Bal_Ram_Katha": 12,
    },
    "Grade 5": {
        "Mathematics": 14,
        "EVS_Looking_Around": 22,
        "English_Marigold": 10,
        "Hindi_Rimjhim": 18,
    },
    "Grade 4": {
        "Mathematics": 14,
        "EVS": 22,
        "English_Marigold": 10,
        "Hindi_Rimjhim": 14,
    },
    "Grade 3": {
        "Mathematics": 14,
        "EVS": 24,
        "English_Marigold": 10,
        "Hindi_Rimjhim": 14,
    },
    "Grade 2": {
        "Mathematics": 15,
        "EVS": 21,
        "English_Marigold": 10,
        "Hindi_Rimjhim": 14,
    },
    "Grade 1": {
        "Mathematics": 13,
        "EVS": 22,
        "English_Marigold": 10,
        "Hindi_Rimjhim": 23,
    },
}

# What we CURRENTLY have extracted (485 chapters)
CURRENT_EXTRACTION = {
    "Grade 10": {
        "Mathematics": 15,
        "Science": 16,
        "Social_Science": 7,  # Partial
        "Hindi_Kritika": 2,  # Partial
        "Hindi_Sparsh": 17,  # NEW: Complete (10 earlier + 14 new + overlaps)
    },
    "Grade 9": {
        "Mathematics": 15,
        "Science": 15,
        "Social_Science": 6,  # Partial
        "English_Beehive": 8,  # Partial
        "Hindi_Kritika": 3,  # Partial
        "Hindi_Sparsh": 17,  # NEW: Partial (earlier + 10 new)
        "Hindi_Kshitij": 13,  # NEW: Complete
    },
    "Grade 8": {
        "Mathematics": 16,
        "Science": 18,
        "Hindi_Vasant": 13,  # NEW: Partial
        "Hindi_Bharat_Ki_Khoj": 9,  # Partial
    },
    "Grade 7": {
        "Mathematics": 15,
        "Science": 18,
        "English_Honeycomb": 10,
        "English_An_Alien_Hand": 10,
        "Social_Science": 8,  # Partial
        "Hindi_Vasant": 15,  # NEW: Partial
    },
    "Grade 6": {
        "Mathematics": 14,
        "Science": 16,
    },
    "Grade 5": {
        "Mathematics": 8,  # Partial
        "EVS_Looking_Around": 22,  # Complete
        "EVS_Aaspass": 22,  # Hindi version (additional)
    },
    "Grade 4": {
        "Mathematics": 14,
        "EVS": 22,  # Complete (10 English + 22 Hindi)
    },
    "Grade 3": {
        "Mathematics": 13,
        "EVS": 24,  # Complete (12 English + additional Hindi)
    },
    "Grade 2": {
        "Mathematics": 11,
        "English_Marigold": 13,  # NEW: Complete
    },
    "Grade 1": {
        "Mathematics": 13,
        "English_Marigold": 9,  # NEW: Partial
    },
}

def calculate_remaining():
    """Calculate what's remaining to extract"""

    total_available = 0
    total_extracted = 0
    remaining_by_grade = {}

    print("="*80)
    print("NCERT EXTRACTION GAP ANALYSIS")
    print("="*80)
    print()

    for grade in sorted(COMPLETE_NCERT_CATALOG.keys(), key=lambda x: int(x.split()[1])):
        available = COMPLETE_NCERT_CATALOG[grade]
        extracted = CURRENT_EXTRACTION.get(grade, {})

        grade_total_available = sum(available.values())
        grade_total_extracted = sum(extracted.values())
        grade_remaining = grade_total_available - grade_total_extracted

        total_available += grade_total_available
        total_extracted += grade_total_extracted

        print(f"{grade}:")
        print(f"  Available: {grade_total_available} chapters")
        print(f"  Extracted: {grade_total_extracted} chapters")
        print(f"  Remaining: {grade_remaining} chapters")

        # Show what's missing
        missing = []
        for subject, count in available.items():
            extracted_count = extracted.get(subject, 0)
            if extracted_count < count:
                missing.append(f"{subject} ({count - extracted_count}/{count})")

        if missing:
            print(f"  Missing: {', '.join(missing)}")
        print()

        remaining_by_grade[grade] = grade_remaining

    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total Available: {total_available} chapters")
    print(f"Total Extracted: {total_extracted} chapters")
    print(f"Total Remaining: {total_available - total_extracted} chapters")
    print(f"Completion: {(total_extracted/total_available)*100:.1f}%")
    print("="*80)
    print()

    # Priority extraction targets
    print("="*80)
    print("HIGH PRIORITY TARGETS (Subjects with large gaps)")
    print("="*80)

    priorities = []
    for grade in COMPLETE_NCERT_CATALOG:
        available = COMPLETE_NCERT_CATALOG[grade]
        extracted = CURRENT_EXTRACTION.get(grade, {})

        for subject, total in available.items():
            extracted_count = extracted.get(subject, 0)
            missing = total - extracted_count
            if missing > 0:
                priorities.append((missing, grade, subject, total, extracted_count))

    # Sort by missing count (descending)
    priorities.sort(reverse=True)

    for missing, grade, subject, total, extracted in priorities[:15]:
        print(f"{grade} - {subject}: {missing} chapters missing (have {extracted}/{total})")

    print()

if __name__ == "__main__":
    calculate_remaining()
