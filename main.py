"""
main.py - Starts the Flask server, exposes it via ngrok,
          and generates a QR code pointing to the live public URL.
"""

import threading
import time
import webbrowser

from pyngrok import ngrok
from qr.encoder import encode


def start_server():
    """Run the Flask server in a background thread."""
    from server import app
    app.run(port=5000, debug=False, use_reloader=False)


def main():
    print("Starting local server on http://localhost:5000 ...")
    t = threading.Thread(target=start_server, daemon=True)
    t.start()

    # Give Flask a moment to boot
    time.sleep(2)

    print("Opening ngrok tunnel...")
    tunnel = ngrok.connect(5000, bind_tls=True)
    public_url = tunnel.public_url
    print(f"Public URL: {public_url}")

    # Generate the QR pointing at the live URL
    output_path = "output/boris_qr.png"
    encode(public_url, error_level="M", output_path=output_path)
    print(f"\nQR code saved to → {output_path}")
    print("Scan it with your phone — it will open the landing page.\n")

    # Open the local page in the browser so you can preview it too
    webbrowser.open("http://localhost:5000")

    print("Press Ctrl+C to stop the server and close the tunnel.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        ngrok.disconnect(public_url)
        ngrok.kill()


if __name__ == "__main__":
    main()
