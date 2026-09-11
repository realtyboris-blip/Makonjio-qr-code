# Custom QR Code Generator

A from-scratch QR code generator built in Python, with support for custom logos, colors, and fonts.

## Project Structure

```
custom_qr/
├── main.py               # Entry point
├── qr/                   # Core QR encoding library
│   ├── encoder.py        # High-level encoder orchestration
│   ├── bit_buffer.py     # Bit-level buffer utility
│   ├── data_encoding.py  # Data mode encoding (numeric, alphanumeric, byte)
│   ├── error_correction.py # Reed-Solomon error correction
│   ├── matrix.py         # QR matrix construction
│   ├── patterns.py       # Finder, alignment, timing patterns
│   ├── masking.py        # Data masking
│   ├── format_info.py    # Format and version information
│   ├── version.py        # Version selection logic
│   └── renderer.py       # Image rendering (PNG/SVG)
├── tests/                # Unit tests
├── output/               # Generated QR code images
└── assets/               # Logos and fonts for customization
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```
