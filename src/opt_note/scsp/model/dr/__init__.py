"""
.. include:: ./README.md
"""

from collections.abc import Callable
import datetime
from .. import la_sh


def longest_suffix_index(s1: str, s2: str) -> int:
    """
    `s1[idx:]` が `s2` の部分配列となるもののうち最小の idx を返す.
    (つまり `s1[idx]` が最長となるようにする. )
    """

    next = len(s1) - 1
    for c in reversed(s2):
        if next == -1:
            break
        if s1[next] == c:
            next -= 1

    return next + 1


def solve(
    instance: list[str],
    time_limit: int | None = 60,
    deposition: Callable[[list[str]], str | None] = la_sh.solve,
    reduction: Callable[[list[str]], str | None] = la_sh.solve,
) -> str | None:
    start = datetime.datetime.now()
    if time_limit is not None:
        limit = start + datetime.timedelta(seconds=time_limit)
    else:
        limit = None

    template = deposition(instance)
    if template is None:
        return None

    solution = template

    update = True
    while update:
        update = False
        for i in range(len(solution)):
            now = datetime.datetime.now()
            if limit is not None and now >= limit:
                break
            right = solution[i + 1 :]
            left = reduction([s[: longest_suffix_index(s, right)] for s in instance])
            if left is None:
                break
            if len(left) < i + 1:
                update = True
                solution = left + right
                break
        if not update:
            break

    return solution
