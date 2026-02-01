from types import SimpleNamespace

CELL_SIZE = 20
CELL_FRACTION = 0.65 * CELL_SIZE

def cell_pts():
    return SimpleNamespace(
        top_left=(0, 0),
        top_right=(CELL_SIZE, 0),
        bottom_left=(0, CELL_SIZE),
        bottom_right=(CELL_SIZE, CELL_SIZE),
        center=(CELL_SIZE / 2, CELL_SIZE / 2),

        top_mid=(CELL_SIZE / 2, 0),
        bottom_mid=(CELL_SIZE / 2, CELL_SIZE),
        left_mid=(0, CELL_SIZE / 2),
        right_mid=(CELL_SIZE, CELL_SIZE / 2),
        
        top_mid_left=(CELL_FRACTION, 0),
        top_mid_right=(CELL_SIZE - CELL_FRACTION, 0),
        bottom_mid_left=(CELL_FRACTION, CELL_SIZE),
        bottom_mid_right=(CELL_SIZE - CELL_FRACTION, CELL_SIZE),
        left_mid_top=(0, CELL_FRACTION),
        left_mid_bottom=(0, CELL_SIZE - CELL_FRACTION),
        right_mid_top=(CELL_SIZE, CELL_FRACTION),
        right_mid_bottom=(CELL_SIZE, CELL_SIZE - CELL_FRACTION),
    )