"""
Text formatter module for rendering text as ASCII art letters.
"""
from pathlib import Path
from typing import TypeAlias

# Letter representation: exactly 5 rows, each row is a string of characters
Letter: TypeAlias = list[str]  # Always 5 elements


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



def combine_letters(letters: list[Letter], spacing: int = 1) -> list[str]:
    """
    Combine multiple letters horizontally.
    Assumes all letters have exactly 5 rows.
    Each row is padded to a minimum width of 3 characters.
    
    Args:
        letters: List of letter representations (each is a list of 5 lines)
        spacing: Number of spaces between letters
        
    Returns:
        Combined lines
    """
    if not letters:
        return []
    
    # Find the maximum width for each row across all letters, with minimum of 3
    max_widths = [3] * 5  # Start with minimum width of 3
    for letter in letters:
        if letter:
            for row in range(min(5, len(letter))):
                max_widths[row] = max(max_widths[row], len(letter[row]), 3)
    
    # Pad all letters to the same width per row
    padded_letters = []
    for letter in letters:
        if letter:
            padded = []
            for row in range(5):
                if row < len(letter):
                    # Pad this row to the max width for this row (minimum 3)
                    padded.append(letter[row].ljust(max_widths[row]))
                else:
                    padded.append(' ' * max_widths[row])
            padded_letters.append(padded)
        else:
            # Space - use empty strings for all rows
            padded_letters.append([''] * 5)
    
    # Combine horizontally
    result = []
    for row in range(5):
        line_parts = []
        for padded_letter in padded_letters:
            line_parts.append(padded_letter[row])
        result.append((' ' * spacing).join(line_parts))
    
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

