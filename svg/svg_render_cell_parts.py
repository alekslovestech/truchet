from tilestyle import TileStyle
from .svg_utils import make_svg_triangle_points, FILL_TRIANGLE
from .cell_constants import CELL_FRACTION, cell_pts

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

def fill_quadrant(corner: tuple[float, float],
    pt1: tuple[float, float],
    pt2: tuple[float, float], style: TileStyle) -> str:
    """
    SVG for a filled quadrant.
    """
    if style == TileStyle.BOWTIE:
        raise ValueError("Invalid style: BOWTIE is not supported for fill_quadrant")
    elif style == TileStyle.CIRCLE:
        return _fill_circle_quadrant(corner, pt1, pt2)
    elif style == TileStyle.TRIANGLE:
        return make_svg_triangle_points(corner, pt1, pt2)

def empty_quadrant(corner: tuple[float, float], pt1: tuple[float, float], pt2: tuple[float, float]) -> str:
    """
    SVG for an empty quadrant.
    """
    return make_svg_triangle_points(corner, pt1, pt2, filled=False)

def bowtie_triangle(corner_a: tuple[float, float], corner_b: tuple[float, float]) -> str:
    """Triangle from center to two corners (bowtie style)."""
    cell=cell_pts()
    return make_svg_triangle_points(cell.center, corner_a, corner_b, filled=True)