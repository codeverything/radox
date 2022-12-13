import cgi

class POST:
    __slots__ = 'data'
    
    def __init__(self, data):
        self.data = data
        
    def get(self, key):
        value = self.data.get(key, [''])
        if type(value) == str:
            value = cgi.escape(value)
        return value
    
    def __iter__(self):
        for key, value in self.data:
            yield key, value
            
# Credits: Joetib (https://github.com/jeotib/joeweb)
class Request:
    __slots__ = [
        "environ", 
        "http_host",
        "http_user_agent",
        "lang","method", 
        "path",
        "host_address", 
        "gateway_interface",
        "server_port", 
        "remote_host",
        "content_type",
        "content_length",
        "body",
        "query_string",
        "server_protocol",
        "server_software", 
        "start_response",
        "post",
        ]

    def __init__(self, environ, start_response):
        self.environ = environ
        self.http_host = environ['HTTP_HOST']
        self.http_user_agent = environ['HTTP_USER_AGENT']
        self.lang = environ.get('LANG')
        self.method = environ.get('REQUEST_METHOD')
        self.path = environ.get('PATH_INFO')
        self.host_address = environ.get('HTTP_HOST')
        self.gateway_interface = environ.get('GATEWAY_INTERFACE')
        self.server_port = environ.get('SERVER_PORT')
        self.remote_host = environ.get('REMOTE_HOST')
        self.content_type = environ.get('CONTENT_TYPE')
        self.content_length = environ.get('CONTENT_LENGTH')
        self.body = environ.get('BODY')
        self.query_string = environ.get('QUERY_STRING')
        self.server_protocol = environ.get('SEVER_PROTOCOL')
        self.server_software = environ.get('SERVER_SOFTWARE')
        self.start_response = start_response
        self.post = POST({})
        self.parse()

           
    def parse(self):
        if self.method != "POST":
            return
        environ = self.environ        
        field_storage = cgi.FieldStorage(
            fp=environ['wsgi.input'],
            environ = environ,
            keep_blank_values= True
        )     
        for i in field_storage.list:
            if not i.filename:
                self.post.data[i.name] = i.value
            else:
                self.post.data[i.name] = i
