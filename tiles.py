"""
Tile/character operations for Truchet-style glyphs.
"""

INVERT: dict[str, str] = {
    " ": "X",
    "X": " ",
    "λ": "ɣ",
    "y": "ʎ",
    "ʎ": "y",
    "ɣ": "λ",
}


def inverse(ch: str) -> str:
    """Return the inverted character. Unknown characters are returned unchanged."""
    return INVERT.get(ch, ch)
