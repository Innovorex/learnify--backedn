#!/bin/bash
# Comprehensive URL pattern testing for ALL remaining subjects

echo "========================================================================"
echo "COMPREHENSIVE URL PATTERN DISCOVERY - ALL REMAINING SUBJECTS"
echo "========================================================================"
echo ""

test_pattern() {
    pattern=$1
    name=$2
    test_ch=$3

    url="https://ncert.nic.in/textbook/pdf/${pattern}${test_ch}.pdf"
    if curl -s -I "$url" 2>/dev/null | grep -q "200 OK"; then
        echo "✅ $name ($pattern)"
        return 0
    else
        return 1
    fi
}

# GRADE 10 - English patterns
echo "=== GRADE 10 - ENGLISH ==="
for prefix in "jeel" "jeff" "jefp" "jefl" "keel" "keff"; do
    test_pattern "${prefix}1" "English ${prefix}" "01"
done
echo ""

# GRADE 9 - English patterns
echo "=== GRADE 9 - ENGLISH ==="
for prefix in "ieel" "iebh" "iemm" "iefl" "ieff"; do
    test_pattern "${prefix}1" "English ${prefix}" "01"
done
echo ""

# GRADE 8 - English patterns
echo "=== GRADE 8 - ENGLISH ==="
for prefix in "heel" "hehd" "heis" "hefl"; do
    test_pattern "${prefix}1" "English ${prefix}" "01"
done
echo ""

# GRADE 7 - English patterns
echo "=== GRADE 7 - ENGLISH ==="
for prefix in "geel" "gehc" "geah" "gefl"; do
    test_pattern "${prefix}1" "English ${prefix}" "01"
done
echo ""

# GRADE 6 - English patterns
echo "=== GRADE 6 - ENGLISH ==="
for prefix in "feel" "fehc" "fefl"; do
    test_pattern "${prefix}1" "English ${prefix}" "01"
done
echo ""

# GRADE 5 - English & Hindi
echo "=== GRADE 5 ==="
for prefix in "eeel" "eerm" "eemg" "ehri" "ehrm"; do
    test_pattern "${prefix}1" "Grade 5 ${prefix}" "01"
done
echo ""

# GRADE 4 - English & Hindi
echo "=== GRADE 4 ==="
for prefix in "deel" "demg" "dhri" "dhrm"; do
    test_pattern "${prefix}1" "Grade 4 ${prefix}" "01"
done
echo ""

# GRADE 3 - English & Hindi
echo "=== GRADE 3 ==="
for prefix in "ceel" "cemg" "chri" "chrm"; do
    test_pattern "${prefix}1" "Grade 3 ${prefix}" "01"
done
echo ""

# GRADE 2 - ALL subjects
echo "=== GRADE 2 ==="
for prefix in "bemm" "beev" "beel" "berm" "bemg" "bhri" "bhrm"; do
    test_pattern "${prefix}1" "Grade 2 ${prefix}" "01"
done
echo ""

# GRADE 1 - ALL subjects
echo "=== GRADE 1 ==="
for prefix in "aemm" "aeev" "aeel" "aerm" "aemg" "ahri" "ahrm" "aejm"; do
    test_pattern "${prefix}1" "Grade 1 ${prefix}" "01"
done
echo ""

# Additional Social Science patterns
echo "=== SOCIAL SCIENCE - DETAILED ==="
for grade_prefix in "j" "i" "h" "g" "f"; do
    for subj in "ehs" "egy" "eps" "eec" "ess"; do
        pattern="${grade_prefix}${subj}1"
        test_pattern "$pattern" "Social ${pattern}" "01"
    done
done
echo ""

echo "========================================================================"
echo "Pattern Discovery Complete!"
echo "========================================================================"
