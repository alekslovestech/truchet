"""
Text formatter module for rendering text as ASCII art letters.
"""
from pathlib import Path
from typing import TypeAlias

from tiles import inverse

# Letter representation: exactly 5 rows, each row is a string of characters
Letter: TypeAlias = list[str]  # Always 5 elements

# Inverted/framed letter: 7×5 (rows × cols) with X frame
UNFRAMED_ROWS = 5
FRAMED_ROWS = 7
FRAMED_COLS = 5


def load_letter(letter: str) -> Letter:
    """
    Load a letter from the data folder.
    
    Args:
        letter: The letter to load (lowercase)
        
    Returns:
        List of exactly 5 lines representing the letter, or empty list if not found
    """
    data_dir = Path(__file__).parent / "data"
    letter_file = data_dir / f"{letter}.txt"
    
    if not letter_file.exists():
        return []
    
    with open(letter_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Strip trailing newlines and empty lines
    lines = [line.rstrip('\n\r') for line in lines]
    while lines and not lines[-1]:
        lines.pop()
    
    return lines



def combine_letters(letters: list[Letter], spacing: int = 1, rows: int = 5) -> list[str]:
    """
    Combine multiple letters horizontally.
    Assumes all letters have exactly `rows` lines.

    Args:
        letters: List of letter representations (each is a list of lines)
        spacing: Number of spaces between letters
        rows: Number of rows per letter (default UNFRAMED_ROWS; use FRAMED_ROWS for framed)

    Returns:
        Combined lines
    """
    if not letters:
        return []

    max_widths = [3] * rows
    for letter in letters:
        if letter:
            for row in range(min(rows, len(letter))):
                max_widths[row] = max(max_widths[row], len(letter[row]), 3)

    padded_letters = []
    for letter in letters:
        if letter:
            padded = []
            for row in range(rows):
                if row < len(letter):
                    padded.append(letter[row].ljust(max_widths[row]))
                else:
                    padded.append(" " * max_widths[row])
            padded_letters.append(padded)
        else:
            padded_letters.append([""] * rows)

    result = []
    for row in range(rows):
        line_parts = [padded_letter[row] for padded_letter in padded_letters]
        result.append((" " * spacing).join(line_parts))

    return result


def combine_letters_vertical(letters: list[Letter]) -> list[str]:
    """
    Combine multiple letters vertically, appending one after the other.
    
    Args:
        letters: List of letter representations (each is a list of lines)
        
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


def create_inverted_letter(letter: Letter) -> Letter:
    """
    Create an inverted version of a letter using tile inverse.
    Returns 7×5 (FRAMED_ROWS × FRAMED_COLS): 1 X row top, 5 content, 1 X row bottom.
    Empty letter → full X block.
    """
    if not letter:
        return ["X" * FRAMED_COLS] * FRAMED_ROWS

    frame = "X" * FRAMED_COLS
    content_width = FRAMED_COLS - 2  # 1 left + 1 right X
    content = []
    for row in letter:
        inverted_row = "".join(inverse(char) for char in row)
        inverted_row = inverted_row[:content_width].ljust(content_width, "X")
        content.append("X" + inverted_row + "X")

    content_height = UNFRAMED_ROWS
    while len(content) < content_height:
        content.append("X" + "X" * content_width + "X")
    content = content[:content_height]

    return [frame] + content + [frame]


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
    letters: list[Letter] = []
    
    for char in text:
        if char == " ":
            # Add a space (empty letter) - full 7×5 X block
            letters.append(create_inverted_letter([]))
        elif char.isalpha():
            # Load the letter and convert to empty space version
            letter_lines = load_letter(char)
            if letter_lines:
                inverted_letter = create_inverted_letter(letter_lines)
                letters.append(inverted_letter)
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
    letters: list[Letter] = []
    
    for char in text:
        if char == ' ':
            # Add a space (empty letter)
            letters.append([])
        elif char.isalpha():
            # Load the letter
            letter_lines = load_letter(char)
            letters.append(letter_lines)
        # Skip non-alphabetic characters
    
    # Combine all letters
    if not letters:
        return ""
    
    result_lines = combine_letters(letters, spacing=1)
    return '\n'.join(result_lines)

