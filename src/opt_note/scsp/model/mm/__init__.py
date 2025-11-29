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
        indices = [0 for _ in self.instance]
        solution = ""

        while not all(idx == len(s) for idx, s in zip(indices, self.instance)):
            fronts = [s[idx] for idx, s in zip(indices, self.instance) if idx < len(s)]
            counts = [fronts.count(c) for c in chars]
            next_char = chars[counts.index(max(counts))]

            solution += next_char
            for jdx in range(len(self.instance)):
                s = self.instance[jdx]
                idx = indices[jdx]
                if idx < len(s) and s[idx] == next_char:
                    indices[jdx] += 1

        self.solution = solution
        return self.solution
