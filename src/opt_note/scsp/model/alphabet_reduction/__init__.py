"""
.. include:: ./README.md
"""

from dataclasses import dataclass


@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(self, *args, **kwargs) -> str | None:
        chars = "".join(sorted(list(set("".join(self.instance)))))
        solution = ""

        for i in range(max([len(s) for s in self.instance])):
            used = [False for _ in chars]
            for s in self.instance:
                if i >= len(s):
                    continue
                used[chars.index(s[i])] = True

            for c, u in zip(chars, used):
                if u:
                    solution += c

        self.solution = solution
        return self.solution
