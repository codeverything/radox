from __future__ import annotations

from wsgiref.simple_server import make_server
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import re
from typing import TYPE_CHECKING, TypeVar, Generic

# Import typing for compatibility with typing extensions in older Python versions
if TYPE_CHECKING:
    from typing_extensions import ParamSpec
    from collections.abc import Callable

    P = ParamSpec("P")
else:
    P = Generic

T = TypeVar("T")

class radox:
    """
    A simple web framework for defining routes and serving HTTP requests.
    Uses regular expressions to match routes and invokes the corresponding handler.
    """
    
    __slots__ = ("routes",)  # Optimize memory usage by limiting instance attributes
    
    def __init__(self) -> None:
        # List to store route patterns and their corresponding handlers
        self.routes: list[tuple[re.Pattern[str], Callable[..., str]]] = []
    
    def route(self, path_pattern: str) -> Callable[[Callable[P, str]], Callable[P, str]]:
        """
        Decorator for defining routes. Takes a string pattern (e.g. '/path/<param>') 
        and converts it into a regex pattern for matching dynamic URLs.
        """
        def decorator(handler: Callable[P, str]) -> Callable[P, str]:
            # Convert path pattern (e.g. '/path/<param>') to regex pattern
            pattern = re.sub(r'<([^>]+)>', r'(?P<\1>[^/]+)', path_pattern)
            # Append the compiled pattern and handler function to the route list
            self.routes.append((re.compile(f'^{pattern}$'), handler))
            return handler
        return decorator
    
    def serve(self, port: int) -> None:
        """
        Start the server on the given port and listen indefinitely.
        """
        handler = self.make_handler()
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"Serving on port {port}")
            httpd.serve_forever()
    
    def __call__(self, environ: dict[str, str], start_response: Callable[[str, list[tuple[str, str]]], None]) -> list[bytes]:
        """
        WSGI interface for handling requests. This function is called on each request.
        It matches the request path with defined routes and calls the appropriate handler.
        """
        path = environ['PATH_INFO']
        
        # Iterate over all registered routes and find a matching pattern
        for pattern, handler in self.routes:
            match = pattern.match(path)
            if match:
                kwargs = match.groupdict()  # Extract named parameters from the path
                try:
                    # Call the handler with parameters and return the response
                    response = handler(**kwargs)
                    start_response('200 OK', [('Content-Type', 'text/plain')])
                    return [response.encode()]
                except Exception as e:
                    # Handle exceptions and return 500 Internal Server Error
                    start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
                    return [f'500 Internal Server Error: {str(e)}'.encode()]
        
        # If no match is found, return a 404 Not Found response
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'404 Not Found']
    
    @staticmethod
    def render_template(template_name: str) -> str:
        """
        Render an HTML template by reading it from the file system.
        """
        with open(template_name, "r") as f:
            return f.read()
    
    def make_handler(self) -> type[BaseHTTPRequestHandler]:
        """
        Dynamically create a custom HTTP request handler class, which handles GET requests.
        This method is invoked by the serve method to define how requests are handled.
        """
        app = self
        
        class RequestHandler(BaseHTTPRequestHandler):
            __slots__ = ()
            
            def do_GET(self) -> None:
                """
                Handle GET requests by matching the request path against registered routes.
                """
                for pattern, handler in app.routes:
                    match = pattern.match(self.path)
                    if match:
                        kwargs = match.groupdict()  # Extract path parameters
                        try:
                            # Call the handler function and send the response
                            response = handler(**kwargs)
                            self.send_response(200)
                            self.send_header('Content-Type', 'text/plain')
                            self.end_headers()
                            self.wfile.write(response.encode())
                            return
                        except Exception as e:
                            # If an error occurs, return 500 Internal Server Error
                            self.send_response(500)
                            self.send_header('Content-Type', 'text/plain')
                            self.end_headers()
                            self.wfile.write(f'500 Internal Server Error: {str(e)}'.encode())
                            return
                
                # If no matching route is found, return 404 Not Found
                self.send_response(404)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"404 Not Found")
        
        return RequestHandler
