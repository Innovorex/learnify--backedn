#!/bin/bash
# Extract remaining Grade 10 Math chapters (3-14)

cd /home/learnify/lt/learnify-teach/backend/scripts/ncert_extractor

for i in 3 4 5 6 7 8 9 10 11 12 13 14; do
  chapter=$(printf "%02d" $i)
  pdf_file="/home/learnify/lt/learnify-teach/backend/ncert_pdfs/grade_10_math_ch${chapter}.pdf"

  if [ -f "$pdf_file" ] && [ -s "$pdf_file" ]; then
    echo "=========================================="
    echo "Processing Chapter $i..."
    python3 extract_chapter.py "$pdf_file" 10 Mathematics $i
    echo ""
  fi
done

echo "=========================================="
echo "Grade 10 Mathematics - Complete!"
echo "=========================================="
