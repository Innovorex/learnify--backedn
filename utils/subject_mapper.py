"""
Subject Name Mapper - Normalizes different subject name variations

This module handles mapping between different subject naming conventions:
- ERPNext/UI may use: "Maths", "Math", "EVS"
- Database uses: "Mathematics", "Environmental Education"
"""


def normalize_subject_name(subject: str) -> str:
    """
    Normalize subject name for database queries

    Args:
        subject: Subject name from UI/ERPNext

    Returns:
        str: Normalized subject name for database

    Examples:
        >>> normalize_subject_name("Maths")
        'Mathematics'
        >>> normalize_subject_name("Math")
        'Mathematics'
        >>> normalize_subject_name("EVS")
        'Environmental Education'
    """
    if not subject:
        return subject

    subject_lower = subject.lower().strip()

    # Mathematics variations
    if subject_lower in ["maths", "math", "mathematics"]:
        return "Mathematics"

    # Science (already correct in most cases)
    if subject_lower in ["science", "sciences"]:
        return "Science"

    # English (already correct)
    if subject_lower in ["english"]:
        return "English"

    # Hindi variations
    if subject_lower in ["hindi", "hindi first language", "hindi 1st language"]:
        return "Hindi First Language"

    if subject_lower in ["hindi second language", "hindi 2nd language"]:
        return "Hindi Second Language"

    # Telugu variations
    if subject_lower in ["telugu", "telugu first language", "telugu 1st language"]:
        return "Telugu First Language"

    if subject_lower in ["telugu second language", "telugu 2nd language"]:
        return "Telugu Second Language"

    # Social Studies / Social Science
    if subject_lower in ["social", "social studies", "social science", "ss"]:
        return "Social Studies"

    # Environmental Education / EVS
    if subject_lower in ["evs", "environmental education", "environmental studies", "env"]:
        return "Environmental Education"

    # Physical Science
    if subject_lower in ["physical science", "physics"]:
        return "Physical Science"

    # Biological Science
    if subject_lower in ["biological science", "biology", "bio"]:
        return "Biological Science"

    # If no mapping found, return original (with title case)
    return subject.title()


def get_subject_variations(subject: str) -> list:
    """
    Get all possible variations of a subject name for flexible matching

    Args:
        subject: Normalized subject name

    Returns:
        list: All possible variations

    Examples:
        >>> get_subject_variations("Mathematics")
        ['Mathematics', 'Maths', 'Math']
    """
    subject_lower = subject.lower().strip()

    variations = [subject]  # Always include original

    if subject_lower == "mathematics":
        variations.extend(["Maths", "Math"])

    elif subject_lower == "environmental education":
        variations.extend(["EVS", "Evs", "Environmental Studies"])

    elif subject_lower == "social studies":
        variations.extend(["Social Science", "Social", "SS"])

    elif subject_lower == "hindi first language":
        variations.extend(["Hindi", "Hindi 1st Language"])

    elif subject_lower == "telugu first language":
        variations.extend(["Telugu", "Telugu 1st Language"])

    elif subject_lower == "physical science":
        variations.extend(["Physics"])

    elif subject_lower == "biological science":
        variations.extend(["Biology", "Bio"])

    return list(set(variations))  # Remove duplicates
