#!/usr/bin/env python3
"""
Chanakya/Kruti Dev to Unicode Devanagari Converter
===================================================
Converts legacy Chanakya/Kruti Dev encoded text to proper Unicode Devanagari.

NCERT Hindi PDFs use fonts like "Walkman-Chanakya905" which are NOT Unicode.
They use custom glyph mappings that need to be converted.
"""

# Chanakya to Unicode mapping (comprehensive)
CHANAKYA_TO_UNICODE = {
    # Vowels
    'v': 'अ', 'vk': 'आ', 'b': 'इ', 'bZ': 'ई', 'mq': 'उ', 'Å': 'ऊ',
    '½': 'ऋ', ',': ',', ';': ';', '/': '/', '\\': '।',

    # Consonants
    'd': 'क', 'D': 'क्', '[k': 'ख', '[': 'ख्', 'x': 'ग', 'X': 'ग्',
    '?k': 'घ', '?': 'घ्', 'M': 'ङ',
    'p': 'च', 'P': 'च्', 'N': 'छ', 't': 'ज', 'T': 'ज्',
    '÷': 'झ', '×': 'झ्', '´': 'ञ',
    'V': 'ट', 'B': 'ठ', 'M': 'ड', '¡': 'ढ', '.k': 'ण',
    'r': 'त', 'R': 'त्', 'F': 'थ', 'n': 'द', 'N': 'द्',
    '/k': 'ध', '\\': 'ध्', 'u': 'न', 'U': 'न्',
    'i': 'प', 'I': 'प्', 'iQ': 'फ', 'Q': 'फ्', 'c': 'ब', 'C': 'ब्',
    'Hk': 'भ', 'H': 'भ्', 'e': 'म', 'E': 'म्',
    ';': 'य', ';': 'य्', 'j': 'र', 'J': 'र्', 'y': 'ल', 'Y': 'ल्',
    'o': 'व', 'O': 'व्', '\'k': 'श', '\"': 'ष', 'l': 'स', 'L': 'स्',
    'g': 'ह', 'G': 'ह्', 'K': 'ज्ञ',

    # Matras (vowel signs)
    'k': 'ा', 'h': 'ि', 'S': 'ी', 'q': 'ु', 'w': 'ू', 's': 'े',
    'S': 'ै', 'ksa': 'ों', 'kas': 'ौ',

    # Special characters
    '&': 'ं', '¡': 'ँ', '\\': ':', 'A': 'ः', '~': 'ऽ',
    'a': '्', '\\': '।', '॥': '॥',

    # Numbers
    '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
    '5': '५', '6': '६', '7': '७', '8': '८', '9': '९',

    # Common combinations
    'os': 'के', 'oQ': 'कि', 'dh': 'की', 'dk': 'का', 'dks': 'को',
    'osQ': 'के', 'ds': 'के', 'dh': 'की', 'esa': 'में', 'eas': 'में',
    'us': 'ने', 'ls': 'से', 'gS': 'है', 'gSa': 'हैं', 'Fkk': 'था',
    'Fks': 'थे', 'Fkh': 'थी', 'Fkha': 'थीं',
}

# Extended mapping for better coverage
CHANAKYA_EXTENDED = {
    # More complex combinations
    'ftu': 'जिन', 'ftl': 'जिस', 'Øe': 'क्रम', 'iz': 'प्र',
    'xzke': 'ग्राम', 'f\'k{kk': 'शिक्षा', 'iqLrd': 'पुस्तक',
    'vo\';': 'अवश्य', 'vU;': 'अन्य', 'lekt': 'समाज',
}


def chanakya_to_unicode(text):
    """
    Convert Chanakya/Kruti Dev encoded text to Unicode Devanagari.

    Args:
        text: String in Chanakya encoding

    Returns:
        String in proper Unicode Devanagari
    """
    if not text:
        return text

    result = text

    # First apply extended mappings (longer patterns)
    for chanakya, unicode_char in sorted(CHANAKYA_EXTENDED.items(), key=lambda x: -len(x[0])):
        result = result.replace(chanakya, unicode_char)

    # Then apply basic mappings
    for chanakya, unicode_char in sorted(CHANAKYA_TO_UNICODE.items(), key=lambda x: -len(x[0])):
        result = result.replace(chanakya, unicode_char)

    return result


def is_chanakya_encoded(text):
    """
    Detect if text is in Chanakya encoding.

    Returns True if text contains Chanakya-specific patterns.
    """
    if not text:
        return False

    # Check for common Chanakya patterns
    chanakya_indicators = ['osQ', 'esa', 'gS', 'Fkk', 'dk', 'dh']

    for indicator in chanakya_indicators:
        if indicator in text[:500]:  # Check first 500 chars
            return True

    return False


def test_conversion():
    """Test the conversion with sample text"""
    test_cases = [
        ("johna uz kFk BkoQq j", "रवीन्द्रनाथ ठाकुर"),  # Should convert
        ("6 ebZ 1861 dks caxky osQ ,d laiUu", "६ मई १८६१ को बंगाल के एक संपन्न"),
        ("ftl iqLrd ls ;g mís';", "जिस पुस्तक से यह उद्देश्य"),
    ]

    print("Testing Chanakya to Unicode conversion:\n")
    for chanakya, expected in test_cases:
        converted = chanakya_to_unicode(chanakya)
        print(f"Input:    {chanakya}")
        print(f"Output:   {converted}")
        print(f"Expected: {expected}")
        print()


if __name__ == "__main__":
    test_conversion()
