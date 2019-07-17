# Standard library imports...
import unittest
from unittest.mock import patch
import requests

# Local imports...
from services import get_users
from tests.mocks import get_free_port, start_mock_server


class TestMockServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configure mock server
        # cls.mock_server_port = get_free_port()
        cls.mock_server_port = 8080
        start_mock_server(cls.mock_server_port)

    def test_request_response(self):
        mock_users_url = 'http://localhost:{port}/users'.format(port=self.mock_server_port)

        # Patch USERS_URL so that the service uses the mock server URL instead of the real URL
        with patch.dict('services.__dict__', {'USERS_URL': mock_users_url}):
            response = get_users()

        self.assertTrue({'Content-Type': 'application/json; charset=utf-8'}.items() <= response.headers.items())

        self.assertTrue(response.ok)

        self.assertListEqual(response.json(), [])

    def test_wrong_request_path_return_404_not_found(self):

        mock_wrong_url = 'http://localhost:{port}/wrong'.format(port=self.mock_server_port)

        response = requests.get(mock_wrong_url)
        print(response)

        self.assertEqual(response.status_code, 404)
