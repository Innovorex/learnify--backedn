#!/usr/bin/env python3
"""
Telangana SCERT Download Verifier
Verifies downloaded PDFs are valid and complete
"""

import json
from pathlib import Path
from typing import Dict, Any
import PyPDF2

def verify_pdf(pdf_path: Path) -> Dict[str, Any]:
    """
    Verify a PDF file is valid and readable

    Returns:
        dict with verification results
    """
    result = {
        'valid': False,
        'num_pages': 0,
        'file_size_mb': 0,
        'error': None
    }

    try:
        # Check file exists
        if not pdf_path.exists():
            result['error'] = "File not found"
            return result

        # Check file size
        file_size = pdf_path.stat().st_size
        result['file_size_mb'] = file_size / (1024 * 1024)

        # File too small (likely invalid)
        if file_size < 50000:  # < 50KB
            result['error'] = f"File too small ({result['file_size_mb']:.2f} MB)"
            return result

        # Try to open with PyPDF2
        with open(pdf_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            result['num_pages'] = len(pdf_reader.pages)

            # Check has pages
            if result['num_pages'] == 0:
                result['error'] = "PDF has 0 pages"
                return result

        result['valid'] = True
        return result

    except Exception as e:
        result['error'] = str(e)
        return result


def verify_all_downloads(
    catalog_path: str = "/home/learnify/telangana_textbook_catalog_complete.json",
    pdf_dir: str = None
) -> Dict[str, Any]:
    """
    Verify all downloaded Telangana textbooks

    Returns:
        Dict with verification statistics
    """
    print("=" * 70)
    print("TELANGANA SCERT DOWNLOAD VERIFICATION")
    print("=" * 70)

    # Load catalog
    with open(catalog_path, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    if pdf_dir is None:
        pdf_dir = catalog['pdf_directory']

    pdf_path = Path(pdf_dir)
    print(f"\n📁 PDF directory: {pdf_path}")

    # Verification stats
    stats = {
        'total_expected': 0,
        'total_found': 0,
        'total_valid': 0,
        'total_invalid': 0,
        'total_missing': 0,
        'by_grade': {},
        'invalid_files': [],
        'missing_files': []
    }

    # Verify each textbook
    print(f"\n🔍 Verifying downloads...\n")

    for grade_key, grade_data in catalog['grades'].items():
        grade = int(grade_key)

        stats['by_grade'][grade] = {
            'expected': 0,
            'found': 0,
            'valid': 0,
            'invalid': 0,
            'missing': 0
        }

        print(f"\n{'='*70}")
        print(f"CLASS {grade}")
        print(f"{'='*70}")

        for subject_name, subject_data in grade_data['subjects'].items():
            for medium, textbook_info in subject_data.items():
                filename = textbook_info['filename']
                textbook_name = textbook_info['textbook_name']
                file_path = pdf_path / filename

                stats['total_expected'] += 1
                stats['by_grade'][grade]['expected'] += 1

                # Verify
                verification = verify_pdf(file_path)

                if not file_path.exists():
                    print(f"  ❌ MISSING: {filename}")
                    stats['total_missing'] += 1
                    stats['by_grade'][grade]['missing'] += 1
                    stats['missing_files'].append({
                        'grade': grade,
                        'subject': subject_name,
                        'medium': medium,
                        'filename': filename
                    })

                elif verification['valid']:
                    print(f"  ✅ VALID: {filename} ({verification['num_pages']} pages, {verification['file_size_mb']:.1f} MB)")
                    stats['total_valid'] += 1
                    stats['total_found'] += 1
                    stats['by_grade'][grade]['valid'] += 1
                    stats['by_grade'][grade]['found'] += 1

                else:
                    print(f"  ⚠️  INVALID: {filename} - {verification['error']}")
                    stats['total_invalid'] += 1
                    stats['total_found'] += 1
                    stats['by_grade'][grade]['invalid'] += 1
                    stats['by_grade'][grade]['found'] += 1
                    stats['invalid_files'].append({
                        'grade': grade,
                        'subject': subject_name,
                        'medium': medium,
                        'filename': filename,
                        'error': verification['error']
                    })

    # Print summary
    print(f"\n\n{'='*70}")
    print("VERIFICATION SUMMARY")
    print(f"{'='*70}")
    print(f"\n📊 Overall Statistics:")
    print(f"   Total expected:   {stats['total_expected']}")
    print(f"   ✅ Valid PDFs:     {stats['total_valid']}")
    print(f"   ⚠️  Invalid PDFs:   {stats['total_invalid']}")
    print(f"   ❌ Missing PDFs:   {stats['total_missing']}")
    print(f"   📈 Completion:    {(stats['total_valid'] / stats['total_expected'] * 100):.1f}%")

    print(f"\n📊 By Grade:")
    for grade in sorted(stats['by_grade'].keys()):
        grade_stats = stats['by_grade'][grade]
        completion = (grade_stats['valid'] / grade_stats['expected'] * 100) if grade_stats['expected'] > 0 else 0
        print(f"   Grade {grade:2d}: ✅ {grade_stats['valid']:2d}/{grade_stats['expected']:2d}  ⚠️ {grade_stats['invalid']:2d}  ❌ {grade_stats['missing']:2d}  ({completion:.0f}%)")

    if stats['missing_files']:
        print(f"\n❌ Missing Files ({len(stats['missing_files'])}):")
        for missing in stats['missing_files'][:10]:  # Show first 10
            print(f"   - Grade {missing['grade']}: {missing['subject']} ({missing['medium']}) - {missing['filename']}")
        if len(stats['missing_files']) > 10:
            print(f"   ... and {len(stats['missing_files']) - 10} more")

    if stats['invalid_files']:
        print(f"\n⚠️  Invalid Files ({len(stats['invalid_files'])}):")
        for invalid in stats['invalid_files'][:10]:  # Show first 10
            print(f"   - Grade {invalid['grade']}: {invalid['filename']} - {invalid['error']}")
        if len(stats['invalid_files']) > 10:
            print(f"   ... and {len(stats['invalid_files']) - 10} more")

    # Save verification log
    log_path = pdf_path.parent / "telangana_verification_log.json"
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"\n📝 Verification log saved to: {log_path}")

    return stats


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Verify Telangana SCERT textbook downloads')
    parser.add_argument(
        '--catalog',
        default='/home/learnify/telangana_textbook_catalog_complete.json',
        help='Path to catalog JSON file'
    )
    parser.add_argument(
        '--pdf-dir',
        default=None,
        help='PDF directory (default from catalog)'
    )

    args = parser.parse_args()

    try:
        stats = verify_all_downloads(
            catalog_path=args.catalog,
            pdf_dir=args.pdf_dir
        )

        if stats['total_missing'] == 0 and stats['total_invalid'] == 0:
            print("\n✅ All textbooks verified successfully!")
        else:
            print(f"\n⚠️  Verification complete with issues:")
            print(f"   Missing: {stats['total_missing']}")
            print(f"   Invalid: {stats['total_invalid']}")

    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
