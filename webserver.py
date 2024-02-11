#!/usr/bin/env python3
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from socket import gaierror
from constants import (
    LOGGER, 
    HELP_MESSAGE, 
    DEFAULT_HOST, 
    DEFAULT_PORT, 
    HOMEPAGE_PATH, 
    FAVICON_PATH
)


class WebServer(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        client_host, client_port = self.client_address
        timestamp = self.log_date_time_string()
        request = self.requestline
        response_code = args[1]
        user_agent = self.headers.get("User-Agent")

        access_log = "%s - - [%s] \"%s\" %s - - \"%s\"" % (
            f"{client_host}:{client_port}",
            timestamp,
            request,
            response_code,
            user_agent
        )
        LOGGER.info(access_log)

    def _set_headers(
            self, 
            status_code=200, 
            content_type="application/json", 
            content_length=0
        ):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", content_length)
        self.end_headers()

    def _serve_content(self, filepath, content_type="text/html"):
        try:
            with open(filepath, "rb") as file:
                content = file.read()
                self._set_headers(
                    content_type=content_type, 
                    content_length=len(content)
                )
                self.wfile.write(content)
                LOGGER.info(f"Served file: {filepath}")
        except FileNotFoundError:
            self._set_headers(status_code=404, content_type="text/plain")
            self.wfile.write(bytes("File not found.", "utf-8"))
            LOGGER.error(f"File not found: {filepath}")

    def serve_favicon(self):
        self._serve_content(filepath=FAVICON_PATH, content_type="image/x-icon")

    def serve_homepage(self):
        self._serve_content(filepath=HOMEPAGE_PATH)

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
            LOGGER.error(f"Resource not found: {self.path}")


def help():
    return HELP_MESSAGE


def read_args(args):
    server_args = [DEFAULT_HOST, DEFAULT_PORT]

    # Checks that correct number of arguments were passed
    if len(args) == 0:
        return server_args
    elif (len(args) == 1) and ((args[0] == "--help") or (args[0] == "-h")):
        print(help())
        sys.exit(0)
    elif (len(args) % 2 == 1) or (len(args) > 4):
        if ("--help" in args) or ("-h" in args):
            print(help())
            sys.exit(0)
        err_msg = f"Invalid number of arguments: Recieved {len(args)}."
        raise ValueError(f"{err_msg}\n{help()}")

    # Checks that correct values were passed for arguments
    while len(args) > 0:
        option = args.pop(0)
        if (option == "--hostname") or (option == "-n"):
            arg = args.pop(0)
            server_args[0] = arg
        elif (option == "--port") or (option == "-p"):
            arg = args.pop(0)
            try:
                arg = int(arg)
            except ValueError:
                err_msg = f"Invalid port number: '{arg}'. Must be an integer."
                raise ValueError(f"{err_msg}\n{help()}")
            if (arg < 0) or (arg > 65535):
                err_msg = f"Invalid port number: '{arg}'." + \
                    " Must be in range 0-65535."
                raise ValueError(f"{err_msg}\n{help()}")
            server_args[1] = arg
        elif (option == "--help") or (option == "-h"):
            print(help())
            sys.exit(0)
        else:
            err_msg = f"Invalid option: '{option}' is not a valid option."
            raise ValueError(f"{err_msg}\n{help()}")

    return server_args


def run_server(hostname, port):
    try:
        web_server = HTTPServer((hostname, port), WebServer)
    except gaierror:
        err_msg = f"Invalid hostname: '{hostname}'." + \
        " Must be valid IP address or DNS name."
        raise gaierror(f"{err_msg}\n{help()}")

    try:
        LOGGER.info("Starting web server on http://%s:%s" % (hostname, port))
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass
    
    web_server.server_close()
    LOGGER.info("Web server stopped.")


def main():
    # Excludes sys.argv[0] since it's just the name of this module
    hostname, port = read_args(sys.argv[1:])
    run_server(hostname, port)


if __name__ == "__main__":
    main()
