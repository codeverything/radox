from __future__ import annotations

import re

from radox.main import radox


def test_init() -> None:
    app = radox()
    assert app.routes == []


def test_register_route() -> None:
    app = radox()

    @app.route("/<file>")
    def handle_file(file: str) -> str:
        return f"Requested {file!r}"

    assert app.routes[0] == (re.compile("^/(?P<file>[^/]+)$"), handle_file)
