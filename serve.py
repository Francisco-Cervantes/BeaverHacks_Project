#!/usr/bin/env python3
"""
Frontend dev server — serves Frontend/ with no-cache headers so the browser
always loads fresh files. Run from the project root:
    python3 serve.py
"""
import http.server
import socketserver

PORT = 8000


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    """Serve the Frontend/ directory with aggressive no-cache headers."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="Frontend", **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format, *args):
        # Print a clean, readable log line
        print(f"  {self.command} {self.path}")


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), NoCacheHandler) as httpd:
        print(f"Frontend server running → http://127.0.0.1:{PORT}")
        print("Press Ctrl+C to stop.\n")
        httpd.serve_forever()
