from wsgiref.simple_server import make_server
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import re

class radox:
    def __init__(self):
        self.routes = []
    
    def route(self, path_pattern):
        def decorator(handler):
            pattern = re.sub(r'<([^>]+)>', r'(?P<\1>[^/]+)', path_pattern)
            self.routes.append((re.compile(f'^{pattern}$'), handler))
            def wrapper():
                return handler()
            return wrapper
        return decorator
    
    def serve(self, port):
        handler = self.make_handler()
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"Serving on port {port}")
            httpd.serve_forever()
    
    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        
        for pattern, handler in self.routes:
            match = pattern.match(path)
            if match:
                kwargs = match.groupdict()
                try:
                    response = handler(**kwargs)
                    start_response('200 OK', [('Content-Type', 'text/plain')])
                    return [response.encode()]
                except Exception as e:
                    start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
                    return [f'500 Internal Server Error: {str(e)}'.encode()]
        
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'404 Not Found']
    
    @staticmethod
    def render_template(template_name):
        with open(template_name, "r") as f:
            return f.read()
    
    def make_handler(self):
        app = self
        
        class RequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                for pattern, handler in app.routes:
                    match = pattern.match(self.path)
                    if match:
                        kwargs = match.groupdict()
                        try:
                            response = handler(**kwargs)
                            self.send_response(200)
                            self.send_header('Content-Type', 'text/plain')
                            self.end_headers()
                            self.wfile.write(response.encode())
                            return
                        except Exception as e:
                            self.send_response(500)
                            self.send_header('Content-Type', 'text/plain')
                            self.end_headers()
                            self.wfile.write(f'500 Internal Server Error: {str(e)}'.encode())
                            return
                
                self.send_response(404)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"404 Not Found")
        
        return RequestHandler
