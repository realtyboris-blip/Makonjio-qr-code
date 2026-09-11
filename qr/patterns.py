"""
patterns.py - Finder, alignment, and timing pattern placement.
"""

# Alignment pattern center coordinates per version (version index = version - 1)
ALIGNMENT_POSITIONS = [
    [], [], [6, 18], [6, 22], [6, 26], [6, 30], [6, 34],
    [6, 22, 38], [6, 24, 42], [6, 26, 46], [6, 28, 50],
]


def _place_finder(matrix: list[list[int]], row: int, col: int):
    """Place a 7x7 finder pattern with its separator at (row, col) top-left."""
    for r in range(7):
        for c in range(7):
            dark = (
                r in (0, 6) or c in (0, 6) or (2 <= r <= 4 and 2 <= c <= 4)
            )
            matrix[row + r][col + c] = 1 if dark else 0

    # Separator (light border around finder)
    for i in range(8):
        if row + 7 < len(matrix) and col + i < len(matrix[0]):
            matrix[row + 7][col + i] = 0
        if col + 7 < len(matrix[0]) and row + i < len(matrix):
            matrix[row + i][col + 7] = 0


def place_finder_patterns(matrix: list[list[int]], size: int):
    _place_finder(matrix, 0, 0)           # Top-left
    _place_finder(matrix, 0, size - 7)    # Top-right
    _place_finder(matrix, size - 7, 0)    # Bottom-left


def place_timing_patterns(matrix: list[list[int]], size: int):
    for i in range(8, size - 8):
        matrix[6][i] = 1 if i % 2 == 0 else 0
        matrix[i][6] = 1 if i % 2 == 0 else 0


def place_alignment_patterns(matrix: list[list[int]], version: int):
    if version < 2:
        return
    positions = ALIGNMENT_POSITIONS[version - 1] if version - 1 < len(ALIGNMENT_POSITIONS) else []
    for row in positions:
        for col in positions:
            # Skip if overlapping a finder pattern area
            if matrix[row][col] != -1:
                continue
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    dark = abs(dr) == 2 or abs(dc) == 2 or (dr == 0 and dc == 0)
                    matrix[row + dr][col + dc] = 1 if dark else 0
