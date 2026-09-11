"""
test_renderer.py - Tests for the QR image renderer.
"""

import pytest
from pathlib import Path


def _dummy_matrix(size: int = 21) -> list[list[int]]:
    return [[1 if (r + c) % 2 == 0 else 0 for c in range(size)] for r in range(size)]


def test_render_creates_file(tmp_path):
    pytest.importorskip("PIL", reason="Pillow not installed")
    from qr.renderer import render

    output = str(tmp_path / "test_qr.png")
    render(_dummy_matrix(), output_path=output, module_size=4)
    assert Path(output).exists()
    assert Path(output).stat().st_size > 0


def test_render_without_pillow(monkeypatch, tmp_path):
    import qr.renderer as renderer_mod
    monkeypatch.setattr(renderer_mod, "_PIL_AVAILABLE", False)
    with pytest.raises(ImportError, match="Pillow"):
        renderer_mod.render(_dummy_matrix(), output_path=str(tmp_path / "qr.png"))


def test_render_custom_colors(tmp_path):
    pytest.importorskip("PIL", reason="Pillow not installed")
    from qr.renderer import render

    output = str(tmp_path / "colored_qr.png")
    render(
        _dummy_matrix(),
        output_path=output,
        dark_color=(0, 0, 128),
        light_color=(255, 255, 200),
    )
    assert Path(output).exists()
