#!/usr/bin/env python3
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from constants import LOGGER, HELP_MESSAGE, HOME_PAGE, FAVICON


class WebServer(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        #LOGGER.info("%s - - [%s] %s\n" % (self.address_string(),self.log_date_time_string(),format%args))
        LOGGER.info("%s %s- - [%s] %s\n" % (self.address_string(),self.headers.get("User-Agent"), self.log_date_time_string(),format%args))

    def _set_headers(self, status_code=200, content_type="application/json"):
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def _serve_content(self, filepath, content_type="text/html"):
        try:
            with open(filepath, "rb") as file:
                content = file.read()
                self._set_headers(content_type=content_type)
                self.wfile.write(content)
        except FileNotFoundError:
            self._set_headers(status_code=404, content_type="text/plain")
            self.wfile.write(bytes("File not found.", "utf-8"))

    def serve_favicon(self):
        self._serve_content(filepath=FAVICON, content_type="image/x-icon")

    def serve_homepage(self):
        self._serve_content(filepath=HOME_PAGE)

    def do_GET(self):
        routes = {
            "/": self.serve_homepage,
            "/favicon.ico": self.serve_favicon
        }

        if self.path in routes.keys():
            routes[self.path]()
        else:
            self._set_headers(status_code=404, content_type="text/plain")
            self.wfile.write(bytes("Resource not found.", "utf-8"))


def help():
    return HELP_MESSAGE


def read_args(args):
    server_args = ["localhost", 8080]

    if len(sys.argv) == 1:
        return server_args
    elif (len(sys.argv) % 2 == 0) or (len(sys.argv) > 5):
        err_msg = f"Invalid number of arguments: Recieved {len(sys.argv)}.\n{help()}"
        raise ValueError(f"{err_msg}\n{help()}")

    while len(args) > 1:
        option = args.pop(1)
        arg = args.pop(1)
        if (option == "--hostname") or (option == "-n"):
            if type(arg) is not str:
                raise ValueError(f"Invalid hostname.\n{help()}") 
            server_args[0] = arg
        elif (option == "--port") or (option == "-p"):
            try:
                arg = int(arg)
            except ValueError:
                err_msg = f"Invalid port number: {arg} must be an integer."
                raise ValueError(f"{err_msg}\n{help()}")
            if (arg < 0) or (arg > 65535):
                err_msg = f"Invalid port number: {arg} must be in range 0-65535."
                raise ValueError(f"{err_msg}\n{help()}")
            server_args[1] = arg
        elif (option == "--help") or (option == "-h"):
            print(help())
            sys.exit(0)

    return server_args


def run_server(hostname="localhost", port=8080):
    web_server = HTTPServer((hostname, port), WebServer)
    LOGGER.info("Web server started on http://%s:%s" % (hostname, port))

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass
    
    web_server.server_close()
    LOGGER.info("Web server stopped.")


def main():
    hostname, port = read_args(sys.argv)
    run_server(hostname, port)


if __name__ == "__main__":
    main()
