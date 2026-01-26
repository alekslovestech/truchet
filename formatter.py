"""
Text formatter module for rendering text as ASCII art letters.
"""
from letter_glyph import UNFRAMED_ROWS, LetterGlyph, UNFRAMED_COLS, create_inverted_letter


def combine_letters(letters: list[LetterGlyph], isInverted: bool) -> list[str]:
    """
    Combine multiple letter glyphs horizontally with shared borders.
    Assumes all glyphs have exactly `rows` lines.

    Args:
        letters: List of LetterGlyph instances
        isInverted: Whether the letters are inverted (empty-space style)
    Returns:
        Combined lines
    """
    rows = UNFRAMED_ROWS
    if not letters:
        return []

    max_widths = [
        max(UNFRAMED_COLS, max(L.row_widths(rows)[r] for L in letters))
        for r in range(rows)
    ]
    padded_letters = [L.pad(max_widths, rows) for L in letters]

    result = []
    for row in range(rows):
        line_parts = []
        for i, letter in enumerate(padded_letters):
            # Remove the right border of all but the last letter
            if i < len(padded_letters) - 1:
                line_parts.append(letter[row])  # Exclude the last character (right border)
            else:
                line_parts.append(letter[row])  # Keep the full row for the last letter

        # Join the parts with the specified spacing
        SPACING_CHARACTER = "X" if isInverted else " "
        result.append((SPACING_CHARACTER * 1).join(line_parts))

    return result


def process_text_empty_space(input_string: str) -> str:
    """
    Process the input string and return the graphical version with empty space letters.
    Each letter is shown as blank spaces, and the frame is added afterward.
    
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
            # Add a space (empty glyph) without a frame
            letters.append(LetterGlyph.empty())
        elif char.isalpha():
            # Load the glyph and convert to an inverted version without a frame
            glyph = LetterGlyph.load(char)
            if glyph:
                inverted_glyph = create_inverted_letter(glyph)
                letters.append(LetterGlyph(inverted_glyph))
        # Skip non-alphabetic characters
    
    # Combine all letters without a frame
    if not letters:
        return ""
    
    combined_lines = combine_letters(letters, isInverted=True)  # Exclude top and bottom frame rows

    # Add the frame around the combined result
    top_frame = "X" * (len(combined_lines[0]) + 2)
    framed_result = [top_frame]
    for line in combined_lines:
        framed_result.append(f"X{line}X")
    framed_result.append(top_frame)

    return "\n".join(framed_result)


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
    
    result_lines = combine_letters(letters, isInverted=False)
    return '\n'.join(result_lines)

