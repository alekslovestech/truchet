"""
Text formatter module for rendering text as ASCII art letters.
"""
from letter_glyph import FRAMED_ROWS, LetterGlyph, UNFRAMED_COLS, create_inverted_letter


def combine_letters(letters: list[LetterGlyph], spacing: int = 1, rows: int = 5) -> list[str]:
    """
    Combine multiple letter glyphs horizontally.
    Assumes all glyphs have exactly `rows` lines.

    Args:
        letters: List of LetterGlyph instances
        spacing: Number of spaces between letters
        rows: Number of rows per letter (default UNFRAMED_ROWS; use FRAMED_ROWS for framed)

    Returns:
        Combined lines
    """
    if not letters:
        return []

    max_widths = [
        max(UNFRAMED_COLS, max(L.row_widths(rows)[r] for L in letters))
        for r in range(rows)
    ]
    padded_letters = [L.pad(max_widths, rows) for L in letters]

    result = []
    for row in range(rows):
        line_parts = [p[row] for p in padded_letters]
        result.append((" " * spacing).join(line_parts))

    return result


def combine_letters_vertical(letters: list[LetterGlyph]) -> list[str]:
    """
    Combine multiple letter glyphs vertically, appending one after the other.

    Args:
        letters: List of LetterGlyph instances

    Returns:
        Combined lines with letters stacked vertically
    """
    result = []
    for letter in letters:
        if letter:
            result.extend(letter)
            result.append("")  # Add a newline after each letter
        # Skip empty letters (spaces)

    return result


def process_text_empty_space(input_string: str) -> str:
    """
    Process the input string and return the graphical version with empty space letters.
    Each letter is shown as blank spaces within a 7×5 frame.
    
    Args:
        input_string: The text to process
        
    Returns:
        The processed graphical version with inverted letters
    """
    # Convert to lowercase and process
    text = input_string.lower()
    letters: list[LetterGlyph] = []

    for char in text:
        if char == " ":
            # Add a space (empty glyph) - full 7×5 X block
            letters.append(LetterGlyph(create_inverted_letter(LetterGlyph.empty())))
        elif char.isalpha():
            # Load the glyph and convert to empty space version
            glyph = LetterGlyph.load(char)
            if glyph:
                letters.append(LetterGlyph(create_inverted_letter(glyph)))
        # Skip non-alphabetic characters
    
    # Combine all letters
    if not letters:
        return ""
    
    result_lines = combine_letters(letters, spacing=1, rows=FRAMED_ROWS)
    return "\n".join(result_lines)


def process_text(input_string: str) -> str:
    """
    Process the input string and return the graphical version.
    
    Args:
        input_string: The text to process
        
    Returns:
        The processed graphical version of the text
    """
    # Convert to lowercase and process
    text = input_string.lower()
    letters: list[LetterGlyph] = []

    for char in text:
        if char == " ":
            # Add a space (empty glyph)
            letters.append(LetterGlyph.empty())
        elif char.isalpha():
            letters.append(LetterGlyph.load(char))
        # Skip non-alphabetic characters
    
    # Combine all letters
    if not letters:
        return ""
    
    result_lines = combine_letters(letters, spacing=1)
    return '\n'.join(result_lines)

