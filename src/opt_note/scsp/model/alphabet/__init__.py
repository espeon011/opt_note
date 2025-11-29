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
        self.solution = chars * max([len(s) for s in self.instance])
        return self.solution
