from src.main import *
from utils.srv_info import *
from wsgiref.simple_server import make_server

app = radox()

@app.route("/")
def index():
    return "Hello World"

@app.route("/home")
def index(request):
    return "Home Page"

if __name__=='__main__':
    server = make_server('127.0.0.1', 3301, app)
    info()
    server.serve_forever()
