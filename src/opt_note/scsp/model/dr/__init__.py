"""
.. include:: ./README.md
"""

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


def original_reduction(
    instance: list[str],
    template: str,
    time_limit: int | None = 60,
    solve_func: Callable[[list[str]], str | None] = la_sh.solve,
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
    ) -> str | None: ...


def solve(
    instance: list[str],
    time_limit: int | None = 60,
    deposition: DepositionFuncType = la_sh.solve,
    reduction: ReductionFuncType = original_reduction,
) -> str | None:
    template = deposition(instance)
    if template is None:
        return None

    return reduction(instance, template, time_limit)
