import http.server
import socketserver
import json
import os

PORT = 8000

class VendingMachineRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        elif self.path == '/transactions.json':
            try:
                with open('transactions.json', 'r') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(f.read().encode())
                    return
            except FileNotFoundError:
                self.send_error(404, 'File Not Found: transactions.json')
                return
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

with socketserver.TCPServer(("", PORT), VendingMachineRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()