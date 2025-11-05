#!/bin/bash
# Comprehensive pattern discovery for Hindi literature and English primary books

echo "========================================================================"
echo "DISCOVERING HINDI LITERATURE & ENGLISH PRIMARY PATTERNS"
echo "========================================================================"
echo ""

test_url() {
    pattern=$1
    name=$2
    ch=$3

    url="https://ncert.nic.in/textbook/pdf/${pattern}${ch}.pdf"
    if curl -s -I "$url" 2>/dev/null | grep -q "200 OK"; then
        echo "✅ FOUND: $name ($pattern)"
        return 0
    fi
    return 1
}

# HINDI LITERATURE - Grade 10
echo "=== GRADE 10 - HINDI LITERATURE ==="
for prefix in "jhks" "jhkj" "jhkt" "jhsn" "jhsp"; do
    test_url "${prefix}1" "Hindi ${prefix}" "01"
done
echo ""

# HINDI LITERATURE - Grade 9
echo "=== GRADE 9 - HINDI LITERATURE ==="
for prefix in "ihks" "ihkj" "ihkt" "ihsn" "ihsp"; do
    test_url "${prefix}1" "Hindi ${prefix}" "01"
done
echo ""

# HINDI LITERATURE - Grade 8
echo "=== GRADE 8 - HINDI LITERATURE ==="
for prefix in "hhvs" "hhbh" "hhds" "hhsn"; do
    test_url "${prefix}1" "Hindi ${prefix}" "01"
done
echo ""

# HINDI LITERATURE - Grade 7
echo "=== GRADE 7 - HINDI LITERATURE ==="
for prefix in "ghvs" "ghdh" "ghds" "ghbm"; do
    test_url "${prefix}1" "Hindi ${prefix}" "01"
done
echo ""

# HINDI LITERATURE - Grade 6
echo "=== GRADE 6 - HINDI LITERATURE ==="
for prefix in "fhvs" "fhds" "fhbm"; do
    test_url "${prefix}1" "Hindi ${prefix}" "01"
done
echo ""

# HINDI PRIMARY - Grades 5-1 (Rimjhim series)
echo "=== HINDI PRIMARY - RIMJHIM SERIES ==="
for grade in "e" "d" "c" "b" "a"; do
    for prefix in "hrj" "hrm" "hri"; do
        pattern="${grade}${prefix}1"
        test_url "$pattern" "Hindi Primary ${pattern}" "01"
    done
done
echo ""

# ENGLISH PRIMARY - Marigold series
echo "=== ENGLISH PRIMARY - MARIGOLD SERIES ==="
for grade in "e" "d" "c" "b" "a"; do
    for prefix in "emg" "eel" "erm" "emr"; do
        pattern="${grade}${prefix}1"
        test_url "$pattern" "English Primary ${pattern}" "01"
    done
done
echo ""

# ENGLISH PRIMARY - Raindrops series
echo "=== ENGLISH PRIMARY - RAINDROPS ==="
for grade in "e" "d" "c" "b" "a"; do
    for prefix in "erd" "erp" "erb"; do
        pattern="${grade}${prefix}1"
        test_url "$pattern" "English Raindrops ${pattern}" "01"
    done
done
echo ""

# Additional Social Science patterns
echo "=== SOCIAL SCIENCE - SEPARATE BOOKS ==="
for grade in "h" "g" "f"; do
    for subj in "ehs" "egy" "epc" "eec"; do
        pattern="${grade}${subj}1"
        test_url "$pattern" "Social ${pattern}" "01"
    done
done
echo ""

echo "========================================================================"
echo "Pattern Discovery Complete!"
echo "========================================================================"
