"""
Render letter glyphs and combined ASCII art as SVG, and display in the browser.
"""
import tempfile
import webbrowser
from pathlib import Path

from letter_glyph import LetterGlyph
from tiles import Direction, TileChar, available_directions

# Fill and stroke colors for SVG elements
FILL_TRIANGLE = "#444"
STROKE_CONTOUR = "#111"
STROKE_GRID = "#ccc"
CELL_SIZE = 20


def _make_svg_line(x1: float, y1: float, x2: float, y2: float) -> str:
    """Return an SVG line element from (x1,y1) to (x2,y2)."""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'


def _make_svg_triangle(
    x1: float, y1: float, x2: float, y2: float, x3: float, y3: float
) -> str:
    """Return an SVG polygon element for a triangle with the three given vertices."""
    pts = f"{x1},{y1} {x2},{y2} {x3},{y3}"
    return f'<polygon points="{pts}" fill="{FILL_TRIANGLE}" stroke="none"/>'


def draw_cell_contours(ch: TileChar) -> str:
    """
    SVG for one cell: full diagonals and half-segments (center to corner).
    Half-segments run from cell center to the appropriate corner.
    Returns line elements only; stroke/fill are set by the caller.
    """

    cell_size = CELL_SIZE
    if ch == " ":
        return ""
    c = cell_size / 2

    def half(x: float, y: float) -> str:
        return _make_svg_line(c, c, x, y)

    diag_back = _make_svg_line(0, 0, cell_size, cell_size)
    diag_fwd = _make_svg_line(cell_size, 0, 0, cell_size)
    lower_left = half(0, cell_size)
    top_right = half(cell_size, 0)
    top_left = half(0, 0)
    bottom_right = half(cell_size, cell_size)
    match ch:
        case "X":
            return diag_back + diag_fwd
        case "λ":
            return diag_back + lower_left  
        case "ɣ":
            return diag_back + top_right  
        case "y":
            return diag_fwd + top_left
        case "ʎ":
            return diag_fwd + bottom_right 
        case _:
            return ""

# tiles can be filled either as an hourglass (⧗) or a bowtie (⧓). They alternate, but the initial tile determines the rest
def draw_cell_fills(ch: TileChar, isEven: bool, init_tile_bowtie: bool) -> str:
    """
    SVG for filled regions in one cell. 
    """
    if ch == " ":
        return ""
    cell_size = CELL_SIZE
    mid = cell_size / 2
    output = ""
    directions = available_directions(ch)
    if isEven == init_tile_bowtie:
        if Direction.LEFT in directions:
            # Left triangle: left edge to center to bottom edge
            output += _make_svg_triangle(0, 0, mid, mid, 0, cell_size)
        if Direction.RIGHT in directions:
            # Right triangle: right edge to center to top edge
            output += _make_svg_triangle(cell_size, 0, mid, mid, cell_size, cell_size)
    else:
        if Direction.TOP in directions:
            output += _make_svg_triangle(0, 0, mid, mid, cell_size, 0)
        if Direction.BOTTOM in directions:
            output += _make_svg_triangle(0, cell_size, mid, mid, cell_size, cell_size)
    return output


def lines_to_svg(lines: list[str], init_tile_bowtie: bool) -> str:
    """
    Convert a 2D grid of characters (list of rows) to an SVG string.
    Each character uses draw_cell_fills (top/bottom triangles) and draw_cell_contours (lines and half-segments).
    """
    if not lines:
        return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 0 0"></svg>'

    cell_size = CELL_SIZE
    cols = max(len(row) for row in lines)
    rows = len(lines)
    width = cols * cell_size
    height = rows * cell_size

    # Grid: vertical and horizontal lines (fainter than draw_cell strokes)
    grid_lines = []
    for i in range(cols + 1):
        x = i * cell_size
        grid_lines.append(_make_svg_line(x, 0, x, height))
    for j in range(rows + 1):
        y = j * cell_size
        grid_lines.append(_make_svg_line(0, y, width, y))
    grid = (
        f'<g stroke="{STROKE_GRID}" stroke-width="0.5" fill="none">'
        + "".join(grid_lines)
        + "</g>"
    )

    cells = []
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            x = c * cell_size
            y = r * cell_size
            isEven = (r + c) % 2 == 0
            tileChar: TileChar = ch  # type: ignore
            contour = draw_cell_contours(tileChar)
            fills = draw_cell_fills(tileChar, isEven, init_tile_bowtie)
            cells.append(
                f'<g transform="translate({x},{y})" stroke="{STROKE_CONTOUR}" fill="none" stroke-width="1">'
                + fills + contour
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
