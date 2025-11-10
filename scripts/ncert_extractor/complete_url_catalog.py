#!/usr/bin/env python3
"""
Complete NCERT URL Catalog - ALL Subjects Grades 1-10
Based on actual NCERT textbook URL patterns from ncert.nic.in

URL Pattern Structure: https://ncert.nic.in/textbook/pdf/{code}{chapter}.pdf
Where code format is: [grade_letter][subject_code][version][volume]

Grade Letters:
a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10

Subject Codes:
- e = English, h = Hindi, m = Mathematics/Math
- sc = Science, ss = Social Science, ev = EVS
- Various book-specific codes for literature

Examples:
- jemh101.pdf = Grade 10 (j) English Medium (e) Mathematics (mh) Volume 1, Chapter 01
- aehr101.pdf = Grade 1 (a) English Medium (e) Hindi (h) Rimjhim (r) Volume 1, Chapter 01
"""

COMPLETE_NCERT_CATALOG = {
    # ============================================================================
    # GRADE 10
    # ============================================================================
    "10": {
        "Mathematics": {
            "pattern": "jemh1{ch:02d}",  # jemh101-jemh115
            "chapters": 15,
            "book": "Mathematics"
        },
        "Science": {
            "pattern": "jesc1{ch:02d}",  # jesc101-jesc113
            "chapters": 13,
            "book": "Science"
        },
        "Social_Science": {
            "pattern": "jess1{ch:02d}",  # jess101-jess122
            "chapters": 22,
            "book": "Democratic Politics, Economics, History, Geography"
        },
        "English_First_Flight": {
            "pattern": "jefl1{ch:02d}",  # jefl101-jefl111
            "chapters": 11,
            "book": "First Flight"
        },
        "English_Footprints": {
            "pattern": "jefp1{ch:02d}",  # jefp101-jefp110
            "chapters": 10,
            "book": "Footprints without Feet (Supplementary)"
        },
        "Hindi_Kshitij": {
            "pattern": "jhks1{ch:02d}",  # jhks101-jhks117
            "chapters": 17,
            "book": "Kshitij"
        },
        "Hindi_Kritika": {
            "pattern": "jhkr1{ch:02d}",  # jhkr101-jhkr105
            "chapters": 5,
            "book": "Kritika (Supplementary)"
        },
        "Hindi_Sparsh": {
            "pattern": "jhsp1{ch:02d}",  # jhsp101-jhsp117
            "chapters": 17,
            "book": "Sparsh (Course B)"
        },
        "Hindi_Sanchayan": {
            "pattern": "jhsa1{ch:02d}",  # jhsa101-jhsa103
            "chapters": 3,
            "book": "Sanchayan (Supplementary)"
        },
    },

    # ============================================================================
    # GRADE 9
    # ============================================================================
    "9": {
        "Mathematics": {
            "pattern": "iemh1{ch:02d}",  # iemh101-iemh115
            "chapters": 15,
            "book": "Mathematics"
        },
        "Science": {
            "pattern": "iesc1{ch:02d}",  # iesc101-iesc115
            "chapters": 15,
            "book": "Science"
        },
        "Social_Science": {
            "pattern": "iess1{ch:02d}",  # iess101-iess122
            "chapters": 22,
            "book": "India and the Contemporary World, Economics"
        },
        "English_Beehive": {
            "pattern": "iebe1{ch:02d}",  # iebe101-iebe111
            "chapters": 11,
            "book": "Beehive"
        },
        "English_Moments": {
            "pattern": "iemo1{ch:02d}",  # iemo101-iemo110
            "chapters": 10,
            "book": "Moments (Supplementary)"
        },
        "Hindi_Kshitij": {
            "pattern": "ihks1{ch:02d}",  # ihks101-ihks117
            "chapters": 17,
            "book": "Kshitij"
        },
        "Hindi_Kritika": {
            "pattern": "ihkr1{ch:02d}",  # ihkr101-ihkr105
            "chapters": 5,
            "book": "Kritika (Supplementary)"
        },
        "Hindi_Sparsh": {
            "pattern": "ihsp1{ch:02d}",  # ihsp101-ihsp113
            "chapters": 13,
            "book": "Sparsh (Course B)"
        },
        "Hindi_Sanchayan": {
            "pattern": "ihsa1{ch:02d}",  # ihsa101-ihsa103
            "chapters": 3,
            "book": "Sanchayan (Supplementary)"
        },
    },

    # ============================================================================
    # GRADE 8
    # ============================================================================
    "8": {
        "Mathematics": {
            "pattern": "hemh1{ch:02d}",  # hemh101-hemh116
            "chapters": 16,
            "book": "Mathematics"
        },
        "Science": {
            "pattern": "hesc1{ch:02d}",  # hesc101-hesc118
            "chapters": 18,
            "book": "Science"
        },
        "Social_Science": {
            "pattern": "hess1{ch:02d}",  # hess101-hess128
            "chapters": 28,
            "book": "Resources and Development, Social and Political Life"
        },
        "English_Honeydew": {
            "pattern": "hehn1{ch:02d}",  # hehn101-hehn110
            "chapters": 10,
            "book": "Honeydew"
        },
        "English_It_So_Happened": {
            "pattern": "heih1{ch:02d}",  # heih101-heih110
            "chapters": 10,
            "book": "It So Happened (Supplementary)"
        },
        "Hindi_Vasant": {
            "pattern": "hhvs1{ch:02d}",  # hhvs101-hhvs118
            "chapters": 18,
            "book": "Vasant"
        },
        "Hindi_Durva": {
            "pattern": "hhdu1{ch:02d}",  # hhdu101-hhdu118
            "chapters": 18,
            "book": "Durva"
        },
        "Hindi_Bharat_Ki_Khoj": {
            "pattern": "hhbk1{ch:02d}",  # hhbk101-hhbk110
            "chapters": 10,
            "book": "Bharat Ki Khoj (Supplementary)"
        },
    },

    # ============================================================================
    # GRADE 7
    # ============================================================================
    "7": {
        "Mathematics": {
            "pattern": "gemh1{ch:02d}",  # gemh101-gemh115
            "chapters": 15,
            "book": "Mathematics"
        },
        "Science": {
            "pattern": "gesc1{ch:02d}",  # gesc101-gesc118
            "chapters": 18,
            "book": "Science"
        },
        "Social_Science": {
            "pattern": "gess1{ch:02d}",  # gess101-gess128
            "chapters": 28,
            "book": "Our Past, Social and Political Life"
        },
        "English_Honeycomb": {
            "pattern": "gehn1{ch:02d}",  # gehn101-gehn110
            "chapters": 10,
            "book": "Honeycomb"
        },
        "English_Alien_Hand": {
            "pattern": "geah1{ch:02d}",  # geah101-geah110
            "chapters": 10,
            "book": "An Alien Hand (Supplementary)"
        },
        "Hindi_Vasant": {
            "pattern": "ghvs1{ch:02d}",  # ghvs101-ghvs120
            "chapters": 20,
            "book": "Vasant"
        },
        "Hindi_Durva": {
            "pattern": "ghdu1{ch:02d}",  # ghdu101-ghdu115
            "chapters": 15,
            "book": "Durva"
        },
        "Hindi_Mahabharat": {
            "pattern": "ghmb1{ch:02d}",  # ghmb101-ghmb110
            "chapters": 10,
            "book": "Mahabharat (Supplementary)"
        },
    },

    # ============================================================================
    # GRADE 6
    # ============================================================================
    "6": {
        "Mathematics_Ganita_Prakash": {
            "pattern": "fegp1{ch:02d}",  # fegp101-fegp108 (NEP 2020)
            "chapters": 8,
            "book": "Ganita Prakash (NEP 2020)"
        },
        "Science_Curiosity": {
            "pattern": "fecu1{ch:02d}",  # fecu101-fecu112 (NEP 2020)
            "chapters": 12,
            "book": "Curiosity (NEP 2020)"
        },
        "Social_Science": {
            "pattern": "fess1{ch:02d}",  # fess101-fess128
            "chapters": 28,
            "book": "The Earth Our Habitat, Social and Political Life"
        },
        "English_Honeysuckle": {
            "pattern": "fehs1{ch:02d}",  # fehs101-fehs110
            "chapters": 10,
            "book": "Honeysuckle"
        },
        "English_A_Pact_with_the_Sun": {
            "pattern": "feps1{ch:02d}",  # feps101-feps110
            "chapters": 10,
            "book": "A Pact with the Sun (Supplementary)"
        },
        "Hindi_Vasant": {
            "pattern": "fhvs1{ch:02d}",  # fhvs101-fhvs116
            "chapters": 16,
            "book": "Vasant"
        },
        "Hindi_Durva": {
            "pattern": "fhdu1{ch:02d}",  # fhdu101-fhdu128
            "chapters": 28,
            "book": "Durva"
        },
        "Hindi_Bal_Ram_Katha": {
            "pattern": "fhbr1{ch:02d}",  # fhbr101-fhbr112
            "chapters": 12,
            "book": "Bal Ram Katha (Supplementary)"
        },
    },

    # ============================================================================
    # GRADE 5
    # ============================================================================
    "5": {
        "Mathematics_Math_Magic": {
            "pattern": "eemm1{ch:02d}",  # eemm101-eemm114
            "chapters": 14,
            "book": "Math-Magic"
        },
        "EVS_Looking_Around": {
            "pattern": "eeev1{ch:02d}",  # eeev101-eeev122
            "chapters": 22,
            "book": "Looking Around (EVS)"
        },
        "English_Marigold": {
            "pattern": "eemr1{ch:02d}",  # eemr101-eemr110
            "chapters": 10,
            "book": "Marigold"
        },
        "Hindi_Rimjhim": {
            "pattern": "ehrj1{ch:02d}",  # ehrj101-ehrj118
            "chapters": 18,
            "book": "Rimjhim"
        },
    },

    # ============================================================================
    # GRADE 4
    # ============================================================================
    "4": {
        "Mathematics_Math_Magic": {
            "pattern": "demm1{ch:02d}",  # demm101-demm114
            "chapters": 14,
            "book": "Math-Magic"
        },
        "EVS_Looking_Around": {
            "pattern": "deev1{ch:02d}",  # deev101-deev127
            "chapters": 27,
            "book": "Looking Around (EVS)"
        },
        "English_Marigold": {
            "pattern": "demr1{ch:02d}",  # demr101-demr110
            "chapters": 10,
            "book": "Marigold"
        },
        "Hindi_Rimjhim": {
            "pattern": "dhrj1{ch:02d}",  # dhrj101-dhrj114
            "chapters": 14,
            "book": "Rimjhim"
        },
    },

    # ============================================================================
    # GRADE 3
    # ============================================================================
    "3": {
        "Mathematics_Math_Magic": {
            "pattern": "cemm1{ch:02d}",  # cemm101-cemm114
            "chapters": 14,
            "book": "Math-Magic"
        },
        "EVS_Looking_Around": {
            "pattern": "ceev1{ch:02d}",  # ceev101-ceev124
            "chapters": 24,
            "book": "Looking Around (EVS)"
        },
        "English_Marigold": {
            "pattern": "cemr1{ch:02d}",  # cemr101-cemr110
            "chapters": 10,
            "book": "Marigold"
        },
        "Hindi_Rimjhim": {
            "pattern": "chrj1{ch:02d}",  # chrj101-chrj114
            "chapters": 14,
            "book": "Rimjhim"
        },
    },

    # ============================================================================
    # GRADE 2
    # ============================================================================
    "2": {
        "Mathematics_Math_Magic": {
            "pattern": "bemm1{ch:02d}",  # bemm101-bemm115
            "chapters": 15,
            "book": "Math-Magic"
        },
        "EVS": {
            "pattern": "beev1{ch:02d}",  # beev101-beev121
            "chapters": 21,
            "book": "Raindrops (EVS)"
        },
        "English_Marigold": {
            "pattern": "bemr1{ch:02d}",  # bemr101-bemr110
            "chapters": 10,
            "book": "Marigold"
        },
        "Hindi_Rimjhim": {
            "pattern": "bhrj1{ch:02d}",  # bhrj101-bhrj114
            "chapters": 14,
            "book": "Rimjhim"
        },
    },

    # ============================================================================
    # GRADE 1
    # ============================================================================
    "1": {
        "Mathematics_Math_Magic": {
            "pattern": "aemm1{ch:02d}",  # aemm101-aemm113
            "chapters": 13,
            "book": "Math-Magic"
        },
        "EVS": {
            "pattern": "aeev1{ch:02d}",  # aeev101-aeev122
            "chapters": 22,
            "book": "Raindrops (EVS)"
        },
        "English_Marigold": {
            "pattern": "aemr1{ch:02d}",  # aemr101-aemr110
            "chapters": 10,
            "book": "Marigold"
        },
        "Hindi_Rimjhim": {
            "pattern": "ahrj1{ch:02d}",  # ahrj101-ahrj123
            "chapters": 23,
            "book": "Rimjhim"
        },
    },
}


def generate_url(grade, subject, chapter):
    """Generate NCERT PDF URL for given grade/subject/chapter"""
    grade_str = str(grade)

    if grade_str not in COMPLETE_NCERT_CATALOG:
        return None

    if subject not in COMPLETE_NCERT_CATALOG[grade_str]:
        return None

    pattern = COMPLETE_NCERT_CATALOG[grade_str][subject]["pattern"]
    url = f"https://ncert.nic.in/textbook/pdf/{pattern.format(ch=chapter)}.pdf"

    return url


def get_all_urls():
    """Generate all NCERT URLs"""
    all_urls = []

    for grade, subjects in COMPLETE_NCERT_CATALOG.items():
        for subject, info in subjects.items():
            for ch in range(1, info["chapters"] + 1):
                url = generate_url(grade, subject, ch)
                all_urls.append({
                    "grade": grade,
                    "subject": subject,
                    "chapter": ch,
                    "url": url,
                    "book": info["book"]
                })

    return all_urls


def count_total_chapters():
    """Count total chapters across all grades"""
    total = 0
    for grade, subjects in COMPLETE_NCERT_CATALOG.items():
        for subject, info in subjects.items():
            total += info["chapters"]
    return total


if __name__ == "__main__":
    print(f"Total chapters: {count_total_chapters()}")

    # Test a few URLs
    print(f"\nGrade 10 Math Ch.1: {generate_url(10, 'Mathematics', 1)}")
    print(f"Grade 1 Hindi Ch.1: {generate_url(1, 'Hindi_Rimjhim', 1)}")
    print(f"Grade 6 Science Ch.5: {generate_url(6, 'Science_Curiosity', 5)}")
