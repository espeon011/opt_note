"""
.. include:: ./README.md
"""

from dataclasses import dataclass
from .. import wmm_hexaly


@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(
        self, time_limit: int | None = 60, log: bool = False, *args, **kwargs
    ) -> str | None:
        initial_weights = [
            [len(s) - cidx for cidx, _ in enumerate(s)] for s in self.instance
        ]
        model = wmm_hexaly.Model(self.instance)
        self.solution = model.solve(time_limit, log, initial_weights)
        return self.solution
