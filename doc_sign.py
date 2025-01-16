import http.server
import socketserver


PORT = 8000


DIRECTORY = "."

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "doc_signature_request.html"  # Name file HTML
        return super().do_GET()

# Avvia il server
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Server avviato su http://localhost:{PORT}")
    httpd.serve_forever()
