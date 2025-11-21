"""
.. include:: ./README.md
"""

from typing import Literal
import pathlib
from .. import util

DATA_DIR = pathlib.Path(__file__).parent

ExampleFileName = Literal[
    "nucleotide_n005k010.txt",
    "nucleotide_n010k010.txt",
    "nucleotide_n010k050.txt",
    "nucleotide_n050k010.txt",
    "nucleotide_n050k050.txt",
    "nucleotide_n050k100.txt",
    "nucleotide_n100k050.txt",
    "nucleotide_n100k100.txt",
    "nucleotide_n100k500.txt",
    "protein_n005k010.txt",
    "protein_n010k010.txt",
    "protein_n010k050.txt",
    "protein_n050k010.txt",
    "protein_n050k050.txt",
    "protein_n050k100.txt",
    "protein_n100k050.txt",
    "protein_n100k100.txt",
    "protein_n100k500.txt",
    "uniform_q05n010k010-010.txt",
    "uniform_q05n010k020-020.txt",
    "uniform_q05n050k010-010.txt",
    "uniform_q05n050k020-020.txt",
    "uniform_q05n100k010-010.txt",
    "uniform_q05n100k020-020.txt",
    "uniform_q05n500k010-010.txt",
    "uniform_q05n500k020-020.txt",
    "uniform_q26n002k015-025.txt",
    "uniform_q26n004k015-025.txt",
    "uniform_q26n008k015-025.txt",
    "uniform_q26n016k015-025.txt",
    "uniform_q26n032k015-025.txt",
    "uniform_q26n064k015-025.txt",
]


def load(filename: ExampleFileName) -> list[str]:
    """
    サンプルデータセット読み込み.
    サンプルファイル名は https://github.com/espeon011/opt_note/tree/main/src/opt_note/scsp/example を参照.
    """

    filepath = DATA_DIR / filename
    return util.parse(filepath)
