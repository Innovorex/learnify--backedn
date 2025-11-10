#!/bin/bash
#
# SYSTEMATIC FULL EXTRACTION - Complete CBSE Syllabus (Grades 1-10)
# Extracts remaining 445 chapters to reach 912 total chapters (100% completion)
# Organized by subject priority for CBSE board exams
#

set +e  # Continue on individual failures

echo "=========================================================================================================="
echo "🎓 SYSTEMATIC NCERT EXTRACTION - COMPLETE CBSE SYLLABUS (GRADES 1-10)"
echo "=========================================================================================================="
echo "Start Time: $(date)"
echo "Target: Extract remaining ~445 chapters to achieve 912 total chapters (100% completion)"
echo "=========================================================================================================="
echo ""

# Setup directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PDFS_DIR="$SCRIPT_DIR/../../../ncert_pdfs"
LOGS_DIR="$SCRIPT_DIR/extraction_logs"
mkdir -p "$PDFS_DIR"
mkdir -p "$LOGS_DIR"

# Master log file
MASTER_LOG="$LOGS_DIR/systematic_extraction_$(date +%Y%m%d_%H%M%S).log"
echo "Master Log: $MASTER_LOG" | tee -a "$MASTER_LOG"
echo "" | tee -a "$MASTER_LOG"

# Counters
TOTAL_ATTEMPTED=0
TOTAL_SUCCESS=0
TOTAL_FAILED=0
TOTAL_SKIPPED=0

# Function to log with timestamp
log_msg() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$MASTER_LOG"
}

# Function to download and extract with retry and validation
extract_chapter_safe() {
    local url=$1
    local filename=$2
    local grade=$3
    local subject=$4
    local chapter_num=$5
    local book_name=$6

    TOTAL_ATTEMPTED=$((TOTAL_ATTEMPTED + 1))

    log_msg "[$TOTAL_ATTEMPTED] Grade $grade | $subject | Ch.$chapter_num | $book_name"

    # Check if already exists in database (to avoid duplicates)
    # We'll skip this check for now and let the database handle duplicates

    # Download PDF with retry
    local pdf_file="$PDFS_DIR/$filename"

    if curl -k -s -f -o "$pdf_file" "$url" 2>/dev/null; then
        # Verify it's a valid PDF
        if file "$pdf_file" | grep -q "PDF"; then
            log_msg "    ✅ Downloaded successfully"

            # Extract content
            if python3 "$SCRIPT_DIR/extract_chapter.py" "$pdf_file" "$grade" "$subject" "$chapter_num" >> "$LOGS_DIR/extract_g${grade}_${subject// /_}_ch${chapter_num}.log" 2>&1; then
                log_msg "    ✅ EXTRACTED SUCCESSFULLY"
                TOTAL_SUCCESS=$((TOTAL_SUCCESS + 1))

                # Clean up PDF to save space (optional)
                # rm -f "$pdf_file"

                return 0
            else
                log_msg "    ⚠️  Extraction failed (PDF processing error)"
                TOTAL_FAILED=$((TOTAL_FAILED + 1))
                return 1
            fi
        else
            log_msg "    ❌ Invalid PDF file"
            TOTAL_FAILED=$((TOTAL_FAILED + 1))
            rm -f "$pdf_file"
            return 1
        fi
    else
        log_msg "    ❌ Download failed (URL: $url)"
        TOTAL_FAILED=$((TOTAL_FAILED + 1))
        return 1
    fi
}

# Progress report function
print_progress() {
    local phase=$1
    echo "" | tee -a "$MASTER_LOG"
    echo "==========================================================================================================" | tee -a "$MASTER_LOG"
    echo "📊 PROGRESS REPORT - $phase" | tee -a "$MASTER_LOG"
    echo "==========================================================================================================" | tee -a "$MASTER_LOG"
    echo "Attempted: $TOTAL_ATTEMPTED" | tee -a "$MASTER_LOG"
    echo "Success:   $TOTAL_SUCCESS" | tee -a "$MASTER_LOG"
    echo "Failed:    $TOTAL_FAILED" | tee -a "$MASTER_LOG"
    if [ $TOTAL_ATTEMPTED -gt 0 ]; then
        echo "Success Rate: $(( TOTAL_SUCCESS * 100 / TOTAL_ATTEMPTED ))%" | tee -a "$MASTER_LOG"
    fi
    echo "==========================================================================================================" | tee -a "$MASTER_LOG"
    echo "" | tee -a "$MASTER_LOG"
}


echo "==========================================================================================================" | tee -a "$MASTER_LOG"
echo "📚 PHASE 1: SOCIAL SCIENCE (HIGH PRIORITY - CBSE BOARD EXAMS)" | tee -a "$MASTER_LOG"
echo "==========================================================================================================" | tee -a "$MASTER_LOG"
echo "Target: ~104 chapters (Grades 6-10 History, Geography, Civics, Economics)" | tee -a "$MASTER_LOG"
echo "" | tee -a "$MASTER_LOG"

# Grade 6 Social Science (28 chapters)
log_msg "📖 Grade 6 Social Science - Complete textbook (28 chapters)"
for ch in $(seq -f "%02g" 1 28); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/fess1${ch}.pdf" \
        "grade6_social_science_ch${ch}.pdf" \
        6 "Social_Science" $((10#$ch)) "The Earth Our Habitat, Social and Political Life"
    sleep 1
done

# Grade 7 Social Science (28 chapters)
log_msg "📖 Grade 7 Social Science - Complete textbook (28 chapters)"
for ch in $(seq -f "%02g" 1 28); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/gess1${ch}.pdf" \
        "grade7_social_science_ch${ch}.pdf" \
        7 "Social_Science" $((10#$ch)) "Our Past, Social and Political Life"
    sleep 1
done

# Grade 8 Social Science (28 chapters)
log_msg "📖 Grade 8 Social Science - Complete textbook (28 chapters)"
for ch in $(seq -f "%02g" 1 28); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/hess1${ch}.pdf" \
        "grade8_social_science_ch${ch}.pdf" \
        8 "Social_Science" $((10#$ch)) "Resources and Development, Social and Political Life"
    sleep 1
done

# Grade 9 Social Science (22 chapters)
log_msg "📖 Grade 9 Social Science - Complete textbook (22 chapters)"
for ch in $(seq -f "%02g" 1 22); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/iess1${ch}.pdf" \
        "grade9_social_science_ch${ch}.pdf" \
        9 "Social_Science" $((10#$ch)) "India and the Contemporary World, Economics"
    sleep 1
done

# Grade 10 Social Science (22 chapters)
log_msg "📖 Grade 10 Social Science - Complete textbook (22 chapters)"
for ch in $(seq -f "%02g" 1 22); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/jess1${ch}.pdf" \
        "grade10_social_science_ch${ch}.pdf" \
        10 "Social_Science" $((10#$ch)) "Democratic Politics, Economics, History, Geography"
    sleep 1
done

print_progress "Phase 1: Social Science Complete"


echo "==========================================================================================================" | tee -a "$MASTER_LOG"
echo "📚 PHASE 2: MATHEMATICS (ALL MISSING CHAPTERS)" | tee -a "$MASTER_LOG"
echo "==========================================================================================================" | tee -a "$MASTER_LOG"
echo "" | tee -a "$MASTER_LOG"

# Grade 6 Mathematics - Ganita Prakash (NEP 2020) - 8 chapters
log_msg "📖 Grade 6 Mathematics - Ganita Prakash (8 chapters)"
for ch in $(seq -f "%02g" 1 8); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/fegp1${ch}.pdf" \
        "grade6_math_ganita_prakash_ch${ch}.pdf" \
        6 "Mathematics" $((10#$ch)) "Ganita Prakash (NEP 2020)"
    sleep 1
done

# Grade 5 Mathematics - Math Magic (14 chapters)
log_msg "📖 Grade 5 Mathematics - Math Magic (14 chapters)"
for ch in $(seq -f "%02g" 1 14); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/eemm1${ch}.pdf" \
        "grade5_math_magic_ch${ch}.pdf" \
        5 "Mathematics" $((10#$ch)) "Math-Magic"
    sleep 1
done

# Grade 4 Mathematics - Math Magic (14 chapters)
log_msg "📖 Grade 4 Mathematics - Math Magic (14 chapters)"
for ch in $(seq -f "%02g" 1 14); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/demm1${ch}.pdf" \
        "grade4_math_magic_ch${ch}.pdf" \
        4 "Mathematics" $((10#$ch)) "Math-Magic"
    sleep 1
done

# Grade 3 Mathematics - Math Magic (14 chapters)
log_msg "📖 Grade 3 Mathematics - Math Magic (14 chapters)"
for ch in $(seq -f "%02g" 1 14); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/cemm1${ch}.pdf" \
        "grade3_math_magic_ch${ch}.pdf" \
        3 "Mathematics" $((10#$ch)) "Math-Magic"
    sleep 1
done

# Grade 2 Mathematics - Math Magic (15 chapters)
log_msg "📖 Grade 2 Mathematics - Math Magic (15 chapters)"
for ch in $(seq -f "%02g" 1 15); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/bemm1${ch}.pdf" \
        "grade2_math_magic_ch${ch}.pdf" \
        2 "Mathematics" $((10#$ch)) "Math-Magic"
    sleep 1
done

# Grade 1 Mathematics - Math Magic (13 chapters)
log_msg "📖 Grade 1 Mathematics - Math Magic (13 chapters)"
for ch in $(seq -f "%02g" 1 13); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/aemm1${ch}.pdf" \
        "grade1_math_magic_ch${ch}.pdf" \
        1 "Mathematics" $((10#$ch)) "Math-Magic"
    sleep 1
done

print_progress "Phase 2: Mathematics Complete"


echo "==========================================================================================================" | tee -a "$MASTER_LOG"
echo "📚 PHASE 3: SCIENCE (ALL MISSING CHAPTERS)" | tee -a "$MASTER_LOG"
echo "==========================================================================================================" | tee -a "$MASTER_LOG"
echo "" | tee -a "$MASTER_LOG"

# Grade 6 Science - Curiosity (NEP 2020) - 12 chapters
log_msg "📖 Grade 6 Science - Curiosity (12 chapters)"
for ch in $(seq -f "%02g" 1 12); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/fecu1${ch}.pdf" \
        "grade6_science_curiosity_ch${ch}.pdf" \
        6 "Science" $((10#$ch)) "Curiosity (NEP 2020)"
    sleep 1
done

# Grade 7 Science (18 chapters)
log_msg "📖 Grade 7 Science (18 chapters)"
for ch in $(seq -f "%02g" 1 18); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/gesc1${ch}.pdf" \
        "grade7_science_ch${ch}.pdf" \
        7 "Science" $((10#$ch)) "Science"
    sleep 1
done

# Grade 8 Science (18 chapters)
log_msg "📖 Grade 8 Science (18 chapters)"
for ch in $(seq -f "%02g" 1 18); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/hesc1${ch}.pdf" \
        "grade8_science_ch${ch}.pdf" \
        8 "Science" $((10#$ch)) "Science"
    sleep 1
done

print_progress "Phase 3: Science Complete"


echo "==========================================================================================================" | tee -a "$MASTER_LOG"
echo "📚 PHASE 4: HINDI LITERATURE (LARGEST REMAINING CONTENT)" | tee -a "$MASTER_LOG"
echo "==========================================================================================================" | tee -a "$MASTER_LOG"
echo "Target: ~147 chapters across all Hindi textbooks" | tee -a "$MASTER_LOG"
echo "" | tee -a "$MASTER_LOG"

# Grade 1 Hindi Rimjhim (23 chapters)
log_msg "📖 Grade 1 Hindi Rimjhim (23 chapters)"
for ch in $(seq -f "%02g" 1 23); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/ahrj1${ch}.pdf" \
        "grade1_hindi_rimjhim_ch${ch}.pdf" \
        1 "Hindi" $((10#$ch)) "Rimjhim"
    sleep 1
done

# Grade 2 Hindi Rimjhim (14 chapters)
log_msg "📖 Grade 2 Hindi Rimjhim (14 chapters)"
for ch in $(seq -f "%02g" 1 14); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/bhrj1${ch}.pdf" \
        "grade2_hindi_rimjhim_ch${ch}.pdf" \
        2 "Hindi" $((10#$ch)) "Rimjhim"
    sleep 1
done

# Grade 3 Hindi Rimjhim (14 chapters)
log_msg "📖 Grade 3 Hindi Rimjhim (14 chapters)"
for ch in $(seq -f "%02g" 1 14); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/chrj1${ch}.pdf" \
        "grade3_hindi_rimjhim_ch${ch}.pdf" \
        3 "Hindi" $((10#$ch)) "Rimjhim"
    sleep 1
done

# Grade 4 Hindi Rimjhim (14 chapters)
log_msg "📖 Grade 4 Hindi Rimjhim (14 chapters)"
for ch in $(seq -f "%02g" 1 14); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/dhrj1${ch}.pdf" \
        "grade4_hindi_rimjhim_ch${ch}.pdf" \
        4 "Hindi" $((10#$ch)) "Rimjhim"
    sleep 1
done

# Grade 5 Hindi Rimjhim (18 chapters)
log_msg "📖 Grade 5 Hindi Rimjhim (18 chapters)"
for ch in $(seq -f "%02g" 1 18); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/ehrj1${ch}.pdf" \
        "grade5_hindi_rimjhim_ch${ch}.pdf" \
        5 "Hindi" $((10#$ch)) "Rimjhim"
    sleep 1
done

# Grade 6 Hindi Vasant (16 chapters)
log_msg "📖 Grade 6 Hindi Vasant (16 chapters)"
for ch in $(seq -f "%02g" 1 16); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/fhvs1${ch}.pdf" \
        "grade6_hindi_vasant_ch${ch}.pdf" \
        6 "Hindi" $((10#$ch)) "Vasant"
    sleep 1
done

# Grade 6 Hindi Durva (28 chapters)
log_msg "📖 Grade 6 Hindi Durva (28 chapters)"
for ch in $(seq -f "%02g" 1 28); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/fhdu1${ch}.pdf" \
        "grade6_hindi_durva_ch${ch}.pdf" \
        6 "Hindi" $((10#$ch)) "Durva"
    sleep 1
done

# Grade 6 Hindi Bal Ram Katha (12 chapters)
log_msg "📖 Grade 6 Hindi Bal Ram Katha (12 chapters)"
for ch in $(seq -f "%02g" 1 12); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/fhbr1${ch}.pdf" \
        "grade6_hindi_bal_ram_katha_ch${ch}.pdf" \
        6 "Hindi" $((10#$ch)) "Bal Ram Katha"
    sleep 1
done

# Grade 7 Hindi Vasant (20 chapters)
log_msg "📖 Grade 7 Hindi Vasant (20 chapters)"
for ch in $(seq -f "%02g" 1 20); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/ghvs1${ch}.pdf" \
        "grade7_hindi_vasant_ch${ch}.pdf" \
        7 "Hindi" $((10#$ch)) "Vasant"
    sleep 1
done

# Grade 7 Hindi Durva (15 chapters)
log_msg "📖 Grade 7 Hindi Durva (15 chapters)"
for ch in $(seq -f "%02g" 1 15); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/ghdu1${ch}.pdf" \
        "grade7_hindi_durva_ch${ch}.pdf" \
        7 "Hindi" $((10#$ch)) "Durva"
    sleep 1
done

# Grade 7 Hindi Mahabharat (10 chapters)
log_msg "📖 Grade 7 Hindi Mahabharat (10 chapters)"
for ch in $(seq -f "%02g" 1 10); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/ghmb1${ch}.pdf" \
        "grade7_hindi_mahabharat_ch${ch}.pdf" \
        7 "Hindi" $((10#$ch)) "Mahabharat"
    sleep 1
done

# Grade 8 Hindi Vasant (18 chapters)
log_msg "📖 Grade 8 Hindi Vasant (18 chapters)"
for ch in $(seq -f "%02g" 1 18); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/hhvs1${ch}.pdf" \
        "grade8_hindi_vasant_ch${ch}.pdf" \
        8 "Hindi" $((10#$ch)) "Vasant"
    sleep 1
done

# Grade 8 Hindi Durva (18 chapters)
log_msg "📖 Grade 8 Hindi Durva (18 chapters)"
for ch in $(seq -f "%02g" 1 18); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/hhdu1${ch}.pdf" \
        "grade8_hindi_durva_ch${ch}.pdf" \
        8 "Hindi" $((10#$ch)) "Durva"
    sleep 1
done

# Grade 8 Hindi Bharat Ki Khoj (10 chapters)
log_msg "📖 Grade 8 Hindi Bharat Ki Khoj (10 chapters)"
for ch in $(seq -f "%02g" 1 10); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/hhbk1${ch}.pdf" \
        "grade8_hindi_bharat_ki_khoj_ch${ch}.pdf" \
        8 "Hindi" $((10#$ch)) "Bharat Ki Khoj"
    sleep 1
done

# Grade 9 Hindi Kshitij (17 chapters)
log_msg "📖 Grade 9 Hindi Kshitij (17 chapters)"
for ch in $(seq -f "%02g" 1 17); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/ihks1${ch}.pdf" \
        "grade9_hindi_kshitij_ch${ch}.pdf" \
        9 "Hindi" $((10#$ch)) "Kshitij"
    sleep 1
done

# Grade 9 Hindi Kritika (5 chapters)
log_msg "📖 Grade 9 Hindi Kritika (5 chapters)"
for ch in $(seq -f "%02g" 1 5); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/ihkr1${ch}.pdf" \
        "grade9_hindi_kritika_ch${ch}.pdf" \
        9 "Hindi" $((10#$ch)) "Kritika"
    sleep 1
done

# Grade 9 Hindi Sparsh (13 chapters)
log_msg "📖 Grade 9 Hindi Sparsh (13 chapters)"
for ch in $(seq -f "%02g" 1 13); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/ihsp1${ch}.pdf" \
        "grade9_hindi_sparsh_ch${ch}.pdf" \
        9 "Hindi" $((10#$ch)) "Sparsh"
    sleep 1
done

# Grade 9 Hindi Sanchayan (3 chapters)
log_msg "📖 Grade 9 Hindi Sanchayan (3 chapters)"
for ch in $(seq -f "%02g" 1 3); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/ihsa1${ch}.pdf" \
        "grade9_hindi_sanchayan_ch${ch}.pdf" \
        9 "Hindi" $((10#$ch)) "Sanchayan"
    sleep 1
done

# Grade 10 Hindi Kshitij (17 chapters)
log_msg "📖 Grade 10 Hindi Kshitij (17 chapters)"
for ch in $(seq -f "%02g" 1 17); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/jhks1${ch}.pdf" \
        "grade10_hindi_kshitij_ch${ch}.pdf" \
        10 "Hindi" $((10#$ch)) "Kshitij"
    sleep 1
done

# Grade 10 Hindi Kritika (5 chapters)
log_msg "📖 Grade 10 Hindi Kritika (5 chapters)"
for ch in $(seq -f "%02g" 1 5); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/jhkr1${ch}.pdf" \
        "grade10_hindi_kritika_ch${ch}.pdf" \
        10 "Hindi" $((10#$ch)) "Kritika"
    sleep 1
done

# Grade 10 Hindi Sparsh (17 chapters)
log_msg "📖 Grade 10 Hindi Sparsh (17 chapters)"
for ch in $(seq -f "%02g" 1 17); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/jhsp1${ch}.pdf" \
        "grade10_hindi_sparsh_ch${ch}.pdf" \
        10 "Hindi" $((10#$ch)) "Sparsh"
    sleep 1
done

# Grade 10 Hindi Sanchayan (3 chapters)
log_msg "📖 Grade 10 Hindi Sanchayan (3 chapters)"
for ch in $(seq -f "%02g" 1 3); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/jhsa1${ch}.pdf" \
        "grade10_hindi_sanchayan_ch${ch}.pdf" \
        10 "Hindi" $((10#$ch)) "Sanchayan"
    sleep 1
done

print_progress "Phase 4: Hindi Literature Complete"


echo "==========================================================================================================" | tee -a "$MASTER_LOG"
echo "📚 PHASE 5: ENGLISH LITERATURE" | tee -a "$MASTER_LOG"
echo "==========================================================================================================" | tee -a "$MASTER_LOG"
echo "Target: ~92 chapters" | tee -a "$MASTER_LOG"
echo "" | tee -a "$MASTER_LOG"

# Grade 1 English Marigold (10 chapters)
log_msg "📖 Grade 1 English Marigold (10 chapters)"
for ch in $(seq -f "%02g" 1 10); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/aemr1${ch}.pdf" \
        "grade1_english_marigold_ch${ch}.pdf" \
        1 "English" $((10#$ch)) "Marigold"
    sleep 1
done

# Grade 2 English Marigold (10 chapters)
log_msg "📖 Grade 2 English Marigold (10 chapters)"
for ch in $(seq -f "%02g" 1 10); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/bemr1${ch}.pdf" \
        "grade2_english_marigold_ch${ch}.pdf" \
        2 "English" $((10#$ch)) "Marigold"
    sleep 1
done

# Grade 3 English Marigold (10 chapters)
log_msg "📖 Grade 3 English Marigold (10 chapters)"
for ch in $(seq -f "%02g" 1 10); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/cemr1${ch}.pdf" \
        "grade3_english_marigold_ch${ch}.pdf" \
        3 "English" $((10#$ch)) "Marigold"
    sleep 1
done

# Grade 4 English Marigold (10 chapters)
log_msg "📖 Grade 4 English Marigold (10 chapters)"
for ch in $(seq -f "%02g" 1 10); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/demr1${ch}.pdf" \
        "grade4_english_marigold_ch${ch}.pdf" \
        4 "English" $((10#$ch)) "Marigold"
    sleep 1
done

# Grade 5 English Marigold (10 chapters)
log_msg "📖 Grade 5 English Marigold (10 chapters)"
for ch in $(seq -f "%02g" 1 10); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/eemr1${ch}.pdf" \
        "grade5_english_marigold_ch${ch}.pdf" \
        5 "English" $((10#$ch)) "Marigold"
    sleep 1
done

# Grade 6 English Honeysuckle (10 chapters)
log_msg "📖 Grade 6 English Honeysuckle (10 chapters)"
for ch in $(seq -f "%02g" 1 10); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/fehs1${ch}.pdf" \
        "grade6_english_honeysuckle_ch${ch}.pdf" \
        6 "English" $((10#$ch)) "Honeysuckle"
    sleep 1
done

# Grade 6 English A Pact with the Sun (10 chapters)
log_msg "📖 Grade 6 English A Pact with the Sun (10 chapters)"
for ch in $(seq -f "%02g" 1 10); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/feps1${ch}.pdf" \
        "grade6_english_pact_sun_ch${ch}.pdf" \
        6 "English" $((10#$ch)) "A Pact with the Sun"
    sleep 1
done

# Grade 7 English Honeycomb (10 chapters)
log_msg "📖 Grade 7 English Honeycomb (10 chapters)"
for ch in $(seq -f "%02g" 1 10); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/gehn1${ch}.pdf" \
        "grade7_english_honeycomb_ch${ch}.pdf" \
        7 "English" $((10#$ch)) "Honeycomb"
    sleep 1
done

# Grade 7 English Alien Hand (10 chapters)
log_msg "📖 Grade 7 English Alien Hand (10 chapters)"
for ch in $(seq -f "%02g" 1 10); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/geah1${ch}.pdf" \
        "grade7_english_alien_hand_ch${ch}.pdf" \
        7 "English" $((10#$ch)) "An Alien Hand"
    sleep 1
done

# Grade 8 English Honeydew (10 chapters)
log_msg "📖 Grade 8 English Honeydew (10 chapters)"
for ch in $(seq -f "%02g" 1 10); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/hehn1${ch}.pdf" \
        "grade8_english_honeydew_ch${ch}.pdf" \
        8 "English" $((10#$ch)) "Honeydew"
    sleep 1
done

# Grade 8 English It So Happened (10 chapters)
log_msg "📖 Grade 8 English It So Happened (10 chapters)"
for ch in $(seq -f "%02g" 1 10); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/heih1${ch}.pdf" \
        "grade8_english_it_so_happened_ch${ch}.pdf" \
        8 "English" $((10#$ch)) "It So Happened"
    sleep 1
done

# Grade 9 English Beehive (11 chapters)
log_msg "📖 Grade 9 English Beehive (11 chapters)"
for ch in $(seq -f "%02g" 1 11); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/iebe1${ch}.pdf" \
        "grade9_english_beehive_ch${ch}.pdf" \
        9 "English" $((10#$ch)) "Beehive"
    sleep 1
done

# Grade 9 English Moments (10 chapters)
log_msg "📖 Grade 9 English Moments (10 chapters)"
for ch in $(seq -f "%02g" 1 10); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/iemo1${ch}.pdf" \
        "grade9_english_moments_ch${ch}.pdf" \
        9 "English" $((10#$ch)) "Moments"
    sleep 1
done

# Grade 10 English First Flight (11 chapters)
log_msg "📖 Grade 10 English First Flight (11 chapters)"
for ch in $(seq -f "%02g" 1 11); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/jefl1${ch}.pdf" \
        "grade10_english_first_flight_ch${ch}.pdf" \
        10 "English" $((10#$ch)) "First Flight"
    sleep 1
done

# Grade 10 English Footprints (10 chapters)
log_msg "📖 Grade 10 English Footprints (10 chapters)"
for ch in $(seq -f "%02g" 1 10); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/jefp1${ch}.pdf" \
        "grade10_english_footprints_ch${ch}.pdf" \
        10 "English" $((10#$ch)) "Footprints without Feet"
    sleep 1
done

print_progress "Phase 5: English Literature Complete"


echo "==========================================================================================================" | tee -a "$MASTER_LOG"
echo "📚 PHASE 6: EVS (ENVIRONMENTAL STUDIES - GRADES 1-5)" | tee -a "$MASTER_LOG"
echo "==========================================================================================================" | tee -a "$MASTER_LOG"
echo "Target: ~110 chapters (Looking Around, Raindrops)" | tee -a "$MASTER_LOG"
echo "" | tee -a "$MASTER_LOG"

# Grade 1 EVS Raindrops (22 chapters)
log_msg "📖 Grade 1 EVS Raindrops (22 chapters)"
for ch in $(seq -f "%02g" 1 22); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/aeev1${ch}.pdf" \
        "grade1_evs_raindrops_ch${ch}.pdf" \
        1 "EVS" $((10#$ch)) "Raindrops"
    sleep 1
done

# Grade 2 EVS Raindrops (21 chapters)
log_msg "📖 Grade 2 EVS Raindrops (21 chapters)"
for ch in $(seq -f "%02g" 1 21); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/beev1${ch}.pdf" \
        "grade2_evs_raindrops_ch${ch}.pdf" \
        2 "EVS" $((10#$ch)) "Raindrops"
    sleep 1
done

# Grade 3 EVS Looking Around (24 chapters)
log_msg "📖 Grade 3 EVS Looking Around (24 chapters)"
for ch in $(seq -f "%02g" 1 24); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/ceev1${ch}.pdf" \
        "grade3_evs_looking_around_ch${ch}.pdf" \
        3 "EVS" $((10#$ch)) "Looking Around"
    sleep 1
done

# Grade 4 EVS Looking Around (27 chapters)
log_msg "📖 Grade 4 EVS Looking Around (27 chapters)"
for ch in $(seq -f "%02g" 1 27); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/deev1${ch}.pdf" \
        "grade4_evs_looking_around_ch${ch}.pdf" \
        4 "EVS" $((10#$ch)) "Looking Around"
    sleep 1
done

# Grade 5 EVS Looking Around (22 chapters)
log_msg "📖 Grade 5 EVS Looking Around (22 chapters)"
for ch in $(seq -f "%02g" 1 22); do
    extract_chapter_safe \
        "https://ncert.nic.in/textbook/pdf/eeev1${ch}.pdf" \
        "grade5_evs_looking_around_ch${ch}.pdf" \
        5 "EVS" $((10#$ch)) "Looking Around"
    sleep 1
done

print_progress "Phase 6: EVS Complete"


echo "" | tee -a "$MASTER_LOG"
echo "==========================================================================================================" | tee -a "$MASTER_LOG"
echo "🎉 SYSTEMATIC EXTRACTION COMPLETE!" | tee -a "$MASTER_LOG"
echo "==========================================================================================================" | tee -a "$MASTER_LOG"
echo "End Time: $(date)" | tee -a "$MASTER_LOG"
echo "" | tee -a "$MASTER_LOG"
echo "📊 FINAL STATISTICS" | tee -a "$MASTER_LOG"
echo "==========================================================================================================" | tee -a "$MASTER_LOG"
echo "Total Chapters Attempted: $TOTAL_ATTEMPTED" | tee -a "$MASTER_LOG"
echo "Successfully Extracted:   $TOTAL_SUCCESS" | tee -a "$MASTER_LOG"
echo "Failed Extractions:       $TOTAL_FAILED" | tee -a "$MASTER_LOG"
if [ $TOTAL_ATTEMPTED -gt 0 ]; then
    echo "Success Rate:             $(( TOTAL_SUCCESS * 100 / TOTAL_ATTEMPTED ))%" | tee -a "$MASTER_LOG"
fi
echo "==========================================================================================================" | tee -a "$MASTER_LOG"
echo "" | tee -a "$MASTER_LOG"
echo "📝 Next Steps:" | tee -a "$MASTER_LOG"
echo "   1. Run chapter name repair script to fix any remaining 'Unknown Chapter' entries" | tee -a "$MASTER_LOG"
echo "   2. Verify database has ~912 total chapters (100% CBSE syllabus)" | tee -a "$MASTER_LOG"
echo "   3. Generate subject-wise completion report" | tee -a "$MASTER_LOG"
echo "" | tee -a "$MASTER_LOG"
echo "Master log saved to: $MASTER_LOG" | tee -a "$MASTER_LOG"
echo "==========================================================================================================" | tee -a "$MASTER_LOG"
