# Standard library imports...
import unittest
from unittest import skipIf
from unittest.mock import Mock, patch

# Local imports...
from services import get_todos, get_uncompleted_todos
from constants import SKIP_REAL


class TestServer(unittest.TestCase):

    def test_request_response(self):
        # Send a request to the API server and store the response
        response = get_todos()

        # Confirm that the request-response cycle completed successfully
        self.assertIsNotNone(response)

    # Mocking with a @patch decorator - mocking services.request.get() method to return "return_value.ok = True"
    @patch('services.requests.get')
    def test_getting_todos(self, mock_get):
        # Configure the mock to return a response with an OK status code
        mock_get.return_value.ok = True

        # Call the service, which will send a request to the server
        response = get_todos()

        # If a request is sent successfully, then I expect a response to be returned
        self.assertIsNotNone(response)

    # Mocking with "with statement"
    def test_getting_todos_with(self):
        with patch('services.requests.get') as mock_get:
            # Configure the mock to return a response with an OK status code
            mock_get.return_value.ok = True

            # Call the service, which will send a request to the server
            response = get_todos()

        # If the request is sent successfully, then I expec a response to be returned
        self.assertIsNotNone(response)

    # Mocking with 'patcher'
    def test_getting_todos_patcher(self):
        mock_get_patcher = patch('services.requests.get')

        # Start patching 'requests.get'
        mock_get = mock_get_patcher.start()

        # Configure the mock to return a response with an OK status code
        mock_get.return_value.ok = True

        # Call the service, which will send a request to the server
        response = get_todos()

        # Stop patching 'requests.get'
        mock_get_patcher.stop()

        # If the request is sent successfully, then I expect a response to be returned
        self.assertIsNotNone(response)

    @patch('services.requests.get')
    def test_getting_todos_when_response_is_ok(self, mock_get):
        todos = [{
            'userId': 1,
            'id': 1,
            'title': 'Make the bed',
            'completed': False,
        }]

        # Configure the mock to return a response with an OK status code. Also, the mock should have a 'json()'
        # method that returns a list of todos
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = todos

        # Call the service, which will send a request to the server
        response = get_todos()

        # If the request is sent successfully, then I expect a response to be returned
        self.assertListEqual(response.json(), todos)

    @patch('services.requests.get')
    def test_getting_todos_when_response_is_not_ok(self, mock_get):
        # Configure the mock to not return a response with an OK status code
        mock_get.return_value.ok = False

        # Call the service, which will send a request to the server
        response = get_todos()

        # If the response containts an error, I should get no todos
        self.assertIsNone(response)

    @patch('services.get_todos')
    def test_getting_uncompleted_todos_when_todo_is_not_none(self, mock_get_todos):
        todo1 = {
            'userId': 1,
            'id': 1,
            'title': 'Make the bed',
            'completed': False
        }
        todo2 = {
            'userId': 1,
            'id': 2,
            'title': 'Walk the dog',
            'completed': True
        }

        # Configure mock to return a response with a JSON-serialized list of todos
        mock_get_todos.return_value = Mock()
        mock_get_todos.return_value.json.return_value = [todo1, todo2]

        # Call the service, which will get a list of todos filtered on uncompleted
        uncompleted_todos = get_uncompleted_todos()

        # Confirm that the mock was called
        self.assertTrue(mock_get_todos.called)

        # Confirm that the expected filtered list of todos was returned
        self.assertListEqual(uncompleted_todos, [todo1])

    @patch('services.get_todos')
    def test_getting_uncompleted_todos_when_todos_is_none(self, mock_get_todos):
        # Configure mock to return None
        mock_get_todos.return_value = None

        # Call the service, which will return an empty list
        uncompleted_todos = get_uncompleted_todos()

        # Confirm that the mock was called
        self.assertTrue(mock_get_todos.called)

        # Confirm that an empty list was returned
        self.assertListEqual(uncompleted_todos, [])

    @skipIf(SKIP_REAL, 'Skipping tests that hit the real API server')
    def test_integration_contract(self):
        # Call the service to hit the actual API
        actual = get_todos()
        actual_keys = actual.json().pop().keys()

        # Call the service to hit the mocked API
        with patch('services.requests.get') as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = [{
                'userId': 1,
                'id': 1,
                'title': 'Make the bed',
                'completed': False
            }]

            mocked = get_todos()
            mocked_keys = mocked.json().pop().keys()

        # An object from the actual API and an object from the mocked API should have the same data structure
        self.assertListEqual(list(actual_keys), list(mocked_keys))
