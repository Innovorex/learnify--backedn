#!/usr/bin/env python3
"""
NCERT Textbook PDF Catalog
Official NCERT PDF URLs for Grades 1-10 (All Subjects)
"""

# NCERT Textbook URLs - Directly from ncert.nic.in
NCERT_TEXTBOOKS = {
    # Grade 10
    "10": {
        "Mathematics": {
            "url": "https://ncert.nic.in/textbook/pdf/jemh1dd.pdf",
            "book_name": "Mathematics - Class 10"
        },
        "Science": {
            "url": "https://ncert.nic.in/textbook/pdf/jesc1dd.pdf",
            "book_name": "Science - Class 10"
        },
        "Social Science": {
            "url": "https://ncert.nic.in/textbook/pdf/jess1dd.pdf",
            "book_name": "Social Science - Class 10"
        },
        "English": {
            "url": "https://ncert.nic.in/textbook/pdf/jefl1dd.pdf",
            "book_name": "First Flight - Class 10 (English)"
        },
        "Hindi": {
            "url": "https://ncert.nic.in/textbook/pdf/jhkh1cc.pdf",
            "book_name": "Kshitij - Class 10 (Hindi)"
        }
    },

    # Grade 9
    "9": {
        "Mathematics": {
            "url": "https://ncert.nic.in/textbook/pdf/iemh1dd.pdf",
            "book_name": "Mathematics - Class 9"
        },
        "Science": {
            "url": "https://ncert.nic.in/textbook/pdf/iesc1dd.pdf",
            "book_name": "Science - Class 9"
        },
        "Social Science": {
            "url": "https://ncert.nic.in/textbook/pdf/iess1dd.pdf",
            "book_name": "Social Science - Class 9"
        },
        "English": {
            "url": "https://ncert.nic.in/textbook/pdf/iebe1dd.pdf",
            "book_name": "Beehive - Class 9 (English)"
        },
        "Hindi": {
            "url": "https://ncert.nic.in/textbook/pdf/ihks1cc.pdf",
            "book_name": "Kshitij - Class 9 (Hindi)"
        }
    },

    # Grade 8
    "8": {
        "Mathematics": {
            "url": "https://ncert.nic.in/textbook/pdf/hemh1dd.pdf",
            "book_name": "Mathematics - Class 8"
        },
        "Science": {
            "url": "https://ncert.nic.in/textbook/pdf/hesc1dd.pdf",
            "book_name": "Science - Class 8"
        },
        "Social Science": {
            "url": "https://ncert.nic.in/textbook/pdf/hess1dd.pdf",
            "book_name": "Social Science - Class 8"
        },
        "English": {
            "url": "https://ncert.nic.in/textbook/pdf/hehn1dd.pdf",
            "book_name": "Honeydew - Class 8 (English)"
        },
        "Hindi": {
            "url": "https://ncert.nic.in/textbook/pdf/hhva1cc.pdf",
            "book_name": "Vasant - Class 8 (Hindi)"
        }
    },

    # Grade 7
    "7": {
        "Mathematics": {
            "url": "https://ncert.nic.in/textbook/pdf/gemh1dd.pdf",
            "book_name": "Mathematics - Class 7"
        },
        "Science": {
            "url": "https://ncert.nic.in/textbook/pdf/gesc1dd.pdf",
            "book_name": "Science - Class 7"
        },
        "Social Science": {
            "url": "https://ncert.nic.in/textbook/pdf/gess1dd.pdf",
            "book_name": "Social Science - Class 7"
        },
        "English": {
            "url": "https://ncert.nic.in/textbook/pdf/gehn1dd.pdf",
            "book_name": "Honeycomb - Class 7 (English)"
        },
        "Hindi": {
            "url": "https://ncert.nic.in/textbook/pdf/ghva1cc.pdf",
            "book_name": "Vasant - Class 7 (Hindi)"
        }
    },

    # Grade 6
    "6": {
        "Mathematics": {
            "url": "https://ncert.nic.in/textbook/pdf/femh1dd.pdf",
            "book_name": "Mathematics - Class 6"
        },
        "Science": {
            "url": "https://ncert.nic.in/textbook/pdf/fesc1dd.pdf",
            "book_name": "Science - Class 6"
        },
        "Social Science": {
            "url": "https://ncert.nic.in/textbook/pdf/fess1dd.pdf",
            "book_name": "Social Science - Class 6"
        },
        "English": {
            "url": "https://ncert.nic.in/textbook/pdf/fehn1dd.pdf",
            "book_name": "Honeysuckle - Class 6 (English)"
        },
        "Hindi": {
            "url": "https://ncert.nic.in/textbook/pdf/fhva1cc.pdf",
            "book_name": "Vasant - Class 6 (Hindi)"
        }
    },

    # Grade 5
    "5": {
        "Mathematics": {
            "url": "https://ncert.nic.in/textbook/pdf/eemh1dd.pdf",
            "book_name": "Math-Magic - Class 5"
        },
        "English": {
            "url": "https://ncert.nic.in/textbook/pdf/eemr1dd.pdf",
            "book_name": "Marigold - Class 5 (English)"
        },
        "Environmental Studies": {
            "url": "https://ncert.nic.in/textbook/pdf/eeap1dd.pdf",
            "book_name": "Looking Around - Class 5 (EVS)"
        },
        "Hindi": {
            "url": "https://ncert.nic.in/textbook/pdf/ehrm1cc.pdf",
            "book_name": "Rimjhim - Class 5 (Hindi)"
        }
    },

    # Grade 4
    "4": {
        "Mathematics": {
            "url": "https://ncert.nic.in/textbook/pdf/demh1dd.pdf",
            "book_name": "Math-Magic - Class 4"
        },
        "English": {
            "url": "https://ncert.nic.in/textbook/pdf/demr1dd.pdf",
            "book_name": "Marigold - Class 4 (English)"
        },
        "Environmental Studies": {
            "url": "https://ncert.nic.in/textbook/pdf/deap1dd.pdf",
            "book_name": "Looking Around - Class 4 (EVS)"
        },
        "Hindi": {
            "url": "https://ncert.nic.in/textbook/pdf/dhrm1cc.pdf",
            "book_name": "Rimjhim - Class 4 (Hindi)"
        }
    },

    # Grade 3
    "3": {
        "Mathematics": {
            "url": "https://ncert.nic.in/textbook/pdf/cemh1dd.pdf",
            "book_name": "Math-Magic - Class 3"
        },
        "English": {
            "url": "https://ncert.nic.in/textbook/pdf/cemr1dd.pdf",
            "book_name": "Marigold - Class 3 (English)"
        },
        "Environmental Studies": {
            "url": "https://ncert.nic.in/textbook/pdf/ceap1dd.pdf",
            "book_name": "Looking Around - Class 3 (EVS)"
        },
        "Hindi": {
            "url": "https://ncert.nic.in/textbook/pdf/chrm1cc.pdf",
            "book_name": "Rimjhim - Class 3 (Hindi)"
        }
    },

    # Grade 2
    "2": {
        "Mathematics": {
            "url": "https://ncert.nic.in/textbook/pdf/bemh1dd.pdf",
            "book_name": "Math-Magic - Class 2"
        },
        "English": {
            "url": "https://ncert.nic.in/textbook/pdf/bemr1dd.pdf",
            "book_name": "Marigold - Class 2 (English)"
        },
        "Environmental Studies": {
            "url": "https://ncert.nic.in/textbook/pdf/beap1dd.pdf",
            "book_name": "Raindrops - Class 2 (EVS)"
        },
        "Hindi": {
            "url": "https://ncert.nic.in/textbook/pdf/bhrm1cc.pdf",
            "book_name": "Rimjhim - Class 2 (Hindi)"
        }
    },

    # Grade 1
    "1": {
        "Mathematics": {
            "url": "https://ncert.nic.in/textbook/pdf/aemh1dd.pdf",
            "book_name": "Math-Magic - Class 1"
        },
        "English": {
            "url": "https://ncert.nic.in/textbook/pdf/aemr1dd.pdf",
            "book_name": "Marigold - Class 1 (English)"
        },
        "Environmental Studies": {
            "url": "https://ncert.nic.in/textbook/pdf/aeap1dd.pdf",
            "book_name": "Raindrops - Class 1 (EVS)"
        },
        "Hindi": {
            "url": "https://ncert.nic.in/textbook/pdf/ahrm1cc.pdf",
            "book_name": "Rimjhim - Class 1 (Hindi)"
        }
    }
}


def get_all_textbooks():
    """Get all textbooks as flat list"""
    textbooks = []
    for grade, subjects in NCERT_TEXTBOOKS.items():
        for subject, info in subjects.items():
            textbooks.append({
                'grade': int(grade),
                'subject': subject,
                'book_name': info['book_name'],
                'pdf_url': info['url']
            })
    return textbooks


def get_textbook(grade, subject):
    """Get specific textbook info"""
    grade_str = str(grade)
    if grade_str in NCERT_TEXTBOOKS:
        if subject in NCERT_TEXTBOOKS[grade_str]:
            return NCERT_TEXTBOOKS[grade_str][subject]
    return None


def get_subject_mapping():
    """Map CBSE subject names to NCERT textbook subjects"""
    return {
        "Mathematics": "Mathematics",
        "Science": "Science",
        "Social Science": "Social Science",
        "English": "English",
        "Hindi": "Hindi",
        "Environmental Studies": "Environmental Studies",
        "EVS": "Environmental Studies"
    }


if __name__ == "__main__":
    # Test the catalog
    all_books = get_all_textbooks()
    print(f"✅ Total NCERT Textbooks: {len(all_books)}")
    print(f"✅ Grades covered: 1-10")
    print(f"✅ Subjects per grade: 4-5")

    # Test specific lookup
    book = get_textbook(10, "Mathematics")
    if book:
        print(f"\n📖 Grade 10 Mathematics:")
        print(f"   Book: {book['book_name']}")
        print(f"   URL: {book['url']}")
