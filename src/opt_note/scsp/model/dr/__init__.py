"""
.. include:: ./README.md
"""

from dataclasses import dataclass
from collections.abc import Callable
from typing import Protocol
import datetime
from .. import la_sh


def longest_suffix_index(s1: str, s2: str) -> int:
    """
    `s1[idx:]` が `s2` の部分配列となるもののうち最小の idx を返す.
    (つまり `s1[idx:]` が最長となるようにする. )
    """

    next = len(s1) - 1
    for c in reversed(s2):
        if next == -1:
            break
        if s1[next] == c:
            next -= 1

    return next + 1


def solve_func_default(instance: list[str]) -> str | None:
    return la_sh.Model(instance).solve()


def original_deposition(instance: list[str]) -> str | None:
    return la_sh.Model(instance).solve()


def original_reduction(
    instance: list[str],
    template: str,
    time_limit: int | None = 60,
    *args,
    solve_func: Callable[[list[str]], str | None] = solve_func_default,
    **kwargs,
) -> str | None:
    start = datetime.datetime.now()
    if time_limit is not None:
        limit = start + datetime.timedelta(seconds=time_limit)
    else:
        limit = None

    update = True
    while update:
        update = False
        for i in range(len(template)):
            now = datetime.datetime.now()
            if limit is not None and now >= limit:
                break

            right = template[i + 1 :]

            remaining_prefixes = list(
                filter(
                    lambda s: len(s) > 0,
                    [s[: longest_suffix_index(s, right)] for s in instance],
                )
            )
            if len(remaining_prefixes) == 0:
                left = ""
            else:
                left = solve_func(remaining_prefixes)

            if left is None:
                break

            if len(left) < i + 1:
                update = True
                template = left + right
                break

        if not update:
            break

    return template


class DepositionFuncType(Protocol):
    def __call__(self, instance: list[str]) -> str | None: ...


class ReductionFuncType(Protocol):
    def __call__(
        self,
        instance: list[str],
        template: str,
        time_limit: int | None = 60,
        log: bool = False,
    ) -> str | None: ...


@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(
        self,
        time_limit: int | None = 60,
        log: bool = False,
        deposition: DepositionFuncType = original_deposition,
        reduction: ReductionFuncType = original_reduction,
        *args,
        **kwargs,
    ) -> str | None:
        template = deposition(self.instance)
        if template is None:
            return None
        self.solution = reduction(self.instance, template, time_limit, log)
        return self.solution
