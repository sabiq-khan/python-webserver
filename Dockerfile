FROM python:alpine
COPY . /
ENTRYPOINT ["/usr/bin/env", "python3", "./webserver.py"]
CMD ["--hostname", "0.0.0.0"]
