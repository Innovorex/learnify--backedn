#!/bin/bash
#
# EXTRACT MISSING CHAPTERS - Using Corrected URL Patterns
# Extracts the 111 missing chapters with verified working URLs
#

set -e

echo "========================================================================"
echo "🔧 EXTRACTING MISSING NCERT CHAPTERS - CORRECTED PATTERNS"
echo "========================================================================"
echo "Starting at: $(date)"
echo ""

PDFS_DIR="../../../ncert_pdfs"
LOGS_DIR="./extraction_logs"
mkdir -p "$PDFS_DIR"
mkdir -p "$LOGS_DIR"

TOTAL_ATTEMPTED=0
TOTAL_SUCCESS=0
TOTAL_FAILED=0

# Extract function
extract_chapter() {
    local url=$1
    local filename=$2
    local grade=$3
    local subject=$4
    local chapter_num=$5

    TOTAL_ATTEMPTED=$((TOTAL_ATTEMPTED + 1))

    echo "[$TOTAL_ATTEMPTED] Grade $grade $subject Ch.$chapter_num..."

    if curl -k -s -L -o "$PDFS_DIR/$filename" "$url" 2>/dev/null; then
        if file "$PDFS_DIR/$filename" | grep -q "PDF"; then
            echo "  ✅ Downloaded"

            if python3 extract_chapter.py "$PDFS_DIR/$filename" "$grade" "$subject" "$chapter_num" >> "$LOGS_DIR/missing_${grade}_${subject}_${chapter_num}.log" 2>&1; then
                echo "  ✅ Extracted"
                TOTAL_SUCCESS=$((TOTAL_SUCCESS + 1))
                return 0
            else
                echo "  ⚠️  Extraction failed"
                TOTAL_FAILED=$((TOTAL_FAILED + 1))
                return 1
            fi
        fi
    fi

    echo "  ❌ Download failed"
    TOTAL_FAILED=$((TOTAL_FAILED + 1))
    return 1
}

# ==========================================================================
# PRIORITY 1: Grade 10 English First Flight (VERIFIED PATTERN)
# ==========================================================================
echo "📚 PRIORITY 1: Grade 10 English First Flight"
echo "Pattern: jeff1XX (VERIFIED)"
echo ""

for ch in {01..11}; do
    extract_chapter \
        "https://ncert.nic.in/textbook/pdf/jeff1${ch}.pdf" \
        "grade10_english_first_flight_ch${ch}.pdf" \
        10 "English_First_Flight" $((10#$ch))
    sleep 0.5
done

# ==========================================================================
# PRIORITY 2: Grade 10 Hindi Books (VERIFIED PATTERNS)
# ==========================================================================
echo ""
echo "📚 PRIORITY 2: Grade 10 Hindi Kshitij (17 chapters)"
echo ""

for ch in {01..17}; do
    extract_chapter \
        "https://ncert.nic.in/textbook/pdf/jhks1${ch}.pdf" \
        "grade10_hindi_kshitij_ch${ch}.pdf" \
        10 "Hindi_Kshitij" $((10#$ch))
    sleep 0.5
done

echo ""
echo "📚 Grade 10 Hindi Sparsh (17 chapters)"
echo ""

for ch in {01..17}; do
    extract_chapter \
        "https://ncert.nic.in/textbook/pdf/jhsp1${ch}.pdf" \
        "grade10_hindi_sparsh_ch${ch}.pdf" \
        10 "Hindi_Sparsh" $((10#$ch))
    sleep 0.5
done

echo ""
echo "📚 Grade 10 Hindi Kritika (5 chapters)"
echo ""

for ch in {01..05}; do
    extract_chapter \
        "https://ncert.nic.in/textbook/pdf/jhkr1${ch}.pdf" \
        "grade10_hindi_kritika_ch${ch}.pdf" \
        10 "Hindi_Kritika" $((10#$ch))
    sleep 0.5
done

# ==========================================================================
# PRIORITY 3: Grade 6 Math & Science (VERIFIED PATTERNS)
# ==========================================================================
echo ""
echo "📚 PRIORITY 3: Grade 6 Mathematics - Ganita Prakash (8 chapters)"
echo ""

for ch in {01..08}; do
    extract_chapter \
        "https://ncert.nic.in/textbook/pdf/fegp1${ch}.pdf" \
        "grade6_math_ganita_prakash_ch${ch}.pdf" \
        6 "Mathematics" $((10#$ch))
    sleep 0.5
done

echo ""
echo "📚 Grade 6 Science - Curiosity (12 chapters)"
echo ""

for ch in {01..12}; do
    extract_chapter \
        "https://ncert.nic.in/textbook/pdf/fecu1${ch}.pdf" \
        "grade6_science_curiosity_ch${ch}.pdf" \
        6 "Science" $((10#$ch))
    sleep 0.5
done

# ==========================================================================
# PRIORITY 4: Grade 1-2 Math & English (VERIFIED PATTERNS)
# ==========================================================================
echo ""
echo "📚 PRIORITY 4: Grade 1 Mathematics - Joyful (13 chapters)"
echo ""

for ch in {01..13}; do
    extract_chapter \
        "https://ncert.nic.in/textbook/pdf/aejm1${ch}.pdf" \
        "grade1_math_joyful_ch${ch}.pdf" \
        1 "Mathematics" $((10#$ch))
    sleep 0.5
done

echo ""
echo "📚 Grade 1 English Marigold (10 chapters)"
echo ""

for ch in {01..10}; do
    extract_chapter \
        "https://ncert.nic.in/textbook/pdf/aemr1${ch}.pdf" \
        "grade1_english_marigold_ch${ch}.pdf" \
        1 "English_Marigold" $((10#$ch))
    sleep 0.5
done

echo ""
echo "📚 Grade 2 Mathematics - Joyful (15 chapters)"
echo ""

for ch in {01..15}; do
    extract_chapter \
        "https://ncert.nic.in/textbook/pdf/bejm1${ch}.pdf" \
        "grade2_math_joyful_ch${ch}.pdf" \
        2 "Mathematics" $((10#$ch))
    sleep 0.5
done

echo ""
echo "📚 Grade 2 English Marigold (10 chapters)"
echo ""

for ch in {01..10}; do
    extract_chapter \
        "https://ncert.nic.in/textbook/pdf/bemr1${ch}.pdf" \
        "grade2_english_marigold_ch${ch}.pdf" \
        2 "English_Marigold" $((10#$ch))
    sleep 0.5
done

# ==========================================================================
# PRIORITY 5: Grade 5 Hindi & EVS (VERIFIED PATTERNS)
# ==========================================================================
echo ""
echo "📚 PRIORITY 5: Grade 5 Hindi (18 chapters)"
echo ""

for ch in {01..18}; do
    extract_chapter \
        "https://ncert.nic.in/textbook/pdf/ehhn1${ch}.pdf" \
        "grade5_hindi_ch${ch}.pdf" \
        5 "Hindi" $((10#$ch))
    sleep 0.5
done

echo ""
echo "📚 Grade 5 EVS (22 chapters)"
echo ""

for ch in {01..22}; do
    extract_chapter \
        "https://ncert.nic.in/textbook/pdf/eeen1${ch}.pdf" \
        "grade5_evs_ch${ch}.pdf" \
        5 "EVS" $((10#$ch))
    sleep 0.5
done

# ==========================================================================
# SUMMARY
# ==========================================================================
echo ""
echo "========================================================================"
echo "📊 EXTRACTION SUMMARY"
echo "========================================================================"
echo "Attempted: $TOTAL_ATTEMPTED"
echo "Success: $TOTAL_SUCCESS"
echo "Failed: $TOTAL_FAILED"
if [ $TOTAL_ATTEMPTED -gt 0 ]; then
    SUCCESS_RATE=$(( TOTAL_SUCCESS * 100 / TOTAL_ATTEMPTED ))
    echo "Success Rate: ${SUCCESS_RATE}%"
fi
echo "========================================================================"
echo "Completed at: $(date)"
echo ""
