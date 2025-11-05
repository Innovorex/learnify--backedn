#!/bin/bash
# Download Grade 7 Science chapters (1-18)

cd /home/learnify/lt/learnify-teach/backend/ncert_pdfs

echo "Downloading Grade 7 Science chapters..."
echo ""

for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18; do
  chapter=$(printf "%02d" $i)
  filename="grade_7_science_ch${chapter}.pdf"
  url="https://ncert.nic.in/textbook/pdf/gesc1${chapter}.pdf"

  echo "[$i/18] Downloading Chapter $i..."
  wget --no-check-certificate -q -O "$filename" "$url"

  if [ -s "$filename" ]; then
    size=$(du -h "$filename" | cut -f1)
    echo "  ✅ Downloaded: $size"
  else
    echo "  ❌ Failed or empty"
    rm -f "$filename"
  fi
  sleep 1
done

echo ""
echo "==========================================="
downloaded=$(ls -1 grade_7_science_ch*.pdf 2>/dev/null | wc -l)
echo "Downloaded: $downloaded/18 chapters"
echo "==========================================="
