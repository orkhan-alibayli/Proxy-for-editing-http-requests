import http.server
import socketserver

class CustomRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.log_full_request()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'HTTP request logged successfully.')

    def do_POST(self):
        self.log_full_request()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'HTTP request logged successfully.')

    def log_full_request(self):
        with open('http_requests.log', 'a') as log_file:
            log_file.write(f'{self.command} {self.path} HTTP/{self.request_version}\n')
            for header, value in self.headers.items():
                log_file.write(f'{header}: {value}\n')
            
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                payload = self.rfile.read(content_length)
                log_file.write(f'\n{payload.decode()}')

            log_file.write('\n-----\n')

# Set up the server
PORT = 8080
Handler = CustomRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print(f"Serving on port {PORT}")
httpd.serve_forever()
