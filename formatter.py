"""
Text formatter module for rendering text as ASCII art letters.
"""
from letter_glyph import UNFRAMED_ROWS, LetterGlyph, create_inverted_letter


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

    # Pad each letter to its own width
    padded_letters = [L.pad([L.letter_width()] * rows, rows) for L in letters]

    result = []
    for row in range(rows):
        line_parts = []
        for i, letter in enumerate(padded_letters):
            # Remove the right border of all but the last letter
            line_parts.append(letter[row])  # Exclude the last character (right border)

        # Join the parts with the specified spacing
        SPACING_CHARACTER = "X" if isInverted else " "
        result.append((SPACING_CHARACTER).join(line_parts))

    return result


def process_text(input_string: str, is_inverted: bool = False) -> str:
    """
    Process the input string and return the graphical version.

    Args:
        input_string: The text to process
        is_inverted: Whether to use inverted (empty-space) style
        
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
            glyph = LetterGlyph.load(char)
            if glyph:
                if is_inverted:
                    glyph = create_inverted_letter(glyph)
                letters.append(LetterGlyph(glyph))

    if not letters:
        return ""

    # Combine letters into lines
    combined_lines = combine_letters(letters, isInverted=is_inverted)

    # Add a frame if required
    if is_inverted:
        top_frame = "X" * (len(combined_lines[0]) + 2)
        framed_result = [top_frame]
        for line in combined_lines:
            framed_result.append(f"X{line}X")
        framed_result.append(top_frame)
        return "\n".join(framed_result)

    return "\n".join(combined_lines)


def frame_word(word: list[list[str]], width: int, height: int, fill_char: str = "X") -> list[str]:
    """
    Frame a word (list of letter rows) to a specific width and height.

    Args:
        word: A list of rows representing the word (each row is a list of strings).
        width: The desired width of the framed word.
        height: The desired height of the framed word.
        fill_char: The character to use for padding.

    Returns:
        A list of strings representing the framed word.
    """
    # Combine the rows of all letters into a single word
    combined_rows = ["".join(row) for row in zip(*word)]

    # Pad each row to the specified width
    framed_rows = [row[:width].ljust(width, fill_char) for row in combined_rows]

    # Adjust the number of rows to the specified height
    while len(framed_rows) < height:
        framed_rows.append(fill_char * width)
    return framed_rows[:height]
