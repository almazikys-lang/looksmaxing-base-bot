#!/usr/bin/env python3
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

print("[BOOT] Python version:", sys.version)
print("[BOOT] Loading BOT_TOKEN from environment...")

BOT_TOKEN = os.getenv("BOT_TOKEN", "NOT_SET")
print(f"[BOOT] BOT_TOKEN set: {'YES' if BOT_TOKEN != 'NOT_SET' else 'NO'}")

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 Looksmaxing Base Bot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 60px 40px;
            max-width: 600px;
            text-align: center;
            animation: slideUp 0.6s ease-out;
        }
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .emoji {
            font-size: 80px;
            margin-bottom: 20px;
        }
        h1 {
            color: #333;
            font-size: 2.5em;
            margin-bottom: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .status {
            display: inline-block;
            background: #10b981;
            color: white;
            padding: 8px 16px;
            border-radius: 50px;
            font-weight: bold;
            margin-top: 10px;
            font-size: 14px;
        }
        p {
            color: #666;
            font-size: 16px;
            margin: 20px 0;
            line-height: 1.6;
        }
        .features {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 40px 0;
        }
        .feature {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }
        .feature-emoji {
            font-size: 40px;
            margin-bottom: 10px;
        }
        .feature h3 {
            color: #333;
            font-size: 14px;
            margin-bottom: 8px;
        }
        .feature p {
            color: #999;
            font-size: 12px;
            margin: 0;
        }
        .button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 14px 40px;
            border: none;
            border-radius: 50px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 30px;
            transition: transform 0.3s, box-shadow 0.3s;
            text-decoration: none;
            display: inline-block;
        }
        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #999;
            font-size: 12px;
        }
        .stats {
            display: flex;
            justify-content: space-around;
            margin: 40px 0;
            padding: 20px 0;
            border-top: 1px solid #eee;
            border-bottom: 1px solid #eee;
        }
        .stat {
            text-align: center;
        }
        .stat-number {
            font-size: 28px;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            color: #999;
            font-size: 12px;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="emoji">🎯</div>
        <h1>Looksmaxing Base Bot</h1>
        <div class="status">퉪 ⚠️ LIVE</div>
        
        <p>Your personal guide to maxing out your looks and potential</p>
        
        <div class="features">
            <div class="feature">
                <div class="feature-emoji">🧌‍♂️</div>
                <h3>Atlas Guide</h3>
                <p>Complete facial anatomy</p>
            </div>
            <div class="feature">
                <div class="feature-emoji">👷‍♂️</div>
                <h3>V-Shape</h3>
                <p>Body development tips</p>
            </div>
            <div class="feature">
                <div class="feature-emoji">🏃</div>
                <h3>Health</h3>
                <p>Wellness & fitness</p>
            </div>
            <div class="feature">
                <div class="feature-emoji">🤣</div>
                <h3>Mewing</h3>
                <p>Oral posture tips</p>
            </div>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-number">✅</div>
                <div class="stat-label">Online 24/7</div>
            </div>
            <div class="stat">
                <div class="stat-number">100%</div>
                <div class="stat-label">Free Access</div>
            </div>
            <div class="stat">
                <div class="stat-number">🚀</div>
                <div class="stat-label">Fast</div>
            </div>
        </div>
        
        <a href="https://t.me/looksmaxing_base_bot" class="button">Open Bot 🤖</a>
        
        <div class="footer">
            <p>✨ Powered by Telegram Bot | Hosted on Render</p>
        </div>
    </div>
</body>
</html>
"""

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
            print(f"[REQUEST] GET / - Served HTML page")
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"404 Not Found")
            print(f"[REQUEST] GET {self.path} - Not found")
    
    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"[BOOT] Starting HTTP server on port {port}...")
    
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f"[BOOT] Server ready! Waiting for requests...")
    print(f"[BOOT] Available at: http://localhost:{port}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server stopped")
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
