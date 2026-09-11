"""
matrix.py - QR matrix construction: places all functional and data modules.
"""

from .patterns import place_finder_patterns, place_timing_patterns, place_alignment_patterns
from .version import matrix_size


def build_matrix(codewords: list[int], version: int) -> list[list[int]]:
    """
    Build the full QR matrix by placing all patterns and data modules.

    Args:
        codewords: Final list of data + EC codeword integers.
        version: QR version (1–40).

    Returns:
        2D list of ints: 1 = dark, 0 = light, -1 = reserved/unfilled.
    """
    size = matrix_size(version)
    matrix = [[-1] * size for _ in range(size)]

    place_finder_patterns(matrix, size)
    place_timing_patterns(matrix, size)
    place_alignment_patterns(matrix, version)
    _place_data(matrix, codewords, size)

    return matrix


def _place_data(matrix: list[list[int]], codewords: list[int], size: int):
    """Zigzag placement of data bits into the matrix."""
    bits: list[int] = []
    for cw in codewords:
        for i in range(7, -1, -1):
            bits.append((cw >> i) & 1)

    bit_index = 0
    right = size - 1
    going_up = True

    while right >= 1:
        if right == 6:  # Skip timing column
            right -= 1
        for row in (range(size - 1, -1, -1) if going_up else range(size)):
            for col_offset in (0, 1):
                col = right - col_offset
                if matrix[row][col] == -1:
                    matrix[row][col] = bits[bit_index] if bit_index < len(bits) else 0
                    bit_index += 1
        right -= 2
        going_up = not going_up
