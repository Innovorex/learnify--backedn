#!/usr/bin/env python3
"""
Retry downloading missing and corrupted Telangana textbooks
"""

import requests
import os
from pathlib import Path
import time

# Base directory for PDFs
PDF_DIR = Path("/home/learnify/lt/learnify-teach/backend/ts_pdfs")

# Base URL for SCERT Telangana textbooks
BASE_URL = "https://scert.telangana.gov.in/downloads"

# Files to retry (missing + corrupted)
FILES_TO_DOWNLOAD = {
    # Missing English subject books
    "grade2_english.pdf": f"{BASE_URL}/class2/english.pdf",
    "grade3_english.pdf": f"{BASE_URL}/class3/english.pdf", 
    "grade4_english.pdf": f"{BASE_URL}/class4/english.pdf",
    
    # Corrupted files - retry
    "grade5_sanskrit_english.pdf": f"{BASE_URL}/class5/sanskrit.pdf",
    "grade8_biological_science_english.pdf": f"{BASE_URL}/class8/biological_science.pdf",
    "grade8_social_studies_english.pdf": f"{BASE_URL}/class8/social_studies.pdf",
}

def download_file(url, filepath):
    """Download a file with retry logic"""
    try:
        print(f"Downloading: {filepath.name}")
        print(f"  URL: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30, stream=True)
        
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            
            with open(filepath, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
            
            file_size = os.path.getsize(filepath)
            file_size_mb = file_size / (1024 * 1024)
            
            if file_size > 1024:  # At least 1KB
                print(f"  ✅ Downloaded: {file_size_mb:.2f} MB")
                return True
            else:
                print(f"  ❌ Failed: File too small ({file_size} bytes)")
                return False
        else:
            print(f"  ❌ Failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    print("=" * 80)
    print("TELANGANA - RETRY MISSING & CORRUPTED FILES")
    print("=" * 80)
    print()
    
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    failed_count = 0
    failed_files = []
    
    for filename, url in FILES_TO_DOWNLOAD.items():
        filepath = PDF_DIR / filename
        
        # Backup corrupted file if exists
        if filepath.exists() and os.path.getsize(filepath) < 10240:  # Less than 10KB
            backup_path = filepath.with_suffix('.pdf.corrupted')
            filepath.rename(backup_path)
            print(f"Backed up corrupted file: {backup_path.name}")
        
        if download_file(url, filepath):
            success_count += 1
        else:
            failed_count += 1
            failed_files.append(filename)
        
        time.sleep(2)  # Be nice to the server
        print()
    
    print("=" * 80)
    print("DOWNLOAD SUMMARY")
    print("=" * 80)
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed:     {failed_count}")
    
    if failed_files:
        print("\nFailed files:")
        for f in failed_files:
            print(f"  - {f}")

if __name__ == "__main__":
    main()
