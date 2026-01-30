from types import SimpleNamespace
from tiles import Direction, TileChar, available_directions
from svg_utils import make_svg_line_points, make_svg_triangle_points

# Fill and stroke colors for SVG elements

STROKE_CONTOUR = "#111"
STROKE_GRID = "#ccc"
CELL_SIZE = 20

def cell_pts():
    return SimpleNamespace(
        top_left=(0, 0),
        top_right=(CELL_SIZE, 0),
        bottom_left=(0, CELL_SIZE),
        bottom_right=(CELL_SIZE, CELL_SIZE),
        center=(CELL_SIZE / 2, CELL_SIZE / 2)
    )

def draw_cell_contours(ch: TileChar) -> str:
    """
    SVG for one cell: full diagonals and half-segments (center to corner).
    Half-segments run from cell center to the appropriate corner.
    Returns line elements only; stroke/fill are set by the caller.
    """

    if ch == " ":
        return ""
    
    cell=cell_pts()
    
    def center_to(pt: tuple[float, float]) -> str:
        return make_svg_line_points( cell.center, pt )
    
    diag_back = make_svg_line_points(cell.top_left, cell.bottom_right)
    diag_fwd = make_svg_line_points(cell.bottom_left, cell.top_right) 
    match ch:
        case "X":
            return diag_back + diag_fwd
        case "λ":
            return diag_back + center_to(cell.bottom_left) 
        case "ɣ":
            return diag_back + center_to(cell.top_right)        
        case "y":
            return diag_fwd + center_to(cell.top_left)
        case "ʎ":
            return diag_fwd + center_to(cell.bottom_right)
        case _:
            return ""

# tiles can be filled either as an hourglass (⧗) or a bowtie (⧓). They alternate, but the initial tile determines the rest
def draw_cell_fills(ch: TileChar, isEven: bool, init_tile_bowtie: bool) -> str:
    """
    SVG for filled regions in one cell. 
    """
    if ch == " ":
        return ""
    output = ""
    directions = available_directions(ch)

    cell=cell_pts()
    if isEven == init_tile_bowtie:
        if Direction.LEFT in directions:
            # Left triangle: left edge to center to bottom edge
            output += make_svg_triangle_points(
                cell.top_left,
                cell.center,
                cell.bottom_left
            )            
        if Direction.RIGHT in directions:
            # Right triangle: right edge to center to top edge
            output += make_svg_triangle_points(
                cell.top_right,
                cell.center,
                cell.bottom_right
            )
    else:
        if Direction.TOP in directions:
            output += make_svg_triangle_points(
                cell.top_left,
                cell.center,
                cell.top_right
            )
        if Direction.BOTTOM in directions:
            output += make_svg_triangle_points(
                cell.bottom_left,
                cell.center,
                cell.bottom_right
            )
    return output
