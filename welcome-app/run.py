from radox.app import App

from radox.router import Path

from radox.response import HttpResponse, RenderResponse

from wsgiref.simple_server import make_server

app = App()

app.set_static('/static/', '.')

def print_received(request):

    print(request.query_string)

    return RenderResponse(

        request,

    'index.html',

    None

    )

if __name__=='__main__':

    server = make_server('127.0.0.1', 80, app)

    server.serve_forever()
