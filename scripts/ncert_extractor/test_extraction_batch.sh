#!/bin/bash
#
# TEST EXTRACTION - Small batch to verify the pipeline works
# Extracts a few high-priority subjects to test:
# 1. Grade 6 Mathematics (missing chapters)
# 2. Grade 6 Science (missing chapters)
# 3. Grade 1 Hindi Rimjhim (sample)
#

set -e  # Exit on error

echo "========================================"
echo "🧪 TEST EXTRACTION - VERIFICATION BATCH"
echo "========================================"
echo ""

# Create PDFs directory
PDFS_DIR="../../../ncert_pdfs"
mkdir -p "$PDFS_DIR"

# Test 1: Grade 6 Mathematics - Ganita Prakash (Chapter 3)
echo "📥 Test 1: Downloading Grade 6 Math Chapter 3..."
curl -k -s -o "$PDFS_DIR/grade6_math_ch03.pdf" "https://ncert.nic.in/textbook/pdf/fegp103.pdf" || wget --no-check-certificate -q -O "$PDFS_DIR/grade6_math_ch03.pdf" "https://ncert.nic.in/textbook/pdf/fegp103.pdf"

if [ -f "$PDFS_DIR/grade6_math_ch03.pdf" ]; then
    echo "✅ Downloaded Grade 6 Math Ch.3"

    echo "📖 Extracting content..."
    python3 extract_chapter.py "$PDFS_DIR/grade6_math_ch03.pdf" 6 "Mathematics" 3

    if [ $? -eq 0 ]; then
        echo "✅ Extraction successful!"
    else
        echo "❌ Extraction failed"
        exit 1
    fi
else
    echo "❌ Download failed for Grade 6 Math Ch.3"
    exit 1
fi

echo ""
echo "----------------------------------------"
echo ""

# Test 2: Grade 6 Science - Curiosity (Chapter 5)
echo "📥 Test 2: Downloading Grade 6 Science Chapter 5..."
curl -k -s -o "$PDFS_DIR/grade6_science_ch05.pdf" "https://ncert.nic.in/textbook/pdf/fecu105.pdf" || wget --no-check-certificate -q -O "$PDFS_DIR/grade6_science_ch05.pdf" "https://ncert.nic.in/textbook/pdf/fecu105.pdf"

if [ -f "$PDFS_DIR/grade6_science_ch05.pdf" ]; then
    echo "✅ Downloaded Grade 6 Science Ch.5"

    echo "📖 Extracting content..."
    python3 extract_chapter.py "$PDFS_DIR/grade6_science_ch05.pdf" 6 "Science" 5

    if [ $? -eq 0 ]; then
        echo "✅ Extraction successful!"
    else
        echo "❌ Extraction failed"
        exit 1
    fi
else
    echo "❌ Download failed for Grade 6 Science Ch.5"
    exit 1
fi

echo ""
echo "----------------------------------------"
echo ""

# Test 3: Grade 10 Social Science (Chapter 8 - Drainage)
echo "📥 Test 3: Downloading Grade 10 Social Science Chapter 8..."
curl -k -s -o "$PDFS_DIR/grade10_ss_ch08.pdf" "https://ncert.nic.in/textbook/pdf/jess108.pdf" || wget --no-check-certificate -q -O "$PDFS_DIR/grade10_ss_ch08.pdf" "https://ncert.nic.in/textbook/pdf/jess108.pdf"

if [ -f "$PDFS_DIR/grade10_ss_ch08.pdf" ]; then
    echo "✅ Downloaded Grade 10 Social Science Ch.8"

    echo "📖 Extracting content..."
    python3 extract_chapter.py "$PDFS_DIR/grade10_ss_ch08.pdf" 10 "Social_Science" 8

    if [ $? -eq 0 ]; then
        echo "✅ Extraction successful!"
    else
        echo "❌ Extraction failed"
        exit 1
    fi
else
    echo "❌ Download failed for Grade 10 Social Science Ch.8"
    exit 1
fi

echo ""
echo "========================================"
echo "✅ TEST EXTRACTION COMPLETE!"
echo "========================================"
echo ""
echo "📊 Summary:"
echo "  - Grade 6 Mathematics Ch.3: ✅"
echo "  - Grade 6 Science Ch.5: ✅"
echo "  - Grade 10 Social Science Ch.8: ✅"
echo ""
echo "🎯 Next Steps:"
echo "  1. Verify the data in database"
echo "  2. Check chapter names are correct"
echo "  3. If successful, run full extraction"
echo ""
