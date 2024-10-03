from wsgiref.simple_server import make_server
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import TCPServer

class Radox:
    def __init__(self):
        self.routes = {}

    def route(self, path):
        def decorator(handler):
            self.routes[path] = handler
            return handler
        return decorator

    def serve(self, port):
        handler = self.make_handler()
        with TCPServer(("", port), handler) as httpd:
            print(f"Serving on port {port}")
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

    def render_template(self, template_name):
        with open(template_name, "r") as f:
            return f.read()

    def make_handler(self):
        # Nested RequestHandler class inheriting from BaseHTTPRequestHandler
        class RequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path in self.server.web_framework.routes:
                    handler = self.server.web_framework.routes[self.path]
                    response = handler()
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response.encode())
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"404 Not Found")

        # this class will integrate the web framework
        class CustomTCPServer(TCPServer):
            def __init__(self, *args, **kwargs):
                self.web_framework = kwargs.pop("web_framework")
                super().__init__(*args, **kwargs)

        return CustomTCPServer(web_framework=self)
