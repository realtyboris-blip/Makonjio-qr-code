"""
main.py - Single entry point.
Generates a QR code that redirects to https://realtyboris.com/
"""

from qr.encoder import encode

TARGET_URL = "https://quiet-caramel-d85792.netlify.app/"
OUTPUT_PATH = "output/boris_qr.png"


def main():
    print(f"Generating QR code for: {TARGET_URL}")
    encode(TARGET_URL, error_level="M", output_path=OUTPUT_PATH)
    print(f"Done! QR code saved to → {OUTPUT_PATH}")
    print("Scan it with any phone camera — it will open https://quiet-caramel-d85792.netlify.app/")


if __name__ == "__main__":
    main()
