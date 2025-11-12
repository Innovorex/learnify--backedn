"""
Board value mapper - Maps ERPNext board names to database board names

This module handles the mapping between different board naming conventions:
- ERPNext may return: "CBSE", "State", "State Board", "Telangana State Board"
- Database uses: "CBSE" or "TELANGANA"
"""


def map_board_to_db(erpnext_board: str) -> str:
    """
    Map ERPNext board value to database board name

    ERPNext Values → Database Values:
    - "CBSE" → "CBSE"
    - "State" → "TELANGANA"
    - "State Board" → "TELANGANA"
    - "Telangana State Board" → "TELANGANA"
    - "SCERT" → "TELANGANA"

    Args:
        erpnext_board: Board value from ERPNext (can be mixed case)

    Returns:
        str: Normalized board name ("CBSE" or "TELANGANA")

    Examples:
        >>> map_board_to_db("State")
        'TELANGANA'
        >>> map_board_to_db("CBSE")
        'CBSE'
        >>> map_board_to_db("state board")
        'TELANGANA'
    """
    if not erpnext_board:
        return "CBSE"  # Default

    board_lower = erpnext_board.lower().strip()

    # State board variations
    state_keywords = ["state", "telangana", "scert", "ts board"]
    if any(keyword in board_lower for keyword in state_keywords):
        return "TELANGANA"

    # CBSE
    if "cbse" in board_lower:
        return "CBSE"

    # ICSE (if ever added in future)
    if "icse" in board_lower:
        return "ICSE"

    # Default to CBSE
    return "CBSE"


def map_board_to_display(db_board: str) -> str:
    """
    Map database board name to user-friendly display name

    Database → Display:
    - "CBSE" → "CBSE"
    - "TELANGANA" → "Telangana State Board"
    - "ICSE" → "ICSE"

    Args:
        db_board: Board value from database

    Returns:
        str: User-friendly display name

    Examples:
        >>> map_board_to_display("TELANGANA")
        'Telangana State Board'
        >>> map_board_to_display("CBSE")
        'CBSE'
    """
    board_display_map = {
        "TELANGANA": "Telangana State Board",
        "CBSE": "CBSE",
        "ICSE": "ICSE"
    }

    return board_display_map.get(db_board, db_board)


def get_board_abbreviation(db_board: str) -> str:
    """
    Get short abbreviation for board

    Args:
        db_board: Board value from database

    Returns:
        str: Short abbreviation

    Examples:
        >>> get_board_abbreviation("TELANGANA")
        'TS'
        >>> get_board_abbreviation("CBSE")
        'CBSE'
    """
    abbreviations = {
        "TELANGANA": "TS",
        "CBSE": "CBSE",
        "ICSE": "ICSE"
    }

    return abbreviations.get(db_board, db_board)
