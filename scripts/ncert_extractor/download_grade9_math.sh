#!/bin/bash
# Download Grade 9 Mathematics chapters (1-15)

cd /home/learnify/lt/learnify-teach/backend/ncert_pdfs

echo "Downloading Grade 9 Mathematics..."

for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
  chapter=$(printf "%02d" $i)
  echo "Chapter $i..."
  wget --no-check-certificate -q -O "grade_9_math_ch${chapter}.pdf" "https://ncert.nic.in/textbook/pdf/iemh1${chapter}.pdf"

  if [ -s "grade_9_math_ch${chapter}.pdf" ]; then
    size=$(du -h "grade_9_math_ch${chapter}.pdf" | cut -f1)
    echo "  Downloaded: $size"
  else
    echo "  Failed"
    rm -f "grade_9_math_ch${chapter}.pdf"
  fi
  sleep 1
done

echo ""
echo "Grade 9 Math download complete!"
ls -lh grade_9_math_ch*.pdf 2>/dev/null | wc -l
echo "chapters downloaded"
