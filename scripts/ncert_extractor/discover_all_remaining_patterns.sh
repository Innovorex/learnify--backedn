#!/bin/bash
# Aggressive pattern discovery for ALL remaining content

echo "========================================================================"
echo "AGGRESSIVE URL PATTERN DISCOVERY - ALL REMAINING SUBJECTS"
echo "========================================================================"
echo ""

test_url() {
    url="https://ncert.nic.in/textbook/pdf/$1.pdf"
    if curl -s -I "$url" 2>/dev/null | grep -q "200 OK"; then
        echo "✅ FOUND: $2 ($1)"
        return 0
    fi
    return 1
}

echo "=== GRADE 9 - ENGLISH (Beehive, Moments) ==="
for p in "iebh1" "ieel1" "iemm1" "iemt1" "iebe1"; do test_url "${p}01" "Grade 9 English $p"; done
echo ""

echo "=== GRADE 6 - ALL MISSING SUBJECTS ==="
for p in "feel1" "fehc1" "feem1" "fhvs1" "fhri1" "fess1"; do test_url "${p}01" "Grade 6 $p"; done
echo ""

echo "=== GRADE 5 - ENGLISH & HINDI ==="
for p in "eeel1" "eemg1" "eemr1" "ehrm1" "ehri1" "eerm1"; do test_url "${p}01" "Grade 5 $p"; done
echo ""

echo "=== GRADE 4 - ENGLISH & HINDI ==="
for p in "deel1" "demg1" "derm1" "dhri1" "dhrm1"; do test_url "${p}01" "Grade 4 $p"; done
echo ""

echo "=== GRADE 3 - ENGLISH & HINDI ==="
for p in "ceel1" "cemg1" "cerm1" "chri1" "chrm1"; do test_url "${p}01" "Grade 3 $p"; done
echo ""

echo "=== GRADE 2 - ALL SUBJECTS (Multiple Patterns) ==="
# Math patterns
for p in "bemm1" "bejm1" "bemh1"; do test_url "${p}01" "Grade 2 Math $p"; done
# English patterns
for p in "beel1" "bemg1" "berm1" "bema1"; do test_url "${p}01" "Grade 2 English $p"; done
# Hindi patterns
for p in "bhri1" "bhrm1" "bhim1"; do test_url "${p}01" "Grade 2 Hindi $p"; done
# EVS patterns
for p in "beev1" "bela1" "beap1"; do test_url "${p}01" "Grade 2 EVS $p"; done
echo ""

echo "=== GRADE 1 - REMAINING SUBJECTS ==="
for p in "aeel1" "aemg1" "aerm1" "aema1" "ahri1" "ahrm1" "ahim1" "aeev1" "aela1" "aeap1"; do test_url "${p}01" "Grade 1 $p"; done
echo ""

echo "=== HINDI LITERATURE - ALL GRADES ==="
# Grade 10 Hindi
for p in "jhkt1" "jhsn1" "jhkh1"; do test_url "${p}01" "Grade 10 Hindi $p"; done
# Grade 9 Hindi
for p in "ihkt1" "ihsn1" "ihkh1"; do test_url "${p}01" "Grade 9 Hindi $p"; done
# Grade 8 Hindi
for p in "hhbk1" "hhdr1" "hhbv1"; do test_url "${p}01" "Grade 8 Hindi $p"; done
# Grade 7 Hindi
for p in "ghdr1" "ghmh1"; do test_url "${p}01" "Grade 7 Hindi $p"; done
# Grade 6 Hindi
for p in "fhvs1" "fhri1" "fhdr1"; do test_url "${p}01" "Grade 6 Hindi $p"; done
echo ""

echo "=== SOCIAL SCIENCE - DETAILED SUBJECTS ==="
# Grade 8 Social Science
for p in "hess1" "hehs1" "hegy1" "heps1"; do test_url "${p}01" "Grade 8 Social $p"; done
# Grade 6 Social Science
for p in "fess1" "fehs1" "fegy1" "feps1"; do test_url "${p}01" "Grade 6 Social $p"; done
echo ""

echo "=== ADDITIONAL EVS PATTERNS ==="
for g in "e" "d" "c"; do
    for p in "eev" "ela" "eap"; do
        test_url "${g}${p}101" "Grade EVS ${g}${p}1"
    done
done
echo ""

echo "========================================================================"
echo "Discovery Complete!"
echo "========================================================================"
