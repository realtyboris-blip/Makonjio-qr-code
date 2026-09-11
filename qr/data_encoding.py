"""
data_encoding.py - Data mode encoding: numeric, alphanumeric, and byte modes.
"""

from .bit_buffer import BitBuffer

# Mode indicators
MODE_NUMERIC = 0b0001
MODE_ALPHANUMERIC = 0b0010
MODE_BYTE = 0b0100

ALPHANUMERIC_CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"


def _detect_mode(data: str) -> int:
    if data.isdigit():
        return MODE_NUMERIC
    if all(c in ALPHANUMERIC_CHARSET for c in data):
        return MODE_ALPHANUMERIC
    return MODE_BYTE


def encode_data(data: str, version: int, error_level: str) -> BitBuffer:
    """
    Encode `data` into a BitBuffer using the most compact applicable mode.

    Args:
        data: Input string.
        version: QR version (1–40).
        error_level: Error correction level ('L', 'M', 'Q', 'H').

    Returns:
        BitBuffer containing the encoded bit stream.
    """
    mode = _detect_mode(data)
    buf = BitBuffer()

    # Mode indicator (4 bits)
    buf.put(mode, 4)

    # Character count indicator length varies by version and mode
    cc_bits = _char_count_bits(mode, version)
    buf.put(len(data), cc_bits)

    if mode == MODE_NUMERIC:
        _encode_numeric(data, buf)
    elif mode == MODE_ALPHANUMERIC:
        _encode_alphanumeric(data, buf)
    else:
        _encode_byte(data, buf)

    return buf


def _char_count_bits(mode: int, version: int) -> int:
    if mode == MODE_NUMERIC:
        return [10, 12, 14][[1, 10, 27].index(next(v for v in [1, 10, 27] if version <= v))]  # noqa
    if mode == MODE_ALPHANUMERIC:
        sizes = {range(1, 10): 9, range(10, 27): 11, range(27, 41): 13}
        for r, bits in sizes.items():
            if version in r:
                return bits
    # Byte mode
    sizes = {range(1, 10): 8, range(10, 41): 16}
    for r, bits in sizes.items():
        if version in r:
            return bits
    return 8


def _encode_numeric(data: str, buf: BitBuffer):
    for i in range(0, len(data), 3):
        chunk = data[i:i + 3]
        if len(chunk) == 3:
            buf.put(int(chunk), 10)
        elif len(chunk) == 2:
            buf.put(int(chunk), 7)
        else:
            buf.put(int(chunk), 4)


def _encode_alphanumeric(data: str, buf: BitBuffer):
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            val = ALPHANUMERIC_CHARSET.index(data[i]) * 45 + ALPHANUMERIC_CHARSET.index(data[i + 1])
            buf.put(val, 11)
        else:
            buf.put(ALPHANUMERIC_CHARSET.index(data[i]), 6)


def _encode_byte(data: str, buf: BitBuffer):
    for byte in data.encode("utf-8"):
        buf.put(byte, 8)
