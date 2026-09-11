"""
version.py - QR version selection based on data length and error level.
"""

# Data capacity table: capacity[version][error_level] = max bytes
# (Byte mode capacities, versions 1–10 as a starting point)
CAPACITY = {
    1:  {"L": 17,  "M": 14,  "Q": 11,  "H": 7},
    2:  {"L": 32,  "M": 26,  "Q": 20,  "H": 14},
    3:  {"L": 53,  "M": 42,  "Q": 32,  "H": 24},
    4:  {"L": 78,  "M": 62,  "Q": 46,  "H": 34},
    5:  {"L": 106, "M": 84,  "Q": 60,  "H": 44},
    6:  {"L": 134, "M": 106, "Q": 74,  "H": 58},
    7:  {"L": 154, "M": 122, "Q": 86,  "H": 64},
    8:  {"L": 192, "M": 152, "Q": 108, "H": 84},
    9:  {"L": 230, "M": 180, "Q": 130, "H": 98},
    10: {"L": 271, "M": 213, "Q": 151, "H": 119},
}


def select_version(data: str, error_level: str) -> int:
    """
    Return the smallest QR version that can hold `data` at `error_level`.

    Args:
        data: The string to encode.
        error_level: 'L', 'M', 'Q', or 'H'.

    Returns:
        Version integer (1–40).

    Raises:
        ValueError: If the data exceeds the capacity of version 10 (extend table as needed).
    """
    length = len(data.encode("utf-8"))
    for version, caps in CAPACITY.items():
        if length <= caps[error_level]:
            return version
    raise ValueError(
        f"Data length {length} bytes exceeds supported version capacity. "
        "Extend the CAPACITY table for versions > 10."
    )


def matrix_size(version: int) -> int:
    """Return the side length (in modules) of a QR code for a given version."""
    return 17 + 4 * version
