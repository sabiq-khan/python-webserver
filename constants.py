import sys
import logging

LOGGER = logging.getLogger("webserver.py")
LOGGER.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s]: %(message)s")
handler.setFormatter(formatter)
LOGGER.addHandler(handler)

DEFAULT_HOST = "localhost"
DEFAULT_PORT = "8080"

FAVICON_PATH = "favicon.ico"
HOMEPAGE_PATH = "home.html"

HELP_MESSAGE = \
"""
Usage: ./webserver.py [--hostname/-n HOSTNAME] [--port/-p PORT_NUMBER] [--help/-h]

Starts an HTTP server. If no arguments are provided, the server listens on `localhost:8080`.

Options:
	--hostname/-n\tString representing the host name or IP address of the network interface that the server will listen on.\n\t\t\tDefault value is `localhost`.

	--port/-p       Integer between 0 and 65535 representing the TCP port that the server will listen on.\n\t\t\tDefault value is 8080.

	--help/-h       Prints this help message.

Examples:
    # Starting a server that listens on `localhost:8080`
    $ ./webserver.py

    # Starting a server that listens on port 8080 on all interfaces
    $ ./webserver.py -n 0.0.0.0

    # Starting a server that listens on port 8081 on all interfaces
    $ ./webserver.py -n 0.0.0.0 -p 8081
"""
