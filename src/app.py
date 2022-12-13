from radox.response import *
import os

class App:
    def __init__(self):
        self.sdir = None
        self.surl = None

    def set_static(self, static_url, static_dir):
        self.static_dir  = static_dir
        self.static_url = static_url
        
    def serve_static(self,request : Request):
        new_url = request.url[len(self.static_url)::]
        return FileResponse(request, os.url.join(self.static_dir, new_url))

    def __call__(self, environ, response):
        try:
            request = Request(environ, response)
            if self.static_url !=None and  request.url.startswith(self.static_url):
                response = self.serve_static(request)
                return response.make_response()
            else:
                func = self.router.get_route(request.url)
                if func is not None:
                    response: Response = func(request)
                    return response.make_response()  
                else:
                    print(f'route Not found : {request.url}')
        except Exception as e:
            print(e)

        response =  Http404(request)
        return response.make_response()
