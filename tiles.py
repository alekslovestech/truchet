"""
Tile/character operations for Truchet-style glyphs.
"""
from enum import Enum
from typing import Literal

TileChar = Literal[" ", "X", "λ", "ɣ", "y", "ʎ"]

class Direction(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    TOP = "TOP"
    BOTTOM = "BOTTOM"

class Corners(Enum):
    TOP_LEFT = "TOP_LEFT"
    TOP_RIGHT = "TOP_RIGHT"
    BOTTOM_LEFT = "BOTTOM_LEFT"
    BOTTOM_RIGHT = "BOTTOM_RIGHT"


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

def available_corners(ch: TileChar) -> list[Corners]:
    """
    Return the corners that are available for this tile character.
    """
    match ch:
        case " ":
            return []
        case "X":
            return [Corners.TOP_LEFT, Corners.TOP_RIGHT, Corners.BOTTOM_LEFT, Corners.BOTTOM_RIGHT]
        case "λ":
            return [Corners.BOTTOM_LEFT, Corners.BOTTOM_RIGHT, Corners.TOP_LEFT]
        case "ɣ":
            return [Corners.TOP_RIGHT, Corners.BOTTOM_RIGHT, Corners.TOP_LEFT]
        case "y":
            return [Corners.TOP_LEFT, Corners.BOTTOM_LEFT, Corners.TOP_RIGHT]
        case "ʎ":
            return [Corners.BOTTOM_RIGHT, Corners.BOTTOM_LEFT, Corners.TOP_RIGHT]
        case _:
            return []

def unavailable_corners(ch: TileChar) -> list[Corners]:
    match ch:        
        case "λ":
            return [Corners.TOP_RIGHT]
        case "ɣ":
            return [Corners.BOTTOM_LEFT]
        case "y":
            return [Corners.BOTTOM_RIGHT]
        case "ʎ":
            return [Corners.TOP_LEFT]
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
