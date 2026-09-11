"""
masking.py - Data masking: applies all 8 mask patterns and picks the best.
"""

import copy

MASK_FUNCTIONS = [
    lambda r, c: (r + c) % 2 == 0,
    lambda r, c: r % 2 == 0,
    lambda r, c: c % 3 == 0,
    lambda r, c: (r + c) % 3 == 0,
    lambda r, c: (r // 2 + c // 3) % 2 == 0,
    lambda r, c: (r * c) % 2 + (r * c) % 3 == 0,
    lambda r, c: ((r * c) % 2 + (r * c) % 3) % 2 == 0,
    lambda r, c: ((r + c) % 2 + (r * c) % 3) % 2 == 0,
]


def _apply_mask(matrix: list[list[int]], pattern: int) -> list[list[int]]:
    fn = MASK_FUNCTIONS[pattern]
    result = copy.deepcopy(matrix)
    for r, row in enumerate(result):
        for c, val in enumerate(row):
            if val != -1:  # Only flip data modules
                result[r][c] = val ^ (1 if fn(r, c) else 0)
    return result


def _penalty_score(matrix: list[list[int]]) -> int:
    """Calculate the QR penalty score for a masked matrix."""
    score = 0
    size = len(matrix)

    # Rule 1: Five or more same-color in a row/column
    for row in matrix:
        score += _run_penalty(row)
    for c in range(size):
        col = [matrix[r][c] for r in range(size)]
        score += _run_penalty(col)

    # Rule 2: 2x2 blocks of the same color
    for r in range(size - 1):
        for c in range(size - 1):
            color = matrix[r][c]
            if color == matrix[r][c + 1] == matrix[r + 1][c] == matrix[r + 1][c + 1]:
                score += 3

    return score


def _run_penalty(line: list[int]) -> int:
    score, count, current = 0, 1, line[0]
    for val in line[1:]:
        if val == current:
            count += 1
        else:
            if count >= 5:
                score += 3 + (count - 5)
            count, current = 1, val
    if count >= 5:
        score += 3 + (count - 5)
    return score


def apply_best_mask(matrix: list[list[int]]) -> tuple[list[list[int]], int]:
    """
    Try all 8 mask patterns and return the one with the lowest penalty score.

    Returns:
        (masked_matrix, best_pattern_index)
    """
    best_matrix, best_score, best_pattern = None, float("inf"), 0
    for pattern in range(8):
        masked = _apply_mask(matrix, pattern)
        score = _penalty_score(masked)
        if score < best_score:
            best_score, best_matrix, best_pattern = score, masked, pattern
    return best_matrix, best_pattern
