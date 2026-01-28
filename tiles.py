"""
Tile/character operations for Truchet-style glyphs.
"""
from enum import Enum
from typing import Literal, TypeGuard

TileChar = Literal[" ", "X", "λ", "ɣ", "y", "ʎ"]

class Direction(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    TOP = "TOP"
    BOTTOM = "BOTTOM"


def available_directions(ch: TileChar) -> list[Direction]:
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


def inverse(ch: TileChar) -> TileChar:
    """Return the inverted tile (e.g. λ↔ɣ, X↔space)."""
    match ch:
        case " ":
            return "X"
        case "X":
            return " "
        case "λ":
            return "ɣ"
        case "ɣ":
            return "λ"
        case "y":
            return "ʎ"
        case "ʎ":
            return "y"
        case _:
            return ch
