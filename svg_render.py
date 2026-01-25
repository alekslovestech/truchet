"""
Render letter glyphs and combined ASCII art as SVG, and display in the browser.
"""
import tempfile
import webbrowser
from pathlib import Path

from letter_glyph import LetterGlyph


def draw_cell(ch: str, size: int) -> str:
    """
    SVG for one cell: full diagonals and half-segments (center to corner).
    Half-segments run from cell center to the appropriate corner.
    Returns line elements only; stroke/fill are set by the caller.
    """
    if ch == " " or size <= 0:
        return ""
    c = size / 2

    def half(x: float, y: float) -> str:
        return f'<line x1="{c}" y1="{c}" x2="{x}" y2="{y}"/>'

    diag_back = f'<line x1="0" y1="0" x2="{size}" y2="{size}"/>'
    diag_fwd = f'<line x1="{size}" y1="0" x2="0" y2="{size}"/>'

    if ch == "X":
        return diag_back + diag_fwd
    if ch == "λ":
        return diag_back + half(0, size)  # \ + lower-left
    if ch == "ɣ":
        return diag_back + half(size, 0)  # / + top-right
    if ch == "y":
        return diag_fwd + half(0, 0)  # \ + top-left
    if ch == "ʎ":
        return diag_fwd + half(size, size)  # / + bottom-right
    return ""


def lines_to_svg(lines: list[str], cell_size: int = 20) -> str:
    """
    Convert a 2D grid of characters (list of rows) to an SVG string.
    Each character is drawn via draw_cell (lines and half-segments).
    """
    if not lines:
        return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 0 0"></svg>'

    cols = max(len(row) for row in lines)
    rows = len(lines)
    width = cols * cell_size
    height = rows * cell_size

    # Grid: vertical and horizontal lines (fainter than draw_cell strokes)
    grid_lines = []
    for i in range(cols + 1):
        x = i * cell_size
        grid_lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{height}"/>')
    for j in range(rows + 1):
        y = j * cell_size
        grid_lines.append(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}"/>')
    grid = (
        '<g stroke="#ccc" stroke-width="0.5" fill="none">'
        + "".join(grid_lines)
        + "</g>"
    )

    cells = []
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            x = c * cell_size
            y = r * cell_size
            inner = draw_cell(ch, cell_size)
            if inner:
                cells.append(
                    f'<g transform="translate({x},{y})" stroke="#111" fill="none" stroke-width="1">'
                    + inner
                    + "</g>"
                )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">'
        + grid
        + "".join(cells)
        + "</svg>"
    )


def letter_glyph_to_svg(glyph: LetterGlyph, cell_size: int = 20) -> str:
    """Convert a single LetterGlyph to SVG."""
    return lines_to_svg(glyph.lines, cell_size)


def display_svg(svg: str) -> None:
    """Write the SVG to a temp file and open it in the default browser."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".svg", delete=False, encoding="utf-8"
    ) as f:
        f.write(svg)

    webbrowser.open(Path(f.name).as_uri())
