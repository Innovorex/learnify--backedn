#!/bin/bash
# Download ALL remaining subjects for Grades 6-10

cd /home/learnify/lt/learnify-teach/backend/ncert_pdfs

echo "============================================================"
echo "Downloading ALL Remaining NCERT Subjects (Grades 6-10)"
echo "============================================================"
echo ""

# GRADE 9
echo "=== GRADE 9 ==="

echo "📚 Social Science (22 chapters)..."
for i in {1..22}; do
  chapter=$(printf "%02d" $i)
  wget -q -O "grade_9_social_ch${chapter}.pdf" "https://ncert.nic.in/textbook/pdf/iess1${chapter}.pdf" 2>/dev/null
  [ -s "grade_9_social_ch${chapter}.pdf" ] && echo "  ✅ Ch $i" || rm -f "grade_9_social_ch${chapter}.pdf"
  sleep 0.5
done

echo "📚 Hindi Sparsh (14 chapters)..."
for i in {1..17}; do
  chapter=$(printf "%02d" $i)
  wget -q -O "grade_9_hindi_ch${chapter}.pdf" "https://ncert.nic.in/textbook/pdf/ihsp1${chapter}.pdf" 2>/dev/null
  [ -s "grade_9_hindi_ch${chapter}.pdf" ] && echo "  ✅ Ch $i" || rm -f "grade_9_hindi_ch${chapter}.pdf"
  sleep 0.5
done
echo ""

# GRADE 8
echo "=== GRADE 8 ==="

echo "📚 Hindi Vasant (~18 chapters)..."
for i in {1..20}; do
  chapter=$(printf "%02d" $i)
  wget -q -O "grade_8_hindi_ch${chapter}.pdf" "https://ncert.nic.in/textbook/pdf/hhvs1${chapter}.pdf" 2>/dev/null
  [ -s "grade_8_hindi_ch${chapter}.pdf" ] && echo "  ✅ Ch $i" || rm -f "grade_8_hindi_ch${chapter}.pdf"
  sleep 0.5
done
echo ""

echo "============================================================"
echo "Download Summary:"
echo "Grade 9 Social Science:" $(ls -1 grade_9_social_ch*.pdf 2>/dev/null | wc -l)
echo "Grade 9 Hindi:" $(ls -1 grade_9_hindi_ch*.pdf 2>/dev/null | wc -l)
echo "Grade 8 Hindi:" $(ls -1 grade_8_hindi_ch*.pdf 2>/dev/null | wc -l)
echo "============================================================"
