#!/bin/bash
# Download EVERYTHING remaining - massive extraction

cd /home/learnify/lt/learnify-teach/backend/ncert_pdfs

echo "========================================================================"
echo "DOWNLOADING ALL REMAINING NCERT CONTENT - COMPREHENSIVE"
echo "========================================================================"
echo ""

download_range() {
    pattern=$1
    name=$2
    start=$3
    end=$4

    echo "📚 $name ($pattern)..."
    count=0
    for i in $(seq $start $end); do
        ch=$(printf "%02d" $i)
        wget -q -O "temp_${pattern}_${ch}.pdf" "https://ncert.nic.in/textbook/pdf/${pattern}${ch}.pdf" 2>/dev/null
        if [ -s "temp_${pattern}_${ch}.pdf" ]; then
            mv "temp_${pattern}_${ch}.pdf" "${name// /_}_ch${ch}.pdf"
            count=$((count+1))
            echo "  ✅ Ch $i"
        else
            rm -f "temp_${pattern}_${ch}.pdf" 2>/dev/null
        fi
        sleep 0.2
    done
    echo "  Total: $count chapters"
}

# GRADE 10 - English
echo "=== GRADE 10 - ENGLISH ==="
download_range "jeff1" "grade_10_English_FirstFlight" 1 11
download_range "jefp1" "grade_10_English_Footprints" 1 10
echo ""

# GRADE 10 - Complete Social Science
echo "=== GRADE 10 - SOCIAL SCIENCE (Complete) ==="
download_range "jess1" "grade_10_Social_Complete" 1 22
echo ""

# GRADE 9 - Social Science Complete
echo "=== GRADE 9 - SOCIAL SCIENCE (Complete) ==="
download_range "iess1" "grade_9_Social_Complete" 1 22
echo ""

# GRADE 8 - English
echo "=== GRADE 8 - ENGLISH ==="
download_range "hehd1" "grade_8_English_Honeydew" 1 10
echo ""

# GRADE 7 - English
echo "=== GRADE 7 - ENGLISH ==="
download_range "gehc1" "grade_7_English_Honeycomb" 1 10
download_range "geah1" "grade_7_English_AlienHand" 1 10
echo ""

# GRADE 7 - Complete Social Science
echo "=== GRADE 7 - SOCIAL SCIENCE (Complete) ==="
download_range "gess1" "grade_7_Social_Complete" 9 22
echo ""

# GRADE 1 - Joyful Mathematics
echo "=== GRADE 1 - MATHEMATICS ==="
download_range "aejm1" "grade_1_Math_Joyful" 1 13
echo ""

# GRADE 5 - Complete remaining Math
echo "=== GRADE 5 - COMPLETE MATH ==="
download_range "gegp1" "grade_5_Math_Complete" 9 15
echo ""

# GRADE 5 - Complete remaining EVS
echo "=== GRADE 5 - COMPLETE EVS ==="
download_range "eeev1" "grade_5_EVS_Complete" 11 22
echo ""

# GRADE 3 - Complete remaining EVS
echo "=== GRADE 3 - COMPLETE EVS ==="
download_range "ceev1" "grade_3_EVS_Complete" 13 24
echo ""

echo ""
echo "========================================================================"
echo "DOWNLOAD COMPLETE!"
echo "========================================================================"
echo ""
echo "Summary of new downloads:"
ls -1 grade_*_English_*.pdf 2>/dev/null | wc -l | xargs echo "English:"
ls -1 grade_*_Social_Complete*.pdf 2>/dev/null | wc -l | xargs echo "Social Science:"
ls -1 grade_1_*.pdf 2>/dev/null | wc -l | xargs echo "Grade 1:"
ls -1 grade_*_Complete*.pdf 2>/dev/null | wc -l | xargs echo "Complete/Additional:"
echo ""
