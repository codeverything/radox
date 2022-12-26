from src.request import Request

file_types = {
    'html': 'text/html',
    'css':  'text/css'
}

class Response:
    __slots__ = 'headers', 'status_code', 'make_response', 'content_type', 'response_content'

    def __init__(self,request: Request, status_code: str, content_type: str):
        self.headers = []
        self.status_code = status_code
        self.make_response = request.make_response
        self.content_type = content_type
        self.response_content = []
        
    def response(self):
        self.make_response(self.status_code, [('Content-Type', self.content_type)])
        return self.response_content         


class HttpResponse(Response):
    def __init__(self, request: Request, content, status_code='200 OK', content_type='text/html'):
        super().__init__( request, status_code, content_type)
        if type(content) == str:
            content = content.encode()
        self.response_content.append(content)

        
class Render(HttpResponse):
    def __init__(self, request: Request, filename: str, context: dict = {}):
        try:
            with open(filename, 'r') as f:
                text = f.read()
        except FileNotFoundError:
            print(f'Error when opening file {filename}')
            raise Exception(f'File Could not be found! {filename}')
        super().__init__(request, text, '200 OK')


class Error(Response):
    def __init__(self, request: Request, error_code: str):
        super().__init__(request, '404 Not Found', 'text/html')
        self.response_content.append("404 Not Found".encode())


class Http404(Error):
    def __init__(self, request):
        super().__init__(request, '404 Not Found')