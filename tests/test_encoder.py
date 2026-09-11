"""
test_encoder.py - Tests for the high-level encoder pipeline.
"""

import pytest
from unittest.mock import patch
from qr.encoder import encode


def test_encode_runs_without_error(tmp_path):
    output = str(tmp_path / "qr.png")
    with patch("qr.renderer.render") as mock_render:
        encode("https://example.com", output_path=output)
        mock_render.assert_called_once()


def test_encode_selects_correct_version():
    from qr.version import select_version
    version = select_version("HELLO", "M")
    assert version == 1


def test_encode_short_numeric():
    from qr.version import select_version
    version = select_version("12345", "H")
    assert version >= 1
