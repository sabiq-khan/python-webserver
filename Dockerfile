FROM python:alpine
RUN mkdir /app /app/resources
RUN pip install requests
COPY src /app
ENTRYPOINT ["/usr/bin/env", "python3", "/app/webserver.py"]
CMD ["--hostname", "0.0.0.0"]
