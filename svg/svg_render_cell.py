from tiles import Direction, TileChar, Corners, available_directions, unavailable_corners
from tilestyle import TileStyle
from .svg_utils import make_svg_line_points
from .cell_constants import CELL_SIZE, cell_pts
from .svg_render_cell_parts import fill_quadrant, empty_quadrant, bowtie_triangle

STROKE_CONTOUR = "#111"
STROKE_GRID = "#ccc"

def _draw_cell_contours(ch: TileChar) -> str:
    """
    SVG for one cell: full diagonals and half-segments (center to corner).
    Half-segments run from cell center to the appropriate corner.
    Returns line elements only; stroke/fill are set by the caller.
    """
    if ch == " ":
        return ""
    cell = cell_pts()
    def center_to(pt: tuple[float, float]) -> str:
        return make_svg_line_points(cell.center, pt)
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
def _draw_bowtie_fills(ch: TileChar, isEven: bool, init_tile_flipped: bool) -> str:
    """
    SVG for filled regions in one cell. 
    """
    if ch == " ":
        return ""
    output = ""
    directions = available_directions(ch)

    cell=cell_pts()
    if isEven == init_tile_flipped:
        if Direction.LEFT in directions:
            output += bowtie_triangle(
                cell.top_left,
                cell.bottom_left
            )            
        if Direction.RIGHT in directions:
            output += bowtie_triangle(
                cell.top_right,
                cell.bottom_right
            )
    else:
        if Direction.TOP in directions:
            output += bowtie_triangle(
                cell.top_left,
                cell.top_right
            )
        if Direction.BOTTOM in directions:
            output += bowtie_triangle(
                cell.bottom_left,
                cell.bottom_right
            )
    return output

def _draw_corner_fills(ch: TileChar, isEven: bool, init_tile_flipped: bool, style: TileStyle) -> str:
    """
    SVG for filled circular arcs in one cell. 
    """
    if ch == " ":
        return ""
    output = ""

    cell = cell_pts()
    if isEven == init_tile_flipped:        
        output += fill_quadrant(cell.top_left, cell.top_mid_left, cell.left_mid_top, style)
        output += fill_quadrant(cell.bottom_right, cell.bottom_mid_right, cell.right_mid_bottom, style)
    else:
        output += fill_quadrant(cell.top_right, cell.top_mid_right, cell.right_mid_top, style)
        output += fill_quadrant(cell.bottom_left, cell.bottom_mid_left, cell.left_mid_bottom, style)
    
    return output

def _draw_direction_exclusions(ch: TileChar, style: TileStyle) -> str:
    """
    SVG excluded corners based on the tile character.
    """
    if ch == " " or ch == "X":
        return ""
        
    corners = unavailable_corners(ch)
    cell = cell_pts()
    
    output = ""    
    if Corners.TOP_LEFT in corners:
        output += empty_quadrant(cell.top_left, cell.top_right, cell.bottom_left)
    if Corners.BOTTOM_RIGHT in corners:
        output += empty_quadrant(cell.bottom_right, cell.bottom_left, cell.top_right)
    if Corners.TOP_RIGHT in corners:
        output += empty_quadrant(cell.top_right, cell.bottom_right, cell.top_left)
    if Corners.BOTTOM_LEFT in corners:
        output += empty_quadrant(cell.bottom_left, cell.top_left, cell.bottom_right)    

    return output    

def draw_cell(ch: TileChar, isEven: bool, init_tile_flipped: bool, style: TileStyle) -> str:
    """
    SVG for one cell. 
    """
    if ch == " ":
        return ""
    output = ""
    if style == TileStyle.BOWTIE:
        output += _draw_cell_contours(ch)
        output += _draw_bowtie_fills(ch, isEven, init_tile_flipped)
    elif style == TileStyle.CIRCLE or style == TileStyle.TRIANGLE:
        output += _draw_corner_fills(ch, isEven, init_tile_flipped, style)
        output += _draw_direction_exclusions(ch, style)
    return output