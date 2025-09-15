"""
.. include:: ./README.md
"""

import pathlib
from .. import util

DATA_DIR = pathlib.Path(__file__).parent


def load(filename: str) -> list[str]:
    filepath = DATA_DIR / filename
    return util.parse(filepath)
