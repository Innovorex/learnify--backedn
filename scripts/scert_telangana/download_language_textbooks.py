#!/usr/bin/env python3
"""
Telangana SCERT - Language Textbooks Downloader
Downloads Telugu First Language and Hindi First/Second Language textbooks
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
    print("TELANGANA SCERT - LANGUAGE TEXTBOOKS DOWNLOAD")
    print("=" * 90)

    # Load catalog
    catalog_path = "/home/learnify/telangana_textbook_catalog_complete.json"
    with open(catalog_path, 'r') as f:
        catalog = json.load(f)

    output_dir = Path(catalog['pdf_directory'])
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📂 Output directory: {output_dir}")
    print(f"📚 Downloading: Telugu FL + Hindi FL/SL textbooks")
    print(f"📊 Total expected: 20 textbooks (~350 MB)")

    # Language subjects to download
    language_subjects = [
        'Telugu_First_Language',
        'Hindi_First_Language',
        'Hindi_Second_Language'
    ]

    stats = {
        'total': 0,
        'success': 0,
        'failed': 0,
        'skipped': 0,
        'telugu': 0,
        'hindi': 0
    }

    print(f"\n🚀 Starting downloads...\n")

    for grade_key in sorted(catalog['grades'].keys(), key=int):
        grade_data = catalog['grades'][grade_key]
        grade = int(grade_key)

        # Check if grade has language subjects
        has_language = any(subj in grade_data['subjects'] for subj in language_subjects)
        if not has_language:
            continue

        print(f"\n{'='*90}")
        print(f"CLASS {grade}")
        print(f"{'='*90}")

        for subject_name in language_subjects:
            if subject_name not in grade_data['subjects']:
                continue

            subject_data = grade_data['subjects'][subject_name]

            # Determine the medium (telugu or hindi)
            if 'Telugu' in subject_name:
                medium = 'telugu'
            elif 'Hindi' in subject_name:
                medium = 'hindi'
            else:
                continue

            if medium not in subject_data:
                continue

            textbook_info = subject_data[medium]
            download_url = textbook_info['download_url']
            filename = textbook_info['filename']
            textbook_name = textbook_info['textbook_name']

            destination = output_dir / filename

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
                if medium == 'telugu':
                    stats['telugu'] += 1
                else:
                    stats['hindi'] += 1
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

    print(f"\n📚 By Language:")
    print(f"   Telugu FL:  {stats['telugu']} textbooks")
    print(f"   Hindi FL/SL: {stats['hindi']} textbooks")

    total_downloaded = stats['success'] + stats['skipped']
    print(f"\n✅ Total language textbooks: {total_downloaded}/20")

    if stats['failed'] == 0:
        print("\n🎉 All language textbooks downloaded successfully!")

    print(f"\n📁 Files saved to: {output_dir}")

    print("\n" + "=" * 90)
    print("NEXT STEPS:")
    print("=" * 90)
    print("""
1. Install Telugu OCR (if not already installed):
   sudo apt-get install tesseract-ocr-tel

2. Verify Hindi OCR is installed:
   tesseract --list-langs | grep hin

3. Extract content with OCR (similar to CBSE Hindi extraction)

4. Save to database with board='TELANGANA'
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
