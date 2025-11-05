#!/bin/bash
# Download newly discovered Hindi literature and English primary books

cd /home/learnify/lt/learnify-teach/backend/ncert_pdfs

echo "========================================================================"
echo "DOWNLOADING NEWLY DISCOVERED BOOKS"
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
    echo "  Total: $c chapters"
}

# HINDI LITERATURE - New discoveries
echo "=== GRADE 10 - HINDI SPARSH (Additional) ==="
dl "jhsp1" "grade_10_Hindi_Sparsh_Additional" 1 20
echo ""

echo "=== GRADE 9 - HINDI KSHITIJ ==="
dl "ihks1" "grade_9_Hindi_Kshitij" 1 20
echo ""

echo "=== GRADE 9 - HINDI SPARSH (Complete) ==="
dl "ihsp1" "grade_9_Hindi_Sparsh_Complete" 1 20
echo ""

echo "=== GRADE 8 - HINDI VASANT (Complete) ==="
dl "hhvs1" "grade_8_Hindi_Vasant_Complete" 1 20
echo ""

echo "=== GRADE 7 - HINDI VASANT ==="
dl "ghvs1" "grade_7_Hindi_Vasant" 1 20
echo ""

# ENGLISH PRIMARY - New discoveries
echo "=== GRADE 2 - ENGLISH MARIGOLD ==="
dl "bemr1" "grade_2_English_Marigold" 1 15
echo ""

echo "=== GRADE 1 - ENGLISH MARIGOLD ==="
dl "aemr1" "grade_1_English_Marigold" 1 15
echo ""

echo ""
echo "========================================================================"
echo "DOWNLOAD SUMMARY:"
ls -1 grade_*_Hindi_*.pdf 2>/dev/null | wc -l | xargs echo "Hindi chapters:"
ls -1 grade_*_English_*.pdf 2>/dev/null | wc -l | xargs echo "English chapters:"
ls -1 grade_1_*.pdf 2>/dev/null | wc -l | xargs echo "Grade 1 total:"
ls -1 grade_2_*.pdf 2>/dev/null | wc -l | xargs echo "Grade 2 total:"
echo "========================================================================"
