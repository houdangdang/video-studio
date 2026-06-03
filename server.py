#!/usr/bin/env python3
"""
VideoForge — 一键本地服务器（自动打开浏览器）
Usage: python3 server.py
       或直接双击此文件（macOS 右键 → 打开方式 → Python Launcher）
"""

import http.server
import os
import sys
import webbrowser
import threading
import time

PORT = 8765
DIR = os.path.dirname(os.path.abspath(__file__))

MIME = {
    ".html": "text/html; charset=utf-8",
    ".js":   "application/javascript; charset=utf-8",
    ".wasm": "application/wasm",
    ".css":  "text/css; charset=utf-8",
    ".svg":  "image/svg+xml",
    ".png":  "image/png",
    ".jpg":  "image/jpeg",
    ".mp4":  "video/mp4",
    ".webm": "video/webm",
    ".gif":  "image/gif",
    ".json": "application/json",
}


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def guess_type(self, path):
        ext = os.path.splitext(path)[1].lower()
        return MIME.get(ext, "application/octet-stream")

    def end_headers(self):
        # CORS + COOP/COEP for cross-origin isolation (SharedArrayBuffer for FFmpeg threads)
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Cross-Origin-Resource-Policy", "cross-origin")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def log_message(self, fmt, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}")


if __name__ == "__main__":
    URL = f"http://localhost:{PORT}"
    print(f"\n  🎬 VideoForge dev server")
    print(f"  Serving: {DIR}")
    print(f"  Open:    {URL}\n")

    # Auto-open browser after a short delay (in background thread)
    def _open_browser():
        time.sleep(0.6)
        webbrowser.open(URL)

    threading.Thread(target=_open_browser, daemon=True).start()

    with http.server.HTTPServer(("127.0.0.1", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  👋 Shutting down.\n")
            httpd.server_close()
            sys.exit(0)
