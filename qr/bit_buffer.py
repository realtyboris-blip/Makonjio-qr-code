"""
bit_buffer.py - Bit-level buffer utility for building QR bit streams.
"""


class BitBuffer:
    """Accumulates bits into a list for QR encoding."""

    def __init__(self):
        self._buffer: list[int] = []

    def put(self, value: int, length: int):
        """Append `length` bits of `value` (MSB first)."""
        for i in range(length - 1, -1, -1):
            self._buffer.append((value >> i) & 1)

    def put_bit(self, bit: int):
        """Append a single bit (0 or 1)."""
        self._buffer.append(bit & 1)

    def __len__(self) -> int:
        return len(self._buffer)

    def __getitem__(self, index: int) -> int:
        return self._buffer[index]

    def get_bytes(self) -> list[int]:
        """Pack bits into a list of bytes (zero-padded to full byte)."""
        padded = self._buffer + [0] * (-len(self._buffer) % 8)
        return [
            int("".join(str(b) for b in padded[i:i + 8]), 2)
            for i in range(0, len(padded), 8)
        ]
