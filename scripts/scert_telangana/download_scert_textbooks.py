#!/usr/bin/env python3
"""
Telangana SCERT Textbook Downloader
Downloads all Telangana State Board textbooks from Google Drive
"""

import json
import requests
import time
from pathlib import Path
from typing import Dict, Any
import sys

def download_file_from_google_drive(url: str, destination: Path) -> bool:
    """
    Download a file from Google Drive with progress tracking

    Args:
        url: Google Drive download URL
        destination: Path where file should be saved

    Returns:
        bool: True if download successful, False otherwise
    """
    try:
        print(f"  Downloading: {destination.name}")

        # Create session for handling cookies
        session = requests.Session()

        # Download with stream to handle large files
        response = session.get(url, stream=True, timeout=120)
        response.raise_for_status()

        # Check if it's a confirmation page (for large files)
        if 'download_warning' in response.text or 'virus scan warning' in response.text:
            # Extract confirmation token
            for key, value in response.cookies.items():
                if key.startswith('download_warning'):
                    params = {'confirm': value}
                    response = session.get(url, params=params, stream=True, timeout=120)
                    break

        # Save file
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    # Print progress every 1MB
                    if downloaded % (1024 * 1024) == 0:
                        mb_downloaded = downloaded / (1024 * 1024)
                        if total_size > 0:
                            mb_total = total_size / (1024 * 1024)
                            progress = (downloaded / total_size) * 100
                            print(f"    Progress: {mb_downloaded:.1f}/{mb_total:.1f} MB ({progress:.1f}%)", end='\r')
                        else:
                            print(f"    Downloaded: {mb_downloaded:.1f} MB", end='\r')

        print(f"\n  ✅ Downloaded: {destination.name} ({downloaded / (1024*1024):.1f} MB)")
        return True

    except requests.exceptions.RequestException as e:
        print(f"  ❌ Error downloading {destination.name}: {str(e)}")
        return False
    except Exception as e:
        print(f"  ❌ Unexpected error: {str(e)}")
        return False


def download_all_textbooks(
    catalog_path: str = "/home/learnify/telangana_textbook_catalog_complete.json",
    output_dir: str = None,
    priority_only: bool = False,
    grades: list = None
) -> Dict[str, Any]:
    """
    Download all Telangana SCERT textbooks

    Args:
        catalog_path: Path to the textbook catalog JSON
        output_dir: Directory to save PDFs (default from catalog)
        priority_only: If True, only download priority subjects (Telugu, English mediums)
        grades: List of grades to download (e.g., [1, 2, 3]), None for all

    Returns:
        Dict with download statistics
    """
    print("=" * 70)
    print("TELANGANA SCERT TEXTBOOK DOWNLOADER")
    print("=" * 70)

    # Load catalog
    print(f"\n📂 Loading catalog from: {catalog_path}")
    with open(catalog_path, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    # Setup output directory
    if output_dir is None:
        output_dir = catalog['pdf_directory']

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"📁 Output directory: {output_path}")

    # Priority mediums
    priority_mediums = catalog.get('priority_download_list', {}).get('priority_mediums', ['telugu', 'english'])
    priority_subjects = catalog.get('priority_download_list', {}).get('priority_subjects', [])

    print(f"\n⚙️  Settings:")
    print(f"   Priority only: {priority_only}")
    if priority_only:
        print(f"   Priority mediums: {', '.join(priority_mediums)}")
        print(f"   Priority subjects: {', '.join(priority_subjects)}")
    if grades:
        print(f"   Grades to download: {', '.join(map(str, grades))}")
    else:
        print(f"   Downloading all grades: 1-10")

    # Download statistics
    stats = {
        'total_attempted': 0,
        'total_success': 0,
        'total_failed': 0,
        'total_skipped': 0,
        'by_grade': {},
        'failed_downloads': []
    }

    # Download each textbook
    print(f"\n🚀 Starting downloads...\n")

    for grade_key, grade_data in catalog['grades'].items():
        grade = int(grade_key)

        # Skip if not in requested grades
        if grades and grade not in grades:
            continue

        stats['by_grade'][grade] = {
            'attempted': 0,
            'success': 0,
            'failed': 0,
            'skipped': 0
        }

        print(f"\n{'='*70}")
        print(f"CLASS {grade}")
        print(f"{'='*70}")

        for subject_name, subject_data in grade_data['subjects'].items():
            print(f"\n📚 Subject: {subject_name}")

            for medium, textbook_info in subject_data.items():
                # Check priority filter
                if priority_only:
                    if medium not in priority_mediums:
                        stats['by_grade'][grade]['skipped'] += 1
                        stats['total_skipped'] += 1
                        print(f"  ⏭️  Skipped: {medium} (not priority)")
                        continue

                    if subject_name not in priority_subjects:
                        stats['by_grade'][grade]['skipped'] += 1
                        stats['total_skipped'] += 1
                        print(f"  ⏭️  Skipped: {subject_name} (not priority)")
                        continue

                # Get download info
                download_url = textbook_info['download_url']
                filename = textbook_info['filename']
                textbook_name = textbook_info['textbook_name']

                destination = output_path / filename

                # Skip if already downloaded
                if destination.exists():
                    file_size = destination.stat().st_size
                    if file_size > 100000:  # > 100KB (likely valid)
                        print(f"  ⏭️  Already exists: {filename} ({file_size / (1024*1024):.1f} MB)")
                        stats['by_grade'][grade]['skipped'] += 1
                        stats['total_skipped'] += 1
                        continue

                # Attempt download
                print(f"  📖 {textbook_name} ({medium})")
                stats['total_attempted'] += 1
                stats['by_grade'][grade]['attempted'] += 1

                success = download_file_from_google_drive(download_url, destination)

                if success:
                    stats['total_success'] += 1
                    stats['by_grade'][grade]['success'] += 1
                else:
                    stats['total_failed'] += 1
                    stats['by_grade'][grade]['failed'] += 1
                    stats['failed_downloads'].append({
                        'grade': grade,
                        'subject': subject_name,
                        'medium': medium,
                        'filename': filename,
                        'url': download_url
                    })

                # Rate limiting - be nice to Google Drive
                time.sleep(2)

    # Print summary
    print(f"\n\n{'='*70}")
    print("DOWNLOAD SUMMARY")
    print(f"{'='*70}")
    print(f"\n📊 Overall Statistics:")
    print(f"   Total attempted:  {stats['total_attempted']}")
    print(f"   ✅ Successful:     {stats['total_success']}")
    print(f"   ❌ Failed:         {stats['total_failed']}")
    print(f"   ⏭️  Skipped:       {stats['total_skipped']}")

    print(f"\n📊 By Grade:")
    for grade in sorted(stats['by_grade'].keys()):
        grade_stats = stats['by_grade'][grade]
        print(f"   Grade {grade:2d}: ✅ {grade_stats['success']:2d}  ❌ {grade_stats['failed']:2d}  ⏭️ {grade_stats['skipped']:2d}")

    if stats['failed_downloads']:
        print(f"\n❌ Failed Downloads ({len(stats['failed_downloads'])}):")
        for failed in stats['failed_downloads']:
            print(f"   - Grade {failed['grade']}: {failed['subject']} ({failed['medium']})")
            print(f"     File: {failed['filename']}")

    # Save download log
    log_path = output_path.parent / "telangana_download_log.json"
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"\n📝 Download log saved to: {log_path}")

    return stats


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Download Telangana SCERT textbooks')
    parser.add_argument(
        '--catalog',
        default='/home/learnify/telangana_textbook_catalog_complete.json',
        help='Path to catalog JSON file'
    )
    parser.add_argument(
        '--output-dir',
        default=None,
        help='Output directory (default from catalog)'
    )
    parser.add_argument(
        '--priority-only',
        action='store_true',
        help='Only download priority subjects (Telugu, English mediums)'
    )
    parser.add_argument(
        '--grades',
        type=int,
        nargs='+',
        help='Specific grades to download (e.g., --grades 1 2 3)'
    )

    args = parser.parse_args()

    try:
        stats = download_all_textbooks(
            catalog_path=args.catalog,
            output_dir=args.output_dir,
            priority_only=args.priority_only,
            grades=args.grades
        )

        if stats['total_failed'] == 0:
            print("\n✅ All downloads completed successfully!")
            sys.exit(0)
        else:
            print(f"\n⚠️  Completed with {stats['total_failed']} failures")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
