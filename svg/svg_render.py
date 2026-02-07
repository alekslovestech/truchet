"""
Render letter glyphs and combined ASCII art as SVG, and display in the browser.
"""
import tempfile
import webbrowser
from pathlib import Path

from letter_glyph import LetterGlyph
from tilestyle import TileStyle
from .svg_render_cell import CELL_SIZE, STROKE_CONTOUR, STROKE_GRID, TileChar, draw_cell
from .svg_utils import make_svg_line_points


def _make_svg_grid_lines(cols: int, rows: int, cell_size: int) -> str:
    """
    Generate SVG for grid lines given number of columns, rows, and cell size.
    """
    width = cols * cell_size
    height = rows * cell_size
    grid_lines = []
    for i in range(cols + 1):
        x = i * cell_size
        grid_lines.append(make_svg_line_points((x, 0), (x, height)))
    for j in range(rows + 1):
        y = j * cell_size
        grid_lines.append(make_svg_line_points((0, y), (width, y)))
    grid = (
        f'<g stroke="{STROKE_GRID}" stroke-width="0.5" fill="none">'
        + "".join(grid_lines)
        + "</g>"
    )
    return grid


def lines_to_svg(lines: list[str], init_tile_flipped: bool, style: TileStyle = TileStyle.BOWTIE) -> str:
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

    grid = _make_svg_grid_lines(cols, rows, cell_size)

    cells = []    
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            x = c * cell_size
            y = r * cell_size
            isEven = (r + c) % 2 == 0
            tileChar: TileChar = ch  # type: ignore
            cell = draw_cell(tileChar, isEven, init_tile_flipped, style)
            output = (
                f'<g transform="translate({x},{y})" stroke="{STROKE_CONTOUR}" fill="none" stroke-width="1">'
                + cell
                + "</g>"
            )
            cells.append(output)

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">'
        + grid
        + "".join(cells)
        + "</svg>"
    )



def display_svg(svg: str) -> None:
    """Write the SVG to a temp file and open it in the default browser."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".svg", delete=False, encoding="utf-8"
    ) as f:
        f.write(svg)

    webbrowser.open(Path(f.name).as_uri())
