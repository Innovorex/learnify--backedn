#!/bin/bash
# Discover ALL URL patterns for all subjects grades 1-10

echo "========================================="
echo "Discovering ALL NCERT URL Patterns"
echo "========================================="
echo ""

test_url() {
    url=$1
    label=$2
    if curl -s -I "$url" 2>/dev/null | grep -q "200 OK"; then
        echo "✅ $label: FOUND"
        return 0
    else
        echo "❌ $label"
        return 1
    fi
}

# GRADE 10
echo "=== GRADE 10 ==="
test_url "https://ncert.nic.in/textbook/pdf/jeel101.pdf" "English First Flight (jeel1)"
test_url "https://ncert.nic.in/textbook/pdf/jeep101.pdf" "English Footprints (jeep1)"
test_url "https://ncert.nic.in/textbook/pdf/jhkt101.pdf" "Hindi Kshitij (jhkt1)"
test_url "https://ncert.nic.in/textbook/pdf/jhsn101.pdf" "Hindi Sanchayan (jhsn1)"
test_url "https://ncert.nic.in/textbook/pdf/jhkr101.pdf" "Hindi Kritika (jhkr1)"
echo ""

# GRADE 9
echo "=== GRADE 9 ==="
test_url "https://ncert.nic.in/textbook/pdf/ieel101.pdf" "English Beehive (ieel1)"
test_url "https://ncert.nic.in/textbook/pdf/ieep101.pdf" "English Moments (ieep1)"
test_url "https://ncert.nic.in/textbook/pdf/ihkt101.pdf" "Hindi Kshitij (ihkt1)"
test_url "https://ncert.nic.in/textbook/pdf/ihkr101.pdf" "Hindi Kritika (ihkr1)"
test_url "https://ncert.nic.in/textbook/pdf/ihsn101.pdf" "Hindi Sanchayan (ihsn1)"
echo ""

# GRADE 8
echo "=== GRADE 8 ==="
test_url "https://ncert.nic.in/textbook/pdf/heel101.pdf" "English Honeydew (heel1)"
test_url "https://ncert.nic.in/textbook/pdf/heep101.pdf" "English It So Happened (heep1)"
test_url "https://ncert.nic.in/textbook/pdf/hess101.pdf" "Social Science (hess1)"
test_url "https://ncert.nic.in/textbook/pdf/hhdr101.pdf" "Hindi Durva (hhdr1)"
test_url "https://ncert.nic.in/textbook/pdf/hhbv101.pdf" "Hindi Bharat Vi Khoj (hhbv1)"
echo ""

# GRADE 7
echo "=== GRADE 7 ==="
test_url "https://ncert.nic.in/textbook/pdf/geel101.pdf" "English Honeycomb (geel1)"
test_url "https://ncert.nic.in/textbook/pdf/geep101.pdf" "English An Alien Hand (geep1)"
test_url "https://ncert.nic.in/textbook/pdf/ghvs101.pdf" "Hindi Vasant (ghvs1)"
test_url "https://ncert.nic.in/textbook/pdf/ghdr101.pdf" "Hindi Durva (ghdr1)"
test_url "https://ncert.nic.in/textbook/pdf/gess101.pdf" "Social Science (gess1)"
echo ""

# GRADE 6
echo "=== GRADE 6 ==="
test_url "https://ncert.nic.in/textbook/pdf/fess101.pdf" "Social Science (fess1)"
test_url "https://ncert.nic.in/textbook/pdf/feel101.pdf" "English (feel1)"
test_url "https://ncert.nic.in/textbook/pdf/fhvs101.pdf" "Hindi Vasant (fhvs1)"
echo ""

# GRADE 5
echo "=== GRADE 5 ==="
test_url "https://ncert.nic.in/textbook/pdf/eeel101.pdf" "English Marigold (eeel1)"
test_url "https://ncert.nic.in/textbook/pdf/eerm101.pdf" "English Raindrops (eerm1)"
test_url "https://ncert.nic.in/textbook/pdf/ehri101.pdf" "Hindi Rimjhim (ehri1)"
echo ""

# GRADE 4
echo "=== GRADE 4 ==="
test_url "https://ncert.nic.in/textbook/pdf/deel101.pdf" "English Marigold (deel1)"
test_url "https://ncert.nic.in/textbook/pdf/dhri101.pdf" "Hindi Rimjhim (dhri1)"
echo ""

# GRADE 3
echo "=== GRADE 3 ==="
test_url "https://ncert.nic.in/textbook/pdf/ceel101.pdf" "English Marigold (ceel1)"
test_url "https://ncert.nic.in/textbook/pdf/chri101.pdf" "Hindi Rimjhim (chri1)"
test_url "https://ncert.nic.in/textbook/pdf/ceev101.pdf" "EVS (ceev1)"
echo ""

# GRADE 2
echo "=== GRADE 2 ==="
test_url "https://ncert.nic.in/textbook/pdf/beel101.pdf" "English Marigold (beel1)"
test_url "https://ncert.nic.in/textbook/pdf/berm101.pdf" "English Raindrops (berm1)"
test_url "https://ncert.nic.in/textbook/pdf/bhri101.pdf" "Hindi Rimjhim (bhri1)"
test_url "https://ncert.nic.in/textbook/pdf/beev101.pdf" "EVS (beev1)"
echo ""

# GRADE 1
echo "=== GRADE 1 ==="
test_url "https://ncert.nic.in/textbook/pdf/aeel101.pdf" "English Marigold (aeel1)"
test_url "https://ncert.nic.in/textbook/pdf/aerm101.pdf" "English Raindrops (aerm1)"
test_url "https://ncert.nic.in/textbook/pdf/ahri101.pdf" "Hindi Rimjhim (ahri1)"
test_url "https://ncert.nic.in/textbook/pdf/aeev101.pdf" "EVS (aeev1)"
echo ""

echo "========================================="
echo "Pattern Discovery Complete!"
echo "========================================="
