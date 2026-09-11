"""
format_info.py - Embed format and version information into the QR matrix.
"""

# Error correction level indicators
EC_LEVEL_BITS = {"L": 0b01, "M": 0b00, "Q": 0b11, "H": 0b10}

# Format info generator polynomial: 10100110111
FORMAT_GEN = 0b10100110111

FORMAT_MASK = 0b101010000010010


def _format_bits(error_level: str, mask_pattern: int) -> int:
    """Compute the 15-bit format information word."""
    data = (EC_LEVEL_BITS[error_level] << 3) | mask_pattern
    remainder = data << 10
    for _ in range(10):
        if remainder & (1 << (remainder.bit_length() - 1)):
            remainder ^= FORMAT_GEN << (remainder.bit_length() - FORMAT_GEN.bit_length())
    return ((data << 10) | remainder) ^ FORMAT_MASK


def embed_format_info(
    matrix: list[list[int]], error_level: str, mask_pattern: int
) -> list[list[int]]:
    """
    Write the 15-bit format string into its two reserved locations.

    Args:
        matrix: QR matrix with data already placed.
        error_level: 'L', 'M', 'Q', or 'H'.
        mask_pattern: Chosen mask pattern index (0–7).

    Returns:
        Updated matrix with format info embedded.
    """
    bits = _format_bits(error_level, mask_pattern)
    size = len(matrix)

    # Format bit positions around the top-left finder pattern
    positions_h = [(8, i) for i in range(6)] + [(8, 7), (8, 8), (7, 8)] + [(i, 8) for i in range(5, -1, -1)]
    positions_v = [(size - 1 - i, 8) for i in range(7)] + [(8, size - 8 + i) for i in range(8)]

    for i, (r, c) in enumerate(positions_h):
        matrix[r][c] = (bits >> (14 - i)) & 1

    for i, (r, c) in enumerate(positions_v):
        matrix[r][c] = (bits >> (14 - i)) & 1

    # Dark module (always set)
    matrix[size - 8][8] = 1

    return matrix
