"""
renderer.py - Render a QR matrix to a PNG image using Pillow.
Supports custom colors and optional logo overlay.
"""

from pathlib import Path

try:
    from PIL import Image, ImageDraw
    _PIL_AVAILABLE = True
except ImportError:
    _PIL_AVAILABLE = False


def render(
    matrix: list[list[int]],
    output_path: str = "output/qr.png",
    module_size: int = 10,
    quiet_zone: int = 4,
    dark_color: tuple = (0, 0, 0),
    light_color: tuple = (255, 255, 255),
    logo_path: str | None = None,
    logo_ratio: float = 0.25,
):
    """
    Render the QR matrix to a PNG file.

    Args:
        matrix: 2D list of module values (1 = dark, 0 = light).
        output_path: Destination file path.
        module_size: Pixels per module.
        quiet_zone: Quiet zone width in modules.
        dark_color: RGB tuple for dark modules.
        light_color: RGB tuple for light modules.
        logo_path: Optional path to a logo image to overlay in the center.
        logo_ratio: Logo size as a fraction of the QR code size (0.0–0.3 recommended).
    """
    if not _PIL_AVAILABLE:
        raise ImportError("Pillow is required for rendering. Run: pip install pillow")

    size = len(matrix)
    canvas = size + 2 * quiet_zone
    img_size = canvas * module_size

    img = Image.new("RGB", (img_size, img_size), light_color)
    draw = ImageDraw.Draw(img)

    for r, row in enumerate(matrix):
        for c, val in enumerate(row):
            color = dark_color if val == 1 else light_color
            x0 = (c + quiet_zone) * module_size
            y0 = (r + quiet_zone) * module_size
            draw.rectangle([x0, y0, x0 + module_size - 1, y0 + module_size - 1], fill=color)

    if logo_path:
        _overlay_logo(img, logo_path, logo_ratio)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)


def _overlay_logo(qr_img: "Image.Image", logo_path: str, ratio: float):
    """Paste a logo image centered on the QR code."""
    logo = Image.open(logo_path).convert("RGBA")
    qr_w, qr_h = qr_img.size
    logo_w = int(qr_w * ratio)
    logo_h = int(qr_h * ratio)
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
    pos = ((qr_w - logo_w) // 2, (qr_h - logo_h) // 2)
    qr_img.paste(logo, pos, mask=logo)
