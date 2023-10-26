#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostname = "localhost"
server_port = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/webpage":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>Sample Webpage</title></head>", "utf-8"))
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>This is an example web page.</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
        elif self.path == "/teapot":
            self.send_response(418)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>Teapot</title></head>", "utf-8"))
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>The request was both short and stout.</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))           
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("Page not found.", "utf-8"))

if __name__ == "__main__":
    web_server = HTTPServer((hostname, server_port), MyServer)
    print("Server started http://%s:%s" % (hostname, server_port))

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass
    
    web_server.server_close()
    print("Server stopped.")
