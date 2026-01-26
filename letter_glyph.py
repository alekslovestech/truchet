"""
LetterGlyph: loading and transforming ASCII art glyphs for letters.
"""
from pathlib import Path

from tiles import inverse, TileChar

# Unframed: 5 rows, min 3 cols per row
UNFRAMED_ROWS = 5
UNFRAMED_COLS = 3
# Framed (inverted): 7×5 with X frame
FRAMED_ROWS = 7
FRAMED_COLS = 5


class LetterGlyph:
    """
    Unframed ASCII art glyph for a letter: a list of character rows.
    Empty glyph (e.g. for space) has no rows.
    """

    def __init__(self, lines: list[str]) -> None:
        self._lines = lines  # type: list[str]  # each string is a row of TileChar chars

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

        return cls(lines)

    @classmethod
    def empty(cls) -> "LetterGlyph":
        """Empty glyph (e.g. for space)."""
        return cls([])

    def row_widths(self, rows: int) -> list[int]:
        """
        Width of each row. Present rows use at least UNFRAMED_COLS; missing rows are 0.

        Args:
            rows: Number of rows to consider

        Returns:
            List of length `rows`: for each index, max(UNFRAMED_COLS, len(row)) if exists, else 0
        """
        result = []
        for r in range(rows):
            if r < len(self._lines):
                result.append(max(UNFRAMED_COLS, len(self._lines[r])))
            else:
                result.append(0)
        return result

    def pad(self, row_widths: list[int], rows: int) -> "LetterGlyph":
        """
        Pad this glyph to the given row widths and row count.
        Each row is left-justified to row_widths[r]; missing rows become spaces.

        Args:
            row_widths: Target width for each row (length must be >= rows)
            rows: Number of rows to produce

        Returns:
            New LetterGlyph with exactly `rows` lines. Empty glyph → [""] * rows.
        """
        if not self._lines:
            return LetterGlyph([""] * rows)
        padded: list[str] = []
        for r in range(rows):
            if r < len(self._lines):
                padded.append(self._lines[r].ljust(row_widths[r]))
            else:
                padded.append(" " * row_widths[r])
        return LetterGlyph(padded)

    def __bool__(self) -> bool:
        return bool(self._lines)

    def __getitem__(self, i: int) -> str:
        return self._lines[i]

    def __iter__(self):
        return iter(self._lines)

    def __len__(self) -> int:
        return len(self._lines)


def create_inverted_letter(glyph: LetterGlyph) -> list[str]:
    """
    Create an inverted (framed) version of a letter glyph using tile inverse.
    Returns 7×5 (FRAMED_ROWS × FRAMED_COLS): 1 X row top, 5 content, 1 X row bottom.
    Empty glyph → full X block.

    This is framed logic; it returns raw list[str] for the caller to wrap in LetterGlyph if needed.
    """
    if not glyph:
        return ["X" * FRAMED_COLS] * FRAMED_ROWS

    frame: TileChar = "X"
    frame_row: str = frame * FRAMED_COLS
    content_width = FRAMED_COLS - 2  # 1 left + 1 right X
    content: list[str] = []
    for row in glyph:
        # row is a string of TileChar
        inverted_row = "".join(inverse(c) for c in row)  # type: ignore
        inverted_row = inverted_row[:content_width].ljust(content_width, "X")
        content.append(frame + inverted_row + frame)

    content_height = UNFRAMED_ROWS
    while len(content) < content_height:
        content.append(frame + ("X" * content_width) + frame)
    content = content[:content_height]

    return [frame_row] + content + [frame_row]
