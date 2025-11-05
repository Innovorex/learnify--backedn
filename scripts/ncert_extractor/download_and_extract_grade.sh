#!/bin/bash
# Download and extract a complete grade-subject combination
# Usage: ./download_and_extract_grade.sh <grade> <subject> <url_prefix> <num_chapters>

GRADE=$1
SUBJECT=$2
URL_PREFIX=$3
NUM_CHAPTERS=$4

cd /home/learnify/lt/learnify-teach/backend/ncert_pdfs

echo "=========================================="
echo "Grade $GRADE $SUBJECT"
echo "=========================================="

# Download
for i in $(seq 1 $NUM_CHAPTERS); do
  chapter=$(printf "%02d" $i)
  filename="grade_${GRADE}_${SUBJECT}_ch${chapter}.pdf"
  url="${URL_PREFIX}${chapter}.pdf"

  wget --no-check-certificate -q -O "$filename" "$url"

  if [ -s "$filename" ]; then
    size=$(du -h "$filename" | cut -f1)
    echo "Chapter $i: $size"
  else
    rm -f "$filename"
  fi
  sleep 1
done

echo ""
echo "Download complete. Starting extraction..."
echo ""

# Extract
cd /home/learnify/lt/learnify-teach/backend/scripts/ncert_extractor
python3 batch_extract.py $GRADE $SUBJECT 1 $NUM_CHAPTERS "/home/learnify/lt/learnify-teach/backend/ncert_pdfs/grade_${GRADE}_${SUBJECT}_ch{chapter}.pdf"
