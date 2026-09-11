"""
test_error_correction.py - Tests for Reed-Solomon error correction.
"""

import pytest
from qr.bit_buffer import BitBuffer
from qr.error_correction import add_error_correction


def _make_buffer(data: str) -> BitBuffer:
    buf = BitBuffer()
    for byte in data.encode("utf-8"):
        buf.put(byte, 8)
    return buf


def test_ec_output_length():
    buf = _make_buffer("HELLO")
    result = add_error_correction(buf, version=1, error_level="M")
    # Should have data bytes + 10 EC bytes (version 1, M)
    assert len(result) == len(buf.get_bytes()) + 10


def test_ec_is_list_of_ints():
    buf = _make_buffer("TEST")
    result = add_error_correction(buf, version=1, error_level="L")
    assert all(isinstance(b, int) for b in result)
    assert all(0 <= b <= 255 for b in result)
