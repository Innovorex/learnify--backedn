#!/bin/bash
# Discover MORE patterns for primary grades and remaining subjects

echo "========================================================================"
echo "COMPREHENSIVE PATTERN DISCOVERY - PRIMARY GRADES & ADDITIONAL SUBJECTS"
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

# HINDI PRIMARY - More patterns for Grades 6-1
echo "=== HINDI PRIMARY - ALL PATTERNS ==="
for grade in "f" "e" "d" "c" "b" "a"; do
    for prefix in "hri" "hrm" "hrj" "hvs" "hdu"; do
        pattern="${grade}${prefix}1"
        test_url "$pattern" "Hindi Primary ${pattern}" "01"
    done
done
echo ""

# ENGLISH PRIMARY - More patterns for Grades 6-3
echo "=== ENGLISH PRIMARY - ALL PATTERNS ==="
for grade in "f" "e" "d" "c"; do
    for prefix in "emg" "emr" "eel" "erm" "erb"; do
        pattern="${grade}${prefix}1"
        test_url "$pattern" "English Primary ${pattern}" "01"
    done
done
echo ""

# GRADE 6 - ALL subjects
echo "=== GRADE 6 - ALL SUBJECTS ==="
# Hindi
for prefix in "fhvs" "fhrm" "fhrj"; do
    test_url "${prefix}1" "Grade 6 Hindi ${prefix}" "01"
done
# English
for prefix in "fehc" "fefl" "ferm"; do
    test_url "${prefix}1" "Grade 6 English ${prefix}" "01"
done
# Math
for prefix in "femt" "fegp"; do
    test_url "${prefix}1" "Grade 6 Math ${prefix}" "01"
done
# Science
for prefix in "fesc"; do
    test_url "${prefix}1" "Grade 6 Science ${prefix}" "01"
done
echo ""

# GRADE 5 - Additional subjects
echo "=== GRADE 5 - ADDITIONAL SUBJECTS ==="
# English
for prefix in "eemg" "eemr"; do
    test_url "${prefix}1" "Grade 5 English ${prefix}" "01"
done
# Hindi
for prefix in "ehrm" "ehrj"; do
    test_url "${prefix}1" "Grade 5 Hindi ${prefix}" "01"
done
echo ""

# GRADE 4 - Additional subjects
echo "=== GRADE 4 - ADDITIONAL SUBJECTS ==="
# English
for prefix in "demg" "demr"; do
    test_url "${prefix}1" "Grade 4 English ${prefix}" "01"
done
# Hindi
for prefix in "dhrm" "dhrj"; do
    test_url "${prefix}1" "Grade 4 Hindi ${prefix}" "01"
done
echo ""

# GRADE 3 - Additional subjects
echo "=== GRADE 3 - ADDITIONAL SUBJECTS ==="
# English
for prefix in "cemg" "cemr"; do
    test_url "${prefix}1" "Grade 3 English ${prefix}" "01"
done
# Hindi
for prefix in "chrm" "chrj"; do
    test_url "${prefix}1" "Grade 3 Hindi ${prefix}" "01"
done
echo ""

# GRADE 10 - Additional Hindi literature
echo "=== GRADE 10 - ADDITIONAL HINDI PATTERNS ==="
for prefix in "jhkt" "jhkj" "jhks" "jhsn"; do
    test_url "${prefix}1" "Grade 10 Hindi ${prefix}" "01"
done
echo ""

# GRADE 9 - Additional Hindi literature
echo "=== GRADE 9 - ADDITIONAL HINDI PATTERNS ==="
for prefix in "ihkt" "ihsn"; do
    test_url "${prefix}1" "Grade 9 Hindi ${prefix}" "01"
done
echo ""

# GRADE 8 - Additional Hindi literature
echo "=== GRADE 8 - ADDITIONAL HINDI PATTERNS ==="
for prefix in "hhdu" "hhbv"; do
    test_url "${prefix}1" "Grade 8 Hindi ${prefix}" "01"
done
echo ""

# GRADE 7 - Additional Hindi literature
echo "=== GRADE 7 - ADDITIONAL HINDI PATTERNS ==="
for prefix in "ghdh" "ghdu"; do
    test_url "${prefix}1" "Grade 7 Hindi ${prefix}" "01"
done
echo ""

# GRADE 6 - Hindi literature
echo "=== GRADE 6 - HINDI LITERATURE ==="
for prefix in "fhvs" "fhps"; do
    test_url "${prefix}1" "Grade 6 Hindi ${prefix}" "01"
done
echo ""

echo "========================================================================"
echo "Pattern Discovery Complete!"
echo "========================================================================"
