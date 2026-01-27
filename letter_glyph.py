"""
LetterGlyph: loading and transforming ASCII art glyphs for letters.
"""
from pathlib import Path

from tiles import inverse, TileChar

# Unframed: 5 rows
UNFRAMED_ROWS = 5

class LetterGlyph:
    """
    Unframed ASCII art glyph for a letter: a list of character rows.
    Empty glyph (e.g. for space) has no rows.
    """

    def __init__(self, lines: list[str]) -> None:
        self._lines = lines  # type: list[str]  # each string is a row of TileChar chars
        self.width = max(len(line) for line in lines) if lines else 0  # Calculate the width dynamically

    @property
    def lines(self) -> list[str]:
        return self._lines

    @classmethod
    def load(cls, char: TileChar) -> "LetterGlyph":
        """
        Load the glyph for a letter from the data folder.

        Args:
            char: The letter to load (lowercase)

        Returns:
            LetterGlyph with its lines, or empty LetterGlyph if not found
        """
        data_dir = Path(__file__).parent / "data"
        letter_file = data_dir / f"{char}.txt"

        if not letter_file.exists():
            return cls([])

        with open(letter_file, "r", encoding="utf-8") as f:
            raw = f.readlines()

        # Each line is intended to be a str of TileChar
        lines: list[str] = [line.rstrip("\n\r") for line in raw]
        while lines and not lines[-1]:
            lines.pop()

        # Pad each row to the maximum width of the glyph
        max_width = max(len(line) for line in lines) if lines else 0
        padded_lines = [line.ljust(max_width) for line in lines]

        return cls(padded_lines)

    @classmethod
    def empty(cls) -> "LetterGlyph":
        """Empty glyph (e.g. for space)."""
        return cls([])

    def pad(self, max_widths: list[int], rows: int) -> "LetterGlyph":
        """
        Pad the glyph to match the maximum widths for each row.

        Args:
            max_widths: The maximum width for each row
            rows: The number of rows in the glyph

        Returns:
            A padded list of strings representing the glyph
        """
        padded = []
        for row in range(rows):
            if row < len(self._lines):
                line = self._lines[row].ljust(max_widths[row])
            else:
                line = " " * max_widths[row]
            padded.append(line)
        return LetterGlyph(padded)

    def __bool__(self) -> bool:
        return bool(self._lines)

    def __getitem__(self, i: int) -> str:
        return self._lines[i]

    def __iter__(self):
        return iter(self._lines)

    def __len__(self) -> int:
        return len(self._lines)

    def letter_width(self) -> int:
        """
        Calculate the maximum width of the letter glyph.

        Returns:
            The maximum width of the letter glyph
        """
        return max((len(row) for row in self._lines), default=0)


def create_inverted_letter(glyph: LetterGlyph) -> list[str]:
    """
    Create an inverted version of a letter glyph using tile inverse.
    Does NOT handle framing or padding.
    """
    if not glyph:
        return []

    # Invert each row of the glyph
    return ["".join(inverse(c) for c in row) for row in glyph]
