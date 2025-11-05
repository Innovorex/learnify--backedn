#!/usr/bin/env python3
"""
NCERT PDF Downloader
Downloads all NCERT textbook PDFs from official ncert.nic.in website
"""

import sys
import os
sys.path.insert(0, '/home/learnify/lt/learnify-teach/backend')

import requests
from pathlib import Path
from database import SessionLocal
from models import NCERTPDFSource
from ncert_catalog import get_all_textbooks
from datetime import datetime
import time


# Storage directory for downloaded PDFs
PDF_STORAGE_DIR = Path("/home/learnify/lt/learnify-teach/backend/ncert_pdfs")


def setup_storage():
    """Create storage directory structure"""
    PDF_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✅ Storage directory: {PDF_STORAGE_DIR}")


def download_pdf(url, local_path, book_name):
    """Download a single PDF file with progress tracking"""
    try:
        print(f"\n📥 Downloading: {book_name}")
        print(f"   URL: {url}")

        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"   Progress: {percent:.1f}%", end='\r')

        file_size_mb = os.path.getsize(local_path) / (1024 * 1024)
        print(f"\n   ✅ Downloaded: {file_size_mb:.2f} MB")
        return True, file_size_mb

    except Exception as e:
        print(f"\n   ❌ Error: {str(e)}")
        return False, 0


def update_database_record(db, grade, subject, book_name, pdf_url, local_path,
                          status, file_size_mb=None, error_msg=None):
    """Update or create database record for PDF source"""

    # Check if record exists
    record = db.query(NCERTPDFSource).filter(
        NCERTPDFSource.grade == grade,
        NCERTPDFSource.subject == subject
    ).first()

    if record:
        # Update existing record
        record.pdf_url = pdf_url
        record.local_path = str(local_path) if local_path else None
        record.extraction_status = status
        record.file_size_mb = file_size_mb
        record.error_message = error_msg
        record.updated_at = datetime.now()
    else:
        # Create new record
        record = NCERTPDFSource(
            grade=grade,
            subject=subject,
            book_name=book_name,
            pdf_url=pdf_url,
            local_path=str(local_path) if local_path else None,
            file_size_mb=file_size_mb,
            extraction_status=status,
            error_message=error_msg
        )
        db.add(record)

    db.commit()
    return record


def download_all_pdfs(start_grade=1, end_grade=10):
    """Download all NCERT PDFs for specified grade range"""

    setup_storage()
    db = SessionLocal()

    textbooks = get_all_textbooks()
    textbooks = [t for t in textbooks if start_grade <= t['grade'] <= end_grade]

    total = len(textbooks)
    success_count = 0
    failed_count = 0

    print(f"\n{'='*80}")
    print(f"📚 NCERT PDF Downloader")
    print(f"{'='*80}")
    print(f"Total books to download: {total}")
    print(f"Grades: {start_grade}-{end_grade}")
    print(f"{'='*80}\n")

    for idx, book in enumerate(textbooks, 1):
        grade = book['grade']
        subject = book['subject']
        book_name = book['book_name']
        pdf_url = book['pdf_url']

        print(f"\n[{idx}/{total}] Grade {grade} - {subject}")

        # Create local filename
        filename = f"grade_{grade}_{subject.replace(' ', '_').lower()}.pdf"
        local_path = PDF_STORAGE_DIR / filename

        # Skip if already downloaded
        if local_path.exists():
            file_size_mb = os.path.getsize(local_path) / (1024 * 1024)
            print(f"   ⏭️  Already exists ({file_size_mb:.2f} MB)")

            # Update database
            update_database_record(
                db, grade, subject, book_name, pdf_url,
                local_path, "downloaded", file_size_mb
            )
            success_count += 1
            continue

        # Mark as downloading in database
        update_database_record(
            db, grade, subject, book_name, pdf_url,
            None, "downloading"
        )

        # Download the PDF
        success, file_size_mb = download_pdf(pdf_url, local_path, book_name)

        if success:
            # Update database with success
            update_database_record(
                db, grade, subject, book_name, pdf_url,
                local_path, "downloaded", file_size_mb
            )
            success_count += 1
        else:
            # Update database with failure
            update_database_record(
                db, grade, subject, book_name, pdf_url,
                None, "failed", error_msg="Download failed"
            )
            failed_count += 1

        # Small delay to be respectful to NCERT servers
        time.sleep(1)

    db.close()

    # Final summary
    print(f"\n{'='*80}")
    print(f"📊 Download Summary")
    print(f"{'='*80}")
    print(f"✅ Successful: {success_count}/{total}")
    print(f"❌ Failed: {failed_count}/{total}")
    print(f"📁 Storage location: {PDF_STORAGE_DIR}")
    print(f"{'='*80}\n")


def list_downloaded():
    """List all downloaded PDFs"""
    db = SessionLocal()

    downloaded = db.query(NCERTPDFSource).filter(
        NCERTPDFSource.extraction_status == "downloaded"
    ).order_by(NCERTPDFSource.grade, NCERTPDFSource.subject).all()

    print(f"\n📚 Downloaded NCERT PDFs: {len(downloaded)}\n")
    print(f"{'Grade':<8} {'Subject':<20} {'Size (MB)':<12} {'Path'}")
    print(f"{'-'*80}")

    for pdf in downloaded:
        print(f"{pdf.grade:<8} {pdf.subject:<20} {pdf.file_size_mb:<12.2f} {Path(pdf.local_path).name}")

    db.close()


def main():
    """Main CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="NCERT PDF Downloader")
    parser.add_argument('--download', action='store_true', help='Download all PDFs')
    parser.add_argument('--grade-start', type=int, default=1, help='Start grade (default: 1)')
    parser.add_argument('--grade-end', type=int, default=10, help='End grade (default: 10)')
    parser.add_argument('--list', action='store_true', help='List downloaded PDFs')

    args = parser.parse_args()

    if args.download:
        download_all_pdfs(args.grade_start, args.grade_end)
    elif args.list:
        list_downloaded()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
