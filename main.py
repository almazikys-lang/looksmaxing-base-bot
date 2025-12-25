#!/usr/bin/env python3
import os
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

print("[BOOT] Python version:", sys.version)
print("[BOOT] Loading BOT_TOKEN from environment...")

BOT_TOKEN = os.getenv("BOT_TOKEN", "NOT_SET")
print(f"[BOOT] BOT_TOKEN set: {'YES' if BOT_TOKEN != 'NOT_SET' else 'NO'}")

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Looksmaxing Base Bot is running!\n")
        print(f"[REQUEST] GET {self.path}")
    
    def log_message(self, format, *args):
        # Silent logger
        pass

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"[BOOT] Starting HTTP server on port {port}...")
    
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f"[BOOT] Server ready! Waiting for requests...")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server stopped")
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
