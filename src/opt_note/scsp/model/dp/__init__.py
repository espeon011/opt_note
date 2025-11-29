"""
.. include:: ./README.md
"""

from dataclasses import dataclass
import itertools


@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(self, *args, **kwargs) -> str | None:
        dp: dict[tuple[int, ...], tuple[int, tuple[int, ...] | None]] = {
            (0,) * len(self.instance): (0, None)
        }
        for transversal in itertools.product(
            *[range(len(s) + 1) for s in self.instance]
        ):
            if transversal in dp:
                continue

            end_chars = set(
                s[t - 1] for s, t in zip(self.instance, transversal) if t > 0
            )
            pretransversals = [
                tuple(
                    t - 1 if t > 0 and s[t - 1] == c else t
                    for s, t in zip(self.instance, transversal)
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

        solution: str = ""
        left_transversal: tuple[int, ...] = (0,) * len(self.instance)
        right_transversal: tuple[int, ...] = tuple(len(s) for s in self.instance)
        current_transversal = right_transversal
        while current_transversal != left_transversal:
            pretransversal = dp[current_transversal][1]
            assert pretransversal is not None
            c = None
            for s, t1, t2 in zip(self.instance, current_transversal, pretransversal):
                if t1 == t2 + 1:
                    c = s[t2]
                    break
            assert c is not None
            solution += c
            current_transversal = pretransversal

        self.solution = solution[::-1]
        self.best_bound = float(len(self.solution))
        return self.solution
