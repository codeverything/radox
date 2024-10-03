import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import *
from wsgiref.simple_server import make_server

app = Radox()

@app.route("/")
def index():
    return "Hello World"

@app.route("/home")
def home():
    return "Home Page"

def info():
    print("Server running at http://127.0.0.1:3301")

if __name__ == '__main__':
    server = make_server('127.0.0.1', 3301, app)
    info()
    server.serve_forever()
