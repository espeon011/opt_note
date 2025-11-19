"""
.. include:: ./README.md
"""

import hexaly.optimizer


class Model:
    def __init__(self, instance: list[str]):
        self.instance: list[str] = instance
        self.status: hexaly.optimizer.HxSolutionStatus | None = None
        self.solution: str | None = None
        self.best_bound: int = 0

    def solve(self, time_limit: int | None = 60, log: bool = False) -> "Model":
        with hexaly.optimizer.HexalyOptimizer() as hxoptimizer:
            assert isinstance(hxoptimizer.model, hexaly.optimizer.HxModel)
            assert isinstance(hxoptimizer.param, hexaly.optimizer.HxParam)
            hxmodel: hexaly.optimizer.HxModel = hxoptimizer.model
            hxparam: hexaly.optimizer.HxParam = hxoptimizer.param

            chars: str = "".join(sorted(list(set("".join(self.instance)))))
            max_len = len(chars) * max(len(s) for s in self.instance)

            cvars = [
                [hxmodel.int(0, max_len // len(chars) - 1) for c in s]
                for s in self.instance
            ]

            for sidx, s in enumerate(self.instance):
                for cidx, c in enumerate(s):
                    if cidx == 0:
                        continue
                    prev_c = s[cidx - 1]
                    if chars.index(prev_c) < chars.index(c):
                        hxmodel.constraint(cvars[sidx][cidx - 1] <= cvars[sidx][cidx])
                    else:
                        hxmodel.constraint(cvars[sidx][cidx - 1] < cvars[sidx][cidx])

            embeds = [
                hxmodel.array(
                    [len(chars) * x + chars.index(c) for x, c in zip(cvar, s)]
                )
                for cvar, s in zip(cvars, self.instance)
            ]

            hxmodel.minimize(hxmodel.count(hxmodel.union(embeds)))

            hxmodel.close()

            if time_limit is not None:
                hxparam.time_limit = time_limit
            hxparam.verbosity = 1 if log else 0

            hxoptimizer.solve()

            assert isinstance(hxoptimizer.solution, hexaly.optimizer.HxSolution)
            hxsolution: hexaly.optimizer.HxSolution = hxoptimizer.solution

            self.status = hxsolution.status
            self.best_bound = hxsolution.get_objective_bound(0)

            if self.status in {
                hexaly.optimizer.HxSolutionStatus.OPTIMAL,
                hexaly.optimizer.HxSolutionStatus.FEASIBLE,
            }:
                solution = ""
                cvars_val: list[list[int]] = [
                    [x.value * len(chars) + chars.index(c) for x, c in zip(cvar, s)]
                    for cvar, s in zip(cvars, self.instance)
                ]
                for idx in sorted(list(set(sum(cvars_val, [])))):
                    solution += chars[idx % len(chars)]
                self.solution = solution

        return self

    def to_solution(self) -> str | None:
        return self.solution


def solve(
    instance: list[str], time_limit: int | None = 60, log: bool = False
) -> str | None:
    return Model(instance).solve(time_limit, log).to_solution()
