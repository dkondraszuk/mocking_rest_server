# Standard library imports...
from __future__ import print_function
import socket
import ssl
import time
from threading import Thread
try:
    # python 3.x
    from http.server import SimpleHTTPRequestHandler
    from socketserver import TCPServer
except ImportError:
    # python 2.x
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from SocketServer import TCPServer


class LocalWebServer:

    def __init__(self, port=None, key_file=None, cert_file=None):
        self.key_file = key_file
        self.cert_file = cert_file
        self.port = self._find_free_port() if not port else port
        self._handler = SimpleHTTPRequestHandler
        self._httpd = TCPServer(('', self.port), self._handler)

    @staticmethod
    def _find_free_port():
        s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        _, port = s.getsockname()
        s.close()
        return port

    def start_web_server(self, threading=False):
        if self.key_file and self.cert_file:
            self._httpd.socket = ssl.wrap_socket(self._httpd.socket,
                                                 keyfile=self.key_file,
                                                 certfile=self.cert_file,
                                                 server_side=True)
            print('Serving HTTPs server at port {}'.format(self.port))
        else:
            print('Serving HTTP server at port {}'.format(self.port))

        if threading:
            print('Server started in separate thread...')
            server_thread = Thread(target=self._httpd.serve_forever)
            server_thread.setDaemon(True)
            server_thread.start()
        else:
            self._httpd.serve_forever()

    def stop_web_server(self):
        self._httpd.shutdown()
        print('HTTPs server thread stopped.')


if __name__ == '__main__':
    local_server = LocalWebServer(port=8080)
    local_server.start_web_server(threading=True)
    for i in range(108):
        print(i)
        time.sleep(1)
