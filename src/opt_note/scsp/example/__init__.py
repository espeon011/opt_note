"""
.. include:: ./README.md
"""

import pathlib
from .. import util

DATA_DIR = pathlib.Path(__file__).parent


def load(filename: str) -> list[str]:
    """
    サンプルデータセット読み込み.
    サンプルファイル名は https://github.com/espeon011/opt_note/tree/main/src/opt_note/scsp/example を参照.
    """

    filepath = DATA_DIR / filename
    return util.parse(filepath)
