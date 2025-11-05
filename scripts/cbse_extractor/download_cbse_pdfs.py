#!/usr/bin/env python3
"""
CBSE PDF Downloader - Automated download of official CBSE syllabus PDFs
Downloads from: https://cbseacademic.nic.in/
"""

import requests
import hashlib
import time
import json
from pathlib import Path
from datetime import datetime

class CBSEPDFDownloader:
    """Downloads official CBSE syllabus PDFs for Grades 9-10"""

    BASE_URL = "https://cbseacademic.nic.in/web_material/CurriculumMain25/Sec"

    # Official CBSE Syllabus PDF URLs (2024-25)
    SYLLABUS_URLS = {
        "9": {
            "Mathematics": f"{BASE_URL}/Maths_IX_2024-25.pdf",
            "Science": f"{BASE_URL}/Science_IX_2024-25.pdf",
            "Social_Science": f"{BASE_URL}/SocialScience_IX_2024-25.pdf",
            "English": f"{BASE_URL}/English_IX_2024-25.pdf",
            "Hindi": f"{BASE_URL}/HindiA_IX_2024-25.pdf"
        },
        "10": {
            "Mathematics": f"{BASE_URL}/Maths_X_2024-25.pdf",
            "Science": f"{BASE_URL}/Science_X_2024-25.pdf",
            "Social_Science": f"{BASE_URL}/SocialScience_X_2024-25.pdf",
            "English": f"{BASE_URL}/English_X_2024-25.pdf",
            "Hindi": f"{BASE_URL}/HindiA_X_2024-25.pdf"
        }
    }

    def __init__(self, output_dir="scripts/cbse_extractor/data/cbse_pdfs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metadata = {}
        self.log_file = Path("scripts/cbse_extractor/logs/download_log.txt")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(self, message):
        """Log message to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)

        with open(self.log_file, 'a') as f:
            f.write(log_msg + "\n")

    def download_all(self):
        """Download all CBSE PDFs for grades 9-10"""

        self.log("="*80)
        self.log("CBSE PDF DOWNLOADER - STARTING")
        self.log("="*80)

        downloaded = {}
        total = sum(len(subjects) for subjects in self.SYLLABUS_URLS.values())
        current = 0

        for grade, subjects in self.SYLLABUS_URLS.items():
            self.log(f"\n📚 Grade {grade}:")

            for subject, url in subjects.items():
                current += 1
                self.log(f"\n[{current}/{total}] {subject}...")

                try:
                    filepath = self._download_pdf(grade, subject, url)
                    downloaded[f"{grade}_{subject}"] = str(filepath)
                    self.log(f"  ✅ Downloaded successfully")
                    time.sleep(2)  # Rate limiting to be respectful

                except Exception as e:
                    self.log(f"  ❌ Failed: {e}")
                    downloaded[f"{grade}_{subject}"] = None

        # Save metadata
        self._save_metadata()

        # Summary
        success_count = sum(1 for v in downloaded.values() if v is not None)
        self.log(f"\n{'='*80}")
        self.log(f"DOWNLOAD COMPLETE: {success_count}/{total} successful")
        self.log(f"{'='*80}")

        return downloaded

    def _download_pdf(self, grade, subject, url):
        """Download single PDF with verification"""

        filename = f"CBSE_Grade_{grade}_{subject}_2024-25.pdf"
        filepath = self.output_dir / filename

        # Check if already exists and valid
        if filepath.exists():
            if self._verify_pdf(filepath):
                self.log(f"  ⚡ Using cached version (valid)")
                return filepath
            else:
                self.log(f"  ⚠️  Cached file invalid, re-downloading...")

        # Download with retry
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.log(f"  📥 Downloading from {url}")

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }

                response = requests.get(url, headers=headers, timeout=60, stream=True)
                response.raise_for_status()

                # Save
                total_size = int(response.headers.get('content-length', 0))
                self.log(f"  📊 Size: {total_size / 1024 / 1024:.2f} MB")

                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                # Verify
                if not self._verify_pdf(filepath):
                    raise ValueError("Downloaded PDF is invalid")

                # Calculate checksum
                checksum = self._calculate_checksum(filepath)

                # Store metadata
                self.metadata[f"{grade}_{subject}"] = {
                    "grade": grade,
                    "subject": subject,
                    "filename": filename,
                    "url": url,
                    "size_bytes": filepath.stat().st_size,
                    "checksum_sha256": checksum,
                    "downloaded_at": datetime.now().isoformat()
                }

                return filepath

            except Exception as e:
                if attempt < max_retries - 1:
                    self.log(f"  ⚠️  Attempt {attempt + 1} failed, retrying...")
                    time.sleep(5)
                else:
                    raise

    def _verify_pdf(self, filepath):
        """Verify PDF is valid"""
        try:
            # Check file size
            if filepath.stat().st_size < 1000:
                return False

            # Check PDF header
            with open(filepath, 'rb') as f:
                header = f.read(5)
                if header != b'%PDF-':
                    return False

            # Try to parse with PyPDF2
            try:
                import PyPDF2
                with open(filepath, 'rb') as f:
                    PyPDF2.PdfReader(f)
            except:
                return False

            return True

        except Exception as e:
            self.log(f"  ⚠️  Verification error: {e}")
            return False

    def _calculate_checksum(self, filepath):
        """Calculate SHA-256 checksum"""
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _save_metadata(self):
        """Save download metadata to JSON"""
        metadata_file = self.output_dir / "download_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
        self.log(f"\n💾 Metadata saved to: {metadata_file}")

def main():
    """Main execution"""
    downloader = CBSEPDFDownloader()
    downloaded_files = downloader.download_all()

    # Print summary
    print("\n" + "="*80)
    print("DOWNLOADED FILES:")
    print("="*80)
    for key, filepath in downloaded_files.items():
        if filepath:
            print(f"✅ {key}: {filepath}")
        else:
            print(f"❌ {key}: FAILED")

if __name__ == "__main__":
    main()
