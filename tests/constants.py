import os

WAIT_TIME = 2

TESTS_DIR = os.path.dirname(__file__)
SRC_DIR = f"{TESTS_DIR}/../src"

EXPECTED_PAGE = \
"""
.<!DOCTYPE html>
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
"""