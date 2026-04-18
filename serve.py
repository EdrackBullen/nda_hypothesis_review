"""Run a local dev server for the NDA Hypothesis Review app.

Usage:  python serve.py [port]   (default port: 8000)
Then open http://localhost:8000 in your browser.
"""
import http.server
import socketserver
import sys
import webbrowser

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

handler = http.server.SimpleHTTPRequestHandler
handler.extensions_map.update({".json": "application/json"})

with socketserver.TCPServer(("", PORT), handler) as httpd:
    url = f"http://localhost:{PORT}"
    print(f"Serving at {url}  (Ctrl+C to stop)")
    webbrowser.open(url)
    httpd.serve_forever()
