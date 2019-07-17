# Standard-library imports...
import os


BASE_URL = 'http://jsonplaceholder.typicode.com'
SKIP_REAL = os.getenv('SKIP_REAL', False)  # works only in the same terminal session (run tests from the same terminal)
# SKIP_REAL = True
