#!/usr/bin/env python3
"""
CORRECTED NCERT URL CATALOG
Based on actual testing of NCERT website URLs

VERIFIED Working Patterns:
- Grade 1-2: Joyful Mathematics (aejm1, bejm1)
- Grade 1-2: English Marigold (aemr1, bemr1)
- Grade 5: Hindi (ehhn1), EVS (eeen1)
- Grade 6: Ganita Prakash (fegp1), Curiosity Science (fecu1)
- Grade 7-10: Most subjects work with original patterns
- Grade 10: First Flight uses 'jeff1' not 'jefl1'
- Grade 10: Hindi books (jhks1, jhsp1, jhkr1)

NOT Available as Chapter PDFs:
- Grades 1-4: Hindi Rimjhim (only full book available)
- Grades 1-4: EVS (only full book available)
- Grade 10: Footprints without Feet, Sanchayan (limited availability)
"""

CORRECTED_NCERT_CATALOG = {
    # ==========================================================================
    # GRADE 10 - CORRECTED
    # ==========================================================================
    "10": {
        "Mathematics": {
            "pattern": "jemh1{ch:02d}",
            "chapters": 15,
            "verified": True
        },
        "Science": {
            "pattern": "jesc1{ch:02d}",
            "chapters": 13,
            "verified": True
        },
        "Social_Science": {
            "pattern": "jess1{ch:02d}",
            "chapters": 22,
            "verified": True
        },
        "English_First_Flight": {
            "pattern": "jeff1{ch:02d}",  # CORRECTED: was jefl1
            "chapters": 11,
            "verified": True
        },
        "English_Footprints": {
            "pattern": "jefp1{ch:02d}",  # May not work, needs verification
            "chapters": 10,
            "verified": False
        },
        "Hindi_Kshitij": {
            "pattern": "jhks1{ch:02d}",
            "chapters": 17,
            "verified": True
        },
        "Hindi_Kritika": {
            "pattern": "jhkr1{ch:02d}",
            "chapters": 5,
            "verified": True
        },
        "Hindi_Sparsh": {
            "pattern": "jhsp1{ch:02d}",
            "chapters": 17,
            "verified": True
        },
    },

    # ==========================================================================
    # GRADE 9
    # ==========================================================================
    "9": {
        "Mathematics": {
            "pattern": "iemh1{ch:02d}",
            "chapters": 15,
            "verified": True
        },
        "Science": {
            "pattern": "iesc1{ch:02d}",
            "chapters": 15,
            "verified": True
        },
        "Social_Science": {
            "pattern": "iess1{ch:02d}",
            "chapters": 22,
            "verified": True
        },
        "English_Beehive": {
            "pattern": "iebe1{ch:02d}",
            "chapters": 11,
            "verified": True
        },
        "English_Moments": {
            "pattern": "iemo1{ch:02d}",
            "chapters": 10,
            "verified": False
        },
        "Hindi_Kshitij": {
            "pattern": "ihks1{ch:02d}",
            "chapters": 17,
            "verified": True
        },
        "Hindi_Kritika": {
            "pattern": "ihkr1{ch:02d}",
            "chapters": 5,
            "verified": True
        },
        "Hindi_Sparsh": {
            "pattern": "ihsp1{ch:02d}",
            "chapters": 13,
            "verified": True
        },
    },

    # ==========================================================================
    # GRADE 8
    # ==========================================================================
    "8": {
        "Mathematics": {
            "pattern": "hemh1{ch:02d}",
            "chapters": 16,
            "verified": True
        },
        "Science": {
            "pattern": "hesc1{ch:02d}",
            "chapters": 18,
            "verified": True
        },
        "Social_Science": {
            "pattern": "hess1{ch:02d}",
            "chapters": 28,
            "verified": True
        },
        "English_Honeydew": {
            "pattern": "hehn1{ch:02d}",
            "chapters": 10,
            "verified": False
        },
        "Hindi_Vasant": {
            "pattern": "hhvs1{ch:02d}",
            "chapters": 18,
            "verified": True
        },
    },

    # ==========================================================================
    # GRADE 7
    # ==========================================================================
    "7": {
        "Mathematics": {
            "pattern": "gemh1{ch:02d}",
            "chapters": 15,
            "verified": True
        },
        "Science": {
            "pattern": "gesc1{ch:02d}",
            "chapters": 18,
            "verified": True
        },
        "Social_Science": {
            "pattern": "gess1{ch:02d}",
            "chapters": 28,
            "verified": True
        },
        "English_Honeycomb": {
            "pattern": "gehn1{ch:02d}",
            "chapters": 10,
            "verified": True
        },
        "Hindi_Vasant": {
            "pattern": "ghvs1{ch:02d}",
            "chapters": 20,
            "verified": True
        },
    },

    # ==========================================================================
    # GRADE 6 - CORRECTED
    # ==========================================================================
    "6": {
        "Mathematics": {
            "pattern": "fegp1{ch:02d}",  # Ganita Prakash
            "chapters": 8,
            "verified": True
        },
        "Science": {
            "pattern": "fecu1{ch:02d}",  # Curiosity
            "chapters": 12,
            "verified": True
        },
        "Social_Science": {
            "pattern": "fess1{ch:02d}",
            "chapters": 28,
            "verified": True
        },
        "English_Honeysuckle": {
            "pattern": "fehs1{ch:02d}",
            "chapters": 10,
            "verified": False
        },
        "Hindi_Vasant": {
            "pattern": "fhvs1{ch:02d}",
            "chapters": 16,
            "verified": True
        },
    },

    # ==========================================================================
    # GRADE 5 - CORRECTED
    # ==========================================================================
    "5": {
        "Mathematics": {
            "pattern": "eejm1{ch:02d}",  # CORRECTED: Joyful Math
            "chapters": 14,
            "verified": False
        },
        "English_Marigold": {
            "pattern": "eemr1{ch:02d}",
            "chapters": 10,
            "verified": False
        },
        "Hindi": {
            "pattern": "ehhn1{ch:02d}",  # VERIFIED
            "chapters": 18,
            "verified": True
        },
        "EVS": {
            "pattern": "eeen1{ch:02d}",  # VERIFIED
            "chapters": 22,
            "verified": True
        },
    },

    # ==========================================================================
    # GRADE 3-4 - CORRECTED
    # ==========================================================================
    "4": {
        "Mathematics": {
            "pattern": "dejm1{ch:02d}",  # CORRECTED: Joyful Math
            "chapters": 14,
            "verified": False
        },
        "English_Marigold": {
            "pattern": "demr1{ch:02d}",
            "chapters": 10,
            "verified": False
        },
    },
    "3": {
        "Mathematics": {
            "pattern": "cejm1{ch:02d}",  # CORRECTED: Joyful Math
            "chapters": 14,
            "verified": False
        },
        "English_Marigold": {
            "pattern": "cemr1{ch:02d}",
            "chapters": 10,
            "verified": False
        },
    },

    # ==========================================================================
    # GRADE 1-2 - CORRECTED & VERIFIED
    # ==========================================================================
    "2": {
        "Mathematics": {
            "pattern": "bejm1{ch:02d}",  # VERIFIED: Joyful Math
            "chapters": 15,
            "verified": True
        },
        "English_Marigold": {
            "pattern": "bemr1{ch:02d}",  # VERIFIED
            "chapters": 10,
            "verified": True
        },
    },
    "1": {
        "Mathematics": {
            "pattern": "aejm1{ch:02d}",  # VERIFIED: Joyful Math
            "chapters": 13,
            "verified": True
        },
        "English_Marigold": {
            "pattern": "aemr1{ch:02d}",  # VERIFIED
            "chapters": 10,
            "verified": True
        },
    },
}


def generate_url(grade, subject, chapter):
    """Generate NCERT PDF URL"""
    grade_str = str(grade)
    if grade_str not in CORRECTED_NCERT_CATALOG:
        return None
    if subject not in CORRECTED_NCERT_CATALOG[grade_str]:
        return None

    pattern = CORRECTED_NCERT_CATALOG[grade_str][subject]["pattern"]
    return f"https://ncert.nic.in/textbook/pdf/{pattern.format(ch=chapter)}.pdf"


def count_verified_chapters():
    """Count chapters with verified URLs"""
    verified = 0
    unverified = 0

    for grade, subjects in CORRECTED_NCERT_CATALOG.items():
        for subject, info in subjects.items():
            if info.get("verified", False):
                verified += info["chapters"]
            else:
                unverified += info["chapters"]

    return verified, unverified


if __name__ == "__main__":
    verified, unverified = count_verified_chapters()
    print(f"Verified working patterns: {verified} chapters")
    print(f"Unverified patterns: {unverified} chapters")
    print(f"Total: {verified + unverified} chapters")

    # Test a few
    print("\nSample URLs:")
    print(generate_url(1, "Mathematics", 1))
    print(generate_url(6, "Mathematics", 1))
    print(generate_url(10, "English_First_Flight", 1))
