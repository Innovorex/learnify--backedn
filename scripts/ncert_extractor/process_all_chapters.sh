#!/bin/bash
# Process all Grade 10 Math chapters

cd /home/learnify/lt/learnify-teach/backend/scripts/ncert_extractor

for i in 2 3 4 5 6 7 8 9 10 11 12 13 14; do
  chapter=$(printf "%02d" $i)
  pdf_file="../ncert_pdfs/grade_10_math_ch${chapter}.pdf"

  if [ -f "$pdf_file" ] && [ -s "$pdf_file" ]; then
    echo "=========================================="
    echo "Processing Chapter $i..."
    echo "=========================================="
    python3 extract_chapter.py "$pdf_file" 10 Mathematics $i
  else
    echo "Skipping Chapter $i (file not found or empty)"
  fi
done

echo ""
echo "=========================================="
echo "All chapters processed!"
echo "=========================================="
