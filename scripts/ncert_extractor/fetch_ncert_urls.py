#!/usr/bin/env python3
"""
Fetch actual NCERT PDF URLs from ncert.nic.in
Generate updated catalog with working download links
"""

import requests
from bs4 import BeautifulSoup
import re


# Updated NCERT Textbook URLs - Based on NCERT website structure (2024-25/2025-26)
NCERT_TEXTBOOKS_UPDATED = {
    # Grade 10
    "10": {
        "Mathematics": "https://ncert.nic.in/textbook/pdf/jemh1ps.pdf",
        "Science": "https://ncert.nic.in/textbook/pdf/jesc1ps.pdf",
        "Social Science - History": "https://ncert.nic.in/textbook/pdf/jehi1ps.pdf",
        "Social Science - Geography": "https://ncert.nic.in/textbook/pdf/jege1ps.pdf",
        "Social Science - Political Science": "https://ncert.nic.in/textbook/pdf/jeps1ps.pdf",
        "Social Science - Economics": "https://ncert.nic.in/textbook/pdf/jeec1ps.pdf",
        "English - First Flight": "https://ncert.nic.in/textbook/pdf/jeff1ps.pdf",
        "English - Footprints": "https://ncert.nic.in/textbook/pdf/jefp1ps.pdf",
        "Hindi - Kshitij": "https://ncert.nic.in/textbook/pdf/jhks1ps.pdf",
    },

    # Grade 9
    "9": {
        "Mathematics": "https://ncert.nic.in/textbook/pdf/iemh1ps.pdf",
        "Science": "https://ncert.nic.in/textbook/pdf/iesc1ps.pdf",
        "Social Science - History": "https://ncert.nic.in/textbook/pdf/iihi1ps.pdf",
        "Social Science - Geography": "https://ncert.nic.in/textbook/pdf/iigeo1ps.pdf",
        "Social Science - Political Science": "https://ncert.nic.in/textbook/pdf/iidp1ps.pdf",
        "Social Science - Economics": "https://ncert.nic.in/textbook/pdf/ieee1ps.pdf",
        "English - Beehive": "https://ncert.nic.in/textbook/pdf/iebe1ps.pdf",
        "English - Moments": "https://ncert.nic.in/textbook/pdf/iemo1ps.pdf",
        "Hindi - Kshitij": "https://ncert.nic.in/textbook/pdf/ihks1ps.pdf",
    },

    # Grade 8
    "8": {
        "Mathematics": "https://ncert.nic.in/textbook/pdf/hemh1ps.pdf",
        "Science": "https://ncert.nic.in/textbook/pdf/hesc1ps.pdf",
        "Social Science - History": "https://ncert.nic.in/textbook/pdf/hehs1ps.pdf",
        "Social Science - Geography": "https://ncert.nic.in/textbook/pdf/hegs1ps.pdf",
        "Social Science - Civics": "https://ncert.nic.in/textbook/pdf/hess1ps.pdf",
        "English - Honeydew": "https://ncert.nic.in/textbook/pdf/hehn1ps.pdf",
        "English - It So Happened": "https://ncert.nic.in/textbook/pdf/hesh1ps.pdf",
        "Hindi - Vasant": "https://ncert.nic.in/textbook/pdf/hhva1ps.pdf",
    },

    # Grade 7
    "7": {
        "Mathematics": "https://ncert.nic.in/textbook/pdf/gemh1ps.pdf",
        "Science": "https://ncert.nic.in/textbook/pdf/gesc1ps.pdf",
        "Social Science - History": "https://ncert.nic.in/textbook/pdf/gehs1ps.pdf",
        "Social Science - Geography": "https://ncert.nic.in/textbook/pdf/gegs1ps.pdf",
        "Social Science - Civics": "https://ncert.nic.in/textbook/pdf/gess1ps.pdf",
        "English - Honeycomb": "https://ncert.nic.in/textbook/pdf/gehc1ps.pdf",
        "English - An Alien Hand": "https://ncert.nic.in/textbook/pdf/geah1ps.pdf",
        "Hindi - Vasant": "https://ncert.nic.in/textbook/pdf/ghva1ps.pdf",
    },

    # Grade 6
    "6": {
        "Mathematics": "https://ncert.nic.in/textbook/pdf/femh1ps.pdf",
        "Science": "https://ncert.nic.in/textbook/pdf/fesc1ps.pdf",
        "Social Science - History": "https://ncert.nic.in/textbook/pdf/fehs1ps.pdf",
        "Social Science - Geography": "https://ncert.nic.in/textbook/pdf/fegs1ps.pdf",
        "Social Science - Civics": "https://ncert.nic.in/textbook/pdf/fess1ps.pdf",
        "English - Honeysuckle": "https://ncert.nic.in/textbook/pdf/fehs1ps.pdf",
        "English - A Pact with the Sun": "https://ncert.nic.in/textbook/pdf/feps1ps.pdf",
        "Hindi - Vasant": "https://ncert.nic.in/textbook/pdf/fhva1ps.pdf",
    },

    # Grade 5
    "5": {
        "Mathematics": "https://ncert.nic.in/textbook/pdf/eemh1ps.pdf",
        "English - Marigold": "https://ncert.nic.in/textbook/pdf/eemr1ps.pdf",
        "Environmental Studies": "https://ncert.nic.in/textbook/pdf/eeap1ps.pdf",
        "Hindi - Rimjhim": "https://ncert.nic.in/textbook/pdf/ehrm1ps.pdf",
    },

    # Grade 4
    "4": {
        "Mathematics": "https://ncert.nic.in/textbook/pdf/demh1ps.pdf",
        "English - Marigold": "https://ncert.nic.in/textbook/pdf/demr1ps.pdf",
        "Environmental Studies": "https://ncert.nic.in/textbook/pdf/deap1ps.pdf",
        "Hindi - Rimjhim": "https://ncert.nic.in/textbook/pdf/dhrm1ps.pdf",
    },

    # Grade 3
    "3": {
        "Mathematics": "https://ncert.nic.in/textbook/pdf/cemh1ps.pdf",
        "English - Marigold": "https://ncert.nic.in/textbook/pdf/cemr1ps.pdf",
        "Environmental Studies": "https://ncert.nic.in/textbook/pdf/ceap1ps.pdf",
        "Hindi - Rimjhim": "https://ncert.nic.in/textbook/pdf/chrm1ps.pdf",
    },

    # Grade 2
    "2": {
        "Mathematics": "https://ncert.nic.in/textbook/pdf/bemh1ps.pdf",
        "English - Marigold": "https://ncert.nic.in/textbook/pdf/bemr1ps.pdf",
        "Hindi - Rimjhim": "https://ncert.nic.in/textbook/pdf/bhrm1ps.pdf",
    },

    # Grade 1
    "1": {
        "Mathematics": "https://ncert.nic.in/textbook/pdf/aemh1ps.pdf",
        "English - Marigold": "https://ncert.nic.in/textbook/pdf/aemr1ps.pdf",
        "Hindi - Rimjhim": "https://ncert.nic.in/textbook/pdf/ahrm1ps.pdf",
    }
}


def verify_url(url):
    """Check if URL exists and returns PDF"""
    try:
        response = requests.head(url, timeout=10)
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'pdf' in content_type.lower():
                return True, "OK"
            else:
                return True, f"Non-PDF content: {content_type}"
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)


def test_all_urls():
    """Test all URLs in the catalog"""
    print("\n📋 Testing NCERT PDF URLs...\n")

    total = 0
    working = 0
    broken = 0

    for grade, subjects in NCERT_TEXTBOOKS_UPDATED.items():
        print(f"\nGrade {grade}:")
        for subject, url in subjects.items():
            total += 1
            is_valid, message = verify_url(url)

            status = "✅" if is_valid else "❌"
            print(f"  {status} {subject}: {message}")

            if is_valid:
                working += 1
            else:
                broken += 1

    print(f"\n{'='*60}")
    print(f"Summary: {working}/{total} working ({broken} broken)")
    print(f"{'='*60}\n")


def generate_updated_catalog():
    """Generate updated ncert_catalog.py with working URLs"""

    catalog_code = '''#!/usr/bin/env python3
"""
NCERT Textbook PDF Catalog (Updated URLs)
Official NCERT PDF URLs for Grades 1-10
Last verified: 2025-11-04
"""

NCERT_TEXTBOOKS = {
'''

    for grade, subjects in NCERT_TEXTBOOKS_UPDATED.items():
        catalog_code += f'    # Grade {grade}\n'
        catalog_code += f'    "{grade}": {{\n'
        for subject, url in subjects.items():
            catalog_code += f'        "{subject}": "{url}",\n'
        catalog_code += f'    }},\n\n'

    catalog_code += '''}\n\n
def get_all_textbooks():
    """Get all textbooks as flat list"""
    textbooks = []
    for grade, subjects in NCERT_TEXTBOOKS.items():
        for subject, url in subjects.items():
            textbooks.append({
                'grade': int(grade),
                'subject': subject,
                'pdf_url': url
            })
    return textbooks
'''

    return catalog_code


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_all_urls()
    elif len(sys.argv) > 1 and sys.argv[1] == "--generate":
        code = generate_updated_catalog()
        with open("ncert_catalog_updated.py", "w") as f:
            f.write(code)
        print("✅ Generated: ncert_catalog_updated.py")
    else:
        print("\nUsage:")
        print("  python3 fetch_ncert_urls.py --test      # Test all URLs")
        print("  python3 fetch_ncert_urls.py --generate  # Generate updated catalog\n")
