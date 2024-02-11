# Python Web Server
This is a web server implemented with the Python [http](https://docs.python.org/3/library/http.server.html) library that serves an HTML page.

# Project Directory
```
.
├── Dockerfile
├── .dockerignore
├── .gitignore
├── README.md
├── src
│   ├── constants.py
│   ├── resources
│   │   ├── favicon.ico
│   │   └── home.html
│   └── webserver.py
└── tests
    ├── constants.py
    └── tests.py
```
[src](./src/) contains the code for the web server. The [src/resources](./src/resources) subdirectory contains the HTML page to be served.

[tests](./tests) contains unit and integration tests.

The project root contains a [Dockerfile](./Dockerfile) for containerizing the web server.

# Installation
`git clone` this repository. Then, run the following command to install Python packages required for this project:
```
pip install -r requirements.txt
```

Note that not all of the listed packages are required to run the web server itself. Some, like the [requests](https://requests.readthedocs.io/en/latest/) library, are required to run the [tests](./tests).

# Usage
## Options
The web server can be run as follows:
```
$ cd src
$ ./webserver.py
```

### Getting help
Passing the `--help` or `-h` option prints a help message. This message also gets printed when errors occur. 
```
$ ./webserver.py -h

Usage: ./webserver.py [--hostname/-n HOSTNAME] [--port/-p PORT_NUMBER] [--help/-h]

Starts an HTTP server. If no arguments are provided, the server listens on `localhost:8080`.

Options:
	--hostname/-n	String representing the host name or IP address of the network interface that the server will listen on.
			Default value is `localhost`.

	--port/-p       Integer between 0 and 65535 representing the TCP port that the server will listen on.
			Default value is 8080.

	--help/-h       Prints this help message.

Examples:
    # Starting a server that listens on `localhost:8080`
    $ ./webserver.py

    # Starting a server that listens on port 8080 on all interfaces
    $ ./webserver.py -n 0.0.0.0

    # Starting a server that listens on port 8081 on all interfaces
    $ ./webserver.py -n 0.0.0.0 -p 8081

```

### No options
By default, the web server listens on `localhost:8080`. 
```
$ ./webserver.py
[2024-02-11 13:11:24,810][webserver.py][INFO]: Starting web server on http://localhost:8080
...

$ curl http://localhost:8080
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Home Page</title>
        <link rel="icon" href="favicon.ico" type="image/x-icon">
    </head>

    <body>
        <h1>Home Page</h1>
        <p>This is a home page served by a sample Python web server.</p>
    </body>
</html>
```

### Hostname
The web server can be configured to listen on a different interface with the `--hostname` or `-n` option.
```
# Starting a web server that listens on all interfaces
$ ./webserver.py -n 0.0.0.0
[2024-02-11 13:15:17,157][webserver.py][INFO]: Starting web server on http://0.0.0.0:8080
...

$ curl http://0.0.0.0:8080
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Home Page</title>
        <link rel="icon" href="favicon.ico" type="image/x-icon">
    </head>

    <body>
        <h1>Home Page</h1>
        <p>This is a home page served by a sample Python web server.</p>
    </body>
</html>
```

### Port
The web server can be configured to listen on a different port with the `--port` or `-p` option.
```
$ ./webserver.py -p 8081
[2024-02-11 13:09:23,580][webserver.py][INFO]: Starting web server on http://localhost:8081
...

$ curl http://localhost:8081
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Home Page</title>
        <link rel="icon" href="favicon.ico" type="image/x-icon">
    </head>

    <body>
        <h1>Home Page</h1>
        <p>This is a home page served by a sample Python web server.</p>
    </body>
</html>
```

### Passing both options
Both options can be passed to change both the interface and the port.
```
$ ./webserver.py -n 0.0.0.0 -p 8081

$ curl http://0.0.0.0:8081
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Home Page</title>
        <link rel="icon" href="favicon.ico" type="image/x-icon">
    </head>

    <body>
        <h1>Home Page</h1>
        <p>This is a home page served by a sample Python web server.</p>
    </body>
</html>
```

## Logging
The web server generates access logs with the following format:
```
[{timestamp}][{module}][{log-level}]: {client-address}:{client-port} - - [{access-timestamp}] "{http-method} / {http-version}" {http-response-code} - - "{user-agent}"

```

For example:
```
$ ./webserver.py -n 0.0.0.0
[2024-02-11 13:23:56,781][webserver.py][INFO]: Starting web server on http://0.0.0.0:8080
[2024-02-11 13:24:13,882][webserver.py][INFO]: 127.0.0.1:39868 - - [11/Feb/2024 13:24:13] "GET / HTTP/1.1" 200 - - "curl/7.81.0"
[2024-02-11 13:24:13,882][webserver.py][INFO]: Served file: src/resources/home.html
[2024-02-11 13:24:42,024][webserver.py][INFO]: xxx.xxx.xxx.xxx:57604 - - [11/Feb/2024 13:24:42] "GET / HTTP/1.1" 200 - - "Mozilla/5.0 (iPhone; CPU iPhone OS x_x_x like Mac OS X) AppleWebKit/x.x.xx (KHTML, like Gecko) Version/xx.x Mobile/xxxxxx Safari/xxx.x"
[2024-02-11 13:24:42,024][webserver.py][INFO]: Served file: src/resources/home.html
[2024-02-11 13:25:09,146][webserver.py][INFO]: 127.0.0.1:55886 - - [11/Feb/2024 13:25:09] "GET /invalid-path HTTP/1.1" 404 - - "curl/7.81.0"
[2024-02-11 13:25:09,146][webserver.py][ERROR]: Resource not found: /invalid-path
^C[2024-02-11 13:25:22,769][webserver.py][INFO]: Web server stopped.
```

## Docker
### Image build
A container image can be built with the [Dockerfile](./Dockerfile) in the project root with the following command:
```
$ docker build -t webserver .

Sending build context to Docker daemon   38.4kB
Step 1/5 : FROM python:alpine
 ---> c54b53ca8371
Step 2/5 : RUN mkdir /app /app/resources
 ---> Using cache
 ---> 0e1b7b6f438d
Step 3/5 : COPY src /app
 ---> fe0b52b52ae8
Step 4/5 : ENTRYPOINT ["/usr/bin/env", "python3", "/app/webserver.py"]
 ---> Running in 73b53d4508e4
Removing intermediate container 73b53d4508e4
 ---> 0c7f7ad5e494
Step 5/5 : CMD ["--hostname", "0.0.0.0"]
 ---> Running in 2383a3868924
Removing intermediate container 2383a3868924
 ---> 2f58cf9b3719
Successfully built 2f58cf9b3719
Successfully tagged webserver:latest
```

### Listening for traffic
Note that the [Dockerfile](./Dockerfile) uses the `CMD` instruction to pass `0.0.0.0` as the default interface to listen on:
```
CMD ["--hostname", "0.0.0.0"]
```

This is because by default, the `docker run` command runs the container in a bridge network, with its own network namespace separate from the host. Thus, if a container running in a bridge network listens on its own `localhost`, it will be unable to listen for external traffic, including traffic from its host.
```
$ docker run webserver -n localhost
[2024-02-11 21:35:26,634][webserver.py][INFO]: Starting web server on http://localhost:8080
...

# This fails because there is nothing listening on the host's localhost
$ curl http://localhost:8080
curl: (7) Failed to connect to localhost port 8080 after 0 ms: Connection refused

# The containerized web server is listening on its own localhost
# Accessible only from inside the container
$ container_id=$(docker ps | grep webserver | awk '{print $1}')
$ docker exec -it $container_id /bin/sh
/ # apk add curl
...
/ # curl http://localhost:8080
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Home Page</title>
        <link rel="icon" href="favicon.ico" type="image/x-icon">
    </head>

    <body>
        <h1>Home Page</h1>
        <p>This is a home page served by a sample Python web server.</p>
    </body>
</html>
/ # exit
$
```

To send external traffic (from the host or other devices on the LAN) to the container, the container needs to be listening on the host's network interfaces. 

### Bridge networking
In the default Docker [bridge network](https://docs.docker.com/network/drivers/bridge/), this can be done by having the container listen on all interfaces available to it (`--hostname 0.0.0.0`), and passing the `-p` option for Docker run to make the bridge map a port on the host to the port being used on the container.
```
# The container is listening on port 8080 on its network interfaces
# The bridge has mapped this port to port 80 on the host's network interfaces
$ docker run -p 80:8080 webserver
[2024-02-11 21:50:27,641][webserver.py][INFO]: Starting web server on http://0.0.0.0:8080
...

# The host can now send traffic to the container over localhost:80
$ curl http://localhost:80
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Home Page</title>
        <link rel="icon" href="favicon.ico" type="image/x-icon">
    </head>

    <body>
        <h1>Home Page</h1>
        <p>This is a home page served by a sample Python web server.</p>
    </body>
</html>

# Other devices on the LAN can send traffic to the container over <host-ip>:80
$ curl http://xxx.xxx.xxx.xxx:80
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Home Page</title>
        <link rel="icon" href="favicon.ico" type="image/x-icon">
    </head>

    <body>
        <h1>Home Page</h1>
        <p>This is a home page served by a sample Python web server.</p>
    </body>
</html>
```

### Host networking
However, if you want the container to strictly listen for traffic from the host and not from external devices, this can be done by using Docker [host networking](https://docs.docker.com/network/drivers/host/) instead of bridge networking, which makes it so that the container will use the host's network namespace and interfaces. Then, when the container listens on `localhost`, it will be listening on the host's `localhost`.
```
# No port mappings are necessary this time because the container is using the host's port 8080
$ docker run --network host webserver -n localhost
[2024-02-11 21:59:56,082][webserver.py][INFO]: Starting web server on http://localhost:8080
...

# The container is listening on the host's loopback interface
# Thus, it can receive traffic from the host
$ curl http://localhost:8080
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Home Page</title>
        <link rel="icon" href="favicon.ico" type="image/x-icon">
    </head>

    <body>
        <h1>Home Page</h1>
        <p>This is a home page served by a sample Python web server.</p>
    </body>
</html>

# The container is not listening on the host's other interfaces
# Thus, it cannot recieve traffic from other devices on the LAN
$ curl http://<host-ip>:8080
curl: (7) Failed to connect to <host-ip> port 8080 after 0 ms: Connection refused
```