from __future__ import annotations

import sys
from signal import SIGINT, signal
from typing import TYPE_CHECKING

import simple_colors

if TYPE_CHECKING:
    from types import FrameType


def handler(sig: int, frame: FrameType | None) -> None:
    sys.exit(0)


def info() -> None:
    signal(SIGINT, handler)
    print("Compiled Successfully   " + simple_colors.green("DONE"))
    print("Your Project is ready and serving now")
    print(simple_colors.red("WARNING!! This is a Development server don't use it on production"))
    print(" -> Running server at http://127.0.0.1:3301")
    print(" -> Press Ctrl+C to exit")
