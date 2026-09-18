"""
SCSP を解くアルゴリズム, ヒューリスティック, 数理最適化モデル.
"""

import importlib
from types import ModuleType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import (
        alphabet,
        alphabet_reduction,
        automaton_cpsat,
        descending,
        didp,
        didp_scs3,
        dp,
        dr,
        dr_alphabet_cpsat,
        dr_alphabet_hexaly,
        ibs_scs,
        la_sh,
        la_sw,
        linear1_cpsat,
        linear1_highs,
        linear1_scip,
        linear2_cpsat,
        linear2_highs,
        linear2_scip,
        mm,
        tsp_cpsat,
        tsp_hexaly,
        wmm,
        wmm_hexaly,
        wmm_hexaly_init,
    )

__all__ = [
    "alphabet",
    "alphabet_reduction",
    "automaton_cpsat",
    "descending",
    "didp",
    "didp_scs3",
    "dp",
    "dr",
    "dr_alphabet_cpsat",
    "dr_alphabet_hexaly",
    "ibs_scs",
    "la_sh",
    "la_sw",
    "linear1_cpsat",
    "linear1_highs",
    "linear1_scip",
    "linear2_cpsat",
    "linear2_highs",
    "linear2_scip",
    "mm",
    "tsp_cpsat",
    "tsp_hexaly",
    "wmm",
    "wmm_hexaly",
    "wmm_hexaly_init",
]


def __getattr__(name: str) -> ModuleType:
    if name not in __all__:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return importlib.import_module(f".{name}", __name__)


def __dir__() -> list[str]:
    return sorted(__all__)
