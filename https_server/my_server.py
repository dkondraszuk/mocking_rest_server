from http.server import HTTPServer, BaseHTTPRequestHandler

resource = b'/home/dkondraszuk/dev/mocking_rest_server/tests/mocks.py'

PORT = 8080


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        # self.wfile.write(resource)


httpd = HTTPServer(('localhost', PORT), BaseHTTPRequestHandler)
# httpd = HTTPServer(('localhost', PORT), SimpleHTTPRequestHandler)
print('Serving at port {}...'.format(PORT))
httpd.serve_forever()
