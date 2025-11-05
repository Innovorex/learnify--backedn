#!/bin/bash
# MASSIVE final download - all remaining discoverable content

cd /home/learnify/lt/learnify-teach/backend/ncert_pdfs

echo "========================================================================"
echo "MASSIVE FINAL DOWNLOAD - ALL REMAINING CONTENT"
echo "========================================================================"
echo ""

dl() {
    pattern=$1; name=$2; start=$3; end=$4
    echo "📚 $name..."
    c=0
    for i in $(seq $start $end); do
        ch=$(printf "%02d" $i)
        wget -q -O "temp.pdf" "https://ncert.nic.in/textbook/pdf/${pattern}${ch}.pdf" 2>/dev/null
        if [ -s "temp.pdf" ]; then
            mv "temp.pdf" "${name}_ch${ch}.pdf"
            c=$((c+1))
            echo "  ✅ Ch $i"
        else
            rm -f "temp.pdf" 2>/dev/null
        fi
        sleep 0.15
    done
    echo "  Total: $c"
}

echo "=== GRADE 9 - ENGLISH BEEHIVE ==="
dl "iebe1" "grade_9_English_Beehive" 1 15
echo ""

echo "=== GRADE 8 - HINDI BHARAT KI KHOJ ==="
dl "hhbk1" "grade_8_Hindi_BharatKiKhoj" 1 11
echo ""

echo "=== GRADE 2 - JOYFUL MATHEMATICS ==="
dl "bejm1" "grade_2_Math_Joyful" 1 12
echo ""

echo "=== GRADE 5 - COMPLETE EVS (Looking Around) ==="
dl "eeev1" "grade_5_EVS_LookingAround_Complete" 11 22
dl "eeap1" "grade_5_EVS_Aaspass" 1 22
echo ""

echo "=== GRADE 4 - COMPLETE EVS ==="
dl "deev1" "grade_4_EVS_Complete" 11 22
dl "deap1" "grade_4_EVS_Aaspass" 1 22
echo ""

echo "=== GRADE 3 - COMPLETE EVS ==="
dl "ceev1" "grade_3_EVS_Complete" 13 24
echo ""

echo "=== REMAINING SOCIAL SCIENCE ==="
# Grade 10 - remaining
dl "jess1" "grade_10_Social_Remaining" 8 22
# Grade 9 - remaining
dl "iess1" "grade_9_Social_Remaining" 7 22
# Grade 7 - remaining
dl "gess1" "grade_7_Social_Remaining" 9 22
echo ""

echo ""
echo "========================================================================"
echo "DOWNLOAD SUMMARY:"
ls -1 grade_*_English_*.pdf 2>/dev/null | wc -l | xargs echo "English chapters:"
ls -1 grade_*_Hindi_*.pdf 2>/dev/null | wc -l | xargs echo "Hindi chapters:"
ls -1 grade_*_Social_*.pdf 2>/dev/null | wc -l | xargs echo "Social Science:"
ls -1 grade_*_EVS_*.pdf 2>/dev/null | wc -l | xargs echo "EVS chapters:"
ls -1 grade_2_*.pdf 2>/dev/null | wc -l | xargs echo "Grade 2 total:"
echo "========================================================================"
