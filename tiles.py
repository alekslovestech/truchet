"""
Tile/character operations for Truchet-style glyphs.
"""
from enum import Enum

INVERT: dict[str, str] = {
    " ": "X",
    "X": " ",
    "λ": "ɣ",
    "y": "ʎ",
    "ʎ": "y",
    "ɣ": "λ",
}


class Direction(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    TOP = "TOP"
    BOTTOM = "BOTTOM"


def available_directions(ch: str) -> list[Direction]:
    """
    Return the directions that are available for this tile character.
    """
    match ch:
        case " ":
            return []
        case "X":
            return [Direction.LEFT, Direction.RIGHT, Direction.TOP, Direction.BOTTOM]
        case "λ":
            return [Direction.LEFT, Direction.BOTTOM]
        case "ɣ":
            return [Direction.TOP, Direction.RIGHT]
        case "y":
            return [Direction.TOP, Direction.LEFT]
        case "ʎ":
            return [Direction.BOTTOM, Direction.RIGHT]
        case _:
            return []


def inverse(ch: str) -> str:
    """Return the inverted character. Unknown characters are returned unchanged."""
    return INVERT.get(ch, ch)
