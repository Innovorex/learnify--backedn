#!/bin/bash
# Download ALL remaining subjects for ALL grades 1-10

cd /home/learnify/lt/learnify-teach/backend/ncert_pdfs

echo "================================================================"
echo "DOWNLOADING ALL REMAINING SUBJECTS - GRADES 1-10"
echo "================================================================"
echo ""

download_subject() {
    grade=$1
    pattern=$2
    subject_name=$3
    start=$4
    end=$5

    echo "📚 $subject_name..."
    count=0
    for i in $(seq $start $end); do
        ch=$(printf "%02d" $i)
        filename="grade_${grade}_${subject_name// /_}_ch${ch}.pdf"
        wget -q -O "$filename" "https://ncert.nic.in/textbook/pdf/${pattern}${ch}.pdf" 2>/dev/null
        if [ -s "$filename" ]; then
            count=$((count+1))
            echo "  ✅ Ch $i"
        else
            rm -f "$filename" 2>/dev/null
        fi
        sleep 0.3
    done
    echo "  Downloaded: $count chapters"
}

# GRADE 10 - Remaining subjects
echo "=== GRADE 10 ==="
download_subject 10 "jhkr1" "Hindi_Kritika" 1 10
download_subject 10 "jess1" "Social_Science_Full" 8 22  # Continue from ch 8
echo ""

# GRADE 9 - Remaining subjects
echo "=== GRADE 9 ==="
download_subject 9 "ihkr1" "Hindi_Kritika" 1 10
download_subject 9 "ihsp1" "Hindi_Sparsh_Full" 11 17  # Continue from ch 11
download_subject 9 "iess1" "Social_Science_Full" 7 22  # Continue from ch 7
echo ""

# GRADE 8 - Remaining subjects
echo "=== GRADE 8 ==="
download_subject 8 "hhvs1" "Hindi_Vasant_Full" 14 20  # Continue from ch 14
echo ""

# GRADE 7 - Remaining subjects
echo "=== GRADE 7 ==="
download_subject 7 "ghvs1" "Hindi_Vasant" 1 18
download_subject 7 "gess1" "Social_Science" 1 22
echo ""

# GRADE 6 - New subjects
echo "=== GRADE 6 ==="
# No additional patterns found yet
echo "  No additional patterns available"
echo ""

# GRADE 5 - No new patterns found
echo "=== GRADE 5 ==="
echo "  No additional patterns available"
echo ""

# GRADE 4 - Core subjects
echo "=== GRADE 4 ==="
download_subject 4 "demm1" "Math" 1 14
download_subject 4 "deev1" "EVS" 1 22
echo ""

# GRADE 3 - Core subjects
echo "=== GRADE 3 ==="
download_subject 3 "cemm1" "Math" 1 13
download_subject 3 "ceev1" "EVS" 1 24
echo ""

# GRADE 2 - Core subjects
echo "=== GRADE 2 ==="
download_subject 2 "bemm1" "Math" 1 11
download_subject 2 "beev1" "EVS" 1 15
echo ""

# GRADE 1 - Core subjects
echo "=== GRADE 1 ==="
download_subject 1 "aemm1" "Math" 1 13
download_subject 1 "aeev1" "EVS" 1 16
echo ""

echo "================================================================"
echo "DOWNLOAD COMPLETE!"
echo "================================================================"
echo ""
echo "Summary by Grade:"
for g in {1..10}; do
    count=$(ls -1 grade_${g}_*.pdf 2>/dev/null | wc -l)
    [ $count -gt 0 ] && echo "  Grade $g: $count chapters"
done
echo ""
