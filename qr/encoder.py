"""
encoder.py - High-level orchestration of the QR encoding pipeline.

For a guaranteed-scannable QR code, the pipeline uses the `qrcode` library
to produce the correct matrix, then passes it through our custom renderer
so all the custom styling (colors, logos, etc.) still applies.
"""

import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H

from .renderer import render

_EC_MAP = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H,
}


def encode(
    data: str,
    error_level: str = "M",
    output_path: str = "output/qr.png",
    module_size: int = 10,
    quiet_zone: int = 4,
    dark_color: tuple = (0, 0, 0),
    light_color: tuple = (255, 255, 255),
    logo_path: str | None = None,
    logo_ratio: float = 0.25,
):
    """
    Encode `data` as a QR code and save it to `output_path`.

    Args:
        data:        The string to encode.
        error_level: Error correction level — 'L', 'M', 'Q', or 'H'.
        output_path: Destination image file (.png).
        module_size: Pixels per QR module.
        quiet_zone:  Quiet zone width in modules.
        dark_color:  RGB tuple for dark modules.
        light_color: RGB tuple for light modules.
        logo_path:   Optional path to a logo to overlay at the centre.
        logo_ratio:  Logo size as a fraction of the QR image (≤ 0.3 recommended).
    """
    ec = _EC_MAP.get(error_level.upper(), ERROR_CORRECT_M)

    qr = qrcode.QRCode(
        error_correction=ec,
        box_size=1,   # We handle sizing in renderer
        border=0,     # We handle quiet zone in renderer
    )
    # Use qrcode.image.base.BaseImage data type to force plain byte encoding,
    # preventing any scanner from interpreting the content as a URL.
    qr.add_data(qrcode.util.QRData(data.encode("utf-8"), mode=qrcode.util.MODE_8BIT_BYTE))
    qr.make(fit=True)

    # Extract the boolean matrix from the qrcode object
    modules = qr.modules  # list[list[bool]]
    matrix = [[1 if cell else 0 for cell in row] for row in modules]

    render(
        matrix,
        output_path=output_path,
        module_size=module_size,
        quiet_zone=quiet_zone,
        dark_color=dark_color,
        light_color=light_color,
        logo_path=logo_path,
        logo_ratio=logo_ratio,
    )
