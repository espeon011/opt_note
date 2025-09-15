"""
.. include:: ./README.md
"""

import itertools


def solve(instance: list[str]) -> str:
    dp: dict[tuple[int, ...], tuple[int, tuple[int, ...] | None]] = {
        (0,) * len(instance): (0, None)
    }
    for transversal in itertools.product(*[range(len(s) + 1) for s in instance]):
        if transversal in dp:
            continue

        end_chars = set(s[t - 1] for s, t in zip(instance, transversal) if t > 0)
        pretransversals = [
            tuple(
                t - 1 if t > 0 and s[t - 1] == c else t
                for s, t in zip(instance, transversal)
            )
            for c in end_chars
        ]

        min_transversal = pretransversals[0]
        min_length = dp[min_transversal][0]
        for pretransversal in pretransversals:
            if dp[pretransversal][0] < min_length:
                min_transversal = pretransversal
                min_length = dp[pretransversal][0]

        dp[transversal] = (min_length + 1, min_transversal)

    solution = ""
    left_transversal = (0,) * len(instance)
    right_transversal = tuple(len(s) for s in instance)
    current_transversal = right_transversal
    while current_transversal != left_transversal:
        pretransversal = dp[current_transversal][1]
        assert pretransversal is not None
        c = None
        for s, t1, t2 in zip(instance, current_transversal, pretransversal):
            if t1 == t2 + 1:
                c = s[t2]
                break
        assert c is not None
        solution += c
        current_transversal = pretransversal

    return solution[::-1]
