#!/usr/bin/env python3
"""
Telangana SCERT - Telugu Second Language Downloader
Downloads Telugu Second Language textbooks (Grades 6-7)
"""

import json
import requests
import time
from pathlib import Path
import sys

def download_file_from_google_drive(url: str, destination: Path) -> bool:
    """Download a file from Google Drive"""
    try:
        print(f"  📥 Downloading: {destination.name}")

        session = requests.Session()
        response = session.get(url, stream=True, timeout=120)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    if downloaded % (1024 * 1024) == 0:
                        mb_downloaded = downloaded / (1024 * 1024)
                        if total_size > 0:
                            mb_total = total_size / (1024 * 1024)
                            progress = (downloaded / total_size) * 100
                            print(f"    Progress: {mb_downloaded:.1f}/{mb_total:.1f} MB ({progress:.1f}%)", end='\r')

        file_size = destination.stat().st_size
        print(f"\n  ✅ Downloaded: {file_size / (1024*1024):.1f} MB")
        return file_size > 100000

    except Exception as e:
        print(f"\n  ❌ Error: {str(e)}")
        return False


def main():
    print("=" * 90)
    print("TELANGANA SCERT - TELUGU SECOND LANGUAGE DOWNLOAD")
    print("=" * 90)

    # Load catalog
    catalog_path = "/home/learnify/telangana_textbook_catalog_complete.json"
    with open(catalog_path, 'r') as f:
        catalog = json.load(f)

    output_dir = Path(catalog['pdf_directory'])
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📂 Output directory: {output_dir}")
    print(f"📚 Downloading: Telugu Second Language textbooks")
    print(f"📊 Total expected: 2 textbooks (Grades 6-7)")

    stats = {
        'total': 0,
        'success': 0,
        'failed': 0,
        'skipped': 0
    }

    print(f"\n🚀 Starting downloads...\n")

    for grade_key in sorted(catalog['grades'].keys(), key=int):
        grade_data = catalog['grades'][grade_key]
        grade = int(grade_key)

        # Check if grade has Telugu Second Language
        if 'Telugu_Second_Language' not in grade_data['subjects']:
            continue

        subject_data = grade_data['subjects']['Telugu_Second_Language']

        # Check if Telugu medium exists
        if 'telugu' not in subject_data:
            continue

        textbook_info = subject_data['telugu']
        download_url = textbook_info['download_url']
        filename = textbook_info['filename']
        textbook_name = textbook_info['textbook_name']

        destination = output_dir / filename

        print(f"\n{'='*90}")
        print(f"CLASS {grade}")
        print(f"{'='*90}")

        # Skip if already exists
        if destination.exists():
            file_size = destination.stat().st_size
            if file_size > 100000:  # > 100KB
                print(f"\n📖 {textbook_name}")
                print(f"  ⏭️  Already exists: {filename} ({file_size / (1024*1024):.1f} MB)")
                stats['skipped'] += 1
                continue

        # Download
        print(f"\n📖 {textbook_name}")
        stats['total'] += 1

        success = download_file_from_google_drive(download_url, destination)

        if success:
            stats['success'] += 1
        else:
            stats['failed'] += 1

        # Rate limiting
        time.sleep(2)

    # Summary
    print(f"\n\n{'='*90}")
    print("DOWNLOAD SUMMARY")
    print(f"{'='*90}")
    print(f"\n📊 Statistics:")
    print(f"   Total attempted:  {stats['total']}")
    print(f"   ✅ Successful:     {stats['success']}")
    print(f"   ❌ Failed:         {stats['failed']}")
    print(f"   ⏭️  Skipped:       {stats['skipped']}")

    total_downloaded = stats['success'] + stats['skipped']
    print(f"\n✅ Total Telugu Second Language textbooks: {total_downloaded}/2")

    if stats['failed'] == 0:
        print("\n🎉 All Telugu Second Language textbooks downloaded successfully!")

    print(f"\n📁 Files saved to: {output_dir}")

    print("\n" + "=" * 90)
    print("NOTE:")
    print("=" * 90)
    print("""
Telugu Second Language (TSL) is for non-native Telugu speakers in English medium schools.
These textbooks are written in Telugu script and require tesseract-ocr-tel for OCR extraction.

TSL vs Telugu First Language (TFL):
- TFL: Comprehensive Telugu for native speakers (Grades 1-9)
- TSL: Basic/functional Telugu for learners (Grades 6-7)
""")
    print("=" * 90)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Download interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
