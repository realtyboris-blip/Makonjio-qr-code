"""
test_matrix.py - Tests for QR matrix construction.
"""

import pytest
from qr.matrix import build_matrix
from qr.version import matrix_size


def test_matrix_dimensions():
    version = 1
    codewords = [0] * 26  # Dummy codewords
    matrix = build_matrix(codewords, version)
    size = matrix_size(version)
    assert len(matrix) == size
    assert all(len(row) == size for row in matrix)


def test_matrix_values_are_0_or_1():
    codewords = [0xAB] * 26
    matrix = build_matrix(codewords, 1)
    for row in matrix:
        for val in row:
            assert val in (0, 1), f"Unexpected matrix value: {val}"


def test_finder_pattern_top_left():
    """Top-left of matrix should be the dark corner of the finder pattern."""
    matrix = build_matrix([0] * 26, 1)
    assert matrix[0][0] == 1
    assert matrix[6][0] == 1
    assert matrix[0][6] == 1
