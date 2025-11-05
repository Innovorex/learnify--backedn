#!/bin/bash
# Download ALL Grade 10 subjects

cd /home/learnify/lt/learnify-teach/backend/ncert_pdfs

echo "========================================="
echo "Downloading ALL Grade 10 NCERT Content"
echo "========================================="
echo ""

# Social Science (22 chapters total)
echo "📚 Downloading Social Science (22 chapters)..."
for i in {1..22}; do
  chapter=$(printf "%02d" $i)
  wget --no-check-certificate -q -O "grade_10_social_ch${chapter}.pdf" "https://ncert.nic.in/textbook/pdf/jess1${chapter}.pdf"
  [ -s "grade_10_social_ch${chapter}.pdf" ] && echo "  ✅ Chapter $i" || rm -f "grade_10_social_ch${chapter}.pdf"
  sleep 1
done
echo ""

# Hindi Sparsh (14 chapters)
echo "📚 Downloading Hindi Sparsh (14 chapters)..."
for i in {1..17}; do
  chapter=$(printf "%02d" $i)
  wget --no-check-certificate -q -O "grade_10_hindi_sparsh_ch${chapter}.pdf" "https://ncert.nic.in/textbook/pdf/jhsp1${chapter}.pdf"
  [ -s "grade_10_hindi_sparsh_ch${chapter}.pdf" ] && echo "  ✅ Chapter $i" || rm -f "grade_10_hindi_sparsh_ch${chapter}.pdf"
  sleep 1
done
echo ""

echo "========================================="
echo "Grade 10 - Download Complete!"
ls -1 grade_10_social_ch*.pdf 2>/dev/null | wc -l | xargs echo "Social Science:"
ls -1 grade_10_hindi_*.pdf 2>/dev/null | wc -l | xargs echo "Hindi:"
echo "========================================="
