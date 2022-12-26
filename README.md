# Radox

A WSGI based Python Web Framework inspired from Flask

# Installing
```
$ pip install git+https://github.com/codeverything/radox.git
```

# Example:
```
from wsgiref.simple_server import make_server
from radox import app

app = radox()

@app.route("/")
def index():
   return "Hello Radox"
   
if __name__=='__main__':
   server = make_server('127.0.0.1',3301,app)
   server.serve_forever()
```


# Links

* Source Code - https://github.com/codeverything/radox.git
* Pypi        - https://pypi.org/project/radox/
* Issues      - https://github.com/codeverything/radox/issues
* Discord     - https://discord.gg/RnQHNAmx
