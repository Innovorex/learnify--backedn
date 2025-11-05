#!/bin/bash
# Download Grade 5 Mathematics chapters (Maths Mela - 15 chapters)

cd /home/learnify/lt/learnify-teach/backend/ncert_pdfs

echo "Downloading Grade 5 Mathematics (Maths Mela) chapters..."
echo ""

for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
  chapter=$(printf "%02d" $i)
  filename="grade_5_math_ch${chapter}.pdf"
  url="https://ncert.nic.in/textbook/pdf/gegp1${chapter}.pdf"

  echo "[$i/15] Downloading Chapter $i..."
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
downloaded=$(ls -1 grade_5_math_ch*.pdf 2>/dev/null | wc -l)
echo "Downloaded: $downloaded/15 chapters"
echo "==========================================="
