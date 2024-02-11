#!/usr/bin/env python3
import unittest
import subprocess
import requests
import time
from constants import WAIT_TIME, TESTS_DIR, SRC_DIR, EXPECTED_PAGE


class TestWebServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start server and write output to log files
        with open(f"{TESTS_DIR}/stdout.log", "w") as stdout_file, open(f"{TESTS_DIR}/stderr.log", "w") as stderr_file:
            cls.server_process = subprocess.Popen(
                ["/usr/bin/env", "python3", f"{SRC_DIR}/webserver.py"],
                stdout=stdout_file,
                stderr=stderr_file
            )

        # Give server time to start
        time.sleep(WAIT_TIME)

    @classmethod
    def tearDownClass(cls):
        # Stop server after tests
        cls.server_process.terminate()

    def test_valid_path(self):
        response = requests.get("http://localhost:8080/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.text, EXPECTED_PAGE)

    def test_invalid_path(self):
        response = requests.get("http://localhost:8080/invalid_path")
        self.assertEqual(response.status_code, 404)


# Run tests with `./tests.py`
if __name__ == "__main__":
    unittest.main()
