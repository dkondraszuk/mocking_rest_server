from urllib.parse import urljoin

import requests

from constants import BASE_URL

TODOS_URL = urljoin(BASE_URL, 'todos')
USERS_URL = urljoin(BASE_URL, 'users')
WRONG_URL = urljoin(BASE_URL, 'wrong')


def get_todos():
    response = requests.get(TODOS_URL)

    return response if response.ok else None


def get_uncompleted_todos():
    response = get_todos()
    if response is None:
        return []
    else:
        todos = response.json()
        return [todo for todo in todos if todo['completed'] is False]


def get_users():
    response = requests.get(USERS_URL)

    return response if response.ok else None

