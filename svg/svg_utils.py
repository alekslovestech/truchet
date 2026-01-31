FILL_TRIANGLE = "#444"

def make_svg_line_points(pt1:tuple[float, float], pt2:tuple[float, float]) -> str:
    """Return an SVG line element from pt1 to pt2."""
    return f'<line x1="{pt1[0]}" y1="{pt1[1]}" x2="{pt2[0]}" y2="{pt2[1]}"/>'

def make_svg_triangle_points(
    pt1: tuple[float, float], pt2: tuple[float, float], pt3: tuple[float, float]
) -> str:
    """Return an SVG polygon element for a triangle with the three given vertices."""
    pts = f"{pt1[0]},{pt1[1]} {pt2[0]},{pt2[1]} {pt3[0]},{pt3[1]}"
    return f'<polygon points="{pts}" fill="{FILL_TRIANGLE}" stroke="none"/>'


