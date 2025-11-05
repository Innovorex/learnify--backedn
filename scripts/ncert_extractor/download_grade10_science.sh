#!/bin/bash
# Download Grade 10 Science chapters (1-16)

cd /home/learnify/lt/learnify-teach/backend/ncert_pdfs

for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16; do
  chapter=$(printf "%02d" $i)
  echo "Downloading Science Chapter $i..."
  wget --no-check-certificate -q -O "grade_10_science_ch${chapter}.pdf" "https://ncert.nic.in/textbook/pdf/jesc1${chapter}.pdf"

  if [ -s "grade_10_science_ch${chapter}.pdf" ]; then
    size=$(du -h "grade_10_science_ch${chapter}.pdf" | cut -f1)
    echo "  Downloaded: $size"
  else
    echo "  Failed or empty"
    rm -f "grade_10_science_ch${chapter}.pdf"
  fi
  sleep 1
done

echo ""
echo "Download complete!"
ls -lh grade_10_science_ch*.pdf | wc -l
echo "chapters downloaded"
