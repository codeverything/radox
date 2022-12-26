from wsgiref.simple_server import make_server
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import *


class radox:
    def __init__(self):
        self.routes = {}

    def route(self, path):
        def decorator(handler):
            self.routes[path] = handler
            def wrapper():
                return handler()
            return wrapper
        return decorator

    def serve(self, port):
        handler = self.make_handler()
        with socketserver.TCPServer(("", port), handler) as httpd:
            print("Serving on port", port)
            httpd.serve_forever()

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        handler = self.routes.get(path)
        if handler is None:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return [b'404 Not Found']
        else:
             start_response('200 OK', [('Content-Type', 'text/plain')])
             response = self.routes[path]()
             return [response.encode()]

    def render_template(template_name):
        with open(template_name, "r") as f:
           return f.read()

    def make_handler(self):
        class RequestHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path in self.server.web_framework.routes:
                    handler = self.server.web_framework.routes[self.path]
                    handler(self)
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"404 Not Found")

        class TCPServer(socketserver.TCPServer):
            def __init__(self, *args, **kwargs):
                self.web_framework = kwargs.pop("web_framework")
                super().__init__(*args, **kwargs)

        return TCPServer(web_framework=self)
