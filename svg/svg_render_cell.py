from tiles import Direction, TileChar, Corners, available_directions, available_corners
from tilestyle import TileStyle
from .svg_utils import make_svg_line_points, make_svg_triangle_points, FILL_TRIANGLE
from .cell_constants import CELL_SIZE, CELL_FRACTION, cell_pts

# Fill and stroke colors for SVG elements

STROKE_CONTOUR = "#111"
STROKE_GRID = "#ccc"

def _fill_circle_quadrant(
    corner: tuple[float, float],
    pt1: tuple[float, float],
    pt2: tuple[float, float],
) -> str:
    """
    SVG path for a circular quadrant: arc from pt1 to pt2.
    Sweep direction is derived from corner (main diagonal = clockwise).
    """
    radius = CELL_FRACTION
    sweep = 1 if corner[0] == corner[1] else 0
    return (
        f'<path d="M {corner[0]} {corner[1]} '
        f'L {pt1[0]} {pt1[1]} '
        f'A {radius} {radius} 0 0 {sweep} {pt2[0]} {pt2[1]} Z" '
        f'fill="{FILL_TRIANGLE}" stroke="none"/>'
    )

def _draw_cell_contours(ch: TileChar) -> str:
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
def _draw_cell_fills(ch: TileChar, isEven: bool, init_tile_bowtie: bool) -> str:
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
            output += make_svg_triangle_points(
                cell.top_left,
                cell.center,
                cell.bottom_left
            )            
        if Direction.RIGHT in directions:
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



def _draw_circular_fills(ch: TileChar, isEven: bool, init_tile_bowtie: bool) -> str:
    """
    SVG for filled circular arcs in one cell. 
    """
    if ch == " ":
        return ""
    output = ""
    corners = available_corners(ch)

    cell = cell_pts()
    radius = CELL_SIZE / 2
    if isEven == init_tile_bowtie:
        if Corners.TOP_LEFT in corners:
            output += _fill_circle_quadrant(cell.top_left, cell.top_mid_left, cell.left_mid_top)
        if Corners.BOTTOM_RIGHT in corners:
            output += _fill_circle_quadrant(cell.bottom_right, cell.bottom_mid_right, cell.right_mid_bottom)
    else:
        if Corners.TOP_RIGHT in corners:
            output += _fill_circle_quadrant(cell.top_right, cell.top_mid_right, cell.right_mid_top)
        if Corners.BOTTOM_LEFT in corners:
            output += _fill_circle_quadrant(cell.bottom_left, cell.bottom_mid_left, cell.left_mid_bottom)
    return output

def _draw_triangle_fills(ch: TileChar, isEven: bool, init_tile_bowtie: bool) -> str:
    """
    SVG for filled triangles in one cell. 
    """
    if ch == " ":
        return ""
    output = ""
    corners = available_corners(ch)
    cell = cell_pts()
    radius = CELL_SIZE / 2
    if isEven == init_tile_bowtie:
        if Corners.TOP_LEFT in corners:
            output += make_svg_triangle_points(cell.top_left, cell.top_mid_left, cell.left_mid_top)
        if Corners.BOTTOM_RIGHT in corners:
            output += make_svg_triangle_points(cell.bottom_right, cell.bottom_mid_right, cell.right_mid_bottom)
    else:
        if Corners.TOP_RIGHT in corners:
            output += make_svg_triangle_points(cell.top_right, cell.top_mid_right, cell.right_mid_top)
        if Corners.BOTTOM_LEFT in corners:
            output += make_svg_triangle_points(cell.bottom_left, cell.bottom_mid_left, cell.left_mid_bottom)
    return output

def draw_cell(ch: TileChar, isEven: bool, init_tile_bowtie: bool, style: TileStyle) -> str:
    """
    SVG for one cell. 
    """
    if ch == " ":
        return ""
    output = ""
    if style == TileStyle.BOWTIE:
        output += _draw_cell_contours(ch)
        output += _draw_cell_fills(ch, isEven, init_tile_bowtie)
    elif style == TileStyle.CIRCLE:
        output += _draw_circular_fills(ch, isEven, init_tile_bowtie)
    elif style == TileStyle.TRIANGLE:
        output += _draw_triangle_fills(ch, isEven, init_tile_bowtie)
    return output