"""
error_correction.py - Reed-Solomon error correction codeword generation.
"""

from .bit_buffer import BitBuffer

# GF(256) arithmetic using primitive polynomial x^8 + x^4 + x^3 + x^2 + 1
GF_EXP = [0] * 512
GF_LOG = [0] * 256

_x = 1
for _i in range(255):
    GF_EXP[_i] = _x
    GF_LOG[_x] = _i
    _x <<= 1
    if _x & 0x100:
        _x ^= 0x11D
for _i in range(255, 512):
    GF_EXP[_i] = GF_EXP[_i - 255]


def _gf_mul(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return GF_EXP[GF_LOG[a] + GF_LOG[b]]


def _rs_generator(degree: int) -> list[int]:
    """Build the Reed-Solomon generator polynomial of given degree."""
    poly = [1]
    for i in range(degree):
        poly = _poly_mul(poly, [1, GF_EXP[i]])
    return poly


def _poly_mul(p: list[int], q: list[int]) -> list[int]:
    result = [0] * (len(p) + len(q) - 1)
    for i, pi in enumerate(p):
        for j, qj in enumerate(q):
            result[i + j] ^= _gf_mul(pi, qj)
    return result


def _rs_remainder(data: list[int], generator: list[int]) -> list[int]:
    remainder = data[:]
    for _ in range(len(generator) - 1):
        remainder.append(0)
    for i in range(len(data)):
        coef = remainder[i]
        if coef != 0:
            for j, g in enumerate(generator):
                remainder[i + j] ^= _gf_mul(g, coef)
    return remainder[len(data):]


def add_error_correction(bit_stream: BitBuffer, version: int, error_level: str) -> list[int]:
    """
    Attach Reed-Solomon error correction codewords to the data codewords.

    Args:
        bit_stream: Encoded data bits.
        version: QR version.
        error_level: 'L', 'M', 'Q', or 'H'.

    Returns:
        Final list of codeword integers (data + EC).
    """
    data_bytes = bit_stream.get_bytes()
    ec_count = _ec_codewords_per_block(version, error_level)
    generator = _rs_generator(ec_count)
    ec_bytes = _rs_remainder(data_bytes, generator)
    return data_bytes + ec_bytes


def _ec_codewords_per_block(version: int, error_level: str) -> int:
    """Lookup table stub — expand with full QR spec values as needed."""
    table = {
        ("L", 1): 7,  ("M", 1): 10, ("Q", 1): 13, ("H", 1): 17,
        ("L", 2): 10, ("M", 2): 16, ("Q", 2): 22, ("H", 2): 28,
    }
    return table.get((error_level, version), 10)
