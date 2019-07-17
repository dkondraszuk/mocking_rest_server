# Standard library imports...
import unittest

# Third-party imports...
import requests

# Local imports...
from services import get_users, WRONG_URL


class TestRealServer(unittest.TestCase):

    def test_request_response(self):
        response = get_users()

        # Check that below is a subset of response.headers
        self.assertTrue({'Content-Type': 'application/json; charset=utf-8'}.items() <= response.headers.items())

        self.assertTrue(response.ok)

        self.assertIsInstance(response.json(), list)

    def test_wrong_request_path_return_404_not_found(self):
        response = requests.get(WRONG_URL)

        print(response)

        self.assertEqual(response.status_code, 404)
