
<p align="center">
<img src="/logo/logo.png"></p>

<p align="center">
  <img src="https://img.shields.io/github/license/codeverything/radox?color=FFBB00">

  <img src="https://img.shields.io/github/issues/codeverything/radox?color=EA4335">
  <img src="https://img.shields.io/pypi/v/radox.svg?color=4285F4">

  <img src="https://sonarcloud.io/api/project_badges/measure?project=codeverything_radox&metric=alert_status">

</p>

<!-- BADGIE TIME -->

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![code style: black](https://img.shields.io/badge/code_style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

<!-- END BADGIE TIME -->

Your next web framework for python web applications.

Radox is a light weight WSGI based web framework for python web applications. It provides a basic routing.

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

# Server-Info
```
Your Project is ready and serving now
WARNING!! This is a Development server don't use it on production
 -> Running server at http://127.0.0.1:3301
 -> Press Ctrl+C to exit
 ```

# Links

* Source Code - https://github.com/codeverything/radox.git
* Pypi        - https://pypi.org/project/radox/
* Issues      - https://github.com/codeverything/radox/issues
* Discord     - https://discord.gg/wDXSgZ5JRZ

License
-------



Code and documentation are available according to the MIT License (see [LICENSE](https://github.com/codeverything/radox/blob/main/LICENSE)).
