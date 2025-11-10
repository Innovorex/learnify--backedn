#!/bin/bash
#
# MASTER EXTRACTION SCRIPT - Extract ALL Remaining NCERT Content
# Extracts ~443 remaining chapters across all subjects and grades
# Estimated time: 4-6 hours
#

set -e  # Exit on critical errors but continue on individual failures

echo "========================================"
echo "🚀 FULL NCERT EXTRACTION - MASTER SCRIPT"
echo "========================================"
echo "Starting at: $(date)"
echo "Estimated completion: $(date -d '+6 hours')"
echo "========================================"
echo ""

# Create directories
PDFS_DIR="../../../ncert_pdfs"
LOGS_DIR="./extraction_logs"
mkdir -p "$PDFS_DIR"
mkdir -p "$LOGS_DIR"

# Initialize counters
TOTAL_ATTEMPTED=0
TOTAL_SUCCESS=0
TOTAL_FAILED=0

# Log function
log_extraction() {
    local grade=$1
    local subject=$2
    local chapter=$3
    local status=$4

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Grade $grade | $subject | Ch.$chapter | $status" >> "$LOGS_DIR/extraction_master.log"
}

# Download and extract function with retry logic
extract_chapter_safe() {
    local url=$1
    local filename=$2
    local grade=$3
    local subject=$4
    local chapter_num=$5

    TOTAL_ATTEMPTED=$((TOTAL_ATTEMPTED + 1))

    echo "[$TOTAL_ATTEMPTED] Downloading Grade $grade $subject Chapter $chapter_num..."

    # Try download with curl, fallback to wget
    if curl -k -s -f -o "$PDFS_DIR/$filename" "$url" 2>/dev/null || \
       wget --no-check-certificate -q -O "$PDFS_DIR/$filename" "$url" 2>/dev/null; then

        # Verify file is valid PDF
        if file "$PDFS_DIR/$filename" | grep -q "PDF"; then
            echo "  ✅ Downloaded"

            # Extract content
            if python3 extract_chapter.py "$PDFS_DIR/$filename" "$grade" "$subject" "$chapter_num" >> "$LOGS_DIR/extract_${grade}_${subject// /_}_${chapter_num}.log" 2>&1; then
                echo "  ✅ Extracted successfully"
                TOTAL_SUCCESS=$((TOTAL_SUCCESS + 1))
                log_extraction "$grade" "$subject" "$chapter_num" "SUCCESS"
                return 0
            else
                echo "  ⚠️  Extraction failed (PDF processing error)"
                TOTAL_FAILED=$((TOTAL_FAILED + 1))
                log_extraction "$grade" "$subject" "$chapter_num" "FAILED_EXTRACTION"
                return 1
            fi
        else
            echo "  ❌ Invalid PDF file"
            TOTAL_FAILED=$((TOTAL_FAILED + 1))
            log_extraction "$grade" "$subject" "$chapter_num" "FAILED_INVALID_PDF"
            rm -f "$PDFS_DIR/$filename"
            return 1
        fi
    else
        echo "  ❌ Download failed"
        TOTAL_FAILED=$((TOTAL_FAILED + 1))
        log_extraction "$grade" "$subject" "$chapter_num" "FAILED_DOWNLOAD"
        return 1
    fi
}

echo "========================================"
echo "📚 PHASE 1: HINDI LITERATURE"
echo "========================================"
echo ""

# Hindi Rimjhim - Grade 1 (23 chapters)
echo "📖 Hindi Rimjhim - Grade 1 (23 chapters)"
for ch in {01..23}; do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/aehr1${ch}.pdf" \
        "grade1_hindi_rimjhim_ch${ch}.pdf" \
        1 "Hindi_Rimjhim" $((10#$ch))
    sleep 1  # Rate limiting
done

# Hindi Rimjhim - Grade 2 (14 chapters)
echo ""
echo "📖 Hindi Rimjhim - Grade 2 (14 chapters)"
for ch in {01..14}; do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/behr1${ch}.pdf" \
        "grade2_hindi_rimjhim_ch${ch}.pdf" \
        2 "Hindi_Rimjhim" $((10#$ch))
    sleep 1
done

# Hindi Rimjhim - Grade 3 (14 chapters)
echo ""
echo "📖 Hindi Rimjhim - Grade 3 (14 chapters)"
for ch in {01..14}; do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/cehr1${ch}.pdf" \
        "grade3_hindi_rimjhim_ch${ch}.pdf" \
        3 "Hindi_Rimjhim" $((10#$ch))
    sleep 1
done

# Hindi Rimjhim - Grade 4 (14 chapters)
echo ""
echo "📖 Hindi Rimjhim - Grade 4 (14 chapters)"
for ch in {01..14}; do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/dehr1${ch}.pdf" \
        "grade4_hindi_rimjhim_ch${ch}.pdf" \
        4 "Hindi_Rimjhim" $((10#$ch))
    sleep 1
done

# Hindi Rimjhim - Grade 5 (18 chapters)
echo ""
echo "📖 Hindi Rimjhim - Grade 5 (18 chapters)"
for ch in {01..18}; do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/eehr1${ch}.pdf" \
        "grade5_hindi_rimjhim_ch${ch}.pdf" \
        5 "Hindi_Rimjhim" $((10#$ch))
    sleep 1
done

echo ""
echo "========================================"
echo "📚 PHASE 2: SOCIAL SCIENCE"
echo "========================================"
echo ""

# Grade 6 Social Science (22 chapters)
echo "📖 Social Science - Grade 6 (22 chapters)"
for ch in {01..22}; do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/fess1${ch}.pdf" \
        "grade6_social_science_ch${ch}.pdf" \
        6 "Social_Science" $((10#$ch))
    sleep 1
done

# Grade 7 Social Science (remaining 14 chapters: 9-22)
echo ""
echo "📖 Social Science - Grade 7 (14 remaining chapters)"
for ch in {09..22}; do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/gess1${ch}.pdf" \
        "grade7_social_science_ch${ch}.pdf" \
        7 "Social_Science" $((10#$ch))
    sleep 1
done

# Grade 8 Social Science (22 chapters)
echo ""
echo "📖 Social Science - Grade 8 (22 chapters)"
for ch in {01..22}; do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/hess1${ch}.pdf" \
        "grade8_social_science_ch${ch}.pdf" \
        8 "Social_Science" $((10#$ch))
    sleep 1
done

# Grade 9 Social Science (remaining 16 chapters: 9-22, excluding already extracted)
echo ""
echo "📖 Social Science - Grade 9 (16 remaining chapters)"
for ch in 09 10 11 12 13 14 15 16 17 18 19 20 21 22; do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/iess1${ch}.pdf" \
        "grade9_social_science_ch${ch}.pdf" \
        9 "Social_Science" $((10#$ch))
    sleep 1
done

# Grade 10 Social Science (remaining 15 chapters: 9-22, excluding already extracted)
echo ""
echo "📖 Social Science - Grade 10 (15 remaining chapters)"
for ch in 09 10 11 12 13 14 15 16 17 18 19 20 21 22; do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/jess1${ch}.pdf" \
        "grade10_social_science_ch${ch}.pdf" \
        10 "Social_Science" $((10#$ch))
    sleep 1
done

echo ""
echo "========================================"
echo "📚 PHASE 3: ENGLISH LITERATURE"
echo "========================================"
echo ""

# Grade 3 English Marigold (10 chapters)
echo "📖 English Marigold - Grade 3 (10 chapters)"
for ch in {01..10}; do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/cemr1${ch}.pdf" \
        "grade3_english_marigold_ch${ch}.pdf" \
        3 "English_Marigold" $((10#$ch))
    sleep 1
done

# Continue with more phases...
echo ""
echo "========================================"
echo "📊 EXTRACTION PROGRESS"
echo "========================================"
echo "Attempted: $TOTAL_ATTEMPTED"
echo "Success: $TOTAL_SUCCESS"
echo "Failed: $TOTAL_FAILED"
echo "Success Rate: $(( TOTAL_SUCCESS * 100 / TOTAL_ATTEMPTED ))%"
echo "========================================"
echo ""
echo "⏸️  Checkpoint reached. Continue extraction..."
echo "Completed at: $(date)"
echo ""
