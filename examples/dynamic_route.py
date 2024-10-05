from __future__ import annotations

from src.main import *
from utils.srv_info import *
from wsgiref.simple_server import make_server


app = radox()


@app.route("/")
def index() -> str:
    return "Hello World"


@app.route("/home")
def index(request: str) -> str:
    return "Home Page"


@app.route('/user/<username>')
def user_profile(username: str) -> str:
    return f"Profile page for user: {username}"


if __name__=='__main__':
    server = make_server('127.0.0.1', 3301, app)
    info()
    server.serve_forever()