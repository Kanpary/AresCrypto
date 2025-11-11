#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 5000
DIRECTORY = "."

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 QuasarProtect Advanced Server")
        print(f"📡 Rodando em http://0.0.0.0:{PORT}")
        print(f"📁 Servindo arquivos do diretório: {os.path.abspath(DIRECTORY)}")
        print("✅ Pronto para criptografar com 15 camadas!")
        print("=" * 60)
        httpd.serve_forever()
